"""Shared helpers for the literature knowledge-base maintenance scripts."""
from __future__ import annotations

import json
import re
import shutil
import sys
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parents[1]
BACKUP_STAMP = datetime.now().strftime("%Y%m%d-%H%M%S")


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="backslashreplace")


def safe_print(message: object) -> None:
    text = str(message)
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="backslashreplace").decode(encoding), flush=True)


@lru_cache(maxsize=1)
def load_schema() -> dict[str, Any]:
    with (SCRIPT_DIR / "schema.json").open(encoding="utf-8") as f:
        return json.load(f)


def today_iso() -> str:
    return date.today().isoformat()


def parse_args_with_write_options(parser):
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files.")
    parser.add_argument("--no-backup", action="store_true", help="Do not create backups before writing.")
    return parser.parse_args()


def vault_path(*parts: str) -> Path:
    return VAULT_ROOT.joinpath(*parts)


def _quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _format_list(values: list[Any]) -> str:
    formatted = []
    for value in values:
        text = str(value)
        if re.fullmatch(r"[A-Za-z0-9_-]+", text):
            formatted.append(text)
        else:
            formatted.append(_quote(text))
    return "[" + ", ".join(formatted) + "]"


def format_frontmatter_value(value: Any) -> str:
    if isinstance(value, list):
        return _format_list(value)
    if value is None:
        return '""'
    text = str(value)
    if "\n" in text or "\r" in text:
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        return "|\n" + "\n".join("  " + line for line in normalized.split("\n"))
    return _quote(text)


def render_frontmatter(note_type: str, data: dict[str, Any], schema: dict[str, Any] | None = None) -> str:
    schema = schema or load_schema()
    order = schema[note_type]["canonical_order"]
    lines = ["---"]
    for key in order:
        if key in data:
            lines.append(f"{key}: {format_frontmatter_value(data[key])}")
    for key, value in data.items():
        if key not in order:
            lines.append(f"{key}: {format_frontmatter_value(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def extract_frontmatter(text: str) -> tuple[str, str] | None:
    match = re.match(r"^---\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not match:
        return None
    return match.group(1), match.group(2)


def parse_frontmatter_map(fm_text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in fm_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def parse_list_value(value: str) -> list[str]:
    raw = value.strip().strip("[]")
    if not raw:
        return []
    return [item.strip().strip('"') for item in raw.split(",") if item.strip()]


def frontmatter_status(text: str) -> str | None:
    parsed = extract_frontmatter(text)
    if not parsed:
        return None
    fields = parse_frontmatter_map(parsed[0])
    status = fields.get("status")
    if status is None:
        return None
    return status.strip().strip('"')


def safe_write(path: Path, content: str, *, dry_run: bool = False, backup: bool = True) -> bool:
    path = Path(path)
    old_content = path.read_text(encoding="utf-8") if path.exists() else None
    if old_content == content:
        safe_print(f"UNCHANGED: {path.relative_to(VAULT_ROOT)}")
        return False

    rel = path.relative_to(VAULT_ROOT)
    action = "create" if old_content is None else "update"
    if dry_run:
        safe_print(f"DRY-RUN {action}: {rel}")
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    if backup and path.exists():
        backup_path = VAULT_ROOT / ".claude" / "backups" / BACKUP_STAMP / rel
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_path)
    # This vault is often backed by a synced/removable Windows drive where
    # os.replace and temp-file deletion can be denied. Backups already provide
    # rollback, so use direct UTF-8 writes for predictable maintenance runs.
    path.write_text(content, encoding="utf-8")
    safe_print(f"{action.upper()}: {rel}")
    return True
