from __future__ import annotations

from pathlib import Path

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from active_seed_dashboard import build_accepted_backlog, build_dashboard, write_accepted_backlog, write_dashboard
from publish_research_run import publish
from research_seed_v2_common import artifact_dir, read_json, write_json, write_run_artifact
from research_governance_common import pilot_plan_dir
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
        result = publish(RUN_DATE, dry_run=True, target_policy="formal")
        self.assertEqual(result["status"], "legacy_formal_publish_disabled_use_formal_rehearsal_packet")
        self.assertEqual(result["published"], [])
        self.assertIn("v1_disables_legacy_formal_seed_writing", result["blocked"])
        survival_after = read_json(artifact_dir(RUN_DATE) / "survival-decision.json")
        self.assertFalse(survival_after["decisions"][0]["active_seed_allowed"])

    def test_accepted_backlog_is_derived_only(self) -> None:
        accepted_dir = Path(self.tmp.name) / "seed-candidates" / "accepted" / RUN_DATE
        for index in range(2):
            cid = f"cand-accepted-{index}"
            write_json(
                accepted_dir / f"{cid}.json",
                {
                    "schema_version": "research_seed_bucket_item.v1",
                    "run_date": RUN_DATE,
                    "candidate_id": cid,
                    "candidate": {"candidate_id": cid, "title": f"Accepted {index}"},
                    "survival_decision": {
                        "candidate_id": cid,
                        "candidate_title": f"Accepted {index}",
                        "decision": "accept_for_user_review",
                        "risks": ["manual_prior_art_review_missing", "baseline_table_missing"],
                        "blocks": [],
                        "formal_rehearsal_allowed": False,
                        "active_seed_allowed": False,
                        "pilot_ready_allowed": False,
                    },
                },
            )
        payload = write_accepted_backlog()
        self.assertEqual(payload["source_of_truth"], "derived_view_only")
        self.assertEqual(len(payload["rows"]), 2)
        self.assertTrue(all(row["active_seed_allowed"] is False for row in payload["rows"]))
        self.assertTrue((Path(self.tmp.name) / "dashboard" / "accepted-backlog.json").exists())

    def test_dashboard_reads_v1_pilot_plan_path(self) -> None:
        self.write_base_reviews(stale_cache=True)
        self.write_manual_review()
        self.write_baseline_table(execution_status="partial")
        write_json(
            pilot_plan_dir("cand-alpha") / "pilot-plan.json",
            {
                "schema_version": "pilot_plan.v1",
                "candidate_id": "cand-alpha",
                "plan_status": "draft",
                "owner": "human",
                "resource_budget": "one GPU day",
                "timeline": "2099Q1",
                "metric": "failure_detection_auc",
                "baseline_implementation_path": "baselines/diffusion-policy-threshold",
                "kill_criteria": "baseline wins",
                "human_confirmed": False,
                "confirmed_by": "",
                "confirmed_at": "",
                "created_at": "2099-03-04T00:00:00Z",
                "boundary": "test fixture",
            },
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        payload = build_dashboard(RUN_DATE)
        self.assertEqual(payload["rows"][0]["pilot_plan_status"], "draft")
