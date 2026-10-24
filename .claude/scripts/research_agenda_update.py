"""Update the long-term research agenda after reading papers."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Any

from kb_common import safe_print, safe_write, vault_path
from research_agenda_common import (
    AGENDA_ROOT,
    CONCEPT_DELTA_DIR,
    DAILY_DIR,
    EVIDENCE_MATRIX,
    IDEA_BANK_DIR,
    MECHANISM_GRAPH_DIR,
    PROBLEM_POOL_DIR,
    REVIEWS_DIR,
    ensure_agenda_dirs,
    load_evidence_matrix,
    merge_evidence_records,
    note_link,
    read_frontmatter,
    rel,
    render_frontmatter,
    split_csv,
    write_jsonl,
)
from research_agenda_extract import _structured_fields, extract_records, validate_records, write_paper_cards
from research_agenda_ideate import generate_seed_report
from generate_knowledge_diagrams import build_paper_packet, render_paper_markdown
from research_agenda_review import iter_idea_folders, review_folder


POOL_FILES = {
    "open_questions.md": {"claim_types": {"open_question", "limitation"}, "title": "Open Questions"},
    "contradictions.md": {"claim_types": {"method", "limitation"}, "title": "Potential Contradictions"},
    "missing_experiments.md": {"claim_types": {"metric", "evidence_note", "limitation"}, "title": "Missing Experiments"},
    "failure_modes.md": {"claim_types": {"limitation", "open_question"}, "title": "Failure Modes"},
    "transfer_opportunities.md": {"claim_types": {"method", "task", "sensor", "paper_summary"}, "title": "Transfer Opportunities"},
}
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")


def _source_count(records: list[dict[str, Any]]) -> int:
    return len({record.get("source_note") for record in records})


def _domain_counts(records: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for record in records:
        for domain in record.get("domains", []):
            counts[domain] += 1
    return counts


def _group_counts(seed_report: dict[str, Any]) -> Counter[str]:
    return Counter(str(item.get("candidate_group", "unclassified") or "unclassified") for item in seed_report.get("greenhouse", []))


def _portfolio_summary(seed_report: dict[str, Any]) -> dict[str, Any]:
    summary = seed_report.get("portfolio_summary")
    if isinstance(summary, dict) and summary:
        return summary
    greenhouse = seed_report.get("greenhouse", [])
    return {
        "origin_type_counts": dict(Counter(str(item.get("origin_type", "unclassified") or "unclassified") for item in greenhouse)),
        "research_claim_type_counts": dict(Counter(str(item.get("research_claim_type", "unclassified") or "unclassified") for item in greenhouse)),
        "bottleneck_type_counts": dict(Counter(str(item.get("bottleneck_type", "unclassified") or "unclassified") for item in greenhouse)),
        "evidence_mode_counts": dict(Counter(str(item.get("evidence_mode", "unclassified") or "unclassified") for item in greenhouse)),
        "risk_class_counts": dict(Counter(str(item.get("risk_class", "unclassified") or "unclassified") for item in greenhouse)),
        "portfolio_slot_counts": dict(Counter(str(item.get("portfolio_slot", "unclassified") or "unclassified") for item in greenhouse)),
        "warnings": [],
    }


def _readiness_tier(item: dict[str, Any]) -> str:
    label = str(item.get("greenhouse_label", "unlabeled"))
    if label == "promoted_to_seed":
        return str(item.get("readiness_tier", "seed_ready"))
    if label == "speculative_preserve":
        return str(item.get("readiness_tier", "speculative_weekly_review"))
    if label == "rewrite_needed":
        return str(item.get("readiness_tier", "rewrite_required"))
    if label == "parked_for_weekly_review":
        return str(item.get("readiness_tier", "weekly_review"))
    if label == "blocked_with_rescue_signal":
        return str(item.get("readiness_tier", "rescue_only"))
    return str(item.get("readiness_tier", "untriaged"))


def _records_for_pool(records: list[dict[str, Any]], claim_types: set[str]) -> list[dict[str, Any]]:
    selected = [record for record in records if record.get("claim_type") in claim_types]
    return sorted(selected, key=lambda item: (item.get("source_note", ""), item.get("claim_type", "")))


def _pool_item(record: dict[str, Any]) -> str:
    title = record.get("source_title", Path(record.get("source_note", "")).stem)
    domains = ", ".join(record.get("domains", [])[:5]) or "-"
    return (
        f"- {note_link(record.get('source_note', ''), title)} "
        f"`{record.get('claim_type')}` domains={domains}: {record.get('statement', '')[:260]}"
    )


def _source_path(source_note: str) -> Path:
    return vault_path(*Path(source_note).parts)


def _section_text(body: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", flags=re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", body[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(body)
    return body[start:end].strip()


def _concept_page_exists(label: str) -> bool:
    concept_dir = vault_path("wiki", "concepts")
    candidates = {
        label.strip(),
        label.strip().lower(),
        label.strip().replace(" ", "-").lower(),
    }
    return any((concept_dir / f"{candidate}.md").exists() for candidate in candidates if candidate)


def _concepts_for_source(source_note: str, records: list[dict[str, Any]]) -> list[str]:
    concepts: set[str] = set()
    path = _source_path(source_note)
    if path.exists():
        _, body = read_frontmatter(path)
        section = _section_text(body, "相关概念")
        for match in WIKILINK_RE.finditer(section):
            concepts.add((match.group(2) or match.group(1)).strip())
    for record in records:
        if record.get("source_note") == source_note:
            concepts.update(str(domain).strip() for domain in record.get("domains", []) if str(domain).strip())
    return sorted(concepts)


def build_concept_delta(run_date: str, focus_records: list[dict[str, Any]], merged_records: list[dict[str, Any]]) -> dict[str, Any]:
    focus_sources = sorted({record.get("source_note", "") for record in focus_records if record.get("source_note")})
    records_by_source: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in merged_records:
        if record.get("source_note"):
            records_by_source[str(record.get("source_note"))].append(record)
    focus_concepts: dict[str, set[str]] = defaultdict(set)
    total_sources: dict[str, set[str]] = defaultdict(set)
    for source, items in records_by_source.items():
        for concept in _concepts_for_source(source, items):
            total_sources[concept].add(source)
            if source in focus_sources:
                focus_concepts[concept].add(source)
    concept_items: list[dict[str, Any]] = []
    for label, sources in sorted(focus_concepts.items(), key=lambda item: (-len(item[1]), item[0].lower())):
        page_exists = _concept_page_exists(label)
        status = "missing_concept_page" if not page_exists else ("strengthened" if len(total_sources[label]) > len(sources) or len(sources) > 1 else "observed")
        concept_items.append(
            {
                "label": label,
                "status": status,
                "focus_paper_count": len(sources),
                "total_paper_count": len(total_sources[label]),
                "focus_sources": sorted(sources),
                "strong_sources": sorted(total_sources[label])[:8],
                "concept_page_exists": page_exists,
            }
        )
    return {
        "schema_version": "concept_delta.v1",
        "run_date": run_date,
        "focus_sources": focus_sources,
        "focus_paper_count": len(focus_sources),
        "concept_count": len(concept_items),
        "missing_concept_page_count": sum(1 for item in concept_items if item["status"] == "missing_concept_page"),
        "concepts": concept_items,
        "boundary": "Local concept delta only; missing concept pages require human review and do not block daily automation.",
    }


def render_concept_delta(delta: dict[str, Any]) -> str:
    run_date = str(delta["run_date"])
    lines = [
        render_frontmatter(
            f"Concept Delta - {run_date}",
            ["research-agenda", "concept-delta"],
            "Daily local concept changes inferred from newly read papers.",
        ).rstrip(),
        f"# Concept Delta - {run_date}",
        "",
        f"- schema_version: {delta.get('schema_version')}",
        f"- focus_paper_count: {delta.get('focus_paper_count', 0)}",
        f"- concept_count: {delta.get('concept_count', 0)}",
        f"- missing_concept_page_count: {delta.get('missing_concept_page_count', 0)}",
        "- boundary: concept gaps are review signals, not automation failures.",
        "",
        "## Focus Papers",
        "",
    ]
    if not delta.get("focus_sources"):
        lines.append("- none")
    for source in delta.get("focus_sources", []):
        lines.append(f"- {note_link(source)}")
    lines.extend(["", "## Concept Signals", ""])
    if not delta.get("concepts"):
        lines.append("- no concept signal extracted.")
    for item in delta.get("concepts", []):
        sources = ", ".join(note_link(source) for source in item.get("focus_sources", [])[:4])
        lines.append(
            f"- **{item.get('label')}**: status={item.get('status')} "
            f"focus_papers={item.get('focus_paper_count')} total_papers={item.get('total_paper_count')} "
            f"sources={sources or '-'}"
        )
    lines.extend(["", "## Human Attention", ""])
    gaps = [item for item in delta.get("concepts", []) if item.get("status") == "missing_concept_page"]
    if not gaps:
        lines.append("- none")
    for item in gaps[:20]:
        lines.append(f"- missing_concept_page: {item.get('label')} ({item.get('focus_paper_count')} focus papers)")
    return "\n".join(lines).rstrip() + "\n"


def _mermaid_label(value: str, *, limit: int = 88) -> str:
    text = " ".join(str(value or "-").replace('"', "'").replace("[", "(").replace("]", ")").split())
    if len(text) > limit:
        text = text[: limit - 1].rstrip() + "…"
    return text or "-"


def render_mechanism_graph(path: Path, run_date: str) -> str:
    packet = build_paper_packet(path, depth="lightweight")
    packet["run_date"] = run_date
    return render_paper_markdown(packet)


def write_concept_delta(delta: dict[str, Any], *, dry_run: bool) -> tuple[Path, Path]:
    run_date = str(delta["run_date"])
    json_path = CONCEPT_DELTA_DIR / f"{run_date}-concept-delta.json"
    md_path = CONCEPT_DELTA_DIR / f"{run_date}-concept-delta.md"
    safe_write(json_path, json.dumps(delta, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=True)
    safe_write(md_path, render_concept_delta(delta), dry_run=dry_run, backup=True)
    return json_path, md_path


def write_mechanism_graphs(run_date: str, focus_records: list[dict[str, Any]], *, dry_run: bool) -> list[Path]:
    out_dir = MECHANISM_GRAPH_DIR / run_date
    written: list[Path] = []
    for source in sorted({record.get("source_note", "") for record in focus_records if record.get("source_note")}):
        source_path = _source_path(source)
        if not source_path.exists():
            continue
        out_path = out_dir / f"{Path(source).stem}.md"
        json_path = out_dir / f"{Path(source).stem}.json"
        packet = build_paper_packet(source_path, depth="lightweight")
        packet["run_date"] = run_date
        safe_write(out_path, render_paper_markdown(packet), dry_run=dry_run, backup=True)
        safe_write(json_path, json.dumps(packet, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=True)
        written.append(out_path)
    return written


def render_pool_file(filename: str, records: list[dict[str, Any]]) -> str:
    meta = POOL_FILES[filename]
    selected = _records_for_pool(records, meta["claim_types"])
    lines = [
        render_frontmatter(meta["title"], ["research-agenda", "problem-pool"], f"Long-term agenda pool: {meta['title']}.").rstrip(),
        f"# {meta['title']}",
        "",
        "- source: projects/research-agenda/evidence/evidence_matrix.jsonl",
        "- rule: rebuilt deterministically from local done-paper evidence.",
        "",
    ]
    if filename == "contradictions.md":
        by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in selected:
            for domain in record.get("domains", [])[:4]:
                by_domain[domain].append(record)
        lines.extend(["## Potential Tensions To Review", ""])
        for domain, items in sorted(by_domain.items(), key=lambda item: (-len(item[1]), item[0]))[:20]:
            methods = [item for item in items if item.get("claim_type") == "method"]
            limits = [item for item in items if item.get("claim_type") == "limitation"]
            if not methods or not limits:
                continue
            lines.append(f"## {domain}")
            lines.append("")
            lines.append(f"- method_signal: {methods[0].get('statement', '')[:220]}")
            lines.append(f"- limitation_signal: {limits[0].get('statement', '')[:220]}")
            lines.append("- review_need: check whether the method claim and limitation imply a real research gap.")
            lines.append("")
    else:
        lines.extend(["## Items", ""])
        if not selected:
            lines.append("- evidence_gap: no matching evidence records yet.")
        else:
            lines.extend(_pool_item(item) for item in selected[:80])
    return "\n".join(lines).rstrip() + "\n"


def render_readme() -> str:
    return "\n".join(
        [
            render_frontmatter(
                "Research Agenda README",
                ["research-agenda", "manual"],
                "How the long-term research agenda system should be used.",
            ).rstrip(),
            "# Research Agenda",
            "",
            "This folder is the long-term research agenda system. It is not a daily idea dump.",
            "",
            "Daily arXiv reading adds evidence, problem signals, and transfer opportunities. v2 raw candidates and formal seed publication are handled by the transactional state-machine scripts.",
            "",
            "## Workflow",
            "",
            "1. Read papers into `wiki/topics/` until they are `status: done`.",
            "2. Extract evidence into `evidence/evidence_matrix.jsonl`.",
            "3. Update `problem_pool/` and daily agenda delta.",
            "4. Generate raw candidates with `research_agenda_ideate.py` into `runs/YYYY-MM-DD/artifacts/raw-candidates.json`.",
            "5. Publish formal seeds only through `publish_research_run.py` after v2 review and survival artifacts pass validation.",
            "",
        ]
    )


def render_dashboard(records: list[dict[str, Any]], seed_count: int, seed_report: dict[str, Any] | None = None) -> str:
    domains = _domain_counts(records)
    maturity = [review_folder(folder, state) for state, folder in iter_idea_folders()]
    state_counts = Counter(item["state"] for item in maturity)
    developing_ready = sum(1 for item in maturity if item["developing_ready"])
    promoted_ready = sum(1 for item in maturity if item["promoted_ready"])
    similar_ready = sum(1 for item in maturity if item["has_similar_work"])
    experiment_ready = sum(1 for item in maturity if item["has_experiment_plan"])
    evidence_ge8 = sum(1 for item in maturity if item["evidence_count"] >= 8)
    quality_blocked = sum(1 for item in maturity if item.get("quality_flags"))
    generated_experiment_ready = sum(1 for item in maturity if item.get("has_generated_experiment_plan"))
    seed_report = seed_report or {}
    group_counts = _group_counts(seed_report)
    portfolio = _portfolio_summary(seed_report)
    lines = [
        render_frontmatter(
            "Research Agenda Dashboard",
            ["research-agenda", "dashboard"],
            "Current state of the long-term research agenda.",
        ).rstrip(),
        "# Research Agenda Dashboard",
        "",
        f"- evidence_records: {len(records)}",
        f"- evidence_sources: {_source_count(records)}",
        f"- seed_candidates_created_or_updated_last_run: {seed_count}",
        "",
        "## Idea Bank",
        "",
    ]
    lines.extend(f"- {state}: {state_counts.get(state, 0)}" for state in ["seed", "developing", "promoted", "pilot-ready", "rejected", "archived"])
    lines.extend(
        [
            "",
            "## Maturity Gate",
            "",
            f"- developing_ready: {developing_ready}",
            f"- promoted_ready: {promoted_ready}",
            f"- ideas_with_completed_similar_work: {similar_ready}",
            f"- ideas_with_completed_experiment_plan: {experiment_ready}",
            f"- ideas_with_generated_complete_experiment_plan: {generated_experiment_ready}",
            f"- ideas_with_8_done_evidence_sources: {evidence_ge8}",
            f"- ideas_blocked_by_quality_gate: {quality_blocked}",
            "- boundary: seed ideas are not high-quality research proposals until the maturity gate is passed.",
            "",
            "## Idea Generation Quality",
            "",
            f"- generator_mode: {seed_report.get('mode', 'unknown')}",
            f"- generator_backend: {seed_report.get('generator', 'unknown')}",
            f"- generator_status: {seed_report.get('generator_status', 'unknown')}",
            f"- high_quality_seed_candidates: {len(seed_report.get('high_quality', []))}",
            f"- raw_gemini_candidates: {len(seed_report.get('greenhouse', []))}",
            f"- raw_candidate_limit: {seed_report.get('raw_candidate_limit', '-')}",
            f"- min_raw_candidates: {seed_report.get('min_raw_candidates', '-')}",
            f"- free_divergence: {seed_report.get('free_divergence', False)}",
            f"- free_divergence_start_date: {seed_report.get('free_divergence_start_date', '-')}",
            f"- candidate_group_evidence_bound: {group_counts.get('evidence_bound', 0)}",
            f"- candidate_group_wild_engineering: {group_counts.get('wild_engineering', 0)}",
            f"- portfolio_origin_type_counts: {json.dumps(portfolio.get('origin_type_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- portfolio_research_claim_type_counts: {json.dumps(portfolio.get('research_claim_type_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- portfolio_bottleneck_type_counts: {json.dumps(portfolio.get('bottleneck_type_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- portfolio_risk_class_counts: {json.dumps(portfolio.get('risk_class_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- portfolio_slot_counts: {json.dumps(portfolio.get('portfolio_slot_counts', {}), ensure_ascii=False, sort_keys=True)}",
            f"- portfolio_warnings: {json.dumps(portfolio.get('warnings', []), ensure_ascii=False)}",
            f"- parked_candidates: {len(seed_report.get('parked', []))}",
            f"- blocked_candidates: {len(seed_report.get('blocked', []))}",
            f"- quality_tier_S: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'S')}",
            f"- quality_tier_A: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'A')}",
            f"- quality_tier_B: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'B')}",
            f"- quality_tier_C: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'C')}",
            "- quality_tier_semantics: potential_only_not_seed_readiness",
            f"- potential_tier_S: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'S')}",
            f"- potential_tier_A: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'A')}",
            f"- potential_tier_B: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'B')}",
            f"- potential_tier_C: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'C')}",
            f"- readiness_seed_ready: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'seed_ready')}",
            f"- readiness_rewrite_required: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'rewrite_required')}",
            f"- readiness_weekly_review: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'weekly_review')}",
            f"- readiness_speculative_weekly_review: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'speculative_weekly_review')}",
            f"- readiness_rescue_only: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'rescue_only')}",
            f"- no_high_quality_seed_today_reason: {seed_report.get('no_high_quality_seed_today_reason') or '-'}",
            "",
            "## Daily Quality Review",
            "",
            "- codex_seed_review_task: `DailyCodexSeedReview` at 16:30 local time.",
            "- codex_review_output: `projects/research-agenda/reviews/YYYY-MM-DD-codex-seed-review.md`",
            "- boundary: Codex reviews shortlist, rewrite, park, and rescue; it does not auto-promote paper claims.",
        ]
    )
    lines.extend(["", "## Dominant Evidence Domains", ""])
    if not domains:
        lines.append("- evidence_gap: no matrix records yet.")
    else:
        lines.extend(f"- {domain}: {count}" for domain, count in domains.most_common(15))
    lines.extend(
        [
            "",
            "## Core Files",
            "",
            "- [[open_questions]]",
            "- [[contradictions]]",
            "- [[missing_experiments]]",
            "- [[failure_modes]]",
            "- [[transfer_opportunities]]",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_daily_delta(
    *,
    run_date: str,
    focus_keys: list[str],
    new_records: list[dict[str, Any]],
    merged_records: list[dict[str, Any]],
    seeds: list[tuple[dict[str, Any], list[dict[str, Any]], int]],
    seed_report: dict[str, Any],
    missing: list[str],
    rebuild_all: bool,
    concept_delta_path: Path | None = None,
    concept_delta: dict[str, Any] | None = None,
    mechanism_graph_paths: list[Path] | None = None,
    sidecar_warnings: list[str] | None = None,
    battle_result: dict[str, Any] | None = None,
) -> str:
    focus_sources = sorted({record["source_note"] for record in new_records})
    update_scope = "full_matrix_rebuild" if rebuild_all else "daily_focus_update"
    evidence_heading = "Rebuilt Evidence Sample" if rebuild_all else "Newly Read Evidence"
    group_counts = _group_counts(seed_report)
    portfolio = _portfolio_summary(seed_report)
    snippet_coverage = sum(1 for record in new_records if record.get("source_snippet"))
    mechanism_graph_paths = mechanism_graph_paths or []
    sidecar_warnings = sidecar_warnings or []
    battle_result = battle_result or {}
    lines = [
        render_frontmatter(
            f"Research Agenda Delta - {run_date}",
            ["research-agenda", "daily", "agenda-delta"],
            "Daily research agenda update from newly read papers and the long-term evidence matrix.",
        ).rstrip(),
        f"# Research Agenda Delta - {run_date}",
        "",
        f"- update_scope: {update_scope}",
        f"- focus_zotero_keys: {', '.join(focus_keys) if focus_keys else '-'}",
        f"- evidence_records_in_update: {len(new_records)}",
        f"- evidence_sources_in_update: {len(focus_sources)}",
        f"- evidence_snippet_coverage: {snippet_coverage}/{len(new_records)}",
        f"- matrix_records_total: {len(merged_records)}",
        f"- matrix_sources_total: {_source_count(merged_records)}",
        f"- concept_delta_file: `{rel(concept_delta_path) if concept_delta_path else '-'}`",
        f"- concept_delta_concepts: {concept_delta.get('concept_count', 0) if concept_delta else 0}",
        f"- mechanism_graph_dir: `{rel(MECHANISM_GRAPH_DIR / run_date)}`",
        f"- mechanism_graphs_created: {len(mechanism_graph_paths)}",
        f"- notemd_sidecar_warnings: {len(sidecar_warnings)}",
        f"- idea_generator: {seed_report.get('generator', '-')}",
        f"- idea_generator_status: {seed_report.get('generator_status', '-')}",
        f"- gemini_model: {seed_report.get('gemini_model', '-')}",
        f"- raw_candidate_limit: {seed_report.get('raw_candidate_limit', '-')}",
        f"- min_raw_candidates: {seed_report.get('min_raw_candidates', '-')}",
        f"- free_divergence: {seed_report.get('free_divergence', False)}",
        f"- free_divergence_start_date: {seed_report.get('free_divergence_start_date', '-')}",
        f"- raw_gemini_candidates: {len(seed_report.get('greenhouse', []))}",
        f"- candidate_group_evidence_bound: {group_counts.get('evidence_bound', 0)}",
        f"- candidate_group_wild_engineering: {group_counts.get('wild_engineering', 0)}",
        f"- portfolio_origin_type_counts: {json.dumps(portfolio.get('origin_type_counts', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_research_claim_type_counts: {json.dumps(portfolio.get('research_claim_type_counts', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_bottleneck_type_counts: {json.dumps(portfolio.get('bottleneck_type_counts', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_evidence_mode_counts: {json.dumps(portfolio.get('evidence_mode_counts', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_risk_class_counts: {json.dumps(portfolio.get('risk_class_counts', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_slot_counts: {json.dumps(portfolio.get('portfolio_slot_counts', {}), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_warnings: {json.dumps(portfolio.get('warnings', []), ensure_ascii=False)}",
        f"- high_quality_seed_candidates: {len(seeds)}",
        f"- parked_candidates: {len(seed_report.get('parked', []))}",
        f"- blocked_candidates: {len(seed_report.get('blocked', []))}",
        f"- quality_tier_S: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'S')}",
        f"- quality_tier_A: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'A')}",
        f"- quality_tier_B: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'B')}",
        f"- quality_tier_C: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('quality_tier') == 'C')}",
        "- quality_tier_semantics: potential_only_not_seed_readiness",
        f"- potential_tier_S: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'S')}",
        f"- potential_tier_A: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'A')}",
        f"- potential_tier_B: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'B')}",
        f"- potential_tier_C: {sum(1 for item in seed_report.get('greenhouse', []) if item.get('potential_tier', item.get('quality_tier')) == 'C')}",
        f"- readiness_seed_ready: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'seed_ready')}",
        f"- readiness_rewrite_required: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'rewrite_required')}",
        f"- readiness_weekly_review: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'weekly_review')}",
        f"- readiness_speculative_weekly_review: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'speculative_weekly_review')}",
        f"- readiness_rescue_only: {sum(1 for item in seed_report.get('greenhouse', []) if _readiness_tier(item) == 'rescue_only')}",
        f"- no_high_quality_seed_today_reason: {seed_report.get('no_high_quality_seed_today_reason') or '-'}",
        f"- mandatory_model_battle_status: {battle_result.get('status', 'not_run')}",
        f"- mandatory_model_battle_report: `{battle_result.get('review_path') or '-'}`",
        f"- mandatory_model_battle_packet: `{battle_result.get('packet_path') or '-'}`",
        "",
        f"## {evidence_heading}",
        "",
    ]
    if not focus_sources:
        lines.append("- evidence_gap: no newly read done-paper sources were found for this update.")
    display_sources = focus_sources[:40] if rebuild_all else focus_sources
    for source in display_sources:
        title = next((record.get("source_title", Path(source).stem) for record in new_records if record["source_note"] == source), Path(source).stem)
        lines.append(f"- {note_link(source, title)}")
    if rebuild_all and len(focus_sources) > len(display_sources):
        lines.append(f"- omitted_rebuild_sources: {len(focus_sources) - len(display_sources)}")
    lines.extend(["", "## Problem Pool Changes", ""])
    for name in POOL_FILES:
        lines.append(f"- updated: `projects/research-agenda/problem_pool/{name}`")
    lines.extend(["", "## High Quality Seed Candidates", ""])
    if not seeds:
        lines.append("- no_high_quality_seed_today: no candidate passed the mechanism evidence gate.")
    for axis, evidence, recent in seeds:
        lines.append(
            f"- {axis['title']}: local_sources={_source_count(evidence)} recent_sources={recent} "
            f"mechanism={axis.get('mechanism', '-')[:140]}"
        )
    lines.extend(["", "## Gemini Greenhouse Candidates", ""])
    greenhouse = seed_report.get("greenhouse", [])
    if not greenhouse:
        lines.append("- none")
    for item in greenhouse[:12]:
        issues = ", ".join(item.get("issues", [])) or "-"
        lines.append(
            f"- {item.get('title')}: label={item.get('greenhouse_label', 'unlabeled')} "
            f"group={item.get('candidate_group', '-')} "
            f"origin={item.get('origin_type', '-')} "
            f"claim={item.get('research_claim_type', '-')} "
            f"bottleneck={item.get('bottleneck_type', '-')} "
            f"risk={item.get('risk_class', '-')} "
            f"slot={item.get('portfolio_slot', '-')} "
            f"quality_tier={item.get('quality_tier', '-')} "
            f"potential_tier={item.get('potential_tier', item.get('quality_tier', '-'))} "
            f"readiness_tier={_readiness_tier(item)} "
            f"promotion_decision={item.get('promotion_decision', '-')} "
            f"research_quality_score={item.get('research_quality_score', '-')} "
            f"evidence_support_score={item.get('evidence_support_score', item.get('score', '-'))} "
            f"support_score={item.get('support_score', '-')} "
            f"originality_score={item.get('originality_score', '-')} "
            f"engineering_value_score={item.get('engineering_value_score', '-')} "
            f"sharpness_score={item.get('sharpness_score', '-')} "
            f"evidence_execution_score={item.get('evidence_execution_score', '-')} "
            f"ordinaryness_penalty={item.get('ordinaryness_penalty', '-')} "
            f"novelty_pressure={item.get('novelty_pressure', {}).get('pressure', '-') if isinstance(item.get('novelty_pressure'), dict) else '-'} "
            f"issues={issues}"
        )
    lines.extend(["", "## Parked Candidates", ""])
    parked = seed_report.get("parked", [])
    if not parked:
        lines.append("- none")
    for item in parked[:8]:
        issues = ", ".join(item.get("issues", [])) or "-"
        lines.append(f"- {item.get('title')}: reason={item.get('park_reason', 'not_selected')} issues={issues}")
    lines.extend(["", "## Blocked Candidates", ""])
    blocked = seed_report.get("blocked", [])
    if not blocked:
        lines.append("- none")
    for item in blocked[:8]:
        issues = ", ".join(item.get("issues", [])) or "-"
        lines.append(f"- {item.get('title')}: issues={issues}")
    if missing:
        lines.extend(["", "## Evidence Gaps", ""])
        lines.extend(f"- missing_zotero_key: {key}" for key in missing)
    if sidecar_warnings:
        lines.extend(["", "## Sidecar Warnings", ""])
        lines.extend(f"- {warning}" for warning in sidecar_warnings)
    lines.extend(["", "## Mandatory Gemini DeepSeek Battle", ""])
    if battle_result:
        lines.append(f"- status: {battle_result.get('status', '-')}")
        lines.append(f"- selected_items: {battle_result.get('selected_items', 0)}")
        lines.append(f"- report: `{battle_result.get('review_path') or '-'}`")
        lines.append(f"- mutation_actions: {json.dumps(battle_result.get('mutation_actions', {}), ensure_ascii=False, sort_keys=True)}")
        if battle_result.get("deepseek_error"):
            lines.append(f"- deepseek_error: {battle_result.get('deepseek_error')}")
        if battle_result.get("gemini_error"):
            lines.append(f"- gemini_error: {battle_result.get('gemini_error')}")
    else:
        lines.append("- not_run")
    lines.extend(["", "## Boundary", "", "- This daily delta is not a validated idea list. It only updates the long-term agenda."])
    return "\n".join(lines).rstrip() + "\n"


def run_update(args: argparse.Namespace) -> int:
    ensure_agenda_dirs()
    focus_keys = split_csv(args.zotero_keys)
    rebuild_all = args.all or not EVIDENCE_MATRIX.exists()
    base_records = [] if rebuild_all else load_evidence_matrix()
    all_records: list[dict[str, Any]] = []
    missing: list[str] = []
    if rebuild_all:
        all_records, all_missing = extract_records(all_notes=True, zotero_keys=[], run_date=args.run_date)
        missing.extend(all_missing)
    focus_records: list[dict[str, Any]] = []
    if focus_keys:
        focus_records, focus_missing = extract_records(all_notes=False, zotero_keys=focus_keys, run_date=args.run_date)
        missing.extend(focus_missing)
    new_records = merge_evidence_records([], [*all_records, *focus_records])
    issues = validate_records(new_records)
    if issues:
        for issue in issues[:20]:
            safe_print(f"ERROR {issue}")
        return 1
    merged = merge_evidence_records(base_records, new_records)
    sidecar_records = focus_records or all_records
    concept_json_path = CONCEPT_DELTA_DIR / f"{args.run_date}-concept-delta.json"
    concept_md_path = CONCEPT_DELTA_DIR / f"{args.run_date}-concept-delta.md"
    sidecar_warnings: list[str] = []
    try:
        concept_delta = build_concept_delta(args.run_date, sidecar_records, merged)
    except Exception as exc:
        concept_delta = {
            "schema_version": "concept_delta.v1",
            "run_date": args.run_date,
            "focus_sources": [],
            "focus_paper_count": 0,
            "concept_count": 0,
            "missing_concept_page_count": 0,
            "concepts": [],
            "error": f"{type(exc).__name__}:{exc}",
            "boundary": "Concept delta generation failed; this sidecar does not block daily automation.",
        }
        sidecar_warnings.append(f"concept_delta_failed:{type(exc).__name__}:{exc}")
    mechanism_graph_paths = [
        MECHANISM_GRAPH_DIR / args.run_date / f"{Path(source).stem}.md"
        for source in sorted({record.get("source_note", "") for record in sidecar_records if record.get("source_note")})
    ]
    if not args.dry_run:
        try:
            write_concept_delta(concept_delta, dry_run=False)
        except Exception as exc:
            sidecar_warnings.append(f"concept_delta_write_failed:{type(exc).__name__}:{exc}")
            safe_print(f"WARN concept_delta_write_failed:{type(exc).__name__}:{exc}")
        try:
            mechanism_graph_paths = write_mechanism_graphs(args.run_date, sidecar_records, dry_run=False)
        except Exception as exc:
            sidecar_warnings.append(f"mechanism_graph_write_failed:{type(exc).__name__}:{exc}")
            safe_print(f"WARN mechanism_graph_write_failed:{type(exc).__name__}:{exc}")
    if args.idea_generator != "none":
        safe_print("WARN research_agenda_update_is_evidence_only: idea generation moved to research_agenda_ideate.py v2 raw-candidate stage")
    seed_report = generate_seed_report(
        merged,
        focus_keys=focus_keys,
        limit=args.max_generated,
        include_dynamic=args.include_dynamic,
        mode=args.idea_mode,
        generator="none",
        generator_timeout=args.idea_timeout,
        raw_candidate_limit=args.raw_candidate_limit,
        min_raw_candidates=args.min_raw_candidates,
        gemini_model=args.gemini_model,
        run_date=args.run_date,
    )
    seeds = seed_report["high_quality"]

    safe_print(
        "AGENDA_UPDATE "
        f"rebuild_all={rebuild_all} new_records={len(new_records)} "
        f"matrix_total={len(merged)} high_quality={len(seeds)} "
        f"parked={len(seed_report.get('parked', []))} blocked={len(seed_report.get('blocked', []))} "
        f"greenhouse={len(seed_report.get('greenhouse', []))} "
        f"concepts={concept_delta.get('concept_count', 0)} "
        f"mechanism_graphs={len(mechanism_graph_paths)} "
        f"sidecar_warnings={len(sidecar_warnings)} "
        f"generator={seed_report.get('generator')}:{seed_report.get('generator_status')} missing_keys={len(missing)}"
    )
    safe_print(f"CONCEPT_DELTA: {rel(concept_md_path)} concepts={concept_delta.get('concept_count', 0)}")
    safe_print(f"MECHANISM_GRAPHS: {rel(MECHANISM_GRAPH_DIR / args.run_date)} count={len(mechanism_graph_paths)}")
    if seed_report.get("no_high_quality_seed_today_reason"):
        safe_print(f"NO_HIGH_QUALITY_SEED_TODAY: {seed_report['no_high_quality_seed_today_reason']}")
    exit_code = 2 if str(seed_report.get("generator_status", "")).startswith("failed:") else 0
    if args.dry_run:
        return exit_code

    write_jsonl(EVIDENCE_MATRIX, merged, dry_run=False)
    write_paper_cards(new_records, dry_run=False)
    for filename in POOL_FILES:
        safe_write(PROBLEM_POOL_DIR / filename, render_pool_file(filename, merged), dry_run=False, backup=True)
    safe_write(AGENDA_ROOT / "README.md", render_readme(), dry_run=False, backup=True)
    safe_write(AGENDA_ROOT / "agenda-dashboard.md", render_dashboard(merged, len(seeds), seed_report), dry_run=False, backup=True)
    battle_result: dict[str, Any] = {
        "status": "moved_to_v2_state_machine",
        "boundary": "DeepSeek/Codex promotion review is handled by v2 run artifacts, not research_agenda_update.py.",
    }
    delta_path = DAILY_DIR / f"{args.run_date}-agenda-delta.md"
    safe_write(
        delta_path,
        render_daily_delta(
            run_date=args.run_date,
            focus_keys=focus_keys,
            new_records=focus_records or all_records,
            merged_records=merged,
            seeds=seeds,
            seed_report=seed_report,
            missing=missing,
            rebuild_all=rebuild_all,
            concept_delta_path=concept_md_path,
            concept_delta=concept_delta,
            mechanism_graph_paths=mechanism_graph_paths,
            sidecar_warnings=sidecar_warnings,
            battle_result=battle_result,
        ),
        dry_run=False,
        backup=True,
    )
    pending_path = REVIEWS_DIR / f"{args.run_date}-codex-review-pending.json"
    safe_write(
        pending_path,
        json.dumps(
            {
                "run_date": args.run_date,
                "status": "pending",
                "agenda_delta": rel(delta_path),
                "concept_delta": rel(concept_md_path),
                "mechanism_graph_dir": rel(MECHANISM_GRAPH_DIR / args.run_date),
                "mechanism_graphs_created": len(mechanism_graph_paths),
                "sidecar_warnings": sidecar_warnings,
                "raw_gemini_candidates": len(seed_report.get("greenhouse", [])),
                "high_quality_seed_candidates": len(seeds),
                "mandatory_model_battle_status": battle_result.get("status", "not_run"),
                "mandatory_model_battle_report": battle_result.get("review_path", ""),
                "mandatory_model_battle_packet": battle_result.get("packet_path", ""),
                "free_divergence": seed_report.get("free_divergence", False),
                "candidate_group_counts": dict(_group_counts(seed_report)),
                "portfolio_summary": _portfolio_summary(seed_report),
                "created_by": "research_agenda_update.py",
                "boundary": "Evidence/agenda update only; raw candidates and seed publication are handled by v2 state-machine scripts.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        dry_run=False,
        backup=True,
    )
    safe_print(f"AGENDA_DELTA: {rel(delta_path)}")
    safe_print(f"MANDATORY_MODEL_BATTLE: {battle_result.get('status', 'not_run')} report={battle_result.get('review_path', '-')}")
    safe_print(f"CODEX_REVIEW_PENDING: {rel(pending_path)}")
    safe_print(f"EVIDENCE_MATRIX: {rel(EVIDENCE_MATRIX)}")
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Rebuild from all done literature notes.")
    parser.add_argument("--zotero-keys", default="", help="Comma-separated newly read Zotero keys.")
    parser.add_argument("--run-date", default=__import__("datetime").date.today().isoformat())
    parser.add_argument("--seed-limit", type=int, default=3, help="Deprecated alias for --max-generated.")
    parser.add_argument("--max-generated", type=int, default=None, help="Maximum high-quality idea seeds to write. Defaults to --seed-limit.")
    parser.add_argument("--raw-candidate-limit", type=int, default=8, help="Maximum raw Gemini greenhouse candidates to preserve.")
    parser.add_argument("--min-raw-candidates", type=int, default=6, help="Minimum raw Gemini candidates before one divergent retry is attempted.")
    parser.add_argument("--idea-mode", choices=["mechanism", "curated"], default="mechanism")
    parser.add_argument("--idea-generator", choices=["template", "claude", "gemini-cli", "gemini-divergent", "none"], default="none")
    parser.add_argument("--idea-timeout", type=int, default=1200)
    parser.add_argument("--gemini-model", default="gemini-3.1-pro-preview")
    parser.add_argument("--deepseek-model", default="abrdns/deepseek-v4-pro")
    parser.add_argument("--deepseek-timeout", type=int, default=1200)
    parser.add_argument("--include-dynamic-ideas", dest="include_dynamic", action="store_true", help="Deprecated; only applies to curated mode.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.max_generated is None:
        args.max_generated = args.seed_limit
    return run_update(args)


if __name__ == "__main__":
    raise SystemExit(main())

