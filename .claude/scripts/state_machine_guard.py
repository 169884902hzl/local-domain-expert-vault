"""Audit and validate v1 Research Governance Workbench state transitions."""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path
from typing import Any

from kb_common import vault_path
from research_governance_common import SCHEDULED_FORBIDDEN_STATES, STATES, scheduled_command_errors, transition_errors


SENSITIVE_WRITE_TARGETS = {
    "seed": ["idea_bank/seed", "projects/research-agenda/idea_bank/seed"],
    "active_seeds": ["governance/active-seeds", "active-seeds", "active-seed-record.json"],
    "ledger": ["governance/ledger", "governance-ledger.jsonl"],
    "formal_rehearsal": ["formal-rehearsal", "formal_rehearsal", "formal-rehearsals"],
}
WRITE_APIS = {
    "open",
    "Path.open",
    "write_text",
    "write_bytes",
    "safe_write",
    "safe_write_json",
    "write_json",
    "append_jsonl",
    "copy",
    "copy2",
    "copytree",
    "move",
    "rmtree",
    "remove",
    "unlink",
    "replace",
    "rename",
    "mkdir",
}
POWERSHELL_MUTATION_RE = re.compile(
    r"\b(Set-Content|Add-Content|Out-File|New-Item|Copy-Item|Move-Item|Remove-Item|Rename-Item)\b",
    re.IGNORECASE,
)


def _source_files() -> list[Path]:
    roots = [
        vault_path(".claude", "scripts"),
        vault_path("tools"),
    ]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*.py") if path.is_file())
            files.extend(path for path in root.rglob("*.ps1") if path.is_file())
    files.extend(path for path in vault_path().glob("*.py") if path.is_file())
    return sorted(set(files))


def _node_tokens(node: ast.AST) -> list[str]:
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.Add)):
        return [*_node_tokens(node.left), *_node_tokens(node.right)]
    if isinstance(node, ast.Constant):
        return [str(node.value)]
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        return [node.attr, *_node_tokens(node.value)]
    if isinstance(node, ast.Call):
        tokens: list[str] = []
        for arg in node.args:
            tokens.extend(_node_tokens(arg))
        for keyword in node.keywords:
            tokens.extend(_node_tokens(keyword.value))
        if isinstance(node.func, ast.Name):
            return [f"{node.func.id}()", *tokens]
        if isinstance(node.func, ast.Attribute):
            return [node.func.attr, *_node_tokens(node.func.value), *tokens]
    if isinstance(node, ast.Subscript):
        return [*_node_tokens(node.value), *_node_tokens(node.slice)]
    if isinstance(node, ast.JoinedStr):
        return ["".join(str(part.value) for part in node.values if isinstance(part, ast.Constant))]
    return []


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        base = ".".join(_node_tokens(func.value))
        return f"{base}.{func.attr}" if base else func.attr
    return ""


def _target_kinds(expr: ast.AST, variable_targets: dict[str, set[str]]) -> set[str]:
    tokens = _node_tokens(expr)
    kinds: set[str] = set()
    for token in tokens:
        kinds.update(variable_targets.get(token, set()))
    normalized = "/".join(token.lower().replace("\\", "/") for token in tokens)
    for kind, markers in SENSITIVE_WRITE_TARGETS.items():
        if any(marker in normalized for marker in markers):
            kinds.add(kind)
    if "idea_bank" in normalized and "/seed" in normalized:
        kinds.add("seed")
    if "active_seed_dir()" in normalized:
        kinds.add("active_seeds")
    if "active-seed-record.json" in normalized:
        kinds.add("active_seeds")
    if "governance_ledger_path()" in normalized:
        kinds.add("ledger")
    if "governance" in normalized and "ledger" in normalized:
        kinds.add("ledger")
    return kinds


def _write_target_exprs(node: ast.Call) -> list[ast.AST]:
    name = _call_name(node)
    short = name.split(".")[-1]
    if short not in {api.split(".")[-1] for api in WRITE_APIS}:
        return []
    if short == "open":
        mode = ""
        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
            mode = str(node.args[1].value)
        for keyword in node.keywords:
            if keyword.arg == "mode" and isinstance(keyword.value, ast.Constant):
                mode = str(keyword.value.value)
        if not any(flag in mode for flag in ("w", "a", "x", "+")):
            return []
        return list(node.args[:1])
    if short in {"copy", "copy2", "copytree", "move"}:
        return list(node.args[1:2])
    if short in {"replace", "rename"} and isinstance(node.func, ast.Attribute):
        return list(node.args[:1])
    if short in {"unlink", "remove", "rmtree"}:
        targets = list(node.args[:1])
        if isinstance(node.func, ast.Attribute):
            targets.append(node.func.value)
        return targets
    targets = list(node.args[:1])
    if short in {"write_text", "write_bytes", "mkdir"} and isinstance(node.func, ast.Attribute):
        targets.append(node.func.value)
    return targets


def _allowed_write(path: Path, kinds: set[str]) -> bool:
    if "tests" in path.parts:
        return True
    if path.name == "active_seed_commit.py":
        return kinds <= {"active_seeds", "ledger"}
    if path.name == "formal_rehearsal_packet.py":
        return kinds <= {"formal_rehearsal"}
    if path.name == "migrate_v03_to_v10.py":
        return not (kinds & {"seed", "active_seeds", "ledger", "formal_rehearsal"})
    return False


def _kinds_in_text(text: str) -> set[str]:
    normalized = text.lower().replace("\\", "/")
    kinds: set[str] = set()
    for kind, markers in SENSITIVE_WRITE_TARGETS.items():
        if any(marker in normalized for marker in markers):
            kinds.add(kind)
    if "idea_bank" in normalized and "/seed" in normalized:
        kinds.add("seed")
    return kinds


def scan_powershell_sensitive_writes(path: Path, text: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for index, line in enumerate(text.splitlines(), start=1):
        if not POWERSHELL_MUTATION_RE.search(line):
            continue
        kinds = _kinds_in_text(line)
        if kinds and not _allowed_write(path, kinds):
            issues.append(
                {
                    "level": "FAIL",
                    "code": "sensitive_governance_writer",
                    "path": str(path),
                    "line": index,
                    "targets": sorted(kinds),
                    "call": POWERSHELL_MUTATION_RE.search(line).group(1),
                }
            )
    return issues


def scan_sensitive_writes(path: Path, text: str) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    try:
        tree = ast.parse(text.lstrip("\ufeff"), filename=str(path))
    except SyntaxError as exc:
        return [{"level": "FAIL", "code": "state_machine_guard_parse_failed", "path": str(path), "detail": f"{type(exc).__name__}:{exc}"}]
    variable_targets: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            value = node.value
            if value is None:
                continue
            kinds = _target_kinds(value, variable_targets)
            if kinds:
                for target in targets:
                    if isinstance(target, ast.Name):
                        variable_targets.setdefault(target.id, set()).update(kinds)
        if isinstance(node, ast.Call):
            kinds: set[str] = set()
            for expr in _write_target_exprs(node):
                kinds.update(_target_kinds(expr, variable_targets))
            if kinds and not _allowed_write(path, kinds):
                issues.append(
                    {
                        "level": "FAIL",
                        "code": "sensitive_governance_writer",
                        "path": str(path),
                        "line": getattr(node, "lineno", 0),
                        "targets": sorted(kinds),
                        "call": _call_name(node),
                    }
                )
    return issues


def audit_direct_governance_writers() -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for path in _source_files():
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".ps1":
            issues.extend(scan_powershell_sensitive_writes(path, text))
        else:
            issues.extend(scan_sensitive_writes(path, text))
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
