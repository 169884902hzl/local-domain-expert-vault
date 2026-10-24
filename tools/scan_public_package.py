"""Scan the public package for tracked runtime artifacts and high-confidence secrets."""
from __future__ import annotations

import argparse
import hashlib
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
]
SECRET_RE = re.compile("|".join(SENSITIVE_PATTERNS))
RESTRICTED_TOKEN_HASHES = {
    "3cf4e2fa6394ec4554f3df4a31d662180c0a49a733b7704eadb304da0b227a8f",
    "f3b0a0746e437a58dcfede33c1e6694873e3c80d982de8a095b17a9c9e9547e0",
    "86ec6666b9549ce6f1f6e0cd7ba6a7c12ed305ef16b6a1506335773b10773392",
    "f56c9370aadeee50ecff507251d1d46d0bfe09e35b394cdcbd297aa668839d90",
    "8fb01a3cbf4e1f1003d5a93e8be345ab7253112a20b1913810cb1eee2eadf0a3",
    "1aab57bd8a77a470c0e770c01a17ea2d2af6ce037cc4786dee47fff0b2af057e",
    "c2297af8db2e824420ac2014a3c1cdcdf2f06ad9de057ee22263ac731dbd80ee",
    "f1d98fcdcdbf336d8f5dde086c1e1b4db464e8e51a8fcc11315010d227f43865",
    "39fafdb95a4f7466bb2091da1e8d5384306bd15043999bc768a2b3d5fa779409",
    "1c577c2ca302eeb849eb3b0457196f3352a92e7a0d1376c30bbe35a5fd988294",
    "199066f096905e51a3de188f8c7cce31dca65688d371308fade789ecfb0b6676",
}
TOKEN_SCAN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.@-]*")


def _has_secret_or_restricted_token(text: str) -> bool:
    if SECRET_RE.search(text):
        return True
    for token in TOKEN_SCAN_RE.findall(text.lower()):
        if hashlib.sha256(token.encode("utf-8")).hexdigest() in RESTRICTED_TOKEN_HASHES:
            return True
    return False
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
        if _has_secret_or_restricted_token(text):
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
    secret_hits = [name for name, text in texts.items() if _has_secret_or_restricted_token(text)]
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
