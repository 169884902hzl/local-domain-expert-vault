from __future__ import annotations

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from pdf_evidence_extract import build_anchor_records, is_pdf_verified_anchor, validate_result_row_anchor
from research_seed_v2_common import validate_payload


class PdfEvidenceExtractTest(V03TempAgendaTest):
    def primitive(self, source_pdf: str = "") -> dict[str, object]:
        return {
            "schema_version": "paper_primitives.v1",
            "run_date": RUN_DATE,
            "paper_key": "PAPER-A",
            "source_note": "wiki/topics/PAPER-A.md",
            "source_pdf": source_pdf,
            "claims": [
                {
                    "claim_id": "claim-1",
                    "claim_type": "actual_baseline_result",
                    "statement": "Baseline result is reported in the Results section.",
                    "confidence": "medium",
                    "evidence_anchor": "wiki/topics/PAPER-A.md#Results",
                    "anchor_type": "section",
                    "anchor_source": "note_section",
                    "summary_origin": "section_summary",
                    "requires_human_check": False,
                    "anchor": {
                        "anchor_type": "section",
                        "anchor_source": "note_section",
                        "section": "Results",
                        "snippet": "Baseline result is reported.",
                    },
                }
            ],
        }

    def test_pdf_evidence_anchors_schema_validates(self) -> None:
        records = build_anchor_records([self.primitive()], run_date=RUN_DATE)
        payload = {"schema_version": "pdf_evidence_anchors.v1", "run_date": RUN_DATE, "records": records}
        self.assertEqual(validate_payload(payload, "pdf_evidence_anchors.v1"), [])

    def test_missing_pdf_degrades_to_note_section_without_fabrication(self) -> None:
        record = build_anchor_records([self.primitive("attachments/missing.pdf")], run_date=RUN_DATE)[0]
        self.assertEqual(record["source_pdf"], "attachments/missing.pdf")
        self.assertEqual(len(record["anchors"]), 1)
        anchor = record["anchors"][0]
        self.assertEqual(anchor["anchor_source"], "note_section")
        self.assertFalse(is_pdf_verified_anchor(anchor))
        self.assertEqual(anchor["page"], None)
        self.assertEqual(anchor["table"], "")

    def test_result_row_requires_page_and_row_fields(self) -> None:
        anchor = {
            "anchor_type": "result_row",
            "anchor_source": "pdf_table",
            "page": 3,
            "row_index": 2,
            "row_text": "baseline | auc | 0.72",
            "metric_name": "auc",
            "baseline_name": "baseline",
            "reported_value": "0.72",
            "task_or_dataset": "contact shift",
        }
        self.assertEqual(validate_result_row_anchor(anchor), [])
        self.assertTrue(is_pdf_verified_anchor(anchor))
        missing = dict(anchor)
        missing.pop("row_text")
        self.assertIn("result_row_missing_row_text", validate_result_row_anchor(missing))

    def test_note_section_anchor_does_not_count_pdf_verified(self) -> None:
        anchor = {
            "anchor_type": "section",
            "anchor_source": "note_section",
            "page": None,
            "section": "Results",
            "snippet": "Result summary.",
        }
        self.assertFalse(is_pdf_verified_anchor(anchor))
