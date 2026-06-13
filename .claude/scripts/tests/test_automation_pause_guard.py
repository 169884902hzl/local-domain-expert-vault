from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from v03_test_helpers import SCRIPTS_DIR

import audit_scheduled_tasks as audit_tasks


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class AutomationPauseGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.pause_dir = self.root / "projects" / "arxiv-daily" / "pauses"
        self.pause_dir.mkdir(parents=True, exist_ok=True)
        self.patch_vault = patch.object(audit_tasks, "vault_path", lambda *parts: self.root.joinpath(*parts))
        self.patch_vault.start()

    def tearDown(self) -> None:
        self.patch_vault.stop()
        self.tmp.cleanup()

    def test_active_pause_ignores_superseded_prior_pause(self) -> None:
        old_pause = self.pause_dir / "pause-20260524-150402.json"
        write_json(
            old_pause,
            {
                "schema_version": "vault_automation_pause.v1",
                "paused_at": "2026-05-24T15:04:02+08:00",
                "paused_dates": ["2026-05-24", "2026-05-25", "2026-05-26"],
                "intended_resume_not_before": "2026-05-27T00:00:00+08:00",
                "disabled_tasks": ["DailyArxivEmbodiedAIScout"],
            },
        )
        write_json(
            self.pause_dir / "resume-20260524-150810.json",
            {
                "schema_version": "vault_automation_resume.v1",
                "resumed_at": "2026-05-24T15:08:11+08:00",
                "prior_pause_record": "projects/arxiv-daily/pauses/pause-20260524-150402.json",
            },
        )
        write_json(
            self.pause_dir / "pause-20260525-185942.json",
            {
                "schema_version": "vault_automation_pause.v1",
                "paused_at": "2026-05-25T18:59:42+08:00",
                "paused_dates": ["2026-05-25", "2026-05-26"],
                "intended_resume_not_before": "2026-05-27T00:00:00+08:00",
                "disabled_tasks": ["DailyArxivEmbodiedAIScout", "DailyCodexSeedReview"],
            },
        )

        records = audit_tasks.active_pause_records(now=datetime.fromisoformat("2026-05-25T19:00:00+08:00"))

        self.assertEqual(len(records), 1)
        self.assertTrue(records[0]["path"].endswith("pause-20260525-185942.json"))
        self.assertIn("DailyCodexSeedReview", records[0]["disabled_tasks"])

    def task_xml(self, path: Path, script: Path, enabled: bool = False) -> None:
        enabled_text = "true" if enabled else "false"
        text = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-05-21T04:00:00Z</StartBoundary>
      <ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Settings>
    <Enabled>{enabled_text}</Enabled>
    <StartWhenAvailable>true</StartWhenAvailable>
  </Settings>
  <Actions><Exec><Arguments>-File "{script}"</Arguments></Exec></Actions>
</Task>
"""
        path.write_text(text, encoding="utf-16")

    def expected_task(self, script: Path, log_path: Path) -> audit_tasks.ExpectedTask:
        return audit_tasks.ExpectedTask(
            name="DailyArxivEmbodiedAIScout",
            script=script,
            log_path=log_path,
            schedule="daily",
            expected_local_time="12:00",
            max_log_age_hours=36,
        )

    def test_disabled_task_passes_scheduler_health_during_active_pause(self) -> None:
        script = self.root / ".claude" / "scripts" / "run_daily_arxiv_task.ps1"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("automation_pause_guard.ps1\nTest-VaultAutomationPaused\n", encoding="utf-8")
        log_path = self.root / "projects" / "arxiv-daily" / "scheduled-task.log"
        task_xml = self.root / "DailyArxivEmbodiedAIScout.xml"
        self.task_xml(task_xml, script, enabled=False)
        query = {
            "ok": True,
            "parsed": {
                "runtime_status": "Disabled",
                "scheduled_task_state": "Disabled",
                "last_result": "0",
                "last_run_time": "2026/5/25 12:00:00",
            },
        }
        active_pause = [{"disabled_tasks": ["DailyArxivEmbodiedAIScout"], "path": "pause.json"}]

        with (
            patch.object(audit_tasks, "_system_task_path", return_value=task_xml),
            patch.object(audit_tasks, "_run_query", return_value=query),
            patch.object(audit_tasks, "_latest_log_status", return_value={"exists": True, "latest_exit_code": 0}),
        ):
            result = audit_tasks.audit_task(self.expected_task(script, log_path), active_pause)

        self.assertEqual(result["status"], "PASS")
        self.assertIn("task_disabled_by_active_pause", result["notes"])
        self.assertIn("runtime_status_disabled_by_active_pause", result["notes"])
        self.assertIn("scheduled_task_state_disabled_by_active_pause", result["notes"])

    def test_enabled_task_fails_during_active_pause(self) -> None:
        script = self.root / ".claude" / "scripts" / "run_daily_arxiv_task.ps1"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("automation_pause_guard.ps1\nTest-VaultAutomationPaused\n", encoding="utf-8")
        log_path = self.root / "projects" / "arxiv-daily" / "scheduled-task.log"
        task_xml = self.root / "DailyArxivEmbodiedAIScout.xml"
        self.task_xml(task_xml, script, enabled=True)
        query = {
            "ok": True,
            "parsed": {
                "runtime_status": "Ready",
                "scheduled_task_state": "Enabled",
                "last_result": "0",
                "last_run_time": "2026/5/25 12:00:00",
            },
        }
        active_pause = [{"disabled_tasks": ["DailyArxivEmbodiedAIScout"], "path": "pause.json"}]

        with (
            patch.object(audit_tasks, "_system_task_path", return_value=task_xml),
            patch.object(audit_tasks, "_run_query", return_value=query),
            patch.object(audit_tasks, "_latest_log_status", return_value={"exists": True, "latest_exit_code": 0}),
        ):
            result = audit_tasks.audit_task(self.expected_task(script, log_path), active_pause)

        self.assertIn("task_enabled_during_active_pause", result["errors"])
        self.assertIn("runtime_status_not_disabled_during_active_pause:ready", result["errors"])
        self.assertIn("scheduled_task_state_enabled_during_active_pause", result["errors"])

    def test_audit_suppresses_prior_quality_warning_during_active_pause(self) -> None:
        pause = [{"disabled_tasks": ["DailyArxivEmbodiedAIScout"], "path": "pause.json"}]
        with (
            patch.object(audit_tasks, "active_pause_records", return_value=pause),
            patch.object(audit_tasks, "_expected_tasks", return_value=[]),
            patch.object(
                audit_tasks,
                "_latest_quality_audit",
                return_value={"exists": True, "quality_readiness": "blocked", "run_date": "2026-05-25"},
            ),
        ):
            result = audit_tasks.audit()

        self.assertEqual(result["latest_run_status"], "PASS")
        self.assertEqual(result["business_warnings"], [])
        self.assertIn("paused_prior_business_warning:DailyArxivEmbodiedAIScout:latest_quality_readiness:blocked:run_date:2026-05-25", result["pause_notes"])

    def test_register_scripts_refuse_non_dry_run_during_active_pause(self) -> None:
        for script_name in [
            "register_daily_arxiv_task.ps1",
            "register_daily_codex_seed_review_task.ps1",
            "register_weekly_agenda_review_task.ps1",
        ]:
            text = (SCRIPTS_DIR / script_name).read_text(encoding="utf-8")
            self.assertIn("[switch]$IgnorePauseGuard", text, script_name)
            self.assertIn("Test-VaultAutomationPaused", text, script_name)
            self.assertIn("scheduled_task_pause_active_refusing_register", text, script_name)


if __name__ == "__main__":
    unittest.main()
