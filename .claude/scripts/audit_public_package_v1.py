"""Fail if the public package contains v1-forbidden runtime or private artifacts."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import tarfile
from pathlib import Path
from typing import Any
import zipfile

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


def archive_files(path: Path) -> tuple[list[str], dict[str, str]]:
    names: list[str] = []
    texts: dict[str, str] = {}
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for info in archive.infolist():
                if info.is_dir():
                    continue
                name = info.filename.replace("\\", "/")
                names.append(name)
                if Path(name).suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".zip", ".pdf"}:
                    continue
                try:
                    texts[name] = archive.read(info).decode("utf-8")
                except UnicodeDecodeError:
                    pass
    elif tarfile.is_tarfile(path):
        with tarfile.open(path) as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                name = member.name.replace("\\", "/")
                names.append(name)
                if Path(name).suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".zip", ".pdf"}:
                    continue
                handle = archive.extractfile(member)
                if handle is None:
                    continue
                try:
                    texts[name] = handle.read().decode("utf-8")
                except UnicodeDecodeError:
                    pass
    else:
        raise ValueError(f"unsupported_archive:{path}")
    return names, texts


def scan(root: Path, *, files: list[str] | None = None, text_by_path: dict[str, str] | None = None) -> dict[str, Any]:
    forbidden: list[str] = []
    secret_hits: list[str] = []
    paths = files if files is not None else git_files(root)
    text_by_path = text_by_path or {}
    for rel in paths:
        if files is None and not (root / rel).exists():
            continue
        if Path(rel).name == ".gitkeep":
            continue
        lower = rel.lower()
        if Path(lower).suffix in PUBLIC_FORBIDDEN_SUFFIXES:
            forbidden.append(rel)
        for part in PUBLIC_FORBIDDEN_PARTS:
            if part in lower:
                forbidden.append(rel)
        path = root / rel
        if rel in text_by_path:
            text = text_by_path[rel]
        elif path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".zip"}:
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                text = ""
        else:
            text = ""
        if text and SECRET_RE.search(text):
            secret_hits.append(rel)
    forbidden = sorted(set(forbidden))
    secret_hits = sorted(set(secret_hits))
    return {"schema_version": "public_package_audit_v1.v1", "status": "success" if not forbidden and not secret_hits else "failed", "forbidden_artifacts": forbidden, "secret_hits": secret_hits}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="")
    parser.add_argument("--archive", default="")
    args = parser.parse_args()
    if args.archive:
        names, texts = archive_files(Path(args.archive).resolve())
        payload = scan(Path("."), files=names, text_by_path=texts)
    else:
        payload = scan(Path(args.root).resolve() if args.root else vault_path())
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
