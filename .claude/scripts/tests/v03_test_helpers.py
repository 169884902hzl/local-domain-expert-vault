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
        manual_confirmed: bool = False,
    ) -> None:
        anchor = {
            "source_note": f"wiki/topics/{paper_key}.md",
            "evidence_anchor": f"wiki/topics/{paper_key}.md#Results",
            "anchor_type": anchor_type,
            "anchor_source": "note_section",
            "section": "Results",
            "snippet": snippet,
            "pdf_page": None,
            "manual_confirmed": manual_confirmed,
            "confirmed_by": "human" if manual_confirmed else "",
            "confirmed_at": "2099-03-04T12:30:00+00:00" if manual_confirmed else "",
            "confirmation_note": "Manually checked against the PDF table." if manual_confirmed else "",
        }
        if anchor_type == "result_row":
            anchor.update(
                {
                    "anchor_source": "pdf_table",
                    "page": 7,
                    "row_index": 3,
                    "row_text": "baseline | auc | 0.72",
                    "metric_name": "auc",
                    "baseline_name": "baseline",
                    "reported_value": "0.72",
                    "task_or_dataset": "contact shift",
                }
            )
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

    def write_claim_graph_with_edge(self, *, edge_quality_status: str = "requires_human_check", human_confirmed: bool = False) -> None:
        records = []
        for node_id, paper_key, claim_type, statement in [
            ("claim-1", "PAPER-A", "central_claim", "Contact policies fail under latent friction shifts."),
            ("claim-2", "PAPER-B", "contradiction", "Contact policies do not fail when friction is modeled."),
        ]:
            records.append(
                {
                    "schema_version": "research_claim_graph.v1",
                    "record_type": "node",
                    "node_id": node_id,
                    "paper_key": paper_key,
                    "paper_id": paper_key,
                    "source_note": f"wiki/topics/{paper_key}.md",
                    "source_title": paper_key,
                    "claim_type": claim_type,
                    "statement": statement,
                    "confidence": "high",
                    "confidence_reason": "test_fixture",
                    "evidence_anchor": f"wiki/topics/{paper_key}.md#Results",
                    "anchor_type": "section",
                    "anchor_source": "note_section",
                    "summary_origin": "section_summary",
                    "requires_human_check": False,
                    "anchor": {"anchor_type": "section", "section": "Results", "snippet": statement},
                    "supporting_node_ids": [],
                    "domains": ["dlo", "contact"],
                }
            )
        records.append(
            {
                "schema_version": "research_claim_graph.v1",
                "record_type": "edge",
                "edge_id": "edge-cross-1",
                "paper_key": "PAPER-B",
                "source_paper_key": "PAPER-B",
                "target_paper_key": "PAPER-A",
                "source_paper_id": "PAPER-B",
                "target_paper_id": "PAPER-A",
                "edge_scope": "cross_paper",
                "source_node_id": "claim-2",
                "target_node_id": "claim-1",
                "relation": "contradicts",
                "confidence": "high",
                "confidence_reason": "test_fixture",
                "edge_reason": "assumption_conflict",
                "relation_rule": "assumption_conflict",
                "overlap_evidence": {"keyword_overlap": ["contact", "friction"], "domain_overlap": ["dlo"], "metric_overlap": [], "task_overlap": []},
                "evidence_nodes": ["claim-2", "claim-1"],
                "requires_human_check": not human_confirmed,
                "human_check_required": not human_confirmed,
                "human_confirmed": human_confirmed,
                "confirmed_by": "human" if human_confirmed else "",
                "confirmed_at": "2099-03-04T12:45:00+00:00" if human_confirmed else "",
                "edge_quality_status": edge_quality_status,
                "supporting_node_ids": ["claim-2", "claim-1"],
            }
        )
        write_jsonl(artifact_dir(RUN_DATE) / "claim-graph-snapshot.jsonl", records)

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

    def write_manual_review(self, *, decision: str = "allow_active_seed", quality_complete: bool = True) -> None:
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
                        "is_template": False,
                        "reviewer": "human",
                        "reviewed_at": "2099-03-04T12:00:00+00:00",
                        "searched_sources": ["OpenAlex", "Semantic Scholar", "arXiv", "Google Scholar/manual"],
                        "search_queries": ["anchored contact failure DLO benchmark"],
                        "review_quality_checklist": {
                            "venue_proceedings_checked": quality_complete,
                            "google_scholar_checked": quality_complete,
                            "openalex_checked": True,
                            "semantic_scholar_checked": True,
                            "arxiv_checked": True,
                            "lab_specific_sources_checked": quality_complete,
                            "negative_search_log_present": quality_complete,
                            "strongest_baseline_comparison_present": quality_complete,
                            "query_log_present": True,
                        },
                        "negative_search_log": [
                            {
                                "query": "anchored contact failure DLO benchmark",
                                "source": "OpenAlex",
                                "result_summary": "Nearest work is adjacent.",
                                "result_count": 12,
                                "why_not_overlap": "No anchored failure-trigger benchmark.",
                            }
                        ]
                        if quality_complete
                        else [],
                        "venue_search_checklist": [
                            {"venue": "ICRA/RSS/CoRL", "years": "2021-2099", "query": "DLO contact failure", "checked": quality_complete, "notes": "No direct overlap."}
                        ],
                        "nearest_works": [{"title": "Nearest work", "source": "manual", "url": "", "overlap_type": "adjacent", "what_is_already_done": "Adjacent benchmark", "remaining_delta": "Anchored contact failure"}],
                        "explicit_no_near_work_reason": "",
                        "strongest_baseline_comparison_table": [
                            {
                                "work_title": "Nearest work",
                                "source": "manual:W1",
                                "overlap_type": "adjacent",
                                "stronger_than_candidate": False,
                                "why_not_kill_or_kills": "Does not test anchored contact failure.",
                                "remaining_delta": "Contact-failure benchmark remains.",
                                "kill_condition": "Reject if it matches failure detection.",
                            }
                        ]
                        if quality_complete
                        else [],
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
                        "manual_review_quality_status": "complete" if quality_complete else "incomplete",
                        "reviewer_signature": {
                            "reviewer": "human",
                            "signed_at": "2099-03-04T12:00:00+00:00",
                            "statement": "I reviewed nearest works and accept the remaining-delta risk.",
                        }
                        if quality_complete
                        else {"reviewer": "", "signed_at": "", "statement": ""},
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

    def write_baseline_table(self, *, known: bool = True, execution_status: str = "ready") -> None:
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
                "baseline_execution_readiness": {
                    "status": execution_status if known else "unknown",
                    "source": "manual_prior_art_review" if known else "baseline_table",
                    "implementation_path": "baselines/diffusion-policy-threshold" if known else "",
                    "dataset_or_sim": "public sim" if known else "",
                    "compute_budget": "one GPU day" if known else "",
                    "metric_automation": "pytest evaluator" if known else "",
                    "not_applicable_reason": "No executable baseline needed for this protocol seed." if execution_status == "not_applicable" else "",
                    "blocking_issues": [] if execution_status in {"ready", "not_applicable"} and known else [f"baseline_execution_{execution_status if known else 'unknown'}"],
                },
            },
            state="baseline_table_built",
        )

    def write_multi_baseline_table(self, *, candidate_ids: tuple[str, str] = ("cand-alpha", "cand-beta")) -> None:
        tables = []
        for cid in candidate_ids:
            tables.append(
                {
                    "schema_version": "baseline_table.v1",
                    "run_date": RUN_DATE,
                    "candidate_id": cid,
                    "baselines": [
                        {
                            "baseline_id": f"{cid}-baseline",
                            "name": f"{cid} strongest baseline",
                            "source": "manual_prior_art_review",
                            "baseline_role": "manual_strongest_baseline",
                            "kill_condition": "Reject if matched.",
                            "metric": "success_rate",
                            "confidence": "high",
                        }
                    ],
                    "strongest_baseline_id": f"{cid}-baseline",
                    "strongest_baseline_final": {
                        "status": "known",
                        "baseline_id": f"{cid}-baseline",
                        "name": f"{cid} strongest baseline",
                        "source": "manual_prior_art_review",
                        "kill_condition": "Reject if matched.",
                        "metric_or_task": "success_rate",
                    },
                    "baseline_verification_status": "verified",
                    "baseline_execution_readiness": {
                        "status": "ready",
                        "source": "manual_prior_art_review",
                        "implementation_path": f"baselines/{cid}",
                        "dataset_or_sim": "public sim",
                        "compute_budget": "one GPU day",
                        "metric_automation": "pytest evaluator",
                        "not_applicable_reason": "",
                        "blocking_issues": [],
                    },
                }
            )
        write_run_artifact(
            RUN_DATE,
            "baseline-table.json",
            {
                "schema_version": "baseline_table.v1",
                "run_date": RUN_DATE,
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
                "baseline_verification_status": "partial",
                "baseline_execution_readiness": {
                    "status": "unknown",
                    "source": "baseline_table",
                    "implementation_path": "",
                    "dataset_or_sim": "",
                    "compute_budget": "",
                    "metric_automation": "",
                    "not_applicable_reason": "",
                    "blocking_issues": ["multi_candidate_wrapper"],
                },
                "tables": tables,
                "artifact_hashes": {},
                "boundary": "Multi-candidate wrapper; inspect tables for per-candidate strongest baseline status.",
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
