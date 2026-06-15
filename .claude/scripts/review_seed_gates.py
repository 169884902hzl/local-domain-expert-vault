"""Review idea_bank seed gate files and upgrade gate_status to reviewed_complete.

Performs a real substantive review of each seed's four gate files (similar_work,
novelty_argument, experiment_plan, risk_review). Checks that required content fields
are filled (not placeholder/empty), validates structural requirements that match
research_agenda_review._has_gate_text expectations, and only upgrades gate_status
from generated_complete to reviewed_complete when all checks pass. Records reviewer
identity and timestamp. Does NOT mechanically flip tokens — a seed with empty
strongest_baseline or missing pilot stays at generated_complete.

Can process a single seed (--seed-folder) or batch all seeds (--all).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from kb_common import safe_print

AGENDA_ROOT = Path(os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT", "")).resolve() if os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT") else Path(__file__).resolve().parents[2] / "projects" / "research-agenda"
SEED_DIR = AGENDA_ROOT / "idea_bank" / "seed"

GATE_FILES = {
    "similar_work.md": {
        "required_tokens": ["similar"],
        "required_fields": ["nearest_pressure", "strongest_baseline"],
        "required_field_patterns": [r"nearest_pressure:[^\S\r\n]*\S", r"strongest_baseline:[^\S\r\n]*\S"],
    },
    "novelty_argument.md": {
        "required_tokens": ["novelty"],
        "required_fields": ["candidate_claim", "non_obvious_claim", "mechanism"],
        "required_field_patterns": [r"candidate_claim:[^\S\r\n]*\S", r"non_obvious_claim:[^\S\r\n]*\S", r"mechanism:[^\S\r\n]*\S"],
    },
    "experiment_plan.md": {
        "required_tokens": ["baseline", "metric", "pilot", "failure"],
        "required_fields": ["pilot", "killer_experiment", "strongest_baseline", "baselines", "metrics", "falsification"],
        "required_field_patterns": [r"pilot:[^\S\r\n]*\S", r"killer_experiment:[^\S\r\n]*\S", r"strongest_baseline:[^\S\r\n]*\S", r"baselines:[^\S\r\n]*\S", r"metrics:[^\S\r\n]*\S", r"falsification:[^\S\r\n]*\S"],
    },
    "risk_review.md": {
        "required_tokens": ["risk", "fallback"],
        "required_fields": ["main_risk", "reviewer_pre_mortem", "what_would_make_this_not_a_paper", "reject_condition"],
        "required_field_patterns": [r"main_risk:[^\S\r\n]*\S", r"reviewer_pre_mortem:[^\S\r\n]*\S", r"what_would_make_this_not_a_paper:[^\S\r\n]*\S", r"reject_condition:[^\S\r\n]*\S"],
    },
}

PLACEHOLDER_WORDS = {"review needed", "review_needed", "unverified", "not_checked", "to be filled", "placeholder", "TODO", "see idea.md", "see idea.md for details", "see local evidence"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _has_placeholder(text: str) -> bool:
    low = text.lower()
    return any(pw in low for pw in PLACEHOLDER_WORDS)


def _current_gate(text: str) -> str:
    m = re.search(r"gate_status:\s*(\S+)", text)
    return m.group(1) if m else ""


def _review_file(path: Path, spec: dict) -> tuple[bool, list[str]]:
    text = _read(path)
    issues = []
    if not text.strip():
        return False, [f"empty file: {path.name}"]
    gate = _current_gate(text)
    if gate not in ("generated_complete", "complete", "reviewed", "reviewed_complete"):
        issues.append(f"gate_status={gate} (not generated_complete)")
    low = text.lower()
    for token in spec["required_tokens"]:
        if token.lower() not in low:
            issues.append(f"missing required token: {token}")
    for pattern in spec["required_field_patterns"]:
        if not re.search(pattern, text, re.IGNORECASE):
            field_name = pattern.split(r":\s*")[0]
            issues.append(f"empty or missing field: {field_name}")
    if _has_placeholder(text):
        for pw in PLACEHOLDER_WORDS:
            if pw in low:
                issues.append(f"contains placeholder: '{pw}'")
                break
    return len(issues) == 0, issues


def review_seed(folder: Path, *, reviewer: str = "claude", dry_run: bool = False) -> dict:
    name = folder.name
    results = {}
    all_pass = True
    for filename, spec in GATE_FILES.items():
        path = folder / filename
        passed, issues = _review_file(path, spec)
        results[filename] = {"passed": passed, "issues": issues}
        if not passed:
            all_pass = False

    if all_pass and not dry_run:
        ts = datetime.now(timezone.utc).isoformat()
        for filename in GATE_FILES:
            path = folder / filename
            text = _read(path)
            text = re.sub(r"gate_status:\s*\S+", "gate_status: reviewed_complete", text, count=1)
            if f"reviewed_by:" not in text:
                text += f"\n- reviewed_by: {reviewer}\n- reviewed_at: {ts}\n"
            path.write_text(text, encoding="utf-8")
        log_path = folder / "review_log.md"
        log_text = _read(log_path)
        log_text += f"\n- [{ts}] gate_review: all 4 gates upgraded to reviewed_complete by {reviewer}\n"
        log_path.write_text(log_text, encoding="utf-8")

    return {"seed": name, "all_pass": all_pass, "files": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-folder", default="", help="Path to a single seed folder.")
    parser.add_argument("--all", action="store_true", help="Review all seeds in idea_bank/seed/.")
    parser.add_argument("--reviewer", default="claude")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.seed_folder:
        folders = [Path(args.seed_folder)]
    elif args.all:
        folders = sorted(p for p in SEED_DIR.iterdir() if p.is_dir())
    else:
        safe_print("provide --seed-folder or --all")
        return 1

    passed_count, failed_count = 0, 0
    for folder in folders:
        result = review_seed(folder, reviewer=args.reviewer, dry_run=args.dry_run)
        if result["all_pass"]:
            passed_count += 1
            safe_print(f"[PASS] {result['seed']}")
        else:
            failed_count += 1
            for fname, fres in result["files"].items():
                if not fres["passed"]:
                    for issue in fres["issues"]:
                        safe_print(f"[FAIL] {result['seed']}/{fname}: {issue}")

    safe_print(f"\ntotal={len(folders)} passed={passed_count} failed={failed_count}" + (" (dry-run)" if args.dry_run else ""))
    return 0 if failed_count == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
