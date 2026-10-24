"""Repair 2026-06-04 manual Zotero import items using OpenReview metadata.

Default mode is dry-run. ``--apply --yes`` updates existing Zotero items in
place through the Zotero Web API, preserving Zotero keys and PDF attachments.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from zotero_import import WEB_API, _env, _get_json_with_headers, _web_headers, _web_user_id


BATCH_RUN_DIR = Path("output/import_runs/20260604-172607-awesome-embodied-full-import")
DEFAULT_AUDIT_ITEMS = BATCH_RUN_DIR / "repair_audit" / "manual_import_batch_items.jsonl"
DEFAULT_OUT_DIR = BATCH_RUN_DIR / "repair_audit" / "openreview_metadata_repair"
DEFAULT_COLLECTION = "ZJK4PK4G"
OPENREVIEW_API = "https://api2.openreview.net/notes"


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
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def content_value(content: dict[str, Any], key: str, default: Any = "") -> Any:
    value = content.get(key, default)
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def fetch_openreview_metadata(
    openreview_id: str,
    *,
    timeout: int = 30,
    retries: int = 5,
    backoff_seconds: float = 20.0,
) -> dict[str, Any] | None:
    clean_id = openreview_id.split("#", 1)[0].strip()
    query = urllib.parse.urlencode({"id": clean_id})
    req = urllib.request.Request(
        f"{OPENREVIEW_API}?{query}",
        headers={"Accept": "application/json", "User-Agent": "codex-zotero-repair/1.0"},
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt >= retries:
                raise
            retry_after = exc.headers.get("Retry-After")
            try:
                wait = float(retry_after) if retry_after else backoff_seconds * (attempt + 1)
            except ValueError:
                wait = backoff_seconds * (attempt + 1)
            time.sleep(max(wait, backoff_seconds))
    notes = payload.get("notes") or []
    if not notes:
        return None
    note = notes[0]
    content = note.get("content") or {}
    title = str(content_value(content, "title", "") or "").strip()
    authors = content_value(content, "authors", []) or []
    if isinstance(authors, str):
        authors = [part.strip() for part in authors.split(",") if part.strip()]
    abstract = str(content_value(content, "abstract", "") or "").strip()
    tldr = str(content_value(content, "TLDR", "") or "").strip()
    keywords = content_value(content, "keywords", []) or []
    if isinstance(keywords, str):
        keywords = [part.strip() for part in keywords.split(",") if part.strip()]
    return {
        "openreview_id": clean_id,
        "title": title,
        "authors": [str(author).strip() for author in authors if str(author).strip()],
        "abstract": abstract,
        "tldr": tldr,
        "keywords": [str(keyword).strip() for keyword in keywords if str(keyword).strip()],
        "url": f"https://openreview.net/forum?id={clean_id}",
        "pdf_url": f"https://openreview.net/pdf?id={clean_id}",
        "cdate": note.get("cdate"),
        "mdate": note.get("mdate"),
        "invitations": note.get("invitations") or [],
    }


def creator(name: str) -> dict[str, str]:
    parts = [part for part in name.strip().split() if part]
    if len(parts) <= 1:
        return {"creatorType": "author", "name": name.strip()}
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


def repaired_extra(old_extra: str, old: dict[str, Any], meta: dict[str, Any]) -> str:
    marker = "metadata_repair_status: openreview_api_enriched"
    if marker in old_extra:
        return old_extra
    lines = [old_extra.rstrip()] if old_extra.strip() else []
    lines.extend(
        [
            marker,
            "metadata_repair_source: openreview_api2",
            f"metadata_repair_openreview_id: {meta['openreview_id']}",
            f"metadata_repair_at: {now_iso()}",
            f"canonical_repair_for_zotero_key: {old['zotero_key']}",
        ]
    )
    if meta.get("tldr"):
        lines.append(f"openreview_tldr: {meta['tldr']}")
    if meta.get("keywords"):
        lines.append(f"openreview_keywords: {', '.join(meta['keywords'][:20])}")
    return "\n".join(line for line in lines if line)


def year_from_row(row: dict[str, Any]) -> str:
    for value in [row.get("source_sections"), row.get("date")]:
        text = " ".join(value) if isinstance(value, list) else str(value or "")
        for year in ["2026", "2025", "2024", "2023", "2022"]:
            if year in text:
                return year
    return ""


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
    item_type = str(data.get("itemType") or "conferencePaper")
    data.update(
        {
            "itemType": item_type,
            "title": meta["title"] or old.get("title") or data.get("title") or "",
            "creators": [creator(author) for author in meta.get("authors", [])[:30]],
            "abstractNote": meta.get("abstract") or meta.get("tldr") or "",
            "date": year_from_row(old),
            "url": meta.get("url", ""),
            "extra": repaired_extra(str(data.get("extra") or ""), old, meta),
            "tags": merge_tags(
                list(data.get("tags") or []),
                [
                    "metadata-repaired",
                    "metadata-repair-openreview",
                    "codex-0604-repair",
                    "source-openreview",
                ],
            ),
        }
    )
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    headers = {**_web_headers(api_key), "If-Unmodified-Since-Version": version}
    req = urllib.request.Request(item_url, data=body, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            status = resp.status
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        detail = raw.decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"web_update_http_{exc.code}:{detail}") from exc
    if status != 204:
        raise RuntimeError(f"web_update_status_{status}:{raw[:200]!r}")
    return {
        "old_zotero_key": old_key,
        "new_zotero_key": old_key,
        "openreview_id": meta["openreview_id"],
        "status": "updated_in_place",
        "web_item_type": item_type,
        "web_version_before": version,
    }


def eligible_rows(rows: list[dict[str, Any]], *, old_key: str | None) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for row in rows:
        if old_key and row.get("zotero_key") != old_key:
            continue
        if row.get("repair_bucket") != "openreview_metadata_resolve":
            continue
        openreview_id = str(row.get("openreview_id") or "").split("#", 1)[0].strip()
        if not openreview_id:
            continue
        selected.append(row)
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-items", type=Path, default=DEFAULT_AUDIT_ITEMS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--old-key", default="")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--request-delay-seconds", type=float, default=2.0)
    parser.add_argument("--retry-backoff-seconds", type=float, default=20.0)
    args = parser.parse_args(argv)

    rows = eligible_rows(read_jsonl(args.audit_items), old_key=args.old_key or None)
    if args.offset:
        rows = rows[args.offset :]
    if args.limit:
        rows = rows[: args.limit]
    if args.apply and not args.yes:
        parser.error("--apply requires --yes")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    plan_path = args.out_dir / f"openreview_repair_plan_{stamp}.jsonl"
    mapping_path = args.out_dir / f"openreview_repair_mapping_{stamp}.jsonl"
    summary_path = args.out_dir / f"openreview_repair_summary_{stamp}.json"

    planned: list[dict[str, Any]] = []
    apply_results: list[dict[str, Any]] = []
    for row in rows:
        openreview_id = str(row.get("openreview_id") or "").split("#", 1)[0].strip()
        try:
            meta = fetch_openreview_metadata(openreview_id, backoff_seconds=args.retry_backoff_seconds)
            if not meta:
                planned_row = {**row, "repair_status": "metadata_missing"}
                append_jsonl(plan_path, planned_row)
                planned.append(planned_row)
                continue
            ready = bool(meta.get("title") and meta.get("authors") and (meta.get("abstract") or meta.get("tldr")))
            planned_row = {
                "zotero_key": row.get("zotero_key"),
                "openreview_id": openreview_id,
                "title_before": row.get("title"),
                "title_after": meta.get("title"),
                "authors_count": len(meta.get("authors") or []),
                "abstract_len": len(meta.get("abstract") or meta.get("tldr") or ""),
                "ready": ready,
                "repair_status": "ready" if ready else "metadata_incomplete",
            }
            append_jsonl(plan_path, planned_row)
            planned.append(planned_row)
            if args.apply and ready:
                result = web_update_one(row, meta, collection_key=args.collection)
                apply_results.append(result)
                append_jsonl(mapping_path, result)
                print(json.dumps({"progress": len(apply_results), **result}, ensure_ascii=False), flush=True)
        except (RuntimeError, urllib.error.URLError, OSError) as exc:
            result = {
                "old_zotero_key": row.get("zotero_key"),
                "openreview_id": openreview_id,
                "status": "failed",
                "error": f"{type(exc).__name__}:{exc}",
            }
            if args.apply:
                apply_results.append(result)
                append_jsonl(mapping_path, result)
                print(json.dumps({"progress": len(apply_results), **result}, ensure_ascii=False), flush=True)
            else:
                planned_row = {**result, "repair_status": "metadata_error"}
                planned.append(planned_row)
                append_jsonl(plan_path, planned_row)
        time.sleep(max(args.request_delay_seconds, 0.0))

    summary = {
        "generated_at": now_iso(),
        "mode": "apply" if args.apply else "dry-run",
        "selected_rows": len(rows),
        "metadata_found": sum(1 for row in planned if row.get("repair_status") in {"ready", "metadata_incomplete"}),
        "metadata_missing": sum(1 for row in planned if row.get("repair_status") == "metadata_missing"),
        "metadata_errors": sum(1 for row in planned if row.get("repair_status") == "metadata_error"),
        "ready_rows": sum(1 for row in planned if row.get("repair_status") == "ready"),
        "apply_updated_in_place": sum(1 for row in apply_results if row.get("status") == "updated_in_place"),
        "apply_failed": sum(1 for row in apply_results if row.get("status") == "failed"),
        "outputs": {
            "plan_jsonl": str(plan_path.resolve()),
            "summary_json": str(summary_path.resolve()),
            "mapping_jsonl": str(mapping_path.resolve()) if mapping_path.exists() else "",
        },
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["apply_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
