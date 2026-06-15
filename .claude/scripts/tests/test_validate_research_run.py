from __future__ import annotations

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from research_seed_v2_common import artifact_dir, read_json, write_json, write_run_artifact
from survival_decision import decide
from validate_research_run import validate_run


class ValidateResearchRunTest(V03TempAgendaTest):
    def write_survival_decision(self) -> None:
        write_run_artifact(
            RUN_DATE,
            "survival-decision.json",
            decide(run_date=RUN_DATE, allow_human_override=False, target_policy="seed-candidates-only"),
            state="survival_decided",
        )

    def test_stored_candidate_id_is_used_after_content_changes(self) -> None:
        self.write_base_reviews()
        self.write_survival_decision()
        path = artifact_dir(RUN_DATE) / "selected-candidates.json"
        payload = read_json(path)
        payload["selected"][0]["problem"] = "Changed by a refinement pass after the candidate id was assigned."
        write_json(path, payload)
        errors = validate_run(RUN_DATE)["errors"]
        self.assertFalse([item for item in errors if item.startswith("candidate_alignment:")], errors)

    def test_missing_stored_candidate_id_is_reported_explicitly(self) -> None:
        self.write_base_reviews()
        self.write_survival_decision()
        path = artifact_dir(RUN_DATE) / "selected-candidates.json"
        payload = read_json(path)
        payload["selected"][0].pop("candidate_id")
        write_json(path, payload)
        errors = validate_run(RUN_DATE)["errors"]
        self.assertTrue(any(item.startswith("candidate_alignment:selected_candidates:stored_candidate_id_missing:") for item in errors), errors)
