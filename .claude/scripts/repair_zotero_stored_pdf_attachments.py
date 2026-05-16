"""Repair old Zotero linked/missing arXiv PDF attachments into stored attachments.

This is intentionally a local, backed-up repair path for already-created items.
Zotero's local API is read-only, and the Connector can only attach files to
items created in the same save session, so old items require Zotero to be closed
before the SQLite/storage repair is applied.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import random
import re
import shutil
import sqlite3
import string
import sys
import time
import urllib.request
from typing import Any

from kb_common import safe_print, vault_path


RUN_RE = re.compile(
    r"^- arxiv=(?P<arxiv>\S+).*?\bzotero_key=(?P<key>[A-Z0-9]+)\b.*?\bmessage=(?P<message>.*)$"
)
PDF_SYNC_PROBLEM_MARKERS = (
    "webdav_sync_note=linked_file_not_synced_by_webdav",
    "linked_pdf_fallback_failed",
    "pdf_file_upload_failed",
)
LOCAL_PATH_RE = re.compile(r"local_pdf_path=(?P<path>[^;]+)")
ARXIV_EXTRA_RE = re.compile(r"\barXiv:\s*(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)
ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE)


def zotero_dir() -> Path:
    return Path(os.environ.get("ZOTERO_DATA_DIR", str(Path.home() / "Zotero")))


def db_path() -> Path:
    return zotero_dir() / "zotero.sqlite"


def storage_dir() -> Path:
    return zotero_dir() / "storage"


def discover_run_dates() -> list[str]:
    root = vault_path("projects", "arxiv-daily")
    return sorted(path.stem.removesuffix("-run") for path in root.glob("????-??-??-run.md"))


def split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def read_run_records(run_dates: list[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for run_date in run_dates:
        path = vault_path("projects", "arxiv-daily", f"{run_date}-run.md")
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not any(marker in line for marker in PDF_SYNC_PROBLEM_MARKERS):
                continue
            match = RUN_RE.match(line)
            if not match:
                continue
            message = match.group("message")
            local_match = LOCAL_PATH_RE.search(message)
            records.append(
                {
                    "run_date": run_date,
                    "arxiv": match.group("arxiv"),
                    "key": match.group("key"),
                    "message": message,
                    "local_pdf_path": local_match.group("path").strip() if local_match else "",
                }
            )
    return records


def read_collection_linked_pdf_records(collection_key: str) -> list[dict[str, str]]:
    path = db_path()
    records: list[dict[str, str]] = []
    conn = connect(path, write=False)
    try:
        rows = conn.execute(
            """
            SELECT p.key AS parentKey, p.itemID AS parentItemID, ai.key AS attachmentKey, a.path AS localPath
            FROM itemAttachments a
            JOIN items ai ON ai.itemID = a.itemID
            JOIN items p ON p.itemID = a.parentItemID
            JOIN collectionItems ci ON ci.itemID = p.itemID
            JOIN collections c ON c.collectionID = ci.collectionID
            WHERE c.key = ?
              AND a.linkMode = 2
              AND lower(coalesce(a.contentType, '')) = 'application/pdf'
            ORDER BY p.itemID
            """,
            (collection_key,),
        ).fetchall()
        for row in rows:
            if stored_pdf_key(conn, int(row["parentItemID"])):
                continue
            fields = item_data(conn, int(row["parentItemID"]))
            arxiv_id = extract_arxiv_from_item(fields)
            if not arxiv_id:
                path_match = re.search(r"arxiv-(\d{4}\.\d{4,5})(?:v\d+)?\.pdf", str(row["localPath"]), re.IGNORECASE)
                arxiv_id = path_match.group(1) if path_match else ""
            records.append(
                {
                    "run_date": "collection",
                    "arxiv": arxiv_id,
                    "key": str(row["parentKey"]),
                    "message": f"collection_linked_pdf:{row['attachmentKey']}",
                    "local_pdf_path": str(row["localPath"] or ""),
                }
            )
    finally:
        conn.close()
    return records


def connect(path: Path, *, write: bool) -> sqlite3.Connection:
    if write:
        conn = sqlite3.connect(str(path), timeout=30)
    else:
        conn = sqlite3.connect("file:" + str(path) + "?mode=ro&immutable=1", uri=True, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    return [str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")]


def item_by_key(conn: sqlite3.Connection, key: str) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM items WHERE key = ?", (key,)).fetchone()


def item_data(conn: sqlite3.Connection, item_id: int) -> dict[str, str]:
    rows = conn.execute(
        """
        SELECT f.fieldName, v.value
        FROM itemData d
        JOIN fields f ON f.fieldID = d.fieldID
        JOIN itemDataValues v ON v.valueID = d.valueID
        WHERE d.itemID = ?
        """,
        (item_id,),
    )
    return {str(row["fieldName"]): str(row["value"]) for row in rows}


def extract_arxiv_from_item(fields: dict[str, str]) -> str:
    for name in ("extra", "url", "DOI"):
        text = fields.get(name, "")
        for pattern in (ARXIV_EXTRA_RE, ARXIV_URL_RE):
            match = pattern.search(text)
            if match:
                return match.group(1)
    return ""


def stored_pdf_key(conn: sqlite3.Connection, parent_item_id: int) -> str:
    rows = conn.execute(
        """
        SELECT i.key, a.linkMode, a.contentType, a.path, a.storageHash
        FROM itemAttachments a
        JOIN items i ON i.itemID = a.itemID
        WHERE a.parentItemID = ?
        """,
        (parent_item_id,),
    )
    for row in rows:
        link_mode = int(row["linkMode"] or 0)
        path = str(row["path"] or "").lower()
        content_type = str(row["contentType"] or "").lower()
        if link_mode != 2 and (path.startswith("storage:") or content_type == "application/pdf") and row["storageHash"]:
            return str(row["key"])
    return ""


def existing_linked_pdf_keys(conn: sqlite3.Connection, parent_item_id: int) -> list[str]:
    rows = conn.execute(
        """
        SELECT i.key
        FROM itemAttachments a
        JOIN items i ON i.itemID = a.itemID
        WHERE a.parentItemID = ? AND a.linkMode = 2 AND lower(coalesce(a.contentType, '')) = 'application/pdf'
        """,
        (parent_item_id,),
    )
    return [str(row["key"]) for row in rows]


def download_pdf(arxiv_id: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = urllib.request.Request(url, headers={"Accept": "application/pdf,*/*", "User-Agent": "zotero-stored-pdf-repair/1.0"})
    with urllib.request.urlopen(req, timeout=240) as resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        raise RuntimeError(f"downloaded data is not a PDF: {url}")
    dest.write_bytes(data)
    return dest


def safe_filename(value: str, fallback: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', " ", value).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.rstrip(". ")
    if not cleaned:
        cleaned = fallback
    if not cleaned.lower().endswith(".pdf"):
        cleaned += ".pdf"
    return cleaned[:180]


def random_key(existing: set[str]) -> str:
    # Match Zotero item key alphabet; 0, 1, and O are not valid.
    alphabet = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    while True:
        key = "".join(random.choice(alphabet) for _ in range(8))
        if key not in existing:
            existing.add(key)
            return key


def value_id(conn: sqlite3.Connection, value: str) -> int:
    row = conn.execute("SELECT valueID FROM itemDataValues WHERE value = ?", (value,)).fetchone()
    if row:
        return int(row["valueID"])
    cur = conn.execute("INSERT INTO itemDataValues(value) VALUES (?)", (value,))
    return int(cur.lastrowid)


def field_id(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute("SELECT fieldID FROM fields WHERE fieldName = ?", (name,)).fetchone()
    if not row:
        raise RuntimeError(f"missing Zotero field: {name}")
    return int(row["fieldID"])


def insert_item_data(conn: sqlite3.Connection, item_id: int, name: str, value: str) -> None:
    if not value:
        return
    conn.execute(
        "INSERT OR REPLACE INTO itemData(itemID, fieldID, valueID) VALUES (?, ?, ?)",
        (item_id, field_id(conn, name), value_id(conn, value)),
    )


def insert_attachment(
    conn: sqlite3.Connection,
    *,
    parent: sqlite3.Row,
    attachment_key: str,
    title: str,
    url: str,
    filename: str,
    md5: str,
    mtime_ms: int,
) -> int:
    now_sql = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    item_columns = table_columns(conn, "items")
    values: dict[str, Any] = {
        "itemTypeID": 3,
        "dateAdded": now_sql,
        "dateModified": now_sql,
        "clientDateModified": now_sql,
        "libraryID": int(parent["libraryID"]),
        "key": attachment_key,
        "version": 0,
        "synced": 0,
    }
    columns = [column for column in item_columns if column != "itemID" and column in values]
    cur = conn.execute(
        f"INSERT INTO items({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
        tuple(values[column] for column in columns),
    )
    item_id = int(cur.lastrowid)
    attachment_columns = table_columns(conn, "itemAttachments")
    attachment_values: dict[str, Any] = {
        "itemID": item_id,
        "parentItemID": int(parent["itemID"]),
        "linkMode": 1,
        "contentType": "application/pdf",
        "charsetID": None,
        "path": f"storage:{filename}",
        "syncState": 2,
        "storageModTime": mtime_ms,
        "storageHash": md5,
        "lastProcessedModificationTime": None,
        "lastRead": None,
    }
    cols = [column for column in attachment_columns if column in attachment_values]
    conn.execute(
        f"INSERT INTO itemAttachments({', '.join(cols)}) VALUES ({', '.join('?' for _ in cols)})",
        tuple(attachment_values[column] for column in cols),
    )
    insert_item_data(conn, item_id, "title", title)
    insert_item_data(conn, item_id, "url", url)
    insert_item_data(conn, item_id, "accessDate", now_sql)
    return item_id


def repair(records: list[dict[str, str]], *, dry_run: bool, limit: int, cache_dir: Path, cleanup_linked: bool) -> dict[str, Any]:
    path = db_path()
    if not path.exists():
        raise RuntimeError(f"Zotero DB not found: {path}")
    results: list[dict[str, Any]] = []
    processed = 0
    conn = connect(path, write=not dry_run)
    try:
        existing_keys = {str(row["key"]) for row in conn.execute("SELECT key FROM items")}
        for record in records:
            key = record["key"]
            parent = item_by_key(conn, key)
            if not parent:
                results.append({**record, "result": "missing_parent_item"})
                continue
            stored_key = stored_pdf_key(conn, int(parent["itemID"]))
            if stored_key:
                results.append({**record, "result": "exists_stored_pdf", "stored_pdf_key": stored_key})
                continue
            fields = item_data(conn, int(parent["itemID"]))
            arxiv_id = record.get("arxiv") or extract_arxiv_from_item(fields)
            if not arxiv_id:
                results.append({**record, "result": "missing_arxiv_id"})
                continue
            raw_local_pdf = str(record.get("local_pdf_path") or "").strip()
            local_pdf = Path(raw_local_pdf) if raw_local_pdf else None
            if not local_pdf or not local_pdf.is_file():
                local_pdf = cache_dir / f"arxiv-{arxiv_id}.pdf"
                if dry_run:
                    source = "would_download"
                else:
                    local_pdf = download_pdf(arxiv_id, local_pdf)
                    source = "downloaded"
            else:
                source = "existing_local_pdf"
            title = "PDF - " + (fields.get("title") or f"arXiv {arxiv_id}")[:180]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
            filename = safe_filename(f"arxiv-{arxiv_id}", f"arxiv-{arxiv_id}.pdf")
            linked_keys = existing_linked_pdf_keys(conn, int(parent["itemID"]))
            if dry_run:
                results.append(
                    {
                        **record,
                        "result": "would_create_stored_pdf",
                        "source": source,
                        "linked_pdf_keys": ",".join(linked_keys),
                    }
                )
                processed += 1
            else:
                attachment_key = random_key(existing_keys)
                target_dir = storage_dir() / attachment_key
                target_dir.mkdir(parents=True, exist_ok=False)
                target_pdf = target_dir / filename
                shutil.copy2(local_pdf, target_pdf)
                pdf_bytes = target_pdf.read_bytes()
                md5 = hashlib.md5(pdf_bytes).hexdigest()
                mtime_ms = int(target_pdf.stat().st_mtime * 1000)
                insert_attachment(
                    conn,
                    parent=parent,
                    attachment_key=attachment_key,
                    title=title,
                    url=pdf_url,
                    filename=filename,
                    md5=md5,
                    mtime_ms=mtime_ms,
                )
                if cleanup_linked and linked_keys:
                    conn.execute(
                        "UPDATE items SET synced = 0 WHERE key IN (%s)" % ",".join("?" for _ in linked_keys),
                        tuple(linked_keys),
                    )
                results.append(
                    {
                        **record,
                        "result": "created_stored_pdf",
                        "stored_pdf_key": attachment_key,
                        "source": source,
                        "storage_path": str(target_pdf),
                        "linked_pdf_keys": ",".join(linked_keys),
                    }
                )
                processed += 1
            if limit and processed >= limit:
                break
        if not dry_run:
            conn.commit()
    finally:
        conn.close()
    return {"dry_run": dry_run, "processed": processed, "results": results}


def zotero_running() -> bool:
    if os.name != "nt":
        return False
    try:
        import subprocess

        output = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "Get-Process zotero -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return bool(output.strip())
    except Exception:
        return False


def backup_db() -> Path:
    source = db_path()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = vault_path("projects", "arxiv-daily", "zotero-db-backups", f"zotero-before-stored-pdf-repair-{stamp}.sqlite")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["run-logs", "collection"], default="run-logs")
    parser.add_argument("--run-dates", default="all", help="Comma-separated run dates or 'all'.")
    parser.add_argument("--collection", default="", help="Zotero collection key. Required with --source collection.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--cache-dir", default=str(zotero_dir() / "auto-pdf-cache"))
    parser.add_argument("--report", default="")
    parser.add_argument("--write-even-if-zotero-running", action="store_true", help="Unsafe; normally refused.")
    parser.add_argument("--cleanup-linked", action="store_true", help="Mark old linked PDF attachment items unsynced for later cleanup bookkeeping.")
    args = parser.parse_args()

    run_dates = discover_run_dates() if args.run_dates.lower() == "all" else split_csv(args.run_dates)
    if args.source == "collection" and not args.collection.strip():
        safe_print("ERROR: missing_collection_key. Pass --collection or set a private local wrapper script.")
        return 2
    records = read_collection_linked_pdf_records(args.collection) if args.source == "collection" else read_run_records(run_dates)
    if not args.dry_run and zotero_running() and not args.write_even_if_zotero_running:
        safe_print("ERROR: Zotero is running. Close Zotero before applying SQLite/storage repair.")
        return 2
    backup_path = ""
    if not args.dry_run:
        backup_path = str(backup_db())
    report = repair(records, dry_run=args.dry_run, limit=args.limit, cache_dir=Path(args.cache_dir), cleanup_linked=args.cleanup_linked)
    report["run_dates"] = run_dates
    report["source"] = args.source
    report["collection"] = args.collection
    report["records_found"] = len(records)
    report["zotero_db_backup"] = backup_path
    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.json:
        safe_print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in report["results"]:
            safe_print(f"{item.get('run_date')} key={item.get('key')} arxiv={item.get('arxiv')} result={item.get('result')}")
        safe_print(f"SUMMARY records_found={len(records)} processed={report['processed']} dry_run={args.dry_run}")
        if backup_path:
            safe_print(f"BACKUP {backup_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
