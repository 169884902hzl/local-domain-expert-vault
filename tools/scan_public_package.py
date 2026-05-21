"""Scan the public package for tracked runtime artifacts and high-confidence secrets."""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tarfile
import zipfile
from dataclasses import dataclass


ARTIFACT_RE = re.compile(
    r"(?i)(\.pdf$|\.sqlite$|\.sqlite3$|\.db$|\.log$|\.pyc$|\.bak$|__pycache__/|\.env$|"
    r"settings\.local\.json$|workspace\.json$|attachments/|archive/|(^|/)logs/|(^|/)cache/|(^|/)\.cache/|backup|secret|"
    r"projects/research-agenda/runs/|projects/research-agenda/cache/|"
    r"projects/research-agenda/idea_bank/seed/|"
    r"projects/research-agenda/governance/active-seeds/|"
    r"projects/research-agenda/governance/ledger/|"
    r"active-seed-record\.json$|governance-ledger\.jsonl$)"
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


def tree_files(root: pathlib.Path) -> list[str]:
    ignored = {".git", ".pytest_cache", "__pycache__", ".mypy_cache"}
    files: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored for part in path.relative_to(root).parts):
            continue
        files.append(path.relative_to(root).as_posix())
    return files


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
    files = [path for path in files if (root / path).exists() and pathlib.Path(path).name != ".gitkeep"]
    artifacts = [path for path in files if ARTIFACT_RE.search(path)]
    secret_hits: list[str] = []
    for path in files:
        text = read_text(root / path)
        if text is None:
            continue
        if SECRET_RE.search(text):
            secret_hits.append(path)
    return ScanResult(artifacts=artifacts, secret_hits=secret_hits)


def _archive_text(name: str, data: bytes) -> str | None:
    if pathlib.Path(name).suffix.lower() in BINARY_SUFFIXES:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan_archive(path: pathlib.Path) -> ScanResult:
    names: list[str] = []
    texts: dict[str, str] = {}
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                name = info.filename.replace("\\", "/")
                if pathlib.Path(name).name == ".gitkeep":
                    continue
                names.append(name)
                text = _archive_text(name, archive.read(info))
                if text is not None:
                    texts[name] = text
    elif tarfile.is_tarfile(path):
        with tarfile.open(path) as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                name = member.name.replace("\\", "/")
                if pathlib.Path(name).name == ".gitkeep":
                    continue
                names.append(name)
                handle = archive.extractfile(member)
                if handle is None:
                    continue
                text = _archive_text(name, handle.read())
                if text is not None:
                    texts[name] = text
    else:
        raise ValueError(f"unsupported_archive:{path}")
    artifacts = [name for name in names if ARTIFACT_RE.search(name)]
    secret_hits = [name for name, text in texts.items() if SECRET_RE.search(text)]
    return ScanResult(artifacts=artifacts, secret_hits=secret_hits)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root. Defaults to current directory.")
    parser.add_argument("--archive", default="", help="Scan a built zip/tar package instead of git-tracked files.")
    parser.add_argument("--scan-tree", action="store_true", help="Scan the working tree package contents instead of only git-tracked files.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable scan output.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.root).resolve()
    if args.archive:
        result = scan_archive(pathlib.Path(args.archive).resolve())
        files = result.artifacts + result.secret_hits
    else:
        files = tree_files(root) if args.scan_tree else git_files(root)
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
