from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401

import daily_arxiv_pipeline as pipeline


RUN_DATE = "2099-05-21"


def audit_payload(*, passed: bool = True, issues: list[str] | None = None, global_warnings: dict | None = None) -> str:
    return json.dumps(
        {
            "target_note": {
                "path": "wiki/topics/audit-fixture.md",
                "zotero_key": "AUDITKEY",
                "issues": issues or [],
                "strict_reading_pass": passed,
            },
            "global_warnings": global_warnings or {
                "topic_issues": [],
                "concept_issues": [],
                "entity_issues": [],
                "tags_missing_from_taxonomy": [],
            },
            "exit_policy": "target_note_only",
        }
    )


class DailyReadTargetAuditTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        command_dir = self.root / ".claude" / "commands"
        command_dir.mkdir(parents=True, exist_ok=True)
        (command_dir / "read-paper.md").write_text("Read $ARGUMENTS strictly.", encoding="utf-8")
        self.patches = [
            patch.object(pipeline, "vault_path", lambda *parts: self.root.joinpath(*parts)),
            patch.object(pipeline, "local_note_status", lambda key: ("done", "wiki/topics/audit-fixture.md")),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self) -> None:
        for item in reversed(self.patches):
            item.stop()
        self.tmp.cleanup()

    def subprocess_side_effect(self, audit_stdout: str, audit_code: int = 0):
        calls: list[list[str]] = []

        def side_effect(command: list[str], **_kwargs):
            calls.append(command)
            if ".claude/scripts/audit_kb.py" in command:
                return audit_code, audit_stdout, ""
            return 0, "read subprocess finished", ""

        return calls, side_effect

    def test_successful_read_requires_target_note_audit_pass(self) -> None:
        calls, side_effect = self.subprocess_side_effect(audit_payload())
        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, output, logs = pipeline.read_zotero_key("AUDITKEY", run_date=RUN_DATE)

        self.assertEqual(status, "success_done")
        self.assertIn("TARGET_NOTE_AUDIT: status=passed", output)
        self.assertTrue(any(".claude/scripts/audit_kb.py" in call for call in calls))
        self.assertEqual(logs["target_note_audit_status"], "passed")
        self.assertEqual(logs["target_note_issues"], [])
        self.assertTrue(logs["audit_json_path"].endswith("AUDITKEY-attempt1-target-note-audit.json"))
        self.assertTrue((self.root / logs["audit_json_path"]).exists())

    def test_target_note_audit_fail_makes_read_fail_even_when_note_is_done(self) -> None:
        calls, side_effect = self.subprocess_side_effect(
            audit_payload(passed=False, issues=["strict_missing_strict_section:Evidence Ledger"]),
            audit_code=1,
        )
        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, output, logs = pipeline.read_zotero_key("AUDITKEY", run_date=RUN_DATE)

        self.assertEqual(status, "failed:target_note_audit")
        self.assertTrue(any(".claude/scripts/audit_kb.py" in call for call in calls))
        self.assertIn("strict_missing_strict_section:Evidence Ledger", output)
        self.assertEqual(logs["target_note_audit_status"], "failed")
        self.assertEqual(logs["target_note_issues"], ["strict_missing_strict_section:Evidence Ledger"])

    def test_global_warnings_do_not_fail_target_note_audit(self) -> None:
        warnings = {
            "topic_issues": [{"path": "wiki/topics/unrelated.md", "issues": ["old_global_issue"]}],
            "concept_issues": [{"path": "wiki/concepts/unrelated.md", "issues": ["stub"]}],
            "entity_issues": [],
            "tags_missing_from_taxonomy": ["robotic-manipulation"],
        }
        calls, side_effect = self.subprocess_side_effect(audit_payload(global_warnings=warnings))
        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, _output, logs = pipeline.read_zotero_key("AUDITKEY", run_date=RUN_DATE)

        self.assertEqual(status, "success_done")
        self.assertTrue(any(".claude/scripts/audit_kb.py" in call for call in calls))
        self.assertEqual(logs["global_warning_counts"]["topic_issues"], 1)
        self.assertEqual(logs["global_warning_counts"]["concept_issues"], 1)
        self.assertEqual(logs["global_warning_counts"]["tags_missing_from_taxonomy"], 1)
        self.assertEqual(logs["global_warning_paths"]["topic_issues"], ["wiki/topics/unrelated.md"])

    def test_existing_done_read_status_remains_success_when_audit_passes(self) -> None:
        calls, side_effect = self.subprocess_side_effect(audit_payload())
        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, output, fields = pipeline.finalize_read_status_with_target_audit(
                zotero_key="AUDITKEY",
                read_status="success_done_already",
                read_output="already done",
                read_attempt_logs=[],
                run_date=RUN_DATE,
            )

        self.assertEqual(status, "success_done_already")
        self.assertIn("TARGET_NOTE_AUDIT: status=passed", output)
        self.assertTrue(any(".claude/scripts/audit_kb.py" in call for call in calls))
        record = {"read_status": status, **fields}
        for key in ["target_note_audit_status", "target_note_issues", "global_warning_counts", "audit_json_path"]:
            self.assertIn(key, record)
        self.assertEqual(record["target_note_audit_status"], "passed")

    def test_existing_done_read_status_fails_when_audit_fails(self) -> None:
        _calls, side_effect = self.subprocess_side_effect(audit_payload(passed=False, issues=["bad"]), audit_code=1)
        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, _output, fields = pipeline.finalize_read_status_with_target_audit(
                zotero_key="AUDITKEY",
                read_status="success_done_already",
                read_output="already done",
                read_attempt_logs=[],
                run_date=RUN_DATE,
            )

        self.assertEqual(status, "failed:target_note_audit")
        self.assertEqual(fields["target_note_issues"], ["bad"])
