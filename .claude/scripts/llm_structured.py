"""Shared helpers for structured LLM/CLI output parsing and retry control."""
from __future__ import annotations

import json
import re
from typing import Any


_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?(?:\x07|\x1b\\)")

class StructuredOutputError(ValueError):
    """Raised when no JSON object can be recovered from model output."""


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)


def _strip_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return stripped


def _repair_js_object_literal(text: str) -> str:
    repaired = re.sub(r"(?<=[{,])\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", r'"\1":', text)
    return re.sub(r",\s*([}\]])", r"\1", repaired)


def _balanced_json_like_objects(text: str) -> list[str]:
    objects: list[str] = []
    start: int | None = None
    stack: list[str] = []
    in_string = False
    quote = ""
    escaped = False
    for index, char in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue
        if char in {'"', "'"}:
            in_string = True
            quote = char
            continue
        if char == "{":
            if not stack:
                start = index
            stack.append("}")
            continue
        if char == "[" and stack:
            stack.append("]")
            continue
        if char in "}]" and stack and char == stack[-1]:
            stack.pop()
            if not stack and start is not None:
                objects.append(text[start : index + 1])
                start = None
    return objects


def _truncated_json_candidate(text: str) -> str | None:
    start = text.find("{")
    if start < 0:
        return None
    stack: list[str] = []
    in_string = False
    quote = ""
    escaped = False
    for char in text[start:]:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            continue
        if char in {'"', "'"}:
            in_string = True
            quote = char
            continue
        if char == "{":
            stack.append("}")
        elif char == "[":
            stack.append("]")
        elif char in "}]" and stack and char == stack[-1]:
            stack.pop()
    if not stack or in_string:
        return None
    return text[start:] + "".join(reversed(stack))


def extract_json(
    text: str,
    *,
    want: Callable[[dict[str, Any]], bool] | None = None,
    repair: bool = True,
) -> dict[str, Any]:
    """Extract a JSON object from prose, fenced blocks, or CLI event noise."""
    candidates: list[str] = []
    stripped = _strip_fence(_strip_ansi(text))
    candidates.append(stripped)
    candidates.extend(match.group(1).strip() for match in _FENCE_RE.finditer(text))
    candidates.extend(_balanced_json_like_objects(stripped))
    truncated = _truncated_json_candidate(stripped)
    if truncated:
        candidates.append(truncated)

    decoder = json.JSONDecoder()
    first_payload: dict[str, Any] | None = None
    for candidate in candidates:
        variants = [candidate]
        if repair:
            variants.append(_repair_js_object_literal(candidate))
        for variant in variants:
            for index, char in enumerate(variant):
                if char != "{":
                    continue
                try:
                    payload, _ = decoder.raw_decode(variant[index:])
                except json.JSONDecodeError:
                    continue
                if not isinstance(payload, dict):
                    continue
                if first_payload is None:
                    first_payload = payload
                if want is None or want(payload):
                    return payload
    if first_payload is not None:
        return first_payload
    raise StructuredOutputError("provider_output_json_object_not_found")


def classify_transient(stdout: str, stderr: str) -> str:
    text = f"{stdout}\n{stderr}".lower()
    if "already in use" in text:
        return "session_in_use"
    if "api error: 524" in text or "origin_response_timeout" in text:
        return "api_524"
    if "tool call could not be parsed" in text:
        return "tool_call_parse_failed"
    if '"retryable":true' in text or '"retryable": true' in text:
        return "retryable_api_error"
    if "timeout" in text or "temporarily unavailable" in text:
        return "transient_timeout"
    return ""


def backoff_seconds(stdout: str = "", stderr: str = "", *, attempt: int = 1, reason: str = "") -> int:
    reason = reason or classify_transient(stdout, stderr)
    if reason == "session_in_use":
        return 15 * attempt
    match = re.search(r'"retry_after"\s*:\s*(\d+)', f"{stdout}\n{stderr}")
    if match:
        return max(30, min(180, int(match.group(1))))
    return min(180, 30 * attempt)
