from __future__ import annotations

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from manual_prior_art_review import completion_errors, completed_review_by_candidate, validate_reviews, write_template
from research_seed_v2_common import validate_payload, write_run_artifact
from survival_decision import decide


class ManualPriorArtReviewTest(V03TempAgendaTest):
    def test_template_schema_valid_but_not_completed(self) -> None:
        payload = write_template(RUN_DATE, "cand-alpha")
        self.assertEqual(validate_payload(payload, "manual_prior_art_review.v1"), [])
        self.assertIn("manual_prior_art_review_template_not_completed", completion_errors(payload["reviews"][0])[0])
        self.assertEqual(completed_review_by_candidate(RUN_DATE), {})

    def test_completed_manual_review_validates_schema(self) -> None:
        self.write_manual_review()
        _payload, errors = validate_reviews(RUN_DATE)
        self.assertEqual(errors, [])
        self.assertIn("cand-alpha", completed_review_by_candidate(RUN_DATE))

    def test_allow_active_seed_requires_manual_review(self) -> None:
        self.write_base_reviews()
        self.write_baseline_table()
        self.write_pilot_plan()
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        decision = survival["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertIn("manual_prior_art_review_missing", decision["risks"])

    def test_manual_reject_blocks_active_seed(self) -> None:
        self.write_base_reviews()
        self.write_manual_review(decision="reject")
        self.write_baseline_table()
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertIn("manual_prior_art_review_reject", decision["risks"])

    def test_manual_review_cannot_bypass_hard_gates(self) -> None:
        cases = [
            ("deepseek", {"fatal_flaw": True}, "deepseek_fatal_flaw"),
            ("codex", {"codex_action": "reject_with_rescue"}, "codex_action_not_accept"),
            ("novelty", {"novelty": "duplicate"}, "novelty_promotion_not_allowed"),
            ("anchorless", {"anchorless": True}, "anchorless_core_evidence_risk"),
        ]
        for _name, kwargs, expected in cases:
            with self.subTest(expected=expected):
                self.tearDown()
                self.setUp()
                self.write_base_reviews(**kwargs)
                self.write_manual_review()
                self.write_baseline_table()
                self.write_pilot_plan()
                decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
                self.assertFalse(decision["active_seed_allowed"])
                self.assertTrue(any(str(item).startswith(expected) for item in decision["blocks"] + decision["risks"]))

    def test_automation_cannot_generate_completed_human_review(self) -> None:
        write_run_artifact(
            RUN_DATE,
            "manual-prior-art-review.json",
            {
                "schema_version": "manual_prior_art_review.v1",
                "run_date": RUN_DATE,
                "reviews": [{"candidate_id": "cand-alpha", "review_status": "template", "reviewer": "human", "reviewed_at": "", "decision": "needs_more_search", "searched_sources": [], "search_queries": [], "nearest_works": [], "explicit_no_near_work_reason": "", "strongest_baseline_judgment": {"status": "unknown", "baseline_name": "", "source_work_id": "", "why_strongest": "", "kill_condition": "", "implementation_feasibility": "unknown"}, "known_overlap_risk": "unknown", "remaining_delta": "", "reason": "", "limitations": "", "risk_acceptance": "", "cannot_weaken": ["deepseek_success_required"]}],
            },
            state="manual_prior_art_template_written",
        )
        self.assertEqual(completed_review_by_candidate(RUN_DATE), {})
