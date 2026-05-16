"""Add [[wikilinks]] to topic notes by linking concepts and researchers."""
from __future__ import annotations

import argparse
import re

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_args_with_write_options,
    parse_frontmatter_map,
    parse_list_value,
    safe_write,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
ENTITIES_DIR = vault_path("wiki", "entities")
KEYWORD_INFER_CONCEPTS = {
    "bimanual-manipulation",
    "deformable-linear-object",
    "diffusion-model",
    "grasping",
    "planning",
    "sim-to-real",
    "tactile-sensing",
    "vision-language-model",
}


def tag_to_concept(schema: dict) -> dict[str, str]:
    mapping = {}
    for tag, info in schema["literature"]["tag_taxonomy"].items():
        if info.get("concept"):
            mapping[tag] = info["concept"]
    return mapping


def concept_keywords(schema: dict) -> dict[str, list[str]]:
    mapping = {}
    for info in schema["literature"]["tag_taxonomy"].values():
        concept = info.get("concept")
        if concept and concept in KEYWORD_INFER_CONCEPTS:
            mapping[concept] = info.get("keywords", []) + info.get("aliases", [])
    return mapping


def author_lookup() -> dict[str, str]:
    authors = {}
    for path in sorted(ENTITIES_DIR.glob("*.md")):
        parsed = extract_frontmatter(path.read_text(encoding="utf-8"))
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        title = fields.get("title", "").strip('"')
        if title:
            authors[title] = path.stem
    return authors


def infer_concepts(fields: dict[str, str], body: str, schema: dict, tag_mapping: dict[str, str]) -> list[str]:
    tags = parse_list_value(fields.get("tags", ""))
    concepts = []
    for tag in tags:
        concept = tag_mapping.get(tag)
        if concept:
            concepts.append(concept)

    clean_body = re.sub(r"\n*## (相关概念|相关研究者|本地引用关系)\n.*?(?=\n## |\Z)", "", body, flags=re.DOTALL)
    haystack = "\n".join(
        [
            fields.get("title", ""),
            fields.get("summary", ""),
            fields.get("abstract", ""),
            clean_body,
        ]
    ).lower()
    for concept, keywords in concept_keywords(schema).items():
        if concept in concepts:
            continue
        for keyword in keywords:
            if keyword and keyword.lower() in haystack:
                concepts.append(concept)
                break
    return list(dict.fromkeys(concepts))


def build_related_sections(
    fields: dict[str, str],
    body: str,
    schema: dict,
    tag_mapping: dict[str, str],
    authors: dict[str, str],
) -> list[str]:
    concept_links = [f"- [[{concept}]]" for concept in infer_concepts(fields, body, schema, tag_mapping)]
    concept_links = list(dict.fromkeys(concept_links))

    entity_links = []
    authors_str = fields.get("authors", "").strip('"')
    if authors_str:
        for author in authors_str.split(";"):
            author = author.strip()
            entity = authors.get(author)
            if entity:
                entity_links.append(f"- [[{entity}|{author}]]")
    entity_links = list(dict.fromkeys(entity_links))

    sections = []
    if concept_links:
        sections.append("## 相关概念\n\n" + "\n".join(concept_links))
    if entity_links:
        sections.append("## 相关研究者\n\n" + "\n".join(entity_links))
    return sections


def rebuild_content(content: str, schema: dict, tag_mapping: dict[str, str], authors: dict[str, str]) -> str:
    parsed = extract_frontmatter(content)
    if not parsed:
        return content
    fm_text, body = parsed
    fields = parse_frontmatter_map(fm_text)
    sections = build_related_sections(fields, body, schema, tag_mapping, authors)
    if not sections:
        return content

    body = re.sub(r"\n*## 相关概念\n.*?(?=\n## |\Z)", "", body, flags=re.DOTALL)
    body = re.sub(r"\n*## 相关研究者\n.*?(?=\n## |\Z)", "", body, flags=re.DOTALL)
    new_body = body.rstrip() + "\n\n" + "\n\n".join(sections) + "\n"
    return "---\n" + fm_text + "\n---\n" + new_body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args_with_write_options(parser)

    schema = load_schema()
    tag_mapping = tag_to_concept(schema)
    authors = author_lookup()
    updated = 0
    for path in sorted(TOPICS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        new_content = rebuild_content(content, schema, tag_mapping, authors)
        if new_content != content:
            if safe_write(path, new_content, dry_run=args.dry_run, backup=not args.no_backup):
                updated += 1
    print(f"Done. Updated: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
