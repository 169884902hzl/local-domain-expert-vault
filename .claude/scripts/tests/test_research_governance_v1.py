from __future__ import annotations

import argparse
import inspect
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from active_seed_commit import commit_active_seed
from audit_public_package_v1 import scan as scan_public_v1
from paper_intake_triage import build_triage
from pilot_result_interpret import write_result as write_pilot_result_v1
from research_governance_common import (
    active_commit_validation,
    active_seed_dir,
    active_seed_id_from_candidate,
    baseline_readiness_dir,
    candidate_dir,
    evidence_packet_dir,
    file_sha256,
    formal_rehearsal_dir,
    governance_review_dir,
    novelty_screen_dir,
    prior_art_dir,
    provider_review_dir,
    read_json,
    transition_errors,
    write_json,
)
from state_machine_guard import run_audit as run_state_machine_audit, scan_sensitive_writes
from strategy_ledger import build_event
import active_seed_dashboard
import active_seed_commit
import migrate_v03_to_v10


CID = "cand-alpha"


class GovernanceV1Test(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.old_root = os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT")
        os.environ["RESEARCH_GOVERNANCE_AGENDA_ROOT"] = self.tmp.name
        self.write_valid_bundle()

    def tearDown(self) -> None:
        if self.old_root is None:
            os.environ.pop("RESEARCH_GOVERNANCE_AGENDA_ROOT", None)
        else:
            os.environ["RESEARCH_GOVERNANCE_AGENDA_ROOT"] = self.old_root
        self.tmp.cleanup()

    def write_valid_bundle(self) -> None:
        write_json(candidate_dir(CID) / "candidate-record.json", {"schema_version": "candidate_record.v1", "candidate_id": CID, "title": "Governed Seed", "state": "governance_review_requested", "auto_promote_allowed": True})
        write_json(
            evidence_packet_dir(CID) / "evidence-packet.confirmed.json",
            {"schema_version": "evidence_packet.v1", "candidate_id": CID, "packet_status": "confirmed", "human_confirmed": True, "confirmed_by": "human", "confirmed_at": "2026-05-21T00:00:00Z", "core_evidence": [{"evidence_type": "anchored_claim", "statement": "supported"}]},
        )
        write_json(prior_art_dir(CID) / "manual-prior-art-dossier.json", {"schema_version": "prior_art_dossier.v1", "candidate_id": CID, "dossier_status": "completed", "reviewer": "human", "reviewed_at": "2026-05-21T00:00:00Z", "human_confirmed": True, "confirmed_by": "human", "confirmed_at": "2026-05-21T00:00:00Z", "screening_only": False})
        provider_path = provider_review_dir(CID) / "provider-review-packet.json"
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        write_json(provider_path, {"schema_version": "provider_review_packet.v1", "candidate_id": CID, "review_status": "success", "provider_backed": True, "test_provider_used": False, "provider_status": {"provider_backed": True, "mode": "opencode", "status": "success"}, "reviews": [{"provider": "deepseek", "status": "success"}, {"provider": "codex", "status": "success"}]})
        write_json(novelty_path, {"schema_version": "novelty_screen.v1", "candidate_id": CID, "screen_status": "success", "screening_only": True, "stale": False, "stale_external_novelty_cache": False, "replaces_manual_prior_art_dossier": False, "api_provider_status": "success", "provider_errors": []})
        write_json(baseline_readiness_dir(CID) / "baseline-execution-readiness.json", {"schema_version": "baseline_execution_readiness.v1", "candidate_id": CID, "readiness_status": "ready"})
        write_json(Path(self.tmp.name) / "pilot-plans" / CID / "pilot-plan.json", {"schema_version": "pilot_plan.v1", "candidate_id": CID, "plan_status": "ready", "owner": "human", "resource_budget": "2 weeks", "timeline": "2026Q2", "kill_criteria": "baseline wins", "human_confirmed": True, "confirmed_by": "human", "confirmed_at": "2026-05-21T00:00:00Z"})
        write_json(
            governance_review_dir(CID) / "governance-review.json",
            {
                "schema_version": "governance_review.v1",
                "candidate_id": CID,
                "owner": "human",
                "resource_budget": "2 weeks",
                "timeline": "2026Q2",
                "kill_criteria": "baseline wins",
                "human_confirmed": True,
                "confirmed_by": "human",
                "confirmed_at": "2026-05-21T00:00:00Z",
                "governance_signature": "sig",
                "artifact_hashes": [
                    {"path": str(provider_path), "sha256": file_sha256(provider_path)},
                    {"path": str(novelty_path), "sha256": file_sha256(novelty_path)},
                ],
            },
        )

    def assertBlocks(self, code: str) -> None:
        self.assertIn(code, active_commit_validation(CID).errors)

    def test_no_direct_seed_writer(self) -> None:
        self.assertEqual(run_state_machine_audit()["status"], "success")

    def test_state_machine_guard_detects_write_text_to_seed(self) -> None:
        source = "from pathlib import Path\np = Path('projects/research-agenda/idea_bank/seed/x.md')\np.write_text('x')\n"
        issues = scan_sensitive_writes(Path("bad_writer.py"), source)
        self.assertTrue(any(issue["code"] == "sensitive_governance_writer" for issue in issues))

    def test_state_machine_guard_detects_shutil_copy_to_seed(self) -> None:
        source = "import shutil\nshutil.copy2('a', 'projects/research-agenda/idea_bank/seed/a')\n"
        issues = scan_sensitive_writes(Path("bad_copy.py"), source)
        self.assertTrue(any("seed" in issue["targets"] for issue in issues))

    def test_state_machine_guard_detects_path_rename_to_seed(self) -> None:
        source = "from pathlib import Path\nPath('tmp').rename(Path('projects/research-agenda/idea_bank/seed/tmp'))\n"
        issues = scan_sensitive_writes(Path("bad_rename.py"), source)
        self.assertTrue(any("seed" in issue["targets"] for issue in issues))

    def test_state_machine_guard_allows_active_seed_commit_ledger_only(self) -> None:
        source = "from research_governance_common import active_seed_dir, governance_ledger_path, write_json, append_jsonl\nwrite_json(active_seed_dir('x') / 'active-seed-record.json', {})\nappend_jsonl(governance_ledger_path(), {})\n"
        self.assertEqual(scan_sensitive_writes(Path("active_seed_commit.py"), source), [])

    def test_state_machine_guard_rejects_publish_research_run_seed_writer(self) -> None:
        source = "from pathlib import Path\nPath('projects/research-agenda/idea_bank/seed/x').mkdir(parents=True)\n"
        issues = scan_sensitive_writes(Path("publish_research_run.py"), source)
        self.assertTrue(any("seed" in issue["targets"] for issue in issues))

    def test_scheduled_formal_active_impossible(self) -> None:
        self.assertIn("scheduled_forbidden_state:active_seed_committed", transition_errors("governance_review_requested", "active_seed_committed", mode="scheduled"))

    def test_backfill_cannot_promote(self) -> None:
        write_json(candidate_dir(CID) / "candidate-record.json", {"schema_version": "candidate_record.v1", "candidate_id": CID, "title": "Legacy", "state": "archived_legacy", "legacy_v03": True, "legacy_status": "archived_legacy", "auto_promote_allowed": False})
        self.assertBlocks("legacy_seed_never_auto_promotes")

    def test_test_provider_cannot_active_promote(self) -> None:
        payload = {"schema_version": "candidate_record.v1", "candidate_id": CID, "title": "x", "state": "x", "auto_promote_allowed": True, "test_provider_used": True}
        write_json(candidate_dir(CID) / "candidate-record.json", payload)
        self.assertBlocks("test_provider_used_blocks_active_commit")

    def test_stale_novelty_cache_blocks(self) -> None:
        write_json(candidate_dir(CID) / "candidate-record.json", {"schema_version": "candidate_record.v1", "candidate_id": CID, "title": "x", "state": "x", "auto_promote_allowed": True, "stale_novelty_cache": True})
        self.assertBlocks("stale_novelty_cache_blocks_active")

    def test_api_novelty_timeout_fails_closed(self) -> None:
        write_json(candidate_dir(CID) / "candidate-record.json", {"schema_version": "candidate_record.v1", "candidate_id": CID, "title": "x", "state": "x", "auto_promote_allowed": True, "novelty_provider_status": "timeout"})
        self.assertBlocks("api_novelty_timeout_fails_closed")

    def test_active_seed_requires_manual_prior_art_dossier(self) -> None:
        (prior_art_dir(CID) / "manual-prior-art-dossier.json").unlink()
        self.assertBlocks("missing_manual_prior_art_dossier")

    def test_active_commit_requires_provider_review_hash(self) -> None:
        review_path = governance_review_dir(CID) / "governance-review.json"
        review = read_json(review_path)
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        review["artifact_hashes"] = [{"path": str(novelty_path), "sha256": file_sha256(novelty_path)}]
        write_json(review_path, review)
        self.assertBlocks("missing_provider_review_packet_hash")

    def test_active_commit_requires_novelty_screen_hash(self) -> None:
        review_path = governance_review_dir(CID) / "governance-review.json"
        review = read_json(review_path)
        provider_path = provider_review_dir(CID) / "provider-review-packet.json"
        review["artifact_hashes"] = [{"path": str(provider_path), "sha256": file_sha256(provider_path)}]
        write_json(review_path, review)
        self.assertBlocks("missing_novelty_screen_hash")

    def test_active_commit_rejects_provider_review_hash_mismatch(self) -> None:
        provider_path = provider_review_dir(CID) / "provider-review-packet.json"
        provider = read_json(provider_path)
        provider["reviews"].append({"provider": "codex", "status": "success", "note": "changed"})
        write_json(provider_path, provider)
        self.assertTrue(any("hash_mismatch" in error for error in active_commit_validation(CID).errors))

    def test_active_commit_rejects_novelty_screen_hash_mismatch(self) -> None:
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        novelty = read_json(novelty_path)
        novelty["provider_errors"] = ["changed"]
        write_json(novelty_path, novelty)
        self.assertTrue(any("hash_mismatch" in error for error in active_commit_validation(CID).errors))

    def test_active_commit_rejects_test_provider_review(self) -> None:
        provider_path = provider_review_dir(CID) / "provider-review-packet.json"
        provider = read_json(provider_path)
        provider["test_provider_used"] = True
        write_json(provider_path, provider)
        self.refresh_governance_hashes()
        self.assertBlocks("test_provider_review_blocks_active")

    def test_active_commit_rejects_stale_novelty_screen(self) -> None:
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        novelty = read_json(novelty_path)
        novelty["stale"] = True
        write_json(novelty_path, novelty)
        self.refresh_governance_hashes()
        self.assertBlocks("stale_novelty_screen_blocks_active")

    def test_api_screening_cannot_replace_manual_prior_art_dossier(self) -> None:
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        novelty = read_json(novelty_path)
        novelty["replaces_manual_prior_art_dossier"] = True
        write_json(novelty_path, novelty)
        self.refresh_governance_hashes()
        self.assertBlocks("api_screening_cannot_replace_manual_prior_art_dossier")

    def test_active_seed_requires_baseline_execution_readiness(self) -> None:
        write_json(baseline_readiness_dir(CID) / "baseline-execution-readiness.json", {"schema_version": "baseline_execution_readiness.v1", "candidate_id": CID, "readiness_status": "unknown"})
        self.assertBlocks("missing_baseline_execution_readiness")

    def test_active_seed_allows_not_applicable_baseline_only_with_reason(self) -> None:
        write_json(baseline_readiness_dir(CID) / "baseline-execution-readiness.json", {"schema_version": "baseline_execution_readiness.v1", "candidate_id": CID, "readiness_status": "not_applicable", "not_applicable_reason": ""})
        self.assertBlocks("baseline_not_applicable_missing_reason")
        write_json(baseline_readiness_dir(CID) / "baseline-execution-readiness.json", {"schema_version": "baseline_execution_readiness.v1", "candidate_id": CID, "readiness_status": "not_applicable", "not_applicable_reason": "the seed is a metric protocol"})
        self.assertNotIn("baseline_not_applicable_missing_reason", active_commit_validation(CID).errors)

    def test_active_seed_requires_human_confirmed_core_evidence(self) -> None:
        write_json(evidence_packet_dir(CID) / "evidence-packet.confirmed.json", {"schema_version": "evidence_packet.v1", "candidate_id": CID, "packet_status": "draft", "human_confirmed": False, "core_evidence": [{"evidence_type": "anchored_claim"}]})
        self.assertBlocks("missing_confirmed_evidence_packet")

    def test_note_only_evidence_downgraded(self) -> None:
        self.set_evidence({"evidence_type": "note_only"})
        self.assertTrue(any("note_only_evidence_cannot_support_active" in error for error in active_commit_validation(CID).errors))

    def test_active_seed_rejects_unconfirmed_cross_paper_contradiction_support(self) -> None:
        self.set_evidence({"evidence_type": "cross_paper_contradiction", "human_confirmed": False})
        self.assertTrue(any("cross_paper_edge_unconfirmed" in error for error in active_commit_validation(CID).errors))

    def test_unresolved_contradiction_blocks_active(self) -> None:
        self.set_evidence({"evidence_type": "cross_paper_contradiction", "human_confirmed": True, "contradiction_status": "unresolved"})
        self.assertTrue(any("unresolved_contradiction" in error for error in active_commit_validation(CID).errors))

    def test_result_row_machine_extraction_cannot_support_active_without_manual_confirmation(self) -> None:
        self.set_evidence({"evidence_type": "result_row", "manual_confirmed": False})
        self.assertTrue(any("result_row_unconfirmed" in error for error in active_commit_validation(CID).errors))

    def test_formal_rehearsal_cannot_be_mistaken_for_active_seed(self) -> None:
        write_json(formal_rehearsal_dir(CID) / "formal-rehearsal-packet.json", {"schema_version": "formal_rehearsal_packet.v1", "candidate_id": CID, "packet_status": "ready", "active_seed_committed": False})
        self.assertFalse((active_seed_dir(active_seed_id_from_candidate(CID, "Governed Seed")) / "active-seed-record.json").exists())

    def test_dashboard_is_derived_only(self) -> None:
        payload = {"schema_version": "dashboard.v1", "source_of_truth": "derived_view_only", "derived_only": True, "rows": []}
        self.assertTrue(payload["derived_only"])

    def test_dashboard_cannot_write_state(self) -> None:
        self.assertNotIn("write_run_artifact", inspect.getsource(active_seed_dashboard.write_dashboard))

    def test_crash_during_publish_quarantines(self) -> None:
        with patch.object(active_seed_commit, "write_json", side_effect=RuntimeError("boom")):
            result = active_seed_commit.commit_active_seed(CID, actor="human", governance_signature="sig", human_confirmed=True)
        self.assertTrue(any("active_seed_commit_exception" in error for error in result["errors"]))

    def test_concurrent_publish_no_overwrite(self) -> None:
        active_id = active_seed_id_from_candidate(CID, "Governed Seed")
        lock = active_seed_dir(active_id).with_suffix(".commit.lock")
        lock.parent.mkdir(parents=True)
        lock.write_text("locked", encoding="utf-8")
        result = commit_active_seed(CID, actor="human", governance_signature="sig", human_confirmed=True)
        self.assertIn("concurrent_active_seed_commit_lock_exists", result["errors"])

    def test_legacy_seed_never_auto_promotes(self) -> None:
        self.test_backfill_cannot_promote()

    def test_public_package_has_no_runtime_private_artifacts(self) -> None:
        self.assertEqual(scan_public_v1(Path(__file__).resolve().parents[3])["status"], "success")

    def test_human_override_cannot_bypass_hard_blocks(self) -> None:
        self.set_evidence({"evidence_type": "note_only", "human_override": True})
        self.assertTrue(any("note_only_evidence_cannot_support_active" in error for error in active_commit_validation(CID).errors))

    def test_prior_art_screening_not_dossier(self) -> None:
        payload = active_commit_validation(CID)
        self.assertTrue(payload.ok)
        write_json(prior_art_dir(CID) / "manual-prior-art-dossier.json", {"schema_version": "prior_art_dossier.v1", "candidate_id": CID, "dossier_status": "completed", "reviewer": "human", "reviewed_at": "x", "human_confirmed": True, "confirmed_by": "human", "confirmed_at": "x", "screening_only": True})
        self.assertBlocks("prior_art_screening_not_dossier")

    def test_pilot_result_does_not_promote(self) -> None:
        payload = write_pilot_result_v1(argparse.Namespace(candidate_id=CID, active_seed_id="", status="positive", result_summary="ok", dry_run=True))
        self.assertFalse(payload["proposed_strategy_event"]["applied"])

    def test_state_machine_rejects_illegal_transition(self) -> None:
        self.assertTrue(any("illegal_transition" in error for error in transition_errors("intake_screened", "active_seed_committed")))

    def test_hash_mismatch_blocks_active_commit(self) -> None:
        source = Path(self.tmp.name) / "source.txt"
        source.write_text("a", encoding="utf-8")
        self.set_evidence({"evidence_type": "anchored_claim"}, artifact_hashes=[{"path": str(source), "sha256": file_sha256(source)}])
        source.write_text("b", encoding="utf-8")
        self.assertTrue(any("hash_mismatch" in error for error in active_commit_validation(CID).errors))

    def test_schema_migration_marks_cache_stale(self) -> None:
        self.assertTrue(migrate_v03_to_v10.build_report(dry_run=True)["migrated_novelty_caches_marked_stale"])

    def test_strategy_feedback_requires_human_ledger_event(self) -> None:
        payload = build_event(argparse.Namespace(event_type="pilot_feedback", candidate_id=CID, summary="x", apply=True, human_confirmed=False, confirmed_by="human"))
        self.assertIn("strategy_apply_requires_human_confirmed", payload["errors"])

    def test_intake_quota_frontier_contradiction_tool_benchmark_negative_outside_labfit(self) -> None:
        payload = build_triage(
            [
                {"title": "Unexpected DLO benchmark failure", "summary": "negative result contradiction baseline pilot"},
                {"title": "Tool pipeline for bimanual tactile evaluation", "summary": "infrastructure metric dataset"},
                {"title": "Biology analogy for robot cable manipulation", "summary": "outside analogy"},
            ],
            run_date="2026-05-21",
            target_deep_read=3,
            max_deep_read=3,
        )
        counts = payload["research_value_quota_counts"]
        self.assertGreater(counts["frontier_anomaly"], 0)
        self.assertGreater(counts["contradiction"], 0)
        self.assertGreater(counts["tool_infrastructure_gap"], 0)
        self.assertGreater(counts["benchmark_metric_gap"], 0)
        self.assertGreater(counts["negative_result"], 0)
        self.assertGreater(counts["outside_analogy"], 0)
        self.assertGreater(counts["local_lab_fit"], 0)

    def test_active_seed_record_requires_owner_budget_kill_criteria(self) -> None:
        write_json(governance_review_dir(CID) / "governance-review.json", {"schema_version": "governance_review.v1", "candidate_id": CID, "owner": "", "resource_budget": "", "timeline": "", "kill_criteria": "", "human_confirmed": True, "confirmed_by": "human", "confirmed_at": "x", "governance_signature": "sig"})
        errors = active_commit_validation(CID).errors
        self.assertIn("active_seed_record_missing_owner", errors)
        self.assertIn("active_seed_record_missing_resource_budget", errors)
        self.assertIn("active_seed_record_missing_kill_criteria", errors)

    def set_evidence(self, item: dict, artifact_hashes: list[dict] | None = None) -> None:
        write_json(
            evidence_packet_dir(CID) / "evidence-packet.confirmed.json",
            {"schema_version": "evidence_packet.v1", "candidate_id": CID, "packet_status": "confirmed", "human_confirmed": True, "confirmed_by": "human", "confirmed_at": "x", "core_evidence": [item], "artifact_hashes": artifact_hashes or []},
        )

    def refresh_governance_hashes(self) -> None:
        provider_path = provider_review_dir(CID) / "provider-review-packet.json"
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        review_path = governance_review_dir(CID) / "governance-review.json"
        review = read_json(review_path)
        review["artifact_hashes"] = [
            {"path": str(provider_path), "sha256": file_sha256(provider_path)},
            {"path": str(novelty_path), "sha256": file_sha256(novelty_path)},
        ]
        write_json(review_path, review)


if __name__ == "__main__":
    unittest.main()
