from __future__ import annotations

import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch

from audit_scheduled_tasks import ExpectedTask, audit_task


TASK_XML = """<?xml version="1.0" encoding="UTF-16"?>
<Task xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2099-03-04T12:00:00</StartBoundary>
      <ScheduleByDay><DaysInterval>1</DaysInterval></ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Settings>
    {enabled}
    <StartWhenAvailable>true</StartWhenAvailable>
  </Settings>
  <Actions Context="Author">
    <Exec><Arguments>{script}</Arguments></Exec>
  </Actions>
</Task>
"""


class AuditScheduledTasksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.task_path = root / "Task.xml"
        self.script = root / "wrapper.ps1"
        self.log = root / "task.log"
        self.script.write_text("automation_pause_guard.ps1\nTest-VaultAutomationPaused\n", encoding="utf-8")
        self.log.write_text("[2099-03-04 12:00:00 +08:00] START\n[2099-03-04 12:01:00 +08:00] END exit_code=0\n", encoding="utf-8")
        self.expected = ExpectedTask(
            name="ExampleTask",
            script=self.script,
            log_path=self.log,
            schedule="daily",
            expected_local_time="12:00",
            max_log_age_hours=999999,
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_task_xml(self, enabled: str) -> None:
        self.task_path.write_text(TASK_XML.format(enabled=enabled, script=self.script), encoding="utf-16")

    def audit_with_runtime_state(self, scheduled_state: str, active_pauses: list[dict] | None = None) -> dict:
        query = {
            "ok": True,
            "parsed": {
                "runtime_status": "Ready",
                "scheduled_task_state": scheduled_state,
                "last_result": "0",
                "last_run_time": "2099/03/04 12:01:00",
            },
        }
        with patch("audit_scheduled_tasks._system_task_path", return_value=self.task_path), patch("audit_scheduled_tasks._run_query", return_value=query):
            return audit_task(self.expected, active_pauses or [])

    def test_absent_enabled_uses_runtime_enabled_without_task_disabled(self) -> None:
        self.write_task_xml("")
        result = self.audit_with_runtime_state("Enabled")
        self.assertNotIn("task_disabled", result["errors"])
        self.assertIn("task_enabled_by_default_absent_xml_enabled", result["notes"])

    def test_explicit_false_is_task_disabled(self) -> None:
        self.write_task_xml("<Enabled>false</Enabled>")
        result = self.audit_with_runtime_state("Disabled")
        self.assertIn("task_disabled", result["errors"])

    def test_active_pause_still_notes_explicit_disabled(self) -> None:
        self.write_task_xml("<Enabled>false</Enabled>")
        result = self.audit_with_runtime_state("Disabled", [{"disabled_tasks": ["ExampleTask"]}])
        self.assertIn("task_disabled_by_active_pause", result["notes"])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
