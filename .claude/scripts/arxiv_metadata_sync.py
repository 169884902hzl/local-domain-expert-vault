"""Sync and query a local arXiv metadata mirror via OAI-PMH."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import random
import re
import sqlite3
import sys
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from arxiv_ranker import ArxivPaper, DEFAULT_QUERIES
from arxiv_ranker import rank_papers
from kb_common import safe_print, vault_path


OAI_BASE = "https://oaipmh.arxiv.org/oai"
NS = {
    "oai": "http://www.openarchives.org/OAI/2.0/",
    "arxiv": "http://arxiv.org/OAI/arXiv/",
}
DEFAULT_SETS = ["cs", "stat"]
DEFAULT_DB = vault_path("projects", "arxiv-daily", "metadata", "arxiv_metadata.sqlite")
LOCK_PATH = vault_path("projects", "arxiv-daily", "metadata", "arxiv_metadata.lock")
STALE_AFTER_HOURS = 48
DEFAULT_INCREMENTAL_OVERLAP_DAYS = 3


@contextmanager
def file_lock(path: Path, *, timeout: int = 180):
    path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + timeout
    handle = None
    while time.time() < deadline:
        try:
            handle = path.open("x", encoding="utf-8")
            handle.write(f"{time.time()}\n")
            handle.flush()
            break
        except FileExistsError:
            try:
                age = time.time() - path.stat().st_mtime
                if age > timeout * 2:
                    path.unlink()
                    continue
            except OSError:
                pass
            time.sleep(2)
    if handle is None:
        raise TimeoutError(f"could not acquire lock: {path}")
    try:
        yield
    finally:
        handle.close()
        try:
            path.unlink()
        except OSError:
            pass


def connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    init_db(conn)
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors_json TEXT NOT NULL,
            summary TEXT NOT NULL,
            published TEXT NOT NULL,
            updated TEXT NOT NULL,
            url TEXT NOT NULL,
            pdf_url TEXT NOT NULL,
            categories_json TEXT NOT NULL,
            primary_category TEXT NOT NULL,
            doi TEXT NOT NULL,
            journal_ref TEXT NOT NULL,
            comment TEXT NOT NULL,
            last_seen_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sync_state (
            scope TEXT PRIMARY KEY,
            last_success_until TEXT NOT NULL,
            resumption_token TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            status TEXT NOT NULL,
            error TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_papers_updated ON papers(updated)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_papers_published ON papers(published)")
    conn.commit()


def _clean(text: str) -> str:
    return " ".join((text or "").split())


def _node_text(parent: ET.Element, path: str) -> str:
    node = parent.find(path, NS)
    return "" if node is None or node.text is None else _clean(node.text)


def _parse_oai_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        if len(value) == 10:
            return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_oai_date(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).date().isoformat()


def _date_from_oai_string(value: str) -> datetime | None:
    dt = _parse_oai_date(value)
    if not dt:
        return None
    return dt.astimezone(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)


def _arxiv_id_from_identifier(identifier: str) -> str:
    return identifier.removeprefix("oai:arXiv.org:").strip()


def _paper_from_record(record: ET.Element) -> ArxivPaper | None:
    header = record.find("oai:header", NS)
    metadata = record.find("oai:metadata/arxiv:arXiv", NS)
    if header is None or metadata is None:
        return None
    identifier = _node_text(header, "oai:identifier")
    arxiv_id = _arxiv_id_from_identifier(identifier)
    title = _node_text(metadata, "arxiv:title")
    if not arxiv_id or not title:
        return None
    authors = []
    for author in metadata.findall("arxiv:authors/arxiv:author", NS):
        keyname = _node_text(author, "arxiv:keyname")
        forenames = _node_text(author, "arxiv:forenames")
        name = _clean(f"{forenames} {keyname}") if forenames else keyname
        if name:
            authors.append(name)
    categories = _node_text(metadata, "arxiv:categories").split()
    primary = categories[0] if categories else ""
    doi = _node_text(metadata, "arxiv:doi")
    arxiv_url = f"http://arxiv.org/abs/{arxiv_id}"
    return ArxivPaper(
        arxiv_id=arxiv_id,
        title=title,
        authors=authors,
        summary=_node_text(metadata, "arxiv:abstract"),
        published=_node_text(metadata, "arxiv:created"),
        updated=_node_text(header, "oai:datestamp") or _node_text(metadata, "arxiv:created"),
        url=arxiv_url,
        pdf_url=f"http://arxiv.org/pdf/{arxiv_id}",
        categories=categories,
        primary_category=primary,
        doi=doi,
        journal_ref=_node_text(metadata, "arxiv:journal-ref"),
        comment=_node_text(metadata, "arxiv:comments"),
        query_sources=["oai-pmh"],
    )


def upsert_papers(conn: sqlite3.Connection, papers: list[ArxivPaper]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn.executemany(
        """
        INSERT INTO papers (
            arxiv_id, title, authors_json, summary, published, updated, url, pdf_url,
            categories_json, primary_category, doi, journal_ref, comment, last_seen_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(arxiv_id) DO UPDATE SET
            title=excluded.title,
            authors_json=excluded.authors_json,
            summary=excluded.summary,
            published=excluded.published,
            updated=excluded.updated,
            url=excluded.url,
            pdf_url=excluded.pdf_url,
            categories_json=excluded.categories_json,
            primary_category=excluded.primary_category,
            doi=excluded.doi,
            journal_ref=excluded.journal_ref,
            comment=excluded.comment,
            last_seen_at=excluded.last_seen_at
        """,
        [
            (
                paper.arxiv_id,
                paper.title,
                json.dumps(paper.authors, ensure_ascii=False),
                paper.summary,
                paper.published,
                paper.updated,
                paper.url,
                paper.pdf_url,
                json.dumps(paper.categories, ensure_ascii=False),
                paper.primary_category,
                paper.doi,
                paper.journal_ref,
                paper.comment,
                now,
            )
            for paper in papers
        ],
    )
    conn.commit()


def update_state(conn: sqlite3.Connection, scope: str, *, until: str, token: str, status: str, error: str = "") -> None:
    conn.execute(
        """
        INSERT INTO sync_state(scope, last_success_until, resumption_token, updated_at, status, error)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(scope) DO UPDATE SET
            last_success_until=excluded.last_success_until,
            resumption_token=excluded.resumption_token,
            updated_at=excluded.updated_at,
            status=excluded.status,
            error=excluded.error
        """,
        (scope, until, token, datetime.now(timezone.utc).isoformat(), status, error),
    )
    conn.commit()


def mirror_status(conn: sqlite3.Connection) -> dict[str, Any]:
    total = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    state_rows = conn.execute("SELECT * FROM sync_state ORDER BY updated_at DESC").fetchall()
    last_success = ""
    for row in state_rows:
        if row["status"] == "success":
            last_success = row["updated_at"]
            break
    stale = True
    dt = _parse_oai_date(last_success)
    if dt:
        stale = datetime.now(timezone.utc) - dt > timedelta(hours=STALE_AFTER_HOURS)
    return {
        "records_total": int(total),
        "last_success_at": last_success,
        "stale": stale,
        "states": [dict(row) for row in state_rows],
    }


def _request_oai(params: dict[str, str], *, timeout: int, retries: int) -> ET.Element:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            url = f"{OAI_BASE}?{urllib.parse.urlencode(params)}"
            req = urllib.request.Request(url, headers={"User-Agent": "hust-literature-vault/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return ET.fromstring(resp.read())
        except Exception as exc:
            last_error = exc
            if attempt >= retries:
                raise
            time.sleep((2**attempt) * 5 + random.uniform(0, 3))
    raise RuntimeError(f"OAI request failed: {last_error}")


def sync_metadata(
    *,
    days_back: int,
    incremental: bool,
    overlap_days: int,
    sets: list[str],
    max_pages: int,
    dry_run: bool,
    timeout: int,
    retries: int,
    delay: float,
    db_path: Path = DEFAULT_DB,
) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    bootstrap_from = now - timedelta(days=days_back)
    until_date = _format_oai_date(now)
    total_seen = 0
    total_written = 0
    errors: list[str] = []
    scopes: list[dict[str, str]] = []
    conn = connect(db_path)
    with file_lock(LOCK_PATH):
        for set_name in sets:
            scope = f"set:{set_name}"
            state = conn.execute("SELECT * FROM sync_state WHERE scope=?", (scope,)).fetchone()
            token = "" if state is None else str(state["resumption_token"] or "")
            state_until = "" if state is None else str(state["last_success_until"] or "")
            if incremental and state_until and not token:
                state_from = _date_from_oai_string(state_until)
                from_dt = state_from - timedelta(days=overlap_days) if state_from else bootstrap_from
            else:
                from_dt = bootstrap_from
            from_date = _format_oai_date(from_dt)
            scope_status = "token_resume" if token else ("incremental" if incremental and state_until else "bootstrap")
            scope_error_start = len(errors)
            pages = 0
            while True:
                params = {"verb": "ListRecords"}
                if token:
                    params["resumptionToken"] = token
                else:
                    params.update({"metadataPrefix": "arXiv", "from": from_date, "until": until_date, "set": set_name})
                try:
                    root = _request_oai(params, timeout=timeout, retries=retries)
                except Exception as exc:
                    errors.append(f"{scope}:{exc}")
                    if not dry_run and (token or state is None):
                        update_state(conn, scope, until=state_until or from_date, token=token, status="failed", error=str(exc))
                    break
                records = root.findall(".//oai:ListRecords/oai:record", NS)
                papers = [paper for record in records if (paper := _paper_from_record(record))]
                total_seen += len(papers)
                if not dry_run and papers:
                    upsert_papers(conn, papers)
                    total_written += len(papers)
                elif dry_run:
                    total_written += len(papers)
                token_node = root.find(".//oai:resumptionToken", NS)
                token = "" if token_node is None or not token_node.text else token_node.text.strip()
                pages += 1
                if max_pages and pages >= max_pages:
                    break
                if not token:
                    break
                if delay > 0:
                    time.sleep(delay)
            scope_errors = errors[scope_error_start:]
            state_status = "partial" if token else ("failed" if scope_errors else "success")
            if not dry_run and not scope_errors:
                update_state(conn, scope, until=until_date, token=token, status=state_status)
            scopes.append(
                {
                    "scope": scope,
                    "mode": scope_status,
                    "from": from_date,
                    "until": until_date,
                    "status": state_status,
                    "resumption_token": token,
                }
            )
    status = mirror_status(conn)
    conn.close()
    return {
        "dry_run": dry_run,
        "days_back": days_back,
        "incremental": incremental,
        "overlap_days": overlap_days,
        "sets": sets,
        "scopes": scopes,
        "seen": total_seen,
        "written": 0 if dry_run else total_written,
        "errors": errors,
        "mirror_records_total": status["records_total"],
        "mirror_last_success_at": status["last_success_at"],
        "mirror_stale": status["stale"],
    }


def _query_terms_match(text: str, query: str) -> bool:
    quoted = [term.lower() for term in re.findall(r'"([^"]+)"', query)]
    if quoted:
        return any(term in text for term in quoted)
    terms = [term.lower() for term in re.findall(r"[A-Za-z][A-Za-z0-9+-]+", query) if term.lower() not in {"all", "and", "or", "cat"}]
    return any(term in text for term in terms)


def _row_to_paper(row: sqlite3.Row) -> ArxivPaper:
    return ArxivPaper(
        arxiv_id=row["arxiv_id"],
        title=row["title"],
        authors=json.loads(row["authors_json"] or "[]"),
        summary=row["summary"],
        published=row["published"],
        updated=row["updated"],
        url=row["url"],
        pdf_url=row["pdf_url"],
        categories=json.loads(row["categories_json"] or "[]"),
        primary_category=row["primary_category"],
        doi=row["doi"],
        journal_ref=row["journal_ref"],
        comment=row["comment"],
        query_sources=["mirror"],
    )


def query_mirror(
    *,
    queries: list[str] | None = None,
    days_back: int,
    max_candidates: int,
    as_of: datetime | None = None,
    db_path: Path = DEFAULT_DB,
) -> tuple[list[ArxivPaper], dict[str, Any]]:
    conn = connect(db_path)
    reference_time = as_of or datetime.now(timezone.utc)
    cutoff = reference_time - timedelta(days=days_back)
    rows = conn.execute("SELECT * FROM papers").fetchall()
    by_id: dict[str, ArxivPaper] = {}
    query_list = queries or DEFAULT_QUERIES
    for row in rows:
        paper = _row_to_paper(row)
        dt = _parse_oai_date(paper.published) or _parse_oai_date(paper.updated)
        if dt and dt < cutoff:
            continue
        text = " ".join(
            [
                paper.title,
                paper.summary,
                paper.comment,
                paper.journal_ref,
                paper.primary_category,
                " ".join(paper.categories),
            ]
        ).lower()
        matched = [query for query in query_list if _query_terms_match(text, query)]
        if not matched:
            continue
        paper.query_sources = matched
        by_id[paper.arxiv_id] = paper
    status = mirror_status(conn)
    conn.close()
    status.update({"source": "mirror_stale" if status["stale"] else "mirror"})
    ranked = rank_papers(list(by_id.values()))
    return [item.paper for item in ranked[: max_candidates * 3]], status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days-back", type=int, default=480, help="Bootstrap or manual refresh window when no incremental state is available.")
    parser.add_argument("--incremental", action="store_true", help="Sync from the last successful OAI date with a small overlap instead of rescanning --days-back.")
    parser.add_argument("--overlap-days", type=int, default=DEFAULT_INCREMENTAL_OVERLAP_DAYS, help="Days to re-check before the last successful OAI date in --incremental mode.")
    parser.add_argument("--set", dest="sets", action="append", help="OAI set to sync; repeatable. Defaults to cs and stat.")
    parser.add_argument("--max-pages", type=int, default=0, help="Limit pages per set for smoke tests; 0 means unlimited.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--delay", type=float, default=3.5)
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.status:
        conn = connect(DEFAULT_DB)
        safe_print(json.dumps(mirror_status(conn), ensure_ascii=False, indent=2))
        conn.close()
        return 0
    result = sync_metadata(
        days_back=args.days_back,
        incremental=args.incremental,
        overlap_days=args.overlap_days,
        sets=args.sets or DEFAULT_SETS,
        max_pages=args.max_pages,
        dry_run=args.dry_run,
        timeout=args.timeout,
        retries=args.retries,
        delay=args.delay,
    )
    safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not result["errors"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
