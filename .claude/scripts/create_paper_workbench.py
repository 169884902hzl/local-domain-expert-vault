"""Create sidecar notes used by the Obsidian Paper Reading Workbench plugin."""
from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write, vault_path


WORKBENCH_DIR = vault_path("projects", "reading-workbench")
TRANSLATION_DIR = vault_path("projects", "translations")
ZOTERO_LOCAL_API = "http://localhost:23119/api/users/0"


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


def frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    parsed = extract_frontmatter(text)
    return parse_frontmatter_map(parsed[0]) if parsed else {}


def rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def today_iso() -> str:
    from datetime import date

    return date.today().isoformat()


def zotero_uri(zotero_key: str) -> str:
    return f"zotero://select/library/items/{zotero_key}"


def _read_zotero_json(path: str, *, timeout: int = 8) -> Any:
    url = f"{ZOTERO_LOCAL_API}{path}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _attachment_path(data: dict[str, Any]) -> str:
    for key in ("path", "localPath", "filename"):
        value = str(data.get(key, "") or "").strip()
        if value:
            return value
    return ""


def resolve_zotero_source(zotero_key: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "unavailable",
        "item_uri": zotero_uri(zotero_key),
        "item_url": "",
        "title": "",
        "item_type": "",
        "attachments": [],
        "best_attachment_uri": "",
        "best_attachment_path": "",
        "error": "",
    }
    try:
        item = _read_zotero_json(f"/items/{urllib.parse.quote(zotero_key)}?format=json")
        children = _read_zotero_json(f"/items/{urllib.parse.quote(zotero_key)}/children?format=json")
    except (OSError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        result["error"] = f"zotero_local_api_unavailable:{type(exc).__name__}:{exc}"
        return result
    data = item.get("data", {}) if isinstance(item, dict) else {}
    result.update(
        {
            "status": "ok",
            "title": str(data.get("title", "") or ""),
            "item_type": str(data.get("itemType", "") or ""),
            "item_url": str(data.get("url", "") or ""),
        }
    )
    attachments: list[dict[str, str]] = []
    if isinstance(children, list):
        for child in children:
            child_data = child.get("data", {}) if isinstance(child, dict) else {}
            if child_data.get("itemType") != "attachment":
                continue
            key = str(child.get("key") or child_data.get("key") or "")
            path_value = _attachment_path(child_data)
            attachment = {
                "key": key,
                "title": str(child_data.get("title", "") or child_data.get("filename", "") or "attachment"),
                "content_type": str(child_data.get("contentType", "") or ""),
                "link_mode": str(child_data.get("linkMode", "") or ""),
                "path": path_value,
                "url": str(child_data.get("url", "") or ""),
                "uri": zotero_uri(key) if key else "",
            }
            attachments.append(attachment)
    result["attachments"] = attachments
    pdfs = [
        item
        for item in attachments
        if "pdf" in item.get("content_type", "").lower()
        or item.get("path", "").lower().endswith(".pdf")
        or "/pdf/" in item.get("url", "").lower()
    ]
    best = (pdfs or attachments or [{}])[0]
    result["best_attachment_uri"] = best.get("uri", "")
    result["best_attachment_path"] = best.get("path", "")
    return result


def find_arxiv_metadata(zotero_key: str) -> dict[str, str]:
    result = {"arxiv_id": "", "url": "", "pdf_url": "", "source": ""}
    for path in sorted(vault_path("projects", "arxiv-daily").glob("*-candidates.jsonl"), reverse=True):
        text = path.read_text(encoding="utf-8", errors="replace")
        if zotero_key not in text:
            continue
        for line in text.splitlines():
            if zotero_key not in line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            paper = row.get("paper", {})
            result.update(
                {
                    "arxiv_id": str(paper.get("arxiv_id", "")),
                    "url": str(paper.get("url", "")),
                    "pdf_url": str(paper.get("pdf_url", "")),
                    "source": rel(path),
                }
            )
            return result
    for path in sorted(vault_path("projects", "arxiv-daily").glob("*-run.md"), reverse=True):
        text = path.read_text(encoding="utf-8", errors="replace")
        line = next((item for item in text.splitlines() if f"zotero_key={zotero_key}" in item), "")
        if not line:
            continue
        match = re.search(r"arxiv=([0-9.]+)", line)
        if match:
            arxiv_id = match.group(1)
            result.update(
                {
                    "arxiv_id": arxiv_id,
                    "url": f"https://arxiv.org/abs/{arxiv_id}",
                    "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
                    "source": rel(path),
                }
            )
            return result
    return result


def render_zotero_attachment_lines(zotero: dict[str, Any]) -> list[str]:
    attachments = zotero.get("attachments", [])
    if not attachments:
        return ["- Attachments: not resolved from Zotero local API"]
    lines = []
    for item in attachments[:8]:
        label = item.get("title") or item.get("key") or "attachment"
        detail = item.get("content_type") or item.get("link_mode") or "-"
        uri = item.get("uri") or ""
        path_value = item.get("path") or ""
        url = item.get("url") or ""
        storage = "file-backed" if path_value else ("pdf-url" if url else item.get("link_mode") or "-")
        suffix = f"{detail}; storage: {storage}"
        lines.append(f"- Attachment: [{label}]({uri}) — {suffix}" if uri else f"- Attachment: {label} — {suffix}")
        if path_value:
            lines.append(f"  - path: `{path_value}`")
        if url:
            lines.append(f"  - url: {url}")
    return lines


def find_gemini_matches(topic: Path, title: str, zotero_key: str) -> list[dict[str, Any]]:
    strong_needles = {zotero_key.lower(), topic.stem.lower()}
    title_needles = set()
    for token in re.sub(r"[^a-zA-Z0-9]+", " ", title.lower()).split():
        if len(token) >= 7:
            title_needles.add(token)
    matches: list[dict[str, Any]] = []
    for path in sorted(vault_path("projects", "research-agenda", "divergent").glob("*-gemini-raw-candidates.json"), reverse=True)[:20]:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for candidate in data.get("raw_gemini_candidates", []):
            if not isinstance(candidate, dict):
                continue
            text = json.dumps(candidate, ensure_ascii=False).lower()
            direct_score = sum(5 for needle in strong_needles if needle and needle in text)
            token_score = sum(1 for needle in title_needles if needle and needle in text)
            score = direct_score + token_score
            if direct_score or token_score >= 3:
                item = dict(candidate)
                item["archive"] = rel(path)
                item["match_score"] = score
                matches.append(item)
    return sorted(matches, key=lambda item: -int(item.get("match_score", 0)))[:6]


def render_zotero_source_entry(zotero_key: str, topic: Path, title: str, arxiv: dict[str, str], zotero: dict[str, Any]) -> str:
    zotero_status = zotero.get("status", "unavailable")
    zotero_error = zotero.get("error", "")
    attachment_lines = "\n".join(render_zotero_attachment_lines(zotero))
    return (
        "---\n"
        f'title: "Zotero Source - {title.replace(chr(34), chr(39))}"\n'
        "tags: [paper-workbench, zotero-source]\n"
        f'created: "{today_iso()}"\n'
        f'updated: "{today_iso()}"\n'
        'type: "permanent"\n'
        'status: "stub"\n'
        'summary: "Zotero-first source entry for paper reading workbench."\n'
        f'zotero_key: "{zotero_key}"\n'
        f'zotero_source_status: "{zotero_status}"\n'
        "---\n"
        f"# Zotero Source - {title}\n\n"
        f"- Zotero item: [{zotero_key}]({zotero_uri(zotero_key)})\n"
        f"- Zotero local status: `{zotero_status}`\n"
        + (f"- Zotero warning: `{zotero_error}`\n" if zotero_error else "")
        + f"{attachment_lines}\n"
        f"- arXiv: {arxiv.get('url') or 'not found in local daily records'}\n"
        f"- PDF URL: {arxiv.get('pdf_url') or 'not found in local daily records'}\n"
        f"- Metadata source: `{arxiv.get('source') or '-'}`\n"
        f"- Topic note: [[{rel(topic)}]]\n"
        f"- Deep reading: [[raw/readings/{zotero_key}-analysis.md]]\n\n"
        f"- Gemini ideas: [[projects/reading-workbench/{zotero_key}-gemini-ideas.md]]\n"
        f"- Translation cache: [[projects/translations/{zotero_key}-zh.md]]\n"
        f"- Knowledge diagram: [[projects/knowledge-diagrams/papers/{topic.stem}.md]]\n\n"
        "> Boundary: Zotero remains the source of truth for the original PDF. This note stores source links and local reading context; it does not copy PDFs into the vault.\n"
    )


def render_ideas(zotero_key: str, topic: Path, title: str, matches: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        f'title: "Gemini Ideas - {title.replace(chr(34), chr(39))}"',
        "tags: [paper-workbench, gemini, idea]",
        f'created: "{today_iso()}"',
        f'updated: "{today_iso()}"',
        'type: "permanent"',
        'status: "stub"',
        'summary: "Filtered Gemini greenhouse candidates related to this paper."',
        f'zotero_key: "{zotero_key}"',
        "---",
        f"# Gemini Ideas - {title}",
        "",
        f"- Topic note: [[{rel(topic)}]]",
        f"- Deep reading: [[raw/readings/{zotero_key}-analysis.md]]",
        "",
        "## Matched Candidates",
        "",
    ]
    if not matches:
        lines.append("- No direct candidate match found in recent greenhouse archives.")
    for item in matches[:8]:
        lines.extend(
            [
                f"### {item.get('title', 'Untitled candidate')}",
                f"- archive: `{item.get('archive', '-')}`",
                f"- tier: {item.get('quality_tier', '-')}; label: {item.get('greenhouse_label', '-')}; group: {item.get('candidate_group', '-')}",
                f"- problem: {item.get('problem', '-')}",
                f"- mechanism: {item.get('mechanism', '-')}",
                f"- strongest_baseline: {item.get('strongest_baseline', '-')}",
                f"- killer_experiment: {item.get('killer_experiment', '-')}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def render_translation_placeholder(zotero_key: str, topic: Path, title: str) -> str:
    return (
        "---\n"
        f'title: "AI Translation - {title.replace(chr(34), chr(39))}"\n'
        "tags: [paper-workbench, translation]\n"
        f'created: "{today_iso()}"\n'
        f'updated: "{today_iso()}"\n'
        'type: "permanent"\n'
        'status: "stub"\n'
        'summary: "AI translation cache for paper reading workbench."\n'
        f'zotero_key: "{zotero_key}"\n'
        'translation_status: "not_generated"\n'
        'translation_source_scope: "pending"\n'
        "translation_concurrency_limit: 5\n"
        "---\n"
        f"# AI Translation - {title}\n\n"
        "Translation cache has not been generated yet.\n\n"
        "Use Obsidian command: **Paper Reading Workbench: Generate translation cache for current paper**.\n\n"
        "Concurrency policy: translation jobs are capped at 5 parallel Gemini calls.\n"
    )


def create_for_key(zotero_key: str, *, dry_run: bool) -> dict[str, Any]:
    topic = find_topic_by_key(zotero_key)
    if topic is None:
        return {"zotero_key": zotero_key, "status": "failed", "error": "topic_note_not_found"}
    fields = frontmatter(topic)
    title = fields.get("title", topic.stem).strip().strip('"')
    arxiv = find_arxiv_metadata(zotero_key)
    zotero = resolve_zotero_source(zotero_key)
    matches = find_gemini_matches(topic, title, zotero_key)
    source_entry = WORKBENCH_DIR / f"{zotero_key}-zotero-source.md"
    ideas = WORKBENCH_DIR / f"{zotero_key}-gemini-ideas.md"
    translation = TRANSLATION_DIR / f"{zotero_key}-zh.md"
    safe_write(source_entry, render_zotero_source_entry(zotero_key, topic, title, arxiv, zotero), dry_run=dry_run, backup=True)
    safe_write(ideas, render_ideas(zotero_key, topic, title, matches), dry_run=dry_run, backup=True)
    if not translation.exists():
        safe_write(translation, render_translation_placeholder(zotero_key, topic, title), dry_run=dry_run, backup=True)
    return {
        "zotero_key": zotero_key,
        "status": "ok",
        "topic": rel(topic),
        "source_entry": rel(source_entry),
        "ideas": rel(ideas),
        "translation": rel(translation),
        "gemini_matches": len(matches),
        "zotero_source_status": zotero.get("status", "unavailable"),
        "pdf_url": arxiv.get("pdf_url", ""),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zotero-keys", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    results = [create_for_key(key, dry_run=args.dry_run) for key in split_keys(args.zotero_keys)]
    for result in results:
        safe_print(json.dumps(result, ensure_ascii=False))
    return 1 if any(item.get("status") == "failed" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
