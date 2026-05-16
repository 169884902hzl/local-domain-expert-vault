"""Backfill missing Zotero PDF file attachments for auto arXiv imports."""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.parse
from urllib.request import Request, urlopen
from pathlib import Path
from typing import Any

from arxiv_ranker import ArxivPaper, RankedPaper
from kb_common import safe_print, vault_path
from zotero_import import (
    DEFAULT_COLLECTION_KEY,
    LOCAL_API,
    WEB_API,
    _read_json,
    delete_item_web,
    _env,
    _web_headers,
    _web_user_id,
    create_linked_pdf_attachment_web,
    create_pdf_attachment_web,
    pdf_filename_from_ranked,
    should_upload_pdf_files,
)


RUN_IMPORT_RE = re.compile(
    r"^- arxiv=(?P<arxiv>\S+)\s+selection=\S+\s+original=\S+\s+score=(?P<score>\S*)\s+"
    r"status=(?P<status>\S+)\s+zotero_key=(?P<key>\S+)\s+message=(?P<message>.*)$"
)
RUN_ANY_KEY_RE = re.compile(r"^- arxiv=(?P<arxiv>\S+).*?\bzotero_key=(?P<key>[A-Z0-9]+)(?:\b|$).*?(?:\bmessage=(?P<message>.*))?$")

IMPORT_STATUSES = {"created", "exists", "sync_pending", "backlog"}
DEFAULT_LOCAL_LINK_DIR = Path(os.environ.get("ZOTERO_LOCAL_PDF_CACHE", r".local\zotero-pdf-cache"))
ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)
ARXIV_EXTRA_RE = re.compile(r"\barXiv:\s*(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def discover_run_dates() -> list[str]:
    root = vault_path("projects", "arxiv-daily")
    dates: list[str] = []
    for path in sorted(root.glob("????-??-??-run.md")):
        if re.match(r"^\d{4}-\d{2}-\d{2}-run$", path.stem):
            dates.append(path.stem.removesuffix("-run"))
    return dates


def _load_paper_from_mirror(arxiv_id: str) -> ArxivPaper | None:
    db_path = vault_path("projects", "arxiv-daily", "metadata", "arxiv_metadata.sqlite")
    if not db_path.exists():
        return None
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute("SELECT * FROM papers WHERE arxiv_id = ?", (arxiv_id,)).fetchone()
    finally:
        conn.close()
    if row is None:
        return None
    return ArxivPaper(
        arxiv_id=str(row["arxiv_id"]),
        title=str(row["title"]),
        authors=json.loads(row["authors_json"] or "[]"),
        summary=str(row["summary"]),
        published=str(row["published"]),
        updated=str(row["updated"]),
        url=str(row["url"]),
        pdf_url=str(row["pdf_url"]),
        categories=json.loads(row["categories_json"] or "[]"),
        primary_category=str(row["primary_category"]),
        doi=str(row["doi"]),
        journal_ref=str(row["journal_ref"]),
        comment=str(row["comment"]),
        query_sources=["backfill_zotero_pdf_attachments"],
    )


def _fallback_paper(arxiv_id: str) -> ArxivPaper:
    return ArxivPaper(
        arxiv_id=arxiv_id,
        title=f"arXiv {arxiv_id}",
        authors=[],
        summary="",
        published="",
        updated="",
        url=f"https://arxiv.org/abs/{arxiv_id}",
        pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
        categories=[],
        primary_category="",
        doi=f"10.48550/arXiv.{arxiv_id}",
        journal_ref="",
        comment="",
        query_sources=["backfill_zotero_pdf_attachments"],
    )


def _ranked_for_attachment(arxiv_id: str) -> RankedPaper:
    paper = _load_paper_from_mirror(arxiv_id) or _fallback_paper(arxiv_id)
    return RankedPaper(
        paper=paper,
        quality_score=0,
        decision="pdf_attachment_backfill",
        reasons=["pdf_attachment_backfill"],
        matched_terms=[],
        penalties=[],
    )


def _extract_arxiv_id(item: dict[str, Any]) -> str:
    data = item.get("data", {}) if isinstance(item, dict) else {}
    archive_location = str(data.get("archiveLocation", "")).strip()
    if re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", archive_location):
        return archive_location.split("v", 1)[0]
    for field in ("url", "extra", "DOI"):
        text = str(data.get(field, ""))
        for pattern in (ARXIV_URL_RE, ARXIV_EXTRA_RE):
            match = pattern.search(text)
            if match:
                return match.group(1)
    return ""


def iter_collection_arxiv_items(collection_key: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    start = 0
    while True:
        url = (
            f"{LOCAL_API}/collections/{urllib.parse.quote(collection_key)}/items"
            f"?limit=100&start={start}&format=json"
        )
        batch = _read_json(url, timeout=30)
        if not isinstance(batch, list):
            break
        for item in batch:
            data = item.get("data", {}) if isinstance(item, dict) else {}
            if data.get("itemType") in {"attachment", "note"}:
                continue
            arxiv_id = _extract_arxiv_id(item)
            if not arxiv_id:
                continue
            records.append(
                {
                    "run_date": "collection",
                    "status": "collection_item",
                    "arxiv": arxiv_id,
                    "key": str(item.get("key") or data.get("key") or ""),
                    "message": str(data.get("title", "")),
                }
            )
        if len(batch) < 100:
            break
        start += 100
    return records


def _children(zotero_key: str) -> list[dict[str, Any]]:
    url = f"{LOCAL_API}/items/{urllib.parse.quote(zotero_key)}/children?format=json"
    data = _read_json(url, timeout=20)
    return data if isinstance(data, list) else []


def has_pdf_attachment(zotero_key: str) -> bool:
    try:
        children = _children(zotero_key)
    except Exception:
        return False
    for child in children:
        data = child.get("data", {}) if isinstance(child, dict) else {}
        if data.get("itemType") != "attachment":
            continue
        content_type = str(data.get("contentType", "")).lower()
        path_or_url = " ".join(str(data.get(name, "")) for name in ["path", "url", "filename"]).lower()
        if "pdf" in content_type or ".pdf" in path_or_url or "/pdf/" in path_or_url:
            return True
    return False


def _web_children(zotero_key: str, *, user_id: str, api_key: str) -> list[dict[str, Any]]:
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(zotero_key)}/children?format=json"

    req = Request(url, headers={**_web_headers(api_key), "Accept": "application/json"})
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data if isinstance(data, list) else []


def _is_pdf_attachment(child: dict[str, Any]) -> bool:
    data = child.get("data", {}) if isinstance(child, dict) else {}
    if data.get("itemType") != "attachment":
        return False
    content_type = str(data.get("contentType", "")).lower()
    path_or_url = " ".join(str(data.get(name, "")) for name in ["path", "url", "filename"]).lower()
    return "pdf" in content_type or ".pdf" in path_or_url or "/pdf/" in path_or_url


def _is_file_backed_attachment(child: dict[str, Any]) -> bool:
    data = child.get("data", {}) if isinstance(child, dict) else {}
    link_mode = str(data.get("linkMode", ""))
    if link_mode == "linked_file":
        return False
    path = str(data.get("path", "")).lower()
    filename = str(data.get("filename", "")).lower()
    return bool(data.get("md5") and data.get("filename")) or path.startswith("storage:") or (
        link_mode == "imported_file" and (filename.endswith(".pdf") or path.endswith(".pdf"))
    )


def _url_pdf_attachment_keys(children: list[dict[str, Any]]) -> list[str]:
    keys: list[str] = []
    for child in children:
        if not _is_pdf_attachment(child) or _is_file_backed_attachment(child):
            continue
        data = child.get("data", {}) if isinstance(child, dict) else {}
        link_mode = str(data.get("linkMode", ""))
        url = str(data.get("url", ""))
        title = str(data.get("title", ""))
        if link_mode not in {"linked_url", "imported_url"}:
            continue
        if "arxiv.org/pdf/" not in url.lower() and not title.startswith("PDF - "):
            continue
        key = str(child.get("key") or data.get("key") or "")
        if key:
            keys.append(key)
    return keys


def pdf_attachment_state(zotero_key: str, *, user_id: str, api_key: str, state_source: str = "auto") -> dict[str, str]:
    if state_source == "web":
        children = _web_children(zotero_key, user_id=user_id, api_key=api_key)
    elif state_source == "local":
        children = _children(zotero_key)
    else:
        try:
            children = _children(zotero_key)
        except Exception:
            children = _web_children(zotero_key, user_id=user_id, api_key=api_key)
    pdf_children = [child for child in children if _is_pdf_attachment(child)]
    file_backed = [child for child in pdf_children if _is_file_backed_attachment(child)]
    url_only = [child for child in pdf_children if not _is_file_backed_attachment(child)]
    first_url_only = (url_only or [{}])[0]
    first_key = str(first_url_only.get("key") or first_url_only.get("data", {}).get("key") or "")
    cleanup_keys = _url_pdf_attachment_keys(pdf_children) if file_backed else []
    return {
        "has_file_pdf": "1" if file_backed else "",
        "url_only_pdf_key": first_key,
        "cleanup_url_pdf_keys": ",".join(cleanup_keys),
        "pdf_count": str(len(pdf_children)),
    }


def iter_run_imports(run_dates: list[str], *, include_all_run_keys: bool = False) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for run_date in run_dates:
        path = vault_path("projects", "arxiv-daily", f"{run_date}-run.md")
        if not path.exists():
            records.append({"run_date": run_date, "status": "missing_run_log", "arxiv": "", "key": ""})
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            match = RUN_IMPORT_RE.match(line)
            if match:
                status = match.group("status")
                if status not in IMPORT_STATUSES and not include_all_run_keys:
                    continue
                records.append(
                    {
                        "run_date": run_date,
                        "status": status,
                        "arxiv": match.group("arxiv"),
                        "key": match.group("key"),
                        "message": match.group("message"),
                    }
                )
                continue
            if not include_all_run_keys:
                continue
            any_match = RUN_ANY_KEY_RE.match(line)
            if not any_match:
                continue
            records.append(
                {
                    "run_date": run_date,
                    "status": "candidate_pool",
                    "arxiv": any_match.group("arxiv"),
                    "key": any_match.group("key"),
                    "message": any_match.group("message") or "candidate pool key from run log",
                }
            )
    return records


def backfill(
    records: list[dict[str, str]],
    *,
    collection_key: str,
    dry_run: bool,
    limit: int = 0,
    progress_every: int = 0,
    local_link_dir: Path | None = None,
    state_source: str = "auto",
    cleanup_url_pdf: bool = False,
) -> list[dict[str, str]]:
    api_key = _env("ZOTERO_API_KEY")
    user_id = _web_user_id(collection_key) if api_key else ""
    upload_file = should_upload_pdf_files()
    if local_link_dir:
        upload_file = False
    results: list[dict[str, str]] = []
    processed_keys: set[str] = set()
    attempted = 0
    for record in records:
        key = record.get("key", "")
        arxiv_id = record.get("arxiv", "")
        if not key or not arxiv_id:
            results.append({**record, "result": "skipped_missing_key_or_arxiv"})
            continue
        if key in processed_keys:
            results.append({**record, "result": "skipped_duplicate_key"})
            continue
        processed_keys.add(key)
        state = (
            pdf_attachment_state(key, user_id=user_id, api_key=api_key, state_source=state_source)
            if api_key and user_id
            else {"has_file_pdf": "1" if has_pdf_attachment(key) else "", "url_only_pdf_key": "", "cleanup_url_pdf_keys": "", "pdf_count": "0"}
        )
        if state["has_file_pdf"]:
            cleanup_keys = _split_csv(state.get("cleanup_url_pdf_keys", ""))
            if cleanup_url_pdf and cleanup_keys:
                if dry_run:
                    results.append(
                        {
                            **record,
                            "result": "would_delete_redundant_pdf_url_attachments",
                            "pdf_count": state["pdf_count"],
                            "attachment_keys": ",".join(cleanup_keys),
                        }
                    )
                    attempted += 1
                    if progress_every and attempted % progress_every == 0:
                        safe_print(f"progress would_process={attempted} last_key={key}")
                    if limit and attempted >= limit:
                        break
                    continue
                if not api_key or not user_id:
                    results.append({**record, "result": "failed_missing_zotero_web_credentials"})
                    attempted += 1
                    if limit and attempted >= limit:
                        break
                    continue
                statuses = [f"{attachment_key}:{delete_item_web(attachment_key, user_id=user_id, api_key=api_key)}" for attachment_key in cleanup_keys]
                results.append(
                    {
                        **record,
                        "result": "deleted_redundant_pdf_url_attachments:" + "|".join(statuses),
                        "pdf_count": state["pdf_count"],
                    }
                )
                attempted += 1
                if progress_every and attempted % progress_every == 0:
                    safe_print(f"progress processed={attempted} last_key={key} cleanup={len(cleanup_keys)}")
                if limit and attempted >= limit:
                    break
                continue
            results.append({**record, "result": "exists_file_pdf_attachment", "pdf_count": state["pdf_count"]})
            continue
        if state["url_only_pdf_key"] and not upload_file and not local_link_dir:
            results.append({**record, "result": "exists_pdf_url_attachment", "pdf_count": state["pdf_count"]})
            continue
        if dry_run:
            if state["url_only_pdf_key"]:
                if upload_file:
                    result = "would_upload_existing_pdf_url_attachment"
                elif local_link_dir:
                    result = "would_create_local_linked_pdf_attachment"
                else:
                    result = "exists_pdf_url_attachment"
            else:
                if upload_file:
                    result = "would_create_pdf_file_attachment"
                elif local_link_dir:
                    result = "would_create_local_linked_pdf_attachment"
                else:
                    result = "would_create_pdf_url_attachment"
            results.append({**record, "result": result, "pdf_count": state["pdf_count"]})
            if result.startswith("would_"):
                attempted += 1
                if progress_every and attempted % progress_every == 0:
                    safe_print(f"progress would_process={attempted} last_key={key}")
                if limit and attempted >= limit:
                    break
            continue
        if not api_key or not user_id:
            results.append({**record, "result": "failed_missing_zotero_web_credentials"})
            attempted += 1
            if limit and attempted >= limit:
                break
            continue
        ranked = _ranked_for_attachment(arxiv_id)
        if local_link_dir and not upload_file:
            status = create_local_linked_pdf_attachment(
                ranked,
                key,
                local_link_dir,
                user_id=user_id,
                api_key=api_key,
            )
        else:
            status = create_pdf_attachment_web(
                ranked,
                key,
                user_id=user_id,
                api_key=api_key,
                upload_file=upload_file,
            )
        if state["url_only_pdf_key"] and "pdf_attachment_created" in status:
            status += "; old_pdf_url_attachment_preserved"
        results.append({**record, "result": status})
        attempted += 1
        if progress_every and attempted % progress_every == 0:
            safe_print(f"progress processed={attempted} last_key={key} result={status}")
        if limit and attempted >= limit:
            break
    return results


def download_pdf_to_local_cache(ranked: RankedPaper, local_link_dir: Path) -> Path:
    paper = ranked.paper
    pdf_url = paper.pdf_url or (f"https://arxiv.org/pdf/{paper.arxiv_id}" if paper.arxiv_id else "")
    if not pdf_url:
        raise RuntimeError("no PDF URL available")
    local_link_dir.mkdir(parents=True, exist_ok=True)
    path = local_link_dir / pdf_filename_from_ranked(ranked)
    if path.exists() and path.stat().st_size > 1000:
        return path
    req = Request(
        pdf_url,
        headers={"Accept": "application/pdf,*/*", "User-Agent": "daily-arxiv-zotero-pdf-backfill/1.0"},
    )
    with urlopen(req, timeout=180) as resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        raise RuntimeError(f"downloaded file is not a PDF from {pdf_url}")
    path.write_bytes(data)
    return path


def create_local_linked_pdf_attachment(
    ranked: RankedPaper,
    parent_key: str,
    local_link_dir: Path,
    *,
    user_id: str,
    api_key: str,
) -> str:
    try:
        pdf_path = download_pdf_to_local_cache(ranked, local_link_dir)
    except Exception as exc:
        return f"local_pdf_download_failed:{type(exc).__name__}:{str(exc)[:160]}"
    status = create_linked_pdf_attachment_web(
        ranked,
        parent_key,
        str(pdf_path),
        user_id=user_id,
        api_key=api_key,
    )
    return f"{status}; local_pdf_path={pdf_path}" if status.startswith(("linked_pdf_attachment_created", "linked_pdf_attachment_exists")) else status


def summarize_results(results: list[dict[str, str]]) -> dict[str, Any]:
    summary: dict[str, Any] = {"total_results": len(results), "by_result": {}}
    for item in results:
        result = str(item.get("result", ""))
        bucket = result.split(":", 1)[0].split(";", 1)[0]
        summary["by_result"][bucket] = summary["by_result"].get(bucket, 0) + 1
    failures = [item for item in results if is_failure_result(str(item.get("result", "")))]
    summary["failed"] = len(failures)
    summary["needs_file_upload"] = sum(
        1
        for item in results
        if str(item.get("result", "")).startswith(("would_upload", "would_create", "exists_pdf_url_attachment"))
    )
    return summary


def is_failure_result(result: str) -> bool:
    return result.startswith(
        (
            "failed",
            "pdf_attachment_failed",
            "pdf_attachment_upload_failed",
            "pdf_file_upload_failed",
            "linked_pdf_attachment_failed",
            "local_pdf_download_failed",
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dates", required=True, help="Comma-separated run dates, 'all', or 'collection'.")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION_KEY)
    parser.add_argument("--include-all-run-keys", action="store_true", help="Also check candidate-pool zotero_key entries from run logs.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N missing/file-upload-needed records have been processed.")
    parser.add_argument("--progress-every", type=int, default=10, help="Print progress every N processed missing records; 0 disables progress.")
    parser.add_argument("--report", help="Write JSON report to this path.")
    parser.add_argument(
        "--cleanup-url-pdf",
        action="store_true",
        help="Delete redundant arXiv PDF URL attachments only when the same Zotero item already has a file-backed PDF.",
    )
    parser.add_argument(
        "--local-linked-dir",
        nargs="?",
        const=str(DEFAULT_LOCAL_LINK_DIR),
        help=f"Download PDFs to this local directory and attach them as linked_file attachments. Default: {DEFAULT_LOCAL_LINK_DIR}",
    )
    parser.add_argument("--state-source", choices=["auto", "local", "web"], default="auto", help="Where to inspect Zotero child attachments.")
    args = parser.parse_args()

    run_date_arg = args.run_dates.strip().lower()
    if run_date_arg == "collection":
        run_dates = ["collection"]
        records = iter_collection_arxiv_items(args.collection)
    else:
        run_dates = discover_run_dates() if run_date_arg == "all" else _split_csv(args.run_dates)
        records = iter_run_imports(run_dates, include_all_run_keys=args.include_all_run_keys)
    local_link_dir = Path(args.local_linked_dir) if args.local_linked_dir else None
    effective_upload_file = False if local_link_dir else should_upload_pdf_files()
    results = backfill(
        records,
        collection_key=args.collection,
        dry_run=args.dry_run,
        limit=args.limit,
        progress_every=args.progress_every,
        local_link_dir=local_link_dir,
        state_source=args.state_source,
        cleanup_url_pdf=args.cleanup_url_pdf,
    )
    report = {
        "run_dates": run_dates,
        "dry_run": args.dry_run,
        "upload_file": effective_upload_file,
        "local_link_dir": str(local_link_dir) if local_link_dir else "",
        "state_source": args.state_source,
        "cleanup_url_pdf": args.cleanup_url_pdf,
        "summary": summarize_results(results),
        "results": results,
    }
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        safe_print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            safe_print(f"{item.get('run_date')} arxiv={item.get('arxiv')} zotero_key={item.get('key')} result={item.get('result')}")
        safe_print("SUMMARY " + json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    failed = [
        item
        for item in results
        if is_failure_result(str(item.get("result", "")))
    ]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
