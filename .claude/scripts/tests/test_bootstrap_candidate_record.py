from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from bootstrap_candidate_record import bootstrap_from_accepted
from research_governance_common import active_commit_validation, candidate_dir, read_json, validate_governance_payload


class BootstrapCandidateRecordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.old_root = os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT")
        os.environ["RESEARCH_GOVERNANCE_AGENDA_ROOT"] = self.tmp.name
        self.accepted_path = Path(self.tmp.name) / "accepted.json"
        self.accepted_path.write_text(
            json.dumps(
                {
                    "schema_version": "research_seed_bucket_item.v1",
                    "run_date": "2099-03-04",
                    "candidate_id": "cand-alpha",
                    "candidate": {
                        "candidate_id": "cand-alpha",
                        "title": "Accepted Candidate",
                        "problem": "DLO contact failure",
                        "mechanism": "Tactile recovery trigger",
                        "evidence": [{"claim_type": "method", "statement": "Supported by a local note.", "source_note": "wiki/topics/example.md"}],
                    },
                    "survival_decision": {"candidate_id": "cand-alpha", "candidate_title": "Accepted Candidate"},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        if self.old_root is None:
            os.environ.pop("RESEARCH_GOVERNANCE_AGENDA_ROOT", None)
        else:
            os.environ["RESEARCH_GOVERNANCE_AGENDA_ROOT"] = self.old_root
        self.tmp.cleanup()

    def test_bootstrap_record_validates_and_does_not_unlock_active_commit(self) -> None:
        record = bootstrap_from_accepted(self.accepted_path, human_initiated=True)
        self.assertEqual(validate_governance_payload(record, "candidate_record.v1"), [])
        self.assertFalse(record["auto_promote_allowed"])
        self.assertTrue((candidate_dir("cand-alpha") / "candidate-record.json").exists())
        self.assertEqual(read_json(candidate_dir("cand-alpha") / "candidate-record.json")["state"], "program_candidate_synthesized")
        self.assertFalse(active_commit_validation("cand-alpha").ok)

    def test_bootstrap_requires_human_initiated_flag(self) -> None:
        with self.assertRaises(ValueError):
            bootstrap_from_accepted(self.accepted_path, human_initiated=False)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
