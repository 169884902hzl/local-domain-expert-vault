"""Scan the public package for tracked runtime artifacts and high-confidence secrets."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass


ARTIFACT_RE = re.compile(
    r"(?i)(\.pdf$|\.sqlite$|\.sqlite3$|\.db$|\.log$|\.pyc$|__pycache__/|\.env$|"
    r"settings\.local\.json$|workspace\.json$)"
)

SENSITIVE_PATTERNS = [
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
    "hazel" + "666",
    "169884902hzl" + "@" + r"gmail\.com",
]
SECRET_RE = re.compile("|".join(SENSITIVE_PATTERNS))
BINARY_SUFFIXES = {
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".webp",
    ".zip",
}


@dataclass(frozen=True)
class ScanResult:
    artifacts: list[str]
    secret_hits: list[str]

    @property
    def ok(self) -> bool:
        return not self.artifacts and not self.secret_hits


def git_files(root: pathlib.Path) -> list[str]:
    output = subprocess.check_output(["git", "ls-files"], cwd=root, text=True)
    return output.splitlines()


def read_text(path: pathlib.Path) -> str | None:
    if path.suffix.lower() in BINARY_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except OSError:
        return None


def scan_paths(root: pathlib.Path, files: list[str]) -> ScanResult:
    artifacts = [path for path in files if ARTIFACT_RE.search(path)]
    secret_hits: list[str] = []
    for path in files:
        text = read_text(root / path)
        if text is None:
            continue
        if SECRET_RE.search(text):
            secret_hits.append(path)
    return ScanResult(artifacts=artifacts, secret_hits=secret_hits)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable scan output.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.root).resolve()
    files = git_files(root)
    result = scan_paths(root, files)

    if args.json:
        print(json.dumps({"artifacts": result.artifacts, "secret_hits": result.secret_hits}, indent=2))
    elif result.ok:
        print(f"public package scan ok: files={len(files)}")
    else:
        if result.artifacts:
            print("Tracked private/runtime artifacts:")
            print("\n".join(result.artifacts))
        if result.secret_hits:
            print("Potential secret/private path hits:")
            print("\n".join(result.secret_hits))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
