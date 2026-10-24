from __future__ import annotations

import argparse
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from provider_review_packet import write_packet
from research_governance_common import (
    _provider_review_errors,
    provider_review_dir,
    validate_governance_payload,
    write_json,
)
from research_seed_v2_common import artifact_dir

RUN_DATE = "2026-06-13"


def _ns(**kw):
    base = dict(candidate_id="", run_date=RUN_DATE, run_id="", parent_candidate_id="", source_run_id="", validate=False, dry_run=False)
    base.update(kw)
    return argparse.Namespace(**base)


class ProviderReviewPacketTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self._saved = {k: os.environ.get(k) for k in ("RESEARCH_GOVERNANCE_AGENDA_ROOT", "RESEARCH_SEED_V2_AGENDA_ROOT")}
        os.environ["RESEARCH_GOVERNANCE_AGENDA_ROOT"] = self.tmp.name
        os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.tmp.name

    def tearDown(self) -> None:
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.tmp.cleanup()

    def _write_artifacts(self, *, ds_status="success", cx_status="success", ds_backed=True, cx_backed=True, timed_out=False, test_provider=False, cids=("cand-alpha",)) -> None:
        art = artifact_dir(RUN_DATE)
        ds_ps = {"provider": "deepseek", "provider_backed": ds_backed, "mode": "openai-compatible", "timed_out": timed_out}
        cx_ps = {"provider": "codex", "provider_backed": cx_backed, "mode": "codex-cli", "timed_out": timed_out}
        if test_provider:
            ds_ps["test_provider_used"] = True
        write_json(art / "deepseek-review.json", {"schema_version": "deepseek_review.v1", "run_date": RUN_DATE, "status": "success", "provider_status": ds_ps, "reviews": [{"candidate_id": c, "status": ds_status, "survivability_label": "survives", "allowed_next_stage": "novelty_scan", "a_plus_b_risk": "low"} for c in cids]})
        write_json(art / "codex-execution-review.json", {"schema_version": "codex_execution_review.v1", "run_date": RUN_DATE, "status": "success", "provider_status": cx_ps, "reviews": [{"candidate_id": c, "status": cx_status, "action": "accept_for_user_review", "confidence": "high"} for c in cids]})
        write_json(art.parent / "manifest.json", {"run_id": "2026-06-13-test"})

    def test_success_for_reviewed_candidate(self) -> None:
        self._write_artifacts(cids=("cand-alpha",))
        payload = write_packet(_ns(candidate_id="cand-alpha"))
        self.assertEqual(payload["review_status"], "success")
        self.assertTrue(payload["provider_backed"])
        self.assertEqual(len(payload["reviews"]), 2)
        self.assertEqual(validate_governance_payload(payload, "provider_review_packet.v1"), [])
        self.assertEqual(_provider_review_errors(payload), [])
        self.assertTrue((provider_review_dir("cand-alpha") / "provider-review-packet.json").exists())

    def test_blocked_for_unreviewed_candidate(self) -> None:
        self._write_artifacts(cids=("cand-other",))
        payload = write_packet(_ns(candidate_id="cand-alpha", parent_candidate_id="cand-missing"))
        self.assertEqual(payload["review_status"], "blocked")
        self.assertEqual(payload["reviews"], [])
        self.assertEqual(payload["metadata"]["block_reason"], "no_provider_review_for_candidate_in_run")
        self.assertIn("cand-other", payload["metadata"]["available_candidate_ids"])
        self.assertEqual(validate_governance_payload(payload, "provider_review_packet.v1"), [])
        self.assertIn("provider_review_not_success", _provider_review_errors(payload))

    def test_timeout_when_provider_timed_out(self) -> None:
        self._write_artifacts(cids=("cand-alpha",), timed_out=True)
        payload = write_packet(_ns(candidate_id="cand-alpha"))
        self.assertEqual(payload["review_status"], "timeout")
        self.assertTrue(any("unavailable" in error for error in _provider_review_errors(payload)))

    def test_test_provider_blocks(self) -> None:
        self._write_artifacts(cids=("cand-alpha",), test_provider=True)
        payload = write_packet(_ns(candidate_id="cand-alpha"))
        self.assertTrue(payload["test_provider_used"])
        self.assertIn("test_provider_review_blocks_active", _provider_review_errors(payload))

    def test_command_and_log_hash_non_empty(self) -> None:
        self._write_artifacts(cids=("cand-alpha",))
        payload = write_packet(_ns(candidate_id="cand-alpha"))
        self.assertTrue(payload["command_hash"].startswith("sha256:"))
        self.assertTrue(payload["provider_log_hash"].startswith("sha256:"))
        self.assertEqual(len(payload["artifact_hashes"]), 2)


if __name__ == "__main__":
    unittest.main()
