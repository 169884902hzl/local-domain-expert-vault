"""Repair invalid Zotero item keys created for stored PDF attachments.

This is a one-time local repair for Zotero storage folders whose item keys
contain characters Zotero rejects, such as 0, 1, or O. It only targets stored
PDF attachment items and refuses to write while Zotero Desktop is running.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import random
import re
import shutil
import sqlite3
import subprocess
from typing import Any

from kb_common import safe_print, vault_path
from zotero_import import zotero_data_dir


VALID_KEY_RE = re.compile(r"^[23456789ABCDEFGHIJKLMNPQRSTUVWXYZ]{8}$")
VALID_KEY_ALPHABET = "23456789ABCDEFGHIJKLMNPQRSTUVWXYZ"


def db_path() -> Path:
    return zotero_data_dir() / "zotero.sqlite"


def storage_dir() -> Path:
    return zotero_data_dir() / "storage"


def backup_dir() -> Path:
    return vault_path("projects", "arxiv-daily", "zotero-db-backups")


def zotero_desktop_running() -> bool:
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                "Get-Process -Name zotero -ErrorAction SilentlyContinue | "
                "Where-Object { $_.Path -like '*Zotero*' } | Select-Object -First 1 | "
                "ForEach-Object { 'running' }",
            ],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return True
    return "running" in result.stdout


def connect(write: bool) -> sqlite3.Connection:
    if write:
        conn = sqlite3.connect(db_path())
    else:
        uri = "file:" + str(db_path()).replace("\\", "/") + "?mode=ro&immutable=1"
        conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def invalid_stored_pdf_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list(
        conn.execute(
            """
            SELECT i.itemID, i.key, i.synced, a.parentItemID, a.path, a.storageHash
            FROM items i
            JOIN itemAttachments a ON a.itemID = i.itemID
            WHERE a.linkMode = 1
              AND a.parentItemID IS NOT NULL
              AND COALESCE(a.contentType, '') LIKE '%pdf%'
              AND COALESCE(a.storageHash, '') <> ''
            ORDER BY i.itemID
            """
        )
    )


def new_key(existing: set[str]) -> str:
    while True:
        key = "".join(random.choice(VALID_KEY_ALPHABET) for _ in range(8))
        if key not in existing:
            existing.add(key)
            return key


def build_mapping(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    existing = {str(row["key"]) for row in conn.execute("SELECT key FROM items")}
    mappings: list[dict[str, Any]] = []
    for row in invalid_stored_pdf_rows(conn):
        old_key = str(row["key"])
        if VALID_KEY_RE.match(old_key):
            continue
        replacement = new_key(existing)
        filename = str(row["path"] or "").replace("storage:", "", 1)
        old_dir = storage_dir() / old_key
        new_dir = storage_dir() / replacement
        mappings.append(
            {
                "itemID": int(row["itemID"]),
                "parentItemID": int(row["parentItemID"]),
                "old_key": old_key,
                "new_key": replacement,
                "filename": filename,
                "old_dir": str(old_dir),
                "new_dir": str(new_dir),
                "old_dir_exists": old_dir.exists(),
                "target_dir_exists": new_dir.exists(),
            }
        )
    return mappings


def backup_database() -> Path:
    backup_dir().mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = backup_dir() / f"zotero-before-invalid-key-fix-{stamp}.sqlite"
    shutil.copy2(db_path(), target)
    return target


def apply_mapping(mappings: list[dict[str, Any]]) -> None:
    conn = connect(write=True)
    try:
        with conn:
            for item in mappings:
                old_dir = Path(item["old_dir"])
                new_dir = Path(item["new_dir"])
                if new_dir.exists():
                    raise RuntimeError(f"target storage dir already exists: {new_dir}")
                if old_dir.exists():
                    old_dir.rename(new_dir)
                conn.execute(
                    "UPDATE items SET key = ?, synced = 0, version = 0 WHERE itemID = ?",
                    (item["new_key"], item["itemID"]),
                )
    finally:
        conn.close()


def verify_no_invalid_keys() -> int:
    conn = connect(write=False)
    try:
        count = 0
        for row in invalid_stored_pdf_rows(conn):
            if not VALID_KEY_RE.match(str(row["key"])):
                count += 1
        return count
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report", default="")
    parser.add_argument("--write-even-if-zotero-running", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and zotero_desktop_running() and not args.write_even_if_zotero_running:
        safe_print("ERROR: Zotero Desktop is running. Close Zotero before writing invalid key repairs.")
        return 2

    conn = connect(write=False)
    try:
        mappings = build_mapping(conn)
    finally:
        conn.close()

    backup = ""
    if not args.dry_run and mappings:
        backup = str(backup_database())
        apply_mapping(mappings)

    report = {
        "dry_run": args.dry_run,
        "invalid_key_count": len(mappings),
        "backup_path": backup,
        "remaining_invalid_keys": verify_no_invalid_keys() if not args.dry_run else len(mappings),
        "mappings": mappings,
    }

    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        safe_print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        safe_print(
            f"SUMMARY invalid_key_count={report['invalid_key_count']} "
            f"remaining_invalid_keys={report['remaining_invalid_keys']} dry_run={args.dry_run}"
        )
        if backup:
            safe_print(f"BACKUP {backup}")
    return 0 if report["remaining_invalid_keys"] == 0 or args.dry_run else 1


if __name__ == "__main__":
    raise SystemExit(main())
