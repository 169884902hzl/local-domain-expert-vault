from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from audit_experiment_plan import REQUIRED_SECTIONS
from kb_common import vault_path
from kb_search import SearchResult
from plan_experiment import EvidenceSet, collect_evidence, query_from_candidate, render_plan


class PlanExperimentTest(unittest.TestCase):
    def test_collect_evidence_uses_semantic_search_by_default(self) -> None:
        seen = []

        def fake_search(args):
            seen.append(args)
            return []

        with patch("plan_experiment.search", side_effect=fake_search):
            collect_evidence("DLO tactile policy", 3)
        self.assertTrue(seen)
        self.assertTrue(all(args.semantic is True for args in seen))
        self.assertTrue(all(args.semantic_floor == 0.55 for args in seen))

    def test_candidate_query_uses_candidate_metadata(self) -> None:
        query = query_from_candidate(
            {
                "candidate_id": "cand-alpha",
                "title": "Accepted Candidate",
                "metadata": {"problem": "DLO contact failure", "mechanism": "Tactile recovery trigger"},
            }
        )
        self.assertIn("Accepted Candidate", query)
        self.assertIn("DLO contact failure", query)
        self.assertIn("Tactile recovery trigger", query)

    def test_render_plan_contains_required_sections(self) -> None:
        result = SearchResult(
            path=vault_path("wiki", "topics", "example.md"),
            title="Example DLO Paper",
            note_type="literature",
            year="2099",
            status="done",
            summary="DLO tactile diffusion benchmark evidence.",
            tags=["DLO", "tactile", "diffusion", "bimanual", "sim-to-real"],
            score=10.0,
            snippets=["DLO tactile diffusion benchmark evidence."],
        )
        content = render_plan("DLO tactile diffusion", EvidenceSet(items=[result] * 8, coverage={"DLO", "tactile", "diffusion", "bimanual", "sim-to-real", "benchmark"}, gaps=[]))
        for heading in REQUIRED_SECTIONS:
            self.assertIn(heading, content)
        self.assertIn('decision_status: "recommended_pending_approval"', content)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
