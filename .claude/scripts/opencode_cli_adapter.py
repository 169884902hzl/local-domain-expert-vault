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
    r"(sk-[A-Za-z0-9_\-]{8,}|Bearer\s+\S+|api[_-]?key[=:]\s*\S+)",
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
    if len(prompt) > 3000:
        prompt_file = tempfile.NamedTemporaryFile("w+", encoding="utf-8", suffix=".json", delete=False)
        prompt_file.write(prompt)
        prompt_file.flush()
        prompt_path = prompt_file.name
        prompt_file.close()
        command_message = "Read the attached prompt file and return the requested JSON only."
        file_args = ["--file", prompt_path]
    else:
        command_message = prompt
        file_args = []
    command = [
        opencode_path,
        "run",
        "-m",
        model,
        "--format",
        "json",
        "--title",
        title,
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
        )
        stdout, stderr = proc.communicate(timeout=timeout_sec)
        result["exit_code"] = proc.returncode
        result["raw_stdout"] = _redact(stdout or "")[:16000]
        result["raw_stderr"] = _redact(stderr or "")[:4000]
    except FileNotFoundError:
        result["error"] = "opencode_cli_not_found"
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
        return result
    finally:
        if prompt_path is not None:
            try:
                os.unlink(prompt_path)
            except OSError:
                pass

    text, event_count = _extract_text_events(stdout or "")
    result["event_count"] = event_count
    result["clean_output"] = text[:240000]
    if result["exit_code"] != 0:
        result["error"] = f"nonzero_exit:{result['exit_code']}"
    elif not result["clean_output"].strip():
        result["error"] = "empty_output"
    return result


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
        part = event.get("part", {}) if isinstance(event, dict) else {}
        if isinstance(part, dict) and part.get("type") == "text":
            texts.append(str(part.get("text", "")))
    if texts:
        return "\n".join(item for item in texts if item.strip()), events
    return "\n".join(fallback_lines), events


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


