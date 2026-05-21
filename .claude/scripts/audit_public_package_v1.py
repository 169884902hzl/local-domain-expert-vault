"""Fail if the public package contains v1-forbidden runtime or private artifacts."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from kb_common import vault_path
from research_governance_common import PUBLIC_FORBIDDEN_PARTS, PUBLIC_FORBIDDEN_SUFFIXES


SECRET_RE = re.compile(
    "|".join(
        [
            r"sk-[A-Za-z0-9_-]{20,}",
            r"ghp_[A-Za-z0-9_]{20,}",
            r"github_pat_[A-Za-z0-9_]{20,}",
            r"AIza[A-Za-z0-9_-]{20,}",
            "PRIVATE " + "KEY",
            "BEGIN " + "RSA",
            "ANTHROPIC_AUTH_TOKEN" + r"\s*=\s*(?!<|\"\"|'')[^\s#]+",
            "OPENAI_API_KEY" + r"\s*=\s*(?!<|\"\"|'')[^\s#]+",
            "GEMINI_API_KEY" + r"\s*=\s*(?!<|\"\"|'')[^\s#]+",
            "ZOTERO_API_KEY" + r"\s*=\s*(?!<|\"\"|'')[^\s#]+",
            "H:" + r"\\",
            "C:" + r"\\Users\\Administrator",
        ]
    )
)


def git_files(root: Path) -> list[str]:
    output = subprocess.check_output(["git", "ls-files"], cwd=root, text=True)
    return [line.strip().replace("\\", "/") for line in output.splitlines() if line.strip()]


def scan(root: Path) -> dict[str, Any]:
    forbidden: list[str] = []
    secret_hits: list[str] = []
    for rel in git_files(root):
        lower = rel.lower()
        if Path(lower).suffix in PUBLIC_FORBIDDEN_SUFFIXES:
            forbidden.append(rel)
        for part in PUBLIC_FORBIDDEN_PARTS:
            if part in lower:
                forbidden.append(rel)
        path = root / rel
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".zip"}:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                text = ""
            if SECRET_RE.search(text):
                secret_hits.append(rel)
    forbidden = sorted(set(forbidden))
    secret_hits = sorted(set(secret_hits))
    return {"schema_version": "public_package_audit_v1.v1", "status": "success" if not forbidden and not secret_hits else "failed", "forbidden_artifacts": forbidden, "secret_hits": secret_hits}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="")
    args = parser.parse_args()
    payload = scan(Path(args.root).resolve() if args.root else vault_path())
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
