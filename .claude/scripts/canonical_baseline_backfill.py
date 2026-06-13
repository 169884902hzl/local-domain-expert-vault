"""Build a canonical-baseline backfill queue from completed reading notes.

The daily arXiv scout is intentionally recency-biased. This companion audit
looks backward through strict readings and finds repeated strongest-baseline
signals whose original/canonical paper is not yet represented as a literature
note. It only writes a review queue; it does not import, read, publish, or
promote anything.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from arxiv_ranker import normalize_title
from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write, today_iso, vault_path


QUEUE_SCHEMA_VERSION = "canonical_baseline_backfill.v1"
DEFAULT_MIN_MENTIONS = 2
DEFAULT_LIMIT = 50
MAX_CONTEXTS_PER_ENTRY = 6

KNOWN_BASELINE_LABELS = [
    "HIL-SERL",
    "HiL-SERL",
    "SERL",
    "RLPD",
    "HG-DAgger",
    "DAgger",
    "DSRL",
    "Diffusion Policy",
    "Reactive Diffusion Policy",
    "RDP",
    "ACT",
    "MT-ACT",
    "OpenVLA-OFT",
    "OpenVLA",
    "VLA-Adapter",
    "pi0.5",
    "pi0",
    "π0.5",
    "π0",
    "GR00T N1",
    "GR00T",
    "TD-MPC2",
    "TD MPC two",
    "SAC",
    "PPO",
    "GRPO",
    "D4PG",
    "DIPO",
    "BVN",
    "MOKA",
    "ReKep",
    "RT-2-X",
    "Octo",
    "LIBERO",
    "RoboTwin",
    "CALVIN",
]

GENERAL_STOP_LABELS = {
    "DLO",
    "VLA",
    "VLM",
    "RL",
    "LLM",
    "IF",
    "C",
    "SR",
    "OOD",
    "RGB",
    "RGBD",
    "PDF",
    "API",
    "ROS",
    "UR",
    "GPU",
    "CPU",
    "DOF",
    "PID",
    "IK",
    "SOTA",
    "BC",
    "MLP",
    "RMSE",
    "PSNR",
    "SSIM",
    "LPIPS",
    "FID",
    "RTX",
}

NORMALIZED_STOP_LABELS = {
    "no-hardware",
    "dlo-specific",
    "proxy-baseline",
    "replacement-baseline",
    "baseline-pressure",
    "sota",
    "n1",
    "n1-5",
}

CANONICAL_TITLE_ALIASES = {
    "hil-serl": [
        "precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning",
    ],
    "hil serl": [
        "precise and dexterous robotic manipulation via human-in-the-loop reinforcement learning",
    ],
    "openvla-oft": [
        "openvla-oft",
    ],
    "diffusion policy": [
        "diffusion policy",
    ],
    "reactive diffusion policy": [
        "reactive diffusion policy",
    ],
}

ROBOTICS_CONTEXT_TERMS = [
    "robot",
    "robotic",
    "manipulation",
    "dexterous",
    "real-world",
    "sim-to-real",
    "vla",
    "dlo",
    "tactile",
    "bimanual",
    "contact",
    "reinforcement learning",
    "policy",
]


@dataclass(frozen=True)
class BaselineMention:
    label: str
    normalized_label: str
    note_path: str
    note_title: str
    zotero_key: str
    source: str
    context: str


def _section_body(text: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^##\s+{re.escape(heading)}\s*\n(?P<body>.*?)(?=^##\s+|\Z)")
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def _frontmatter_fields(text: str) -> dict[str, str]:
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}
    return parse_frontmatter_map(parsed[0])


def _clean_label(label: str) -> str:
    label = label.strip(" `*_.,;:()[]{}，。；：、")
    label = re.sub(r"\s+", " ", label)
    if label.lower() in {"td mpc two", "td-mpc two"}:
        return "TD-MPC2"
    if label in {"π0.5", "pi0.5", "PI0.5"}:
        return "pi0.5"
    if label in {"π0", "pi0", "PI0"}:
        return "pi0"
    if label.lower() == "hil-serl":
        return "HIL-SERL"
    return label


def _normalized_label(label: str) -> str:
    cleaned = _clean_label(label)
    normalized = normalize_title(cleaned).replace(" ", "-")
    if normalized in {"hi-l-serl", "hil-serl"}:
        return "hil-serl"
    return normalized


def _candidate_labels_from_context(context: str) -> list[str]:
    labels: list[str] = []
    scrubbed = re.sub(r"\[?(?:claim:)?C\d+\]?", " ", context)
    scrubbed = re.sub(r"\bSection\s+[IVXLCDM]+(?:-[A-Z])?\b", " ", scrubbed, flags=re.IGNORECASE)
    for label in sorted(KNOWN_BASELINE_LABELS, key=len, reverse=True):
        pattern = rf"(?<![A-Za-z0-9-]){re.escape(label)}(?![A-Za-z0-9-])"
        if re.search(pattern, scrubbed, flags=re.IGNORECASE):
            labels.append(_clean_label(label))

    for match in re.finditer(r"\b[A-Z][A-Za-z0-9]*(?:[-_.][A-Za-z0-9]+)+\b", scrubbed):
        labels.append(_clean_label(match.group(0)))
    for match in re.finditer(r"(?<![A-Za-z0-9-])([A-Z][A-Z0-9]{1,9})(?![A-Za-z0-9-])", scrubbed):
        labels.append(_clean_label(match.group(0)))
    for match in re.finditer(r"(?:π|pi)\s*0(?:\.5)?", scrubbed, flags=re.IGNORECASE):
        labels.append(_clean_label(match.group(0).replace(" ", "")))

    seen: set[str] = set()
    result: list[str] = []
    for label in labels:
        if not label:
            continue
        if label.upper() in GENERAL_STOP_LABELS:
            continue
        normalized = _normalized_label(label)
        if normalized in NORMALIZED_STOP_LABELS:
            continue
        if re.fullmatch(r"c\d+", normalized):
            continue
        if re.fullmatch(r"[ivxlcdm]+(?:-[a-z])?", normalized):
            continue
        if normalized.endswith("-specific"):
            continue
        if normalized.endswith("-based"):
            continue
        if len(normalized) < 2 or normalized in seen:
            continue
        seen.add(normalized)
        result.append(label)
    return result


def _baseline_context_lines(text: str) -> list[tuple[str, str]]:
    contexts: list[tuple[str, str]] = []
    baseline_body = _section_body(text, "Baseline Pressure")
    if baseline_body:
        for line in baseline_body.splitlines():
            stripped = line.strip()
            if re.search(r"strongest\s+baseline\s*:", stripped, flags=re.IGNORECASE):
                contexts.append(("baseline_pressure", stripped))

    evidence_body = _section_body(text, "Evidence Ledger")
    if evidence_body:
        for line in evidence_body.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if len(cells) < 3:
                continue
            if "baseline" in " ".join(cells[:3]).lower():
                contexts.append(("evidence_ledger_baseline", cells[2]))
    return contexts


def _iter_completed_literature_notes(root: Path) -> list[tuple[Path, str, dict[str, str], str]]:
    notes: list[tuple[Path, str, dict[str, str], str]] = []
    topics_dir = root / "wiki" / "topics"
    if not topics_dir.exists():
        return notes
    for path in sorted(topics_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        fields = _frontmatter_fields(text)
        if str(fields.get("type", "")).strip('"') != "literature":
            continue
        if str(fields.get("status", "")).strip('"') != "done":
            continue
        notes.append((path, text, fields, str(path.relative_to(root)).replace("\\", "/")))
    return notes


def collect_baseline_mentions(root: Path | None = None) -> list[BaselineMention]:
    root = root or vault_path()
    mentions: list[BaselineMention] = []
    for path, text, fields, rel_path in _iter_completed_literature_notes(root):
        note_title = str(fields.get("title", "")).strip('"') or path.stem
        zotero_key = str(fields.get("zotero_key", "")).strip('"')
        for source, context in _baseline_context_lines(text):
            for label in _candidate_labels_from_context(context):
                mentions.append(
                    BaselineMention(
                        label=_clean_label(label),
                        normalized_label=_normalized_label(label),
                        note_path=rel_path,
                        note_title=note_title,
                        zotero_key=zotero_key,
                        source=source,
                        context=context[:600],
                    )
                )
    return mentions


def _note_index(root: Path) -> list[dict[str, str]]:
    index: list[dict[str, str]] = []
    for path, text, fields, rel_path in _iter_completed_literature_notes(root):
        title = str(fields.get("title", "")).strip('"') or path.stem
        index.append(
            {
                "path": rel_path,
                "title": title,
                "normalized_title": normalize_title(title),
                "zotero_key": str(fields.get("zotero_key", "")).strip('"'),
                "head": text[:3000].lower(),
            }
        )
    return index


def _coverage_for_label(normalized_label: str, label: str, note_index: list[dict[str, str]]) -> dict[str, str]:
    label_title = normalize_title(label)
    aliases = CANONICAL_TITLE_ALIASES.get(normalized_label, [])
    alias_titles = {normalize_title(alias) for alias in aliases if alias}
    for item in note_index:
        normalized_title = item["normalized_title"]
        if label_title and label_title in normalized_title:
            return {"status": "covered_by_title", "path": item["path"], "title": item["title"], "zotero_key": item["zotero_key"]}
        if any(alias and alias in normalized_title for alias in alias_titles):
            return {"status": "covered_by_alias_title", "path": item["path"], "title": item["title"], "zotero_key": item["zotero_key"]}
    return {"status": "missing_canonical_note", "path": "", "title": "", "zotero_key": ""}


def _priority_score(label: str, mentions: list[BaselineMention]) -> tuple[int, list[str]]:
    contexts = " ".join(item.context for item in mentions).lower()
    unique_notes = len({item.note_path for item in mentions})
    score = unique_notes * 20 + len(mentions) * 5
    reasons = [f"source_notes:{unique_notes}", f"mentions:{len(mentions)}"]
    if "strongest baseline" in contexts or "strongest baseline" in label.lower():
        score += 20
        reasons.append("strongest_baseline_context")
    domain_hits = sorted({term for term in ROBOTICS_CONTEXT_TERMS if term in contexts})
    if domain_hits:
        score += min(20, len(domain_hits) * 3)
        reasons.append("robotics_context:" + ",".join(domain_hits[:6]))
    if label.lower() in {"hil-serl", "rlpd", "serl", "diffusion policy", "openvla-oft", "act"}:
        score += 15
        reasons.append("known_canonical_baseline")
    return score, reasons


def build_baseline_backfill_report(
    *,
    run_date: str | None = None,
    root: Path | None = None,
    min_mentions: int = DEFAULT_MIN_MENTIONS,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    root = root or vault_path()
    run_date = run_date or today_iso()
    mentions = collect_baseline_mentions(root)
    by_label: dict[str, list[BaselineMention]] = {}
    display_label: dict[str, str] = {}
    for mention in mentions:
        by_label.setdefault(mention.normalized_label, []).append(mention)
        display_label.setdefault(mention.normalized_label, mention.label)

    notes = _note_index(root)
    entries: list[dict[str, Any]] = []
    for normalized_label, label_mentions in by_label.items():
        unique_note_paths = sorted({mention.note_path for mention in label_mentions})
        if len(unique_note_paths) < min_mentions:
            continue
        label = display_label[normalized_label]
        coverage = _coverage_for_label(normalized_label, label, notes)
        priority, reasons = _priority_score(label, label_mentions)
        status = "covered" if coverage["status"].startswith("covered") else "queued"
        contexts = [
            {
                "note_path": mention.note_path,
                "note_title": mention.note_title,
                "zotero_key": mention.zotero_key,
                "source": mention.source,
                "context": mention.context,
            }
            for mention in label_mentions[:MAX_CONTEXTS_PER_ENTRY]
        ]
        entries.append(
            {
                "label": label,
                "normalized_label": normalized_label,
                "status": status,
                "coverage_status": coverage["status"],
                "covered_by": {key: coverage[key] for key in ("path", "title", "zotero_key") if coverage.get(key)},
                "mention_count": len(label_mentions),
                "source_note_count": len(unique_note_paths),
                "priority_score": priority,
                "reasons": reasons,
                "search_query": f'"{label}" robot manipulation baseline',
                "mentions": contexts,
            }
        )

    entries.sort(key=lambda item: (item["status"] != "queued", -int(item["priority_score"]), str(item["label"]).lower()))
    if limit > 0:
        entries = entries[:limit]
    return {
        "schema_version": QUEUE_SCHEMA_VERSION,
        "run_date": run_date,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "min_mentions": min_mentions,
        "limit": limit,
        "mention_total": len(mentions),
        "baseline_total": len(by_label),
        "entry_total": len(entries),
        "queued_total": sum(1 for item in entries if item["status"] == "queued"),
        "covered_total": sum(1 for item in entries if item["status"] == "covered"),
        "entries": entries,
        "boundary": "Queue only. This script does not import papers, run /read-paper, publish seeds, or write active-governance records.",
    }


def render_baseline_backfill_markdown(report: dict[str, Any]) -> str:
    run_date = str(report.get("run_date", today_iso()))
    queued_total = int(report.get("queued_total", 0))
    lines = [
        "---",
        f'title: "Canonical Baseline Backfill Queue - {run_date}"',
        "tags: [arxiv, baseline-backfill, literature]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        f'summary: "{queued_total} repeated baseline signals need canonical-paper backfill review."',
        "---",
        "",
        f"# Canonical Baseline Backfill Queue - {run_date}",
        "",
        f"- schema_version: {report.get('schema_version')}",
        f"- min_mentions: {report.get('min_mentions')}",
        f"- mention_total: {report.get('mention_total')}",
        f"- baseline_total: {report.get('baseline_total')}",
        f"- queued_total: {report.get('queued_total')}",
        f"- covered_total: {report.get('covered_total')}",
        "- boundary: queue only; no import, no /read-paper, no formal seed, no active seed.",
        "",
        "## Queued Canonical Baselines",
        "",
    ]
    queued = [item for item in report.get("entries", []) if item.get("status") == "queued"]
    if not queued:
        lines.append("- none")
    for index, item in enumerate(queued, 1):
        lines.extend(
            [
                f"### Q{index}. {item.get('label')}",
                "",
                f"- priority_score: {item.get('priority_score')}",
                f"- source_note_count: {item.get('source_note_count')}",
                f"- mention_count: {item.get('mention_count')}",
                f"- search_query: {item.get('search_query')}",
                f"- reasons: {', '.join(item.get('reasons', []))}",
                "",
            ]
        )
        for mention in item.get("mentions", [])[:3]:
            lines.append(f"  - `{mention.get('note_path')}`: {mention.get('context')}")
        lines.append("")
    covered = [item for item in report.get("entries", []) if item.get("status") == "covered"]
    lines.extend(["## Covered / No Backfill Needed", ""])
    if not covered:
        lines.append("- none")
    for item in covered[:25]:
        covered_by = item.get("covered_by", {}) if isinstance(item.get("covered_by"), dict) else {}
        lines.append(
            f"- {item.get('label')}: {item.get('coverage_status')} "
            f"`{covered_by.get('path', '-')}` mentions={item.get('mention_count')}"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_baseline_backfill_report(
    report: dict[str, Any],
    *,
    dry_run: bool = False,
    backup: bool = True,
    root: Path | None = None,
) -> tuple[Path, Path]:
    root = root or vault_path()
    run_date = str(report.get("run_date", today_iso()))
    out_dir = root / "projects" / "arxiv-daily" / "baseline-backfill"
    json_path = out_dir / f"{run_date}-baseline-backfill.json"
    md_path = out_dir / f"{run_date}-baseline-backfill.md"
    safe_write(json_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=backup)
    safe_write(md_path, render_baseline_backfill_markdown(report), dry_run=dry_run, backup=backup)
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", default=today_iso())
    parser.add_argument("--min-mentions", type=int, default=DEFAULT_MIN_MENTIONS)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print the report JSON to stdout.")
    args = parser.parse_args()

    report = build_baseline_backfill_report(
        run_date=args.run_date,
        min_mentions=max(1, args.min_mentions),
        limit=max(0, args.limit),
    )
    if args.json:
        safe_print(json.dumps(report, ensure_ascii=False, indent=2))
    json_path, md_path = write_baseline_backfill_report(report, dry_run=args.dry_run)
    safe_print(f"BASELINE_BACKFILL_JSON: {json_path.relative_to(vault_path())}")
    safe_print(f"BASELINE_BACKFILL_MD: {md_path.relative_to(vault_path())}")
    safe_print(f"BASELINE_BACKFILL_QUEUED: {report.get('queued_total', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
