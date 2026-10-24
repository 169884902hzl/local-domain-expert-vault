"""Thin adapter for calling OpenCode CLI with structured, secret-safe output."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


DEFAULT_OPENCODE_MODEL = "abrdns/deepseek-v4-pro"
DEFAULT_OPENCODE_TIMEOUT_SEC = 1200
INLINE_PROMPT_CHAR_LIMIT = 2000
JSON_REVIEW_AGENT_NAME = "research-json-review"
_DISABLED_OPENCODE_TOOLS = {
    "bash": False,
    "edit": False,
    "fetch": False,
    "grep": False,
    "glob": False,
    "list": False,
    "patch": False,
    "read": False,
    "skill": False,
    "task": False,
    "todo": False,
    "todo_write": False,
    "todowrite": False,
    "web": False,
    "web_fetch": False,
    "web_search": False,
    "webfetch": False,
    "websearch": False,
    "write": False,
}
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
    opencode_path = _resolve_opencode_path()
    if not opencode_path:
        result["error"] = "opencode_cli_not_found"
        return result
    prompt_path = None
    workspace = tempfile.TemporaryDirectory(prefix="opencode-review-")
    workspace_path = workspace.name
    _write_json_review_agent_config(workspace_path, model)
    if len(prompt) > INLINE_PROMPT_CHAR_LIMIT:
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
    def command_for(output_format: str) -> list[str]:
        command = [
            opencode_path,
            "run",
            "-m",
            model,
        ]
        if _json_review_pure_mode():
            command.append("--pure")
        command.extend(
            [
                "--format",
                output_format,
                "--agent",
                JSON_REVIEW_AGENT_NAME,
                "--title",
                title,
                "--dir",
                workspace_path,
                command_message,
                *file_args,
            ]
        )
        return command

    def cleanup_prompt_file() -> None:
        if prompt_path is None:
            return
        try:
            os.unlink(prompt_path)
        except OSError:
            pass

    command = command_for("json")
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
        cleanup_prompt_file()
        _cleanup_temporary_directory(workspace)
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
        cleanup_prompt_file()
        _cleanup_temporary_directory(workspace)
        return result

    text, event_count = _extract_text_events(stdout or "")
    event_errors = _extract_error_events(stdout or "")
    file_output = _read_tool_json_output(workspace_path)
    result["event_count"] = event_count
    result["clean_output"] = ((file_output + "\n") if file_output else "") + text[:240000]

    if result["exit_code"] == 0 and event_count and not result["clean_output"].strip():
        fallback = _run_default_format_fallback(command_for("default"), env=env, cwd=workspace_path, timeout_sec=timeout_sec)
        result["default_format_fallback"] = True
        result["default_format_exit_code"] = fallback["exit_code"]
        result["raw_stdout"] = (result["raw_stdout"] + "\n--- default-format fallback ---\n" + fallback["raw_stdout"])[:16000]
        result["raw_stderr"] = (result["raw_stderr"] + "\n--- default-format fallback ---\n" + fallback["raw_stderr"])[:4000]
        if fallback["timed_out"]:
            result["error"] = fallback["error"]
        elif fallback["exit_code"] == 0 and fallback["clean_output"].strip():
            result["clean_output"] = fallback["clean_output"][:240000]
            result["error"] = ""
        elif fallback["exit_code"] not in (None, 0):
            result["error"] = fallback["error"]

    file_output = _read_tool_json_output(workspace_path)
    if file_output:
        result["clean_output"] = ((file_output + "\n") + result["clean_output"])[:240000]
    if event_errors and not result["clean_output"].strip() and not result.get("error"):
        result["error"] = event_errors[0]
    if event_errors:
        result["event_errors"] = event_errors[:8]
    cleanup_prompt_file()
    _cleanup_temporary_directory(workspace)
    if result["exit_code"] != 0:
        result["error"] = f"nonzero_exit:{result['exit_code']}"
    elif not result["clean_output"].strip() and not result.get("error"):
        result["error"] = "empty_output"
    return result


def _run_default_format_fallback(command: list[str], *, env: dict[str, str], cwd: str, timeout_sec: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "exit_code": None,
        "timed_out": False,
        "raw_stdout": "",
        "raw_stderr": "",
        "clean_output": "",
        "error": "",
    }
    try:
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            cwd=cwd,
        )
        stdout, stderr = proc.communicate(timeout=timeout_sec)
        result["exit_code"] = proc.returncode
        result["raw_stdout"] = _redact(stdout or "")[:16000]
        result["raw_stderr"] = _redact(stderr or "")[:4000]
        result["clean_output"] = _strip_ansi(_redact(stdout or "")).strip()
        if proc.returncode != 0:
            result["error"] = f"default_format_nonzero_exit:{proc.returncode}"
    except FileNotFoundError:
        result["error"] = "opencode_cli_not_found"
    except subprocess.TimeoutExpired:
        _kill_process_tree(proc.pid)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
        result["timed_out"] = True
        result["error"] = f"default_format_timeout:{timeout_sec}s"
        result["raw_stdout"] = _redact(stdout or "")[:16000]
        result["raw_stderr"] = _redact(stderr or "")[:4000]
    return result


def _resolve_opencode_path() -> str | None:
    direct_exe = shutil.which("opencode.exe")
    if direct_exe:
        return direct_exe
    path = shutil.which("opencode")
    if not path:
        return None
    lower = path.lower()
    if lower.endswith((".cmd", ".ps1")):
        bundled_exe = os.path.join(os.path.dirname(path), "node_modules", "opencode-ai", "bin", "opencode.exe")
        if os.path.exists(bundled_exe):
            return bundled_exe
    return path


def _write_json_review_agent_config(workspace_path: str, model: str) -> str:
    path = os.path.join(workspace_path, "opencode.json")
    agent_prompt = (
        "You are a strict JSON-only scientific reviewer. Never use tools, including todowrite or webfetch. "
        "Output RFC 8259 JSON only: every key and string value must use double quotes. "
        "Do not output JavaScript object literal syntax, markdown, prose, or code fences."
    )
    config = _load_global_opencode_config()
    config.update({
        "$schema": "https://opencode.ai/config.json",
        "agent": {
            JSON_REVIEW_AGENT_NAME: {
                "description": "Return strict DeepSeek review JSON only; no tools.",
                "mode": "primary",
                "model": _agent_model_name(model),
                "tools": dict(_DISABLED_OPENCODE_TOOLS),
                "temperature": 0.0,
                "prompt": agent_prompt,
            }
        },
        "default_agent": JSON_REVIEW_AGENT_NAME,
        "formatter": False,
        "lsp": False,
        "mcp": {},
        "tools": dict(_DISABLED_OPENCODE_TOOLS),
    })
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2, sort_keys=True)
    return path


def _agent_model_name(model: str) -> str:
    text = str(model or "").strip()
    if "/" in text:
        return text.split("/", 1)[1]
    return text


def _load_global_opencode_config() -> dict[str, Any]:
    for candidate in _global_opencode_config_paths():
        if not candidate.exists():
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            return _normalize_global_opencode_config(dict(payload), candidate.parent)
    return {}


def _global_opencode_config_paths() -> list[Path]:
    paths: list[Path] = []
    home = Path.home()
    paths.append(home / ".config" / "opencode" / "opencode.json")
    paths.append(home / ".opencode" / "opencode.json")
    paths.append(home / ".config" / "opencode.json")
    return paths


def _normalize_global_opencode_config(payload: dict[str, Any], config_dir: Path) -> dict[str, Any]:
    normalized = dict(payload)
    plugins = normalized.get("plugin")
    if isinstance(plugins, list):
        normalized["plugin"] = _normalize_plugin_entries(plugins, config_dir)
    return normalized


def _normalize_plugin_entries(plugins: list[Any], config_dir: Path) -> list[Any]:
    normalized: list[Any] = []
    seen: set[str] = set()
    for plugin in plugins:
        item = plugin
        if isinstance(plugin, str):
            item = _normalize_plugin_entry(plugin, config_dir)
        marker = json.dumps(item, ensure_ascii=False, sort_keys=True) if not isinstance(item, str) else item
        if marker in seen:
            continue
        seen.add(marker)
        normalized.append(item)
    return normalized


def _normalize_plugin_entry(plugin: str, config_dir: Path) -> str:
    text = str(plugin or "").strip()
    if not text:
        return text
    if text.startswith("file://") or os.path.isabs(text) or "@" in text:
        return text
    if text.startswith("./") or text.startswith(".\\"):
        return str((config_dir / text).resolve())
    return text


def _json_review_pure_mode() -> bool:
    value = str(os.environ.get("OPENCODE_JSON_REVIEW_PURE", "")).strip().lower()
    return value in {"1", "true", "yes", "on"}


def _cleanup_temporary_directory(workspace: tempfile.TemporaryDirectory[str], *, retries: int = 6, delay_sec: float = 0.25) -> None:
    for attempt in range(retries):
        try:
            workspace.cleanup()
            return
        except (PermissionError, OSError):
            if attempt == retries - 1:
                return
            time.sleep(delay_sec)


def _read_tool_json_output(workspace_path: str) -> str:
    json_files: list[tuple[float, str]] = []
    for root, _dirs, files in os.walk(workspace_path):
        for filename in files:
            if not filename.lower().endswith(".json"):
                continue
            if not _is_allowed_tool_json_output(workspace_path, root, filename):
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


def _is_allowed_tool_json_output(workspace_path: str, root: str, filename: str) -> bool:
    if filename.lower() != "review-output.json":
        return False
    try:
        rel_parts = os.path.relpath(root, workspace_path).split(os.sep)
    except ValueError:
        return False
    return ".sisyphus" in rel_parts


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
    if texts:
        return "".join(item for item in texts if item.strip()), events
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


def _extract_error_events(stdout: str) -> list[str]:
    errors: list[str] = []
    for raw_line in stdout.splitlines():
        line = _strip_ansi(_redact(raw_line)).strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if str(event.get("type") or "").lower() != "error":
            continue
        error = event.get("error")
        if isinstance(error, dict):
            name = str(error.get("name") or "ProviderError").strip()
            data = error.get("data")
            if isinstance(data, dict):
                message = str(data.get("message") or error.get("message") or "").strip()
                status = data.get("statusCode")
                if message and status is not None:
                    errors.append(f"provider_event_error:{name}:{message}:status={status}")
                    continue
                if message:
                    errors.append(f"provider_event_error:{name}:{message}")
                    continue
            message = str(error.get("message") or "").strip()
            if message:
                errors.append(f"provider_event_error:{name}:{message}")
                continue
        errors.append("provider_event_error:unknown")
    return errors


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


