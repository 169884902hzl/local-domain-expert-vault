from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from research_seed_v2_common import artifact_dir, init_manifest, write_json, write_jsonl, write_run_artifact


RUN_DATE = "2099-03-04"


class V03TempAgendaTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.old_root = os.environ.get("RESEARCH_SEED_V2_AGENDA_ROOT")
        os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.tmp.name
        init_manifest(RUN_DATE, backfill_mode="daily")

    def tearDown(self) -> None:
        if self.old_root is None:
            os.environ.pop("RESEARCH_SEED_V2_AGENDA_ROOT", None)
        else:
            os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.old_root
        self.tmp.cleanup()

    def candidate(self, candidate_id: str = "cand-alpha") -> dict[str, Any]:
        return {
            "candidate_id": candidate_id,
            "title": "Anchored Contact Failure Benchmark",
            "problem": "Contact policies fail under latent friction shifts.",
            "mechanism": "Expose recovery triggers with anchored contact evidence.",
            "strongest_baseline": "Diffusion policy with fixed recovery threshold",
            "lane": "infrastructure_or_benchmark",
            "supporting_nodes": ["claim-1"],
        }

    def write_claim_graph_node(
        self,
        *,
        node_id: str = "claim-1",
        paper_key: str = "PAPER-A",
        claim_type: str = "central_claim",
        confidence: str = "high",
        anchor_type: str = "section",
        snippet: str = "Contact policies fail under latent friction shifts.",
        requires_human_check: bool = False,
    ) -> None:
        anchor = {
            "source_note": f"wiki/topics/{paper_key}.md",
            "evidence_anchor": f"wiki/topics/{paper_key}.md#Results",
            "anchor_type": anchor_type,
            "anchor_source": "note_section",
            "section": "Results",
            "snippet": snippet,
            "pdf_page": None,
        }
        write_jsonl(
            artifact_dir(RUN_DATE) / "claim-graph-snapshot.jsonl",
            [
                {
                    "schema_version": "research_claim_graph.v1",
                    "record_type": "node",
                    "node_id": node_id,
                    "paper_key": paper_key,
                    "paper_id": paper_key,
                    "source_note": anchor["source_note"],
                    "source_title": paper_key,
                    "claim_type": claim_type,
                    "statement": snippet,
                    "confidence": confidence,
                    "confidence_reason": "test_fixture",
                    "evidence_anchor": anchor["evidence_anchor"],
                    "anchor_type": anchor_type,
                    "anchor_source": "note_section",
                    "summary_origin": "section_summary",
                    "requires_human_check": requires_human_check,
                    "anchor": anchor,
                    "supporting_node_ids": [],
                    "domains": ["dlo", "contact"],
                }
            ],
        )

    def write_base_reviews(
        self,
        *,
        novelty: str = "likely_open",
        verification_scope: str = "local_plus_s2_or_openalex",
        codex_action: str = "accept_for_user_review",
        fatal_flaw: bool = False,
        anchorless: bool = False,
        stale_cache: bool = False,
    ) -> None:
        item = self.candidate()
        cid = item["candidate_id"]
        self.write_claim_graph_node(anchor_type="note_only" if anchorless else "section")
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {"schema_version": "selected_candidates.v1", "run_date": RUN_DATE, "selected": [item], "rejected": [], "selection_rules": {}, "artifact_hashes": {}},
            state="portfolio_selected",
        )
        write_run_artifact(
            RUN_DATE,
            "deepseek-review.json",
            {
                "schema_version": "deepseek_review.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "provider_status": {"provider": "deepseek", "provider_backed": True, "mode": "opencode"},
                "reviews": [
                    {
                        "candidate_id": cid,
                        "status": "success",
                        "novelty_attack": "checked",
                        "baseline_attack": "checked",
                        "mechanism_attack": "checked",
                        "evaluation_attack": "checked",
                        "scope_attack": "checked",
                        "a_plus_b_risk": "low",
                        "fatal_flaw": "fatal" if fatal_flaw else "",
                        "rescue_mutation": "",
                        "survivability_label": "reject_fatal" if fatal_flaw else "survives",
                        "allowed_next_stage": "novelty_scan",
                    }
                ],
                "artifact_hashes": {},
            },
            state="attacked_by_deepseek",
        )
        provider_results = {
            "openalex": {
                "provider": "openalex",
                "status": "success",
                "records_scanned": 1,
                "cached": False,
                "cache_status": "stale" if stale_cache else "fresh",
                "queries": 1,
            }
        }
        write_run_artifact(
            RUN_DATE,
            "novelty-scan.json",
            {
                "schema_version": "novelty_scan.v1",
                "run_date": RUN_DATE,
                "status": "completed",
                "scans": [
                    {
                        "candidate_id": cid,
                        "candidate_title": item["title"],
                        "status": "completed",
                        "novelty_classification": novelty,
                        "promotion_allowed": novelty in {"likely_open", "partial_overlap"},
                        "formal_promotion_allowed": novelty in {"likely_open", "partial_overlap"} and not stale_cache,
                        "verification_scope": verification_scope,
                        "external_providers_used": ["openalex"] if verification_scope != "local_only" and not stale_cache else [],
                        "provider_results": provider_results,
                        "provider_errors": [],
                        "formal_publish_risk": "stale_external_novelty_cache" if stale_cache else "",
                        "stale_external_novelty_cache": stale_cache,
                        "nearest_works": [{"source": "openalex", "score": 0.2, "title": "Nearest work", "work_id": "W1"}],
                        "strongest_baseline": {"source": "candidate_field", "score": 0.1, "title": item["strongest_baseline"]},
                        "duplicate_guard": {"status": "pass", "action": "allow_with_lineage", "nearest_candidates": []},
                    }
                ],
                "provider_policy": {},
                "artifact_hashes": {},
            },
            state="novelty_checked",
        )
        write_run_artifact(
            RUN_DATE,
            "codex-execution-review.json",
            {
                "schema_version": "codex_execution_review.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "provider_status": {"provider": "codex", "provider_backed": True, "mode": "codex-cli"},
                "reviews": [
                    {
                        "candidate_id": cid,
                        "status": "success",
                        "action": codex_action,
                        "no_hardware_pilot_feasibility": "feasible",
                        "public_dataset_or_sim_availability": "available",
                        "baseline_training_cost": "single GPU day",
                        "metric_automation": "pytest evaluator",
                        "data_leakage_risk": "low",
                        "minimal_repo_plan": "notebook plus evaluator",
                        "real_robot_pilot_complexity": "low",
                        "reproducibility_path": "public sim",
                        "compute_time_budget": "one day",
                    }
                ],
                "artifact_hashes": {},
            },
            state="execution_reviewed",
        )

    def write_manual_review(self, *, decision: str = "allow_active_seed") -> None:
        write_run_artifact(
            RUN_DATE,
            "manual-prior-art-review.json",
            {
                "schema_version": "manual_prior_art_review.v1",
                "run_date": RUN_DATE,
                "reviews": [
                    {
                        "candidate_id": "cand-alpha",
                        "review_status": "completed",
                        "reviewer": "human",
                        "reviewed_at": "2099-03-04T12:00:00+00:00",
                        "searched_sources": ["OpenAlex", "Semantic Scholar", "arXiv", "Google Scholar/manual"],
                        "search_queries": ["anchored contact failure DLO benchmark"],
                        "nearest_works": [{"title": "Nearest work", "source": "manual", "url": "", "overlap_type": "adjacent", "what_is_already_done": "Adjacent benchmark", "remaining_delta": "Anchored contact failure"}],
                        "explicit_no_near_work_reason": "",
                        "strongest_baseline_judgment": {
                            "status": "known",
                            "baseline_name": "Diffusion policy with fixed recovery threshold",
                            "source_work_id": "manual:W1",
                            "why_strongest": "Direct policy baseline.",
                            "kill_condition": "Reject if it matches failure detection.",
                            "metric_or_task": "failure_detection_auc",
                            "implementation_feasibility": "available",
                        },
                        "known_overlap_risk": "medium",
                        "remaining_delta": "Anchored contact failure benchmark.",
                        "decision": decision,
                        "reason": "Manual review completed.",
                        "limitations": "Not publishability proof.",
                        "risk_acceptance": "Human accepts active-seed risk.",
                        "cannot_weaken": [
                            "deepseek_success_required",
                            "codex_accept_required",
                            "external_novelty_required",
                            "anchored_core_evidence_required",
                            "no_unresolved_fatal_flaw",
                            "fresh_external_cache_required",
                        ],
                    }
                ],
            },
            state="manual_prior_art_reviewed",
        )

    def write_baseline_table(self, *, known: bool = True) -> None:
        write_run_artifact(
            RUN_DATE,
            "baseline-table.json",
            {
                "schema_version": "baseline_table.v1",
                "run_date": RUN_DATE,
                "candidate_id": "cand-alpha",
                "baselines": [
                    {"baseline_id": "baseline-nearest", "name": "Nearest work", "source": "novelty_scan", "baseline_role": "nearest_work", "confidence": "low"},
                    {"baseline_id": "baseline-strongest", "name": "Diffusion policy with fixed recovery threshold", "source": "manual_prior_art", "baseline_role": "manual_strongest_baseline", "kill_condition": "Reject if it matches failure detection.", "metric": "failure_detection_auc", "confidence": "high"},
                ],
                "strongest_baseline_id": "baseline-strongest" if known else "",
                "strongest_baseline_final": {
                    "status": "known" if known else "unknown",
                    "baseline_id": "baseline-strongest" if known else "",
                    "name": "Diffusion policy with fixed recovery threshold" if known else "",
                    "source": "manual_prior_art_review" if known else "",
                    "kill_condition": "Reject if it matches failure detection." if known else "",
                    "metric_or_task": "failure_detection_auc" if known else "",
                },
                "baseline_verification_status": "verified" if known else "partial",
            },
            state="baseline_table_built",
        )

    def write_pilot_plan(self, *, executable: bool = True) -> None:
        path = Path(self.tmp.name) / "pilots" / "anchored-contact-failure-benchmark" / "pilot-plan.json"
        write_json(
            path,
            {
                "schema_version": "pilot_plan.v1",
                "seed_slug": "anchored-contact-failure-benchmark",
                "candidate_id": "cand-alpha",
                "pilot_status": "planned",
                "metric": "failure_detection_auc",
                "metric_automation": "pytest evaluator" if executable else "",
                "baseline_implementation_path": "baselines/diffusion-policy-threshold",
                "resource_budget": "one GPU day",
                "executable": executable,
            },
        )
