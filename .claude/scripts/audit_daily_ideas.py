"""Audit daily embodied-AI idea notes for evidence-cluster completeness."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, vault_path


REQUIRED_FIELDS = [
    "Problem",
    "Hypothesis",
    "Decision Status",
    "Cross-paper Pattern",
    "Knowledge Base Support",
    "Novelty Hypothesis",
    "Why Now",
    "Current Practice",
    "Similar Work",
    "Implementation Plan",
    "Pilot Experiment",
    "Variables",
    "Baselines",
    "Metrics",
    "Evidence Cluster",
    "Risk",
    "Next Step",
]
IDEA_RE = re.compile(r"^## Idea\s+\d+:", flags=re.MULTILINE)
NUMERIC_RE = re.compile(
    r"(?<![A-Za-z])(?:"
    r"\d+(?:\.\d+)?\s*%"
    r"|\d+\s*/\s*\d+"
    r"|\d+(?:\.\d+)?\s*(?:-|to)\s*\d+(?:\.\d+)?"
    r"|\d+(?:\.\d+)?\s*(?:K\+|k\+|x|Hz|FPS|ms|sec(?:onds?)?|min(?:utes?)?)\b"
    r"|\d+(?:\.\d+)?\s*(?:demos?|demonstrations?|episodes?|rollouts?|samples?|tasks?|steps?|conditions?)\b"
    r"|\d+(?:\.\d+)?[- ](?:step|stage|view|arm|task)\b"
    r")",
    flags=re.IGNORECASE,
)
OVERCLAIM_RE = re.compile(r"\b(?:guaranteed|proven|confirmed)\b|必然正确|保证正确|已经证实", flags=re.IGNORECASE)
WIKILINK_RE = re.compile(r"\[\[([^|\]#]+)")


def _rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def _sections(body: str) -> list[tuple[str, str]]:
    matches = list(IDEA_RE.finditer(body))
    sections = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        heading = match.group(0).strip()
        sections.append((heading, body[start:end]))
    return sections


def _evidence_cluster(section: str) -> str:
    match = re.search(r"- Evidence Cluster:\s*(.*?)(?=\n- [A-Z][A-Za-z -]+:|\Z)", section, flags=re.DOTALL)
    return match.group(1) if match else ""


def _daily_paper_count(section: str) -> int:
    cluster = _evidence_cluster(section)
    return len(re.findall(r"arXiv:", cluster))


def _local_done_paper_count(section: str) -> int:
    cluster = _evidence_cluster(section)
    count = 0
    seen: set[str] = set()
    for target in WIKILINK_RE.findall(cluster):
        stem = target.strip()
        if stem in seen:
            continue
        seen.add(stem)
        path = vault_path("wiki", "topics", f"{stem}.md")
        if not path.exists():
            continue
        parsed = extract_frontmatter(path.read_text(encoding="utf-8"))
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        if fields.get("status", "").strip('"') == "done":
            count += 1
    return count


def _has_evidence_cluster(section: str) -> bool:
    cluster = _evidence_cluster(section)
    return bool(cluster and ("[[" in cluster or "](http" in cluster or "arxiv.org" in cluster))


def _unreferenced_numeric_lines(body: str) -> list[str]:
    lines = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "arxiv:" in line.lower() or "score=" in line.lower():
            continue
        if NUMERIC_RE.search(line) and "[[" not in line and "](http" not in line:
            lines.append(line[:220])
    return lines


def audit(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    fields: dict[str, str] = {}
    body = text
    if not parsed:
        errors.append("missing_frontmatter")
    else:
        fm_text, body = parsed
        fields = parse_frontmatter_map(fm_text)
    if fields.get("type", "").strip('"') != "permanent":
        errors.append("frontmatter_type_must_be:permanent")
    if fields.get("evidence_level", "").strip('"') not in {"weak", "partial", "strong"}:
        errors.append("invalid_or_missing_evidence_level")

    tags = fields.get("tags", "")
    if "compatibility" in tags and "agenda_delta:" in body:
        return {
            "status": "WARN",
            "path": _rel(path),
            "idea_count": 0,
            "errors": [],
            "warnings": ["compatibility_pointer_only:not_final_idea_source"],
        }

    ideas = _sections(body)
    if len(ideas) < 5:
        errors.append(f"idea_count_below_5:{len(ideas)}")
    for heading, section in ideas:
        for field in REQUIRED_FIELDS:
            if f"- {field}:" not in section and field != "Evidence Cluster":
                errors.append(f"{heading}:missing_field:{field}")
        if "- Candidate Signal:" in section:
            errors.append(f"{heading}:single_candidate_signal_field_present")
        if "- Evidence Cluster:" not in section:
            errors.append(f"{heading}:missing_field:Evidence Cluster")
        elif not _has_evidence_cluster(section):
            errors.append(f"{heading}:missing_evidence_cluster_link")
        daily_count = _daily_paper_count(section)
        if daily_count < 2:
            errors.append(f"{heading}:too_few_daily_papers:{daily_count}")
        local_done_count = _local_done_paper_count(section)
        if local_done_count < 3:
            errors.append(f"{heading}:too_few_local_done_papers:{local_done_count}")
        if "not proof" not in section and "hypothesis scaffold" not in section:
            warnings.append(f"{heading}:missing_hypothesis_boundary")
        if OVERCLAIM_RE.search(section):
            errors.append(f"{heading}:overclaim_detected")

    numeric_lines = _unreferenced_numeric_lines(body)
    if numeric_lines:
        errors.append("unreferenced_numeric_claims:" + " | ".join(numeric_lines[:5]))

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {"status": status, "path": _rel(path), "idea_count": len(ideas), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_absolute():
        path = vault_path(args.path)
    if not path.exists():
        safe_print(f"FAIL missing_file:{args.path}")
        return 1
    result = audit(path)
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(f"{result['status']} {result['path']} idea_count={result['idea_count']}")
        for error in result["errors"]:
            safe_print(f"ERROR: {error}")
        for warning in result["warnings"]:
            safe_print(f"WARN: {warning}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
