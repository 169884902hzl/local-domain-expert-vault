from __future__ import annotations

import argparse
import sys
from pathlib import Path
from unittest.mock import patch

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from pilot_feedback import write_pilot_plan, write_pilot_result
from research_seed_v2_common import read_json, write_json, write_run_artifact
from weekly_strategy_review import build_resurrection_review, main as weekly_strategy_main, sanitize_overrides


class WeeklyPilotFeedbackTest(V03TempAgendaTest):
    def test_weekly_strategy_override_cannot_weaken_hard_gates(self) -> None:
        safe, errors = sanitize_overrides({"allow_stale_external_cache": True, "lane_quota": {"grounded": 2}})
        self.assertIn("attempted_hard_gate_override:allow_stale_external_cache", errors)
        self.assertEqual(safe["overrides"], {"lane_quota": {"grounded": 2}})

    def test_resurrection_queue_includes_anchorless_and_unknown_novelty(self) -> None:
        write_run_artifact(
            RUN_DATE,
            "survival-decision.json",
            {
                "schema_version": "survival_decision.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "target_policy": "seed-candidates-only",
                "decisions": [
                    {
                        "candidate_id": "cand-alpha",
                        "candidate_title": "Anchored Contact Failure Benchmark",
                        "decision": "killed",
                        "blocks": ["unknown_novelty_without_human_override"],
                        "deepseek_label": "survives",
                        "novelty_classification": "unknown",
                        "verification_scope": "local_only",
                        "external_providers_used": [],
                        "codex_action": "rewrite_before_seed",
                        "human_override_used": False,
                        "risks": [
                            "anchorless_core_evidence_risk",
                            "manual_prior_art_review_missing",
                            "manual_prior_art_quality_incomplete",
                            "result_row_unconfirmed",
                            "cross_paper_edge_requires_human_check",
                            "strongest_baseline_unknown",
                            "baseline_execution_not_ready",
                        ],
                        "formal_rehearsal_allowed": False,
                        "active_seed_allowed": False,
                        "pilot_ready_allowed": False,
                        "publish_target": "killed",
                    }
                ],
                "artifact_hashes": {},
            },
            state="survival_decided",
        )
        review = build_resurrection_review(RUN_DATE)
        queues = review["queues"]
        self.assertTrue(queues["external_novelty_unknown"])
        self.assertTrue(queues["anchorless_evidence"])
        self.assertTrue(queues["manual_prior_art_queue"])
        self.assertTrue(queues["pdf_evidence_queue"])
        self.assertTrue(queues["baseline_table_queue"])
        self.assertTrue(queues["active_seed_qa_queue"])
        self.assertTrue(queues["result_row_confirmation_queue"])
        self.assertTrue(queues["cross_paper_edge_audit_queue"])
        self.assertTrue(queues["baseline_execution_queue"])

    def test_resurrection_queue_includes_accepted_backlog_and_prefers_accepted_source(self) -> None:
        write_run_artifact(
            RUN_DATE,
            "survival-decision.json",
            {
                "schema_version": "survival_decision.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "target_policy": "seed-candidates-only",
                "decisions": [
                    {
                        "candidate_id": "cand-alpha",
                        "candidate_title": "Run Source Candidate",
                        "decision": "accept_for_user_review",
                        "blocks": [],
                        "novelty_classification": "likely_open",
                        "codex_action": "accept_for_user_review",
                        "human_override_used": False,
                        "risks": ["manual_prior_art_review_missing"],
                        "active_seed_allowed": False,
                        "pilot_ready_allowed": False,
                        "publish_target": "seed-candidates",
                    }
                ],
                "artifact_hashes": {},
            },
            state="survival_decided",
        )
        accepted_path = Path(self.tmp.name) / "seed-candidates" / "accepted" / RUN_DATE / "cand-alpha.json"
        write_json(
            accepted_path,
            {
                "schema_version": "research_seed_bucket_item.v1",
                "run_date": RUN_DATE,
                "candidate_id": "cand-alpha",
                "candidate": {"candidate_id": "cand-alpha", "title": "Accepted Source Candidate"},
                "survival_decision": {
                    "candidate_id": "cand-alpha",
                    "candidate_title": "Accepted Source Candidate",
                    "decision": "accept_for_user_review",
                    "blocks": [],
                    "risks": ["manual_prior_art_review_missing", "active_seed_without_pilot_plan"],
                    "active_seed_allowed": False,
                    "pilot_ready_allowed": False,
                },
            },
        )
        review = build_resurrection_review(RUN_DATE)
        manual_queue = review["queues"]["manual_prior_art_queue"]
        self.assertEqual(len([item for item in manual_queue if item["candidate_id"] == "cand-alpha"]), 1)
        self.assertTrue(manual_queue[0]["source"].startswith("accepted:"))
        self.assertTrue(review["queues"]["pilot_candidate_queue"])

    def test_weekly_strategy_main_writes_proposed_files(self) -> None:
        with patch.object(sys, "argv", ["weekly_strategy_review.py", "--run-date", RUN_DATE]):
            self.assertEqual(weekly_strategy_main(), 0)
        week_dir = Path(self.tmp.name) / "strategy"
        self.assertTrue((week_dir / "resurrection-review" / "2099-W10.json").exists())
        self.assertTrue((week_dir / "weekly-overrides" / "2099-W10-strategy-overrides.proposed.json").exists())

    def test_pilot_feedback_writes_feedback_to_strategy(self) -> None:
        plan_args = argparse.Namespace(
            seed_slug="anchored-contact-failure-benchmark",
            candidate_id="cand-alpha",
            metric="failure_detection_auc",
            metric_automation="pytest evaluator",
            baseline_implementation_path="baselines/diffusion-policy-threshold",
            resource_budget="one GPU day",
            executable=True,
            dry_run=False,
        )
        write_pilot_plan(plan_args)
        result_args = argparse.Namespace(
            seed_slug="anchored-contact-failure-benchmark",
            candidate_id="cand-alpha",
            pilot_status="killed",
            result="negative",
            failure_reason="generator_signal_failure",
            baseline_result="baseline matched",
            metric_outcome="auc tie",
            what_generator_predicted_wrong="baseline weakness",
            penalize_patterns="weak_baseline",
            boost_patterns="",
            required_future_checks="baseline_reimplementation",
            dry_run=False,
        )
        write_pilot_result(result_args)
        root = Path(self.tmp.name) / "pilots" / "anchored-contact-failure-benchmark"
        feedback = read_json(root / "feedback-to-strategy.json")
        self.assertEqual(feedback["schema_version"], "pilot_feedback.v1")
        self.assertIn("weak_baseline", feedback["strategy_update"]["penalize_patterns"])
        self.assertIn("generator_signal_failure", feedback["strategy_update"]["required_future_checks"])
        self.assertTrue(feedback["strategy_update"]["cannot_weaken_hard_gates"])
        self.assertFalse(feedback["boundaries"]["seed_deleted"])
