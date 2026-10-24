"""Reset completed literature readings back to clean stubs for rereading."""
from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime
from pathlib import Path

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_args_with_write_options,
    parse_frontmatter_map,
    parse_list_value,
    render_frontmatter,
    safe_print,
    safe_write,
    today_iso,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
READINGS_DIR = vault_path("raw", "readings")
RESET_STATUSES = {"done", "reading"}


def section_map(body: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = "## " + match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[heading] = body[start:end].strip()
    return sections


def list_section(sections: dict[str, str], heading: str) -> str:
    value = sections.get(heading, "").strip()
    return value if value else "-"


def update_frontmatter(fm_text: str, schema: dict) -> str:
    fields = parse_frontmatter_map(fm_text)
    for key, value in list(fields.items()):
        if key == "tags":
            fields[key] = parse_list_value(value)
        else:
            fields[key] = value.strip('"')
    fields["status"] = "stub"
    fields["updated"] = today_iso()
    return render_frontmatter("literature", fields, schema)


def reset_body(body: str, zotero_key: str, schema: dict) -> str:
    sections = section_map(body)
    structured_fields = schema["literature"].get("structured_fields", [])
    structured_lines = "\n".join(f"- {field}: 待精读补充" for field in structured_fields)
    return (
        "## 摘要\n\n"
        f"{sections.get('## 摘要', '').strip()}\n\n"
        "## 中文简述\n\n"
        f"{sections.get('## 中文简述', '').strip()}\n\n"
        "## 证据元数据\n\n"
        "- Fulltext Quality: 待精读补充\n"
        "- Evidence Coverage: 待精读补充\n"
        "- Confidence: 待精读补充\n"
        "- Summary: 待精读补充\n\n"
        "## 关键贡献\n\n"
        f"（待精读 - 在 Claudian 中说 \"精读 {zotero_key}\" 即可生成完整分析）\n\n"
        "## 结构化提取\n\n"
        f"{structured_lines}\n\n"
        "## 本地引用关系\n\n"
        "-\n\n"
        "## 相关概念\n\n"
        f"{list_section(sections, '## 相关概念')}\n\n"
        "## 相关研究者\n\n"
        f"{list_section(sections, '## 相关研究者')}\n"
    )


def reset_note(path: Path, schema: dict, *, dry_run: bool, backup: bool) -> bool:
    content = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(content)
    if not parsed:
        safe_print(f"SKIP no frontmatter: {path.relative_to(vault_path())}")
        return False
    fm_text, body = parsed
    fields = parse_frontmatter_map(fm_text)
    status = fields.get("status", "").strip('"')
    if status not in RESET_STATUSES:
        return False
    zotero_key = fields.get("zotero_key", "").strip('"')
    new_content = update_frontmatter(fm_text, schema) + reset_body(body, zotero_key, schema)
    return safe_write(path, new_content, dry_run=dry_run, backup=backup)


def archive_readings(*, dry_run: bool) -> Path | None:
    if not READINGS_DIR.exists():
        return None
    files = [path for path in READINGS_DIR.iterdir() if path.is_file()]
    if not files:
        return None
    archive_dir = vault_path("raw", f"readings_legacy_{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    if dry_run:
        safe_print(f"DRY-RUN archive {len(files)} files: {READINGS_DIR.relative_to(vault_path())} -> {archive_dir.relative_to(vault_path())}")
        return archive_dir
    archive_dir.mkdir(parents=True, exist_ok=False)
    for path in files:
        shutil.move(str(path), str(archive_dir / path.name))
    safe_print(f"ARCHIVED {len(files)} files: {archive_dir.relative_to(vault_path())}")
    return archive_dir


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-archive-readings", action="store_true", help="Do not move raw/readings files to a legacy directory.")
    args = parse_args_with_write_options(parser)

    schema = load_schema()
    changed = 0
    for path in sorted(TOPICS_DIR.glob("*.md")):
        if reset_note(path, schema, dry_run=args.dry_run, backup=not args.no_backup):
            changed += 1
    if not args.no_archive_readings:
        archive_readings(dry_run=args.dry_run)
    safe_print(f"Done. Reset topic notes: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
