from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from prepare_experiment_for_candidate import prepare_candidate
from research_governance_common import (
    active_commit_validation,
    baseline_readiness_dir,
    evidence_packet_dir,
    file_sha256,
    governance_review_dir,
    novelty_screen_dir,
    pilot_plan_dir,
    prior_art_dir,
    provider_review_dir,
    write_json,
)


CID = "cand-alpha"


class GovernanceBootstrapChainTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self._saved = {k: os.environ.get(k) for k in ("RESEARCH_GOVERNANCE_AGENDA_ROOT", "RESEARCH_SEED_V2_AGENDA_ROOT")}
        os.environ["RESEARCH_GOVERNANCE_AGENDA_ROOT"] = self.tmp.name
        os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.tmp.name
        self.accepted_path = Path(self.tmp.name) / "accepted.json"
        self.accepted_path.write_text(
            json.dumps(
                {
                    "schema_version": "research_seed_bucket_item.v1",
                    "run_date": "2099-03-04",
                    "candidate_id": CID,
                    "candidate": {
                        "candidate_id": CID,
                        "title": "Accepted Candidate",
                        "problem": "DLO contact failure",
                        "mechanism": "Tactile recovery trigger",
                        "evidence": [{"claim_type": "anchored_claim", "statement": "Supported by a local note.", "source_note": "wiki/topics/example.md"}],
                    },
                    "survival_decision": {"candidate_id": CID, "candidate_title": "Accepted Candidate"},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.tmp.cleanup()

    def args(self) -> argparse.Namespace:
        return argparse.Namespace(
            candidate_id="",
            from_accepted=str(self.accepted_path),
            human_initiated=True,
            run_id="run-1",
            limit=12,
            output="",
            owner="human",
            resource_budget="2 weeks",
            timeline="2099Q1",
            metric="success_rate",
            baseline_implementation_path="baselines/baseline",
            kill_criteria="baseline wins",
            dry_run=False,
        )

    def write_confirmed_bundle(self) -> None:
        provider_path = provider_review_dir(CID) / "provider-review-packet.json"
        novelty_path = novelty_screen_dir(CID) / "novelty-screen.json"
        write_json(
            evidence_packet_dir(CID) / "evidence-packet.confirmed.json",
            {
                "schema_version": "evidence_packet.v1",
                "candidate_id": CID,
                "run_id": "run-1",
                "packet_status": "confirmed",
                "created_at": "2099-03-04T00:00:00Z",
                "human_confirmed": True,
                "confirmed_by": "human",
                "confirmed_at": "2099-03-04T00:00:00Z",
                "core_evidence": [{"evidence_type": "anchored_claim", "statement": "supported"}],
                "artifact_hashes": [],
                "boundary": "test fixture",
            },
        )
        write_json(
            prior_art_dir(CID) / "manual-prior-art-dossier.json",
            {
                "schema_version": "prior_art_dossier.v1",
                "candidate_id": CID,
                "dossier_status": "completed",
                "reviewer": "human",
                "reviewed_at": "2099-03-04T00:00:00Z",
                "human_confirmed": True,
                "confirmed_by": "human",
                "confirmed_at": "2099-03-04T00:00:00Z",
                "screening_only": False,
                "manual_sources": ["manual:fixture"],
                "nearest_work_summary": "Nearest work checked manually.",
                "provider_timeout_seen": False,
                "timeout_covered_by_manual_dossier": False,
                "boundary": "test fixture",
            },
        )
        write_json(
            provider_path,
            {
                "schema_version": "provider_review_packet.v1",
                "candidate_id": CID,
                "review_status": "success",
                "provider_backed": True,
                "test_provider_used": False,
                "generated_by_script": "provider_review_packet.py",
                "source_run_id": "run-1",
                "provider_mode": "opencode+codex-cli",
                "provider_status": {"provider": "combined", "provider_backed": True, "mode": "opencode+codex-cli", "status": "success"},
                "command_hash": "sha256:command",
                "provider_log_hash": "sha256:provider-log",
                "created_at": "2099-03-04T00:00:00Z",
                "reviews": [{"provider": "deepseek", "status": "success"}, {"provider": "codex", "status": "success"}],
                "artifact_hashes": [],
            },
        )
        write_json(
            novelty_path,
            {
                "schema_version": "novelty_screen.v1",
                "candidate_id": CID,
                "screen_status": "success",
                "screening_only": True,
                "stale": False,
                "stale_external_novelty_cache": False,
                "replaces_manual_prior_art_dossier": False,
                "api_provider_status": "success",
                "provider_errors": [],
                "artifact_hashes": [],
            },
        )
        write_json(
            baseline_readiness_dir(CID) / "baseline-execution-readiness.json",
            {
                "schema_version": "baseline_execution_readiness.v1",
                "candidate_id": CID,
                "readiness_status": "ready",
                "baseline_name": "baseline",
                "implementation_path": "baselines/baseline",
                "resource_budget": "2 weeks",
                "not_applicable_reason": "",
                "blocking_issues": [],
                "created_at": "2099-03-04T00:00:00Z",
                "boundary": "test fixture",
            },
        )
        write_json(
            pilot_plan_dir(CID) / "pilot-plan.json",
            {
                "schema_version": "pilot_plan.v1",
                "candidate_id": CID,
                "plan_status": "ready",
                "owner": "human",
                "resource_budget": "2 weeks",
                "timeline": "2099Q1",
                "metric": "success_rate",
                "baseline_implementation_path": "baselines/baseline",
                "kill_criteria": "baseline wins",
                "human_confirmed": True,
                "confirmed_by": "human",
                "confirmed_at": "2099-03-04T00:00:00Z",
                "created_at": "2099-03-04T00:00:00Z",
                "boundary": "test fixture",
            },
        )
        write_json(
            governance_review_dir(CID) / "governance-review.json",
            {
                "schema_version": "governance_review.v1",
                "candidate_id": CID,
                "title": "Accepted Candidate",
                "review_status": "requested",
                "owner": "human",
                "resource_budget": "2 weeks",
                "timeline": "2099Q1",
                "kill_criteria": "baseline wins",
                "human_confirmed": True,
                "confirmed_by": "human",
                "confirmed_at": "2099-03-04T00:00:00Z",
                "reviewer": "human",
                "reviewed_at": "2099-03-04T00:00:00Z",
                "governance_signature": "sig",
                "created_at": "2099-03-04T00:00:00Z",
                "artifact_hashes": [
                    {"path": str(provider_path), "sha256": file_sha256(provider_path)},
                    {"path": str(novelty_path), "sha256": file_sha256(novelty_path)},
                ],
                "boundary": "test fixture",
            },
        )

    def test_prepare_chain_stops_at_draft_then_manual_bundle_can_pass(self) -> None:
        offline_scan = {"status": "completed_local_only", "external_providers_used": [], "provider_errors": [{"provider": "openalex", "error": "mocked offline"}], "stale_external_novelty_cache": False}
        with patch(
            "prepare_experiment_for_candidate.plan_experiment.plan_from_query",
            return_value={"status": "success", "path": "projects/experiments/test.md", "audit": {"status": "PASS"}, "evidence_level": "strong", "evidence_gaps": []},
        ), patch("novelty_screen._build_candidate_scan", return_value=offline_scan):
            result = prepare_candidate(self.args())
        self.assertEqual(result["status"], "draft_prepared")
        self.assertFalse(result["active_commit_validation_ok"])
        self.assertEqual(result["pilot_plan_status"], "draft")
        self.assertEqual(result["provider_review_status"], "blocked")
        self.assertIn(result["novelty_screen_status"], {"blocked", "provider_unavailable", "partial_provider_unavailable"})
        self.assertFalse(active_commit_validation(CID).ok)

        self.write_confirmed_bundle()
        self.assertTrue(active_commit_validation(CID).ok)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
