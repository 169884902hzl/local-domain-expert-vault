"""Search the local Obsidian literature knowledge base.

This is the deterministic local-first retrieval layer for Claudian. It never
uses the web and returns note paths that can be opened before answering.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, load_schema, parse_frontmatter_map, parse_list_value, safe_print, vault_path


SEARCH_DIRS = [vault_path("wiki", "topics"), vault_path("wiki", "concepts"), vault_path("wiki", "entities")]
# Semantic-dominant fusion: the semantic score leads the ranking and the
# keyword score is only a secondary tie-break key. A strong-but-narrow keyword
# signal therefore can never drag down a strong semantic match -- the failure
# mode of both weighted and RRF symmetric fusion on this evidence-link task.

# Concept-anchored expansion: after semantic ranking, follow the wikilinks of
# any concept page that surfaced in the results to pull in same-topic papers a
# single-angle query missed. The links are human/reading-curated, so this adds
# precise cross-angle evidence without the keyword noise of a second retriever.
CONCEPT_EXPAND_FLOOR = 0.40
CONCEPT_EXPAND_LIMIT = 8


def _safe_stderr(message: object) -> None:
    text = str(message)
    encoding = sys.stderr.encoding or "utf-8"
    print(text.encode(encoding, errors="backslashreplace").decode(encoding), file=sys.stderr, flush=True)


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
    semantic_score: float = 0.0
    fused_score: float = 0.0
    via_concept: str = ""


def normalize(text: str) -> str:
    return text.lower()


def _slug(value: str) -> str:
    value = value.strip().replace(".md", "")
    return re.sub(r"[^A-Za-z0-9_\-一-鿿]+", "-", value.lower()).strip("-")


def _wikilinks(text: str) -> list[str]:
    return [_slug(match.group(1)) for match in re.finditer(r"\[\[([^\]|#]+)", text)]


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
    use_semantic = bool(getattr(args, "semantic", False))
    semantic_scores: dict[str, float] = {}
    index_meta: list[dict[str, Any]] = []

    if use_semantic:
        try:
            import kb_embed

            loaded = kb_embed.load_index()
            if loaded is None:
                _safe_stderr("KB_SEARCH_SEMANTIC_DISABLED: embedding index unavailable")
                use_semantic = False
            else:
                matrix, index_meta, _manifest = loaded
                qvec = kb_embed.embed_texts([args.query], is_query=True)[0]
                scores = matrix @ qvec
                semantic_scores = {
                    str(item.get("path", "")): float(scores[index])
                    for index, item in enumerate(index_meta)
                    if index < scores.shape[0]
                }
        except kb_embed.EmbeddingUnavailable as exc:
            _safe_stderr(f"KB_SEARCH_SEMANTIC_DISABLED: {exc}")
            use_semantic = False

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
        rel_path = str(path.relative_to(vault_path())).replace("\\", "/")
        raw_sem = semantic_scores.get(rel_path, 0.0) if use_semantic else 0.0
        if score <= 0 and not must_tags:
            if not (use_semantic and raw_sem >= float(getattr(args, "semantic_floor", 0.55))):
                continue
        if use_semantic:
            fused = max(0.0, raw_sem)
        else:
            fused = score
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
                semantic_score=raw_sem,
                fused_score=fused,
            )
        )
    if not use_semantic:
        return sorted(results, key=lambda item: (-item.score, item.year, item.title))[: args.limit]
    ranked = sorted(results, key=lambda item: (-item.fused_score, -item.score, item.year, item.title))[: args.limit]
    if getattr(args, "expand_concepts", True):
        ranked = _expand_via_concepts(ranked, index_meta, semantic_scores)
    return ranked


def _expand_via_concepts(
    ranked: list[SearchResult],
    index_meta: list[dict[str, Any]],
    semantic_scores: dict[str, float],
) -> list[SearchResult]:
    """Append same-topic papers reached via the wikilinks of concept pages that
    already surfaced in the semantic results. Links are curated, so no noise."""
    main_paths = {str(item.path.relative_to(vault_path())).replace("\\", "/") for item in ranked}
    slug_to_path: dict[str, str] = {}
    for entry in index_meta:
        path = str(entry.get("path", ""))
        if not path:
            continue
        slug_to_path.setdefault(_slug(Path(path).stem), path)
        title = str(entry.get("title", ""))
        if title:
            slug_to_path.setdefault(_slug(title), path)

    via: dict[str, str] = {}
    for item in ranked:
        if item.note_type != "concept":
            continue
        try:
            _fields, body = frontmatter(item.path)
        except OSError:
            continue
        for slug in _wikilinks(body):
            target = slug_to_path.get(slug)
            if not target or target in main_paths or "/topics/" not in target:
                continue
            if semantic_scores.get(target, 0.0) < CONCEPT_EXPAND_FLOOR:
                continue
            via.setdefault(target, item.title)
    if not via:
        return ranked

    order = sorted(via, key=lambda p: -semantic_scores.get(p, 0.0))[:CONCEPT_EXPAND_LIMIT]
    for target in order:
        path = vault_path(target)
        try:
            fields, _body = frontmatter(path)
        except OSError:
            continue
        sem = semantic_scores.get(target, 0.0)
        ranked.append(
            SearchResult(
                path=path,
                title=fields.get("title", "").strip('"'),
                note_type=fields.get("type", "").strip('"'),
                status=fields.get("status", "").strip('"'),
                year=fields.get("year", "").strip('"'),
                tags=note_tags(fields),
                summary=fields.get("summary", "").strip('"'),
                score=0.0,
                snippets=[],
                semantic_score=sem,
                fused_score=sem,
                via_concept=via[target],
            )
        )
    return ranked


def as_json(results: list[SearchResult], *, include_semantic: bool = False) -> str:
    payload = []
    for item in results:
        row = {
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
        if include_semantic:
            row["semantic_score"] = item.semantic_score
            row["fused_score"] = item.fused_score
        if item.via_concept:
            row["via_concept"] = item.via_concept
        payload.append(row)
    return json.dumps(payload, ensure_ascii=False, indent=2)


def as_markdown(results: list[SearchResult], *, include_semantic: bool = False) -> str:
    if not results:
        return "NO_LOCAL_MATCHES"
    lines = []
    for index, item in enumerate(results, 1):
        rel = str(item.path.relative_to(vault_path())).replace("\\", "/")
        suffix = f", sem={item.semantic_score:.3f}, fused={item.fused_score:.3f}" if include_semantic else ""
        via = f"  [via concept: {item.via_concept}]" if item.via_concept else ""
        lines.append(f"{index}. {item.title} ({item.year}, {item.status}, score={item.score:g}{suffix}){via}")
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
    parser.add_argument("--semantic", action="store_true", help="Opt in to local embedding semantic recall.")
    parser.add_argument("--semantic-floor", type=float, default=0.55)
    parser.add_argument(
        "--expand-concepts",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="With --semantic, also pull same-topic papers via surfaced concept pages' wikilinks (default on).",
    )
    args = parser.parse_args()

    results = search(args)
    safe_print(as_json(results, include_semantic=args.semantic) if args.json else as_markdown(results, include_semantic=args.semantic))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
