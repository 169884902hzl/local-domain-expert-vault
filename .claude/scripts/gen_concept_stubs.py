"""Generate concept stub pages from the schema tag taxonomy."""
from __future__ import annotations

import argparse

from kb_common import (
    load_schema,
    parse_args_with_write_options,
    render_frontmatter,
    safe_write,
    today_iso,
    vault_path,
)


CONCEPTS_DIR = vault_path("wiki", "concepts")


def concept_map(schema: dict) -> dict[str, dict]:
    concepts = {}
    for tag, info in schema["literature"]["tag_taxonomy"].items():
        concept = info.get("concept")
        if not concept:
            continue
        concepts[tag] = {
            "file": f"{concept}.md",
            "title": info.get("title", concept),
            "summary": info.get("summary", info.get("cn", "")),
            "aliases": info.get("aliases", [tag]),
            "key_ideas": info.get("key_ideas", []),
        }
    return concepts


def render_concept(tag: str, info: dict, schema: dict, run_date: str) -> str:
    frontmatter = render_frontmatter(
        "concept",
        {
            "title": info["title"],
            "tags": ["concept", tag],
            "created": run_date,
            "updated": run_date,
            "type": "concept",
            "status": "stub",
            "summary": info["summary"],
            "aliases": info["aliases"],
        },
        schema,
    )
    key_ideas = info.get("key_ideas") or ["待补充"]
    key_ideas_md = "\n".join(f"- {idea}" for idea in key_ideas)
    return (
        frontmatter
        + "\n"
        + "## Definition\n\n"
        + f"{info['summary']}\n\n"
        + "## Key Ideas\n\n"
        + f"{key_ideas_md}\n\n"
        + "## Related Papers\n\n"
        + "-\n\n"
        + "## Related Concepts\n\n"
        + "-\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args_with_write_options(parser)
    schema = load_schema()
    run_date = today_iso()

    created = 0
    skipped = 0
    for tag, info in sorted(concept_map(schema).items()):
        path = CONCEPTS_DIR / info["file"]
        if path.exists():
            skipped += 1
            continue
        content = render_concept(tag, info, schema, run_date)
        if safe_write(path, content, dry_run=args.dry_run, backup=not args.no_backup):
            created += 1
    print(f"Done. Created: {created}, Skipped (existing): {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
