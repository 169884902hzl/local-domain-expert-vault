"""Make auto-created Zotero linked PDF attachment paths absolute."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from zotero_import import WEB_API, _env, _web_headers


AUTO_TAG = "local-linked-pdf"


def _get_json(url: str, api_key: str, timeout: int = 30) -> Any:
    req = urllib.request.Request(url, headers={**_web_headers(api_key), "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode("utf-8")
        return json.loads(text) if text.strip() else {}


def _put_json(url: str, payload: Any, headers: dict[str, str], timeout: int = 30) -> int:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req_headers = {**headers, "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=body, headers=req_headers, method="PUT")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status


def iter_tagged_attachments(user_id: str, api_key: str, *, tag: str = AUTO_TAG) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    start = 0
    limit = 100
    while True:
        url = (
            f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items"
            f"?tag={urllib.parse.quote(tag)}&limit={limit}&start={start}&format=json"
        )
        batch = _get_json(url, api_key)
        if not isinstance(batch, list):
            break
        items.extend(batch)
        if len(batch) < limit:
            break
        start += limit
    return items


DEFAULT_ASCII_CACHE = Path(os.environ.get("ZOTERO_LOCAL_PDF_CACHE", r".local\zotero-pdf-cache"))


def _absolute_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return vault_path(*path.parts)


def _target_path(source_path: Path, target_dir: Path | None) -> Path:
    if target_dir is None:
        return source_path
    return target_dir / source_path.name


def fix_paths(*, dry_run: bool, report_path: Path | None = None, target_dir: Path | None = None) -> dict[str, Any]:
    api_key = _env("ZOTERO_API_KEY")
    user_id = _env("ZOTERO_USER_ID") or _env("ZOTERO_LIBRARY_ID")
    if not api_key:
        raise RuntimeError("missing ZOTERO_API_KEY")
    if not user_id:
        raise RuntimeError("missing ZOTERO_LIBRARY_ID or ZOTERO_USER_ID")

    results: list[dict[str, str]] = []
    for item in iter_tagged_attachments(user_id, api_key):
        key = str(item.get("key") or "")
        data = item.get("data", {}) if isinstance(item, dict) else {}
        path_value = str(data.get("path") or "")
        link_mode = str(data.get("linkMode") or "")
        content_type = str(data.get("contentType") or "")
        if not key or link_mode != "linked_file" or content_type != "application/pdf":
            results.append({"key": key, "result": "skipped_not_linked_pdf", "path": path_value})
            continue
        if not path_value:
            results.append({"key": key, "result": "skipped_missing_path", "path": ""})
            continue
        absolute = _absolute_path(path_value)
        target = _target_path(absolute, target_dir)
        exists = absolute.exists()
        target_exists = target.exists()
        if Path(path_value).is_absolute() and target == absolute:
            results.append({"key": key, "result": "already_absolute" if exists else "already_absolute_missing_file", "path": str(absolute)})
            continue
        if not exists:
            results.append({"key": key, "result": "missing_local_file", "path": str(absolute)})
            continue
        if dry_run:
            result = "would_update_path"
            if target_dir and target != absolute:
                result = "would_copy_and_update_path" if not target_exists else "would_update_path_to_existing_target"
            results.append({"key": key, "result": result, "old_path": path_value, "source_path": str(absolute), "path": str(target)})
            continue
        if target_dir and target != absolute and not target_exists:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(absolute, target)
        data["path"] = str(target)
        item_url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(key)}"
        headers = {**_web_headers(api_key), "If-Unmodified-Since-Version": str(item.get("version") or "")}
        try:
            status = _put_json(item_url, data, headers, timeout=30)
            result = "updated_path" if status == 204 else f"update_unexpected_status_{status}"
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            result = f"update_failed_HTTP_{exc.code}:{detail[:120]}"
        except Exception as exc:
            result = f"update_failed:{type(exc).__name__}:{str(exc)[:120]}"
        results.append({"key": key, "result": result, "old_path": path_value, "source_path": str(absolute), "path": str(target)})

    summary: dict[str, Any] = {"total": len(results), "by_result": {}}
    for item in results:
        result = item["result"].split(":", 1)[0]
        summary["by_result"][result] = summary["by_result"].get(result, 0) + 1
    report = {"dry_run": dry_run, "tag": AUTO_TAG, "summary": summary, "results": results}
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report", help="Write JSON report.")
    parser.add_argument("--target-dir", help=f"Copy PDFs into this directory and update Zotero paths. Default when provided without value is not supported; suggested: {DEFAULT_ASCII_CACHE}")
    args = parser.parse_args()

    report = fix_paths(
        dry_run=args.dry_run,
        report_path=Path(args.report) if args.report else None,
        target_dir=Path(args.target_dir) if args.target_dir else None,
    )
    safe_print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    failures = sum(count for result, count in report["summary"]["by_result"].items() if result.startswith(("missing", "update_failed")))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
