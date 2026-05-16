"""Generate an evidence-grounded experiment plan from local vault notes."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from kb_common import safe_print, safe_write, today_iso, vault_path
from kb_search import SearchResult, search


TAG_PRIORITY = ["DLO", "tactile", "diffusion", "bimanual", "planning", "sim-to-real", "VLM", "RL"]
SLUG_MAP = {
    "DLO": "dlo",
    "tactile": "tactile",
    "diffusion": "diffusion",
    "bimanual": "bimanual",
    "planning": "planning",
    "sim-to-real": "sim-to-real",
    "VLM": "vlm",
    "RL": "rl",
}
COVERAGE_QUERIES = [
    "DLO deformable linear object rope cable manipulation",
    "tactile force haptic contact-rich manipulation",
    "diffusion policy visuomotor action diffusion",
    "bimanual dual-arm coordination planning",
    "benchmark baseline ablation metrics robot manipulation",
    "sim-to-real domain randomization real-to-sim deformable object",
]
BENCHMARK_TERMS = ("benchmark", "challenge", "基准", "挑战赛")
SIM_TERMS = ("sim-to-real", "sim2real", "real-to-sim", "仿真到真实", "仿真迁移")
TACTILE_TERMS = ("tactile", "touch", "force", "haptic", "触觉", "力")
DIFFUSION_TERMS = ("diffusion", "扩散")
QUERY_STOP_PHRASES = (
    "实验规划",
    "实验方案",
    "设计实验",
    "怎么验证",
    "怎么做实验",
    "研究问题",
    "研究方向",
    "机器人",
    "规划",
    "实验",
    "方案",
    "方向",
    "研究",
    "验证",
    "怎么",
    "如何",
    "的",
)


@dataclass
class EvidenceSet:
    items: list[SearchResult]
    coverage: set[str]
    gaps: list[str]


def ns(query: str, limit: int, *, must_tag: str | None = None) -> argparse.Namespace:
    must_tags = [must_tag] if must_tag else []
    return argparse.Namespace(
        query=query,
        tag=[],
        must_tag=must_tags,
        type=None,
        status="done",
        year_from=None,
        year_to=None,
        limit=limit,
    )


def collect_evidence(query: str, limit: int) -> EvidenceSet:
    by_path: dict[Path, SearchResult] = {}
    for result in search(ns(query, limit)):
        by_path.setdefault(result.path, result)
    for extra in COVERAGE_QUERIES:
        for result in search(ns(f"{query} {extra}", 6)):
            by_path.setdefault(result.path, result)
    for tag in TAG_PRIORITY:
        for result in search(ns(query, 4, must_tag=tag)):
            by_path.setdefault(result.path, result)

    items = sorted(by_path.values(), key=lambda item: (-item.score, item.year, item.title))[:limit]
    coverage = infer_coverage(items)
    gaps = coverage_gaps(query, coverage, items)
    return EvidenceSet(items=items, coverage=coverage, gaps=gaps)


def infer_coverage(items: list[SearchResult]) -> set[str]:
    coverage: set[str] = set()
    for item in items:
        tags = set(item.tags)
        text = item_text(item)
        for tag in TAG_PRIORITY:
            if tag in tags:
                coverage.add(tag)
        if has_any(text, BENCHMARK_TERMS):
            coverage.add("benchmark")
        if "sim-to-real" in tags or has_any(text, SIM_TERMS):
            coverage.add("sim-to-real")
    return coverage


def coverage_gaps(query: str, coverage: set[str], items: list[SearchResult]) -> list[str]:
    required_groups = {"benchmark_or_sim_to_real": ["benchmark", "sim-to-real"]}
    if query_mentions(query, ("DLO", "deformable", "rope", "cable", "可变形", "绳", "线缆")):
        required_groups["DLO"] = ["DLO"]
    if query_mentions(query, TACTILE_TERMS):
        required_groups["tactile"] = ["tactile"]
    if query_mentions(query, DIFFUSION_TERMS):
        required_groups["diffusion"] = ["diffusion"]
    if query_mentions(query, ("bimanual", "dual-arm", "双臂", "双手", "任务规划", "路径规划")):
        required_groups["bimanual_or_planning"] = ["bimanual", "planning"]

    gaps = []
    for name, options in required_groups.items():
        if not any(option in coverage for option in options):
            gaps.append(name)
    if len(items) < 8:
        gaps.append("min_8_local_evidence")
    gaps.extend(query_specific_gaps(query, items))
    return gaps


def query_mentions(query: str, terms: tuple[str, ...]) -> bool:
    q = query.lower()
    return any(term.lower() in q for term in terms)


def salient_query_terms(query: str) -> list[str]:
    terms = re.findall(r"[A-Za-z0-9_\-]+|[\u4e00-\u9fff]{2,}", query.lower())
    cleaned: list[str] = []
    for term in terms:
        value = term
        for stop in QUERY_STOP_PHRASES:
            value = value.replace(stop.lower(), "")
        if len(value) >= 2:
            cleaned.append(value)
    return list(dict.fromkeys(cleaned))


def query_specific_gaps(query: str, items: list[SearchResult]) -> list[str]:
    terms = salient_query_terms(query)
    if not terms:
        return []
    haystack = "\n".join(item_text(item) for item in items)
    matched = [term for term in terms if term in haystack]
    if matched:
        return []
    return ["query_specific_local_evidence"]


def evidence_level(evidence: EvidenceSet) -> str:
    if "query_specific_local_evidence" in evidence.gaps:
        return "weak"
    if len(evidence.items) >= 8 and not evidence.gaps:
        return "strong"
    if len(evidence.items) >= 5:
        return "partial"
    return "weak"


def slug_from_query(query: str, evidence: EvidenceSet) -> str:
    q = query.lower()
    selected: list[str] = []
    checks = [
        ("DLO", ["dlo", "deformable", "rope", "cable", "可变形", "绳", "线缆"]),
        ("tactile", ["tactile", "touch", "force", "haptic", "触觉", "力"]),
        ("diffusion", ["diffusion", "扩散"]),
        ("bimanual", ["bimanual", "dual-arm", "双臂"]),
        ("planning", ["planning", "plan", "规划"]),
        ("sim-to-real", ["sim-to-real", "sim2real", "仿真"]),
    ]
    for tag, needles in checks:
        if any(needle in q for needle in needles) or tag in evidence.coverage:
            selected.append(SLUG_MAP[tag])
        if len(selected) == 3:
            break
    if selected:
        return "-".join(dict.fromkeys(selected))
    ascii_terms = re.findall(r"[a-z0-9]+", q)
    return "-".join(ascii_terms[:3]) or "experiment-plan"


def rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def wikilink(item: SearchResult) -> str:
    return f"[[{item.path.stem}]]"


def item_text(item: SearchResult) -> str:
    return " ".join([item.title, item.summary, " ".join(item.snippets)]).lower()


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term.lower() in text for term in terms)


def first_with(items: list[SearchResult], *tags: str, terms: tuple[str, ...] = ()) -> SearchResult | None:
    wanted = set(tags)
    for item in items:
        if wanted.intersection(item.tags):
            return item
    if terms:
        for item in items:
            if has_any(item_text(item), terms):
                return item
    return None


def render_plan(query: str, evidence: EvidenceSet) -> str:
    today = today_iso()
    level = evidence_level(evidence)
    title = f"实验规划: {query}"
    summary = "基于本地 vault 证据生成的半自动实验规划草案，需人工批准后才能进入 pilot。"
    dlo = first_with(evidence.items, "DLO")
    tactile = first_with(evidence.items, "tactile", terms=TACTILE_TERMS)
    diffusion = first_with(evidence.items, "diffusion", terms=DIFFUSION_TERMS)
    bimanual = first_with(evidence.items, "bimanual")
    planning = first_with(evidence.items, "planning")
    sim = first_with(evidence.items, "sim-to-real", terms=SIM_TERMS)
    benchmark = first_with(evidence.items, terms=BENCHMARK_TERMS)

    def cite(item: SearchResult | None, fallback: str) -> str:
        return wikilink(item) if item else f"evidence_gap:{fallback}"

    lines = [
        "---",
        f'title: "{title}"',
        "tags: [project, experiment, planning]",
        f'created: "{today}"',
        f'updated: "{today}"',
        'type: "permanent"',
        'status: "active"',
        f'summary: "{summary}"',
        'stage: "draft"',
        'decision_status: "recommended_pending_approval"',
        f'evidence_level: "{level}"',
        "---",
        "",
        "## Research Question",
        "",
        query,
        "",
        "## Hypothesis",
        "",
        f"- 主假设：在 {cite(dlo, 'DLO')} 的任务设定上，引入 {cite(tactile, 'tactile')} 风格的接触/力信息，并采用 {cite(diffusion, 'diffusion')} 风格的动作生成，可以提升 DLO 接触丰富任务的鲁棒性。",
        "- 边界：该假设只是一条待验证研究假设，不是已确认结论；进入 pilot 前必须由人工确认平台、传感器和安全边界。",
        "",
        "## Evidence Base",
        "",
    ]
    for index, item in enumerate(evidence.items, 1):
        snippets = "；".join(item.snippets[:1]) if item.snippets else item.summary
        lines.append(
            f"- E{index}: {wikilink(item)} — path: `{rel(item.path)}`; tags: {', '.join(item.tags)}; why: {item.summary}; evidence: {snippets}"
        )
    if evidence.gaps:
        lines.append("- evidence_gap: " + ", ".join(evidence.gaps))
    else:
        lines.append("- evidence_gap: none")

    recommendation = "B" if level == "strong" else "no_strong_recommendation"
    lines.extend(
        [
            "",
            "## Candidate Designs",
            "",
            f"- Design A - planning-first baseline: use {cite(planning, 'planning')} as the transparent constrained baseline for DLO routing or threading.",
            f"- Design B - tactile diffusion policy: combine {cite(tactile, 'tactile')} and {cite(diffusion, 'diffusion')} with the DLO task family in {cite(dlo, 'DLO')}.",
            f"- Design C - sim-to-real conservative path: start from {cite(benchmark or sim, 'benchmark_or_sim_to_real')} and use a smaller pilot to quantify domain gap before full policy training.",
            "",
            "## Recommended Design",
            "",
            "decision_status: recommended_pending_approval",
            f"- recommendation: {recommendation}",
            "- rationale: Design B is preferred only when evidence_level is strong; otherwise the required output is evidence_gap plus a reading/import task.",
            "- human gate: the recommendation must be approved by the user before hardware trials or data collection.",
            "",
            "## Protocol",
            "",
            "- Define one DLO contact-rich task family and one success criterion before collecting data.",
            "- Run the planning-first or existing DLO method as the baseline before testing tactile diffusion.",
            "- Keep all robot, camera, tactile, controller, and DLO material settings fixed during the first pilot.",
            "- Record failures as first-class data: slip, occlusion, overstretch, collision risk, and recovery behavior.",
            "",
            "## Baselines",
            "",
            f"- Local DLO baseline: {cite(dlo, 'DLO')}.",
            f"- Planning/control baseline: {cite(planning, 'planning')}.",
            f"- Diffusion policy baseline: {cite(diffusion, 'diffusion')}.",
            f"- Benchmark or Sim-to-Real reference: {cite(benchmark or sim, 'benchmark_or_sim_to_real')}.",
            "",
            "## Metrics",
            "",
            "- Task success/failure with explicit failure labels.",
            "- Completion time and intervention count.",
            "- DLO shape/path error, overstretch events, and contact stability.",
            "- Sim-to-Real gap if both simulation and physical trials are used.",
            "- Data efficiency measured against the same task and platform.",
            "",
            "## Ablations",
            "",
            "- Remove tactile/force input while keeping the same policy class.",
            "- Replace diffusion action generation with the strongest local baseline available.",
            "- Remove planning or topology constraints where the task requires routing/threading.",
            "- Change DLO material or scene layout only after the fixed-setting pilot passes.",
            "",
            "## Hardware/Data Assumptions",
            "",
            "- TO_CONFIRM: robot platform, gripper/end-effector, tactile sensor availability, camera setup, DLO materials, safety stop policy.",
            "- TO_CONFIRM: demonstration source, annotation format, simulation availability, and data storage convention.",
            "",
            "## Generalization Plan",
            "",
            "- In-distribution: repeat the same task under controlled initial pose changes.",
            "- Object/material: change DLO length, stiffness, friction, or thickness after the pilot.",
            "- Perception: vary camera viewpoint or occlusion only after fixed-view results are stable.",
            "- Task: transfer from one routing/threading/contact task to a related DLO task and report failure modes.",
            "",
            "## Pilot Experiment",
            "",
            "- Goal: test feasibility, logging quality, and failure taxonomy before making performance claims.",
            "- Stop condition: abort if safety, sensing, or data quality assumptions fail.",
            "- Output: pilot report with raw logs, videos, failure labels, and a decision to approve, revise, or reject the full experiment.",
            "",
            "## Risks & Fallback",
            "",
            "- Risk: tactile signal is noisy or hard to align with vision. Fallback: use tactile only for event/failure labels first.",
            "- Risk: diffusion inference is too slow for contact control. Fallback: use receding-horizon low-rate policy plus low-level impedance/control loop.",
            "- Risk: DLO state is under-observed. Fallback: add explicit planning/topology representation before policy learning.",
            "- Risk: evidence is partial. Fallback: import and精读 missing papers before approving pilot.",
            "",
            "## Human Approval Checklist",
            "",
            "- [ ] Research question and hypothesis are approved.",
            "- [ ] Robot, sensors, DLO materials, and safety boundary are approved.",
            "- [ ] Baselines, metrics, ablations, and pilot scope are approved.",
            "- [ ] Evidence gaps are resolved or explicitly accepted.",
            "- [ ] decision_status is changed from recommended_pending_approval only after human approval.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Research question or experiment direction.")
    parser.add_argument("--limit", type=int, default=12, help="Maximum local evidence items to include.")
    parser.add_argument("--output", help="Optional output path relative to the vault root.")
    parser.add_argument("--dry-run", action="store_true", help="Print the draft without writing it.")
    args = parser.parse_args()

    evidence = collect_evidence(args.query, args.limit)
    content = render_plan(args.query, evidence)
    if args.output:
        out_path = vault_path(args.output)
    else:
        slug = slug_from_query(args.query, evidence)
        out_path = vault_path("projects", "experiments", f"{today_iso()}-{slug}.md")

    if args.dry_run:
        safe_print(content)
        return 0

    safe_write(out_path, content)
    safe_print(f"PLAN_PATH: {rel(out_path)}")
    safe_print(f"EVIDENCE_LEVEL: {evidence_level(evidence)}")
    if evidence.gaps:
        safe_print("EVIDENCE_GAPS: " + ", ".join(evidence.gaps))
    else:
        safe_print("EVIDENCE_GAPS: none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
