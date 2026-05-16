"""Shared helpers for focused research tracks."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_write, vault_path


FOCUS_ROOT = vault_path("projects", "focus-tracks")
AGENDA_EVIDENCE_MATRIX = vault_path("projects", "research-agenda", "evidence", "evidence_matrix.jsonl")
TRACK_STATES = ["seed", "replication-ready", "extension-candidate", "blocked"]

TRACKS: dict[str, dict[str, Any]] = {
    "rl-token-vla-online-rl": {
        "title": "RL Token VLA Online RL",
        "summary": "Focused track for RL Token and VLA-to-online-RL interfaces.",
        "core_note": "wiki/topics/xu2026token.md",
        "core_title": "RL Token: Bootstrapping Online RL with Vision-Language-Action Models",
        "keywords": [
            "rl token",
            "rlt",
            "online rl",
            "rl head",
            "policy head",
            "action token",
            "vla anchoring",
            "anchoring",
            "real-robot fine-tuning",
            "real robot practice",
            "pretrained vla",
            "frozen vla",
            "small actor-critic",
            "flow-gspo",
            "gspo",
        ],
        "similar_work": [
            {"stem": "jie2026omnivlarl", "label": "OmniVLA-RL", "role": "VLA plus online RL baseline"},
            {"stem": "kim2024openvla", "label": "OpenVLA", "role": "open VLA representation baseline"},
            {"stem": "dong2025vitavla", "label": "VITA-VLA", "role": "efficient VLA action expert adaptation"},
            {"stem": "brohan2023rt2", "label": "RT-2", "role": "VLA foundation model background"},
            {"stem": "collaboration2025open", "label": "Open X-embodiment", "role": "RT-X pretraining and data background"},
            {"stem": "team2024octo", "label": "Octo", "role": "open generalist robot policy baseline"},
            {"stem": "wang2025vlaadapter", "label": "VLA-adapter", "role": "small adapter comparison"},
            {"stem": "patel2025realtosimtoreal", "label": "VLM keypoint rewards", "role": "low-cost reward and sim-to-real comparison"},
        ],
    }
}


def today() -> str:
    return date.today().isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def strip_quotes(value: str) -> str:
    return value.strip().strip('"')


def track_config(track: str) -> dict[str, Any]:
    if track not in TRACKS:
        raise ValueError(f"unknown_track:{track}")
    return TRACKS[track]


def track_root(track: str) -> Path:
    track_config(track)
    return FOCUS_ROOT / track


def track_evidence_path(track: str) -> Path:
    return track_root(track) / "evidence" / "track_evidence.jsonl"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = read_text(path)
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text
    fields, body = parsed
    return parse_frontmatter_map(fields), body


def note_status(path: Path) -> str:
    fields, _ = read_frontmatter(path)
    return strip_quotes(fields.get("status", ""))


def note_title(path: Path) -> str:
    fields, _ = read_frontmatter(path)
    return strip_quotes(fields.get("title", "")) or path.stem


def topic_path_from_stem(stem: str) -> Path:
    return vault_path("wiki", "topics", f"{stem}.md")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip():
            continue
        try:
            records.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return records


def write_jsonl(path: Path, records: list[dict[str, Any]], *, dry_run: bool) -> None:
    content = "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records)
    if content:
        content += "\n"
    safe_write(path, content, dry_run=dry_run, backup=True)


def render_frontmatter(title: str, tags: list[str], summary: str, *, status: str = "active") -> str:
    now = today()
    tag_text = "[" + ", ".join(tags) + "]"
    return "\n".join(
        [
            "---",
            f'title: "{title}"',
            f"tags: {tag_text}",
            f'created: "{now}"',
            f'updated: "{now}"',
            'type: "permanent"',
            f'status: "{status}"',
            f'summary: "{summary}"',
            "---",
            "",
        ]
    )


def wikilink(stem: str, label: str | None = None) -> str:
    if label:
        return f"[[{stem}|{label}]]"
    return f"[[{stem}]]"


def wikilink_stems(text: str) -> list[str]:
    return re.findall(r"\[\[([^|\]#]+)", text)


def evidence_key(record: dict[str, Any]) -> str:
    return "|".join(
        [
            str(record.get("source_note", "")),
            str(record.get("claim_type", "")),
            str(record.get("statement", ""))[:240],
        ]
    )


def dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {evidence_key(record): record for record in records}
    return sorted(by_key.values(), key=lambda item: (item.get("source_note", ""), item.get("claim_type", "")))


def track_registry_payload() -> dict[str, Any]:
    return {
        "tracks": {
            track: {
                "title": config["title"],
                "summary": config["summary"],
                "core_note": config["core_note"],
                "states": TRACK_STATES,
            }
            for track, config in TRACKS.items()
        }
    }
