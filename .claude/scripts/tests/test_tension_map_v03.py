from __future__ import annotations

import unittest

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401
from tension_map import build_tensions, validate_tensions


def node(node_id: str, paper: str, claim_type: str, *, confidence: str = "high", anchor_type: str = "section") -> dict[str, object]:
    statement = "Contact benchmark success metric limits latent friction claim."
    return {
        "node_id": node_id,
        "paper_key": paper,
        "claim_type": claim_type,
        "statement": statement,
        "confidence": confidence,
        "anchor_type": anchor_type,
        "requires_human_check": False,
        "anchor": {"anchor_type": anchor_type, "section": "Results", "snippet": statement},
    }


class TensionMapV03Test(unittest.TestCase):
    def test_cross_paper_contradiction_generates_cross_paper_tension(self) -> None:
        nodes = [node("a", "PAPER-A", "contradiction"), node("b", "PAPER-B", "method_assumption")]
        edge = {
            "edge_id": "edge-a-b",
            "source_node_id": "a",
            "target_node_id": "b",
            "relation": "contradicts",
            "confidence": "high",
            "edge_scope": "cross_paper",
            "requires_human_check": True,
        }
        tensions, speculative = build_tensions(nodes, [edge])
        self.assertFalse(speculative)
        self.assertEqual(tensions[0]["tension_scope"], "cross_paper")
        self.assertEqual(tensions[0]["supporting_edges"], ["edge-a-b"])

    def test_llm_only_high_tension_rejected_as_speculative(self) -> None:
        tensions = [
            {
                "tension_id": "tension-1",
                "tension_type": "speculative_tension",
                "summary": "LLM-only hunch",
                "supporting_nodes": [],
                "supporting_edges": [],
                "tension_scope": "speculative",
                "confidence": "high",
                "source": "llm",
                "do_not_use_as_seed_evidence": False,
            }
        ]
        errors = validate_tensions(tensions, set(), {}, set())
        self.assertIn("tension-1:high_confidence_llm_only_tension", errors)

    def test_speculative_tension_cannot_support_formal_seed(self) -> None:
        low_node = node("a", "PAPER-A", "interface_boundary", confidence="low")
        tensions, speculative = build_tensions([low_node], [])
        self.assertFalse(tensions)
        self.assertTrue(speculative)
        self.assertTrue(speculative[0]["do_not_use_as_seed_evidence"])
