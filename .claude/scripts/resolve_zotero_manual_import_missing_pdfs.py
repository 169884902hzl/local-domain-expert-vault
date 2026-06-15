#!/usr/bin/env python3
"""Resolve missing PDFs for the cleaned 2026-06-04 manual Zotero import batch.

Default mode is dry-run. ``--apply --yes`` attaches only validated PDF URLs to
existing Zotero items. The resolver fails closed: no PDF is attached unless a
source URL downloads as a real PDF and title matching is high confidence.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from arxiv_ranker import ArxivPaper, RankedPaper
from zotero_import import _env, _web_user_id, create_pdf_attachment_web


DEFAULT_QUEUE = Path(
    "output/import_runs/20260604-172607-awesome-embodied-full-import/"
    "reading_plan_20260613/needs_pdf_before_strict_read.jsonl"
)
DEFAULT_OUT_DIR = Path(
    "output/import_runs/20260604-172607-awesome-embodied-full-import/"
    "repair_audit/pdf_resolver"
)
DEFAULT_COLLECTION = "ZJK4PK4G"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}


@dataclass
class PdfCandidate:
    source: str
    pdf_url: str
    title: str
    authors: list[str]
    abstract: str
    year: str
    arxiv_id: str = ""
    score: float = 0.0


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_title(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def title_score(left: str, right: str) -> float:
    left_norm = normalize_title(left)
    right_norm = normalize_title(right)
    if not left_norm or not right_norm:
        return 0.0
    return SequenceMatcher(None, left_norm, right_norm).ratio()


def fetch_text(url: str, *, timeout: int = 45) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/json,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "codex-zotero-pdf-resolver/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def absolutize(url: str, base: str) -> str:
    return urllib.parse.urljoin(base, html.unescape(url))


def candidate_pdf_links_from_page(row: dict[str, Any]) -> list[str]:
    url = str(row.get("url") or "").strip()
    if not url:
        return []
    page = fetch_text(url)
    links: list[str] = []
    for match in re.finditer(r"href=[\"']([^\"']+)[\"']", page, flags=re.IGNORECASE):
        href = absolutize(match.group(1), url)
        lowered = href.lower()
        if lowered.endswith(".pdf") or "/pdf" in lowered or "openreview.net/pdf" in lowered:
            links.append(href)
    seen: set[str] = set()
    unique: list[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique.append(link)
    return unique


def verify_pdf_url(pdf_url: str, *, timeout: int = 45) -> tuple[bool, int, str]:
    req = urllib.request.Request(
        pdf_url,
        headers={"Accept": "application/pdf,*/*", "User-Agent": "codex-zotero-pdf-resolver/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read(4096)
            length = int(resp.headers.get("Content-Length") or 0)
    except urllib.error.HTTPError as exc:
        return False, 0, f"HTTP_{exc.code}"
    except Exception as exc:  # noqa: BLE001 - reason is reported per candidate.
        return False, 0, f"{type(exc).__name__}:{str(exc)[:120]}"
    if data.startswith(b"%PDF"):
        return True, length, "ok"
    return False, length, "not_pdf"


def arxiv_authors(entry: ET.Element) -> list[str]:
    authors: list[str] = []
    for author in entry.findall("atom:author", ATOM):
        name_node = author.find("atom:name", ATOM)
        name = " ".join((name_node.text or "").split()) if name_node is not None else ""
        if name:
            authors.append(name)
    return authors


def arxiv_id_from_entry(entry: ET.Element) -> str:
    value = (entry.findtext("atom:id", "", ATOM) or "").strip()
    match = re.search(r"/abs/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?$", value)
    return match.group(1) if match else ""


def arxiv_pdf_url(entry: ET.Element, arxiv_id: str) -> str:
    for link in entry.findall("atom:link", ATOM):
        if link.attrib.get("title") == "pdf" and link.attrib.get("href"):
            return link.attrib["href"]
    return f"https://arxiv.org/pdf/{arxiv_id}"


def arxiv_exact_candidate(row: dict[str, Any]) -> tuple[PdfCandidate | None, list[str]]:
    title = str(row.get("title") or "")
    query = urllib.parse.urlencode({"search_query": f'ti:"{title}"', "start": "0", "max_results": "5"})
    url = f"https://export.arxiv.org/api/query?{query}"
    errors: list[str] = []
    try:
        root = ET.fromstring(
            urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": "codex-zotero-pdf-resolver/1.0"}),
                timeout=45,
            ).read()
        )
    except Exception as exc:  # noqa: BLE001 - reason is reported per row.
        return None, [f"arxiv_query:{type(exc).__name__}:{str(exc)[:120]}"]
    best: PdfCandidate | None = None
    for entry in root.findall("atom:entry", ATOM):
        found_title = " ".join((entry.findtext("atom:title", "", ATOM) or "").split())
        score = title_score(title, found_title)
        arxiv_id = arxiv_id_from_entry(entry)
        pdf_url = arxiv_pdf_url(entry, arxiv_id) if arxiv_id else ""
        if score >= 0.94 and pdf_url:
            abstract = " ".join((entry.findtext("atom:summary", "", ATOM) or "").split())
            candidate = PdfCandidate(
                source="arxiv_title_exact",
                pdf_url=pdf_url,
                title=found_title,
                authors=arxiv_authors(entry),
                abstract=abstract,
                year=(entry.findtext("atom:published", "", ATOM) or "")[:4],
                arxiv_id=arxiv_id,
                score=score,
            )
            if best is None or candidate.score > best.score:
                best = candidate
        else:
            errors.append(f"arxiv_low_match:{score:.3f}:{found_title[:120]}")
    return best, errors


def semantic_scholar_candidate(row: dict[str, Any]) -> tuple[PdfCandidate | None, list[str]]:
    title = str(row.get("title") or "")
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(
        {"query": title, "limit": "5", "fields": "title,authors,abstract,year,url,externalIds,openAccessPdf"}
    )
    errors: list[str] = []
    try:
        payload = json.loads(fetch_text(url))
    except urllib.error.HTTPError as exc:
        return None, [f"s2_http_{exc.code}"]
    except Exception as exc:  # noqa: BLE001
        return None, [f"s2_query:{type(exc).__name__}:{str(exc)[:120]}"]
    best: PdfCandidate | None = None
    for paper in payload.get("data") or []:
        found_title = str(paper.get("title") or "")
        score = title_score(title, found_title)
        oa = paper.get("openAccessPdf") or {}
        pdf_url = str(oa.get("url") or "")
        external = paper.get("externalIds") or {}
        arxiv_id = str(external.get("ArXiv") or "")
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        if score >= 0.94 and pdf_url:
            candidate = PdfCandidate(
                source="semantic_scholar_exact",
                pdf_url=pdf_url,
                title=found_title,
                authors=[str(author.get("name") or "") for author in paper.get("authors", []) if author.get("name")],
                abstract=str(paper.get("abstract") or ""),
                year=str(paper.get("year") or ""),
                arxiv_id=arxiv_id,
                score=score,
            )
            if best is None or candidate.score > best.score:
                best = candidate
        else:
            errors.append(f"s2_low_match_or_no_pdf:{score:.3f}:{found_title[:120]}")
    return best, errors


def direct_page_candidate(row: dict[str, Any]) -> tuple[PdfCandidate | None, list[str]]:
    errors: list[str] = []
    for link in candidate_pdf_links_from_page(row):
        ok, size, reason = verify_pdf_url(link)
        if ok:
            return (
                PdfCandidate(
                    source="venue_page_pdf_link",
                    pdf_url=link,
                    title=str(row.get("title") or ""),
                    authors=[],
                    abstract="",
                    year="2026",
                    score=1.0,
                ),
                errors,
            )
        errors.append(f"page_link_failed:{reason}:{link}")
    return None, errors


def resolve_candidate(row: dict[str, Any], *, use_semantic_scholar: bool) -> tuple[PdfCandidate | None, list[str]]:
    errors: list[str] = []
    for resolver in [direct_page_candidate, arxiv_exact_candidate]:
        candidate, resolver_errors = resolver(row)
        errors.extend(resolver_errors)
        if candidate:
            ok, size, reason = verify_pdf_url(candidate.pdf_url)
            if ok:
                return candidate, errors
            errors.append(f"verified_pdf_failed:{reason}:{candidate.pdf_url}")
    if use_semantic_scholar:
        candidate, resolver_errors = semantic_scholar_candidate(row)
        errors.extend(resolver_errors)
        if candidate:
            ok, size, reason = verify_pdf_url(candidate.pdf_url)
            if ok:
                return candidate, errors
            errors.append(f"verified_pdf_failed:{reason}:{candidate.pdf_url}")
    return None, errors


def ranked_from_candidate(row: dict[str, Any], candidate: PdfCandidate) -> RankedPaper:
    key = str(row.get("zotero_key") or "paper")
    arxiv_id = candidate.arxiv_id or f"icml2026-{key}"
    paper = ArxivPaper(
        arxiv_id=arxiv_id,
        title=candidate.title or str(row.get("title") or ""),
        authors=candidate.authors,
        summary=candidate.abstract,
        published=candidate.year,
        updated="",
        url=str(row.get("url") or ""),
        pdf_url=candidate.pdf_url,
        categories=[],
        primary_category="",
        doi="",
        journal_ref="",
        comment="",
        query_sources=["resolve_zotero_manual_import_missing_pdfs", candidate.source],
    )
    return RankedPaper(
        paper=paper,
        quality_score=0,
        decision="manual_import_pdf_resolved",
        reasons=[candidate.source],
        matched_terms=[],
        penalties=[],
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--old-key", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--use-semantic-scholar", action="store_true")
    parser.add_argument("--request-delay-seconds", type=float, default=1.0)
    args = parser.parse_args(argv)

    if args.apply and not args.yes:
        parser.error("--apply requires --yes")

    rows = read_jsonl(args.queue)
    if args.old_key:
        rows = [row for row in rows if row.get("zotero_key") == args.old_key]
    if args.limit:
        rows = rows[: args.limit]

    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    plan_path = args.out_dir / f"pdf_resolver_plan_{run_id}.jsonl"
    summary_path = args.out_dir / f"pdf_resolver_summary_{run_id}.json"
    summary: dict[str, Any] = {
        "created_at": now_iso(),
        "mode": "apply" if args.apply else "dry_run",
        "selected_rows": len(rows),
        "resolved_candidates": 0,
        "apply_created_or_exists": 0,
        "apply_failed": 0,
        "skipped": 0,
        "plan_path": str(plan_path),
    }
    api_key = _env("ZOTERO_API_KEY")
    user_id = _web_user_id(args.collection) if args.apply else ""
    if args.apply and (not api_key or not user_id):
        raise RuntimeError("missing_zotero_web_api_credentials")

    for index, row in enumerate(rows, start=1):
        if args.request_delay_seconds and index > 1:
            time.sleep(args.request_delay_seconds)
        candidate, errors = resolve_candidate(row, use_semantic_scholar=args.use_semantic_scholar)
        resolved = candidate is not None
        if resolved:
            summary["resolved_candidates"] += 1
        else:
            summary["skipped"] += 1
        result = ""
        if args.apply and candidate:
            ranked = ranked_from_candidate(row, candidate)
            result = create_pdf_attachment_web(
                ranked,
                str(row.get("zotero_key")),
                user_id=user_id,
                api_key=api_key,
                upload_file=True,
                linked_fallback=True,
            )
            if result.startswith(("pdf_attachment_created", "pdf_attachment_exists")) or "linked_pdf_fallback:linked_pdf_attachment_created" in result:
                summary["apply_created_or_exists"] += 1
            else:
                summary["apply_failed"] += 1
        out = {
            "index": index,
            "zotero_key": row.get("zotero_key"),
            "queue_id": row.get("queue_id"),
            "title": row.get("title"),
            "resolved": resolved,
            "candidate": candidate.__dict__ if candidate else None,
            "errors": errors,
            "apply_result": result,
        }
        append_jsonl(plan_path, out)
        print(json.dumps(out, ensure_ascii=False))

    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if args.apply and summary["apply_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
