"""Non-destructively migrate legacy v0.3 research seed artifacts into v1 legacy-v03."""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from typing import Any
from research_governance_common import agenda_root, legacy_v03_dir, utc_now, write_json

LEGACY_RELATIVE_DIRS = ["idea_bank/seed", "seed-candidates", "parked", "rescue", "runs"]

def _copy_tree(src: Path, dst: Path, *, dry_run: bool) -> None:
    if dry_run or not src.exists() or dst.exists():
        return
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.log", "*.sqlite", "*.db", "*.pdf", "__pycache__"))

def build_report(*, dry_run: bool) -> dict[str, Any]:
    root = agenda_root()
    copied, missing = [], []
    for rel in LEGACY_RELATIVE_DIRS:
        src = root / rel
        dst = legacy_v03_dir() / rel.replace("/", "__")
        if src.exists():
            copied.append({"source": str(src), "target": str(dst), "status": "planned" if dry_run else "copied"})
            _copy_tree(src, dst, dry_run=dry_run)
        else:
            missing.append(rel)
    report = {"schema_version": "legacy_migration.v1", "created_at": utc_now(), "dry_run": dry_run, "legacy_status": "archived_legacy", "auto_promote_allowed": False, "migrated_novelty_caches_marked_stale": True, "copied": copied, "missing": missing, "rollback_plan": ["No destructive moves are performed.", "Remove projects/research-agenda/legacy-v03 if this migration output is not wanted.", "Candidate-only daily can be restored after audit.", "Legacy formal/active publish must not be restored."], "boundary": "Legacy v0.3 artifacts are archived for traceability and never auto-promote into v1 active seeds."}
    if not dry_run:
        write_json(legacy_v03_dir() / "migration-report.json", report)
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build_report(dry_run=args.dry_run), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
