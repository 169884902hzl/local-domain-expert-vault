"""Extract conservative local paper-to-paper links from literature notes."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from kb_common import (
    extract_frontmatter,
    parse_args_with_write_options,
    parse_frontmatter_map,
    safe_write,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
CITATION_HEADING = "## 本地引用关系"


@dataclass(frozen=True)
class Paper:
    stem: str
    title: str
    year: str
    first_author_last: str


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_note(path: Path) -> tuple[dict[str, str], str]:
    parsed = extract_frontmatter(read(path))
    if not parsed:
        return {}, read(path)
    fm_text, body = parsed
    return parse_frontmatter_map(fm_text), body


def first_author_last(authors: str) -> str:
    first = authors.strip().strip('"').split(";", 1)[0].strip()
    if "," in first:
        return first.split(",", 1)[0].strip()
    return first.split(" ", 1)[0].strip()


def collect_papers() -> dict[Path, Paper]:
    papers = {}
    for path in sorted(TOPICS_DIR.glob("*.md")):
        fields, _ = parse_note(path)
        papers[path] = Paper(
            stem=path.stem,
            title=fields.get("title", "").strip('"'),
            year=fields.get("year", "").strip('"'),
            first_author_last=first_author_last(fields.get("authors", "")),
        )
    return papers


def strip_sections(body: str) -> str:
    return re.sub(r"\n## (相关概念|相关研究者|本地引用关系)\n\n.*?(?=\n## |\Z)", "", body, flags=re.DOTALL)


def existing_local_links(body: str, papers: dict[Path, Paper]) -> list[str]:
    match = re.search(rf"(?:^|\n){re.escape(CITATION_HEADING)}\n\n(.*?)(?=\n## |\Z)", body, flags=re.DOTALL)
    if not match:
        return []
    known_stems = {paper.stem for paper in papers.values()}
    links = []
    for target in re.findall(r"\[\[([^|\]#]+)", match.group(1)):
        if target in known_stems:
            links.append(target)
    return sorted(set(links))


def local_citations(path: Path, paper: Paper, papers: dict[Path, Paper]) -> list[str]:
    _, body = parse_note(path)
    haystack = strip_sections(body).lower()
    links = existing_local_links(body, papers)
    for other_path, other in papers.items():
        if other_path == path:
            continue
        title_hit = len(other.title) >= 25 and other.title.lower() in haystack
        link_hit = f"[[{other.stem}]]" in body
        author_year_hit = False
        if other.first_author_last and other.year and other.year.isdigit():
            author_year_hit = bool(
                re.search(
                    rf"\b{re.escape(other.first_author_last)}\b[^.\n]{{0,80}}\b{re.escape(other.year)}\b",
                    body,
                    flags=re.IGNORECASE,
                )
            )
        if title_hit or link_hit or author_year_hit:
            links.append(other.stem)
    return sorted(set(links))


def replace_citation_section(content: str, links: list[str]) -> str:
    parsed = extract_frontmatter(content)
    if not parsed:
        return content
    fm_text, body = parsed
    section_body = "\n".join(f"- [[{stem}]]" for stem in links) if links else "-"
    new_section = f"{CITATION_HEADING}\n\n{section_body}"
    pattern = re.compile(rf"(?:^|\n){re.escape(CITATION_HEADING)}\n\n.*?(?=\n## |\Z)", re.DOTALL)
    if pattern.search(body):
        body = pattern.sub("\n" + new_section, body).lstrip("\n")
    else:
        match = re.search(r"\n## 相关概念\n", body)
        if match:
            body = body[: match.start()] + "\n\n" + new_section + "\n" + body[match.start() :]
        else:
            body = body.rstrip() + "\n\n" + new_section + "\n"
    return "---\n" + fm_text + "\n---\n" + body.lstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args_with_write_options(parser)
    papers = collect_papers()
    changed = 0
    linked_notes = 0
    for path, paper in papers.items():
        links = local_citations(path, paper, papers)
        if links:
            linked_notes += 1
        content = read(path)
        new_content = replace_citation_section(content, links)
        if new_content != content:
            if safe_write(path, new_content, dry_run=args.dry_run, backup=not args.no_backup):
                changed += 1
    print(f"Done. Citation sections updated: {changed}, notes with local citations: {linked_notes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
