from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=60,
    )


def test_audit_kb_cli_passes() -> None:
    result = run_script(".claude/scripts/audit_kb.py")
    assert result.returncode == 0, result.stdout
    assert "topic_issues=0" in result.stdout
    assert "concept_issues=0" in result.stdout
    assert "entity_issues=0" in result.stdout


def test_arxiv_status_is_read_only_when_mirror_missing() -> None:
    metadata_dir = ROOT / "projects" / "arxiv-daily" / "metadata"
    if metadata_dir.exists():
        pytest.skip("local arXiv metadata mirror exists; fresh-clone read-only check is covered by CI")
    result = run_script(".claude/scripts/arxiv_metadata_sync.py", "--status")
    assert result.returncode == 0, result.stdout
    assert '"missing": true' in result.stdout
    assert not metadata_dir.exists()


def test_mirror_first_dry_run_does_not_use_search_api_on_fresh_clone() -> None:
    metadata_dir = ROOT / "projects" / "arxiv-daily" / "metadata"
    if metadata_dir.exists():
        pytest.skip("local arXiv metadata mirror exists; fresh-clone dry-run check is covered by CI")
    result = run_script(
        ".claude/scripts/daily_arxiv_pipeline.py",
        "--dry-run",
        "--source",
        "mirror-first",
        "--max-candidates",
        "5",
        "--days-back",
        "14",
        "--idea-mode",
        "template",
        "--skip-read",
    )
    assert result.returncode == 0, result.stdout
    assert "source=mirror_missing" in result.stdout
    assert "search_api" not in result.stdout


def test_public_package_scan_on_built_archive(tmp_path: Path) -> None:
    archive = tmp_path / "package.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("README.md", "# public package\n")
        zf.writestr(".claude/scripts/example.py", "print('ok')\n")
    result = run_script("tools/scan_public_package.py", "--archive", str(archive))
    assert result.returncode == 0, result.stdout


def test_public_package_scan_rejects_runtime_projects_artifact_in_archive(tmp_path: Path) -> None:
    archive = tmp_path / "package.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr("projects/research-agenda/runs/2099-01-01/artifacts/run.json", "{}\n")
    result = run_script("tools/scan_public_package.py", "--archive", str(archive))
    assert result.returncode != 0
    assert "projects/research-agenda/runs" in result.stdout
