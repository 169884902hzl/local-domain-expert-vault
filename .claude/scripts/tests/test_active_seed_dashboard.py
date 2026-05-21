from __future__ import annotations

from pathlib import Path

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from active_seed_dashboard import build_dashboard, write_dashboard
from publish_research_run import publish
from research_seed_v2_common import artifact_dir, read_json, write_json, write_run_artifact
from survival_decision import decide


class ActiveSeedDashboardTest(V03TempAgendaTest):
    def test_dashboard_is_derived_run_artifact_and_latest_view(self) -> None:
        self.write_base_reviews(stale_cache=True)
        self.write_manual_review()
        self.write_baseline_table(execution_status="partial")
        self.write_pilot_plan()
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        payload = write_dashboard(RUN_DATE)
        row = payload["rows"][0]
        self.assertEqual(payload["source_of_truth"], "derived_view_only")
        self.assertFalse(row["active_seed_allowed"])
        self.assertEqual(row["novelty_cache_status"], "stale")
        self.assertEqual(row["baseline_execution_status"], "partial")
        self.assertTrue((artifact_dir(RUN_DATE) / "active-seed-dashboard.json").exists())
        self.assertTrue((Path(self.tmp.name) / "dashboard" / "active-seed-dashboard.json").exists())

    def test_dashboard_failure_does_not_relax_survival_or_publish(self) -> None:
        self.write_base_reviews(stale_cache=False)
        self.write_manual_review()
        self.write_baseline_table(execution_status="unknown")
        self.write_pilot_plan()
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        dashboard = build_dashboard(RUN_DATE)
        dashboard["rows"][0]["active_seed_allowed"] = True
        write_json(artifact_dir(RUN_DATE) / "active-seed-dashboard.json", dashboard)
        result = publish(
            RUN_DATE,
            dry_run=True,
            target_policy="formal",
            allow_formal_seed_publish=True,
            allow_test_provider_for_formal=True,
        )
        self.assertNotEqual(result["status"], "success")
        self.assertTrue(any("active_seed_dashboard_mismatch" in item for item in result["blocked"]))
        survival_after = read_json(artifact_dir(RUN_DATE) / "survival-decision.json")
        self.assertFalse(survival_after["decisions"][0]["active_seed_allowed"])
