"""Export a redacted research run packet for human/GPTPro review."""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from research_seed_v2_common import agenda_v2_path, artifact_dir, publish_dir, read_json, run_dir, v2_rel, write_json


PACKET_ARTIFACTS = [
    "intake-triage.json",
    "paper-primitives-snapshot.jsonl",
    "claim-graph-snapshot.jsonl",
    "tension-map.json",
    "raw-candidates.json",
    "selected-candidates.json",
    "deepseek-review.json",
    "novelty-scan.json",
    "codex-execution-review.json",
    "survival-decision.json",
    "manual-prior-art-review.json",
    "baseline-table.json",
    "pdf-evidence-anchors.json",
    "active-seed-dashboard.json",
]
PACKET_TEXT_ARTIFACTS = [
    "active-seed-dashboard.md",
]

PRIVATE_PATH_RE = re.compile(r"[A-Z]:\\|/Users/|\\\\")
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|AIza[A-Za-z0-9_-]{20,})")
DROP_KEYS = {
    "payload",
    "raw_payload",
    "cache_payload",
    "request_headers",
    "api_key",
    "authorization",
    "source_pdf",
    "zotero_api_key",
    "token",
    "access_token",
    "refresh_token",
}


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            if str(key).lower() in DROP_KEYS:
                redacted[key] = "[redacted]"
            else:
                redacted[key] = _redact(item)
        return redacted
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, str):
        text = SECRET_RE.sub("[redacted-secret]", value)
        if PRIVATE_PATH_RE.search(text):
            return "[redacted-private-path]"
        return text
    return value


def _read_artifact(path: Path) -> Any:
    if path.suffix == ".jsonl":
        return [_redact(json.loads(line)) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if path.suffix.lower() in {".md", ".txt"}:
        return _redact(path.read_text(encoding="utf-8-sig"))
    return _redact(read_json(path))


def _week_id(run_date: str) -> str:
    day = date.fromisoformat(run_date)
    year, week, _weekday = day.isocalendar()
    return f"{year}-W{week:02d}"


def _collect_optional_payloads(run_date: str) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    pilot_root = agenda_v2_path("pilots")
    if pilot_root.exists():
        pilot_payloads = [
            {"path": v2_rel(path), "content": _read_artifact(path)}
            for path in sorted(pilot_root.glob("*/*.json"))
            if path.name in {"pilot-plan.json", "result.json", "feedback-to-strategy.json"}
        ]
        if pilot_payloads:
            items.append(("pilot-artifacts.json", {"pilot_artifacts": pilot_payloads}))
    weekly = agenda_v2_path("strategy", "resurrection-review", f"{_week_id(run_date)}.json")
    if weekly.exists():
        items.append(("weekly-resurrection-review.json", _read_artifact(weekly)))
    audit = vault_path("projects", "arxiv-daily", "quality", f"{run_date}-daily-quality-audit.json")
    if audit.exists():
        items.append(("daily-quality-audit.json", _read_artifact(audit)))
    return items


def export_packet(run_date: str, *, dry_run: bool = False) -> dict[str, Any]:
    out_dir = publish_dir(run_date) / "run-packet"
    manifest = {
        "schema_version": "research_run_packet.v1",
        "run_date": run_date,
        "source_run_dir": v2_rel(run_dir(run_date)),
        "included": [],
        "excluded": [
            "raw PDFs",
            "raw/readings",
            "provider cache payloads",
            "logs",
            ".sqlite files",
            "private absolute paths",
            "secrets",
        ],
        "boundary": "Review packet only; it is not proof of novelty, publishability, or doctoral-level quality.",
    }
    if dry_run:
        return manifest
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in PACKET_ARTIFACTS:
        path = artifact_dir(run_date) / name
        if not path.exists():
            continue
        data = _read_artifact(path)
        out_name = name.replace(".jsonl", ".json")
        write_json(out_dir / out_name, {"artifact": name, "content": data}, dry_run=False)
        manifest["included"].append(out_name)
    for name in PACKET_TEXT_ARTIFACTS:
        path = artifact_dir(run_date) / name
        if not path.exists():
            continue
        write_json(out_dir / f"{name}.json", {"artifact": name, "content": _read_artifact(path)}, dry_run=False)
        manifest["included"].append(f"{name}.json")
    for out_name, data in _collect_optional_payloads(run_date):
        write_json(out_dir / out_name, {"artifact": out_name, "content": data}, dry_run=False)
        manifest["included"].append(out_name)
    publish_result = publish_dir(run_date) / "publish-result.json"
    if not publish_result.exists():
        legacy = artifact_dir(run_date) / "publish-result.json"
        publish_result = legacy if legacy.exists() else publish_result
    if publish_result.exists():
        write_json(out_dir / "publish-result.json", {"artifact": "publish-result.json", "content": _read_artifact(publish_result)}, dry_run=False)
        manifest["included"].append("publish-result.json")
    write_json(out_dir / "manifest.json", manifest, dry_run=False)
    return {**manifest, "packet_dir": v2_rel(out_dir)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = export_packet(args.run_date, dry_run=args.dry_run)
    safe_print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
