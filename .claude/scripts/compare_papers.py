"""Compare two local literature notes using structured local evidence only."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, vault_path


TOPICS_DIR = vault_path("wiki", "topics")
FIELDS = ["Problem", "Method", "Tasks", "Sensors", "Robot Setup", "Metrics", "Limitations", "Evidence Notes"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_note(path: Path) -> tuple[dict[str, str], str]:
    parsed = extract_frontmatter(read(path))
    if not parsed:
        return {}, read(path)
    fm_text, body = parsed
    return parse_frontmatter_map(fm_text), body


def find_note(identifier: str) -> Path | None:
    raw = Path(identifier)
    if raw.exists():
        return raw
    candidate = TOPICS_DIR / f"{identifier}.md"
    if candidate.exists():
        return candidate

    key_pattern = re.compile(rf'^zotero_key:\s*"?{re.escape(identifier)}"?\s*$', re.MULTILINE)
    for path in sorted(TOPICS_DIR.glob("*.md")):
        text = read(path)
        if key_pattern.search(text):
            return path
    matches = [path for path in sorted(TOPICS_DIR.glob("*.md")) if identifier.lower() in path.stem.lower()]
    return matches[0] if len(matches) == 1 else None


def section(body: str, heading: str) -> str:
    match = re.search(rf"(?:^|\n){re.escape(heading)}\n\n(.*?)(?=\n## |\Z)", body, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def structured_value(body: str, field: str) -> str:
    structured = section(body, "## 结构化提取")
    match = re.search(rf"^- (?:\*\*)?{re.escape(field)}(?:\*\*)?:\s*(.*)$", structured, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def short(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value[:240] + ("..." if len(value) > 240 else "")


def render_comparison(left_path: Path, right_path: Path) -> str:
    left_fields, left_body = parse_note(left_path)
    right_fields, right_body = parse_note(right_path)
    lines = [
        "# Local Paper Comparison",
        "",
        f"- A: [[{left_path.stem}]] - {left_fields.get('title', '').strip(chr(34))}",
        f"- B: [[{right_path.stem}]] - {right_fields.get('title', '').strip(chr(34))}",
        "",
        "| Aspect | A | B |",
        "|---|---|---|",
        f"| Summary | {short(left_fields.get('summary', '').strip(chr(34)))} | {short(right_fields.get('summary', '').strip(chr(34)))} |",
        f"| Tags | {left_fields.get('tags', '')} | {right_fields.get('tags', '')} |",
    ]
    for field in FIELDS:
        lines.append(f"| {field} | {short(structured_value(left_body, field))} | {short(structured_value(right_body, field))} |")

    detailed_headings = {
        "## Method": "Detailed Method",
        "## Experiments": "Detailed Experiments",
        "## Limitations": "Detailed Limitations",
        "## Key Takeaways": "Detailed Key Takeaways",
        "## 本地引用关系": "Local Citation Links",
    }
    for heading, label in detailed_headings.items():
        left = section(left_body, heading)
        right = section(right_body, heading)
        if left or right:
            lines.append(f"| {label} | {short(left)} | {short(right)} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", help="First paper: zotero_key, topic stem, or path")
    parser.add_argument("right", help="Second paper: zotero_key, topic stem, or path")
    args = parser.parse_args()

    left = find_note(args.left)
    right = find_note(args.right)
    if not left or not right:
        safe_print("ERROR: Could not resolve both papers locally.")
        safe_print(f"  left={args.left} -> {left or 'not found'}")
        safe_print(f"  right={args.right} -> {right or 'not found'}")
        return 1
    safe_print(render_comparison(left, right))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
