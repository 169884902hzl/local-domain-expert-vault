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

    def complete_final_analysis(self) -> str:
        body = "\n\n".join(
            f"{section}\n" + ("Evidence-grounded staged analysis content. " * 20)
            for section in pipeline.STAGED_REQUIRED_FINAL_SECTIONS
        )
        return body + "\n"

    def test_staged_read_uses_one_session_and_requires_complete_final_analysis(self) -> None:
        calls: list[list[str]] = []

        def side_effect(command: list[str], **_kwargs):
            calls.append(command)
            if command and command[0] == "claude":
                stage_id = pipeline.STAGED_READ_STAGES[len([call for call in calls if call and call[0] == "claude"]) - 1][0]
                stage_dir = pipeline.staged_read_root("AUDITKEY", attempt=1)
                stage_path = pipeline._stage_output_path(stage_dir, stage_id)
                stage_path.parent.mkdir(parents=True, exist_ok=True)
                stage_path.write_text(f"# {stage_id}\n" + ("stage checkpoint " * 80), encoding="utf-8")
                if stage_id == "05-assemble-final-analysis":
                    final_path = pipeline._final_analysis_path("AUDITKEY")
                    final_path.parent.mkdir(parents=True, exist_ok=True)
                    final_path.write_text(self.complete_final_analysis(), encoding="utf-8")
                return 0, f"{stage_id} finished", ""
            if ".claude/scripts/finalize_reading.py" in command:
                return 0, "finalized", ""
            if ".claude/scripts/audit_kb.py" in command:
                return 0, audit_payload(), ""
            return 0, "", ""

        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, output, logs = pipeline.read_zotero_key_staged("AUDITKEY", run_date=RUN_DATE)

        self.assertEqual(status, "success_done")
        self.assertIn("STAGED_FINALIZE exit_code=0", output)
        self.assertTrue((self.root / "raw" / "readings" / "AUDITKEY-analysis.md").exists())
        claude_calls = [call for call in calls if call and call[0] == "claude"]
        self.assertEqual(len(claude_calls), len(pipeline.STAGED_READ_STAGES))
        session_ids = {
            call[call.index("--session-id") + 1]
            for call in claude_calls
            if "--session-id" in call
        }
        self.assertEqual(session_ids, {pipeline.staged_session_id("AUDITKEY", attempt=1)})
        self.assertTrue(logs["staged_manifest"].endswith("raw/readings/_staged/AUDITKEY/attempt-1/manifest.json"))
        manifest = json.loads((self.root / logs["staged_manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "success_done")
        self.assertEqual(manifest["final_analysis_path"], "raw/readings/AUDITKEY-analysis.md")

    def test_staged_read_fails_when_assembly_does_not_write_complete_analysis(self) -> None:
        def side_effect(command: list[str], **_kwargs):
            if command and command[0] == "claude":
                stage_index = len(list((self.root / "raw" / "readings" / "_staged" / "AUDITKEY" / "attempt-1").glob("*.md")))
                stage_id = pipeline.STAGED_READ_STAGES[stage_index][0]
                stage_dir = pipeline.staged_read_root("AUDITKEY", attempt=1)
                stage_path = pipeline._stage_output_path(stage_dir, stage_id)
                stage_path.parent.mkdir(parents=True, exist_ok=True)
                stage_path.write_text(f"# {stage_id}\n" + ("stage checkpoint " * 80), encoding="utf-8")
                if stage_id == "05-assemble-final-analysis":
                    final_path = pipeline._final_analysis_path("AUDITKEY")
                    final_path.parent.mkdir(parents=True, exist_ok=True)
                    final_path.write_text("## Evidence Metadata\nincomplete\n", encoding="utf-8")
                return 0, f"{stage_id} finished", ""
            return 0, "", ""

        with patch.object(pipeline, "run_subprocess_capture", side_effect=side_effect):
            status, output, logs = pipeline.read_zotero_key_staged("AUDITKEY", run_date=RUN_DATE)

        self.assertEqual(status, "failed:staged_stage_failed")
        self.assertIn("05-assemble-final-analysis", output)
        last_stage = logs["stages"][-1]
        self.assertIn("final_analysis_too_short", last_stage["missing"])
        self.assertIn("## Problem", last_stage["missing"])

    def test_staged_timed_read_does_not_retry_whole_paper(self) -> None:
        calls: list[int] = []

        def staged_fail(*_args, **_kwargs):
            calls.append(1)
            return "failed:timeout", "stage timed out", {"attempt": 1}

        with patch.object(pipeline, "read_zotero_key_staged", side_effect=staged_fail):
            status, output, _elapsed, logs = pipeline.read_zotero_key_timed(
                "AUDITKEY",
                timeout=4200,
                run_date=RUN_DATE,
                max_attempts=3,
                read_mode="staged",
            )

        self.assertEqual(status, "failed:timeout")
        self.assertIn("READ_ATTEMPT 1/1: mode=staged status=failed:timeout", output)
        self.assertIn("stage timed out", output)
        self.assertEqual(len(logs), 1)
        self.assertEqual(len(calls), 1)
