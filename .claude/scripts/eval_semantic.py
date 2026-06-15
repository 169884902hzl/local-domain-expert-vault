"""Read-only evaluation for the local semantic retrieval layer."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np

import kb_embed
import kb_search
from arxiv_ranker import RankedPaper
from kb_common import extract_frontmatter, load_schema, parse_frontmatter_map, safe_print, vault_path


POSITIVE_DECISIONS = {"top1_candidate", "venue_auto_import", "focus_review_queue", "review_queue"}
NEGATIVE_PENALTY = "non_robotics_cv_context"
SEM_SCALE = 25.0


def _strip_quotes(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _slug(value: str) -> str:
    value = value.strip().replace(".md", "")
    value = re.sub(r"[^A-Za-z0-9_\-\u4e00-\u9fff]+", "-", value.lower()).strip("-")
    return value


def _section(body: str, name: str) -> str:
    match = re.search(rf"(?ms)^##\s+{re.escape(name)}\s*\n(.*?)(?=^##\s+|\Z)", body)
    return match.group(1).strip() if match else ""


def _links(text: str) -> list[str]:
    out = []
    for match in re.finditer(r"\[\[([^\]|#]+)", text):
        out.append(_slug(match.group(1)))
    return out


def _load_notes(meta: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in meta:
        path = vault_path(str(item.get("path", "")))
        text = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(text)
        fields = parse_frontmatter_map(parsed[0]) if parsed else {}
        body = parsed[1] if parsed else text
        rows.append({"path": path, "fields": fields, "body": body, "meta": item})
    return rows


def _note_group(item: dict[str, Any]) -> str:
    note_type = str(item.get("note_type", ""))
    path = str(item.get("path", ""))
    if note_type == "literature" or "/topics/" in path:
        return "literature"
    if note_type == "concept" or "/concepts/" in path:
        return "concept"
    if note_type == "entity" or "/entities/" in path:
        return "entity"
    return "other"


def _gold_sets(rows: list[dict[str, Any]], meta: list[dict[str, Any]]) -> list[set[int]]:
    by_slug: dict[str, int] = {}
    by_title: dict[str, int] = {}
    for index, item in enumerate(meta):
        by_slug[_slug(Path(str(item.get("path", ""))).stem)] = index
        title = str(item.get("title", "")).strip()
        if title:
            by_title[_slug(title)] = index
    gold: list[set[int]] = []
    for index, row in enumerate(rows):
        body = row["body"]
        link_text = "\n".join([_section(body, "本地引用关系"), _section(body, "相关概念")])
        targets: set[int] = set()
        for link in _links(link_text):
            target = by_slug.get(link)
            if target is None:
                target = by_title.get(link)
            if target is not None and target != index:
                targets.add(target)
        gold.append(targets)
    return gold


def _query_text(query_fields: dict[str, str], query_body: str) -> str:
    sections = [
        _section(query_body, "结构化提取"),
        _section(query_body, "Definition"),
        _section(query_body, "Key Ideas"),
        _section(query_body, "Method Families"),
        _section(query_body, "本地引用关系"),
    ]
    section_text = " ".join(item[:500] for item in sections if item)
    if not section_text:
        section_text = re.sub(r"\s+", " ", query_body)[:800]
    return " ".join(
        [
            _strip_quotes(query_fields.get("title", "")),
            _strip_quotes(query_fields.get("summary", "")),
            section_text,
        ]
    )


def _keyword_scores(query_fields: dict[str, str], query_body: str, rows: list[dict[str, Any]]) -> np.ndarray:
    schema = load_schema()
    tag_terms = kb_search.taxonomy_terms(schema)
    query_text = _query_text(query_fields, query_body)
    query_terms = kb_search.tokenize(query_text)
    query_tags = kb_search.infer_query_tags(query_text, tag_terms)
    scoring_terms = kb_search.expand_query_terms(query_terms, query_tags, tag_terms)
    scores = []
    for row in rows:
        score, _snippets = kb_search.score_note(row["fields"], row["body"], scoring_terms, query_tags)
        scores.append(score)
    return np.asarray(scores, dtype=np.float32)


def _rank(scores: np.ndarray, self_index: int) -> list[int]:
    ranked = np.argsort(-scores)
    return [int(item) for item in ranked if int(item) != self_index]


def _rrf_rankings(keyword_rankings: list[list[int]], semantic_rankings: list[list[int]], *, k: int) -> list[list[int]]:
    fused_rankings: list[list[int]] = []
    for keyword, semantic in zip(keyword_rankings, semantic_rankings):
        scores: dict[int, float] = {}
        for rank, item in enumerate(keyword, start=1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
        for rank, item in enumerate(semantic, start=1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
        fused_rankings.append(sorted(scores, key=lambda item: (-scores[item], item)))
    return fused_rankings


def _metrics(rankings: list[list[int]], gold: list[set[int]], ks: tuple[int, ...] = (5, 10, 20)) -> dict[str, float]:
    valid = [(ranking, gold_set) for ranking, gold_set in zip(rankings, gold) if gold_set]
    if not valid:
        return {f"Recall@{k}": 0.0 for k in ks} | {"MRR": 0.0, "nDCG@10": 0.0, "queries": 0.0}
    totals: dict[str, float] = {f"Recall@{k}": 0.0 for k in ks}
    totals.update({"MRR": 0.0, "nDCG@10": 0.0, "queries": float(len(valid))})
    for ranking, gold_set in valid:
        for k in ks:
            totals[f"Recall@{k}"] += len(set(ranking[:k]) & gold_set) / len(gold_set)
        first = next((rank for rank, item in enumerate(ranking, start=1) if item in gold_set), None)
        totals["MRR"] += 1.0 / first if first else 0.0
        dcg = 0.0
        for rank, item in enumerate(ranking[:10], start=1):
            if item in gold_set:
                dcg += 1.0 / math.log2(rank + 1)
        ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(len(gold_set), 10) + 1))
        totals["nDCG@10"] += dcg / ideal if ideal else 0.0
    denom = len(valid)
    for key in list(totals):
        if key != "queries":
            totals[key] /= denom
    return totals


def _ap(labels: list[bool], scores: list[float]) -> float:
    order = sorted(range(len(scores)), key=lambda idx: -scores[idx])
    hits = 0
    total = sum(1 for label in labels if label)
    if total == 0:
        return 0.0
    acc = 0.0
    for rank, idx in enumerate(order, start=1):
        if labels[idx]:
            hits += 1
            acc += hits / rank
    return acc / total


def _u_auc(pos: list[float], neg: list[float]) -> float:
    if not pos or not neg:
        return 0.0
    wins = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / (len(pos) * len(neg))


def _candidate_eval(matrix: np.ndarray, limit: int) -> dict[str, Any]:
    paths = sorted(vault_path("projects", "arxiv-daily").glob("*-candidates.jsonl"))[-limit:]
    rows: list[RankedPaper] = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(RankedPaper.from_dict(json.loads(line)))
    if not rows:
        return {"status": "no_candidates"}
    labels = [
        item.decision in POSITIVE_DECISIONS or item.quality_score >= 70
        for item in rows
        if NEGATIVE_PENALTY in item.penalties or item.decision in POSITIVE_DECISIONS or item.quality_score >= 70
    ]
    filtered = [
        item
        for item in rows
        if NEGATIVE_PENALTY in item.penalties or item.decision in POSITIVE_DECISIONS or item.quality_score >= 70
    ]
    if not filtered:
        return {"status": "no_labeled_candidates", "rows": len(rows)}
    try:
        qvecs = kb_embed.embed_texts([f"{item.paper.title}\n\n{item.paper.summary}" for item in filtered], is_query=True)
    except kb_embed.EmbeddingUnavailable as exc:
        return {"status": "embedding_unavailable", "error": str(exc), "rows": len(rows)}
    sims = []
    for qvec in qvecs:
        hits = kb_embed.query_vector_similar(qvec, matrix, top_k=10)
        sims.append(float(sum(score for _row, score in hits) / len(hits)) if hits else 0.0)
    original_scores = [float(item.quality_score) for item in filtered]
    boosted_scores = [
        min(100.0, float(item.quality_score) + min(15.0, round(sim * 25)))
        for item, sim in zip(filtered, sims)
    ]
    pos = [score for label, score in zip(labels, sims) if label]
    neg = [score for label, score in zip(labels, sims) if not label]
    pushed_negatives = sum(
        1
        for label, item, boosted in zip(labels, filtered, boosted_scores)
        if not label and item.quality_score < 70 <= boosted
    )
    return {
        "status": "ok",
        "rows": len(filtered),
        "positive": sum(1 for label in labels if label),
        "negative": sum(1 for label in labels if not label),
        "positive_mean_similarity": float(np.mean(pos)) if pos else 0.0,
        "negative_mean_similarity": float(np.mean(neg)) if neg else 0.0,
        "mann_whitney_auc": _u_auc(pos, neg),
        "ap_original": _ap(labels, original_scores),
        "ap_boosted": _ap(labels, boosted_scores),
        "negative_pushed_over_70": pushed_negatives,
    }


def evaluate(args: argparse.Namespace) -> dict[str, Any]:
    loaded = kb_embed.load_index()
    if loaded is None:
        return {"status": "embedding_index_unavailable"}
    matrix, meta, manifest = loaded
    rows = _load_notes(meta)
    gold = _gold_sets(rows, meta)
    groups = [_note_group(item) for item in meta]
    sem_scores = matrix @ matrix.T
    keyword_rankings: list[list[int]] = []
    semantic_rankings: list[list[int]] = []
    keyword_cache: list[Any] = []
    for index, row in enumerate(rows):
        semantic = sem_scores[index].copy()
        semantic[index] = -1e9
        semantic_rankings.append(_rank(semantic, index))
        if not args.semantic_only and groups[index] == "literature":
            keyword = _keyword_scores(row["fields"], row["body"], rows)
            keyword[index] = -1e9
            keyword_cache.append(keyword)
            keyword_rankings.append(_rank(keyword, index))
        else:
            keyword_cache.append(None)
            keyword_rankings.append([])

    def group_metrics(rankings: list[list[int]], group: str | None = None) -> dict[str, float]:
        sub = [
            (r, g)
            for r, g, note_group in zip(rankings, gold, groups)
            if group is None or note_group == group
        ]
        return _metrics([r for r, _g in sub], [g for _r, g in sub])

    by_note_type = {}
    for group in ["literature", "concept", "entity", "other", "all"]:
        metrics = {
            "semantic": group_metrics(semantic_rankings, None if group == "all" else group),
            "gold_queries": sum(1 for note_group, item in zip(groups, gold) if item and (group == "all" or note_group == group)),
        }
        if group == "literature" and not args.semantic_only:
            metrics["keyword"] = group_metrics(keyword_rankings, "literature")
        by_note_type[group] = metrics
    baseline = by_note_type["literature"].get("keyword", {})
    semantic = by_note_type["literature"]["semantic"]
    # kb_search --semantic now ranks by semantic score (keyword is only a
    # tie-break), so the `semantic` row above is exactly the live behaviour.
    # weighted/RRF are swept only to confirm they underperform semantic-dominant.
    sweep = []
    if not args.semantic_only:
        for alpha in args.alpha:
            for floor in args.floor:
                fused_rankings = []
                for index, keyword in enumerate(keyword_cache):
                    if keyword is None:
                        fused_rankings.append([])
                        continue
                    semantic_scores = sem_scores[index].copy()
                    semantic_scores[semantic_scores < floor] = 0.0
                    fused = keyword + alpha * np.maximum(0.0, semantic_scores) * SEM_SCALE
                    fused[index] = -1e9
                    fused_rankings.append(_rank(fused, index))
                sweep.append({"fusion": "weighted", "alpha": alpha, "floor": floor, **group_metrics(fused_rankings, "literature")})
        for k in args.rrf_k:
            sweep.append({"fusion": "rrf", "rrf_k": k, **group_metrics(_rrf_rankings(keyword_rankings, semantic_rankings, k=k), "literature")})
    best = max(sweep, key=lambda item: (item["nDCG@10"], item["Recall@10"], item["MRR"])) if sweep else {}
    return {
        "status": "ok",
        "rows": len(meta),
        "topic_gold_queries": by_note_type["literature"]["gold_queries"],
        "gold_queries_by_note_type": {group: metrics["gold_queries"] for group, metrics in by_note_type.items()},
        "manifest": manifest,
        "keyword": baseline,
        "semantic": semantic,
        "by_note_type": by_note_type,
        "best_fused": best,
        "sweep": sweep,
        "candidate_eval": _candidate_eval(matrix, args.candidate_days),
    }


def _print_table(payload: dict[str, Any]) -> None:
    if payload.get("status") != "ok":
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return
    safe_print(f"SEMANTIC_EVAL rows={payload['rows']} topic_gold_queries={payload['topic_gold_queries']}")
    for label in ["keyword", "semantic", "best_fused"]:
        item = payload[label]
        safe_print(
            f"{label}: Recall@10={item.get('Recall@10', 0):.3f} "
            f"nDCG@10={item.get('nDCG@10', 0):.3f} MRR={item.get('MRR', 0):.3f} "
            f"fusion={item.get('fusion', '-')} alpha={item.get('alpha', '-')} "
            f"floor={item.get('floor', '-')} rrf_k={item.get('rrf_k', '-')}"
        )
    for group, metrics in payload.get("by_note_type", {}).items():
        semantic = metrics["semantic"]
        safe_print(
            f"{group}: gold_queries={metrics['gold_queries']} "
            f"semantic_Recall@10={semantic.get('Recall@10', 0):.3f} "
            f"semantic_nDCG@10={semantic.get('nDCG@10', 0):.3f}"
        )
    safe_print("candidate_eval: " + json.dumps(payload["candidate_eval"], ensure_ascii=False, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--alpha", type=float, nargs="*", default=[0.25, 0.5, 0.75, 1.0])
    parser.add_argument("--floor", type=float, nargs="*", default=[0.35, 0.45, 0.55, 0.65])
    parser.add_argument("--rrf-k", type=int, nargs="*", default=[30, 60, 90])
    parser.add_argument("--candidate-days", type=int, default=10)
    parser.add_argument("--semantic-only", action="store_true", help="Skip keyword/fusion sweeps and report semantic metrics by note type.")
    args = parser.parse_args()
    payload = evaluate(args)
    if args.json:
        safe_print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        _print_table(payload)
    return 0 if payload.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
