from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401

import canonical_baseline_backfill as backfill
import daily_arxiv_pipeline as pipeline


def write_done_literature_note(root: Path, rel_path: str, *, title: str, zotero_key: str, body: str) -> Path:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "---",
                f'title: "{title}"',
                "tags: [paper]",
                'created: "2099-01-01"',
                'updated: "2099-01-01"',
                'type: "literature"',
                'status: "done"',
                f'zotero_key: "{zotero_key}"',
                'summary: "fixture summary"',
                "---",
                "",
                body,
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


class CanonicalBaselineBackfillTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_repeated_strongest_baseline_enters_queue_when_canonical_note_missing(self) -> None:
        write_done_literature_note(
            self.root,
            "wiki/topics/paper-a.md",
            title="Paper A",
            zotero_key="AAAAAAA",
            body=(
                "## Baseline Pressure\n\n"
                "- Strongest Baseline: HIL-SERL as real-world human-in-the-loop robot manipulation baseline.\n"
            ),
        )
        write_done_literature_note(
            self.root,
            "wiki/topics/paper-b.md",
            title="Paper B",
            zotero_key="BBBBBBB",
            body=(
                "## Evidence Ledger\n\n"
                "| claim_id | claim_type | claim | evidence_class | anchor_type | anchor | page | confidence | downstream_use |\n"
                "| C1 | baseline | HIL-SERL is the pressure baseline for dexterous robot policy learning. | pdf_verified | section | Sec. 5 | Sec5 | high | strong_evidence |\n"
            ),
        )

        report = backfill.build_baseline_backfill_report(run_date="2099-01-02", root=self.root, min_mentions=2)
        hil = next(item for item in report["entries"] if item["normalized_label"] == "hil-serl")

        self.assertEqual(hil["status"], "queued")
        self.assertEqual(hil["coverage_status"], "missing_canonical_note")
        self.assertEqual(hil["source_note_count"], 2)
        self.assertGreaterEqual(hil["priority_score"], 1)
        self.assertEqual(report["queued_total"], 1)

    def test_alias_title_prevents_queue_for_existing_hil_serl_canonical_note(self) -> None:
        for suffix in ["a", "b"]:
            write_done_literature_note(
                self.root,
                f"wiki/topics/source-{suffix}.md",
                title=f"Source {suffix}",
                zotero_key=f"SRC{suffix.upper()}",
                body=(
                    "## Baseline Pressure\n\n"
                    "- Strongest Baseline: HIL-SERL for real-world robot manipulation.\n"
                ),
            )
        write_done_literature_note(
            self.root,
            "wiki/topics/luo2025precise.md",
            title="Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning",
            zotero_key="6BDBGP7T",
            body="## Baseline Pressure\n\n- Strongest Baseline: not_evidenced\n",
        )

        report = backfill.build_baseline_backfill_report(run_date="2099-01-02", root=self.root, min_mentions=2)
        hil = next(item for item in report["entries"] if item["normalized_label"] == "hil-serl")

        self.assertEqual(hil["status"], "covered")
        self.assertEqual(hil["coverage_status"], "covered_by_alias_title")
        self.assertEqual(hil["covered_by"]["zotero_key"], "6BDBGP7T")
        self.assertEqual(report["queued_total"], 0)

    def test_daily_run_log_renders_baseline_backfill_queue(self) -> None:
        idea_path = self.root / "projects" / "ideas" / "2099-01-02-ideas.md"
        agenda_path = self.root / "projects" / "research-agenda" / "daily" / "2099-01-02-agenda.md"
        gemini_path = self.root / "projects" / "ideas" / "2099-01-02-gemini.md"
        for path in [idea_path, agenda_path, gemini_path]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

        report = {
            "queued_total": 1,
            "json_path": "projects/arxiv-daily/baseline-backfill/2099-01-02-baseline-backfill.json",
            "md_path": "projects/arxiv-daily/baseline-backfill/2099-01-02-baseline-backfill.md",
            "entries": [
                {
                    "status": "queued",
                    "label": "HIL-SERL",
                    "priority_score": 75,
                    "source_note_count": 2,
                    "mention_count": 3,
                    "search_query": '"HIL-SERL" robot manipulation baseline',
                }
            ],
        }
        with patch.object(pipeline, "vault_path", lambda *parts: self.root.joinpath(*parts)):
            text = pipeline.render_run_log(
                run_date="2099-01-02",
                status="success",
                ranked=[],
                imports=[],
                reads=[],
                idea_path=idea_path,
                agenda_delta_path=agenda_path,
                gemini_prompt_path=gemini_path,
                idea_audit={"status": "not_applicable"},
                idea_generation={"mode": "research_agenda_update", "status": "skipped_no_focus_keys"},
                errors=[],
                import_policy={},
                existing_candidates=[],
                baseline_backfill=report,
            )

        self.assertIn("## Canonical Baseline Backfill", text)
        self.assertIn("baseline_backfill_queued: 1", text)
        self.assertIn("HIL-SERL priority=75", text)
        self.assertIn("queue only", text)


if __name__ == "__main__":
    unittest.main()
