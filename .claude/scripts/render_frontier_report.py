"""Render the frontier-research-map data into a human-readable vault report.

When frontier_workflow_result.json exists (produced by a Claude multi-agent session),
renders the full report with frontier maps + candidates + feasibility. When it does not
exist (monthly automated run), renders a gap-only report from topic_clusters.json +
distilled_gaps.json. Date is always derived from today, not hardcoded.
"""
from __future__ import annotations

import json
from datetime import date

from kb_common import safe_print, vault_path

EV = vault_path("projects", "research-agenda", "evidence")
WORKFLOW_RESULT = EV / "frontier_workflow_result.json"
CLUSTERS = EV / "topic_clusters.json"
GAPS = EV / "distilled_gaps.json"


def rec_rank(f: dict) -> int:
    v = f.get("verdict", {})
    rec = 2 if str(v.get("recommended", "")).lower().startswith("y") else 0
    hi = 1 if str(v.get("potential", "")).lower() == "high" else 0
    return rec + hi


def _render_full(r: dict, today: str) -> tuple[str, int]:
    L: list[str] = []
    paired = list(zip(r.get("candidates", []), r.get("feasibility", [])))
    paired.sort(key=lambda p: -rec_rank(p[1]))
    rec = sum(1 for _, f in paired if str(f.get("verdict", {}).get("recommended", "")).lower().startswith("y"))
    L += [
        "---",
        f"title: 机器人操控前沿研究地图与博士课题候选",
        "tags: [research-agenda, frontier-map, output]",
        f"created: {today}",
        f"updated: {today}",
        "type: permanent",
        "status: done",
        f'summary: "深读精读库中 9 大前沿方向代表作建成的前沿地图，综合出 {len(paired)} 个跨方向联合博士课题候选，{rec} 个 recommended。"',
        "---", "",
        "# 机器人操控前沿研究地图与博士课题候选", "",
        f"> {today} · multi-agent 深读代表作生成",
        "> 定位：前沿方法（VLA / diffusion / world-model / tactile / sim-to-real）是潜力来源，DLO / 双臂 / 接触是落地验证场景", "",
        "## 一、博士课题候选（按推荐度排序）", "",
    ]
    for i, (c, f) in enumerate(paired, 1):
        v = f.get("verdict", {})
        tag = " ⭐ 推荐" if str(v.get("recommended", "")).lower().startswith("y") else ""
        L += [
            f"### {i}. {c.get('title', '')}{tag}",
            f"- **联合方向**：{', '.join(c.get('combines_directions', []))}",
            f"- **可行性裁决**：潜力={v.get('potential')} · 可行={v.get('feasible')} · 推荐={v.get('recommended')} — {v.get('reason', '')}",
            f"- **前沿硬骨头**：{c.get('frontier_hard_problem', '')}",
            f"- **方法**：{c.get('method_approach', '')}",
            f"- **验证场景**：{c.get('validation_scene', '')}",
            f"- **为何有潜力**：{c.get('why_high_potential', '')}",
            f"- **证据支撑**：{'; '.join(c.get('evidence_support', []))}",
            f"- **无硬件 pilot**：{f.get('no_hardware_pilot', '')}",
            f"- **新颖性初判**：{f.get('novelty_judgment', '')}",
            f"- **风险**：{f.get('risk', '')}", "",
        ]
    L += ["## 二、九大前沿方向地图", ""]
    for m in r.get("frontier_map", []):
        L += [f"### {m.get('direction', '')}", "", f"**范式**：{m.get('paradigm', '')}", "", f"**演进**：{m.get('evolution', '')}", "", "**真硬骨头**："]
        for h in m.get("hard_problems", []):
            L.append(f"- **{h.get('problem', '')}** — {h.get('why_hard', '')}（触及：{h.get('touched_by', '')}）")
        L.append("**代表作**：")
        for p in m.get("key_papers", []):
            L.append(f"- {p.get('title', '')}：{p.get('contribution', '')}")
        L.append("")
    return "\n".join(L) + "\n", rec


def _render_gap_only(today: str) -> tuple[str, int]:
    L: list[str] = []
    clusters = json.loads(CLUSTERS.read_text(encoding="utf-8")) if CLUSTERS.exists() else {}
    gaps = json.loads(GAPS.read_text(encoding="utf-8")) if GAPS.exists() else {}
    total_gaps = sum(len(c.get("distilled_gaps", [])) for c in gaps.get("clusters", []))
    L += [
        "---",
        f"title: 月度前沿 Gap 报告",
        "tags: [research-agenda, frontier-review, gap-analysis, output]",
        f"created: {today}",
        f"updated: {today}",
        "type: permanent",
        "status: done",
        f'summary: "月度自动盘点：{clusters.get("n_papers", 0)} 篇 → {clusters.get("k", 0)} 簇 → {total_gaps} 条精炼 gap。"',
        "---", "",
        f"# 月度前沿 Gap 报告 — {today}", "",
        f"> 确定性管线自动生成。深度综合（前沿地图 + 课题候选）需在 claudian 会话中运行 frontier workflow。", "",
        f"## 主题聚类（{clusters.get('k', 0)} 簇，{clusters.get('n_papers', 0)} 篇）", "",
    ]
    for cl in clusters.get("clusters", [])[:20]:
        tags = ", ".join(f"{t}:{n}" for t, n in (cl.get("top_tags") or [])[:6])
        L.append(f"- **C{cl['cluster_id']}** n={cl['size']} main={cl.get('main_direction_score', 0)}  {tags}")
    L += ["", f"## 精炼 Gap（{total_gaps} 条）", ""]
    for gc in gaps.get("clusters", []):
        cid = gc.get("cluster_id")
        dg = gc.get("distilled_gaps", [])
        if not dg:
            continue
        tags = ", ".join(f"{t}" for t, _ in (gc.get("top_tags") or [])[:4])
        L.append(f"### C{cid}（{tags}，{gc.get('papers', 0)} 篇 → {len(dg)} gap）")
        for g in dg[:8]:
            L.append(f"- [{g.get('tension_type')}] {g.get('summary', '')[:120]}")
        L.append("")
    return "\n".join(L) + "\n", 0


def main() -> int:
    today = date.today().isoformat()
    if WORKFLOW_RESULT.exists():
        r = json.loads(WORKFLOW_RESULT.read_text(encoding="utf-8"))
        content, rec = _render_full(r, today)
        mode = "full"
    elif GAPS.exists() or CLUSTERS.exists():
        content, rec = _render_gap_only(today)
        mode = "gap-only"
    else:
        safe_print("no frontier data found (need topic_clusters.json or frontier_workflow_result.json)")
        return 1
    out = vault_path("output", f"{today}-frontier-research-map.md")
    out.write_text(content, encoding="utf-8")
    safe_print(f"wrote {out}  (mode={mode}" + (f", {rec} recommended)" if mode == "full" else ")"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
