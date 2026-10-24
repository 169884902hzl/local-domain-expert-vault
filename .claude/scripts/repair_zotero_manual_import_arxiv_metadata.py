#!/usr/bin/env python3
"""Repair arXiv-backed entries from the 2026-06-04 manual Zotero import.

Default mode is dry-run. Apply mode creates canonical Zotero items via the
Zotero Connector, preserving the old malformed item and writing an old->new
mapping. It does not delete, overwrite, or directly edit Zotero SQLite rows.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from zotero_import import (
    WEB_API,
    _env,
    _get_json_with_headers,
    _post_connector_bytes,
    _post_connector_json,
    _web_headers,
    _web_user_id,
    connector_preflight,
)


DEFAULT_RUN_DIR = Path("output/import_runs/20260604-172607-awesome-embodied-full-import")
DEFAULT_AUDIT_ITEMS = DEFAULT_RUN_DIR / "repair_audit" / "manual_import_batch_items.jsonl"
DEFAULT_OUT_DIR = DEFAULT_RUN_DIR / "repair_audit" / "arxiv_metadata_repair"
DEFAULT_ZOTERO_STORAGE = Path(os.environ.get("ZOTERO_STORAGE_DIR", Path.home() / "Zotero" / "storage"))
DEFAULT_ZOTERO_DB = Path(os.environ.get("ZOTERO_DB_PATH", Path.home() / "Zotero" / "zotero.sqlite"))
ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def vault_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def normalize_title(text: str) -> str:
    text = re.sub(r"[\]\[]+$", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def arxiv_text(entry: ET.Element, name: str) -> str:
    node = entry.find(f"arxiv:{name}", ATOM)
    return (node.text or "").strip() if node is not None else ""


def entry_id(entry: ET.Element) -> str:
    node = entry.find("atom:id", ATOM)
    value = (node.text or "").strip() if node is not None else ""
    match = re.search(r"/abs/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?$", value)
    return match.group(1) if match else ""


def atom_text(entry: ET.Element, name: str) -> str:
    node = entry.find(f"atom:{name}", ATOM)
    return re.sub(r"\s+", " ", (node.text or "")).strip() if node is not None else ""


def entry_authors(entry: ET.Element) -> list[str]:
    authors: list[str] = []
    for author in entry.findall("atom:author", ATOM):
        name_node = author.find("atom:name", ATOM)
        name = re.sub(r"\s+", " ", (name_node.text or "")).strip() if name_node is not None else ""
        if name:
            authors.append(name)
    return authors


def entry_pdf_url(entry: ET.Element, arxiv_id: str) -> str:
    for link in entry.findall("atom:link", ATOM):
        if link.attrib.get("title") == "pdf" and link.attrib.get("href"):
            return link.attrib["href"]
    return f"https://arxiv.org/pdf/{arxiv_id}"


def fetch_arxiv_metadata(arxiv_ids: list[str], *, batch_size: int = 50, timeout: int = 60) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for batch in chunks(arxiv_ids, batch_size):
        query = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": str(len(batch))})
        req = urllib.request.Request(
            f"{ARXIV_API}?{query}",
            headers={"Accept": "application/atom+xml", "User-Agent": "zotero-0604-metadata-repair/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            root = ET.fromstring(resp.read())
        for entry in root.findall("atom:entry", ATOM):
            arxiv_id = entry_id(entry)
            if not arxiv_id:
                continue
            published = atom_text(entry, "published")
            updated = atom_text(entry, "updated")
            doi = arxiv_text(entry, "doi") or f"10.48550/arXiv.{arxiv_id}"
            out[arxiv_id] = {
                "arxiv_id": arxiv_id,
                "title": normalize_title(atom_text(entry, "title")),
                "authors": entry_authors(entry),
                "summary": atom_text(entry, "summary"),
                "published": published,
                "updated": updated,
                "date": (published or updated)[:10],
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "pdf_url": entry_pdf_url(entry, arxiv_id),
                "doi": doi,
                "primary_category": "",
                "categories": [cat.attrib.get("term", "") for cat in entry.findall("atom:category", ATOM) if cat.attrib.get("term")],
                "comment": arxiv_text(entry, "comment"),
                "journal_ref": arxiv_text(entry, "journal_ref"),
            }
            primary = entry.find("arxiv:primary_category", ATOM)
            if primary is not None:
                out[arxiv_id]["primary_category"] = primary.attrib.get("term", "")
    return out


def creator(author: str) -> dict[str, str]:
    author = re.sub(r"\s+", " ", author).strip()
    parts = author.split(" ")
    if len(parts) <= 1:
        return {"creatorType": "author", "firstName": "", "lastName": author or "Unknown"}
    return {"creatorType": "author", "firstName": " ".join(parts[:-1]), "lastName": parts[-1]}


def canonical_item(old: dict[str, Any], meta: dict[str, Any], *, connector_id: str) -> dict[str, Any]:
    old_key = old["zotero_key"]
    extra_lines = [
        f"arXiv: {meta['arxiv_id']}",
        "metadata_repair_source: arxiv_api",
        "metadata_repair_batch: 20260604-awesome-embodied-full-import",
        f"canonical_repair_for_zotero_key: {old_key}",
        f"old_import_queue_id: {old.get('queue_id', '')}",
        f"old_import_title: {old.get('title', '')}",
    ]
    if meta.get("comment"):
        extra_lines.append(f"arxiv_comment: {meta['comment']}")
    if meta.get("journal_ref"):
        extra_lines.append(f"journal_ref: {meta['journal_ref']}")
    tags = [
        {"tag": "embodied-ai"},
        {"tag": "metadata-repair-canonical"},
        {"tag": "codex-0604-repair"},
        {"tag": "source-arxiv"},
        {"tag": f"replaces-{old_key}"},
    ]
    return {
        "id": connector_id,
        "itemType": "preprint",
        "title": meta["title"],
        "creators": [creator(author) for author in meta.get("authors", [])[:20]],
        "abstractNote": meta.get("summary", ""),
        "date": meta.get("date", ""),
        "archive": "arXiv",
        "archiveLocation": meta["arxiv_id"],
        "url": meta.get("url", ""),
        "DOI": meta.get("doi", ""),
        "extra": "\n".join(extra_lines),
        "tags": tags,
    }


def old_pdf_bytes(old: dict[str, Any], storage_dir: Path) -> tuple[bytes | None, str]:
    for attachment in old.get("attachments", []):
        if not attachment.get("is_pdf"):
            continue
        raw_path = str(attachment.get("path") or "")
        if raw_path.startswith("storage:"):
            candidate = storage_dir / str(attachment.get("key")) / raw_path.removeprefix("storage:")
            if candidate.exists():
                return candidate.read_bytes(), str(candidate)
    return None, ""


def connector_import_one(
    old: dict[str, Any],
    meta: dict[str, Any],
    *,
    collection_key: str,
    storage_dir: Path,
) -> dict[str, Any]:
    pf = connector_preflight(collection_key)
    if not pf.get("reachable"):
        raise RuntimeError("; ".join(pf.get("errors") or ["connector_not_reachable"]))
    target = str(pf.get("collection_tree_id") or "")
    if not target:
        raise RuntimeError("; ".join(pf.get("errors") or ["collection_target_unresolved"]))

    old_key = old["zotero_key"]
    connector_id = f"repair-arxiv-{old_key}-{meta['arxiv_id']}-{uuid.uuid4().hex[:8]}"
    session_id = f"{connector_id}-{uuid.uuid4().hex[:12]}"
    item = canonical_item(old, meta, connector_id=connector_id)
    status, _, _ = _post_connector_json(
        "/connector/saveItems",
        {"sessionID": session_id, "uri": meta.get("url") or meta.get("pdf_url"), "items": [item]},
        timeout=60,
    )
    if status != 201:
        raise RuntimeError(f"saveItems_status_{status}")

    status, data, _ = _post_connector_json("/connector/updateSession", {"sessionID": session_id, "target": target}, timeout=30)
    if status != 200:
        raise RuntimeError(f"updateSession_status_{status}:{data}")

    pdf_bytes, pdf_source = old_pdf_bytes(old, storage_dir)
    attachment_status = "not_attempted"
    if pdf_bytes:
        metadata = {
            "sessionID": session_id,
            "parentItemID": connector_id,
            "title": f"PDF - {meta['title'][:180]}",
            "url": meta.get("pdf_url") or f"https://arxiv.org/pdf/{meta['arxiv_id']}",
        }
        attachment_http_status, _ = _post_connector_bytes(
            f"/connector/saveAttachment?sessionID={urllib.parse.quote(session_id)}",
            pdf_bytes,
            metadata,
            timeout=240,
        )
        attachment_status = f"saved_http_{attachment_http_status}"
    return {
        "old_zotero_key": old_key,
        "arxiv_id": meta["arxiv_id"],
        "connector_id": connector_id,
        "session_id": session_id,
        "status": "created",
        "attachment_status": attachment_status,
        "pdf_source": pdf_source,
    }


def merge_tags(existing: list[dict[str, Any]], additions: list[str]) -> list[dict[str, Any]]:
    seen = {str(tag.get("tag", "")) for tag in existing if tag.get("tag")}
    merged = list(existing)
    for tag in additions:
        if tag not in seen:
            merged.append({"tag": tag})
            seen.add(tag)
    return merged


def repaired_extra(old_extra: str, old: dict[str, Any], meta: dict[str, Any]) -> str:
    marker = "metadata_repair_status: arxiv_api_enriched"
    if marker in old_extra:
        return old_extra
    lines = [old_extra.rstrip()] if old_extra.strip() else []
    lines.extend(
        [
            marker,
            f"metadata_repair_completed_at: {utc_now()}",
            f"metadata_repair_source: arxiv_api",
            f"metadata_repair_batch: 20260604-awesome-embodied-full-import",
            f"arXiv: {meta['arxiv_id']}",
            f"old_import_queue_id: {old.get('queue_id', '')}",
        ],
    )
    if meta.get("comment"):
        lines.append(f"arxiv_comment: {meta['comment']}")
    if meta.get("journal_ref"):
        lines.append(f"journal_ref: {meta['journal_ref']}")
    return "\n".join(line for line in lines if line)


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
    item_type_before = str(data.get("itemType") or "")
    item_type = item_type_before if item_type_before == "conferencePaper" else "preprint"
    data.update(
        {
            "itemType": item_type,
            "title": meta["title"],
            "creators": [creator(author) for author in meta.get("authors", [])[:20]],
            "abstractNote": meta.get("summary", ""),
            "date": meta.get("date", ""),
            "archive": "arXiv",
            "archiveLocation": meta["arxiv_id"],
            "url": meta.get("url", ""),
            "DOI": meta.get("doi", ""),
            "extra": repaired_extra(str(data.get("extra") or ""), old, meta),
            "tags": merge_tags(
                list(data.get("tags") or []),
                [
                    "metadata-repaired",
                    "metadata-repair-arxiv",
                    "codex-0604-repair",
                    "source-arxiv",
                ],
            ),
        },
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
        "arxiv_id": meta["arxiv_id"],
        "status": "updated_in_place",
        "web_item_type_before": item_type_before,
        "web_item_type_after": item_type,
        "web_version_before": version,
    }


def observe_new_key(old_key: str, db_path: Path, *, retries: int = 20, delay: float = 1.0) -> str:
    needle = f"canonical_repair_for_zotero_key: {old_key}"
    for _ in range(retries):
        try:
            con = sqlite3.connect(db_path)
            con.row_factory = sqlite3.Row
            row = con.execute(
                """
                select i.key
                from items i
                join itemData d on d.itemID = i.itemID
                join fields f on f.fieldID = d.fieldID and f.fieldName = 'extra'
                join itemDataValues v on v.valueID = d.valueID
                left join itemAttachments ia on ia.itemID = i.itemID
                left join deletedItems di on di.itemID = i.itemID
                where ia.itemID is null
                  and di.itemID is null
                  and v.value like ?
                order by i.dateAdded desc, i.itemID desc
                limit 1
                """,
                (f"%{needle}%",),
            ).fetchone()
            con.close()
            if row:
                return str(row["key"])
        except sqlite3.Error:
            pass
        time.sleep(delay)
    return ""


def item_plan(old: dict[str, Any], meta: dict[str, Any] | None) -> dict[str, Any]:
    if not meta:
        return {
            "old_zotero_key": old["zotero_key"],
            "queue_id": old.get("queue_id", ""),
            "arxiv_id": old.get("arxiv_id", ""),
            "status": "metadata_missing",
            "old_title": old.get("title", ""),
        }
    return {
        "old_zotero_key": old["zotero_key"],
        "queue_id": old.get("queue_id", ""),
        "arxiv_id": old.get("arxiv_id", ""),
        "status": "ready",
        "old_title": old.get("title", ""),
        "new_title": meta["title"],
        "author_count": len(meta.get("authors", [])),
        "abstract_len": len(meta.get("summary", "")),
        "published": meta.get("published", ""),
        "doi": meta.get("doi", ""),
        "pdf_attachment_count": old.get("pdf_attachment_count", 0),
        "old_pdf_attachment_key": (old.get("attachments") or [{}])[0].get("key", "") if old.get("attachments") else "",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-items", type=Path, default=DEFAULT_AUDIT_ITEMS)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--collection", default="ZJK4PK4G")
    parser.add_argument("--zotero-storage", type=Path, default=DEFAULT_ZOTERO_STORAGE)
    parser.add_argument("--zotero-db", type=Path, default=DEFAULT_ZOTERO_DB)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--old-key", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--write-strategy", choices=["web-update", "connector-create"], default="web-update")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = vault_root()
    audit_items = args.audit_items if args.audit_items.is_absolute() else root / args.audit_items
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = [
        row
        for row in read_jsonl(audit_items)
        if row.get("repair_bucket") == "arxiv_metadata_reimport_or_enrich"
        and not row.get("duplicate_candidates")
        and row.get("arxiv_id")
    ]
    if args.old_key:
        wanted = set(args.old_key)
        rows = [row for row in rows if row.get("zotero_key") in wanted]
    if args.offset:
        rows = rows[args.offset :]
    if args.limit:
        rows = rows[: args.limit]

    arxiv_ids = sorted({str(row["arxiv_id"]) for row in rows})
    metadata = fetch_arxiv_metadata(arxiv_ids) if arxiv_ids else {}
    plan_rows = [item_plan(row, metadata.get(str(row["arxiv_id"]))) for row in rows]

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    plan_path = out_dir / f"arxiv_repair_plan_{stamp}.jsonl"
    summary_path = out_dir / f"arxiv_repair_summary_{stamp}.json"
    mapping_path = out_dir / f"arxiv_repair_mapping_{stamp}.jsonl"
    write_jsonl(plan_path, plan_rows)

    apply_results: list[dict[str, Any]] = []
    if args.apply:
        if not args.yes:
            raise SystemExit("--apply requires --yes")
        if mapping_path.exists():
            mapping_path.unlink()
        for row in rows:
            meta = metadata.get(str(row["arxiv_id"]))
            if not meta:
                result = {
                    "old_zotero_key": row["zotero_key"],
                    "arxiv_id": row["arxiv_id"],
                    "status": "skipped_metadata_missing",
                }
                apply_results.append(result)
                append_jsonl(mapping_path, result)
                continue
            try:
                if args.write_strategy == "connector-create":
                    result = connector_import_one(
                        row,
                        meta,
                        collection_key=args.collection,
                        storage_dir=args.zotero_storage,
                    )
                    result["new_zotero_key"] = observe_new_key(row["zotero_key"], args.zotero_db)
                else:
                    result = web_update_one(row, meta, collection_key=args.collection)
                apply_results.append(result)
                append_jsonl(mapping_path, result)
                print(json.dumps({"progress": len(apply_results), **result}, ensure_ascii=False), flush=True)
            except (RuntimeError, urllib.error.URLError, OSError) as exc:
                result = {
                    "old_zotero_key": row["zotero_key"],
                    "arxiv_id": row["arxiv_id"],
                    "status": "failed",
                    "error": f"{type(exc).__name__}:{str(exc)[:300]}",
                }
                apply_results.append(result)
                append_jsonl(mapping_path, result)
                print(json.dumps({"progress": len(apply_results), **result}, ensure_ascii=False), flush=True)

    summary = {
        "generated_at": utc_now(),
        "mode": "apply" if args.apply else "dry_run",
        "write_strategy": args.write_strategy if args.apply else "",
        "selected_rows": len(rows),
        "metadata_found": sum(1 for row in rows if str(row["arxiv_id"]) in metadata),
        "metadata_missing": sum(1 for row in rows if str(row["arxiv_id"]) not in metadata),
        "ready_rows": sum(1 for row in plan_rows if row["status"] == "ready"),
        "apply_created": sum(1 for row in apply_results if row.get("status") == "created"),
        "apply_updated_in_place": sum(1 for row in apply_results if row.get("status") == "updated_in_place"),
        "apply_failed": sum(1 for row in apply_results if row.get("status") == "failed"),
        "outputs": {
            "plan_jsonl": str(plan_path),
            "summary_json": str(summary_path),
            "mapping_jsonl": str(mapping_path) if args.apply else "",
        },
    }
    write_json(summary_path, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
