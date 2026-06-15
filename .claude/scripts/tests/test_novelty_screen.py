from __future__ import annotations

import argparse
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from novelty_screen import write_screen
from research_governance_common import (
    _novelty_screen_errors,
    candidate_dir,
    validate_governance_payload,
    write_json,
)


def _ns(**kw):
    base = dict(candidate_id="", max_external_queries=1, external_timeout=12, semantic_scholar_mode="auto", validate=False, dry_run=False)
    base.update(kw)
    return argparse.Namespace(**base)


class NoveltyScreenTest(unittest.TestCase):
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

    def _write_record(self, cid: str = "cand-alpha") -> None:
        write_json(candidate_dir(cid) / "candidate-record.json", {"schema_version": "candidate_record.v1", "candidate_id": cid, "title": "Test Candidate", "state": "program_candidate_synthesized", "auto_promote_allowed": False, "metadata": {"problem": "x", "mechanism": "y"}})

    def test_screen_success_when_external_completed(self) -> None:
        self._write_record()
        scan = {"status": "completed", "external_providers_used": ["openalex", "arxiv_api"], "provider_errors": [], "stale_external_novelty_cache": False, "verification_scope": "local_plus_openalex", "novelty_classification": "likely_open", "nearest_works": []}
        with patch("novelty_screen._build_candidate_scan", return_value=scan):
            payload = write_screen(_ns(candidate_id="cand-alpha"))
        self.assertEqual(payload["screen_status"], "success")
        self.assertTrue(payload["screening_only"])
        self.assertFalse(payload["replaces_manual_prior_art_dossier"])
        self.assertEqual(payload["api_provider_status"], "success")
        self.assertEqual(payload["provider_errors"], [])
        self.assertEqual(validate_governance_payload(payload, "novelty_screen.v1"), [])
        self.assertEqual(_novelty_screen_errors(payload, {}), [])

    def test_screen_provider_unavailable_honest(self) -> None:
        self._write_record()
        scan = {"status": "completed_local_only", "external_providers_used": [], "provider_errors": [{"provider": "openalex", "error": "timeout after 12s"}], "stale_external_novelty_cache": False}
        with patch("novelty_screen._build_candidate_scan", return_value=scan):
            payload = write_screen(_ns(candidate_id="cand-alpha"))
        self.assertEqual(payload["screen_status"], "provider_unavailable")
        self.assertEqual(validate_governance_payload(payload, "novelty_screen.v1"), [])
        self.assertIn("novelty_provider_unavailable_not_covered_by_manual_dossier", _novelty_screen_errors(payload, {}))

    def test_screen_stale_cache_blocks(self) -> None:
        self._write_record()
        scan = {"status": "completed", "external_providers_used": ["openalex"], "provider_errors": [], "stale_external_novelty_cache": True}
        with patch("novelty_screen._build_candidate_scan", return_value=scan):
            payload = write_screen(_ns(candidate_id="cand-alpha"))
        self.assertTrue(payload["stale"])
        self.assertNotEqual(payload["screen_status"], "success")
        self.assertIn("stale_novelty_screen_blocks_active", _novelty_screen_errors(payload, {}))

    def test_screen_never_replaces_dossier(self) -> None:
        self._write_record()
        scans = [
            {"status": "completed", "external_providers_used": ["openalex"], "provider_errors": [], "stale_external_novelty_cache": False},
            {"status": "completed_local_only", "external_providers_used": [], "provider_errors": [{"provider": "x", "error": "unavailable"}], "stale_external_novelty_cache": False},
        ]
        for scan in scans:
            with patch("novelty_screen._build_candidate_scan", return_value=scan):
                payload = write_screen(_ns(candidate_id="cand-alpha"))
            self.assertTrue(payload["screening_only"])
            self.assertFalse(payload["replaces_manual_prior_art_dossier"])

    def test_missing_record_blocks(self) -> None:
        payload = write_screen(_ns(candidate_id="cand-nonexistent"))
        self.assertEqual(payload["screen_status"], "blocked")
        self.assertEqual(payload["api_provider_status"], "missing_candidate_record")
        self.assertEqual(validate_governance_payload(payload, "novelty_screen.v1"), [])


if __name__ == "__main__":
    unittest.main()
