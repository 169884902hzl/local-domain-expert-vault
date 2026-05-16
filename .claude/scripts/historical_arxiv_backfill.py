"""Historical arXiv backfill for high-priority papers missing from Zotero."""
from __future__ import annotations

import argparse
from dataclasses import replace
import sys
from typing import Any

from arxiv_ranker import DEFAULT_QUERIES, FOCUS_REVIEW_DECISION, RankedPaper, rank_papers
from arxiv_metadata_sync import query_mirror
from daily_arxiv_pipeline import (
    collect_candidates,
    exclude_existing_candidates,
    ingest_zotero_key,
    read_zotero_key,
    run_subprocess,
    write_jsonl,
)
from kb_common import safe_print, safe_write, today_iso, vault_path
from zotero_import import DEFAULT_COLLECTION_KEY, ImportResult, import_ranked_paper, preflight


BACKFILL_SELECTIONS = ("top1_candidate", "venue_auto_import", FOCUS_REVIEW_DECISION, "review_queue")
NEW_IMPORT_STATUSES = {"created", "sync_pending"}


def select_backfill_candidates(ranked: list[RankedPaper], *, limit: int) -> list[tuple[RankedPaper, str, str]]:
    selected: list[tuple[RankedPaper, str, str]] = []
    seen: set[str] = set()
    for decision in BACKFILL_SELECTIONS:
        for item in ranked:
            if item.paper.arxiv_id in seen or len(selected) >= limit:
                continue
            if item.decision != decision:
                continue
            seen.add(item.paper.arxiv_id)
            selected.append((item, decision, item.decision))
    return selected


def render_report(
    *,
    run_date: str,
    days_back: int,
    max_candidates: int,
    batch_size: int,
    ranked: list[RankedPaper],
    existing_candidates: list[dict[str, Any]],
    selected: list[tuple[RankedPaper, str, str]],
    imports: list[dict[str, Any]],
    reads: list[dict[str, Any]],
    errors: list[str],
    dry_run: bool,
) -> str:
    lines = [
        "---",
        f'title: "Historical arXiv Backfill - {run_date}"',
        "tags: [arxiv, backfill, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        f'summary: "Historical arXiv backfill candidate report. dry_run={str(dry_run).lower()}."',
        "---",
        "",
        f"# Historical arXiv Backfill - {run_date}",
        "",
        f"- dry_run: {str(dry_run).lower()}",
        f"- days_back: {days_back}",
        f"- max_candidates: {max_candidates}",
        f"- batch_size: {batch_size}",
        f"- candidates_after_existing_prefilter: {len(ranked)}",
        f"- existing_candidates_excluded: {len(existing_candidates)}",
        f"- selected_for_backfill: {len(selected)}",
        f"- imported_or_pending: {sum(1 for item in imports if item.get('status') in NEW_IMPORT_STATUSES)}",
        "- priority_order: top1_candidate, venue_auto_import, focus_review_queue, review_queue",
        "- boundary: historical backfill does not update the daily scout status and does not run Gemini/Codex.",
        "",
        "## Selected Candidates",
        "",
    ]
    if not selected:
        lines.append("- none")
    for item, selection, original in selected:
        paper = item.paper
        lines.append(
            f"- score={item.quality_score} selection={selection} original={original} "
            f"arxiv={paper.arxiv_id} title={paper.title}"
        )
    lines.extend(["", "## Imports", ""])
    if not imports:
        lines.append("- none")
    for item in imports:
        lines.append(
            f"- arxiv={item.get('arxiv_id')} score={item.get('quality_score')} "
            f"status={item.get('status')} zotero_key={item.get('zotero_key', '')} "
            f"message={item.get('message', '')}"
        )
    lines.extend(["", "## Reading", ""])
    if not reads:
        lines.append("- none")
    for item in reads:
        lines.append(f"- zotero_key={item.get('zotero_key')} ingest={item.get('ingest_status')} read={item.get('read_status')}")
    lines.extend(["", "## Existing Excluded Sample", ""])
    if not existing_candidates:
        lines.append("- none")
    for item in existing_candidates[:20]:
        lines.append(
            f"- score={item.get('quality_score')} decision={item.get('decision')} "
            f"arxiv={item.get('arxiv_id')} zotero_key={item.get('zotero_key', '')} title={item.get('title', '')}"
        )
    lines.extend(["", "## Errors", ""])
    lines.extend([f"- {error}" for error in errors] if errors else ["- none"])
    return "\n".join(lines).rstrip() + "\n"


def run_backfill(args: argparse.Namespace) -> int:
    run_date = args.run_date or today_iso()
    errors: list[str] = []
    if args.source == "mirror":
        papers, source_info = query_mirror(queries=args.query or DEFAULT_QUERIES, days_back=args.days_back, max_candidates=args.max_candidates)
    else:
        papers = collect_candidates(
            args.query or DEFAULT_QUERIES,
            max_candidates=args.max_candidates,
            days_back=args.days_back,
            errors=errors,
            fetch_timeout=args.fetch_timeout,
            fetch_retries=args.fetch_retries,
            query_delay=args.query_delay,
        )
        source_info = {"source": "search_api"}
    ranked_all = rank_papers(papers)
    new_ranked_all, existing_candidates, existing_prefilter = exclude_existing_candidates(
        ranked_all,
        collection_key=args.collection,
    )
    if existing_prefilter.startswith("failed:"):
        errors.append(f"existing_prefilter_{existing_prefilter}")
    selected = select_backfill_candidates(new_ranked_all, limit=args.batch_size)

    backfill_dir = vault_path("projects", "arxiv-daily", "backfill")
    candidates_path = backfill_dir / f"{run_date}-historical-backfill-candidates.jsonl"
    report_path = backfill_dir / f"{run_date}-2025-backfill.md"

    if args.dry_run:
        safe_print(
            "DRY-RUN "
            f"days_back={args.days_back} "
            f"source={source_info.get('source', args.source)} "
            f"max_candidates={args.max_candidates} "
            f"existing_excluded={len(existing_candidates)} "
            f"selected={len(selected)} "
            f"top1={sum(1 for item in new_ranked_all if item.decision == 'top1_candidate')} "
            f"venue_auto={sum(1 for item in new_ranked_all if item.decision == 'venue_auto_import')} "
            f"focus_review={sum(1 for item in new_ranked_all if item.decision == FOCUS_REVIEW_DECISION)} "
            f"review={sum(1 for item in new_ranked_all if item.decision == 'review_queue')}"
        )
        for item, selection, original in selected:
            safe_print(f"{item.quality_score:3d} {selection:17s} original={original:17s} {item.paper.arxiv_id} {item.paper.title}")
        if args.write_report:
            write_jsonl(candidates_path, [item.to_dict() for item in new_ranked_all[: args.max_candidates]], dry_run=False)
            safe_write(
                report_path,
                render_report(
                    run_date=run_date,
                    days_back=args.days_back,
                    max_candidates=args.max_candidates,
                    batch_size=args.batch_size,
                    ranked=new_ranked_all[: args.max_candidates],
                    existing_candidates=existing_candidates,
                    selected=selected,
                    imports=[],
                    reads=[],
                    errors=errors,
                    dry_run=True,
                ),
                dry_run=False,
                backup=True,
            )
            safe_print(f"REPORT: {report_path.relative_to(vault_path())}")
        for error in errors:
            safe_print(f"WARN: {error}")
        return 0

    pf = preflight(args.collection)
    if not (pf.get("local_read") and pf.get("write_credentials")):
        for error in pf.get("errors", []):
            safe_print(f"ERROR: {error}")
        return 2

    imports: list[dict[str, Any]] = []
    reads: list[dict[str, Any]] = []
    for ranked_item, selection, original in selected:
        paper = ranked_item.paper
        try:
            result = import_ranked_paper(ranked_item, collection_key=args.collection, dry_run=False)
        except Exception as exc:
            result = ImportResult(status="failed", message=str(exc), mode="web_api")
        imports.append(
            {
                "arxiv_id": paper.arxiv_id,
                "quality_score": ranked_item.quality_score,
                "selection_decision": selection,
                "original_decision": original,
                **result.to_dict(),
            }
        )
        if result.status not in NEW_IMPORT_STATUSES or not result.zotero_key:
            errors.append(f"backfill_import_not_ready:{paper.arxiv_id}:{result.status}:{result.message}")
            continue
        ingest_status, ingest_output = ingest_zotero_key(result.zotero_key)
        read_status = "skipped"
        read_output = ""
        if not args.skip_read and ingest_status == "success":
            read_status, read_output = read_zotero_key(result.zotero_key, timeout=args.read_timeout)
        reads.append(
            {
                "zotero_key": result.zotero_key,
                "ingest_status": ingest_status,
                "ingest_output_tail": ingest_output[-1200:],
                "read_status": read_status,
                "read_output_tail": read_output[-1200:],
            }
        )
        if ingest_status != "success":
            errors.append(f"backfill_ingest_failed:{result.zotero_key}")
        if read_status not in {"skipped"} and not read_status.startswith("success"):
            errors.append(f"backfill_read_failed:{result.zotero_key}:{read_status}")

    if reads and not args.skip_read:
        code, output = run_subprocess([sys.executable, ".claude/scripts/fix_strict_kb_after_read.py"], timeout=300)
        if code != 0:
            errors.append(f"strict_kb_maintenance_failed:{output[-400:]}")

    write_jsonl(candidates_path, [item.to_dict() for item in new_ranked_all[: args.max_candidates]], dry_run=False)
    safe_write(
        report_path,
        render_report(
            run_date=run_date,
            days_back=args.days_back,
            max_candidates=args.max_candidates,
            batch_size=args.batch_size,
            ranked=new_ranked_all[: args.max_candidates],
            existing_candidates=existing_candidates,
            selected=selected,
            imports=imports,
            reads=reads,
            errors=errors,
            dry_run=False,
        ),
        dry_run=False,
        backup=True,
    )
    safe_print(f"REPORT: {report_path.relative_to(vault_path())}")
    if errors:
        safe_print("BACKFILL_STATUS: partial")
        for error in errors:
            safe_print(f"ERROR: {error}")
        return 2
    safe_print("BACKFILL_STATUS: success")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", default="")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Preview only. Use --execute to write Zotero/vault outputs.")
    parser.add_argument("--execute", dest="dry_run", action="store_false", help="Actually import the selected backfill batch.")
    parser.add_argument("--write-report", action="store_true", help="Write a dry-run backfill report under projects/arxiv-daily/backfill.")
    parser.add_argument("--source", choices=["mirror", "search-api"], default="mirror")
    parser.add_argument("--query", action="append", help="Override default arXiv query; can be repeated.")
    parser.add_argument("--days-back", type=int, default=480)
    parser.add_argument("--max-candidates", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION_KEY)
    parser.add_argument("--fetch-timeout", type=int, default=20)
    parser.add_argument("--fetch-retries", type=int, default=1)
    parser.add_argument("--query-delay", type=float, default=3.2)
    parser.add_argument("--skip-read", action="store_true")
    parser.add_argument("--read-timeout", type=int, default=3600)
    return run_backfill(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
