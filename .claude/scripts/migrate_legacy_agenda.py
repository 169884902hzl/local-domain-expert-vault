"""Migrate legacy greenhouse/seed artifacts into v2 lanes without auto-promotion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kb_common import safe_print
from publish_research_run import migrate_legacy_status
from research_seed_v2_common import agenda_v2_path, agenda_root, ensure_v2_dirs


def migrate(*, apply: bool) -> dict[str, int]:
    ensure_v2_dirs()
    counts = {"legacy_seed_count": 0, "greenhouse_files": 0, "seed_candidates": 0}
    counts["legacy_seed_count"] = migrate_legacy_status(apply=apply)
    greenhouse_root = agenda_root() / "divergent"
    target_root = agenda_v2_path("greenhouse")
    if greenhouse_root.exists():
        for path in sorted(greenhouse_root.glob("*raw-candidates.json")):
            counts["greenhouse_files"] += 1
            run_date = path.name[:10]
            if apply:
                target = target_root / run_date / "raw-candidates.json"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Actually write legacy status files/copies. Default is report only.")
    args = parser.parse_args()
    counts = migrate(apply=args.apply)
    safe_print("MIGRATE_LEGACY_AGENDA: " + json.dumps(counts, ensure_ascii=False, sort_keys=True))
    if not args.apply:
        safe_print("DRY-RUN boundary: no legacy seed or greenhouse file was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
