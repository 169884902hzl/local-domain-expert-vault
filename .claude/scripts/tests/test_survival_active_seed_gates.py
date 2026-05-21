from __future__ import annotations

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from research_seed_v2_common import write_run_artifact
from survival_decision import decide


class SurvivalActiveSeedGatesTest(V03TempAgendaTest):
    def _write_all_active_support(self) -> None:
        self.write_base_reviews()
        self.write_manual_review()
        self.write_baseline_table()
        self.write_pilot_plan()

    def test_candidate_without_result_row_is_not_blocked_by_result_confirmation(self) -> None:
        self._write_all_active_support()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertTrue(decision["governance_review_possible"])
        self.assertTrue(decision["requires_human_governance"])
        self.assertEqual(decision["publish_target"], "formal-rehearsal")
        self.assertNotIn("result_row_unconfirmed", decision["risks"])

    def test_unconfirmed_result_row_blocks_active_only_when_used_as_core_evidence(self) -> None:
        self.write_base_reviews()
        self.write_claim_graph_node(claim_type="actual_baseline_result", anchor_type="result_row", manual_confirmed=False)
        self.write_manual_review()
        self.write_baseline_table()
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertTrue(decision["formal_rehearsal_allowed"])
        self.assertIn("result_row_unconfirmed", decision["risks"])

    def test_confirmed_result_row_can_support_active_seed(self) -> None:
        self.write_base_reviews()
        self.write_claim_graph_node(claim_type="actual_baseline_result", anchor_type="result_row", manual_confirmed=True)
        self.write_manual_review()
        self.write_baseline_table()
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertTrue(decision["governance_review_possible"])
        self.assertTrue(decision["requires_human_governance"])
        self.assertEqual(decision["publish_target"], "formal-rehearsal")
        self.assertNotIn("result_row_unconfirmed", decision["risks"])

    def test_unconfirmed_cross_paper_edge_blocks_active_only_when_used_as_core_evidence(self) -> None:
        self.write_base_reviews()
        item = self.candidate()
        item["supporting_edges"] = ["edge-cross-1"]
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {"schema_version": "selected_candidates.v1", "run_date": RUN_DATE, "selected": [item], "rejected": [], "selection_rules": {}, "artifact_hashes": {}},
            state="portfolio_selected",
        )
        self.write_claim_graph_with_edge(edge_quality_status="requires_human_check", human_confirmed=False)
        self.write_manual_review()
        self.write_baseline_table()
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertIn("cross_paper_edge_requires_human_check", decision["risks"])

    def test_confirmed_cross_paper_edge_can_support_active_seed(self) -> None:
        self.write_base_reviews()
        item = self.candidate()
        item["supporting_edges"] = ["edge-cross-1"]
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {"schema_version": "selected_candidates.v1", "run_date": RUN_DATE, "selected": [item], "rejected": [], "selection_rules": {}, "artifact_hashes": {}},
            state="portfolio_selected",
        )
        self.write_claim_graph_with_edge(edge_quality_status="confirmed", human_confirmed=True)
        self.write_manual_review()
        self.write_baseline_table()
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertTrue(decision["governance_review_possible"])
        self.assertTrue(decision["requires_human_governance"])
        self.assertEqual(decision["publish_target"], "formal-rehearsal")
        self.assertNotIn("cross_paper_edge_requires_human_check", decision["risks"])

    def test_baseline_execution_partial_allows_rehearsal_but_blocks_active(self) -> None:
        self.write_base_reviews()
        self.write_manual_review()
        self.write_baseline_table(execution_status="partial")
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertTrue(decision["formal_rehearsal_allowed"])
        self.assertIn("baseline_execution_not_ready", decision["risks"])
