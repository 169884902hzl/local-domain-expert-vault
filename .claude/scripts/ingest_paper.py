"""One-step Zotero-to-Obsidian ingestion for a single paper.

Fetches Zotero metadata, creates or refreshes the literature stub, then runs the
local maintenance pipeline so the note is immediately connected to concepts and
researcher entities.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from batch_index import build_note, existing_notes_by_zotero_key, should_write_existing
from kb_common import load_schema, parse_args_with_write_options, safe_print, safe_write, today_iso, vault_path


SCRIPT_DIR = Path(__file__).resolve().parent
TOPICS_DIR = vault_path("wiki", "topics")


def env_value(name: str, default: str = "") -> str:
    value = os.environ.get(name, "").strip()
    if value or os.name != "nt":
        return value or default
    try:
        import winreg
    except ImportError:
        return default
    for root, subkey in (
        (winreg.HKEY_CURRENT_USER, "Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    ):
        try:
            with winreg.OpenKey(root, subkey) as key:
                value, _ = winreg.QueryValueEx(key, name)
        except OSError:
            continue
        if str(value).strip():
            return str(value).strip()
    return default


def fetch_item(zotero_key: str) -> dict[str, Any]:
    url = f"http://localhost:23119/api/users/0/items/{zotero_key}?format=json"
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        local_error = exc
    item = fetch_item_web(zotero_key)
    if item:
        safe_print(f"FETCHED_FROM_ZOTERO_WEB_API: {zotero_key}")
        return item
    safe_print(f"ERROR: Cannot fetch Zotero item {zotero_key} from localhost:23119 or Zotero Web API.")
    safe_print("  Make sure Zotero is running and synced, or set ZOTERO_API_KEY and ZOTERO_USER_ID.")
    safe_print(f"  Local detail: {local_error}")
    raise SystemExit(1) from local_error


def fetch_item_web(zotero_key: str) -> dict[str, Any] | None:
    api_key = env_value("ZOTERO_API_KEY")
    user_id = env_value("ZOTERO_USER_ID") or env_value("ZOTERO_LIBRARY_ID")
    if not api_key or not user_id:
        return None
    url = f"https://api.zotero.org/users/{user_id}/items/{zotero_key}?format=json"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Zotero-API-Version": "3",
            "Zotero-API-Key": api_key,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (OSError, urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return None


def run_script(script_name: str, args: argparse.Namespace, extra: list[str] | None = None) -> None:
    command = [sys.executable, str(SCRIPT_DIR / script_name)]
    if args.dry_run:
        command.append("--dry-run")
    if args.no_backup:
        command.append("--no-backup")
    if extra:
        command.extend(extra)
    safe_print("RUN: " + " ".join(command))
    subprocess.run(command, check=True)


def ingest_one(zotero_key: str, args: argparse.Namespace) -> Path | None:
    schema = load_schema()
    item = fetch_item(zotero_key)
    filename, content = build_note(item, schema, today_iso())
    existing = existing_notes_by_zotero_key()
    path = existing.get(zotero_key, TOPICS_DIR / filename)

    if not should_write_existing(path, force_overwrite_stub=args.force_overwrite_stub):
        return path
    safe_write(path, content, dry_run=args.dry_run, backup=not args.no_backup)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zotero_key", help="Zotero item key, for example ULDP9XLR.")
    parser.add_argument(
        "--force-overwrite-stub",
        action="store_true",
        help="Overwrite an existing note only when its status is stub.",
    )
    parser.add_argument("--skip-postprocess", action="store_true", help="Only import the stub note.")
    args = parse_args_with_write_options(parser)

    path = ingest_one(args.zotero_key, args)
    if path:
        safe_print(f"INGESTED_OR_FOUND: {path.relative_to(vault_path())}")

    if not args.skip_postprocess:
        run_script("fix_abstracts.py", args)
        run_script("ensure_literature_structure.py", args)
        run_script("gen_entity_stubs.py", args, ["--include-first-authors"])
        run_script("fix_wikilinks.py", args)
        run_script("backfill_concepts.py", args)
        run_script("extract_citation_links.py", args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
