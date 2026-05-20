from __future__ import annotations

import unittest

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401
from research_claim_graph import build_edges, build_nodes


def claim(paper: str, claim_type: str, statement: str, *, confidence: str = "high", anchor_type: str = "section") -> dict[str, object]:
    return {
        "claim_id": f"{paper}-{claim_type}",
        "claim_type": claim_type,
        "statement": statement,
        "confidence": confidence,
        "evidence_anchor": f"wiki/topics/{paper}.md#Results",
        "anchor_type": anchor_type,
        "anchor_source": "note_section",
        "summary_origin": "section_summary",
        "requires_human_check": False,
        "domains": ["dlo", "contact"],
        "anchor": {
            "anchor_type": anchor_type,
            "anchor_source": "note_section",
            "section": "Results",
            "snippet": statement,
        },
    }


def paper(paper_key: str, claims: list[dict[str, object]]) -> dict[str, object]:
    return {"paper_key": paper_key, "source_note": f"wiki/topics/{paper_key}.md", "claims": claims}


class CrossPaperClaimGraphTest(unittest.TestCase):
    def test_cross_paper_edge_requires_two_papers(self) -> None:
        nodes = build_nodes(
            [
                paper(
                    "PAPER-A",
                    [
                        claim("PAPER-A", "actual_baseline_result", "Contact benchmark success metric limits latent friction claim."),
                        claim("PAPER-A", "central_claim", "Latent friction claim uses contact benchmark success metric."),
                    ],
                )
            ]
        )
        self.assertFalse([edge for edge in build_edges(nodes) if edge.get("edge_scope") == "cross_paper"])

    def test_cross_paper_edge_confidence_bounded_by_weakest_node(self) -> None:
        nodes = build_nodes(
            [
                paper("PAPER-A", [claim("PAPER-A", "actual_baseline_result", "Contact benchmark success metric limits latent friction claim.", confidence="medium")]),
                paper("PAPER-B", [claim("PAPER-B", "central_claim", "Latent friction claim uses contact benchmark success metric.", confidence="high")]),
            ]
        )
        edges = [edge for edge in build_edges(nodes) if edge.get("edge_scope") == "cross_paper"]
        self.assertTrue(edges)
        self.assertEqual(edges[0]["confidence"], "medium")
        self.assertNotEqual(edges[0]["source_paper_key"], edges[0]["target_paper_key"])

    def test_high_cross_paper_edge_requires_anchored_nodes(self) -> None:
        nodes = build_nodes(
            [
                paper("PAPER-A", [claim("PAPER-A", "actual_baseline_result", "Contact benchmark success metric limits latent friction claim.", confidence="high", anchor_type="note_only")]),
                paper("PAPER-B", [claim("PAPER-B", "central_claim", "Latent friction claim uses contact benchmark success metric.", confidence="high")]),
            ]
        )
        self.assertFalse([edge for edge in build_edges(nodes) if edge.get("edge_scope") == "cross_paper"])

    def test_no_node_edge_rejected_from_cross_paper_builder(self) -> None:
        edges = build_edges([])
        self.assertEqual(edges, [])
