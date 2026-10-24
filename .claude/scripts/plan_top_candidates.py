"""Generate experiment-plan drafts for the recommended frontier candidates.

Reads frontier_workflow_result.json, takes the recommended (high-potential) candidates,
builds a research question from each, and runs plan_experiment.plan_from_query to write a
local-evidence-grounded experiment draft (decision_status=recommended_pending_approval,
human-approval checklist) per candidate. No active-seed commit — human approval gate stays.
"""
from __future__ import annotations

import json
import re

import plan_experiment
from kb_common import safe_print, vault_path

R = vault_path("projects", "research-agenda", "evidence", "frontier_workflow_result.json")


def query_part(value: object, *, limit: int = 140) -> str:
    text = str(value or "")
    text = re.sub(r"\([^)]*\d[^)]*\)", " ", text)
    text = re.sub(r"\bC\d+(?:/C\d+)?\b", " ", text)
    text = re.sub(r"\d+(?:\.\d+)?", " ", text)
    text = re.sub(r"\s+", " ", text).strip(" 。；;，,")
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip(" 。；;，,") + "…"


def main() -> int:
    r = json.loads(R.read_text(encoding="utf-8"))
    paired = list(zip(r.get("candidates", []), r.get("feasibility", [])))
    rec = [(c, f) for c, f in paired if str(f.get("verdict", {}).get("recommended", "")).lower().startswith("y")]
    safe_print(f"recommended candidates: {len(rec)}\n")
    for i, (c, f) in enumerate(rec, 1):
        query = "。".join(
            part
            for part in [
                query_part(c.get("title", ""), limit=90),
                "问题：" + query_part(c.get("frontier_hard_problem", ""), limit=120),
                "机制：" + query_part(c.get("method_approach", ""), limit=120),
            ]
            if part.strip("。")
        )
        out = f"projects/experiments/2026-06-15-frontier-cand{i}.md"
        try:
            result = plan_experiment.plan_from_query(query, limit=12, output=out)
            safe_print(f"[cand{i}] {c.get('title', '')[:34]} -> status={result.get('status')} path={result.get('path', out)}")
        except Exception as exc:
            safe_print(f"[cand{i}] {c.get('title', '')[:34]} -> ERROR {type(exc).__name__}: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
