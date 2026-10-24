"""Generate evidence-linked daily research ideas from arXiv scout candidates."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from arxiv_ranker import FOCUS_REVIEW_DECISION, RankedPaper
from kb_common import extract_frontmatter, parse_frontmatter_map, parse_list_value, safe_print, safe_write, today_iso, vault_path
from kb_search import search


IDEA_THEMES = [
    {
        "title": "Tactile-conditioned DLO policy",
        "query": "tactile diffusion bimanual DLO",
        "problem": "DLO state is hard to observe from vision alone when contact and self-occlusion dominate.",
        "hypothesis": "Adding tactile contact summaries to a diffusion-style action policy can reduce topology errors in bimanual DLO manipulation.",
        "experiment": "Run the same DLO routing or handover tasks while switching only the sensing channel and policy conditioning.",
        "variables": "independent: vision-only vs tactile-only vs vision+tactile conditioning; dependent: topology error, contact loss, task success; controls: DLO material, initial topology, camera pose, demonstration budget.",
        "baselines": "vision-only Diffusion Policy, tactile-only diagnostic classifier, and a rule-triggered replanning baseline.",
        "metrics": "task success, topology violation count, recovery attempts, contact-loss events, and rollout-level failure category.",
        "current_practice": "Most related work treats tactile input as policy conditioning or evaluates DLO control with vision/planning; the gap is topology-aware tactile feedback for bimanual DLO policies.",
        "similar_work": "Check tactile-diffusion policies, DLO routing with Diffusion Policy, and topological rope planning before claiming novelty.",
        "implementation": "Start with an offline dataset that logs camera frames, tactile contact summaries, end-effector poses, and topology labels; train a vision-only policy first, then add tactile tokens and compare controlled ablations.",
    },
    {
        "title": "VLA planner with local geometric constraints",
        "query": "VLA planning bimanual manipulation",
        "problem": "VLA policies can propose plausible high-level actions while missing geometric or topology constraints.",
        "hypothesis": "A small explicit planner between VLA intent and low-level control can improve constraint satisfaction without discarding language priors.",
        "experiment": "Translate VLA intent into local geometric or topological constraints before action generation, then compare against direct VLA action prediction.",
        "variables": "independent: direct VLA action, VLA plus geometric constraint layer, VLA plus topology-aware planner; dependent: constraint violations, completion, replanning count; controls: instruction set, scene geometry, policy checkpoint.",
        "baselines": "direct VLA action prediction, language-conditioned Diffusion Policy, and classical task-and-motion planning without VLA priors.",
        "metrics": "constraint satisfaction rate, task completion, intervention count, planning latency, and failure-mode distribution.",
        "current_practice": "Current VLA systems usually rely on learned action heads or post-hoc correction, while classical planners enforce geometry but lack language-conditioned priors.",
        "similar_work": "Compare against VLA correction methods, bimanual benchmark policies, and topology-aware rope/cable planners.",
        "implementation": "Represent the VLA output as a task intent, compile it into local distance/contact/topology constraints, then let a low-level diffusion or MPC controller execute only constraint-compatible actions.",
    },
    {
        "title": "Sim-to-Real benchmark for contact-rich manipulation",
        "query": "sim-to-real benchmark tactile manipulation",
        "problem": "Many Sim-to-Real claims are hard to compare because task setup, sensing, and failure categories vary.",
        "hypothesis": "A compact benchmark with fixed DLO geometry, tactile sensor placement, and transfer perturbations can expose which methods generalize.",
        "experiment": "Build a pilot benchmark that varies one transfer factor at a time while keeping metrics and hardware assumptions fixed.",
        "variables": "independent: stiffness, friction, lighting, tactile noise, and initial topology perturbation; dependent: transfer drop, failure category, recovery success; controls: robot, controller frequency, task script, evaluation protocol.",
        "baselines": "simulation-only policy, domain-randomized policy, real-finetuned policy, and tactile-augmented policy.",
        "metrics": "sim-to-real transfer gap, success, constraint violation, contact stability, and per-factor robustness curve.",
        "current_practice": "Many papers report transfer on their own task setup, which makes cross-paper comparison hard when sensors, materials, and failure definitions differ.",
        "similar_work": "Check RoboTwin-style bimanual benchmarks, tactile manipulation benchmarks, and DLO routing or deformable object transfer papers.",
        "implementation": "Define a small task suite with fixed hardware assumptions, one perturbation axis per evaluation block, and a shared failure taxonomy before testing new policies.",
    },
    {
        "title": "Failure-aware bimanual recovery policy",
        "query": "bimanual DLO planning recovery",
        "problem": "Bimanual manipulation failures often accumulate before the policy reaches a terminal failure state.",
        "hypothesis": "A recovery classifier trained on local failure modes can trigger replanning earlier than a monolithic policy.",
        "experiment": "Annotate early warning states from pilot rollouts and compare always-policy execution against classifier-triggered replanning.",
        "variables": "independent: no recovery, threshold recovery, classifier-triggered recovery, planner-triggered recovery; dependent: avoided terminal failures, false recovery triggers, task completion; controls: task suite, policy checkpoint, rollout budget.",
        "baselines": "monolithic policy without recovery, fixed-threshold contact alarm, and periodic replanning.",
        "metrics": "early warning precision/recall, terminal failure rate, recovery success, extra time cost, and human intervention count.",
        "current_practice": "Most pipelines evaluate terminal success, while recovery is handled by fixed thresholds, periodic replanning, or manual intervention.",
        "similar_work": "Check predictive correction methods, Diff-DAgger uncertainty triggers, topological rope planning, and bimanual coordination failure analyses.",
        "implementation": "Collect failed and near-failed rollouts, label early warning windows, train a lightweight failure predictor, and trigger either local recovery or topology-aware replanning.",
    },
    {
        "title": "Data-efficient imitation for deformable manipulation",
        "query": "imitation learning deformable object manipulation",
        "problem": "Collecting demonstrations for deformable manipulation is expensive and task-specific.",
        "hypothesis": "Segmenting demonstrations into reusable contact primitives can improve data efficiency for new DLO layouts.",
        "experiment": "Compare whole-trajectory cloning with primitive-conditioned cloning under the same small demonstration budget.",
        "variables": "independent: whole-trajectory cloning, primitive-conditioned cloning, primitive-conditioned diffusion; dependent: few-shot success, generalization to new layouts, recovery after contact slip; controls: demonstrations, perception backbone, training budget.",
        "baselines": "behavioral cloning, Diffusion Policy, and nearest-neighbor primitive retrieval.",
        "metrics": "few-shot success, layout generalization, contact primitive reuse rate, and failure category under unseen DLO shapes.",
        "current_practice": "Common imitation systems scale demonstrations or improve policy architectures; fewer works explicitly reuse contact primitives across deformable layouts.",
        "similar_work": "Check one-shot bimanual demonstration synthesis, movement primitive diffusion, GenDOM, and imperfect-demonstration filtering.",
        "implementation": "Segment demonstrations into contact primitives, learn a primitive-conditioned policy, and test whether the same primitive library transfers to new DLO geometries with fewer demonstrations.",
    },
]
STOP_TOKENS = {
    "and",
    "the",
    "with",
    "for",
    "from",
    "policy",
    "policies",
    "manipulation",
    "robot",
    "robotic",
    "learning",
}

DECISION_BONUS = {
    "top1_candidate": 4,
    "venue_auto_import": 4,
    FOCUS_REVIEW_DECISION: 3,
    "review_queue": 2,
}


@dataclass
class EvidenceItem:
    label: str
    link: str
    detail: str


def load_ranked_jsonl(path: Path) -> list[RankedPaper]:
    items: list[RankedPaper] = []
    if not path.exists():
        return items
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        items.append(RankedPaper.from_dict(json.loads(line)))
    return items


def _ns(query: str, limit: int = 4, *, status: str | None = None) -> argparse.Namespace:
    return argparse.Namespace(
        query=query,
        tag=[],
        must_tag=[],
        type=None,
        status=status,
        year_from=None,
        year_to=None,
        limit=limit,
        json=False,
    )


def _looks_mojibake(text: str) -> bool:
    markers = ["锛", "鎻", "涓", "鈥", "�", "€", "竴", "鍦", "绛"]
    return any(marker in text for marker in markers)


def _local_detail(result: Any) -> str:
    raw = result.summary or "; ".join(result.snippets[:1])
    return _clean_local_detail(raw, result.tags, result.year, result.path)


def _clean_local_detail(raw: str, tags: list[str], year: str, path: Path) -> str:
    raw = " ".join(raw.split())
    if raw and not _looks_mojibake(raw):
        return raw[:260]
    tag_text = ", ".join(tags[:5]) if tags else "-"
    year_text = year or "unknown-year"
    return f"local_done_evidence; year={year_text}; tags={tag_text}; path={path.as_posix()}"


def local_evidence(query: str, limit: int = 4, *, status: str | None = None) -> list[EvidenceItem]:
    evidence = []
    for result in search(_ns(query, limit, status=status)):
        title = result.title or result.path.stem
        detail = _local_detail(result)
        evidence.append(EvidenceItem(label=title, link=f"[[{result.path.stem}|{title}]]", detail=detail))
    return evidence


def _strip_quotes(value: str) -> str:
    return value.strip().strip('"')


def local_evidence_for_zotero_keys(keys: list[str], limit: int = 10) -> list[EvidenceItem]:
    order = {key.strip().upper(): index for index, key in enumerate(keys) if key.strip()}
    if not order:
        return []
    evidence: list[tuple[int, EvidenceItem]] = []
    for path in sorted(vault_path("wiki", "topics").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(text)
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        key = _strip_quotes(fields.get("zotero_key", "")).upper()
        if key not in order:
            continue
        if _strip_quotes(fields.get("status", "")) != "done":
            continue
        title = _strip_quotes(fields.get("title", "")) or path.stem
        tags = parse_list_value(fields.get("tags", ""))
        year = _strip_quotes(fields.get("year", ""))
        summary = _strip_quotes(fields.get("summary", ""))
        detail = _clean_local_detail(summary, tags, year, path)
        evidence.append((order[key], EvidenceItem(label=title, link=f"[[{path.stem}|{title}]]", detail=detail)))
    return [item for _, item in sorted(evidence, key=lambda item: item[0])[:limit]]


def focus_candidates(candidates: list[RankedPaper], arxiv_ids: list[str]) -> list[RankedPaper]:
    order = {arxiv_id.strip().lower(): index for index, arxiv_id in enumerate(arxiv_ids) if arxiv_id.strip()}
    if not order:
        return []
    focused = [item for item in candidates if item.paper.arxiv_id.lower() in order]
    return sorted(focused, key=lambda item: order[item.paper.arxiv_id.lower()])


def _merge_evidence(primary: list[EvidenceItem], secondary: list[EvidenceItem], limit: int) -> list[EvidenceItem]:
    merged: list[EvidenceItem] = []
    seen: set[str] = set()
    for item in [*primary, *secondary]:
        if item.link in seen:
            continue
        merged.append(item)
        seen.add(item.link)
        if len(merged) >= limit:
            break
    return merged


def _rank_local_for_theme(items: list[EvidenceItem], theme: dict[str, str], limit: int) -> list[EvidenceItem]:
    tokens = _tokens(theme["query"])
    scored: list[tuple[int, int, EvidenceItem]] = []
    for index, item in enumerate(items):
        haystack = f"{item.label} {item.detail}".lower()
        score = sum(1 for token in tokens if token in haystack)
        scored.append((score, -index, item))
    ranked = [item for score, _, item in sorted(scored, key=lambda value: (-value[0], value[1])) if score > 0]
    if len(ranked) < limit:
        seen = {item.link for item in ranked}
        for item in items:
            if item.link not in seen:
                ranked.append(item)
                seen.add(item.link)
            if len(ranked) >= limit:
                break
    return ranked[:limit]


def _tokens(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9-]+", text.lower()) if len(token) > 2 and token not in STOP_TOKENS]


def _abstract_signal(summary: str, tokens: list[str]) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(summary.split()))
    for sentence in sentences:
        if any(token in sentence.lower() for token in tokens):
            return sentence[:260]
    return (sentences[0] if sentences else "")[:260]


def theme_candidates(candidates: list[RankedPaper], theme: dict[str, str], limit: int = 2) -> list[RankedPaper]:
    query_tokens = _tokens(theme["query"])
    scored: list[tuple[int, RankedPaper]] = []
    for ranked in candidates:
        text = f"{ranked.paper.title} {ranked.paper.summary}".lower()
        matches = {token for token in query_tokens if token in text}
        if not matches:
            continue
        decision_bonus = DECISION_BONUS.get(ranked.decision, 0)
        scored.append((len(matches) * 10 + ranked.quality_score + decision_bonus, ranked))
    return [ranked for _, ranked in sorted(scored, key=lambda item: (-item[0], -item[1].quality_score))[:limit]]


def candidate_evidence(candidates: list[RankedPaper], limit: int = 4, *, theme: dict[str, str] | None = None) -> list[EvidenceItem]:
    evidence = []
    tokens = _tokens(theme["query"]) if theme else []
    for ranked in candidates[:limit]:
        paper = ranked.paper
        link = f"[{paper.title}]({paper.url or paper.pdf_url})"
        detail = f"arXiv:{paper.arxiv_id}; score={ranked.quality_score}; decision={ranked.decision}"
        if tokens:
            signal = _abstract_signal(paper.summary, tokens)
            if signal:
                detail = f"{detail}; abstract_signal: {signal}"
        evidence.append(EvidenceItem(label=paper.title, link=link, detail=detail))
    return evidence


def evidence_level(evidence: list[EvidenceItem]) -> str:
    local_count = sum(1 for item in evidence if item.link.startswith("[["))
    external_count = sum(1 for item in evidence if "arxiv.org" in item.link)
    if local_count >= 3 and external_count >= 2:
        return "strong"
    if local_count >= 2 and external_count >= 1:
        return "partial"
    if local_count + external_count >= 2:
        return "weak"
    return "weak"


def _format_evidence(items: list[EvidenceItem]) -> list[str]:
    if not items:
        return ["  - evidence_gap: no local or daily candidate evidence found"]
    return [f"  - {item.link}: {item.detail}" for item in items]


def _ensure_daily_cluster(candidates: list[RankedPaper], theme: dict[str, str], sorted_candidates: list[RankedPaper]) -> list[EvidenceItem]:
    themed = candidate_evidence(theme_candidates(candidates, theme, 3), 3, theme=theme)
    if len(themed) >= 2:
        return themed
    seen = {item.link for item in themed}
    for item in [*candidate_evidence(candidates, 5), *candidate_evidence(sorted_candidates, 5)]:
        if item.link not in seen:
            themed.append(item)
            seen.add(item.link)
        if len(themed) >= 2:
            break
    return themed


def _ensure_local_done_cluster(theme: dict[str, str], preferred: list[EvidenceItem] | None = None) -> list[EvidenceItem]:
    local = _rank_local_for_theme(preferred or [], theme, 3)
    local = _merge_evidence(local, local_evidence(theme["query"], 5, status="done"), 5)
    if len(local) >= 3:
        return local[:5]
    seen = {item.link for item in local}
    for item in local_evidence("DLO tactile diffusion bimanual sim-to-real planning manipulation", 8, status="done"):
        if item.link not in seen:
            local.append(item)
            seen.add(item.link)
        if len(local) >= 3:
            break
    return local[:5]


def _cluster_pattern(theme: dict[str, str], daily: list[EvidenceItem], local: list[EvidenceItem]) -> str:
    daily_names = "; ".join(item.label for item in daily[:3]) or "today's candidates"
    local_names = "; ".join(item.label for item in local[:3]) or "local done papers"
    return (
        f"Daily papers point to {theme['query']} as an active frontier ({daily_names}), "
        f"while the local KB shows related constraints and baselines from {local_names}."
    )


def render_ideas(
    candidates: list[RankedPaper],
    *,
    run_date: str | None = None,
    focus_arxiv_ids: list[str] | None = None,
    focus_zotero_keys: list[str] | None = None,
) -> str:
    run_date = run_date or today_iso()
    sorted_candidates = sorted(candidates, key=lambda item: -item.quality_score)
    focused_candidates = focus_candidates(sorted_candidates, focus_arxiv_ids or [])
    daily_pool = focused_candidates or sorted_candidates
    daily_evidence = candidate_evidence(daily_pool, min(10, len(daily_pool)))
    today_local = local_evidence_for_zotero_keys(focus_zotero_keys or [], 10)
    all_local = _merge_evidence(
        today_local,
        local_evidence("embodied AI robot learning manipulation DLO tactile sim-to-real", 8, status="done"),
        10,
    )
    global_level = evidence_level(daily_evidence + all_local)

    lines = [
        "---",
        f'title: "Daily Embodied AI Ideas - {run_date}"',
        "tags: [idea, arxiv, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        f'summary: "Daily evidence-cluster embodied AI research ideas generated from arXiv scout candidates and done local readings."',
        f'evidence_level: "{global_level}"',
        "---",
        "",
        f"# Daily Embodied AI Ideas - {run_date}",
        "",
        "## Evidence Sources",
        "",
    ]
    if daily_evidence:
        title = "### Daily Deep-Read arXiv Set" if focused_candidates else "### Daily arXiv Candidates"
        lines.append(title)
        lines.extend(_format_evidence(daily_evidence))
        lines.append("")
    if today_local:
        lines.append("### Today's Deep-Read Local Notes (status: done)")
        lines.extend(_format_evidence(today_local))
        lines.append("")
    if all_local:
        lines.append("### Local Vault Evidence (status: done)")
        lines.extend(_format_evidence(all_local))
        lines.append("")

    for index, theme in enumerate(IDEA_THEMES, 1):
        theme_daily = _ensure_daily_cluster(daily_pool, theme, sorted_candidates)
        theme_local = _ensure_local_done_cluster(theme, today_local)
        evidence = theme_daily + theme_local
        level = evidence_level(evidence)
        pattern = _cluster_pattern(theme, theme_daily, theme_local)
        lines.extend(
            [
                f"## Idea {index}: {theme['title']}",
                "",
                f"- Problem: {theme['problem']}",
                f"- Hypothesis: {theme['hypothesis']}",
                "- Decision Status: candidate_pending_human_selection",
                f"- Cross-paper Pattern: {pattern}",
                f"- Knowledge Base Support: This idea is grounded in {len(theme_local)} done local readings and should be treated as weak if fewer than 3 local links appear below.",
                f"- Novelty Hypothesis: The potential novelty is the combination of the daily-paper trend with the local KB gap, not any single paper's claim.",
                f"- Why Now: Today's arXiv cluster suggests the enabling tools are becoming available, while the local KB keeps the idea tied to DLO/tactile/bimanual/Sim-to-Real constraints.",
                f"- Current Practice: {theme['current_practice']}",
                f"- Similar Work: {theme['similar_work']}",
                f"- Implementation Plan: {theme['implementation']}",
                f"- Pilot Experiment: {theme['experiment']}",
                f"- Variables: {theme['variables']}",
                f"- Baselines: {theme['baselines']}",
                f"- Metrics: {theme['metrics']}",
                f"- Evidence Level: {level}",
                "- Evidence Cluster:",
                "  - Daily Papers:",
                *_format_evidence(theme_daily),
                "  - Local Done Papers:",
                *_format_evidence(theme_local),
                "- Risk: The evidence is a hypothesis scaffold, not proof that the idea will work.",
                "- Next Step: Turn this into a `/plan-experiment` draft before any hardware or data-collection decision.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True, help="Ranked candidate JSONL file.")
    parser.add_argument("--output", type=Path, help="Output path relative to the vault root.")
    parser.add_argument("--focus-arxiv-ids", default="", help="Comma-separated arXiv IDs for today's deep-read imports.")
    parser.add_argument("--focus-zotero-keys", default="", help="Comma-separated Zotero keys for today's deep-read imports.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    candidates = load_ranked_jsonl(args.candidates)
    out_path = args.output or Path("projects") / "ideas" / f"{today_iso()}-embodied-ai-ideas.md"
    if not out_path.is_absolute():
        out_path = vault_path(*out_path.parts)
    focus_arxiv_ids = [item.strip() for item in args.focus_arxiv_ids.split(",") if item.strip()]
    focus_zotero_keys = [item.strip() for item in args.focus_zotero_keys.split(",") if item.strip()]
    content = render_ideas(candidates, focus_arxiv_ids=focus_arxiv_ids, focus_zotero_keys=focus_zotero_keys)
    safe_write(out_path, content, dry_run=args.dry_run, backup=True)
    safe_print(f"IDEAS_PATH: {out_path.relative_to(vault_path())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
