"""Search the local Obsidian literature knowledge base.

This is the deterministic local-first retrieval layer for Claudian. It never
uses the web and returns note paths that can be opened before answering.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, load_schema, parse_frontmatter_map, parse_list_value, safe_print, vault_path


SEARCH_DIRS = [vault_path("wiki", "topics"), vault_path("wiki", "concepts"), vault_path("wiki", "entities")]


@dataclass
class SearchResult:
    path: Path
    title: str
    note_type: str
    status: str
    year: str
    tags: list[str]
    summary: str
    score: float
    snippets: list[str]


def normalize(text: str) -> str:
    return text.lower()


def tokenize(query: str) -> list[str]:
    terms = re.findall(r"[A-Za-z0-9_\-]+|[\u4e00-\u9fff]{2,}", query.lower())
    return list(dict.fromkeys(terms))


def taxonomy_terms(schema: dict[str, Any]) -> dict[str, list[str]]:
    taxonomy = schema["literature"].get("tag_taxonomy", {})
    terms: dict[str, list[str]] = {}
    for tag, info in taxonomy.items():
        values = [tag, info.get("cn", ""), info.get("title", "")]
        values.extend(info.get("keywords", []) or [])
        values.extend(info.get("aliases", []) or [])
        terms[tag] = [normalize(str(value)) for value in values if value]
    return terms


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text
    fm_text, body = parsed
    return parse_frontmatter_map(fm_text), body


def note_tags(fields: dict[str, str]) -> list[str]:
    return parse_list_value(fields.get("tags", ""))


def infer_query_tags(query: str, tag_terms: dict[str, list[str]]) -> list[str]:
    q = normalize(query)
    inferred = []
    for tag, terms in tag_terms.items():
        if any(term and term in q for term in terms):
            inferred.append(tag)
    return inferred


def expand_query_terms(query_terms: list[str], query_tags: list[str], tag_terms: dict[str, list[str]]) -> list[str]:
    expanded = list(query_terms)
    for tag in query_tags:
        expanded.append(tag)
        expanded.extend(tag_terms.get(tag, []))
    return list(dict.fromkeys(term for term in expanded if term))


def line_snippets(body: str, terms: list[str], limit: int = 2) -> list[str]:
    snippets = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if len(line) < 8:
            continue
        lower = normalize(line)
        if any(term in lower for term in terms):
            snippets.append(line[:220])
        if len(snippets) >= limit:
            break
    return snippets


def score_note(fields: dict[str, str], body: str, query_terms: list[str], query_tags: list[str]) -> tuple[float, list[str]]:
    title = fields.get("title", "")
    summary = fields.get("summary", "")
    tags = note_tags(fields)
    haystacks = {
        "title": normalize(title),
        "summary": normalize(summary),
        "tags": normalize(" ".join(tags)),
        "body": normalize(body),
    }
    score = 0.0
    for term in query_terms:
        if term in haystacks["title"]:
            score += 8
        if term in haystacks["summary"]:
            score += 5
        if term in haystacks["tags"]:
            score += 5
        if term in haystacks["body"]:
            score += 1
    for tag in query_tags:
        if tag in tags:
            score += 10
    snippets = line_snippets(body, query_terms + query_tags)
    return score, snippets


def iter_notes(note_type: str | None = None) -> list[Path]:
    paths = []
    for directory in SEARCH_DIRS:
        if directory.exists():
            paths.extend(sorted(directory.glob("*.md")))
    if note_type:
        filtered = []
        for path in paths:
            fields, _ = frontmatter(path)
            if fields.get("type", "").strip('"') == note_type:
                filtered.append(path)
        return filtered
    return paths


def search(args: argparse.Namespace) -> list[SearchResult]:
    schema = load_schema()
    tag_terms = taxonomy_terms(schema)
    query_terms = tokenize(args.query)
    query_tags = list(dict.fromkeys(args.tag + infer_query_tags(args.query, tag_terms)))
    scoring_terms = expand_query_terms(query_terms, query_tags, tag_terms)
    must_tags = set(args.must_tag)
    results: list[SearchResult] = []

    for path in iter_notes(args.type):
        fields, body = frontmatter(path)
        tags = note_tags(fields)
        if args.status and fields.get("status", "").strip('"') != args.status:
            continue
        year = fields.get("year", "").strip('"')
        if args.year_from and year and year < args.year_from:
            continue
        if args.year_to and year and year > args.year_to:
            continue
        if must_tags and not must_tags.issubset(set(tags)):
            continue
        score, snippets = score_note(fields, body, scoring_terms, query_tags)
        if score <= 0 and not must_tags:
            continue
        results.append(
            SearchResult(
                path=path,
                title=fields.get("title", "").strip('"'),
                note_type=fields.get("type", "").strip('"'),
                status=fields.get("status", "").strip('"'),
                year=year,
                tags=tags,
                summary=fields.get("summary", "").strip('"'),
                score=score,
                snippets=snippets,
            )
        )
    return sorted(results, key=lambda item: (-item.score, item.year, item.title))[: args.limit]


def as_json(results: list[SearchResult]) -> str:
    payload = []
    for item in results:
        payload.append(
            {
                "path": str(item.path.relative_to(vault_path())).replace("\\", "/"),
                "title": item.title,
                "type": item.note_type,
                "status": item.status,
                "year": item.year,
                "tags": item.tags,
                "summary": item.summary,
                "score": item.score,
                "snippets": item.snippets,
            }
        )
    return json.dumps(payload, ensure_ascii=False, indent=2)


def as_markdown(results: list[SearchResult]) -> str:
    if not results:
        return "NO_LOCAL_MATCHES"
    lines = []
    for index, item in enumerate(results, 1):
        rel = str(item.path.relative_to(vault_path())).replace("\\", "/")
        lines.append(f"{index}. {item.title} ({item.year}, {item.status}, score={item.score:g})")
        lines.append(f"   - path: {rel}")
        lines.append(f"   - tags: {', '.join(item.tags)}")
        if item.summary:
            lines.append(f"   - summary: {item.summary}")
        for snippet in item.snippets:
            lines.append(f"   - evidence: {snippet}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Natural-language query. Searches local wiki only.")
    parser.add_argument("--tag", action="append", default=[], help="Boost a tag, can be repeated.")
    parser.add_argument("--must-tag", action="append", default=[], help="Require a tag, can be repeated.")
    parser.add_argument("--type", choices=["literature", "concept", "entity"], help="Restrict note type.")
    parser.add_argument("--status", help="Restrict status, for example stub or done.")
    parser.add_argument("--year-from", help="Minimum year string, for example 2024.")
    parser.add_argument("--year-to", help="Maximum year string, for example 2025.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    args = parser.parse_args()

    results = search(args)
    safe_print(as_json(results) if args.json else as_markdown(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
