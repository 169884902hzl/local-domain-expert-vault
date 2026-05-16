"""Ensure every literature note has auditable structured-reading sections."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_frontmatter_map,
    parse_args_with_write_options,
    safe_write,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
STRUCTURED_HEADING = "## 结构化提取"
CITATION_HEADING = "## 本地引用关系"
KEY_CONTRIB_HEADING = "## 关键贡献"
EN_KEY_CONTRIB_HEADING = "## Key Contributions"
PLACEHOLDER = "待精读补充"
OLD_ABSTRACT_PLACEHOLDER = "暂无摘要，待精读时补充"
DONE_ABSTRACT_PLACEHOLDER = "Zotero 未提供摘要；详见下方精读分析。"


def section_pattern(heading: str) -> re.Pattern[str]:
    return re.compile(rf"(?:^|\n){re.escape(heading)}\n\n.*?(?=\n## |\Z)", re.DOTALL)


def structured_template(schema: dict) -> str:
    fields = schema["literature"].get("structured_fields", [])
    lines = [STRUCTURED_HEADING, ""]
    lines.extend(f"- {field}: {PLACEHOLDER}" for field in fields)
    return "\n".join(lines)


def citation_template() -> str:
    return f"{CITATION_HEADING}\n\n-"


def structured_field_name(line: str) -> str | None:
    if not line.startswith("-") or ":" not in line:
        return None
    name = line[1:].split(":", 1)[0].strip().strip("*").strip()
    return name or None


def is_placeholder_line(line: str) -> bool:
    return PLACEHOLDER in line


def clean_structured_section(section: str, schema: dict) -> str:
    fields = schema["literature"].get("structured_fields", [])
    by_field: dict[str, list[str]] = {field: [] for field in fields}
    extras: list[str] = []
    for line in section.splitlines()[2:]:
        name = structured_field_name(line.strip())
        if name in by_field:
            by_field[name].append(line.rstrip())
        elif line.strip():
            extras.append(line.rstrip())

    lines = [STRUCTURED_HEADING, ""]
    for field in fields:
        candidates = by_field[field]
        chosen = next((line for line in candidates if not is_placeholder_line(line)), None)
        lines.append(chosen or (candidates[0] if candidates else f"- {field}: {PLACEHOLDER}"))
    if extras:
        lines.extend(["", *extras])
    return "\n".join(lines)


def insert_before_related(body: str, section: str) -> str:
    match = re.search(r"\n## 相关概念\n", body)
    if match:
        return body[: match.start()] + "\n\n" + section + "\n" + body[match.start() :]
    return body.rstrip() + "\n\n" + section + "\n"


def ensure_structured_fields(body: str, schema: dict) -> str:
    template = structured_template(schema)
    if STRUCTURED_HEADING not in body:
        return insert_before_related(body, template)

    match = section_pattern(STRUCTURED_HEADING).search(body)
    if not match:
        return body

    section = match.group(0).lstrip("\n").rstrip()
    new_section = clean_structured_section(section, schema)
    existing = {
        name
        for line in new_section.splitlines()
        if (name := structured_field_name(line.strip()))
    }
    missing = [field for field in schema["literature"].get("structured_fields", []) if field not in existing]
    if not missing and new_section == section:
        return body

    additions = "\n".join(f"- {field}: {PLACEHOLDER}" for field in missing)
    if additions:
        new_section = new_section.rstrip() + "\n" + additions
    return body[: match.start()] + ("\n" if match.group(0).startswith("\n") else "") + new_section + body[match.end() :]


def ensure_citation_section(body: str) -> str:
    if CITATION_HEADING in body:
        return body
    return insert_before_related(body, citation_template())


def clean_done_placeholders(body: str, status: str) -> str:
    if status != "done":
        return body
    body = body.replace(OLD_ABSTRACT_PLACEHOLDER, DONE_ABSTRACT_PLACEHOLDER)

    key_match = section_pattern(KEY_CONTRIB_HEADING).search(body)
    en_match = section_pattern(EN_KEY_CONTRIB_HEADING).search(body)
    if key_match and en_match:
        key_section = key_match.group(0).lstrip("\n").rstrip()
        en_lines = en_match.group(0).lstrip("\n").split("\n", 2)
        en_body = en_lines[2].strip() if len(en_lines) == 3 else ""
        if "待精读" in key_section and en_body:
            new_key_section = f"{KEY_CONTRIB_HEADING}\n\n{en_body}"
            body = body[: key_match.start()] + ("\n" if key_match.group(0).startswith("\n") else "") + new_key_section + body[key_match.end() :]
            en_match = section_pattern(EN_KEY_CONTRIB_HEADING).search(body)
        if en_match:
            body = body[: en_match.start()] + body[en_match.end() :]
    return body


def ensure_content(content: str, schema: dict) -> str:
    parsed = extract_frontmatter(content)
    if not parsed:
        return content
    fm_text, body = parsed
    fields = parse_frontmatter_map(fm_text)
    status = fields.get("status", "").strip('"')
    body = clean_done_placeholders(body, status)
    body = ensure_structured_fields(body, schema)
    body = ensure_citation_section(body)
    return "---\n" + fm_text + "\n---\n" + body.lstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Optional topic note paths. Defaults to all wiki/topics/*.md.")
    args = parse_args_with_write_options(parser)
    schema = load_schema()

    paths = args.paths or sorted(TOPICS_DIR.glob("*.md"))
    changed = 0
    for path in paths:
        if not path.is_absolute():
            path = vault_path(path)
        content = path.read_text(encoding="utf-8")
        new_content = ensure_content(content, schema)
        if new_content != content:
            if safe_write(path, new_content, dry_run=args.dry_run, backup=not args.no_backup):
                changed += 1
    print(f"Done. Structured notes updated: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
