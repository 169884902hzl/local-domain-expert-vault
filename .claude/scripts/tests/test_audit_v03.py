from __future__ import annotations

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from audit_daily_automation_quality import _audit_v2_state_machine
from research_seed_v2_common import write_run_artifact


class AuditV03Test(V03TempAgendaTest):
    def test_audit_fails_active_seed_without_manual_prior_art(self) -> None:
        write_run_artifact(
            RUN_DATE,
            "survival-decision.json",
            {
                "schema_version": "survival_decision.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "target_policy": "formal",
                "decisions": [
                    {
                        "candidate_id": "cand-alpha",
                        "candidate_title": "Anchored Contact Failure Benchmark",
                        "decision": "accept_for_user_review",
                        "blocks": [],
                        "deepseek_label": "survives",
                        "novelty_classification": "likely_open",
                        "verification_scope": "local_plus_s2_or_openalex",
                        "external_providers_used": ["openalex"],
                        "codex_action": "accept_for_user_review",
                        "human_override_used": False,
                        "risks": ["manual_prior_art_review_missing"],
                        "active_seed_allowed": True,
                        "formal_rehearsal_allowed": True,
                        "pilot_ready_allowed": False,
                        "publish_target": "seed",
                    }
                ],
                "artifact_hashes": {},
            },
            state="survival_decided",
        )
        _summary, issues = _audit_v2_state_machine(RUN_DATE)
        self.assertTrue(any(item["code"] == "active_seed_without_manual_prior_art_review" and item["level"] == "FAIL" for item in issues))

    def test_audit_flags_stale_novelty_cache(self) -> None:
        self.write_base_reviews(stale_cache=True)
        _summary, issues = _audit_v2_state_machine(RUN_DATE)
        self.assertTrue(any(item["code"] == "stale_external_novelty_cache" for item in issues))
