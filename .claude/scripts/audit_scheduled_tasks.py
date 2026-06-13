"""Audit Windows scheduled task health for the vault automations."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path


TASK_NS = {"task": "http://schemas.microsoft.com/windows/2004/02/mit/task"}


@dataclass(frozen=True)
class ExpectedTask:
    name: str
    script: Path
    log_path: Path
    schedule: str
    expected_local_time: str
    max_log_age_hours: int


def _system_task_path(name: str) -> Path:
    return Path("C:/Windows/System32/Tasks") / name


def _expected_tasks() -> list[ExpectedTask]:
    root = vault_path()
    return [
        ExpectedTask(
            name="DailyArxivEmbodiedAIScout",
            script=root / ".claude/scripts/run_daily_arxiv_task.ps1",
            log_path=root / "projects/arxiv-daily/scheduled-task.log",
            schedule="daily",
            expected_local_time="12:00",
            max_log_age_hours=36,
        ),
        ExpectedTask(
            name="WeeklyResearchAgendaReview",
            script=root / ".claude/scripts/run_weekly_agenda_review_task.ps1",
            log_path=root / "projects/research-agenda/reviews/weekly-agenda-review-task.log",
            schedule="weekly",
            expected_local_time="20:00",
            max_log_age_hours=24 * 8,
        ),
        ExpectedTask(
            name="DailyCodexSeedReview",
            script=root / ".claude/scripts/run_daily_codex_seed_review_task.ps1",
            log_path=root / "projects/research-agenda/reviews/daily-codex-seed-review-task.log",
            schedule="daily",
            expected_local_time="16:30",
            max_log_age_hours=48,
        ),
    ]


def _parse_iso_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _pause_superseded(pause_path: Path, paused_at: datetime, resume_payloads: list[dict[str, Any]]) -> bool:
    pause_leaf = pause_path.name
    for payload in resume_payloads:
        prior = str(payload.get("prior_pause_record") or "")
        if prior != str(pause_path) and not prior.endswith(pause_leaf):
            continue
        resumed_at = _parse_iso_datetime(str(payload.get("resumed_at") or ""))
        if resumed_at and resumed_at > paused_at:
            return True
    return False


def _load_pause_payloads() -> tuple[list[tuple[Path, dict[str, Any]]], list[dict[str, Any]]]:
    pause_dir = vault_path("projects/arxiv-daily/pauses")
    if not pause_dir.exists():
        return [], []
    pauses: list[tuple[Path, dict[str, Any]]] = []
    resumes: list[dict[str, Any]] = []
    for path in sorted(pause_dir.glob("pause-*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            pauses.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except Exception:
            continue
    for path in sorted(pause_dir.glob("resume-*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            resumes.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return pauses, resumes


def active_pause_records(now: datetime | None = None) -> list[dict[str, Any]]:
    current = now or datetime.now().astimezone()
    today = current.strftime("%Y-%m-%d")
    pauses, resumes = _load_pause_payloads()
    active: list[dict[str, Any]] = []
    for path, payload in pauses:
        if payload.get("schema_version") != "vault_automation_pause.v1":
            continue
        paused_at = _parse_iso_datetime(str(payload.get("paused_at") or ""))
        if not paused_at:
            continue
        if _pause_superseded(path, paused_at, resumes):
            continue
        paused_dates = {str(item) for item in payload.get("paused_dates") or []}
        resume_not_before = _parse_iso_datetime(str(payload.get("intended_resume_not_before") or ""))
        date_active = today in paused_dates
        time_active = bool(resume_not_before and current < resume_not_before)
        if not (date_active or time_active):
            continue
        active.append(
            {
                "path": str(path),
                "pause_reason": payload.get("pause_reason", ""),
                "disabled_tasks": [str(item) for item in payload.get("disabled_tasks") or []],
                "paused_dates": sorted(paused_dates),
                "intended_resume_not_before": payload.get("intended_resume_not_before", ""),
            }
        )
    return active


def _pause_records_for_task(task_name: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [record for record in records if task_name in set(record.get("disabled_tasks") or [])]


def _text(node: ET.Element | None) -> str:
    return "" if node is None or node.text is None else node.text.strip()


def _task_xml(path: Path) -> ET.Element | None:
    try:
        return ET.fromstring(path.read_text(encoding="utf-16"))
    except Exception:
        return None


def _run_query(name: str) -> dict[str, Any]:
    attempts = []
    for task_name in [name, f"\\{name}"]:
        command = ["schtasks.exe", "/Query", "/TN", task_name, "/FO", "LIST", "/V"]
        try:
            proc = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=20)
        except Exception as exc:
            attempts.append({"task_name": task_name, "ok": False, "error": f"{type(exc).__name__}:{exc}"})
            continue
        output = ((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")).strip()
        attempt = {
            "task_name": task_name,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "parsed": _parse_schtasks_list(output) if proc.returncode == 0 else {},
            "output_tail": output[-800:],
        }
        attempts.append(attempt)
        if proc.returncode == 0:
            return {
                "ok": True,
                "method": "schtasks",
                "attempts": attempts,
                "parsed": attempt["parsed"],
                "output_tail": output[-800:],
            }
    return {"ok": False, "method": "schtasks", "attempts": attempts, "output_tail": attempts[-1].get("output_tail", "") if attempts else ""}


def _parse_schtasks_list(output: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    key_map = {
        "TaskName": "task_name",
        "Next Run Time": "next_run_time",
        "Status": "runtime_status",
        "Last Run Time": "last_run_time",
        "Last Result": "last_result",
        "Scheduled Task State": "scheduled_task_state",
        "Start Time": "start_time",
        "Start Date": "start_date",
        "Days": "days",
    }
    for line in output.splitlines():
        if ":" not in line:
            continue
        raw_key, raw_value = line.split(":", 1)
        key = key_map.get(raw_key.strip())
        if key:
            parsed[key] = raw_value.strip()
    return parsed


def _last_run_is_never(value: str) -> bool:
    return (not value) or value.startswith("1999/11/30") or value.upper() in {"N/A", "NEVER"}


def _latest_log_status(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    starts = re.findall(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) [^\]]+\] START", text)
    ends = re.findall(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) [^\]]+\] END exit_code=(\d+)", text)
    latest_start = starts[-1] if starts else ""
    latest_end, exit_code = ends[-1] if ends else ("", "")
    age_hours = None
    if latest_end:
        age_hours = round((datetime.now() - datetime.strptime(latest_end, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600, 2)
    return {
        "exists": True,
        "latest_start": latest_start,
        "latest_end": latest_end,
        "latest_exit_code": int(exit_code) if exit_code else None,
        "age_hours": age_hours,
    }


def _classify_latest_run(task_name: str, log: dict[str, Any], log_path: Path) -> dict[str, Any]:
    if not log.get("exists"):
        return {
            "status": "missing_log",
            "severity": "warning",
            "reason": "missing_run_log",
        }
    exit_code = log.get("latest_exit_code")
    if exit_code == 0:
        return {
            "status": "success",
            "severity": "ok",
            "reason": "latest_wrapper_exit_0",
        }
    if task_name == "DailyCodexSeedReview" and _codex_latest_skip_is_catchup_safe(log_path):
        return {
            "status": "skipped_waiting_for_daily_pipeline",
            "severity": "info",
            "reason": "no_ready_catchup_candidate",
        }
    if exit_code is None:
        return {
            "status": "unknown",
            "severity": "warning",
            "reason": "missing_latest_end",
        }
    return {
        "status": "business_partial",
        "severity": "info",
        "reason": f"latest_wrapper_exit_{exit_code}",
    }


def _codex_latest_skip_is_catchup_safe(path: Path) -> bool:
    if not path.exists():
        return False
    tail = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[-80:])
    return "status=skipped_waiting_for_daily_pipeline" in tail and "selection_reason=no_catch_up_candidate" in tail


def _codex_latest_review_done() -> bool:
    reviews_dir = vault_path("projects/research-agenda/reviews")
    files = sorted(
        reviews_dir.glob("*-codex-seed-review.md"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not files:
        return False
    text = files[0].read_text(encoding="utf-8", errors="replace")
    return 'status: "done"' in text or "status: done" in text or "- status: `done`" in text


def _latest_quality_audit() -> dict[str, Any]:
    quality_dir = vault_path("projects/arxiv-daily/quality")
    if not quality_dir.exists():
        return {"exists": False}
    files = sorted(quality_dir.glob("*-daily-quality-audit.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not files:
        return {"exists": False}
    path = files[0]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"exists": True, "path": str(path), "error": f"{type(exc).__name__}:{exc}"}
    return {
        "exists": True,
        "path": str(path),
        "run_date": payload.get("run_date", ""),
        "quality_readiness": payload.get("quality_readiness", ""),
        "issue_counts": payload.get("issue_counts", {}),
    }


def _parse_schtasks_time(value: str) -> datetime | None:
    if not value:
        return None
    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    match = re.match(r"^(\d{4})/(\d{1,2})/(\d{1,2}) (\d{1,2}):(\d{2}):(\d{2})$", value)
    if not match:
        return None
    year, month, day, hour, minute, second = [int(part) for part in match.groups()]
    return datetime(year, month, day, hour, minute, second)


def _local_start(root: ET.Element) -> str:
    # Task files store UTC timestamps with Z in this vault's current registration.
    raw = _text(root.find(".//task:StartBoundary", TASK_NS))
    if not raw:
        return ""
    try:
        if raw.endswith("Z"):
            value = datetime.fromisoformat(raw[:-1] + "+00:00").astimezone()
        else:
            value = datetime.fromisoformat(raw)
    except ValueError:
        return raw
    return value.strftime("%H:%M")


def audit_task(expected: ExpectedTask, active_pauses: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    notes: list[str] = []
    business_warnings: list[str] = []
    task_pauses = _pause_records_for_task(expected.name, active_pauses or [])
    pause_active = bool(task_pauses)
    task_path = _system_task_path(expected.name)
    xml_root = _task_xml(task_path) if task_path.exists() else None
    xml_info: dict[str, Any] = {"path": str(task_path), "exists": task_path.exists()}

    if xml_root is None:
        errors.append("missing_or_unreadable_task_xml")
    else:
        enabled = _text(xml_root.find(".//task:Settings/task:Enabled", TASK_NS)).lower()
        start_when_available = _text(xml_root.find(".//task:Settings/task:StartWhenAvailable", TASK_NS)).lower()
        action = _text(xml_root.find(".//task:Actions/task:Exec/task:Arguments", TASK_NS))
        local_start = _local_start(xml_root)
        days = [node.tag.rsplit("}", 1)[-1] for node in xml_root.findall(".//task:DaysOfWeek/*", TASK_NS)]
        daily_interval = _text(xml_root.find(".//task:ScheduleByDay/task:DaysInterval", TASK_NS))
        xml_info.update(
            {
                "enabled": enabled,
                "start_when_available": start_when_available,
                "action": action,
                "local_start": local_start,
                "days": days,
                "daily_interval": daily_interval,
            }
        )
        if enabled == "true" and pause_active:
            errors.append("task_enabled_during_active_pause")
        elif enabled != "true" and pause_active:
            notes.append("task_disabled_by_active_pause")
        elif enabled != "true":
            errors.append("task_disabled")
        if str(expected.script) not in action:
            errors.append("action_does_not_point_to_expected_wrapper")
        if local_start and local_start != expected.expected_local_time:
            warnings.append(f"unexpected_start_time:{local_start}:expected:{expected.expected_local_time}")
        if start_when_available != "true":
            warnings.append("start_when_available_false")
        if expected.schedule == "daily" and daily_interval != "1":
            errors.append(f"daily_interval_not_1:{daily_interval}")
        if expected.schedule == "weekly" and "Sunday" not in days:
            errors.append(f"weekly_not_sunday:{','.join(days) or '-'}")

    if not expected.script.exists():
        errors.append("missing_wrapper_script")
    else:
        script_text = expected.script.read_text(encoding="utf-8", errors="replace")
        if "automation_pause_guard.ps1" not in script_text or "Test-VaultAutomationPaused" not in script_text:
            errors.append("missing_wrapper_pause_guard")

    query = _run_query(expected.name)
    if not query.get("ok"):
        notes.append("runtime_query_unavailable:schtasks_query_failed")
    else:
        runtime = query.get("parsed", {})
        runtime_status = runtime.get("runtime_status", "").lower()
        scheduled_state = runtime.get("scheduled_task_state", "").lower()
        last_result = runtime.get("last_result", "")
        last_run_time = runtime.get("last_run_time", "")
        if runtime_status and pause_active and runtime_status in {"ready", "running"}:
            errors.append(f"runtime_status_not_disabled_during_active_pause:{runtime_status}")
        elif runtime_status and runtime_status not in {"ready", "running"}:
            if pause_active and runtime_status == "disabled":
                notes.append("runtime_status_disabled_by_active_pause")
            else:
                warnings.append(f"unexpected_runtime_status:{runtime_status}")
        if scheduled_state and pause_active and scheduled_state == "enabled":
            errors.append("scheduled_task_state_enabled_during_active_pause")
        elif scheduled_state and scheduled_state != "enabled":
            if pause_active and scheduled_state == "disabled":
                notes.append("scheduled_task_state_disabled_by_active_pause")
            else:
                errors.append(f"scheduled_task_state_not_enabled:{scheduled_state}")
        if last_result and last_result != "0":
            if runtime_status == "running" and last_result == "267009":
                notes.append(f"scheduler_task_running:last_result:{last_result}")
            elif _last_run_is_never(last_run_time):
                notes.append(f"scheduler_not_yet_run:last_result:{last_result}")
            else:
                log = _latest_log_status(expected.log_path)
                latest_end = None
                if log.get("latest_end"):
                    latest_end = datetime.strptime(str(log["latest_end"]), "%Y-%m-%d %H:%M:%S")
                scheduler_last_run = _parse_schtasks_time(last_run_time)
                if log.get("latest_exit_code") == 0 and latest_end and scheduler_last_run and latest_end > scheduler_last_run:
                    notes.append(f"stale_scheduler_result:last_result:{last_result}:latest_wrapper_exit:0")
                elif expected.name == "DailyCodexSeedReview" and _codex_latest_review_done():
                    notes.append(f"codex_review_done_despite_scheduler_result:last_result:{last_result}")
                else:
                    business_warnings.append(f"scheduler_last_result_nonzero:{last_result}")

    log = _latest_log_status(expected.log_path)
    latest_run = _classify_latest_run(expected.name, log, expected.log_path)
    if not log.get("exists"):
        warnings.append("missing_run_log")
    else:
        if log.get("latest_exit_code") not in {0, None}:
            if expected.name == "DailyCodexSeedReview" and _codex_latest_skip_is_catchup_safe(expected.log_path):
                notes.append(f"codex_review_no_ready_catchup_candidate:last_exit:{log.get('latest_exit_code')}")
            elif expected.name == "DailyCodexSeedReview" and _codex_latest_review_done():
                notes.append(f"codex_review_done_despite_wrapper_exit:{log.get('latest_exit_code')}")
            else:
                business_warnings.append(f"last_exit_nonzero:{log.get('latest_exit_code')}")
        age = log.get("age_hours")
        if age is not None and age > expected.max_log_age_hours:
            warnings.append(f"log_stale_hours:{age}")

    if not query.get("ok") and (xml_root is None or not log.get("exists")):
        warnings.append("runtime_query_failed_without_xml_or_log_fallback")

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "task": expected.name,
        "status": status,
        "scheduler_health": status,
        "latest_run_status": latest_run,
        "expected": {
            "schedule": expected.schedule,
            "local_time": expected.expected_local_time,
            "wrapper": str(expected.script),
            "log_path": str(expected.log_path),
        },
        "xml": xml_info,
        "active_pause_records": task_pauses,
        "schtasks_query": query,
        "log": log,
        "errors": errors,
        "warnings": warnings,
        "business_warnings": business_warnings,
        "notes": notes,
    }


def audit() -> dict[str, Any]:
    pauses = active_pause_records()
    tasks = [audit_task(item, pauses) for item in _expected_tasks()]
    errors = [f"{item['task']}:{error}" for item in tasks for error in item["errors"]]
    warnings = [f"{item['task']}:{warning}" for item in tasks for warning in item["warnings"]]
    business_warnings = [
        f"{item['task']}:{warning}" for item in tasks for warning in item.get("business_warnings", [])
    ]
    quality_audit = _latest_quality_audit()
    pause_notes: list[str] = []
    daily_paused = bool(_pause_records_for_task("DailyArxivEmbodiedAIScout", pauses))
    if quality_audit.get("exists") and quality_audit.get("quality_readiness") not in {"", "ready"}:
        quality_note = (
            f"DailyArxivEmbodiedAIScout:latest_quality_readiness:{quality_audit.get('quality_readiness')}:"
            f"run_date:{quality_audit.get('run_date')}"
        )
        if daily_paused:
            pause_notes.append(f"paused_prior_business_warning:{quality_note}")
        else:
            business_warnings.append(quality_note)
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    latest_run_status = "WARN" if business_warnings else "PASS"
    return {
        "status": status,
        "scheduler_health": status,
        "latest_run_status": latest_run_status,
        "tasks": tasks,
        "errors": errors,
        "warnings": warnings,
        "business_warnings": business_warnings,
        "latest_quality_audit": quality_audit,
        "active_pause_records": pauses,
        "pause_notes": pause_notes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(
            f"{result['status']} scheduled_tasks={len(result['tasks'])} "
            f"scheduler_health={result['scheduler_health']} latest_run_status={result['latest_run_status']}"
        )
        for error in result["errors"]:
            safe_print(f"ERROR: {error}")
        for warning in result["warnings"]:
            safe_print(f"WARN: {warning}")
        for warning in result.get("business_warnings", []):
            safe_print(f"INFO: previous_business_run_not_success:{warning}")
        for note in result.get("pause_notes", []):
            safe_print(f"INFO: {note}")
        for item in result["tasks"]:
            for note in item.get("notes", []):
                safe_print(f"INFO: {item['task']}:{note}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
