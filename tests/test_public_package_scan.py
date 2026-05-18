from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_PATH = ROOT / "tools" / "scan_public_package.py"


def load_scanner():
    spec = importlib.util.spec_from_file_location("scan_public_package", SCAN_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_scan_public_package_all_tracked_files_are_clean() -> None:
    scanner = load_scanner()
    result = scanner.scan_paths(ROOT, scanner.git_files(ROOT))
    assert result.artifacts == []
    assert result.secret_hits == []


def test_scanner_does_not_skip_wiki_topics(tmp_path: Path) -> None:
    scanner = load_scanner()
    topic = tmp_path / "wiki" / "topics" / "example.md"
    topic.parent.mkdir(parents=True)
    env_name = "OPENAI" + "_API" + "_KEY"
    fake_secret = env_name + "=" + "sk-" + ("test" * 7)
    topic.write_text(fake_secret, encoding="utf-8")
    result = scanner.scan_paths(tmp_path, ["wiki/topics/example.md"])
    assert "wiki/topics/example.md" in result.secret_hits
