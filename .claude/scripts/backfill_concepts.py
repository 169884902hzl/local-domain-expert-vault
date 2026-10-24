"""Backfill concept pages with reverse links to related papers."""
from __future__ import annotations

import argparse
import re

from collections import Counter, defaultdict

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
CONCEPTS_DIR = vault_path("wiki", "concepts")


def tag_to_concept(schema: dict) -> dict[str, str]:
    mapping = {}
    for tag, info in schema["literature"]["tag_taxonomy"].items():
        if info.get("concept"):
            mapping[tag] = info["concept"]
    return mapping


def collect_concept_papers(tag_mapping: dict[str, str]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    concept_papers: dict[str, list[str]] = {concept: [] for concept in tag_mapping.values()}
    related: dict[str, Counter[str]] = defaultdict(Counter)
    for path in sorted(TOPICS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(content)
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        body = parsed[1]
        concepts = []
        for tag in parse_list_value(fields.get("tags", "")):
            concept = tag_mapping.get(tag)
            if concept:
                concepts.append(concept)
        for concept in re.findall(r"\[\[([^|\]#]+)", related_concepts_section(body)):
            if (CONCEPTS_DIR / f"{concept}.md").exists():
                concepts.append(concept)
        concepts = list(dict.fromkeys(concepts))
        for concept in concepts:
            concept_papers[concept].append(path.stem)
        for concept in concepts:
            for other in concepts:
                if other != concept:
                    related[concept][other] += 1
    return concept_papers, {
        concept: [name for name, _ in counter.most_common()]
        for concept, counter in related.items()
    }


def related_concepts_section(body: str) -> str:
    match = re.search(r"^## 相关概念\n\n(.*?)(?=\n## |\Z)", body, flags=re.DOTALL | re.MULTILINE)
    return match.group(1) if match else ""


def replace_related_papers(content: str, papers: list[str]) -> str:
    paper_links = "\n".join(f"- [[{paper}]]" for paper in sorted(set(papers)))
    new_section = f"## Related Papers\n\n{paper_links}"
    if "## Related Papers" not in content:
        return content.rstrip() + "\n\n" + new_section + "\n"
    return re.sub(
        r"## Related Papers\n\n.*?(?=\n## |\Z)",
        new_section,
        content,
        flags=re.DOTALL,
    )


def replace_related_concepts(content: str, concepts: list[str]) -> str:
    concept_links = "\n".join(f"- [[{concept}]]" for concept in concepts) if concepts else "-"
    new_section = f"## Related Concepts\n\n{concept_links}"
    if "## Related Concepts" not in content:
        return content.rstrip() + "\n\n" + new_section + "\n"
    return re.sub(
        r"## Related Concepts\n\n.*?(?=\n## |\Z)",
        new_section,
        content,
        flags=re.DOTALL,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args_with_write_options(parser)

    concept_papers, related_concepts = collect_concept_papers(tag_to_concept(load_schema()))
    updated = 0
    for concept_file, papers in sorted(concept_papers.items()):
        if not papers:
            continue
        path = CONCEPTS_DIR / f"{concept_file}.md"
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        new_content = replace_related_papers(content, papers)
        new_content = replace_related_concepts(new_content, related_concepts.get(concept_file, []))
        if safe_write(path, new_content, dry_run=args.dry_run, backup=not args.no_backup):
            updated += 1
        print(f"{concept_file}: {len(set(papers))} papers linked")
    print(f"Done. Updated: {updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
