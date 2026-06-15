"""Generate Chinese translation cache notes for the Obsidian paper workbench.

The script is intentionally sidecar-only:
- reads wiki topic notes and raw/readings analysis files;
- writes projects/translations/<ZOTERO_KEY>-zh.md;
- never modifies raw/.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from gemini_cli_adapter import DEFAULT_GEMINI_MODEL, DEFAULT_GEMINI_TIMEOUT_SEC, run_gemini_cli
from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write, vault_path
from llm_structured import StructuredOutputError, extract_json


MAX_TRANSLATION_CONCURRENCY = 5
DEFAULT_MAX_SOURCE_CHARS = 200000
TRANSLATION_DIR = vault_path("projects", "translations")
ZOTERO_LOCAL_API = "http://127.0.0.1:23119/api/users/0"


@dataclass(frozen=True)
class PaperSource:
    zotero_key: str
    title: str
    topic_path: Path
    raw_reading_path: Path | None
    source_scope: str
    zotero_fulltext_status: str
    text: str


def clamp_concurrency(value: int) -> int:
    return max(1, min(MAX_TRANSLATION_CONCURRENCY, int(value)))


def split_keys(value: str) -> list[str]:
    return [item.strip().upper() for item in value.split(",") if item.strip()]


def find_topic_by_key(zotero_key: str) -> Path | None:
    pattern = re.compile(rf'^zotero_key:\s*"?{re.escape(zotero_key)}"?\s*$', re.MULTILINE)
    for path in sorted(vault_path("wiki", "topics").glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if pattern.search(text):
            return path
    return None


def read_frontmatter_title(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return path.stem
    parsed = extract_frontmatter(text)
    if not parsed:
        return path.stem
    fields = parse_frontmatter_map(parsed[0])
    return fields.get("title", path.stem).strip().strip('"') or path.stem


def fetch_zotero_fulltext(zotero_key: str, *, timeout: int = 20) -> tuple[str, str]:
    url = f"{ZOTERO_LOCAL_API}/items/{urllib.parse.quote(zotero_key)}/fulltext"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = extract_json(resp.read().decode("utf-8"), want=lambda payload: isinstance(payload, dict))
    except (OSError, urllib.error.URLError, TimeoutError, StructuredOutputError) as exc:
        return "", f"unavailable:{type(exc).__name__}:{exc}"
    content = str(data.get("content", "") or "").strip() if isinstance(data, dict) else ""
    if not content:
        return "", "empty"
    return content, "ok"


def compact_translation_source(text: str, *, max_chars: int) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    skip_sections = {"## 本地引用关系", "## 相关概念", "## 相关研究者"}
    skip = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            skip = stripped in skip_sections
        if skip:
            continue
        lines.append(line)
    compact = "\n".join(lines).strip()
    if len(compact) <= max_chars:
        return compact
    head = compact[: max_chars // 2]
    tail = compact[-max_chars // 2 :]
    return head + "\n\n[... source truncated for translation cache ...]\n\n" + tail


def load_source(zotero_key: str, *, max_chars: int) -> PaperSource:
    topic_path = find_topic_by_key(zotero_key)
    if topic_path is None:
        raise FileNotFoundError(f"topic_note_not_found:{zotero_key}")
    title = read_frontmatter_title(topic_path)
    raw_path = vault_path("raw", "readings", f"{zotero_key}-analysis.md")
    topic_text = topic_path.read_text(encoding="utf-8")
    raw_text = raw_path.read_text(encoding="utf-8") if raw_path.exists() else ""
    zotero_text, zotero_status = fetch_zotero_fulltext(zotero_key)
    if zotero_text:
        source_scope = "zotero_fulltext_plus_claudian_context" if raw_text else "zotero_fulltext"
        context = f"\n\n# Claudian Deep Reading Context\n\n{raw_text}" if raw_text else ""
        source_text = f"# Zotero Fulltext\n\n{zotero_text}{context}\n\n# Topic Note Metadata\n\n{topic_text[:3000]}"
    elif raw_text:
        source_scope = "raw_reading_analysis_plus_topic_note"
        source_text = f"# Topic Note\n\n{topic_text}\n\n# Claudian Deep Reading Analysis\n\n{raw_text}"
    else:
        source_scope = "topic_note_only"
        source_text = topic_text
    return PaperSource(
        zotero_key=zotero_key,
        title=title,
        topic_path=topic_path,
        raw_reading_path=raw_path if raw_path.exists() else None,
        source_scope=source_scope,
        zotero_fulltext_status=zotero_status,
        text=compact_translation_source(source_text, max_chars=max_chars),
    )


def render_prompt(source: PaperSource) -> str:
    packet: dict[str, Any] = {
        "task": "Translate the provided local paper-reading source into polished Chinese for side-by-side Obsidian reading.",
        "boundary": [
            "This is a reading cache, not a new formal claim.",
            "Preserve equations, method names, dataset names, baselines, metrics, and citation-like identifiers.",
            "Do not invent content that is not in the source.",
            "State the translation source scope clearly: Zotero fulltext, Claudian reading analysis, or topic note fallback.",
        ],
        "output_format": [
            "Return markdown only.",
            "Start with a short Translation Scope block.",
            "Then translate by sections with clear headings.",
            "Keep technical terms bilingual when useful, e.g. reward model（奖励模型）.",
        ],
        "paper": {
            "zotero_key": source.zotero_key,
            "title": source.title,
            "source_scope": source.source_scope,
            "zotero_fulltext_status": source.zotero_fulltext_status,
            "topic_note": str(source.topic_path.relative_to(vault_path())).replace("\\", "/"),
            "raw_reading": str(source.raw_reading_path.relative_to(vault_path())).replace("\\", "/") if source.raw_reading_path else "",
        },
        "source_text": source.text,
    }
    return json.dumps(packet, ensure_ascii=False, indent=2)


def render_fallback_translation(source: PaperSource, reason: str) -> str:
    return (
        f"## Translation unavailable\n\n"
        f"- reason: `{reason}`\n"
        f"- source_scope: `{source.source_scope}`\n\n"
        f"- zotero_fulltext_status: `{source.zotero_fulltext_status}`\n\n"
        "The source remains available for manual reading:\n\n"
        f"- Topic note: `wiki/topics/{source.topic_path.name}`\n"
        + (f"- Claudian reading: `raw/readings/{source.raw_reading_path.name}`\n" if source.raw_reading_path else "")
    )


def render_translation_note(source: PaperSource, body: str, *, status: str, model: str, provider_status: str) -> str:
    raw_rel = str(source.raw_reading_path.relative_to(vault_path())).replace("\\", "/") if source.raw_reading_path else ""
    topic_rel = str(source.topic_path.relative_to(vault_path())).replace("\\", "/")
    return (
        "---\n"
        f'title: "AI Translation - {source.title.replace(chr(34), chr(39))}"\n'
        "tags: [paper-workbench, translation]\n"
        f'created: "{today_iso()}"\n'
        f'updated: "{today_iso()}"\n'
        'type: "permanent"\n'
        f'status: "{status}"\n'
        f'summary: "AI translation cache for {source.title.replace(chr(34), chr(39))}."\n'
        f'zotero_key: "{source.zotero_key}"\n'
        f'translation_status: "{status}"\n'
        f'translation_source_scope: "{source.source_scope}"\n'
        f'zotero_fulltext_status: "{source.zotero_fulltext_status.replace(chr(34), chr(39))}"\n'
        f'translation_model: "{model}"\n'
        f'translation_provider_status: "{provider_status.replace(chr(34), chr(39))}"\n'
        f'translation_concurrency_limit: {MAX_TRANSLATION_CONCURRENCY}\n'
        "---\n"
        f"# AI Translation - {source.title}\n\n"
        "## Source Links\n\n"
        f"- Topic note: [[{topic_rel}]]\n"
        + (f"- Claudian reading: [[{raw_rel}]]\n" if raw_rel else "- Claudian reading: not found\n")
        + f"- Zotero fulltext status: `{source.zotero_fulltext_status}`\n"
        + "\n"
        + body.strip()
        + "\n"
    )


def today_iso() -> str:
    from datetime import date

    return date.today().isoformat()


def translate_one(zotero_key: str, args: argparse.Namespace) -> dict[str, str]:
    try:
        source = load_source(zotero_key, max_chars=args.max_source_chars)
    except Exception as exc:
        return {"zotero_key": zotero_key, "status": "failed", "error": f"load_source:{type(exc).__name__}:{exc}"}
    if args.dry_run:
        return {
            "zotero_key": zotero_key,
            "status": "dry_run",
            "source_scope": source.source_scope,
            "zotero_fulltext_status": source.zotero_fulltext_status,
            "title": source.title,
            "target": str(TRANSLATION_DIR / f"{zotero_key}-zh.md"),
        }
    result = run_gemini_cli(render_prompt(source), timeout_sec=args.timeout, model=args.model)
    provider_status = "success" if not result.get("error") else str(result.get("error"))
    body = str(result.get("clean_output") or "").strip()
    status = "done"
    if result.get("error") or not body:
        status = "stub"
        body = render_fallback_translation(source, provider_status or "empty_output")
    target = TRANSLATION_DIR / f"{zotero_key}-zh.md"
    safe_write(target, render_translation_note(source, body, status=status, model=args.model, provider_status=provider_status), dry_run=False, backup=True)
    return {"zotero_key": zotero_key, "status": status, "target": str(target.relative_to(vault_path())), "provider_status": provider_status}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zotero-keys", required=True, help="Comma-separated Zotero keys.")
    parser.add_argument("--max-concurrency", type=int, default=MAX_TRANSLATION_CONCURRENCY)
    parser.add_argument("--timeout", type=int, default=DEFAULT_GEMINI_TIMEOUT_SEC)
    parser.add_argument("--model", default=DEFAULT_GEMINI_MODEL)
    parser.add_argument("--max-source-chars", type=int, default=DEFAULT_MAX_SOURCE_CHARS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    keys = split_keys(args.zotero_keys)
    concurrency = clamp_concurrency(args.max_concurrency)
    safe_print(f"TRANSLATION_QUEUE keys={len(keys)} max_concurrency={concurrency} hard_cap={MAX_TRANSLATION_CONCURRENCY} dry_run={args.dry_run}")
    if not keys:
        return 0
    TRANSLATION_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_map = {executor.submit(translate_one, key, args): key for key in keys}
        for future in concurrent.futures.as_completed(future_map):
            key = future_map[future]
            try:
                result = future.result()
            except Exception as exc:
                result = {"zotero_key": key, "status": "failed", "error": f"{type(exc).__name__}:{exc}"}
            results.append(result)
            safe_print(json.dumps(result, ensure_ascii=False))
    failures = [item for item in results if item.get("status") == "failed"]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
