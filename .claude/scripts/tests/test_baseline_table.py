from __future__ import annotations

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from baseline_table import baseline_allows_active_seed, baseline_execution_status, build_baseline_table, load_baseline_tables


class BaselineTableTest(V03TempAgendaTest):
    def test_nearest_work_not_equal_strongest_baseline(self) -> None:
        self.write_base_reviews()
        table = build_baseline_table(RUN_DATE, self.candidate())
        roles = {item["baseline_role"] for item in table["baselines"]}
        self.assertIn("nearest_work", roles)
        self.assertEqual(table["strongest_baseline_final"]["status"], "unknown")
        self.assertFalse(baseline_allows_active_seed(table))

    def test_manual_prior_art_confirms_strongest_baseline(self) -> None:
        self.write_base_reviews()
        self.write_manual_review()
        table = build_baseline_table(RUN_DATE, self.candidate())
        self.assertEqual(table["strongest_baseline_final"]["status"], "known")
        self.assertEqual(table["strongest_baseline_final"]["source"], "manual_prior_art_review")
        self.assertEqual(baseline_execution_status(table), "ready")
        self.assertTrue(baseline_allows_active_seed(table))

    def test_codex_feasibility_enters_baseline_table(self) -> None:
        self.write_base_reviews()
        table = build_baseline_table(RUN_DATE, self.candidate())
        codex_items = [item for item in table["baselines"] if item["baseline_role"] == "codex_feasibility_baseline"]
        self.assertEqual(len(codex_items), 1)
        self.assertEqual(codex_items[0]["implementation_feasibility"], "available")
        self.assertIn("single GPU day", codex_items[0]["known_result"])

    def test_unknown_strongest_baseline_blocks_active_seed(self) -> None:
        self.write_baseline_table(known=False)
        table = load_baseline_tables(RUN_DATE)["cand-alpha"]
        self.assertFalse(baseline_allows_active_seed(table))

    def test_multi_candidate_wrapper_loads_per_candidate_tables(self) -> None:
        self.write_multi_baseline_table(candidate_ids=("cand-alpha", "cand-beta"))
        tables = load_baseline_tables(RUN_DATE)
        self.assertEqual(set(tables), {"cand-alpha", "cand-beta"})
        self.assertNotIn("__multi__", tables)

    def test_unknown_or_prohibitive_execution_blocks_active_seed(self) -> None:
        for status in ["unknown", "prohibitive", "partial"]:
            with self.subTest(status=status):
                self.tearDown()
                self.setUp()
                self.write_baseline_table(execution_status=status)
                table = load_baseline_tables(RUN_DATE)["cand-alpha"]
                self.assertEqual(baseline_execution_status(table), status)
                self.assertFalse(baseline_allows_active_seed(table))

    def test_not_applicable_execution_requires_reason_and_allows_active_seed(self) -> None:
        self.write_baseline_table(execution_status="not_applicable")
        table = load_baseline_tables(RUN_DATE)["cand-alpha"]
        self.assertEqual(baseline_execution_status(table), "not_applicable")
        self.assertTrue(baseline_allows_active_seed(table))
