#!/usr/bin/env python3
"""Repair tail metadata for the 2026-06-04 manual Zotero import batch.

This script only handles the non-arXiv/non-OpenReview tail:

- direct PDF items with local PDF attachments
- venue-page items with structured venue pages

Default mode is dry-run. ``--apply --yes`` updates existing Zotero items in
place through the Zotero Web API, preserving Zotero keys and attachments. It
does not delete duplicates, move items, or write Zotero SQLite directly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import fitz

from zotero_import import WEB_API, _env, _get_json_with_headers, _web_headers, _web_user_id


BATCH_RUN_DIR = Path("output/import_runs/20260604-172607-awesome-embodied-full-import")
DEFAULT_AUDIT_ITEMS = BATCH_RUN_DIR / "repair_audit" / "manual_import_batch_items.jsonl"
DEFAULT_OUT_DIR = BATCH_RUN_DIR / "repair_audit" / "tail_metadata_repair"
DEFAULT_STORAGE_DIR = Path(os.environ.get("ZOTERO_STORAGE_DIR", Path.home() / "Zotero" / "storage"))
DEFAULT_COLLECTION = "ZJK4PK4G"

DIRECT_BUCKET = "direct_pdf_metadata_resolve"
VENUE_BUCKET = "venue_page_metadata_resolve"


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


def normalize_space(text: str) -> str:
    text = text.replace("-\n", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


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


def strip_tags(fragment: str) -> str:
    fragment = re.sub(r"<script\b.*?</script>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    fragment = re.sub(r"<style\b.*?</style>", " ", fragment, flags=re.IGNORECASE | re.DOTALL)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    return normalize_space(html.unescape(fragment))


def creator(name: str) -> dict[str, str]:
    name = normalize_space(name)
    parts = [part for part in name.split(" ") if part]
    if len(parts) <= 1:
        return {"creatorType": "author", "name": name}
    return {"creatorType": "author", "firstName": " ".join(parts[:-1]), "lastName": parts[-1]}


def merge_tags(existing: list[dict[str, Any]], new_tags: list[str]) -> list[dict[str, str]]:
    seen: set[str] = set()
    merged: list[dict[str, str]] = []
    for item in existing:
        tag = str(item.get("tag") or "").strip()
        if tag and tag not in seen:
            seen.add(tag)
            merged.append({"tag": tag})
    for tag in new_tags:
        if tag and tag not in seen:
            seen.add(tag)
            merged.append({"tag": tag})
    return merged


def eligible_rows(rows: list[dict[str, Any]], *, old_key: str | None) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        if old_key and row.get("zotero_key") != old_key:
            continue
        bucket = row.get("repair_bucket")
        explicit_duplicate = bool(old_key and bucket == "duplicate_candidate_review")
        if bucket not in {DIRECT_BUCKET, VENUE_BUCKET} and not explicit_duplicate:
            continue
        defects = set(row.get("metadata_defects") or [])
        if not {"missing_creators", "missing_abstract"} & defects:
            continue
        selected.append(row)
    return selected


def attachment_pdf_path(row: dict[str, Any], storage_dir: Path) -> Path | None:
    for attachment in row.get("attachments") or []:
        if not attachment.get("is_pdf"):
            continue
        key = str(attachment.get("key") or "").strip()
        raw_path = str(attachment.get("path") or "").strip()
        if not key or not raw_path:
            continue
        filename = raw_path.removeprefix("storage:")
        path = storage_dir / key / filename
        if path.exists():
            return path
    return None


def first_pages_text(path: Path, *, pages: int = 2) -> str:
    with fitz.open(str(path)) as doc:
        values = [doc[index].get_text("text") for index in range(min(pages, doc.page_count))]
    return "\n".join(values)


def clean_author_name(name: str) -> str:
    name = html.unescape(name)
    name = re.sub(r"\b(equal contribution|corresponding author|authors?)\b", " ", name, flags=re.IGNORECASE)
    name = re.sub(r"[\d†‡*#§¶\[\]\(\),;:]+", " ", name)
    name = normalize_space(name)
    bad_tokens = {
        "university",
        "institute",
        "laboratory",
        "department",
        "school",
        "college",
        "academy",
        "lab",
        "http",
        "www",
        "github",
    }
    lowered = name.lower()
    if any(token in lowered for token in bad_tokens):
        return ""
    if len(name) < 2 or len(name.split()) > 5:
        return ""
    return name


def split_author_lines(lines: list[str]) -> list[str]:
    candidates: list[str] = []
    for line in lines:
        line = normalize_space(line)
        if not line:
            continue
        if re.match(r"^\d", line):
            break
        if re.match(r"^(abstract|figure|keywords?|introduction)\b", line, flags=re.IGNORECASE):
            break
        if re.search(r"\b(university|institute|laboratory|department|school|college|academy)\b", line, re.IGNORECASE):
            break
        candidates.append(line)
    joined = ", ".join(candidates)
    joined = re.sub(r"(?<=[A-Za-z])\d+[∗*†‡]*", ", ", joined)
    raw_parts = re.split(r"\s*,\s*|\s+·\s+|\s+ and \s+", joined)
    authors: list[str] = []
    for part in raw_parts:
        name = clean_author_name(part)
        if name and name not in authors:
            authors.append(name)
    return authors


def title_end_index(lines: list[str], expected_title: str) -> int:
    expected_norm = normalize_title(expected_title)
    accumulated: list[str] = []
    best_index = 0
    best_score = 0.0
    for index, line in enumerate(lines[:6]):
        accumulated.append(line)
        candidate = " ".join(accumulated)
        score = title_score(expected_title, candidate)
        if score > best_score:
            best_score = score
            best_index = index
        if expected_norm and normalize_title(candidate) == expected_norm:
            return index
    return best_index


def pdf_abstract(text: str) -> str:
    match = re.search(
        r"\bAbstract\b(.*?)(?:\n\s*(?:1\.?\s+Introduction|I\.?\s+Introduction|Introduction)\b)",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    abstract = normalize_space(match.group(1))
    abstract = re.sub(r"^(abstract\s*)+", "", abstract, flags=re.IGNORECASE).strip()
    return abstract


def pdf_metadata(row: dict[str, Any], storage_dir: Path) -> dict[str, Any] | None:
    path = attachment_pdf_path(row, storage_dir)
    if not path:
        return None
    text = first_pages_text(path)
    lines = [normalize_space(line) for line in text.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return None
    title_index = title_end_index(lines, str(row.get("title") or ""))
    extracted_title = " ".join(lines[: title_index + 1])
    score = title_score(row.get("title", ""), extracted_title)
    if score < 0.55:
        extracted_title = str(row.get("title") or "")
        score = 1.0
    abstract = pdf_abstract(text)
    if len(abstract) < 120:
        return None
    author_lines = lines[title_index + 1 : title_index + 8]
    authors = split_author_lines(author_lines)
    if not authors:
        return None
    return {
        "source": "local_pdf_first_pages",
        "title": extracted_title,
        "authors": authors,
        "abstract": abstract,
        "date": date_from_row(row),
        "url": row.get("url") or first_pdf_url(row),
        "doi": "",
        "source_path": str(path),
        "title_match_score": score,
    }


def first_pdf_url(row: dict[str, Any]) -> str:
    for attachment in row.get("attachments") or []:
        url = str(attachment.get("url") or "").strip()
        if url:
            return url
    return ""


def fetch_url(url: str, *, timeout: int = 45) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "User-Agent": "codex-zotero-tail-repair/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def json_ld_objects(page: str) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for match in re.finditer(
        r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>",
        page,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        raw = html.unescape(match.group(1)).strip()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            objects.append(payload)
        elif isinstance(payload, list):
            objects.extend(item for item in payload if isinstance(item, dict))
    return objects


def venue_abstract(page: str) -> str:
    match = re.search(
        r"<div[^>]+class=[\"'][^\"']*abstract-text-inner[^\"']*[\"'][^>]*>(.*?)</div>",
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        return strip_tags(match.group(1))
    meta = re.search(
        r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'](.*?)[\"']",
        page,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return normalize_space(html.unescape(meta.group(1))) if meta else ""


def venue_metadata(row: dict[str, Any]) -> dict[str, Any] | None:
    url = str(row.get("url") or "").strip()
    if not url:
        return None
    page = fetch_url(url)
    title = ""
    authors: list[str] = []
    date = ""
    for obj in json_ld_objects(page):
        name = str(obj.get("name") or "").strip()
        if name and title_score(row.get("title", ""), name) >= 0.65:
            title = name
            date = str(obj.get("datePublished") or obj.get("dateCreated") or obj.get("dateModified") or "")[:10]
            raw_authors = obj.get("author") or []
            if isinstance(raw_authors, dict):
                raw_authors = [raw_authors]
            for author in raw_authors:
                if isinstance(author, dict):
                    author_name = str(author.get("name") or "").strip()
                else:
                    author_name = str(author or "").strip()
                clean = clean_author_name(author_name)
                if clean and clean not in authors:
                    authors.append(clean)
            break
    if not title:
        title_match = re.search(r"<h1[^>]*class=[\"'][^\"']*event-title[^\"']*[\"'][^>]*>(.*?)</h1>", page, re.I | re.S)
        title = strip_tags(title_match.group(1)) if title_match else str(row.get("title") or "")
    if not authors:
        author_match = re.search(
            r"<div[^>]+class=[\"'][^\"']*event-organizers[^\"']*[\"'][^>]*>(.*?)</div>",
            page,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if author_match:
            for author in re.split(r"\s*⋅\s*|\s*,\s*", strip_tags(author_match.group(1))):
                clean = clean_author_name(author)
                if clean and clean not in authors:
                    authors.append(clean)
    abstract = venue_abstract(page)
    if title_score(row.get("title", ""), title) < 0.65 or len(abstract) < 120 or not authors:
        return None
    return {
        "source": "venue_page_jsonld_html",
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "date": date or date_from_row(row),
        "url": url,
        "doi": "",
        "source_path": url,
        "title_match_score": title_score(row.get("title", ""), title),
    }


def date_from_row(row: dict[str, Any]) -> str:
    texts = [str(row.get("date") or ""), " ".join(row.get("source_sections") or [])]
    for text in texts:
        match = re.search(r"(20\d{2})", text)
        if match:
            return match.group(1)
    return ""


def repaired_extra(old_extra: str, old: dict[str, Any], meta: dict[str, Any]) -> str:
    marker = "metadata_repair_status: tail_metadata_enriched"
    if marker in old_extra:
        return old_extra
    lines = [old_extra.rstrip()] if old_extra.strip() else []
    lines.extend(
        [
            marker,
            f"metadata_repair_source: {meta['source']}",
            "metadata_repair_batch: 20260604-awesome-embodied-full-import",
            f"metadata_repair_at: {now_iso()}",
            f"canonical_repair_for_zotero_key: {old['zotero_key']}",
            f"metadata_repair_source_path: {meta['source_path']}",
            f"metadata_repair_title_match_score: {meta['title_match_score']:.3f}",
        ]
    )
    return "\n".join(line for line in lines if line)


def resolve_metadata(row: dict[str, Any], storage_dir: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        if row.get("repair_bucket") in {DIRECT_BUCKET, "duplicate_candidate_review"}:
            return pdf_metadata(row, storage_dir), ""
        if row.get("repair_bucket") == VENUE_BUCKET:
            return venue_metadata(row), ""
    except Exception as exc:  # noqa: BLE001 - error is recorded per row; batch continues.
        return None, f"{type(exc).__name__}:{exc}"
    return None, "unsupported_bucket"


def web_update_one(old: dict[str, Any], meta: dict[str, Any], *, collection_key: str) -> dict[str, Any]:
    api_key = _env("ZOTERO_API_KEY")
    if not api_key:
        raise RuntimeError("missing_ZOTERO_API_KEY")
    user_id = _web_user_id(collection_key)
    if not user_id:
        raise RuntimeError("missing_ZOTERO_USER_ID")
    old_key = old["zotero_key"]
    item_url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(old_key)}"
    item = _get_json_with_headers(
        item_url + "?format=json",
        {**_web_headers(api_key), "Accept": "application/json"},
        timeout=30,
    )
    version = str(item.get("version") or "")
    data = dict(item.get("data") or {})
    if not version or not data:
        raise RuntimeError("missing_remote_item_version_or_data")
    item_type = str(data.get("itemType") or old.get("item_type") or "conferencePaper")
    data.update(
        {
            "itemType": item_type,
            "title": meta["title"] or old.get("title") or data.get("title") or "",
            "creators": [creator(author) for author in meta.get("authors", [])[:30]],
            "abstractNote": meta.get("abstract") or "",
            "date": meta.get("date") or data.get("date") or "",
            "url": meta.get("url") or data.get("url") or "",
            "extra": repaired_extra(str(data.get("extra") or ""), old, meta),
            "tags": merge_tags(
                list(data.get("tags") or []),
                [
                    "metadata-repaired",
                    "metadata-repair-tail",
                    "codex-0604-repair",
                    f"source-{meta['source']}",
                ],
            ),
        }
    )
    if meta.get("doi"):
        data["DOI"] = meta["doi"]
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    headers = {**_web_headers(api_key), "If-Unmodified-Since-Version": version}
    req = urllib.request.Request(item_url, data=body, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"web_update_http_{exc.code}:{detail}") from exc
    if status != 204:
        raise RuntimeError(f"web_update_status_{status}:{raw[:200]!r}")
    return {
        "old_zotero_key": old_key,
        "new_zotero_key": old_key,
        "status": "updated_in_place",
        "source": meta["source"],
        "title_match_score": meta["title_match_score"],
        "web_item_type": item_type,
        "web_version_before": version,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-items", type=Path, default=DEFAULT_AUDIT_ITEMS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--storage-dir", type=Path, default=DEFAULT_STORAGE_DIR)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--old-key", default="")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--request-delay-seconds", type=float, default=1.0)
    args = parser.parse_args(argv)

    if args.apply and not args.yes:
        parser.error("--apply requires --yes")

    rows = eligible_rows(read_jsonl(args.audit_items), old_key=args.old_key or None)
    if args.offset:
        rows = rows[args.offset :]
    if args.limit:
        rows = rows[: args.limit]

    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    plan_path = args.out_dir / f"tail_repair_plan_{run_id}.jsonl"
    mapping_path = args.out_dir / f"tail_repair_mapping_{run_id}.jsonl"
    summary_path = args.out_dir / f"tail_repair_summary_{run_id}.json"

    summary: dict[str, Any] = {
        "created_at": now_iso(),
        "mode": "apply" if args.apply else "dry_run",
        "selected_rows": len(rows),
        "metadata_found": 0,
        "ready_rows": 0,
        "apply_updated_in_place": 0,
        "apply_failed": 0,
        "skipped": 0,
        "plan_path": str(plan_path),
        "mapping_path": str(mapping_path),
    }

    for index, row in enumerate(rows, start=1):
        if args.request_delay_seconds and row.get("repair_bucket") == VENUE_BUCKET:
            time.sleep(args.request_delay_seconds)
        meta, error = resolve_metadata(row, args.storage_dir)
        ready = bool(meta and meta.get("authors") and meta.get("abstract") and len(meta.get("abstract", "")) >= 120)
        if meta:
            summary["metadata_found"] += 1
        if ready:
            summary["ready_rows"] += 1
        else:
            summary["skipped"] += 1
        plan_row = {
            "index": index,
            "zotero_key": row.get("zotero_key"),
            "title": row.get("title"),
            "bucket": row.get("repair_bucket"),
            "ready": ready,
            "error": error,
            "metadata": meta,
        }
        append_jsonl(plan_path, plan_row)
        print(
            json.dumps(
                {
                    "zotero_key": row.get("zotero_key"),
                    "bucket": row.get("repair_bucket"),
                    "ready": ready,
                    "source": meta.get("source") if meta else "",
                    "authors": len(meta.get("authors", [])) if meta else 0,
                    "abstract_len": len(meta.get("abstract", "")) if meta else 0,
                    "error": error,
                },
                ensure_ascii=False,
            )
        )
        if not args.apply or not ready or not meta:
            continue
        try:
            result = web_update_one(row, meta, collection_key=args.collection)
            summary["apply_updated_in_place"] += 1
            append_jsonl(mapping_path, {**result, "title": row.get("title"), "updated_at": now_iso()})
        except Exception as exc:  # noqa: BLE001 - per-row failure is logged and summarized.
            summary["apply_failed"] += 1
            append_jsonl(
                mapping_path,
                {
                    "old_zotero_key": row.get("zotero_key"),
                    "status": "failed",
                    "error": f"{type(exc).__name__}:{exc}",
                    "title": row.get("title"),
                    "updated_at": now_iso(),
                },
            )

    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if args.apply and summary["apply_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
