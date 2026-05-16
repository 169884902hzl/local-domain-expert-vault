"""Review long-term research agenda ideas and report maturity scores."""
from __future__ import annotations

import argparse
from datetime import date
import json
import re
import shutil
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write
from research_agenda_common import IDEA_BANK_DIR, IDEA_STATES, rel, strip_quotes


WIKILINK_RE = re.compile(r"\[\[([^|\]#]+)")
PLACEHOLDER_TOKENS = [
    "need_to_verify",
    "todo",
    "tbd",
    "define before promotion",
    "seed_pending_review",
    "explain why",
    "may be too broad",
    "narrow to a single pilot",
]
QUALITY_REJECT_PREFIXES = ["cross-gap between "]
GENERATED_GATE_TOKENS = ["gate_status: generated_complete", "gate_status: complete", "gate_status: reviewed", "gate_status: reviewed_complete"]
REVIEWED_GATE_TOKENS = ["gate_status: complete", "gate_status: reviewed", "gate_status: reviewed_complete"]


def _count_wikilinks(folder: Path) -> int:
    seen: set[str] = set()
    for path in folder.glob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        seen.update(WIKILINK_RE.findall(text))
    return len(seen)


def _file_text(folder: Path, filename: str) -> str:
    path = folder / filename
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _frontmatter_counts(folder: Path) -> tuple[int, int]:
    path = folder / "idea.md"
    if not path.exists():
        return 0, 0
    parsed = extract_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    if not parsed:
        return 0, 0
    fields = parse_frontmatter_map(parsed[0])
    try:
        evidence_count = int(fields.get("evidence_count", "0").strip('"'))
    except ValueError:
        evidence_count = 0
    try:
        recent_count = int(fields.get("recent_evidence_count", "0").strip('"'))
    except ValueError:
        recent_count = 0
    return evidence_count, recent_count


def _idea_title(folder: Path) -> str:
    text = _file_text(folder, "idea.md")
    parsed = extract_frontmatter(text)
    if parsed:
        fields = parse_frontmatter_map(parsed[0])
        title = fields.get("title", "").strip().strip('"')
        if title:
            return title
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else folder.name


def _frontmatter_state(folder: Path) -> str:
    text = _file_text(folder, "idea.md")
    parsed = extract_frontmatter(text)
    if not parsed:
        return ""
    fields = parse_frontmatter_map(parsed[0])
    state = strip_quotes(fields.get("idea_state", ""))
    return state if state in IDEA_STATES else ""


def _generated_by_ideate(folder: Path) -> bool:
    return "research_agenda_ideate.py" in _file_text(folder, "review_log.md")


def _has_gate_text(
    folder: Path,
    filename: str,
    tokens: list[str],
    *,
    gate_tokens: list[str],
    allow_placeholders: bool = False,
) -> bool:
    text = _file_text(folder, filename).lower()
    if not text:
        return False
    if not allow_placeholders and any(token in text for token in PLACEHOLDER_TOKENS):
        return False
    if filename in {"similar_work.md", "novelty_argument.md", "experiment_plan.md", "risk_review.md"}:
        if not any(token in text for token in gate_tokens):
            return False
    return all(token.lower() in text for token in tokens)


def review_folder(folder: Path, state: str) -> dict[str, Any]:
    title = _idea_title(folder)
    generated_by_ideate = _generated_by_ideate(folder)
    generic_generated_seed = generated_by_ideate and any(title.lower().startswith(prefix) for prefix in QUALITY_REJECT_PREFIXES)
    quality_flags: list[str] = []
    if generic_generated_seed:
        quality_flags.append("generic_generated_cross_gap")
    folder_link_count = _count_wikilinks(folder)
    evidence_count, recent_evidence_count = _frontmatter_counts(folder)
    evidence_count = max(evidence_count, len(set(WIKILINK_RE.findall(_file_text(folder, "evidence_pack.md")))))
    has_generated_similar = _has_gate_text(folder, "similar_work.md", ["similar"], gate_tokens=GENERATED_GATE_TOKENS)
    has_generated_novelty = _has_gate_text(folder, "novelty_argument.md", ["novelty"], gate_tokens=GENERATED_GATE_TOKENS)
    has_generated_experiment = _has_gate_text(folder, "experiment_plan.md", ["baseline", "metric", "pilot"], gate_tokens=GENERATED_GATE_TOKENS)
    has_generated_risk = _has_gate_text(folder, "risk_review.md", ["risk", "fallback"], gate_tokens=GENERATED_GATE_TOKENS)
    has_similar = _has_gate_text(folder, "similar_work.md", ["similar"], gate_tokens=REVIEWED_GATE_TOKENS)
    has_novelty = _has_gate_text(folder, "novelty_argument.md", ["novelty"], gate_tokens=REVIEWED_GATE_TOKENS)
    has_experiment = _has_gate_text(folder, "experiment_plan.md", ["baseline", "metric", "pilot", "failure"], gate_tokens=REVIEWED_GATE_TOKENS)
    has_risk = _has_gate_text(folder, "risk_review.md", ["risk", "fallback"], gate_tokens=REVIEWED_GATE_TOKENS)
    developing_ready = (
        not quality_flags
        and evidence_count >= 8
        and recent_evidence_count >= 2
        and has_similar
        and has_novelty
        and has_experiment
        and has_risk
    )
    promoted_ready = (
        not quality_flags
        and evidence_count >= 12
        and recent_evidence_count >= 3
        and has_similar
        and has_novelty
        and has_experiment
        and has_risk
    )
    score = min(evidence_count, 12) * 6 + min(recent_evidence_count, 5) * 4
    score += 15 if has_similar else 0
    score += 15 if has_novelty else 0
    score += 20 if has_experiment else 0
    score += 10 if has_risk else 0
    if quality_flags:
        score = min(score, 5)
    recommended_state = state
    if state == "seed" and generic_generated_seed:
        recommended_state = "rejected"
    if state == "seed" and developing_ready:
        recommended_state = "developing"
    if state == "developing" and promoted_ready:
        recommended_state = "promoted"
    if state == "promoted" and not promoted_ready:
        recommended_state = "developing"
    return {
        "path": rel(folder),
        "title": title,
        "state": state,
        "score": score,
        "evidence_count": evidence_count,
        "recent_evidence_count": recent_evidence_count,
        "folder_link_count": folder_link_count,
        "has_similar_work": has_similar,
        "has_novelty_argument": has_novelty,
        "has_experiment_plan": has_experiment,
        "has_risk_review": has_risk,
        "has_generated_similar_work": has_generated_similar,
        "has_generated_novelty_argument": has_generated_novelty,
        "has_generated_experiment_plan": has_generated_experiment,
        "has_generated_risk_review": has_generated_risk,
        "developing_ready": developing_ready,
        "promoted_ready": promoted_ready,
        "recommended_state": recommended_state,
        "quality_flags": quality_flags,
        "generated_by_ideate": generated_by_ideate,
    }


def iter_idea_folders() -> list[tuple[str, Path]]:
    by_slug: dict[str, tuple[int, str, Path]] = {}
    for state in IDEA_STATES:
        root = IDEA_BANK_DIR / state
        if not root.exists():
            continue
        for path in sorted(root.iterdir()):
            if path.is_dir():
                logical_state = _frontmatter_state(path)
                if state != "seed" and logical_state == "seed":
                    logical_state = state
                if not logical_state:
                    logical_state = state
                rank = 0 if state == logical_state else 1
                if logical_state in {"rejected", "archived"}:
                    rank -= 1
                current = by_slug.get(path.name)
                if current is None or rank < current[0]:
                    by_slug[path.name] = (rank, logical_state, path)
    return [(state, path) for _, state, path in sorted(by_slug.values(), key=lambda item: str(item[2]))]


def apply_recommendations(results: list[dict[str, Any]]) -> None:
    for result in results:
        state = result["state"]
        recommended = result["recommended_state"]
        if state == recommended:
            continue
        source = Path(result["path"])
        if not source.is_absolute():
            source = Path.cwd() / source
        target = IDEA_BANK_DIR / recommended / source.name
        if recommended == "rejected":
            _mark_state(source, recommended, result.get("quality_flags", []))
            if target.exists():
                _mark_state(target, recommended, result.get("quality_flags", []))
            continue
        if target.exists():
            _mark_state(source, recommended, result.get("quality_flags", []))
            _mark_state(target, recommended, result.get("quality_flags", []))
            continue
        try:
            shutil.move(str(source), str(target))
            _mark_state(target, recommended, result.get("quality_flags", []))
        except PermissionError:
            _mark_state(source, recommended, result.get("quality_flags", []))


def _mark_state(folder: Path, state: str, quality_flags: list[str]) -> None:
    idea = folder / "idea.md"
    if idea.exists():
        text = idea.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"tags:\s*\[research-agenda,\s*idea,\s*[^\]]+\]", f"tags: [research-agenda, idea, {state}]", text)
        text = re.sub(r"idea_state:\s*\S+", f"idea_state: {state}", text)
        if state == "rejected":
            text = text.replace("- decision_status: seed_pending_review", "- decision_status: rejected_by_quality_gate")
            if "## Quality Gate Result" not in text:
                text = text.rstrip() + "\n\n## Quality Gate Result\n\n- rejected_reason: " + ", ".join(quality_flags or ["quality_gate_failed"]) + "\n"
        safe_write(idea, text, dry_run=False, backup=True)
    review_log = folder / "review_log.md"
    existing = review_log.read_text(encoding="utf-8", errors="replace") if review_log.exists() else "# Review Log\n"
    line = f"- {date.today().isoformat()}: moved_to={state}; quality_flags={','.join(quality_flags) or '-'}\n"
    safe_write(review_log, existing.rstrip() + "\n" + line, dry_run=False, backup=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--apply", action="store_true", help="Move idea folders to the recommended state.")
    args = parser.parse_args()

    results = [review_folder(folder, state) for state, folder in iter_idea_folders()]
    if args.apply:
        apply_recommendations(results)
    if args.json:
        safe_print(json.dumps({"ideas": results}, ensure_ascii=False, indent=2))
    else:
        safe_print(f"REVIEW ideas={len(results)}")
        for item in results:
            safe_print(
                f"{item['state']} score={item['score']} evidence={item['evidence_count']} "
                f"recommended={item['recommended_state']} {item['path']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
