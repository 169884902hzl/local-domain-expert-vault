from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401

import audit_kb
import research_agenda_extract as extractor
from finalize_reading import finalize_content, validate_analysis, extract_sections
from kb_common import load_schema
from research_claim_graph import build_nodes
from research_seed_v2_common import schema_validator_available, validate_payload


RUN_DATE = "2099-05-21"


BASE_NOTE = """---
title: Fixture Paper
tags: [DLO]
created: 2099-01-01
updated: 2099-01-01
type: literature
status: stub
summary: Fixture summary for strict reading tests.
authors: Test Author
year: 2099
venue: TestConf
zotero_key: TESTKEY
---
## 摘要
Stub abstract.

## 中文简述
Stub Chinese summary.

## 关键贡献
- Stub contribution.

## 结构化提取
- Problem: old
- Method: old
- Tasks: old
- Sensors: old
- Robot Setup: old
- Metrics: old
- Limitations: old
- Evidence Notes: old

## 本地引用关系
- Related to [[DLO]]

## 相关概念
- [[DLO]]

## 相关研究者
- [[Test Author]]
"""


GOOD_LEDGER = """| claim_id | claim_type | claim | evidence_class | anchor_type | anchor | page/section/table/figure/appendix | confidence | downstream_use |
|---|---|---|---|---|---|---|---|---|
| C-P1 | problem | The paper frames DLO contact state drift as the core problem. | pdf_verified | section | Section 1 Problem | p1 Section 1 | high | candidate_ok |
| C-M1 | method | The method uses contact-aware state features for planning. | pdf_verified | section | Section 3 Method | p3 Section 3 | high | candidate_ok |
| C-E1 | experiment | The main experiment reports a benchmark metric. | table_verified | table | Table 2 | p5 Table 2 | high | baseline_ok |
| C-L1 | limitation | The paper does not evaluate physical closed-loop DLO control. | pdf_verified | section | Section 6 Limitations | p7 Section 6 | medium | candidate_ok |
| C-B1 | baseline | The strongest baseline is a contact-aware planner. | pdf_verified | table | Table 2 | p5 Table 2 | high | baseline_ok |"""


GOOD_BASELINE = """- Strongest Baseline: Contact-aware planner [C-B1]
- Why strongest: It directly compares on the reported benchmark and metric.
- Evidence anchor / claim_id: C-B1 / Table 2
- Paper win condition: Paper beats the planner on the paper metric.
- Idea kill condition: If the planner matches the paper on the same static metric, the idea is killed.
- DLO replacement baseline: A DLO-specific contact planner with the same observable inputs.
- No-hardware proxy baseline: Recompute Table 2 ranking from reported values."""


GOOD_TRANSFER = """- Source domain: video generation
- Target domain: DLO manipulation
- Transfer distance: high
- Why transfer may fail: Pixels do not encode contact forces or closed-loop control state.
- Negative transfer risk: Direct copying may optimize visual realism while worsening control.
- Misleading direct-copy risk: A generated trajectory may look plausible but be dynamically invalid.
- DLO-specific missing variable: tension, contact mode, and hidden friction.
- DLO replacement baseline: DLO contact planner [C-B1]
- Kill condition: Static metric fails to beat the DLO baseline on reported rows.
- Evidence anchor / claim_id: C-L1"""


GOOD_MICRO_TEST = """- Artifact: synthetic toy arrays and static metric table from paper results.
- Protocol: no robot; no real scene; no new data collection. Use toy arrays, pseudo-code, and static metric calculation only.
- Metric: ranking consistency and absolute metric error.
- Pass condition: Recomputed ranking matches Table 2.
- Kill condition: Recomputed ranking contradicts Table 2 or depends on unavailable data."""


def strict_analysis(
    *,
    ledger: str | None = GOOD_LEDGER,
    include_top_idea: bool = True,
    nested_idea: str = "",
    top_idea: str = "- [C-L1] Treat this as adversarial pressure, not inspiration.",
    baseline: str = GOOD_BASELINE,
    transfer: str = GOOD_TRANSFER,
    micro_test: str = GOOD_MICRO_TEST,
) -> str:
    key_takeaways = "- [C-L1] The limitation is the transfer bottleneck."
    if nested_idea:
        key_takeaways += f"\n\n### Idea Fuel\n{nested_idea}"
    ledger_section = f"## Evidence Ledger\n{ledger}\n\n" if ledger is not None else ""
    idea_section = f"## Idea Fuel\n{top_idea}\n\n" if include_top_idea else ""
    return f"""## Evidence Metadata
- Fulltext Quality: pdf_verified
- Evidence Coverage: tables, figures, and sections checked
- Confidence: medium
- Summary: Anchored fixture reading with strict evidence ledger.

## Problem
- [C-P1] The paper frames DLO contact state drift as the core problem.

## Key Contributions
- [C-M1] It contributes contact-aware planning features.

## Method
- [C-M1] It maps observations to contact-aware state features.

## Experiments
- [C-E1] It reports a benchmark metric in Table 2.

## Limitations
- [C-L1] It lacks physical closed-loop DLO control.

## Key Takeaways
{key_takeaways}

{ledger_section}{idea_section}## Baseline Pressure
{baseline}

## Transfer Risk
{transfer}

## No-hardware Micro-test
{micro_test}

## Evidence Gaps
- [C-L1] No verified physical closed-loop DLO control evidence.

## 结构化提取
- Problem: DLO contact state drift is the core problem. [C-P1]
- Method: Contact-aware planning features. [C-M1]
- Tasks: DLO manipulation proxy benchmark. [C-E1]
- Sensors: Vision-only observations reported by the paper. [C-M1]
- Robot Setup: Not evidenced for physical DLO closed-loop control. [C-L1]
- Metrics: Static benchmark metric from Table 2. [C-E1]
- Limitations: Missing physical DLO closed-loop control. [C-L1]
- Evidence Notes: Ledger rows C-P1, C-M1, C-E1, C-L1, C-B1.

## 本地引用关系
- Related to [[DLO]]
"""


def finalized_strict_note() -> str:
    return finalize_content(BASE_NOTE, strict_analysis(), load_schema())


class FinalizeStrictContractTest(unittest.TestCase):
    def test_top_level_idea_fuel_is_preserved(self) -> None:
        output = finalized_strict_note()
        self.assertIn("## Idea Fuel", output)
        self.assertIn("adversarial pressure", output)
        self.assertIn("## Evidence Ledger", output)

    def test_nested_idea_fuel_is_promoted_when_top_level_absent(self) -> None:
        output = finalize_content(
            BASE_NOTE,
            strict_analysis(include_top_idea=False, nested_idea="- [C-L1] Nested fallback pressure."),
            load_schema(),
        )
        self.assertIn("## Idea Fuel", output)
        self.assertIn("- [C-L1] Nested fallback pressure.", output)

    def test_conflicting_top_level_and_nested_idea_fuel_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate_idea_fuel_conflict"):
            finalize_content(
                BASE_NOTE,
                strict_analysis(nested_idea="- [C-L1] Materially different nested pressure."),
                load_schema(),
            )

    def test_missing_or_malformed_evidence_ledger_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "Evidence Ledger"):
            validate_analysis(extract_sections(strict_analysis(ledger=None)), load_schema())
        malformed = "| claim_id | claim_type | claim |\n|---|---|---|\n| C-P1 | problem | Missing columns |"
        with self.assertRaisesRegex(ValueError, "evidence_ledger_missing_required_columns"):
            validate_analysis(extract_sections(strict_analysis(ledger=malformed)), load_schema())

    def test_anchorless_key_claim_fails_unless_not_evidenced(self) -> None:
        bad = GOOD_LEDGER.replace(
            "| C-P1 | problem | The paper frames DLO contact state drift as the core problem. | pdf_verified | section | Section 1 Problem | p1 Section 1 | high | candidate_ok |",
            "| C-P1 | problem | The paper frames DLO contact state drift as the core problem. | pdf_verified | note_only |  | p1 Section 1 | high | candidate_ok |",
        )
        with self.assertRaisesRegex(ValueError, "evidence_ledger_anchorless_key_claim|evidence_ledger_missing_anchor"):
            validate_analysis(extract_sections(strict_analysis(ledger=bad)), load_schema())

        allowed = GOOD_LEDGER.replace(
            "| C-P1 | problem | The paper frames DLO contact state drift as the core problem. | pdf_verified | section | Section 1 Problem | p1 Section 1 | high | candidate_ok |",
            "| C-P1 | problem | The paper frames DLO contact state drift as the core problem. | not_evidenced | note_only |  | not evidenced | low | screening_only |",
        )
        validate_analysis(extract_sections(strict_analysis(ledger=allowed)), load_schema())

    def test_hardware_micro_tests_fail_and_synthetic_static_test_passes(self) -> None:
        bad_sections = [
            GOOD_MICRO_TEST.replace("Use toy arrays", "Use a real robot arm"),
            GOOD_MICRO_TEST.replace("Use toy arrays", "Evaluate on a real cabinet"),
            GOOD_MICRO_TEST.replace("no new data collection. Use toy arrays", "run new data collection. Use toy arrays"),
        ]
        for section in bad_sections:
            with self.subTest(section=section):
                with self.assertRaisesRegex(ValueError, "no_hardware_micro_test"):
                    validate_analysis(extract_sections(strict_analysis(micro_test=section)), load_schema())
        validate_analysis(extract_sections(strict_analysis(micro_test=GOOD_MICRO_TEST)), load_schema())

    def test_cross_domain_dlo_hook_requires_transfer_risk_fields(self) -> None:
        bad_transfer = """- Source domain: video generation
- Target domain: DLO manipulation
- Transfer distance: medium"""
        with self.assertRaisesRegex(ValueError, "transfer_risk_missing|generation_to_dlo_distance_too_low"):
            validate_analysis(extract_sections(strict_analysis(transfer=bad_transfer)), load_schema())
        validate_analysis(extract_sections(strict_analysis(transfer=GOOD_TRANSFER)), load_schema())

    def test_cross_domain_deformable_terms_require_transfer_risk_fields(self) -> None:
        targets = [
            "rope manipulation",
            "cable routing",
            "cloth folding",
            "deformable object manipulation",
            "线缆整理",
            "绳索操控",
            "布料折叠",
        ]
        for target in targets:
            with self.subTest(target=target):
                bad_transfer = f"""- Source domain: video generation
- Target domain: {target}
- Transfer distance: high"""
                with self.assertRaisesRegex(ValueError, "transfer_risk_missing:why_transfer_may_fail"):
                    validate_analysis(extract_sections(strict_analysis(transfer=bad_transfer)), load_schema())
        bad_source = """- Source domain: rope perception
- Target domain: cable manipulation
- Transfer distance: high"""
        with self.assertRaisesRegex(ValueError, "transfer_risk_missing:why_transfer_may_fail"):
            validate_analysis(extract_sections(strict_analysis(transfer=bad_source)), load_schema())

    def test_generation_to_deformable_transfer_requires_high_distance(self) -> None:
        for target in ["rope manipulation", "DLO manipulation"]:
            for distance in ["low", "medium"]:
                with self.subTest(target=target, distance=distance):
                    transfer = GOOD_TRANSFER.replace("- Target domain: DLO manipulation", f"- Target domain: {target}")
                    transfer = transfer.replace("- Transfer distance: high", f"- Transfer distance: {distance}")
                    with self.assertRaisesRegex(ValueError, "generation_to_dlo_distance_too_low"):
                        validate_analysis(extract_sections(strict_analysis(transfer=transfer)), load_schema())

    def test_baseline_pressure_claim_id_must_exist_in_ledger(self) -> None:
        bad_baseline = GOOD_BASELINE.replace("C-B1 / Table 2", "C-Z9 / Table 2")
        with self.assertRaisesRegex(ValueError, "baseline_pressure_unknown_claim_id:C-Z9"):
            validate_analysis(extract_sections(strict_analysis(baseline=bad_baseline)), load_schema())
        validate_analysis(extract_sections(strict_analysis(baseline=GOOD_BASELINE)), load_schema())


class AuditTargetModeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.topics = self.root / "wiki" / "topics"
        self.concepts = self.root / "wiki" / "concepts"
        self.entities = self.root / "wiki" / "entities"
        for path in [self.topics, self.concepts, self.entities]:
            path.mkdir(parents=True, exist_ok=True)
        self.patches = [
            patch.object(audit_kb, "TOPICS_DIR", self.topics),
            patch.object(audit_kb, "CONCEPTS_DIR", self.concepts),
            patch.object(audit_kb, "ENTITIES_DIR", self.entities),
            patch.object(audit_kb, "vault_path", lambda *parts: self.root.joinpath(*parts)),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self) -> None:
        for item in reversed(self.patches):
            item.stop()
        self.tmp.cleanup()

    def write_concept_warning(self) -> None:
        (self.concepts / "weak-concept.md").write_text(
            """---
title: Weak Concept
tags: [DLO]
created: 2099-01-01
updated: 2099-01-01
type: concept
status: stub
summary: Weak concept fixture.
---
No related sections yet.
""",
            encoding="utf-8",
        )

    def write_topic(self, name: str, content: str) -> Path:
        path = self.topics / name
        path.write_text(content, encoding="utf-8")
        return path

    def test_target_mode_passes_despite_global_warnings(self) -> None:
        self.write_topic("strict.md", finalized_strict_note())
        self.write_concept_warning()
        schema = load_schema()
        topic_issues, _status_counts, tag_counts = audit_kb.audit_topics(schema, strict_reading=True)
        concept_issues = audit_kb.audit_concepts(schema)
        payload, ok = audit_kb.target_payload(
            schema=schema,
            args=argparse.Namespace(zotero_key="TESTKEY", note="", strict_reading=True),
            topic_issues=topic_issues,
            concept_issues=concept_issues,
            entity_issues=[],
            tags_missing=sorted(set(tag_counts) - set(schema["literature"]["tag_taxonomy"])),
        )
        self.assertTrue(ok)
        self.assertTrue(payload["target_note"]["strict_reading_pass"])
        self.assertTrue(payload["global_warnings"]["concept_issues"])
        self.assertEqual(payload["exit_policy"], "target_note_only")

    def test_target_mode_fails_on_missing_strict_sections(self) -> None:
        old_note = finalized_strict_note().replace("## Evidence Ledger", "## Removed Evidence Ledger")
        self.write_topic("broken.md", old_note)
        payload, ok = audit_kb.target_payload(
            schema=load_schema(),
            args=argparse.Namespace(zotero_key="TESTKEY", note="", strict_reading=True),
            topic_issues=[],
            concept_issues=[],
            entity_issues=[],
            tags_missing=[],
        )
        self.assertFalse(ok)
        self.assertIn("strict_missing_strict_section:Evidence Ledger", payload["target_note"]["issues"])

    def test_global_audit_keeps_old_exit_behavior(self) -> None:
        old_global_note = finalized_strict_note()
        for heading in ["Evidence Ledger", "Idea Fuel", "Baseline Pressure", "Transfer Risk", "No-hardware Micro-test", "Evidence Gaps"]:
            old_global_note = old_global_note.replace(f"## {heading}", f"## Removed {heading}")
        self.write_topic("old-global.md", old_global_note)
        self.write_concept_warning()
        schema = load_schema()
        topic_issues, _status_counts, _tag_counts = audit_kb.audit_topics(schema, strict_reading=True)
        concept_issues = audit_kb.audit_concepts(schema)
        self.assertFalse(any("strict_missing_strict_section" in ",".join(item["issues"]) for item in topic_issues))
        self.assertTrue(concept_issues)
        self.assertTrue(topic_issues or concept_issues)


def extractor_note() -> str:
    return """---
title: Extractor Fixture
tags: [DLO]
created: 2099-01-01
updated: 2099-01-01
type: literature
status: done
summary: Extractor fixture with strict ledger rows.
authors: Test Author
year: 2099
venue: TestConf
zotero_key: EXTRACTKEY
---
## 摘要
Done note.

## 结构化提取
- Problem: DLO transfer problem.
- Method: Static metric check.
- Tasks: DLO manipulation proxy.
- Sensors: Existing images only.
- Robot Setup: None.
- Metrics: Static metric.
- Limitations: Transfer risk.
- Evidence Notes: Strict ledger rows.

## Evidence Ledger
| claim_id | claim_type | claim | evidence_class | anchor_type | anchor | page/section/table/figure/appendix | confidence | downstream_use |
|---|---|---|---|---|---|---|---|---|
| C-W1 | central_claim | Note-derived idea should stay screening-only. | note_derived | note_only |  | note only | low | screening_only |
| C-W2 | method_assumption | Abstract-only claim should stay screening-only. | abstract_only | abstract | abstract | abstract | low | screening_only |
| C-W3 | transfer_failure | Not evidenced transfer risk should stay screening-only. | not_evidenced | note_only |  | not evidenced | low | screening_only |
| C-R1 | actual_baseline_result | Result row is unconfirmed until human checks the row. | result_row_unconfirmed | result_row | Table 2 row 1 | p5 Table 2 row 1 | medium | requires_human_check |
| C-A1 | central_claim | Appendix derivation supports the anchored claim. | appendix_verified | appendix | Appendix A derivation | Appendix A p12 | high | candidate_ok |

## Idea Fuel
Speculative transfer hook without a ledger claim reference.

## Baseline Pressure
- Strongest Baseline: Contact planner [C-A1]
- Why strongest: It is the direct DLO comparator.
- Evidence anchor / claim_id: C-A1
- Paper win condition: Beat static metric.
- Idea kill condition: Fails static metric.
- DLO replacement baseline: Contact planner.
- No-hardware proxy baseline: Static metric calculation.

## Transfer Risk
- Source domain: video generation
- Target domain: DLO manipulation
- Transfer distance: high
- Why transfer may fail: Contact and tension are hidden.
- Negative transfer risk: Visual plausibility can mislead control.
- DLO replacement baseline: Contact planner.
- Kill condition: Static metric fails.

## No-hardware Micro-test
No robot; no real scene; no new data collection. Artifact: toy arrays. Protocol: static metric calculation. Metric: ranking error. Pass condition: stable ranking. Kill condition: ranking flip.

## Evidence Gaps
Missing physical DLO closed-loop evidence.
"""


class ResearchAgendaExtractorStrictFieldsTest(unittest.TestCase):
    def extract_records(self) -> list[dict[str, object]]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "extractor.md"
            path.write_text(extractor_note(), encoding="utf-8")
            with patch.object(extractor, "rel", lambda note_path: f"wiki/topics/{Path(note_path).name}"):
                return extractor.extract_from_note(path, run_date=RUN_DATE)

    def test_new_sections_parse_as_review_pressure_not_evidence(self) -> None:
        records = self.extract_records()
        idea = next(record for record in records if record.get("claim_type") == "idea_fuel")
        micro = next(record for record in records if record.get("claim_type") == "no_hardware_micro_test")
        self.assertEqual(idea["record_role"], "review_pressure")
        self.assertFalse(idea["evidence_bearing"])
        self.assertTrue(idea["screening_only"])
        self.assertFalse(idea["linked_strict_anchor"])
        self.assertFalse(micro["pilot_ready"])
        self.assertFalse(micro["evidence_bearing"])

    def test_weak_evidence_classes_stay_screening_only(self) -> None:
        records = self.extract_records()
        weak = [record for record in records if record.get("evidence_class") in {"note_derived", "abstract_only", "not_evidenced"}]
        self.assertEqual(len(weak), 3)
        for record in weak:
            self.assertEqual(record["extraction_confidence"], "low")
            self.assertTrue(record["screening_only"])
            self.assertTrue(record["requires_human_check"])
            self.assertFalse(record["evidence_bearing"])

    def test_result_row_unconfirmed_requires_human_check(self) -> None:
        records = self.extract_records()
        row = next(record for record in records if record.get("evidence_class") == "result_row_unconfirmed")
        self.assertEqual(row["anchor_type"], "result_row")
        self.assertTrue(row["requires_human_check"])
        self.assertEqual(row["confirmation_status"], "unconfirmed")
        self.assertFalse(row["evidence_bearing"])

    def test_transfer_risk_populates_transfer_failure_as_review_pressure(self) -> None:
        records = [record for record in self.extract_records() if record.get("claim_type") != "transfer_failure"]
        primitive = extractor.build_paper_primitives(records)[0]
        self.assertIn("Transfer distance", primitive["primitives"]["transfer_failure"])
        claim = next(claim for claim in primitive["claims"] if claim.get("claim_type") == "transfer_failure")
        self.assertEqual(claim["record_role"], "review_pressure")
        self.assertTrue(claim["screening_only"])
        self.assertTrue(claim["requires_human_check"])
        self.assertEqual(claim["confidence"], "low")

    def test_appendix_anchor_supported_and_schema_ready(self) -> None:
        records = self.extract_records()
        appendix = next(record for record in records if record.get("anchor_type") == "appendix")
        self.assertTrue(appendix["evidence_bearing"])
        self.assertEqual(appendix["evidence_class"], "appendix_verified")

        node = build_nodes(
            [
                {
                    "paper_key": "APP",
                    "source_note": "wiki/topics/app.md",
                    "claims": [
                        {
                            "claim_id": "APP-C1",
                            "claim_type": "central_claim",
                            "statement": "Appendix supports a strict claim.",
                            "evidence_anchor": "Appendix A",
                            "anchor_type": "appendix",
                            "confidence": "high",
                            "confidence_reason": "appendix_verified",
                            "summary_origin": "evidence_ledger",
                            "requires_human_check": False,
                            "anchor": {"anchor_type": "appendix", "section": "Appendix A", "snippet": "Appendix supports a strict claim."},
                        }
                    ],
                }
            ]
        )[0]
        self.assertEqual(node["confidence"], "high")
        self.assertEqual(node["anchor_type"], "appendix")

    def test_pdf_evidence_anchor_schema_rejects_unknown_fields(self) -> None:
        if not schema_validator_available():
            self.skipTest("jsonschema is not available")
        payload = {
            "schema_version": "pdf_evidence_anchors.v1",
            "run_date": RUN_DATE,
            "records": [
                {
                    "schema_version": "pdf_evidence_anchors.v1",
                    "run_date": RUN_DATE,
                    "paper_id": "APP",
                    "source_pdf": "attachments/app.pdf",
                    "source_note": "wiki/topics/app.md",
                    "extension_metadata": {"producer": "fixture"},
                    "anchors": [
                        {
                            "anchor_id": "APP-A1",
                            "anchor_type": "appendix",
                            "anchor_source": "manual_pdf_locator",
                            "section": "Appendix A",
                            "page": 12,
                            "snippet": "Appendix supports a strict claim.",
                            "extraction_method": "manual",
                            "confidence": "high",
                            "requires_human_check": False,
                            "extension_metadata": {"note": "allowed explicit extension block"},
                        }
                    ],
                }
            ],
        }
        self.assertEqual(validate_payload(payload, "pdf_evidence_anchors.v1"), [])

        bad_anchor = {
            **payload,
            "records": [
                {
                    **payload["records"][0],
                    "anchors": [
                        {
                            **payload["records"][0]["anchors"][0],
                            "unexpected_field": "reject me",
                        }
                    ],
                }
            ],
        }
        self.assertTrue(any("Additional properties" in issue for issue in validate_payload(bad_anchor, "pdf_evidence_anchors.v1")))

        bad_record = {
            **payload,
            "records": [
                {
                    **payload["records"][0],
                    "unexpected_field": "reject me",
                }
            ],
        }
        self.assertTrue(any("Additional properties" in issue for issue in validate_payload(bad_record, "pdf_evidence_anchors.v1")))

    def test_weak_claims_cannot_become_strong_graph_evidence(self) -> None:
        node = build_nodes(
            [
                {
                    "paper_key": "WEAK",
                    "source_note": "wiki/topics/weak.md",
                    "claims": [
                        {
                            "claim_id": "WEAK-C1",
                            "claim_type": "central_claim",
                            "statement": "Screening-only claim.",
                            "evidence_anchor": "Section 1",
                            "anchor_type": "section",
                            "confidence": "high",
                            "confidence_reason": "bad_input",
                            "summary_origin": "evidence_ledger",
                            "requires_human_check": False,
                            "evidence_class": "not_evidenced",
                            "screening_only": True,
                            "anchor": {"anchor_type": "section", "section": "Section 1", "snippet": "Screening-only claim."},
                        }
                    ],
                }
            ]
        )[0]
        self.assertEqual(node["confidence"], "low")
        self.assertTrue(node["requires_human_check"])


class ReadPaperPromptContractTest(unittest.TestCase):
    def test_prompt_requires_evidence_ledger_no_hardware_and_transfer_risk(self) -> None:
        prompt = (SCRIPTS_DIR.parent / "commands" / "read-paper.md").read_text(encoding="utf-8")
        self.assertIn("## Evidence Ledger", prompt)
        self.assertIn("claim_id", prompt)
        self.assertIn("no robot", prompt)
        self.assertIn("no real scene", prompt)
        self.assertIn("no new data collection", prompt)
        self.assertIn("Transfer distance", prompt)
        self.assertIn("Negative transfer risk", prompt)
