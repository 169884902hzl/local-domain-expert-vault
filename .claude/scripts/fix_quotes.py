"""Fix double-quoted topic frontmatter values."""
from __future__ import annotations

import argparse

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_args_with_write_options,
    parse_frontmatter_map,
    parse_list_value,
    render_frontmatter,
    safe_write,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")


def strip_extra_quotes(value: str) -> str:
    return value.strip().strip('"')


def rebuild_content(content: str, schema: dict) -> str:
    parsed = extract_frontmatter(content)
    if not parsed:
        return content
    fm_text, body = parsed
    raw_fields = parse_frontmatter_map(fm_text)
    fields = {}
    for key, value in raw_fields.items():
        if key == "tags":
            fields[key] = parse_list_value(value)
        else:
            fields[key] = strip_extra_quotes(value)
    frontmatter = render_frontmatter("literature", fields, schema)
    return frontmatter + (body if body.startswith("\n") else body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args_with_write_options(parser)
    schema = load_schema()

    fixed = 0
    for path in sorted(TOPICS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        new_content = rebuild_content(content, schema)
        if new_content != content:
            if safe_write(path, new_content, dry_run=args.dry_run, backup=not args.no_backup):
                fixed += 1
    print(f"Done. Fixed: {fixed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
