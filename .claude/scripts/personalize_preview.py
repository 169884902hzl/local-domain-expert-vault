"""Preview how read-library personalization re-ranks a day's arXiv candidates.

Shows which candidate papers are most similar to the papers you have actually
finished reading, and how the personalization boost would move them up the
ranking. Read-only -- it never writes or re-imports anything.

Usage:
    python personalize_preview.py [YYYY-MM-DD]

With no date it uses the most recent projects/arxiv-daily/*-candidates.jsonl.
Requires the L20 embedding endpoint (KB_EMBED_API_BASE); degrades gracefully if
it is unreachable.
"""
from __future__ import annotations

import json
import sys

import arxiv_ranker as ranker
from kb_common import safe_print, vault_path


def main() -> int:
    daily_dir = vault_path("projects", "arxiv-daily")
    if len(sys.argv) > 1:
        target = daily_dir / f"{sys.argv[1]}-candidates.jsonl"
    else:
        files = sorted(daily_dir.glob("*-candidates.jsonl"))
        target = files[-1] if files else None
    if not target or not target.exists():
        safe_print("No candidates file found under projects/arxiv-daily/.")
        return 1

    ranked = [
        ranker.RankedPaper.from_dict(json.loads(line))
        for line in target.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not ranked:
        safe_print(f"No candidates in {target.name}.")
        return 1

    papers = [item.paper for item in ranked]
    ranker.ENABLE_READ_LIB_SIMILARITY = True
    sims = ranker._batch_read_lib_similarity(papers)
    if not sims:
        safe_print(
            "read_lib similarity unavailable (L20 unreachable or anchor missing). "
            "Preview skipped -- the daily scout would simply fall back to keyword ranking."
        )
        return 1

    rows = []
    for item in ranked:
        sim = sims.get(id(item.paper), 0.0)
        boost = min(15, round(sim * 25))
        rows.append(
            {
                "title": item.paper.title,
                "q": item.quality_score,
                "sim": sim,
                "boost": boost,
                "new_q": min(100, item.quality_score + boost),
            }
        )

    safe_print(f"=== Personalization preview: {target.name} ({len(rows)} candidates) ===\n")
    safe_print("Most like your read library (top read_lib similarity):")
    for row in sorted(rows, key=lambda item: -item["sim"])[:10]:
        safe_print(
            f"  sim={row['sim']:.3f}  boost=+{row['boost']:<2}  q {row['q']}->{row['new_q']}   {row['title'][:66]}"
        )

    original = [row["title"] for row in sorted(rows, key=lambda item: -item["q"])]
    personalized = [row["title"] for row in sorted(rows, key=lambda item: -item["new_q"])]
    moved_up = [
        (title, original.index(title), personalized.index(title))
        for title in personalized
        if personalized.index(title) < original.index(title)
    ]
    if moved_up:
        safe_print("\nPushed UP the most by personalization (rank was -> now):")
        for title, old_rank, new_rank in sorted(moved_up, key=lambda item: item[2] - item[1])[:8]:
            safe_print(f"  #{old_rank + 1:>3} -> #{new_rank + 1:<3} (+{old_rank - new_rank})  {title[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
