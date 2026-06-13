"""Thin adapter for calling Gemini CLI in headless mode with timeout and structured errors."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?(?:\x07|\x1b\\)")
_WARNING_LINES = {"warning:", "ripgrep is not available", "falling back"}
DEFAULT_GEMINI_TIMEOUT_SEC = 1200
DEFAULT_GEMINI_MODEL = "gemini-3.1-pro-preview"

_SHORT_INSTRUCTION = (
    "Return JSON only with key 'candidates' (array of objects). "
    "Use only the evidence provided. Each candidate needs: title, problem, "
    "engineering_pathology, mechanism, interface, hypothesis, evidence_links, "
    "speculative_jump, contribution_shape, non_obvious_claim, why_now, strongest_baseline, "
    "killer_experiment, online_or_offline_mode, minimum_no_hardware_pilot, baseline_kill_table, "
    "what_would_make_this_not_a_paper, reviewer_pre_mortem, novelty_risk, promotion_reason, rescue_signal, nearest_pressure, "
    "pilot, baselines, metrics, falsification. "
    "If no candidate is strong, return {\"candidates\": []}."
)


def _resolve_gemini_path() -> str:
    candidates: list[str | None] = []
    if os.name == "nt":
        candidates.append(shutil.which("gemini.cmd"))
    candidates.append(shutil.which("gemini"))
    if os.name == "nt":
        candidates.extend(
            [
                str(Path)
                for Path in [
                    os.path.expandvars(r"%APPDATA%\npm\gemini.cmd"),
                    os.path.expandvars(r"%ProgramFiles%\nodejs\gemini.cmd"),
                    r"C:\nvm4w\nodejs\gemini.cmd",
                ]
            ]
        )
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return ""


def run_gemini_cli(
    prompt: str,
    *,
    timeout_sec: int = DEFAULT_GEMINI_TIMEOUT_SEC,
    model: str = DEFAULT_GEMINI_MODEL,
    short_instruction: str = _SHORT_INSTRUCTION,
) -> dict[str, Any]:
    """Call Gemini CLI headlessly with hard timeout. Returns structured result.

    Long prompts are piped via stdin to avoid Windows command-line length limits.
    """
    result: dict[str, Any] = {
        "provider": "gemini-cli",
        "exit_code": None,
        "raw_stdout": "",
        "raw_stderr": "",
        "clean_output": "",
        "timed_out": False,
        "error": "",
        "requested_model": model or "",
        "effective_fallback": False,
    }
    env = {**os.environ, "GEMINI_CLI_NO_RELAUNCH": "1"}
    gemini_path = _resolve_gemini_path()
    if not gemini_path:
        result["error"] = "gemini_cli_not_found"
        return result

    attempts = [model, ""] if model else [""]
    last_result: dict[str, Any] | None = None
    for index, attempt_model in enumerate(attempts):
        attempt = dict(result)
        attempt["effective_fallback"] = index > 0
        if index > 0:
            attempt["raw_stderr"] = (last_result or {}).get("raw_stderr", "")
        _run_gemini_attempt(
            attempt,
            gemini_path=gemini_path,
            prompt=prompt,
            timeout_sec=timeout_sec,
            model=attempt_model,
            env=env,
            short_instruction=short_instruction,
        )
        if not attempt["error"]:
            return attempt
        last_result = attempt
        if index == 0 and model and not _should_try_auto_fallback(attempt["error"], attempt["raw_stderr"]):
            return attempt
    return last_result or result


def _run_gemini_attempt(
    result: dict[str, Any],
    *,
    gemini_path: str,
    prompt: str,
    timeout_sec: int,
    model: str,
    env: dict[str, str],
    short_instruction: str,
) -> None:
    result["effective_model"] = model or "auto"
    prompt_file = None
    base_command = [gemini_path]
    if model:
        base_command.extend(["--model", model])
    if len(prompt) > 4000:
        command = [*base_command, "-p", short_instruction]
        prompt_file = tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False)
        prompt_file.write(prompt)
        prompt_file.flush()
        prompt_file.seek(0)
        stdin_text = None
    else:
        command = [*base_command, "-p", prompt]
        stdin_text = None

    try:
        proc = subprocess.Popen(
            command,
            stdin=prompt_file or (subprocess.PIPE if stdin_text is not None else None),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        stdout, stderr = proc.communicate(input=stdin_text, timeout=timeout_sec)
        result["exit_code"] = proc.returncode
        full_stdout = stdout or ""
        result["raw_stdout"] = full_stdout[:16000]
        result["raw_stderr"] = (stderr or "")[:4000]
    except FileNotFoundError:
        result["error"] = "gemini_cli_not_found"
        return
    except subprocess.TimeoutExpired:
        _kill_process_tree(proc.pid)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
        result["timed_out"] = True
        result["error"] = f"timeout:{timeout_sec}s"
        result["raw_stdout"] = (stdout or "")[:16000]
        result["raw_stderr"] = (stderr or "")[:4000]
        return
    except PermissionError as exc:
        result["error"] = f"permission_error:{exc}"
        return
    finally:
        if prompt_file is not None:
            prompt_path = prompt_file.name
            prompt_file.close()
            try:
                os.unlink(prompt_path)
            except OSError:
                pass

    if result["exit_code"] != 0:
        result["error"] = f"nonzero_exit:{result['exit_code']}"
        return

    clean = _strip_ansi_and_warnings(full_stdout)[:240000]
    result["clean_output"] = clean
    if not clean.strip():
        result["error"] = "empty_output"


def _model_error_is_fallbackable(error: str, stderr: str) -> bool:
    text = f"{error}\n{stderr}".lower()
    return any(
        token in text
        for token in [
            "model",
            "not found",
            "not_found",
            "not supported",
            "unsupported",
            "invalid",
            "permission",
            "quota",
            "429",
        ]
    )


def _should_try_auto_fallback(error: str, stderr: str) -> bool:
    if error.startswith("timeout:"):
        return False
    if _model_error_is_fallbackable(error, stderr):
        return True
    if error.startswith("nonzero_exit:"):
        # Gemini CLI occasionally exits nonzero on long prompts without a model-specific
        # stderr. Auto mode is cheap compared with losing the whole daily ideation pass.
        return True
    return False


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


def _strip_ansi_and_warnings(text: str) -> str:
    lines = []
    for raw_line in text.splitlines():
        line = _ANSI_RE.sub("", raw_line).strip()
        if not line:
            continue
        if line.lower().startswith(tuple(_WARNING_LINES)):
            continue
        lines.append(line)
    return "\n".join(lines)
