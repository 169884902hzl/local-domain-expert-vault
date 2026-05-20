"""Reconstruct candidate baseline tables without treating nearest works as strongest baselines."""
from __future__ import annotations

import argparse
import hashlib
from typing import Any

from kb_common import safe_print
from manual_prior_art_review import completed_review_by_candidate
from research_seed_v2_common import agenda_v2_path, artifact_dir, artifact_hashes, candidate_id, ensure_v2_dirs, load_jsonl, read_json, write_jsonl, write_run_artifact


def _baseline_id(candidate: str, name: str, role: str) -> str:
    basis = f"{candidate}|{role}|{' '.join(str(name).lower().split())}"
    return "baseline-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:14]


def _final_candidates(run_date: str) -> list[dict[str, Any]]:
    selected_path = artifact_dir(run_date) / "selected-candidates.json"
    if not selected_path.exists():
        return []
    selected = read_json(selected_path).get("selected", [])
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    by_parent = {str(item.get("parent_candidate_id")): item for item in mutations if isinstance(item, dict)}
    final: list[dict[str, Any]] = []
    for item in selected:
        if not isinstance(item, dict):
            continue
        final.append(by_parent.get(candidate_id(item), item))
    return final


def _novelty_by_candidate(run_date: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / "novelty-scan.json"
    if not path.exists():
        return {}
    return {str(item.get("candidate_id")): item for item in read_json(path).get("scans", []) if isinstance(item, dict)}


def _codex_by_candidate(run_date: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / "codex-execution-review.json"
    if not path.exists():
        return {}
    return {str(item.get("candidate_id")): item for item in read_json(path).get("reviews", []) if isinstance(item, dict)}


def _claim_graph_baselines() -> list[dict[str, Any]]:
    path = agenda_v2_path("evidence", "research_claim_graph.jsonl")
    if not path.exists():
        return []
    return [
        item
        for item in load_jsonl(path)
        if item.get("record_type", "node") == "node" and item.get("claim_type") in {"strongest_baseline", "actual_baseline_result"}
    ]


def _baseline(
    *,
    candidate: str,
    name: str,
    source: str,
    role: str,
    confidence: str,
    source_work_id: str = "",
    why: str = "",
    kill_condition: str = "",
    feasibility: str = "unknown",
    metric: str = "",
    known_result: str = "",
    anchors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "baseline_id": _baseline_id(candidate, name, role),
        "name": name,
        "source_work_id": source_work_id,
        "source": source,
        "baseline_role": role,
        "why_strongest": why,
        "covered_claim": "",
        "kill_condition": kill_condition,
        "implementation_feasibility": feasibility,
        "metric": metric,
        "known_result": known_result,
        "evidence_anchor_ids": anchors or [],
        "confidence": confidence,
    }


def build_baseline_table(run_date: str, candidate: dict[str, Any]) -> dict[str, Any]:
    cid = candidate_id(candidate)
    novelty = _novelty_by_candidate(run_date).get(cid, {})
    codex = _codex_by_candidate(run_date).get(cid, {})
    manual = completed_review_by_candidate(run_date).get(cid)
    baselines: list[dict[str, Any]] = []

    guess = str(candidate.get("strongest_baseline") or candidate.get("baselines") or "").strip()
    if guess:
        baselines.append(
            _baseline(candidate=cid, name=guess, source="candidate_field", role="candidate_baseline_guess", confidence="low")
        )
    for work in novelty.get("nearest_works", []) if isinstance(novelty.get("nearest_works"), list) else []:
        name = str(work.get("title") or "").strip()
        if not name:
            continue
        baselines.append(
            _baseline(
                candidate=cid,
                name=name,
                source="novelty_scan",
                role="nearest_work",
                confidence="low",
                source_work_id=str(work.get("work_id") or work.get("locator") or ""),
                why=str(work.get("what_is_already_done") or work.get("evidence") or ""),
                metric=str(work.get("venue") or ""),
            )
        )
    if codex:
        cost = str(codex.get("baseline_training_cost") or "")
        plan = str(codex.get("reproducibility_path") or codex.get("minimal_repo_plan") or "")
        if cost or plan:
            baselines.append(
                _baseline(
                    candidate=cid,
                    name=guess or "Codex feasibility baseline",
                    source="codex_review",
                    role="codex_feasibility_baseline",
                    confidence="medium",
                    why=plan,
                    feasibility="available" if codex.get("public_dataset_or_sim_availability") == "available" else "unknown",
                    known_result=cost,
                )
            )
    for node in _claim_graph_baselines():
        statement = str(node.get("statement") or "").strip()
        if statement and guess and statement.lower() in guess.lower():
            baselines.append(
                _baseline(
                    candidate=cid,
                    name=statement,
                    source="claim_graph",
                    role="candidate_baseline_guess",
                    confidence=str(node.get("confidence") or "low"),
                    anchors=[str(node.get("node_id"))],
                    known_result=statement if node.get("claim_type") == "actual_baseline_result" else "",
                )
            )
    if manual:
        judgment = manual.get("strongest_baseline_judgment", {}) if isinstance(manual.get("strongest_baseline_judgment"), dict) else {}
        if judgment.get("status") == "known":
            baselines.append(
                _baseline(
                    candidate=cid,
                    name=str(judgment.get("baseline_name") or ""),
                    source="manual_prior_art",
                    role="manual_strongest_baseline",
                    confidence="high",
                    source_work_id=str(judgment.get("source_work_id") or ""),
                    why=str(judgment.get("why_strongest") or ""),
                    kill_condition=str(judgment.get("kill_condition") or ""),
                    feasibility=str(judgment.get("implementation_feasibility") or "unknown"),
                    metric=str(judgment.get("metric_or_task") or ""),
                )
            )

    manual_strongest = next((item for item in baselines if item["baseline_role"] == "manual_strongest_baseline"), None)
    if manual_strongest:
        strongest = {
            "status": "known",
            "baseline_id": manual_strongest["baseline_id"],
            "name": manual_strongest["name"],
            "source": "manual_prior_art_review",
            "kill_condition": manual_strongest.get("kill_condition", ""),
            "metric_or_task": manual_strongest.get("metric", ""),
            "implementation_feasibility": manual_strongest.get("implementation_feasibility", "unknown"),
            "why_strongest": manual_strongest.get("why_strongest", ""),
        }
        status = "verified"
    else:
        strongest = {
            "status": "unknown",
            "baseline_id": "",
            "name": "",
            "source": "",
            "kill_condition": "",
            "metric_or_task": "",
            "implementation_feasibility": "unknown",
            "why_strongest": "nearest_work_is_not_strongest_baseline",
        }
        status = "partial" if baselines else "unknown"

    return {
        "schema_version": "baseline_table.v1",
        "run_date": run_date,
        "candidate_id": cid,
        "baselines": baselines,
        "strongest_baseline_id": strongest["baseline_id"],
        "strongest_baseline_final": strongest,
        "baseline_verification_status": status,
        "artifact_hashes": artifact_hashes(run_date, ["selected-candidates.json", "novelty-scan.json", "codex-execution-review.json"]),
        "boundary": "Nearest works are baseline candidates only; active seed requires known strongest_baseline_final.",
    }


def load_baseline_tables(run_date: str) -> dict[str, dict[str, Any]]:
    path = artifact_dir(run_date) / "baseline-table.json"
    if not path.exists():
        return {}
    payload = read_json(path)
    if payload.get("schema_version") == "baseline_table.v1" and payload.get("candidate_id"):
        return {str(payload.get("candidate_id")): payload}
    return {str(item.get("candidate_id")): item for item in payload.get("tables", []) if isinstance(item, dict)}


def baseline_allows_active_seed(table: dict[str, Any] | None) -> bool:
    if not table:
        return False
    strongest = table.get("strongest_baseline_final", {}) if isinstance(table.get("strongest_baseline_final"), dict) else {}
    return bool(
        strongest.get("status") == "known"
        and str(strongest.get("name") or "").strip()
        and str(strongest.get("kill_condition") or "").strip()
        and str(strongest.get("metric_or_task") or "").strip()
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    tables = [build_baseline_table(args.run_date, item) for item in _final_candidates(args.run_date)]
    payload: dict[str, Any]
    if len(tables) == 1:
        payload = tables[0]
    else:
        payload = {
            "schema_version": "baseline_table.v1",
            "run_date": args.run_date,
            "candidate_id": "__multi__",
            "baselines": [],
            "strongest_baseline_id": "",
            "strongest_baseline_final": {
                "status": "unknown",
                "baseline_id": "",
                "name": "",
                "source": "",
                "kill_condition": "",
                "metric_or_task": "",
            },
            "baseline_verification_status": "unknown" if not tables else "partial",
            "tables": tables,
            "artifact_hashes": artifact_hashes(args.run_date, ["selected-candidates.json", "novelty-scan.json", "codex-execution-review.json"]),
            "boundary": "Multi-candidate wrapper; inspect tables for per-candidate strongest baseline status.",
        }
    write_run_artifact(args.run_date, "baseline-table.json", payload, state="baseline_table_built", dry_run=args.dry_run)
    write_jsonl(agenda_v2_path("evidence", "baseline_table.jsonl"), tables, dry_run=args.dry_run)
    safe_print(f"BASELINE_TABLE: candidates={len(tables)} known={sum(1 for item in tables if baseline_allows_active_seed(item))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
