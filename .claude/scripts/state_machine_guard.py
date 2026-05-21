"""Audit and validate v1 Research Governance Workbench state transitions."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

from kb_common import vault_path
from research_governance_common import SCHEDULED_FORBIDDEN_STATES, STATES, scheduled_command_errors, transition_errors


ALLOWED_GOVERNANCE_WRITERS = {"active_seed_commit.py", "research_governance_common.py"}


def _script_files() -> list[Path]:
    return sorted((vault_path(".claude", "scripts")).glob("*.py"))


def _has_write_call(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in {"write_json", "append_jsonl", "write_text", "write_run_artifact", "open"}:
            return True
        if isinstance(func, ast.Attribute) and func.attr in {"write_text", "rename", "mkdir"}:
            return True
    return False


def audit_direct_governance_writers() -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for path in _script_files():
        text = path.read_text(encoding="utf-8")
        mentions_target = any(token in text.replace("\\", "/") for token in ["governance/active-seeds", "governance-ledger.jsonl"])
        mentions_parts = any(token in text for token in ['"active-seeds"', "'active-seeds'", '"governance-ledger.jsonl"', "'governance-ledger.jsonl'"])
        if not (mentions_target or mentions_parts):
            continue
        try:
            writes = _has_write_call(ast.parse(text))
        except SyntaxError:
            writes = True
        if writes and path.name not in ALLOWED_GOVERNANCE_WRITERS:
            issues.append({"level": "FAIL", "code": "direct_governance_writer_outside_active_seed_commit", "path": str(path)})
    return issues


def audit_scheduled_wrappers() -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    wrapper = vault_path(".claude", "scripts", "run_daily_arxiv_task.ps1")
    if not wrapper.exists():
        return [{"level": "FAIL", "code": "missing_scheduled_wrapper", "path": str(wrapper)}]
    for error in scheduled_command_errors(wrapper.read_text(encoding="utf-8")):
        issues.append({"level": "FAIL", "code": error.split(":", 1)[0], "detail": error})
    return issues


def run_audit() -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    if not STATES:
        issues.append({"level": "FAIL", "code": "state_machine_empty"})
    for state in SCHEDULED_FORBIDDEN_STATES:
        if state not in STATES:
            issues.append({"level": "FAIL", "code": "scheduled_forbidden_state_unknown", "state": state})
    issues.extend(audit_direct_governance_writers())
    issues.extend(audit_scheduled_wrappers())
    return {"schema_version": "state_machine_audit.v1", "status": "success" if not issues else "failed", "issues": issues}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-state", default="")
    parser.add_argument("--to-state", default="")
    parser.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.audit:
        payload = run_audit()
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if payload["status"] == "success" else 1
    if not args.from_state or not args.to_state:
        parser.error("--from-state and --to-state are required unless --audit is used")
    errors = transition_errors(args.from_state, args.to_state, mode=args.mode)
    payload = {"schema_version": "state_transition.v1", "from_state": args.from_state, "to_state": args.to_state, "mode": args.mode, "valid": not errors, "errors": errors}
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) if args.json else ("OK" if not errors else "FAIL " + ";".join(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
