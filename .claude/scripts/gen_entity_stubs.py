"""Generate entity (researcher) stub pages from authors found in topic notes."""
from __future__ import annotations

import argparse
import re
import unicodedata
from collections import Counter
from pathlib import Path

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_args_with_write_options,
    parse_frontmatter_map,
    parse_list_value,
    render_frontmatter,
    safe_write,
    today_iso,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
ENTITIES_DIR = vault_path("wiki", "entities")
MIN_PAPERS = 2


def collect_authors() -> tuple[Counter[str], dict[str, list[str]], set[str]]:
    author_counter: Counter[str] = Counter()
    author_papers: dict[str, list[str]] = {}
    first_authors: set[str] = set()
    for path in sorted(TOPICS_DIR.glob("*.md")):
        parsed = extract_frontmatter(path.read_text(encoding="utf-8"))
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        authors_str = fields.get("authors", "").strip('"')
        if not authors_str:
            continue
        authors = [author.strip() for author in authors_str.split(";") if author.strip()]
        if authors and "et al." not in authors[0]:
            first_authors.add(authors[0])
        for author in authors:
            author = author.strip()
            if not author or "et al." in author:
                continue
            author_counter[author] += 1
            author_papers.setdefault(author, []).append(path.stem)
    return author_counter, author_papers, first_authors


def slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "entity"


def base_entity_filename(author: str) -> str:
    last_name = author.split(",")[0].strip().lower()
    return f"{slugify(last_name)}.md"


def disambiguated_entity_filename(author: str) -> str:
    parts = [part.strip() for part in author.split(",", 1)]
    if len(parts) == 2 and parts[1]:
        return f"{slugify(parts[0] + '-' + parts[1])}.md"
    return f"{slugify(author)}.md"


def existing_entities() -> dict[str, Path]:
    entities: dict[str, Path] = {}
    for path in sorted(ENTITIES_DIR.glob("*.md")):
        parsed = extract_frontmatter(path.read_text(encoding="utf-8"))
        if not parsed:
            continue
        title = parse_frontmatter_map(parsed[0]).get("title", "").strip('"')
        if title:
            entities[title] = path
    return entities


def normalize_existing_entities(schema: dict, *, dry_run: bool, backup: bool) -> int:
    updated = 0
    for path in sorted(ENTITIES_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(content)
        if not parsed:
            continue
        fm_text, body = parsed
        fields = parse_frontmatter_map(fm_text)
        fields["tags"] = parse_list_value(fields.get("tags", ""))
        for key, value in list(fields.items()):
            if key != "tags":
                fields[key] = value.strip('"')
        fields.setdefault("affiliation", "")
        fields.setdefault("url", "")
        frontmatter = render_frontmatter("entity", fields, schema)
        new_content = frontmatter + "\n" + body.lstrip()
        if safe_write(path, new_content, dry_run=dry_run, backup=backup):
            updated += 1
    return updated


def target_path(author: str, entities_by_title: dict[str, Path]) -> Path | None:
    if author in entities_by_title:
        return None
    base = ENTITIES_DIR / base_entity_filename(author)
    if not base.exists():
        return base
    return ENTITIES_DIR / disambiguated_entity_filename(author)


def render_entity(author: str, papers: list[str], schema: dict, run_date: str) -> str:
    frontmatter = render_frontmatter(
        "entity",
        {
            "title": author,
            "tags": ["entity", "researcher"],
            "created": run_date,
            "updated": run_date,
            "type": "entity",
            "status": "stub",
            "summary": f"研究者，本库中收录 {len(papers)} 篇论文",
            "affiliation": "",
            "url": "",
        },
        schema,
    )
    papers_md = "\n".join(f"- [[{paper}]]" for paper in papers)
    return frontmatter + "\n## Papers\n\n" + papers_md + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-papers", type=int, default=MIN_PAPERS, help="Minimum paper count for coauthor entity stubs.")
    parser.add_argument(
        "--include-first-authors",
        action="store_true",
        help="Create entity stubs for every first author even when they appear only once.",
    )
    args = parse_args_with_write_options(parser)
    schema = load_schema()
    run_date = today_iso()
    author_counter, author_papers, first_authors = collect_authors()
    normalized = normalize_existing_entities(schema, dry_run=args.dry_run, backup=not args.no_backup)
    entities_by_title = existing_entities()

    created = 0
    skipped = 0
    for author, count in author_counter.most_common():
        if count < args.min_papers and not (args.include_first_authors and author in first_authors):
            continue
        path = target_path(author, entities_by_title)
        if path is None or path.exists():
            skipped += 1
            continue
        content = render_entity(author, author_papers[author], schema, run_date)
        if safe_write(path, content, dry_run=args.dry_run, backup=not args.no_backup):
            created += 1
            entities_by_title[author] = path
    print(f"Done. Created: {created}, Skipped: {skipped}, Normalized: {normalized}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
