"""Audit v1 Research Governance Workbench hard invariants."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from kb_common import vault_path
from research_governance_common import PUBLIC_FORBIDDEN_PARTS, PUBLIC_FORBIDDEN_SUFFIXES, scheduled_command_errors
from state_machine_guard import run_audit as run_state_machine_audit


def _git_files(root: Path) -> list[str]:
    output = subprocess.check_output(["git", "ls-files"], cwd=root, text=True)
    return [line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()]


def audit_public_artifact_paths(root: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for rel in _git_files(root):
        if Path(rel).name == ".gitkeep":
            continue
        lower = rel.lower()
        if Path(lower).suffix in PUBLIC_FORBIDDEN_SUFFIXES:
            issues.append({"level": "FAIL", "code": "tracked_runtime_private_artifact", "path": rel})
        for part in PUBLIC_FORBIDDEN_PARTS:
            if part in lower:
                issues.append({"level": "FAIL", "code": "tracked_forbidden_runtime_path", "path": rel, "matched": part})
    return issues


def audit_publish_disabled(root: Path) -> list[dict[str, Any]]:
    publish = root / ".claude" / "scripts" / "publish_research_run.py"
    text = publish.read_text(encoding="utf-8")
    if "legacy_formal_publish_disabled_use_formal_rehearsal_packet" not in text:
        return [{"level": "FAIL", "code": "publish_formal_disable_status_missing", "path": str(publish)}]
    return []


def run_audit(*, strict: bool) -> dict[str, Any]:
    root = vault_path()
    issues = run_state_machine_audit()["issues"]
    issues.extend(audit_public_artifact_paths(root))
    issues.extend(audit_publish_disabled(root))
    wrapper = root / ".claude" / "scripts" / "run_daily_arxiv_task.ps1"
    if wrapper.exists():
        issues.extend({"level": "FAIL", "code": error.split(":", 1)[0], "detail": error} for error in scheduled_command_errors(wrapper.read_text(encoding="utf-8")))
    return {"schema_version": "governance_invariant_audit.v1", "status": "success" if not issues else "failed", "strict": strict, "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    payload = run_audit(strict=args.strict)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
