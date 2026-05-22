"""Thin adapter for calling OpenCode CLI with structured, secret-safe output."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


DEFAULT_OPENCODE_MODEL = "deepseek/deepseek-v4-pro(max)"
DEFAULT_OPENCODE_TIMEOUT_SEC = 1200
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?(?:\x07|\x1b\\)")
_SECRET_RE = re.compile(
    r"((?<![A-Za-z0-9])sk-[A-Za-z0-9_\-]{8,}|Bearer\s+\S+|api[_-]?key[=:]\s*\S+)",
    re.IGNORECASE,
)


def run_opencode_cli(
    prompt: str,
    *,
    model: str = DEFAULT_OPENCODE_MODEL,
    timeout_sec: int = DEFAULT_OPENCODE_TIMEOUT_SEC,
    title: str = "research-agenda-opencode-run",
) -> dict[str, Any]:
    """Call OpenCode headlessly and return parsed text plus bounded diagnostics."""
    result: dict[str, Any] = {
        "provider": "opencode-cli",
        "requested_model": model,
        "effective_model": model,
        "exit_code": None,
        "timed_out": False,
        "raw_stdout": "",
        "raw_stderr": "",
        "clean_output": "",
        "event_count": 0,
        "error": "",
    }
    opencode_path = shutil.which("opencode")
    if not opencode_path:
        result["error"] = "opencode_cli_not_found"
        return result
    prompt_path = None
    workspace = tempfile.TemporaryDirectory(prefix="opencode-review-")
    workspace_path = workspace.name
    if len(prompt) > 3000:
        prompt_file = tempfile.NamedTemporaryFile("w+", encoding="utf-8", suffix=".json", delete=False)
        prompt_file.write(prompt)
        prompt_file.flush()
        prompt_path = prompt_file.name
        prompt_file.close()
        command_message = (
            "Read the attached JSON request. Do not run tools, inspect files, modify files, or start/cancel background tasks. "
            "Return only the requested raw JSON object as the final answer."
        )
        file_args = ["--file", prompt_path]
    else:
        command_message = prompt
        file_args = []
    command = [
        opencode_path,
        "run",
        "-m",
        model,
        "--pure",
        "--format",
        "json",
        "--title",
        title,
        "--dir",
        workspace_path,
        command_message,
        *file_args,
    ]
    env = {**os.environ}
    try:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=workspace_path,
        )
        stdout, stderr = proc.communicate(timeout=timeout_sec)
        result["exit_code"] = proc.returncode
        result["raw_stdout"] = _redact(stdout or "")[:16000]
        result["raw_stderr"] = _redact(stderr or "")[:4000]
    except FileNotFoundError:
        result["error"] = "opencode_cli_not_found"
        workspace.cleanup()
        return result
    except subprocess.TimeoutExpired:
        _kill_process_tree(proc.pid)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
        result["timed_out"] = True
        result["error"] = f"timeout:{timeout_sec}s"
        result["raw_stdout"] = _redact(stdout or "")[:16000]
        result["raw_stderr"] = _redact(stderr or "")[:4000]
        workspace.cleanup()
        return result
    finally:
        if prompt_path is not None:
            try:
                os.unlink(prompt_path)
            except OSError:
                pass

    text, event_count = _extract_text_events(stdout or "")
    file_output = _read_tool_json_output(workspace_path)
    workspace.cleanup()
    result["event_count"] = event_count
    result["clean_output"] = ((file_output + "\n") if file_output else "") + text[:240000]
    if result["exit_code"] != 0:
        result["error"] = f"nonzero_exit:{result['exit_code']}"
    elif not result["clean_output"].strip():
        result["error"] = "empty_output"
    return result


def _read_tool_json_output(workspace_path: str) -> str:
    json_files: list[tuple[float, str]] = []
    for root, _dirs, files in os.walk(workspace_path):
        for filename in files:
            if not filename.lower().endswith(".json"):
                continue
            path = os.path.join(root, filename)
            try:
                if os.path.getsize(path) > 1_000_000:
                    continue
                json_files.append((os.path.getmtime(path), path))
            except OSError:
                continue
    for _mtime, path in sorted(json_files, reverse=True):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
            json.loads(text)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        return _redact(text)[:240000]
    return ""


def _extract_text_events(stdout: str) -> tuple[str, int]:
    texts: list[str] = []
    events = 0
    fallback_lines: list[str] = []
    for raw_line in stdout.splitlines():
        line = _strip_ansi(_redact(raw_line)).strip()
        if not line:
            continue
        if not line.startswith("{"):
            fallback_lines.append(line)
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            fallback_lines.append(line)
            continue
        events += 1
        event_texts = _extract_event_texts(event)
        if event_texts:
            texts.extend(event_texts)
            continue
        part = event.get("part", {}) if isinstance(event, dict) else {}
        if isinstance(part, dict) and part.get("type") == "text":
            texts.append(str(part.get("text", "")))
        else:
            fallback_lines.append(line)
    if texts:
        return "\n".join(item for item in texts if item.strip()), events
    return "\n".join(fallback_lines), events


def _extract_event_texts(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    if isinstance(value, list):
        texts: list[str] = []
        for item in value:
            texts.extend(_extract_event_texts(item))
        return texts
    if not isinstance(value, dict):
        return []

    role = value.get("role")
    if isinstance(role, str) and role.lower() not in {"assistant", "model"}:
        return []

    texts: list[str] = []
    text_value = value.get("text")
    if isinstance(text_value, str) and text_value.strip():
        texts.append(text_value)

    for key in ("content", "message", "delta", "result", "output", "response"):
        nested = value.get(key)
        if nested is not None:
            texts.extend(_extract_event_texts(nested))
    return texts


def _redact(text: str) -> str:
    return _SECRET_RE.sub("[REDACTED]", text)


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _kill_process_tree(pid: int) -> None:
    if sys.platform.startswith("win"):
        try:
            subprocess.run(
                ["taskkill.exe", "/PID", str(pid), "/T", "/F"],
                text=True,
                capture_output=True,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        return
    try:
        os.kill(pid, 9)
    except OSError:
        pass


