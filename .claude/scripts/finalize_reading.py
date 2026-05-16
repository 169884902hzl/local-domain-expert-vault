"""Write a completed reading analysis back into a literature note."""
from __future__ import annotations

import argparse
import re
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
PLACEHOLDER_TEXT = "待精读补充"
WAITING_TEXT = "待精读"
REQUIRED_ANALYSIS_SECTIONS = [
    "## 证据元数据",
    "## Problem",
    "## 关键贡献",
    "## Method",
    "## Experiments",
    "## Limitations",
    "## Key Takeaways",
    "## 结构化提取",
    "## 本地引用关系",
]

SECTION_ALIASES = {
    "## 证据元数据": ["Evidence Metadata", "证据元数据"],
    "## Problem": ["Problem", "问题"],
    "## 关键贡献": ["Key Contributions", "关键贡献"],
    "## Method": ["Method", "方法"],
    "## Experiments": ["Experiments", "实验"],
    "## Limitations": ["Limitations", "局限性"],
    "## Key Takeaways": ["Key Takeaways", "启发", "要点"],
    "## 结构化提取": ["结构化提取", "Structured Extraction"],
    "## 本地引用关系": ["本地引用关系", "Local Citation Links", "Related Papers"],
}


def find_note_by_key(zotero_key: str) -> Path | None:
    pattern = re.compile(rf'^zotero_key:\s*"?{re.escape(zotero_key)}"?\s*$', re.MULTILINE)
    for path in sorted(TOPICS_DIR.glob("*.md")):
        if pattern.search(path.read_text(encoding="utf-8")):
            return path
    return None


def extract_sections(markdown: str) -> dict[str, str]:
    sections = {}
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        for canonical, aliases in SECTION_ALIASES.items():
            if heading in aliases:
                sections[canonical] = body
    return sections


def structured_field_name(line: str) -> str | None:
    if not line.startswith("-") or ":" not in line:
        return None
    name = line[1:].split(":", 1)[0].strip().strip("*").strip()
    return name or None


def extract_metadata_summary(metadata: str) -> str | None:
    for line in metadata.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        normalized = key.strip().strip("*").strip().lower()
        if normalized in {"summary", "one-line summary", "一句话总结", "中文摘要"}:
            summary = value.strip().strip('"')
            return summary or None
    return None


def validate_analysis(sections: dict[str, str], schema: dict) -> None:
    missing = [heading for heading in REQUIRED_ANALYSIS_SECTIONS if heading not in sections]
    if missing:
        raise ValueError("analysis missing required sections: " + ", ".join(missing))

    structured_body = sections["## 结构化提取"]
    if PLACEHOLDER_TEXT in structured_body or WAITING_TEXT in structured_body:
        raise ValueError("analysis structured extraction still contains waiting placeholders")
    names = [
        name
        for line in structured_body.splitlines()
        if (name := structured_field_name(line.strip()))
    ]
    required_fields = schema["literature"].get("structured_fields", [])
    missing_fields = [field for field in required_fields if field not in names]
    if missing_fields:
        raise ValueError("analysis missing structured fields: " + ", ".join(missing_fields))

    metadata = sections["## 证据元数据"]
    for required in ["Fulltext Quality", "Evidence Coverage", "Confidence", "Summary"]:
        if required not in metadata:
            raise ValueError(f"analysis Evidence Metadata missing: {required}")


def replace_or_insert_section(body: str, heading: str, section_body: str) -> str:
    new_section = f"{heading}\n\n{section_body.strip()}\n"
    pattern = re.compile(rf"(?:^|\n){re.escape(heading)}\n\n.*?(?=\n## |\Z)", re.DOTALL)
    match = pattern.search(body)
    if match:
        prefix = "\n" if match.group(0).startswith("\n") else ""
        return body[: match.start()] + prefix + new_section.rstrip() + body[match.end() :]
    related = re.search(r"\n## 相关概念\n", body)
    if related:
        return body[: related.start()] + "\n\n" + new_section + body[related.start() :]
    return body.rstrip() + "\n\n" + new_section


def update_frontmatter(fm_text: str, schema: dict, analysis_summary: str | None = None) -> str:
    fields = parse_frontmatter_map(fm_text)
    for key, value in list(fields.items()):
        if key == "tags":
            fields[key] = parse_list_value(value)
        else:
            fields[key] = value.strip('"')
    fields["status"] = "done"
    fields["updated"] = today_iso()
    if analysis_summary:
        fields["summary"] = analysis_summary
    return render_frontmatter("literature", fields, schema)


def finalize_content(content: str, analysis: str, schema: dict) -> str:
    parsed = extract_frontmatter(content)
    if not parsed:
        raise ValueError("target note has no frontmatter")
    sections = extract_sections(analysis)
    validate_analysis(sections, schema)

    fm_text, body = parsed
    for heading in SECTION_ALIASES:
        if heading in sections:
            body = replace_or_insert_section(body, heading, sections[heading])
    frontmatter = update_frontmatter(fm_text, schema, extract_metadata_summary(sections["## 证据元数据"]))
    return frontmatter + body.lstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zotero_key", help="Zotero item key for the target literature note.")
    parser.add_argument("--analysis", required=True, type=Path, help="Markdown file containing the completed reading analysis.")
    args = parse_args_with_write_options(parser)

    target = find_note_by_key(args.zotero_key)
    if not target:
        safe_print(f"ERROR: No literature note found for zotero_key={args.zotero_key}")
        return 1
    if not args.analysis.exists():
        safe_print(f"ERROR: Analysis file not found: {args.analysis}")
        return 1

    schema = load_schema()
    content = target.read_text(encoding="utf-8")
    analysis = args.analysis.read_text(encoding="utf-8")
    try:
        new_content = finalize_content(content, analysis, schema)
    except ValueError as exc:
        safe_print(f"ERROR: {exc}")
        return 1
    safe_write(target, new_content, dry_run=args.dry_run, backup=not args.no_backup)
    safe_print(f"FINALIZED: {target.relative_to(vault_path())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
