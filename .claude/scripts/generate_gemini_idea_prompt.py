"""Generate a broad manual Gemini prompt from the long-term research agenda."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kb_common import safe_print, safe_write, today_iso, vault_path


def _resolve(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return vault_path(*candidate.parts)


def latest_candidates_path() -> Path | None:
    base = vault_path("projects", "arxiv-daily")
    if not base.exists():
        return None
    paths = sorted(base.glob("*-candidates.jsonl"), reverse=True)
    return paths[0] if paths else None


def latest_agenda_delta_path() -> Path | None:
    base = vault_path("projects", "research-agenda", "daily")
    if not base.exists():
        return None
    paths = sorted(base.glob("*-agenda-delta.md"), reverse=True)
    return paths[0] if paths else None


def load_candidates(path: Path, limit: int) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not path.exists():
        return items
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            items.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
        if len(items) >= limit:
            break
    return items


def _read_excerpt(path: Path | None, *, limit: int = 5000) -> str:
    if path is None or not path.exists():
        return "evidence_gap: file not available."
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def _candidate_lines(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["- evidence_gap: no arXiv candidate file was available."]
    lines: list[str] = []
    for index, item in enumerate(items, 1):
        paper = item.get("paper", {})
        summary = " ".join(str(paper.get("summary", "")).split())[:700]
        lines.extend(
            [
                f"### Candidate {index}: {paper.get('title', '')}",
                f"- arxiv_id: {paper.get('arxiv_id', '')}",
                f"- url: {paper.get('url', '') or paper.get('pdf_url', '')}",
                f"- score: {item.get('quality_score', '')}",
                f"- decision: {item.get('decision', '')}",
                f"- reasons: {', '.join(item.get('reasons', [])[:6])}",
                f"- abstract: {summary}",
                "",
            ]
        )
    return lines


def render_prompt(*, run_date: str, candidates_path: Path | None, items: list[dict[str, Any]]) -> str:
    source = str(candidates_path.relative_to(vault_path())).replace("\\", "/") if candidates_path else "evidence_gap"
    agenda_delta = latest_agenda_delta_path()
    agenda_source = str(agenda_delta.relative_to(vault_path())).replace("\\", "/") if agenda_delta else "evidence_gap"
    dashboard = vault_path("projects", "research-agenda", "agenda-dashboard.md")
    open_questions = vault_path("projects", "research-agenda", "problem_pool", "open_questions.md")
    transfer = vault_path("projects", "research-agenda", "problem_pool", "transfer_opportunities.md")
    lines = [
        f"# Gemini Manual Idea Prompt - {run_date}",
        "",
        "## Manual PowerShell Command",
        "",
        "Gemini CLI help on this machine confirms `-p/--prompt` works in non-interactive mode and can append stdin. If Gemini relaunch fails, keep `GEMINI_CLI_NO_RELAUNCH=true`.",
        "",
        "```powershell",
        "$env:GEMINI_CLI_NO_RELAUNCH = 'true'",
        f"Get-Content -Raw '<local-vault-path>\\projects\\ideas\\{run_date}-gemini-idea-prompt.md' | gemini -p \"请按输入内容发散研究 idea，优先给出新颖但可实验验证的方向。\"",
        "```",
        "",
        "## Prompt",
        "",
        "你是我的研究 idea 发散伙伴，也是一个非常严厉的 Physical AI / robotics PhD advisor。研究背景是双臂机器人 DLO 操控、触觉、VLA、Diffusion Policy、Sim-to-Real 和 embodied robot learning。",
        "",
        "我不希望你太快收敛，也不要只做保守的论文总结。请先发散再审稿，寻找被忽略的问题、跨方向组合、反常识假设、工程病灶、低成本试验切入点，以及能形成博士课题主线的创新点。可以给不成熟但有潜力的 idea，但请标出哪些地方需要后续核查。",
        "",
        "你不需要只围绕当天论文。请优先利用长期 research agenda：problem pool、transfer opportunities、recent agenda delta、已有 seed/developing ideas。当天 arXiv 只作为新刺激，不是唯一来源。不要编造确定实验数字，也不要声称某个 idea 必然正确。",
        "",
        "特别注意：不要为了迎合历史关注点而强行写 RL Token、VLA 或 Sim-to-Real。从 2026-05-08 开始，允许自由发散；只有当证据或工程病灶真的指向这些方向时才使用它们。",
        "",
        "发散时请优先从真实机器人系统问题出发：腕部相机自遮挡、深度噪声、接触不稳定、双臂互相遮挡、标定漂移、低频 diffusion action chunk 追不上快速接触、DLO 拓扑变化不可观测、reset cost 过高、仿真接触模型失真、evaluation metric 掩盖失败模式等。你可以借鉴这些例子，但不要复制。",
        "",
        "核心目标不是“把 A 和 B 拼起来”，而是找出：新的因果机制、新的 sensing/control interface、新的 evaluation protocol、新的 failure model、或者能把已有方法从工程上明显推进一步的 mechanism-changing method improvement。请先写物理失效场景，再引用论文工具；不要先说“把论文 A 的方法 X 用到论文 B 的接口 Y”。",
        "",
        "对 RL Token 方向尤其严格：不要默认 token 空间能做预测、规划、记忆或动作修正。必须说明 token/latent/action/critic 哪个空间承载 loss，是否穿透 decoder/action head，如何避免 off-manifold latent delta，为什么这个接口比 actor residual、raw tactile conditioning、prompt memory 或普通 adapter 更有机制意义。",
        "",
        "每个深入候选都必须新增这些检查项：physical_failure_scene、interface_innovation、optimization_space、loss_placement、decoder_boundary、manifold_safety、falsification_discriminates_mechanism、lab_fit、hardware_assumptions。lab_fit 要明确是否利用我的 Franka 双臂、腕部相机主动视角、FlexiTac/触觉、DLO/cable 任务和本地日志；如果方向需要低成本硬件或大规模机器人资源，必须标为资源错配或 rewrite。",
        "",
        "请参考 HapToken v3.0 这种写法的结构深度，而不是复制内容：它有清楚的 Engineering Pathology、负声明边界（不声称什么）、核心洞察、训练/推理 pipeline、实现防御补丁、B1-B8 baseline 矩阵、指标组、未验证假设与失败处理、竞争格局、两周冲刺。你的候选也要达到这种“能立刻开 pilot”的骨架密度。",
        "",
        "希望输出：",
        "- 第一阶段：给 20-30 个自由发散 seed。每个 seed 用 3-6 句话说明 real robot pathology、可能机制、为什么不是普通组合、需要核查什么。",
        "- 第二阶段：挑出最值得深入的 8-10 个。每个都必须补充：核心问题、physical_failure_scene、engineering_pathology、interface_innovation、optimization_space、loss_placement、decoder_boundary、manifold_safety、negative_claim_boundary、version_evolution_story、core_insight、pipeline_steps、defense_patches、baseline_matrix、metric_suite、risk_assumptions、competition_map、two_week_sprint、non_obvious_claim、online_or_offline_mode、strongest_baseline、baseline_kill_table、minimum_no_hardware_pilot、killer_experiment、falsification_discriminates_mechanism、lab_fit、hardware_assumptions、metrics、主要风险、rescue_mutation。",
        "- 第三阶段：对这 8-10 个做审稿人预演。先写 reviewer_pre_mortem：如果你是 RSS/CoRL/ICRA/RA-L 审稿人，会怎样一刀毙命？如果这个反驳能杀死核心 claim，请标为 rewrite/park，不要强行说它是好 idea。",
        "- 第四阶段：给一个排序表：breakthrough_potential、engineering_pathology_strength、non_obvious_mechanism、baseline_survivability、no_hardware_pilot_feasibility、fit_to_my_lab、risk、first_pilot_cost。",
        "- 对每个深入候选都写 what_would_make_this_not_a_paper：什么情况下它只是工程 patch 或简单拼凑。",
        "- 至少保留一部分 wild_engineering：可以证据较少，但必须有尖锐工程病灶、明确机制、可证伪试验和 rescue path。",
        "- method improvement 不要被自动判成低级增量。只要它改变了 failure mechanism、interface、constraint、feedback loop 或 evaluation signal，并且能扛住最强 baseline，就可以很强。",
        "- 中英混合可以，关键术语保留英文。",
        "- 如果证据不足，请写 need_to_verify，不要装作已经确认。",
        "",
        "Gemini 输出不能直接成为 promoted idea；它只能作为 seed 或 manual review input。",
        "",
        f"agenda_delta_source: {agenda_source}",
        f"candidate_source: {source}",
        "",
        "## Research Agenda Dashboard",
        "",
        _read_excerpt(dashboard, limit=3500),
        "",
        "## Open Questions",
        "",
        _read_excerpt(open_questions, limit=3500),
        "",
        "## Transfer Opportunities",
        "",
        _read_excerpt(transfer, limit=3500),
        "",
        "## Recent Agenda Delta",
        "",
        _read_excerpt(agenda_delta, limit=3500),
        "",
        "## arXiv Candidates",
        "",
        *_candidate_lines(items),
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", help="Ranked candidates JSONL path. Defaults to latest daily file.")
    parser.add_argument("--output", help="Prompt output path. Defaults to projects/ideas/YYYY-MM-DD-gemini-idea-prompt.md.")
    parser.add_argument("--run-date", default=today_iso())
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    candidates_path = _resolve(args.candidates) if args.candidates else latest_candidates_path()
    items = load_candidates(candidates_path, args.limit) if candidates_path else []
    output = _resolve(args.output) if args.output else vault_path("projects", "ideas", f"{args.run_date}-gemini-idea-prompt.md")
    content = render_prompt(run_date=args.run_date, candidates_path=candidates_path, items=items)
    safe_write(output, content, dry_run=args.dry_run, backup=True)
    safe_print(f"GEMINI_PROMPT_PATH: {output.relative_to(vault_path())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
