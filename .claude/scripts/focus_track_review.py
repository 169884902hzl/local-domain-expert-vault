"""Review focused research track gates."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from focus_track_common import (
    note_status,
    read_text,
    rel,
    topic_path_from_stem,
    track_config,
    track_evidence_path,
    track_root,
    wikilink_stems,
)
from kb_common import safe_print, vault_path


def _has_tokens(text: str, tokens: list[str]) -> bool:
    lower = text.lower()
    return all(token.lower() in lower for token in tokens)


def _similar_done_count(track: str) -> int:
    config = track_config(track)
    count = 0
    for item in config["similar_work"]:
        path = topic_path_from_stem(item["stem"])
        if path.exists() and note_status(path) == "done":
            count += 1
    return count


def _accepted_claim_issues(track: str) -> list[str]:
    path = track_root(track) / "paper-claims" / "accepted_claims.jsonl"
    if not path.exists():
        return ["missing_accepted_claims_file"]
    issues: list[str] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
        except json.JSONDecodeError:
            issues.append(f"line_{line_no}:invalid_json")
            continue
        status = str(record.get("status", "unverified"))
        source = str(record.get("source_note", ""))
        if status != "unverified":
            if not source.startswith("wiki/topics/"):
                issues.append(f"line_{line_no}:missing_local_topic_source")
            elif not vault_path(*source.split("/")).exists():
                issues.append(f"line_{line_no}:source_note_missing:{source}")
        extension = str(record.get("extension", "")).lower()
        rationale = str(record.get("rl_token_rationale", ""))
        if extension and not rationale:
            issues.append(f"line_{line_no}:extension_without_rl_token_rationale")
    return issues


def _dashboard_state(root: Path) -> str:
    text = read_text(root / "track-dashboard.md")
    match = re.search(r"^- current_state:\s*`?([^`\n]+)`?", text, re.MULTILINE)
    if not match:
        return "unknown"
    return match.group(1).strip()


def review(track: str) -> dict[str, Any]:
    config = track_config(track)
    root = track_root(track)
    core_path = vault_path(*config["core_note"].split("/"))
    core_text = read_text(core_path)
    core_paper = read_text(root / "core-paper.md")
    experiment = read_text(root / "experiments" / "minimal-replication-plan.md")
    claim_gate = read_text(root / "paper-claims" / "claim-gate.md")
    accepted_claim_issues = _accepted_claim_issues(track)
    similar_count = _similar_done_count(track)
    gates = {
        "paper_understood": core_path.exists()
        and note_status(core_path) == "done"
        and "## 证据元数据" in core_text
        and "待精读" not in core_text,
        "similar_work_checked": similar_count >= 5,
        "mechanism_clear": _has_tokens(core_paper, ["RL token", "actor-critic", "anchoring"]),
        "replication_plan_ready": _has_tokens(experiment, ["baseline", "metric", "pilot", "failure"]),
        "extension_claim_safe": not accepted_claim_issues and _has_tokens(claim_gate, ["unverified", "RL token", "cannot"]),
    }
    status = "PASS" if all(gates.values()) else "WARN"
    if not core_path.exists() or not root.exists():
        status = "FAIL"
    return {
        "track": track,
        "status": status,
        "current_state": _dashboard_state(root),
        "root": rel(root) if root.exists() else str(root),
        "core_note": config["core_note"],
        "evidence_file_exists": track_evidence_path(track).exists(),
        "similar_work_done": similar_count,
        "gates": gates,
        "accepted_claim_issues": accepted_claim_issues,
        "next_actions": [
            "extract exact PDF/code experiment details",
            "run low-cost token-readout pilot",
            "keep all extension claims unverified until local evidence or experiment gate passes",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--track", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = review(args.track)
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(f"{result['status']} track={args.track} state={result['current_state']}")
        for name, passed in result["gates"].items():
            safe_print(f"{'PASS' if passed else 'WARN'} {name}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
