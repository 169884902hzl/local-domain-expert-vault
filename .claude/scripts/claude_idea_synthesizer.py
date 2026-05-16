"""Use Claude Code for compact idea synthesis, then render auditable Markdown."""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from audit_daily_ideas import audit as audit_ideas
from arxiv_ranker import RankedPaper
from generate_daily_ideas import (
    EvidenceItem,
    evidence_level,
    focus_candidates,
    load_ranked_jsonl,
    local_evidence,
    local_evidence_for_zotero_keys,
    render_ideas,
)
from kb_common import safe_print, safe_write, today_iso, vault_path


CLAUDE_COMMAND = ["claude", "--permission-mode", "bypassPermissions", "--effort", "low", "-p"]
IDEA_FIELDS = [
    "title",
    "problem",
    "hypothesis",
    "cross_paper_pattern",
    "knowledge_base_support",
    "novelty_hypothesis",
    "why_now",
    "current_practice",
    "similar_work",
    "implementation_plan",
    "pilot_experiment",
    "variables",
    "baselines",
    "metrics",
    "risk",
    "next_step",
    "candidate_indices",
    "local_evidence_query",
]


def _resolve(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return vault_path(*candidate.parts)


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _candidate_brief(candidates: list[RankedPaper], limit: int = 8) -> str:
    lines: list[str] = []
    for index, item in enumerate(candidates[:limit], 1):
        paper = item.paper
        summary = " ".join(paper.summary.split())[:260]
        lines.append(
            "\n".join(
                [
                    f"{index}. {paper.title}",
                    f"   arxiv: {paper.arxiv_id}",
                    f"   url: {paper.url or paper.pdf_url}",
                    f"   score: {item.quality_score}; decision: {item.decision}",
                    f"   signal: {summary}",
                ]
            )
        )
    return "\n\n".join(lines) if lines else "evidence_gap: no candidates"


def _local_brief(limit: int = 8, *, focus_zotero_keys: list[str] | None = None) -> str:
    focused = local_evidence_for_zotero_keys(focus_zotero_keys or [], limit)
    general = local_evidence("embodied AI robot learning manipulation DLO tactile sim-to-real diffusion bimanual planning", limit, status="done")
    items: list[EvidenceItem] = []
    seen: set[str] = set()
    for item in [*focused, *general]:
        if item.link in seen:
            continue
        items.append(item)
        seen.add(item.link)
        if len(items) >= limit:
            break
    if not items:
        return "evidence_gap: no local evidence"
    return "\n".join(f"- {item.link}: {item.detail[:180]}" for item in items)


def _legacy_mojibake_prompt(candidates: list[RankedPaper], run_date: str) -> str:
    fields = ", ".join(IDEA_FIELDS)
    return f"""你是 vault owner 的 ClaudeCode 研究 idea 合作者。请基于每日 arXiv 候选和本地 vault 线索，发散但可落地地提出 embodied AI / 双臂 DLO / tactile / VLA / Sim-to-Real 方向研究 idea。

请只输出 5 个纯文本 block，不要 Markdown，不要解释。格式必须严格如下，每个字段一行：
BEGIN_IDEA
title: ...
problem: ...
hypothesis: ...
current_practice: ...
similar_work: ...
implementation_plan: ...
experiment: ...
variables: ...
baselines: ...
metrics: ...
risk: ...
next_step: ...
candidate_indices: 1,5
local_evidence_query: ...
END_IDEA

每个 block 都必须包含这些字段：{fields}。

风格要求：
- 不要太保守，要寻找新颖组合、被忽略的问题和低成本 pilot。
- 但不要编造实验数字，不要说 idea 已被证明正确。
- candidate_indices 使用下面候选的编号数组，例如 [1, 5]。
- local_evidence_query 给一个用于 vault 检索的英文关键词短语。
- similar_work 写已有类似工作/需要核查的关键词；如果只基于摘要，就写 need_to_verify。
- implementation_plan 要具体到数据、模型、模块、硬件/仿真、第一版怎么做。
- baselines 和 metrics 必须可执行。
- 不要在字段里写具体百分比、x/y 或 1/3/5 这类无引用数字；实验规模请写 low/medium/high 或 small/medium/large。

run_date: {run_date}

Daily arXiv candidates:
{_candidate_brief(candidates)}

Local vault signals:
{_local_brief()}
"""


def build_prompt(candidates: list[RankedPaper], run_date: str, *, focus_zotero_keys: list[str] | None = None) -> str:
    fields = ", ".join(IDEA_FIELDS)
    return f"""You are ClaudeCode acting as a research-idea synthesis partner for embodied AI, bimanual DLO manipulation, tactile sensing, VLA, diffusion policy, and Sim-to-Real.
Generate ideas from evidence clusters, not from a single paper. First compare the daily arXiv set with the local done readings. The daily set below should be treated as today's deep-read import set when focus IDs are provided. Each idea must be supportable by at least two daily papers and at least three local done readings after rendering.

Output exactly 5 plain-text blocks. Do not output Markdown or explanations outside the blocks. Each field must be one line:
BEGIN_IDEA
title: ...
problem: ...
hypothesis: ...
cross_paper_pattern: ...
knowledge_base_support: ...
novelty_hypothesis: ...
why_now: ...
current_practice: ...
similar_work: ...
implementation_plan: ...
pilot_experiment: ...
variables: ...
baselines: ...
metrics: ...
risk: ...
next_step: ...
candidate_indices: 1,3,7
local_evidence_query: ...
END_IDEA

Every block must include these fields: {fields}.
Rules:
- Be creative: look for cross-paper combinations, ignored problems, and low-cost pilots.
- Do not claim the idea is proven or guaranteed.
- Do not invent specific experimental numbers, percentages, or x/y claims.
- candidate_indices must include at least two daily candidate indices, for example: 1,3,7.
- local_evidence_query must be an English KB query likely to retrieve at least three done local readings.
- similar_work should list related work keywords to verify. Use need_to_verify when uncertain.
- implementation_plan must mention data, model/module, hardware or simulator, and the first prototype.
- pilot_experiment, baselines, and metrics must be executable.
run_date: {run_date}

Daily arXiv candidates:
{_candidate_brief(candidates)}

Local done vault signals:
{_local_brief(focus_zotero_keys=focus_zotero_keys)}
"""


def _extract_idea_blocks(text: str) -> list[dict[str, Any]]:
    blocks = re.findall(r"BEGIN_IDEA\s*(.*?)\s*END_IDEA", text, flags=re.DOTALL | re.IGNORECASE)
    ideas: list[dict[str, Any]] = []
    for block in blocks[:5]:
        item: dict[str, Any] = {}
        current_key = ""
        for raw in block.splitlines():
            line = raw.strip()
            if not line:
                continue
            match = re.match(r"^([a-z_]+):\s*(.*)$", line, flags=re.IGNORECASE)
            if match:
                current_key = match.group(1).lower()
                item[current_key] = match.group(2).strip()
            elif current_key:
                item[current_key] = f"{item[current_key]} {line}".strip()
        raw_indices = str(item.get("candidate_indices", ""))
        item["candidate_indices"] = [int(value) for value in re.findall(r"\d+", raw_indices)[:3]]
        ideas.append(item)
    if len(ideas) < 5:
        raise ValueError(f"idea_count_below_5:{len(ideas)}")
    return ideas


def call_claude(prompt: str, *, timeout: int) -> str:
    if shutil.which("claude") is None:
        raise FileNotFoundError("claude CLI not found")
    if len(prompt) > 12000:
        raise ValueError(f"prompt_too_long:{len(prompt)}")
    proc = subprocess.run(
        [*CLAUDE_COMMAND, prompt],
        cwd=vault_path(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        detail = (proc.stdout or "") + ("\nSTDERR:\n" + proc.stderr if proc.stderr else "")
        raise RuntimeError(detail.strip()[-1600:])
    return proc.stdout or ""


def _candidate_evidence(candidates: list[RankedPaper], indices: list[Any], *, max_items: int = 3) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for value in list(indices)[:max_items]:
        try:
            index = int(value) - 1
        except (TypeError, ValueError):
            continue
        if index < 0 or index >= len(candidates):
            continue
        item = candidates[index]
        paper = item.paper
        detail = f"arXiv:{paper.arxiv_id}; score={item.quality_score}; decision={item.decision}"
        evidence.append(EvidenceItem(label=paper.title, link=f"[{paper.title}]({paper.url or paper.pdf_url})", detail=detail))
    return evidence


def _ensure_candidate_cluster(candidates: list[RankedPaper], indices: list[Any], minimum: int = 2) -> list[EvidenceItem]:
    evidence = _candidate_evidence(candidates, indices)
    seen = {item.link for item in evidence}
    for index in range(1, len(candidates) + 1):
        if len(evidence) >= minimum:
            break
        for item in _candidate_evidence(candidates, [index]):
            if item.link not in seen:
                evidence.append(item)
                seen.add(item.link)
    return evidence


def _ensure_local_done_cluster(query: str, minimum: int = 3, *, preferred: list[EvidenceItem] | None = None) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    seen: set[str] = set()
    for item in preferred or []:
        if item.link in seen:
            continue
        evidence.append(item)
        seen.add(item.link)
        if len(evidence) >= minimum:
            break
    for item in local_evidence(query, 5, status="done"):
        if item.link in seen:
            continue
        evidence.append(item)
        seen.add(item.link)
        if len(evidence) >= 5:
            break
    for item in local_evidence("DLO tactile diffusion bimanual sim-to-real planning manipulation", 8, status="done"):
        if len(evidence) >= minimum:
            break
        if item.link not in seen:
            evidence.append(item)
            seen.add(item.link)
    return evidence[:5]


def _format_evidence(items: list[EvidenceItem]) -> list[str]:
    if not items:
        return ["  - evidence_gap: no linked evidence found"]
    return [f"  - {item.link}: {item.detail}" for item in items]


def _field(item: dict[str, Any], name: str, fallback: str) -> str:
    value = item.get(name, fallback)
    if isinstance(value, list):
        value = ", ".join(str(part) for part in value)
    text = str(value).strip() or fallback
    text = re.sub(r"\b\d+(?:\.\d+)?\s*%", "reported percentage (verify before use)", text)
    text = re.sub(r"\b\d+\s*/\s*\d+(?:\s*/\s*\d+)*", "low/medium/high levels", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\s*(?:-|to)\s*\d+(?:\.\d+)?", "low-to-high range", text)
    text = re.sub(
        r"\b\d+(?:\.\d+)?\s*(?:K\+|k\+)?\s*(demos?|demonstrations?|episodes?|rollouts?|samples?|tasks?|steps?|conditions?)\b",
        r"small/medium/large \1",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\b\d+(?:\.\d+)?\s*(?:K\+|k\+|x|Hz|FPS|ms|sec(?:onds?)?|min(?:utes?)?)\b",
        "reported numeric value (verify before use)",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\b\d+(?:\.\d+)?[- ](?:step|stage|view|arm|task)\b", "multi-step", text, flags=re.IGNORECASE)
    return text


def render_claude_ideas(
    ideas: list[dict[str, Any]],
    candidates: list[RankedPaper],
    *,
    run_date: str,
    focus_zotero_keys: list[str] | None = None,
) -> str:
    focused_local = local_evidence_for_zotero_keys(focus_zotero_keys or [], 10)
    general_local = local_evidence("embodied AI robot learning manipulation DLO tactile sim-to-real", 8, status="done")
    global_local: list[EvidenceItem] = []
    seen_local: set[str] = set()
    for item in [*focused_local, *general_local]:
        if item.link in seen_local:
            continue
        global_local.append(item)
        seen_local.add(item.link)
        if len(global_local) >= 10:
            break
    global_daily = _candidate_evidence(candidates, range(1, min(len(candidates), 10) + 1), max_items=10)
    lines = [
        "---",
        f'title: "Daily Embodied AI Ideas - {run_date}"',
        "tags: [idea, arxiv, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        'summary: "Daily ClaudeCode-synthesized embodied AI research ideas generated from arXiv evidence clusters and done local readings."',
        f'evidence_level: "{evidence_level(global_daily + global_local)}"',
        "---",
        "",
        f"# Daily Embodied AI Ideas - {run_date}",
        "",
        "## Evidence Sources",
        "",
        "### Daily arXiv Candidates",
        *_format_evidence(global_daily),
        "",
        "### Local Vault Evidence (status: done)",
        *_format_evidence(global_local),
        "",
    ]
    for index, idea in enumerate(ideas[:5], 1):
        candidate_items = _ensure_candidate_cluster(candidates, idea.get("candidate_indices", []))
        local_items = _ensure_local_done_cluster(
            _field(idea, "local_evidence_query", "DLO tactile bimanual manipulation"),
            preferred=focused_local,
        )
        evidence = candidate_items + local_items
        risk = _field(idea, "risk", "The idea may be too broad or under-supported by current evidence.")
        if "hypothesis scaffold" not in risk:
            risk = f"{risk} This is a hypothesis scaffold, not proof that the idea will work."
        lines.extend(
            [
                f"## Idea {index}: {_field(idea, 'title', 'Untitled research idea')}",
                "",
                f"- Problem: {_field(idea, 'problem', 'evidence_gap: problem not specified')}",
                f"- Hypothesis: {_field(idea, 'hypothesis', 'evidence_gap: hypothesis not specified')}",
                "- Decision Status: candidate_pending_human_selection",
                f"- Cross-paper Pattern: {_field(idea, 'cross_paper_pattern', 'evidence_gap: cross-paper pattern not specified')}",
                f"- Knowledge Base Support: {_field(idea, 'knowledge_base_support', 'evidence_gap: local KB support not specified')}",
                f"- Novelty Hypothesis: {_field(idea, 'novelty_hypothesis', 'evidence_gap: novelty hypothesis not specified')}",
                f"- Why Now: {_field(idea, 'why_now', 'evidence_gap: why-now rationale not specified')}",
                f"- Current Practice: {_field(idea, 'current_practice', 'need_to_verify: current practice not specified')}",
                f"- Similar Work: {_field(idea, 'similar_work', 'need_to_verify: similar work not specified')}",
                f"- Implementation Plan: {_field(idea, 'implementation_plan', 'evidence_gap: implementation plan not specified')}",
                f"- Pilot Experiment: {_field(idea, 'pilot_experiment', 'evidence_gap: pilot experiment not specified')}",
                f"- Variables: {_field(idea, 'variables', 'independent/dependent/control variables need specification')}",
                f"- Baselines: {_field(idea, 'baselines', 'evidence_gap: baselines not specified')}",
                f"- Metrics: {_field(idea, 'metrics', 'evidence_gap: metrics not specified')}",
                f"- Evidence Level: {evidence_level(evidence)}",
                "- Evidence Cluster:",
                "  - Daily Papers:",
                *_format_evidence(candidate_items),
                "  - Local Done Papers:",
                *_format_evidence(local_items),
                f"- Risk: {risk}",
                f"- Next Step: {_field(idea, 'next_step', 'Turn this into a `/plan-experiment` draft before acting on it.')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def synthesize(args: argparse.Namespace) -> int:
    run_date = args.run_date or today_iso()
    candidates_path = _resolve(args.candidates)
    output_path = _resolve(args.output)
    candidates = sorted(load_ranked_jsonl(candidates_path), key=lambda item: -item.quality_score)
    focus_arxiv_ids = _split_csv(args.focus_arxiv_ids)
    focus_zotero_keys = _split_csv(args.focus_zotero_keys)
    prompt_candidates = focus_candidates(candidates, focus_arxiv_ids) or candidates
    prompt = build_prompt(prompt_candidates, run_date, focus_zotero_keys=focus_zotero_keys)

    if args.prompt_out:
        prompt_path = _resolve(args.prompt_out)
        safe_write(prompt_path, prompt, dry_run=args.dry_run, backup=True)
        safe_print(f"CLAUDE_IDEA_PROMPT: {prompt_path.relative_to(vault_path())}")
    if args.dry_run:
        safe_print(f"CLAUDE_IDEA_PROMPT_CHARS: {len(prompt)}")
        safe_print("CLAUDE_IDEA_STATUS: dry_run")
        return 0

    try:
        raw = call_claude(prompt, timeout=args.timeout)
        ideas = _extract_idea_blocks(raw)
        content = render_claude_ideas(ideas, prompt_candidates, run_date=run_date, focus_zotero_keys=focus_zotero_keys)
        tmp_path = vault_path(".claude", "tmp", f"{run_date}-claude-idea-audit.md")
        tmp_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path.write_text(content, encoding="utf-8")
        result = audit_ideas(tmp_path)
        if result["status"] == "FAIL":
            raise ValueError("audit_failed:" + str(result)[:1200])
        safe_write(output_path, content, dry_run=False, backup=True)
        safe_print("CLAUDE_IDEA_STATUS: success")
        safe_print(f"CLAUDE_IDEA_AUDIT: {result['status']}")
        safe_print(f"CLAUDE_IDEA_OUTPUT: {output_path.relative_to(vault_path())}")
        return 0
    except Exception as exc:
        fallback = render_ideas(
            candidates,
            run_date=run_date,
            focus_arxiv_ids=focus_arxiv_ids,
            focus_zotero_keys=focus_zotero_keys,
        )
        safe_write(output_path, fallback, dry_run=False, backup=True)
        safe_print("CLAUDE_IDEA_STATUS: fallback_template")
        safe_print(f"CLAUDE_IDEA_ERROR: {exc}")
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--draft", help="Accepted for compatibility; no longer required.")
    parser.add_argument("--candidates", required=True, help="Ranked candidates JSONL path.")
    parser.add_argument("--output", required=True, help="Final idea markdown path.")
    parser.add_argument("--run-date", help="Run date in YYYY-MM-DD.")
    parser.add_argument("--focus-arxiv-ids", default="", help="Comma-separated arXiv IDs for today's deep-read imports.")
    parser.add_argument("--focus-zotero-keys", default="", help="Comma-separated Zotero keys for today's deep-read imports.")
    parser.add_argument("--prompt-out", help="Optional path to save the compact Claude prompt.")
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    return synthesize(args)


if __name__ == "__main__":
    raise SystemExit(main())
