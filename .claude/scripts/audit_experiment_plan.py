"""Audit an experiment plan for local-evidence proposal readiness."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, vault_path


REQUIRED_SECTIONS = [
    "## Research Question",
    "## Hypothesis",
    "## Evidence Base",
    "## Candidate Designs",
    "## Recommended Design",
    "## Protocol",
    "## Baselines",
    "## Metrics",
    "## Ablations",
    "## Hardware/Data Assumptions",
    "## Generalization Plan",
    "## Pilot Experiment",
    "## Risks & Fallback",
    "## Human Approval Checklist",
]
STAGE_VALUES = {"draft", "evidence-check", "pilot-ready", "archived"}
DECISION_VALUES = {"recommended_pending_approval", "approved", "rejected", "revised"}
EVIDENCE_VALUES = {"weak", "partial", "strong"}
NUMERIC_RE = re.compile(r"(?<![A-Za-z])(?:\d+(?:\.\d+)?\s*%?|\d+\s*/\s*\d+)")
CORRECTNESS_CLAIM_RE = re.compile(
    r"\b(?:is|are|confirmed|proven|guaranteed)\s+correct\b|"
    r"\bcorrect\s+(?:design|answer|solution|plan)\b|"
    r"已确认正确|确认正确|保证正确|必然正确",
    flags=re.IGNORECASE,
)


def rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def parse_note(path: Path) -> tuple[dict[str, str], str, list[str]]:
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text, ["missing_frontmatter"]
    fm_text, body = parsed
    return parse_frontmatter_map(fm_text), body, []


def section_content(body: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\s*\n+(.*?)(?=\n## |\Z)", body, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def wikilinks(text: str) -> list[str]:
    return re.findall(r"\[\[([^|\]#]+)", text)


def find_unreferenced_numeric_lines(body: str) -> list[str]:
    lines = []
    current_heading = ""
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current_heading = line
            continue
        if not line or current_heading == "## Evidence Base":
            continue
        if NUMERIC_RE.search(line) and "[[" not in line and "evidence_gap" not in line:
            lines.append(line[:220])
    return lines


def audit(path: Path, min_evidence: int) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    fields, body, parse_issues = parse_note(path)
    errors.extend(parse_issues)

    required_fields = ["title", "tags", "created", "updated", "type", "status", "summary", "stage", "decision_status", "evidence_level"]
    for field in required_fields:
        if field not in fields:
            errors.append(f"missing_frontmatter:{field}")
    if fields.get("type", "").strip('"') != "permanent":
        errors.append("frontmatter_type_must_be:permanent")
    if fields.get("stage", "").strip('"') not in STAGE_VALUES:
        errors.append("invalid_stage")
    if fields.get("decision_status", "").strip('"') not in DECISION_VALUES:
        errors.append("invalid_decision_status")
    if fields.get("evidence_level", "").strip('"') not in EVIDENCE_VALUES:
        errors.append("invalid_evidence_level")

    for heading in REQUIRED_SECTIONS:
        content = section_content(body, heading)
        if not content:
            errors.append(f"missing_or_empty_section:{heading.removeprefix('## ')}")

    evidence = section_content(body, "## Evidence Base")
    evidence_links = sorted(set(wikilinks(evidence)))
    if not evidence_links:
        errors.append("missing_local_evidence")
    elif len(evidence_links) < min_evidence:
        if "evidence_gap" in evidence:
            warnings.append(f"local_evidence_below_{min_evidence}:{len(evidence_links)}")
        else:
            errors.append(f"local_evidence_below_{min_evidence}:{len(evidence_links)}")

    if "evidence_gap:" in evidence and "evidence_gap: none" not in evidence:
        warnings.append("evidence_gap_present")
    if "evidence_gap: none" in evidence and "evidence_gap:" in body.replace(evidence, "", 1):
        warnings.append("evidence_gap_reference_outside_evidence_none")

    recommended = section_content(body, "## Recommended Design")
    if "recommended_pending_approval" not in recommended and fields.get("decision_status", "").strip('"') == "recommended_pending_approval":
        errors.append("recommended_design_missing_pending_approval_marker")
    if CORRECTNESS_CLAIM_RE.search(recommended):
        errors.append("recommended_design_claims_correctness")

    checklist = section_content(body, "## Human Approval Checklist")
    if "- [ ]" not in checklist:
        errors.append("missing_human_approval_checkboxes")

    numeric_lines = find_unreferenced_numeric_lines(body)
    if numeric_lines:
        errors.append("unreferenced_numeric_claims:" + " | ".join(numeric_lines[:5]))

    coverage = {
        "DLO": "DLO" in evidence or "deformable" in evidence.lower(),
        "tactile": "tactile" in evidence.lower() or "触觉" in evidence,
        "diffusion": "diffusion" in evidence.lower() or "扩散" in evidence,
        "bimanual_or_planning": "bimanual" in evidence.lower() or "双臂" in evidence or "planning" in evidence.lower() or "规划" in evidence,
        "benchmark_or_sim_to_real": (
            "benchmark" in evidence.lower()
            or "challenge" in evidence.lower()
            or "sim-to-real" in evidence.lower()
            or "sim2real" in evidence.lower()
            or "real-to-sim" in evidence.lower()
            or "基准" in evidence
            or "挑战赛" in evidence
            or "仿真到真实" in evidence
            or "仿真迁移" in evidence
        ),
    }
    missing_coverage = [key for key, ok in coverage.items() if not ok]
    if missing_coverage:
        warnings.append("missing_coverage:" + ", ".join(missing_coverage))

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "status": status,
        "path": rel(path),
        "errors": errors,
        "warnings": warnings,
        "evidence_count": len(evidence_links),
        "missing_coverage": missing_coverage,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Experiment plan path, relative to the vault root or absolute.")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--min-evidence", type=int, default=8)
    args = parser.parse_args()

    path = Path(args.path)
    if not path.is_absolute():
        path = vault_path(args.path)
    if not path.exists():
        safe_print(f"FAIL missing_file:{args.path}")
        return 1

    result = audit(path, args.min_evidence)
    if args.json:
        safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        safe_print(f"{result['status']} {result['path']} evidence_count={result['evidence_count']}")
        for error in result["errors"]:
            safe_print(f"ERROR: {error}")
        for warning in result["warnings"]:
            safe_print(f"WARN: {warning}")
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
