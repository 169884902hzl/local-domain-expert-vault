"""Daily arXiv embodied-AI scout pipeline."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from arxiv_ranker import (
    AUTO_IMPORT_DECISIONS,
    BELOW_REVIEW_DECISION,
    DEFAULT_QUERIES,
    FOCUS_REVIEW_DECISION,
    LEGACY_REJECT_DECISION,
    REVIEW_THRESHOLD,
    TOP1_THRESHOLD,
    ArxivPaper,
    RankedPaper,
    normalize_title,
    rank_papers,
)
from generate_gemini_idea_prompt import render_prompt as render_gemini_prompt
from arxiv_metadata_sync import query_mirror, mirror_status, connect as connect_mirror
from kb_common import extract_frontmatter, parse_frontmatter_map, safe_print, safe_write, today_iso, vault_path
from zotero_import import (
    DEFAULT_COLLECTION_KEY,
    ImportResult,
    find_existing_paper_in_items,
    import_ranked_paper,
    iter_local_items,
    preflight,
)


ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
AUTO_IMPORT_FILL_DECISION = "auto_import_fill"
NEW_IMPORT_STATUSES = {"created", "sync_pending"}
FOCUS_READY_STATUSES = NEW_IMPORT_STATUSES | {"backlog"}
INGEST_READY_STATUSES = {"created", "exists", "sync_pending", "backlog"}
LOW_PRIORITY_DECISIONS = {BELOW_REVIEW_DECISION, LEGACY_REJECT_DECISION}
DEFAULT_FETCH_TIMEOUT = 12
DEFAULT_FETCH_RETRIES = 0
DEFAULT_QUERY_DELAY = 3.2
MIN_MIRROR_CANDIDATES_FOR_DAILY = 20
PRIMARY_DAILY_IMPORT_CAP = 7
FOCUS_DAILY_IMPORT_FLOOR = 2
DOMAIN_DAILY_IMPORT_FLOOR = 1
COVERAGE_DOMAIN_LABELS = {"dlo", "tactile", "bimanual", "sim_to_real"}


def _entry_text(entry: ET.Element, name: str) -> str:
    node = entry.find(f"atom:{name}", ATOM)
    return "" if node is None or node.text is None else " ".join(node.text.split())


def _entry_arxiv_text(entry: ET.Element, name: str) -> str:
    node = entry.find(f"arxiv:{name}", ATOM)
    return "" if node is None or node.text is None else " ".join(node.text.split())


def _entry_categories(entry: ET.Element) -> list[str]:
    categories = []
    for node in entry.findall("atom:category", ATOM):
        term = node.attrib.get("term", "")
        if term:
            categories.append(term)
    return categories


def _entry_primary_category(entry: ET.Element) -> str:
    node = entry.find("arxiv:primary_category", ATOM)
    return "" if node is None else node.attrib.get("term", "")


def _entry_pdf_url(entry: ET.Element) -> str:
    for node in entry.findall("atom:link", ATOM):
        if node.attrib.get("title") == "pdf" or node.attrib.get("type") == "application/pdf":
            return node.attrib.get("href", "")
    return ""


def _arxiv_id_from_url(url: str) -> str:
    value = url.rstrip("/").split("/")[-1]
    return value.split("v")[0] if "v" in value else value


def _parse_arxiv_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def fetch_arxiv(
    query: str,
    *,
    max_results: int,
    retries: int = DEFAULT_FETCH_RETRIES,
    timeout: int = DEFAULT_FETCH_TIMEOUT,
) -> list[ArxivPaper]:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"{ARXIV_API}?{params}"
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                root = ET.fromstring(resp.read())
            break
        except Exception as exc:
            last_error = exc
            if attempt >= retries:
                raise
            time.sleep(2 * (attempt + 1))
    else:
        raise RuntimeError(f"arXiv fetch failed: {last_error}")
    papers = []
    for entry in root.findall("atom:entry", ATOM):
        url_value = _entry_text(entry, "id")
        authors = []
        for author in entry.findall("atom:author", ATOM):
            name = author.find("atom:name", ATOM)
            if name is not None and name.text:
                authors.append(" ".join(name.text.split()))
        papers.append(
            ArxivPaper(
                arxiv_id=_arxiv_id_from_url(url_value),
                title=_entry_text(entry, "title"),
                authors=authors,
                summary=_entry_text(entry, "summary"),
                published=_entry_text(entry, "published"),
                updated=_entry_text(entry, "updated"),
                url=url_value,
                pdf_url=_entry_pdf_url(entry),
                categories=_entry_categories(entry),
                primary_category=_entry_primary_category(entry),
                doi=_entry_arxiv_text(entry, "doi"),
                journal_ref=_entry_arxiv_text(entry, "journal_ref"),
                comment=_entry_arxiv_text(entry, "comment"),
                query_sources=[query],
            )
        )
    return papers


def collect_candidates(
    queries: list[str],
    *,
    max_candidates: int,
    days_back: int,
    errors: list[str] | None = None,
    fetch_timeout: int = DEFAULT_FETCH_TIMEOUT,
    fetch_retries: int = DEFAULT_FETCH_RETRIES,
    query_delay: float = DEFAULT_QUERY_DELAY,
) -> list[ArxivPaper]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    by_id: dict[str, ArxivPaper] = {}
    per_query = max(20, max_candidates)
    for index, query in enumerate(queries):
        if index > 0 and query_delay > 0:
            time.sleep(query_delay)
        try:
            fetched = fetch_arxiv(query, max_results=per_query, retries=fetch_retries, timeout=fetch_timeout)
        except Exception as exc:
            if errors is not None:
                errors.append(f"arxiv_fetch_failed:{query}:{exc}")
            continue
        for paper in fetched:
            updated = _parse_arxiv_date(paper.updated) or _parse_arxiv_date(paper.published)
            if updated is not None and updated < cutoff:
                continue
            existing = by_id.get(paper.arxiv_id)
            if existing:
                existing.query_sources = sorted(set(existing.query_sources + [query]))
            else:
                by_id[paper.arxiv_id] = paper
        if max_candidates <= 20 and len(by_id) >= max_candidates * 3:
            break
    return list(by_id.values())


def collect_candidates_from_source(
    queries: list[str],
    *,
    source: str,
    max_candidates: int,
    days_back: int,
    as_of: datetime | None,
    errors: list[str],
    fetch_timeout: int,
    fetch_retries: int,
    query_delay: float,
) -> tuple[list[ArxivPaper], dict[str, Any]]:
    mirror_info: dict[str, Any] = {}
    if source in {"mirror-first", "mirror-only"}:
        try:
            papers, mirror_info = query_mirror(queries=queries, days_back=days_back, max_candidates=max_candidates, as_of=as_of)
        except Exception as exc:
            papers, mirror_info = [], {"source": "mirror_failed", "records_total": 0, "last_success_at": "", "stale": True}
            errors.append(f"arxiv_mirror_failed:{exc}")
        if source == "mirror-only":
            mirror_info["search_api_fallback_used"] = False
            return papers, mirror_info
        if len(papers) >= MIN_MIRROR_CANDIDATES_FOR_DAILY:
            mirror_info["search_api_fallback_used"] = False
            return papers, mirror_info
        if papers:
            errors.append(f"arxiv_mirror_insufficient:candidates={len(papers)}:threshold={MIN_MIRROR_CANDIDATES_FOR_DAILY}")
    if source == "mirror-first":
        errors.append("arxiv_mirror_empty_search_api_fallback")
    papers = collect_candidates(
        queries,
        max_candidates=max_candidates,
        days_back=days_back,
        errors=errors,
        fetch_timeout=fetch_timeout,
        fetch_retries=fetch_retries,
        query_delay=query_delay,
    )
    if papers:
        return papers, {
            **mirror_info,
            "source": "search_api" if source == "search-api" else "search_api_fallback",
            "search_api_fallback_used": source == "mirror-first",
        }
    try:
        conn = connect_mirror()
        status = mirror_status(conn)
        conn.close()
    except Exception:
        status = {}
    return papers, {
        **mirror_info,
        "source": "search_api_empty",
        "search_api_fallback_used": source == "mirror-first",
        "records_total": status.get("records_total", 0),
        "last_success_at": status.get("last_success_at", ""),
        "stale": status.get("stale", True),
    }


def write_jsonl(path: Path, records: list[dict[str, Any]], *, dry_run: bool) -> None:
    content = "\n".join(json.dumps(record, ensure_ascii=False) for record in records)
    if content:
        content += "\n"
    safe_write(path, content, dry_run=dry_run, backup=True)


def load_cached_ranked(path: Path) -> list[RankedPaper]:
    if not path.exists():
        return []
    ranked: list[RankedPaper] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            ranked.append(RankedPaper.from_dict(json.loads(line)))
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    return ranked


def parse_backlog(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    pattern = re.compile(
        r"^- arxiv=(?P<arxiv>\S+)\s+zotero_key=(?P<key>\S*)\s+"
        r"import_status=(?P<import_status>\S+)\s+read_status=(?P<read_status>\S+)"
    )
    records: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        record = match.groupdict()
        if record.get("key"):
            records.append(record)
    return records


def parse_successful_read_keys(path: Path) -> list[str]:
    if not path.exists():
        return []
    pattern = re.compile(r"^- zotero_key=(?P<key>\S+)\s+ingest=\S+\s+read=(?P<read_status>\S+)")
    keys: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        if not match.group("read_status").startswith("success"):
            continue
        key = match.group("key")
        if key not in seen:
            seen.add(key)
            keys.append(key)
    return keys


def parse_successful_read_keys_with_backups(path: Path) -> list[str]:
    keys = parse_successful_read_keys(path)
    seen = set(keys)
    try:
        rel_pattern = path.relative_to(vault_path()).as_posix()
    except ValueError:
        return keys
    backup_roots = [vault_path(".claude", "backups"), vault_path(".claude", "scripts", "backups")]
    for backup_root in backup_roots:
        if not backup_root.exists():
            continue
        for backup_path in sorted(backup_root.glob(f"*/{rel_pattern}")):
            for key in parse_successful_read_keys(backup_path):
                if key not in seen:
                    seen.add(key)
                    keys.append(key)
    return keys


def _section_list_items(text: str, heading: str) -> list[str]:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n\n(?P<body>.*?)(?=^## |\Z)")
    match = pattern.search(text)
    if not match:
        return []
    items: list[str] = []
    for line in match.group("body").splitlines():
        line = line.strip()
        if line.startswith("- "):
            value = line[2:].strip()
            if value and value != "none":
                items.append(value)
    return items


def _replace_markdown_section(text: str, heading: str, body_lines: list[str]) -> str:
    replacement = f"## {heading}\n\n" + "\n".join(body_lines).rstrip() + "\n\n"
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n\n.*?(?=^## |\Z)")
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1).rstrip() + "\n"
    return text.rstrip() + "\n\n" + replacement


def reconcile_run_log_after_recovery(
    *,
    run_log_path: Path,
    recovery_log_path: Path,
    recovery_status: str,
    agenda_status: str,
) -> bool:
    if recovery_status != "success" or agenda_status not in {"success", "skipped_no_focus_keys"}:
        return False
    if not run_log_path.exists():
        return False
    text = run_log_path.read_text(encoding="utf-8", errors="replace")
    initial_errors = _section_list_items(text, "Errors")
    if not initial_errors:
        existing_initial_errors = re.search(r"(?m)^- initial_errors: (?P<errors>.+)$", text)
        if existing_initial_errors and existing_initial_errors.group("errors") != "none":
            initial_errors = [existing_initial_errors.group("errors")]
    try:
        recovery_rel = str(recovery_log_path.relative_to(vault_path())).replace("\\", "/")
    except ValueError:
        recovery_rel = str(recovery_log_path)

    text = re.sub(
        r'(?m)^summary: "Daily arXiv scout run status: .*?"$',
        'summary: "Daily arXiv scout run status: success after recovery."',
        text,
        count=1,
    )
    text = re.sub(r"(?m)^- status: .*$", "- status: success", text, count=1)
    text = re.sub(r"(?m)^- agenda_update_status: .*$", f"- agenda_update_status: {agenda_status}", text, count=1)
    text = re.sub(
        r"(?ms)(^## Agenda Update\n\n- mode: [^\n]+\n)- status: [^\n]+",
        lambda match: f"{match.group(1)}- status: {agenda_status}",
        text,
        count=1,
    )
    if "- recovery_status:" not in text:
        metadata = [
            "- recovery_status: success",
            f"- recovery_log: `{recovery_rel}`",
            "- initial_status: partial",
        ]
        if initial_errors:
            metadata.append(f"- initial_errors: {'; '.join(initial_errors)}")
        text = text.replace(
            f"- agenda_update_status: {agenda_status}\n",
            f"- agenda_update_status: {agenda_status}\n" + "\n".join(metadata) + "\n",
            1,
        )

    recovery_lines = [
        "- recovery_status: success",
        f"- recovery_log: `{recovery_rel}`",
        "- initial_status: partial",
    ]
    if initial_errors:
        recovery_lines.append(f"- initial_errors: {'; '.join(initial_errors)}")
    else:
        recovery_lines.append("- initial_errors: none")
    text = _replace_markdown_section(text, "Recovery", recovery_lines)
    text = _replace_markdown_section(text, "Errors", ["- none"])
    safe_write(run_log_path, text, dry_run=False, backup=True)
    return True


def _robotics_relevant(item: RankedPaper) -> bool:
    if "weak_robotics_signal" in item.penalties or "non_robotics_cv_context" in item.penalties:
        return False
    reasons = " ".join(item.reasons)
    if "domain:" in reasons or "research_direction_fit" in item.reasons:
        return True
    text = " ".join(
        [
            item.paper.title,
            item.paper.summary,
            item.paper.primary_category,
            " ".join(item.paper.categories),
        ]
    ).lower()
    return any(term in text for term in ["robot", "embodied", "tactile", "bimanual", "dlo", "deformable", "grasp", "dexterous", "vla"])


def _coverage_relevant(item: RankedPaper) -> bool:
    return _robotics_relevant(item) and any(f"domain:{label}" in item.reasons for label in COVERAGE_DOMAIN_LABELS)


def _fill_import_candidate(item: RankedPaper, *, fill_threshold: int) -> RankedPaper:
    reasons = sorted(set(item.reasons + ["minimum_daily_import_fill", f"original_decision:{item.decision}"]))
    return replace(item, decision=AUTO_IMPORT_FILL_DECISION, reasons=reasons)


def select_import_candidates(
    ranked: list[RankedPaper],
    *,
    max_attempts: int,
    fill_threshold: int,
) -> list[tuple[RankedPaper, str, str]]:
    """Return import attempts ordered by confidence, with review/relevant fill candidates after primary auto-imports."""
    selected: list[tuple[RankedPaper, str, str]] = []
    seen: set[str] = set()
    primary_cap = min(PRIMARY_DAILY_IMPORT_CAP, max_attempts)
    target_floor = min(10, max_attempts)

    def add(item: RankedPaper, selection: str, original_decision: str | None = None) -> None:
        if item.paper.arxiv_id in seen or len(selected) >= max_attempts:
            return
        seen.add(item.paper.arxiv_id)
        selected.append((item, selection, original_decision or item.decision))

    for item in ranked:
        if item.decision in AUTO_IMPORT_DECISIONS:
            if len([entry for entry in selected if entry[1] in AUTO_IMPORT_DECISIONS]) >= primary_cap:
                continue
            add(item, item.decision)

    for item in ranked:
        focus_count = len([entry for entry in selected if entry[1] == FOCUS_REVIEW_DECISION])
        if focus_count >= FOCUS_DAILY_IMPORT_FLOOR and len(selected) >= target_floor:
            break
        if item.decision == FOCUS_REVIEW_DECISION and _robotics_relevant(item):
            add(item, FOCUS_REVIEW_DECISION)

    coverage_count = len([entry for entry in selected if _coverage_relevant(entry[0])])
    if coverage_count < DOMAIN_DAILY_IMPORT_FLOOR:
        for item in ranked:
            if item.quality_score < fill_threshold:
                continue
            if item.decision in AUTO_IMPORT_DECISIONS | {FOCUS_REVIEW_DECISION, "review_queue"} and _coverage_relevant(item):
                selection = item.decision if item.decision in AUTO_IMPORT_DECISIONS | {FOCUS_REVIEW_DECISION} else AUTO_IMPORT_FILL_DECISION
                candidate = item if selection != AUTO_IMPORT_FILL_DECISION else _fill_import_candidate(item, fill_threshold=fill_threshold)
                add(candidate, selection, item.decision)
                break

    for item in ranked:
        if len(selected) >= target_floor:
            break
        if item.decision in AUTO_IMPORT_DECISIONS:
            add(item, item.decision)

    for item in ranked:
        if len(selected) >= target_floor:
            break
        if item.decision == "review_queue" and _robotics_relevant(item):
            add(_fill_import_candidate(item, fill_threshold=fill_threshold), AUTO_IMPORT_FILL_DECISION, item.decision)

    for item in ranked:
        if len(selected) >= target_floor:
            break
        if item.decision in LOW_PRIORITY_DECISIONS and item.quality_score >= fill_threshold and _robotics_relevant(item):
            add(_fill_import_candidate(item, fill_threshold=fill_threshold), AUTO_IMPORT_FILL_DECISION, item.decision)

    for item in ranked:
        if len(selected) >= max_attempts:
            break
        if item.decision in AUTO_IMPORT_DECISIONS:
            add(item, item.decision)

    for item in ranked:
        if len(selected) >= max_attempts:
            break
        if item.decision == FOCUS_REVIEW_DECISION and _robotics_relevant(item):
            add(item, FOCUS_REVIEW_DECISION)

    for item in ranked:
        if len(selected) >= max_attempts:
            break
        if item.decision == "review_queue" and _robotics_relevant(item):
            add(_fill_import_candidate(item, fill_threshold=fill_threshold), AUTO_IMPORT_FILL_DECISION, item.decision)

    for item in ranked:
        if len(selected) >= max_attempts:
            break
        if item.decision in LOW_PRIORITY_DECISIONS and item.quality_score >= fill_threshold and _robotics_relevant(item):
            add(_fill_import_candidate(item, fill_threshold=fill_threshold), AUTO_IMPORT_FILL_DECISION, item.decision)

    return selected


def selection_quota_summary(selected: list[tuple[RankedPaper, str, str]], *, target: int | None = None) -> dict[str, int]:
    daily_slice = selected[:target] if target else selected
    return {
        "primary": sum(1 for _, selection, _ in daily_slice if selection in AUTO_IMPORT_DECISIONS),
        "focus": sum(1 for _, selection, _ in daily_slice if selection == FOCUS_REVIEW_DECISION),
        "domain_coverage": sum(1 for item, _, _ in daily_slice if _coverage_relevant(item)),
        "fill": sum(1 for item, _, _ in daily_slice if item.decision == AUTO_IMPORT_FILL_DECISION),
        "attempts_total": len(selected),
    }


def _selection_quota_text(summary: dict[str, int]) -> str:
    return ";".join(f"{key}={summary.get(key, 0)}" for key in ["primary", "focus", "domain_coverage", "fill", "attempts_total"])


def _non_robotics_rejected_sample(ranked: list[RankedPaper], *, limit: int = 8) -> list[RankedPaper]:
    return [item for item in ranked if "non_robotics_cv_context" in item.penalties][:limit]


def exclude_existing_candidates(
    ranked: list[RankedPaper],
    *,
    collection_key: str,
) -> tuple[list[RankedPaper], list[dict[str, Any]], str]:
    try:
        local_items = iter_local_items(collection_key)
    except Exception as exc:
        return ranked, [], f"failed:{exc}"

    new_ranked: list[RankedPaper] = []
    existing_records: list[dict[str, Any]] = []
    for item in ranked:
        existing = find_existing_paper_in_items(item.paper, local_items)
        if not existing:
            new_ranked.append(item)
            continue
        existing_records.append(
            {
                "arxiv_id": item.paper.arxiv_id,
                "title": item.paper.title,
                "quality_score": item.quality_score,
                "decision": item.decision,
                **existing.to_dict(),
            }
        )
    return new_ranked, existing_records, f"success:local_items={len(local_items)}"


def existing_literature_notes_by_title() -> dict[str, dict[str, Any]]:
    notes: dict[str, dict[str, Any]] = {}
    for path in sorted(vault_path("wiki", "topics").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        parsed = extract_frontmatter(text)
        if not parsed:
            continue
        fields = parse_frontmatter_map(parsed[0])
        if str(fields.get("type", "")).strip('"') != "literature":
            continue
        title = str(fields.get("title", "")).strip('"')
        normalized = normalize_title(title)
        if not normalized:
            continue
        notes.setdefault(
            normalized,
            {
                "path": str(path.relative_to(vault_path())),
                "title": title,
                "status": str(fields.get("status", "")).strip('"'),
                "zotero_key": str(fields.get("zotero_key", "")).strip('"'),
            },
        )
    return notes


def render_review_queue(ranked: list[RankedPaper], run_date: str) -> str:
    focus_review = [item for item in ranked if item.decision == FOCUS_REVIEW_DECISION]
    review = [item for item in ranked if item.decision == "review_queue"]
    venue_auto = [item for item in ranked if item.decision == "venue_auto_import"]
    lines = [
        "---",
        f'title: "arXiv Review Queue - {run_date}"',
        "tags: [arxiv, review-queue, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        f'summary: "{len(focus_review) + len(review)} arXiv candidates need human or focus-track review."',
        "---",
        "",
        f"# arXiv Review Queue - {run_date}",
        "",
        f"- top1_threshold: {TOP1_THRESHOLD}",
        f"- review_threshold: {REVIEW_THRESHOLD}",
        f"- focus_review_queue: {len(focus_review)}",
        "- decision_boundary: review_queue items can fill the daily minimum only after top1/venue candidates.",
        "- focus_boundary: focus_review_queue items matched an active specialized track and are considered before generic review fill.",
        f"- venue_auto_import: {len(venue_auto)} accepted top-venue candidates will bypass review queue.",
        "",
        "## Focus Review Queue",
        "",
    ]
    if not focus_review:
        lines.append("- No focus_review_queue candidates today.")
    for index, item in enumerate(focus_review, 1):
        paper = item.paper
        focus = "; ".join(f"{track}: {', '.join(matches)}" for track, matches in item.focus_matches.items())
        lines.extend(
            [
                f"## F{index}. {paper.title}",
                "",
                f"- arxiv: [{paper.arxiv_id}]({paper.url})",
                f"- score: {item.quality_score}",
                f"- focus_matches: {focus or '-'}",
                f"- reasons: {', '.join(item.reasons) if item.reasons else '-'}",
                f"- penalties: {', '.join(item.penalties) if item.penalties else '-'}",
                f"- authors: {', '.join(paper.authors[:6])}",
                f"- summary: {paper.summary[:700]}",
                "",
            ]
        )
    lines.extend(["## General Review Queue", ""])
    if not review:
        lines.append("- No review_queue candidates today.")
    for index, item in enumerate(review, 1):
        paper = item.paper
        lines.extend(
            [
                f"## {index}. {paper.title}",
                "",
                f"- arxiv: [{paper.arxiv_id}]({paper.url})",
                f"- score: {item.quality_score}",
                f"- reasons: {', '.join(item.reasons) if item.reasons else '-'}",
                f"- penalties: {', '.join(item.penalties) if item.penalties else '-'}",
                f"- authors: {', '.join(paper.authors[:6])}",
                f"- summary: {paper.summary[:700]}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def run_subprocess(command: list[str], *, timeout: int) -> tuple[int, str]:
    proc = subprocess.Popen(
        command,
        cwd=vault_path(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        kill_process_tree(proc.pid)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
        return 124, f"timeout:{timeout}s"
    output = (stdout or "") + ("\nSTDERR:\n" + stderr if stderr else "")
    return proc.returncode, output.strip()


def run_subprocess_capture(
    command: list[str],
    *,
    timeout: int,
    heartbeat: Callable[[int], None] | None = None,
    heartbeat_interval: int = 60,
) -> tuple[int, str, str]:
    proc = subprocess.Popen(
        command,
        cwd=vault_path(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if heartbeat:
        heartbeat(proc.pid)
    deadline = time.monotonic() + timeout
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise subprocess.TimeoutExpired(command, timeout)
            try:
                stdout, stderr = proc.communicate(timeout=min(heartbeat_interval, remaining))
                break
            except subprocess.TimeoutExpired:
                if heartbeat:
                    heartbeat(proc.pid)
        if heartbeat:
            heartbeat(proc.pid)
    except subprocess.TimeoutExpired:
        kill_process_tree(proc.pid)
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""
        return 124, stdout or "", (stderr or "") + f"\nTIMEOUT: {timeout}s"
    return proc.returncode, stdout or "", stderr or ""


def kill_process_tree(pid: int) -> None:
    if sys.platform.startswith("win"):
        try:
            subprocess.run(
                ["taskkill.exe", "/PID", str(pid), "/T", "/F"],
                text=True,
                capture_output=True,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            pass
        return
    try:
        import os

        os.kill(pid, 9)
    except OSError:
        pass


def ingest_zotero_key(zotero_key: str, *, timeout: int = 600) -> tuple[str, str]:
    command = [sys.executable, ".claude/scripts/ingest_paper.py", zotero_key, "--force-overwrite-stub"]
    code, output = run_subprocess(command, timeout=timeout)
    return ("success" if code == 0 else "failed", output)


def local_note_status(zotero_key: str) -> tuple[str, str]:
    key_pattern = re.compile(rf'^zotero_key:\s*"?{re.escape(zotero_key)}"?\s*$', re.MULTILINE)
    for path in sorted(vault_path("wiki", "topics").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not key_pattern.search(text):
            continue
        parsed = extract_frontmatter(text)
        if not parsed:
            return "missing_frontmatter", str(path.relative_to(vault_path()))
        fields = parse_frontmatter_map(parsed[0])
        status = fields.get("status", "").strip('"')
        return status or "missing_status", str(path.relative_to(vault_path()))
    return "missing_note", ""


def local_note_fields_from_relpath(rel_path: str) -> tuple[str, str, str]:
    cleaned = rel_path.strip().strip("`").replace("\\", "/")
    if not cleaned:
        return "missing_note", "", ""
    path = vault_path(*cleaned.split("/"))
    if not path.exists() or not path.is_file():
        return "missing_note", "", ""
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    if not parsed:
        return "missing_frontmatter", "", str(path.relative_to(vault_path()))
    fields = parse_frontmatter_map(parsed[0])
    status = str(fields.get("status", "")).strip('"') or "missing_status"
    zotero_key = str(fields.get("zotero_key", "")).strip('"')
    return status, zotero_key, str(path.relative_to(vault_path()))


def local_note_from_ingest_output(output: str) -> tuple[str, str, str]:
    pattern = re.compile(r"^INGESTED_OR_FOUND:\s+(?P<path>.+?)\s*$")
    for line in reversed(output.splitlines()):
        match = pattern.match(line.strip())
        if not match:
            continue
        status, zotero_key, note_path = local_note_fields_from_relpath(match.group("path"))
        if note_path:
            return status, zotero_key, note_path
    return "missing_note", "", ""


def wait_for_local_note(zotero_key: str, *, timeout_sec: int = 180, interval_sec: int = 10) -> tuple[str, str]:
    deadline = time.monotonic() + timeout_sec
    while True:
        note_status, note_path = local_note_status(zotero_key)
        if note_status != "missing_note":
            return note_status, note_path
        if time.monotonic() >= deadline:
            return note_status, note_path
        time.sleep(interval_sec)


def read_paper_prompt(zotero_key: str) -> str:
    template_path = vault_path(".claude", "commands", "read-paper.md")
    template = template_path.read_text(encoding="utf-8")
    return template.replace("$ARGUMENTS", zotero_key)


def _write_read_attempt_log(
    *,
    run_date: str,
    zotero_key: str,
    attempt: int,
    stdout: str,
    stderr: str,
) -> dict[str, str]:
    log_dir = vault_path("projects", "arxiv-daily", "read-logs", run_date)
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = log_dir / f"{zotero_key}-attempt{attempt}.out.log"
    stderr_path = log_dir / f"{zotero_key}-attempt{attempt}.err.log"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    return {
        "stdout": str(stdout_path.relative_to(vault_path())).replace("\\", "/"),
        "stderr": str(stderr_path.relative_to(vault_path())).replace("\\", "/"),
    }


def _write_read_heartbeat(
    *,
    run_date: str,
    zotero_key: str,
    attempt: int,
    pid: int,
    status: str,
    timeout: int,
) -> str:
    log_dir = vault_path("projects", "arxiv-daily", "read-logs", run_date)
    log_dir.mkdir(parents=True, exist_ok=True)
    heartbeat_path = log_dir / f"{zotero_key}-attempt{attempt}.heartbeat.json"
    payload = {
        "run_date": run_date,
        "zotero_key": zotero_key,
        "attempt": attempt,
        "pid": pid,
        "status": status,
        "timeout_sec": timeout,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    heartbeat_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return str(heartbeat_path.relative_to(vault_path())).replace("\\", "/")


def _read_failure_reason(output: str, note_status: str) -> str:
    lowered = output.lower()
    if "too many requests" in lowered or "429" in lowered:
        return "claude_rate_limited"
    if "timeout:" in lowered or "timed out" in lowered:
        return "timeout"
    if "could not resolve authentication" in lowered or "authentication" in lowered:
        return "claude_auth"
    if "eperm" in lowered or "permission" in lowered:
        return "permission"
    if note_status == "missing_note":
        return "missing_note_after_read"
    if note_status != "done":
        return f"not_finalized:{note_status}"
    return "unknown"


def read_zotero_key(
    zotero_key: str,
    *,
    timeout: int = 3600,
    run_date: str = "",
    attempt: int = 1,
) -> tuple[str, str, dict[str, str]]:
    prompt = read_paper_prompt(zotero_key)
    command = ["claude", "--dangerously-skip-permissions", "--print", prompt]
    heartbeat_path = ""

    def heartbeat(pid: int) -> None:
        nonlocal heartbeat_path
        if run_date:
            heartbeat_path = _write_read_heartbeat(
                run_date=run_date,
                zotero_key=zotero_key,
                attempt=attempt,
                pid=pid,
                status="running",
                timeout=timeout,
            )

    try:
        code, stdout, stderr = run_subprocess_capture(
            command,
            timeout=timeout,
            heartbeat=heartbeat if run_date else None,
            heartbeat_interval=60,
        )
    except FileNotFoundError:
        return "failed", "claude CLI not found", {}
    if run_date and heartbeat_path:
        heartbeat_path = _write_read_heartbeat(
            run_date=run_date,
            zotero_key=zotero_key,
            attempt=attempt,
            pid=0,
            status=f"finished:exit_code={code}",
            timeout=timeout,
        )
    log_paths: dict[str, str] = {}
    if run_date:
        log_paths = _write_read_attempt_log(
            run_date=run_date,
            zotero_key=zotero_key,
            attempt=attempt,
            stdout=stdout,
            stderr=stderr,
        )
        if heartbeat_path:
            log_paths["heartbeat"] = heartbeat_path
    output = (stdout or "") + ("\nSTDERR:\n" + stderr if stderr else "")
    note_status, note_path = local_note_status(zotero_key)
    verification = f"\nREAD_VERIFY: note={note_path or '-'} status={note_status}"
    if note_status == "done":
        return "success_done", output + verification, log_paths
    if code == 0:
        return f"failed_not_done:{note_status}", output + verification, log_paths
    reason = _read_failure_reason(output, note_status)
    return f"failed:{reason}", output + verification, log_paths


def read_zotero_key_timed(
    zotero_key: str,
    *,
    timeout: int,
    run_date: str = "",
    max_attempts: int = 1,
    retry_delay_sec: int = 60,
) -> tuple[str, str, float, list[dict[str, str]]]:
    started = time.monotonic()
    outputs: list[str] = []
    logs: list[dict[str, str]] = []
    status = "failed:not_started"
    for attempt in range(1, max(1, max_attempts) + 1):
        status, output, log_paths = read_zotero_key(
            zotero_key,
            timeout=timeout,
            run_date=run_date,
            attempt=attempt,
        )
        if log_paths:
            logs.append({"attempt": str(attempt), **log_paths})
        outputs.append(f"READ_ATTEMPT {attempt}/{max_attempts}: status={status}\n{output}")
        if status.startswith("success"):
            break
        if attempt < max_attempts:
            time.sleep(max(0, retry_delay_sec))
    return status, "\n\n".join(outputs), round(time.monotonic() - started, 2), logs


def render_run_log(
    *,
    run_date: str,
    status: str,
    ranked: list[RankedPaper],
    imports: list[dict[str, Any]],
    reads: list[dict[str, Any]],
    idea_path: Path,
    agenda_delta_path: Path,
    gemini_prompt_path: Path,
    idea_audit: dict[str, Any],
    idea_generation: dict[str, Any],
    errors: list[str],
    import_policy: dict[str, Any],
    existing_candidates: list[dict[str, Any]],
) -> str:
    top = [item for item in ranked if item.decision == "top1_candidate"]
    venue_auto = [item for item in ranked if item.decision == "venue_auto_import"]
    focus_review = [item for item in ranked if item.decision == FOCUS_REVIEW_DECISION]
    review = [item for item in ranked if item.decision == "review_queue"]
    new_imports = sum(1 for item in imports if item.get("status") in NEW_IMPORT_STATUSES)
    resumed_backlog = sum(1 for item in imports if item.get("status") == "backlog")
    existing_duplicates = sum(1 for item in imports if item.get("status") == "exists")
    fill_imports = sum(1 for item in imports if item.get("selection_decision") == AUTO_IMPORT_FILL_DECISION)
    focus_imports = sum(1 for item in imports if item.get("selection_decision") == FOCUS_REVIEW_DECISION)
    quota_summary = import_policy.get("selection_quota_summary", {})
    read_by_key = {str(item.get("zotero_key", "")): item for item in reads}
    new_read_success = [
        item
        for item in imports
        if item.get("status") in FOCUS_READY_STATUSES
        and str(read_by_key.get(str(item.get("zotero_key", "")), {}).get("read_status", "")).startswith("success")
    ]
    lines = [
        "---",
        f'title: "Daily arXiv Scout Run - {run_date}"',
        "tags: [arxiv, automation, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        f'summary: "Daily arXiv scout run status: {status}."',
        "---",
        "",
        f"# Daily arXiv Scout Run - {run_date}",
        "",
        f"- status: {status}",
        f"- candidates_total: {len(ranked)}",
        f"- top1_candidates: {len(top)}",
        f"- venue_auto_import: {len(venue_auto)}",
        f"- focus_review_queue: {len(focus_review)}",
        f"- review_queue: {len(review)}",
        f"- arxiv_source: {import_policy.get('arxiv_source', 'unknown')}",
        f"- mirror_records_total: {import_policy.get('mirror_records_total', 0)}",
        f"- mirror_last_success_at: {import_policy.get('mirror_last_success_at', '-')}",
        f"- search_api_fallback_used: {str(import_policy.get('search_api_fallback_used', False)).lower()}",
        f"- arxiv_fetch_errors: {import_policy.get('arxiv_fetch_errors', 0)}",
        f"- no_new_focus_keys_reason: {import_policy.get('no_new_focus_keys_reason', '-')}",
        f"- days_back: {import_policy.get('days_back')}",
        f"- max_candidates: {import_policy.get('max_candidates')}",
        f"- min_new_imports: {import_policy.get('min_new_imports')}",
        f"- max_import_attempts: {import_policy.get('max_auto_import')}",
        f"- max_daily_reads: {import_policy.get('max_read')}",
        f"- fill_import_threshold: {import_policy.get('fill_import_threshold')}",
        f"- existing_prefilter: {import_policy.get('existing_prefilter', 'not_run')}",
        f"- existing_candidates_excluded: {len(existing_candidates)}",
        f"- import_attempts: {len(imports)}",
        f"- new_imports_created: {new_imports}",
        f"- resumed_backlog_imports: {resumed_backlog}",
        f"- new_imports_read_success: {len(new_read_success)}",
        f"- existing_duplicates: {existing_duplicates}",
        f"- auto_import_fill_attempts: {fill_imports}",
        f"- focus_review_import_attempts: {focus_imports}",
        f"- selection_quota_summary: {_selection_quota_text(quota_summary) if isinstance(quota_summary, dict) else quota_summary}",
        f"- legacy_idea_pointer: `{idea_path.relative_to(vault_path())}`",
        f"- agenda_delta_file: `{agenda_delta_path.relative_to(vault_path())}`",
        f"- gemini_prompt_file: `{gemini_prompt_path.relative_to(vault_path())}`",
        "- workflow_manifest: `projects/research-agenda/workflow-contracts/daily-readable-workflow.json`",
        "- provider_matrix: `projects/research-agenda/workflow-contracts/provider-matrix.json`",
        f"- agenda_update_mode: {idea_generation.get('mode', 'research_agenda_update')}",
        f"- agenda_update_status: {idea_generation.get('status', 'unknown')}",
        f"- strict_kb_maintenance: {import_policy.get('strict_kb_maintenance', 'not_run')}",
        f"- legacy_idea_audit: {idea_audit.get('status', 'not_applicable')}",
        "",
        "## Top Candidates",
        "",
    ]
    if not top:
        lines.append("- evidence_gap: no candidate reached top1_candidate threshold.")
    for item in top:
        paper = item.paper
        lines.append(f"- [{paper.title}]({paper.url}) - score={item.quality_score}; arXiv={paper.arxiv_id}; reasons={', '.join(item.reasons)}")
    lines.extend(["", "## Venue Auto Imports", ""])
    if not venue_auto:
        lines.append("- none")
    for item in venue_auto:
        paper = item.paper
        lines.append(f"- [{paper.title}]({paper.url}) - score={item.quality_score}; arXiv={paper.arxiv_id}; reasons={', '.join(item.reasons)}")
    lines.extend(["", "## Focus Review Queue", ""])
    if not focus_review:
        lines.append("- none")
    for item in focus_review:
        paper = item.paper
        focus = "; ".join(f"{track}: {', '.join(matches)}" for track, matches in item.focus_matches.items())
        lines.append(
            f"- [{paper.title}]({paper.url}) - score={item.quality_score}; arXiv={paper.arxiv_id}; "
            f"focus={focus or '-'}; reasons={', '.join(item.reasons)}"
        )
    lines.extend(["", "## Existing Zotero Candidates Excluded", ""])
    if not existing_candidates:
        lines.append("- none")
    for item in existing_candidates:
        lines.append(
            f"- arxiv={item.get('arxiv_id')} score={item.get('quality_score')} "
            f"decision={item.get('decision')} zotero_key={item.get('zotero_key', '')} "
            f"title={item.get('title', '')}"
        )
    lines.extend(["", "## Imports", ""])
    if not imports:
        lines.append("- No Zotero imports attempted.")
    for item in imports:
        lines.append(
            f"- arxiv={item.get('arxiv_id')} selection={item.get('selection_decision', '')} "
            f"original={item.get('original_decision', '')} score={item.get('quality_score', '')} "
            f"status={item.get('status')} zotero_key={item.get('zotero_key', '')} message={item.get('message', '')}"
        )
    lines.extend(["", "## Reading", ""])
    if not reads:
        lines.append("- No Claudian reading attempted.")
    for item in reads:
        lines.append(
            f"- zotero_key={item.get('zotero_key')} ingest={item.get('ingest_status')} "
            f"read={item.get('read_status')} read_elapsed_sec={item.get('read_elapsed_sec', '-')}"
        )
        if item.get("read_attempt_logs"):
            logs = "; ".join(
                f"attempt{log.get('attempt')}:out={log.get('stdout')},err={log.get('stderr')},heartbeat={log.get('heartbeat', '-')}"
                for log in item.get("read_attempt_logs", [])
            )
            lines.append(f"  - read_attempt_logs: {logs}")
    lines.extend(["", "## Agenda Update", ""])
    lines.append(f"- mode: {idea_generation.get('mode', 'research_agenda_update')}")
    lines.append(f"- status: {idea_generation.get('status', 'unknown')}")
    if idea_generation.get("message"):
        lines.append(f"- message: {idea_generation['message']}")
        for marker in ["MANDATORY_MODEL_BATTLE:", "AGENDA_DELTA:", "CODEX_REVIEW_PENDING:"]:
            match = re.search(rf"^{re.escape(marker)}\s*(.+)$", str(idea_generation["message"]), re.MULTILINE)
            if match:
                key = marker.rstrip(":").lower()
                lines.append(f"- {key}: {match.group(1).strip()}")
    lines.extend(["", "## Errors", ""])
    if not errors:
        lines.append("- none")
    else:
        lines.extend(f"- {error}" for error in errors)
    return "\n".join(lines).rstrip() + "\n"


def render_reading_backlog(*, run_date: str, imports: list[dict[str, Any]], reads: list[dict[str, Any]]) -> str:
    read_by_key = {str(item.get("zotero_key", "")): item for item in reads}
    lines = [
        "---",
        f'title: "Daily arXiv Reading Backlog - {run_date}"',
        "tags: [arxiv, reading-backlog, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        'summary: "Imported arXiv papers that still need full Claudian reading."',
        "---",
        "",
        f"# Daily arXiv Reading Backlog - {run_date}",
        "",
    ]
    pending = 0
    for item in imports:
        key = str(item.get("zotero_key", ""))
        read = read_by_key.get(key, {})
        if str(read.get("read_status", "")).startswith("success"):
            continue
        if read.get("read_status") == "skipped":
            continue
        pending += 1
        lines.append(f"- arxiv={item.get('arxiv_id')} zotero_key={key} import_status={item.get('status')} read_status={read.get('read_status', 'not_started')}")
    if pending == 0:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def render_resume_log(
    *,
    run_date: str,
    status: str,
    imports: list[dict[str, Any]],
    reads: list[dict[str, Any]],
    focus_keys: list[str],
    agenda_status: str,
    errors: list[str],
) -> str:
    lines = [
        "---",
        f'title: "Daily arXiv Backlog Recovery - {run_date}"',
        "tags: [arxiv, reading-backlog, recovery]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        f'summary: "Backlog recovery status: {status}."',
        "---",
        "",
        f"# Daily arXiv Backlog Recovery - {run_date}",
        "",
        f"- status: {status}",
        f"- attempted_reads: {len(reads)}",
        f"- successful_reads: {sum(1 for item in reads if str(item.get('read_status', '')).startswith('success'))}",
        f"- focus_zotero_keys: {', '.join(focus_keys) if focus_keys else '-'}",
        f"- agenda_update_status: {agenda_status}",
        "",
        "## Imports",
        "",
    ]
    for item in imports:
        lines.append(
            f"- arxiv={item.get('arxiv_id')} status={item.get('status')} "
            f"zotero_key={item.get('zotero_key', '')} message={item.get('message', '')}"
        )
    if not imports:
        lines.append("- none")
    lines.extend(["", "## Reading", ""])
    for item in reads:
        lines.append(
            f"- zotero_key={item.get('zotero_key')} ingest={item.get('ingest_status')} "
            f"read={item.get('read_status')} read_elapsed_sec={item.get('read_elapsed_sec', '-')}"
        )
        if item.get("read_attempt_logs"):
            logs = "; ".join(
                f"attempt{log.get('attempt')}:out={log.get('stdout')},err={log.get('stderr')},heartbeat={log.get('heartbeat', '-')}"
                for log in item.get("read_attempt_logs", [])
            )
            lines.append(f"  - read_attempt_logs: {logs}")
    if not reads:
        lines.append("- none")
    lines.extend(["", "## Errors", ""])
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def merge_resume_backlog(
    *,
    run_date: str,
    original_records: list[dict[str, str]],
    reads: list[dict[str, Any]],
) -> str:
    read_by_key = {str(item.get("zotero_key", "")): item for item in reads}
    lines = [
        "---",
        f'title: "Daily arXiv Reading Backlog - {run_date}"',
        "tags: [arxiv, reading-backlog, embodied-ai]",
        f'created: "{run_date}"',
        f'updated: "{run_date}"',
        'type: "permanent"',
        'status: "draft"',
        'summary: "Imported arXiv papers that still need full Claudian reading."',
        "---",
        "",
        f"# Daily arXiv Reading Backlog - {run_date}",
        "",
    ]
    pending = 0
    for record in original_records:
        key = record.get("key", "")
        if not key:
            continue
        read = read_by_key.get(key)
        if read and str(read.get("read_status", "")).startswith("success"):
            continue
        note_status, _ = local_note_status(key)
        if note_status == "done":
            continue
        pending += 1
        read_status = str(read.get("read_status", record.get("read_status", "backlog"))) if read else record.get("read_status", "backlog")
        lines.append(
            f"- arxiv={record.get('arxiv', '')} zotero_key={key} "
            f"import_status={record.get('import_status', 'backlog')} read_status={read_status}"
        )
    if pending == 0:
        lines.append("- none")
    return "\n".join(lines).rstrip() + "\n"


def render_legacy_idea_pointer(*, run_date: str, agenda_delta_path: Path, focus_keys: list[str], agenda_status: str) -> str:
    agenda_delta_rel = str(agenda_delta_path.relative_to(vault_path())).replace("\\", "/")
    return "\n".join(
        [
            "---",
            f'title: "Daily Embodied AI Ideas - {run_date}"',
            "tags: [idea, arxiv, embodied-ai, compatibility]",
            f'created: "{run_date}"',
            f'updated: "{run_date}"',
            'type: "permanent"',
            'status: "done"',
            'summary: "Compatibility pointer. Final research ideas now live in the long-term research agenda."',
            'evidence_level: "partial"',
            "---",
            "",
            f"# Daily Embodied AI Ideas - {run_date}",
            "",
            "This file is kept only for backward compatibility. The daily workflow no longer treats this as the final idea source.",
            "",
            f"- agenda_delta: `{agenda_delta_rel}`",
            f"- agenda_update_status: {agenda_status}",
            f"- focus_zotero_keys: {', '.join(focus_keys) if focus_keys else '-'}",
            "- boundary: high-quality ideas are promoted from `projects/research-agenda/idea_bank/` only after evidence and review gates.",
            "",
        ]
    )


def run_resume_backlog(args: argparse.Namespace) -> int:
    run_date = args.run_date or today_iso()
    base_dir = vault_path("projects", "arxiv-daily")
    run_log_path = base_dir / f"{run_date}-run.md"
    backlog_path = base_dir / f"{run_date}-reading-backlog.md"
    recovery_log_path = base_dir / f"{run_date}-backlog-recovery.md"
    idea_path = vault_path("projects", "ideas", f"{run_date}-embodied-ai-ideas.md")
    agenda_delta_path = vault_path("projects", "research-agenda", "daily", f"{run_date}-agenda-delta.md")
    gemini_prompt_path = vault_path("projects", "ideas", f"{run_date}-gemini-idea-prompt.md")
    errors: list[str] = []

    resume_records = parse_backlog(backlog_path)
    if args.dry_run:
        pending_records = []
        for record in resume_records:
            key = record.get("key", "")
            note_status, note_path = local_note_status(key) if key else ("missing_key", "")
            if key and not record.get("read_status", "").startswith("success") and note_status != "done":
                pending_records.append((record, note_status, note_path))
        safe_print(
            "DRY-RUN RESUME-BACKLOG "
            f"run_date={run_date} "
            f"pending={len(pending_records)} "
            f"max_read={args.max_read} "
            f"read_retries={args.read_retries}"
        )
        for record, note_status, note_path in pending_records[: max(1, args.max_read)]:
            safe_print(
                f"{record.get('arxiv', '')} zotero_key={record.get('key', '')} "
                f"note_status={note_status} note={note_path or '-'}"
            )
        return 0
    prior_success_keys = parse_successful_read_keys_with_backups(run_log_path)
    imports: list[dict[str, Any]] = []
    reads: list[dict[str, Any]] = []
    read_attempts = 0
    for record in resume_records:
        if record.get("read_status", "").startswith("success"):
            continue
        key = record.get("key", "")
        if not key:
            continue
        note_status, note_path = local_note_status(key)
        imports.append(
            {
                "arxiv_id": record.get("arxiv", ""),
                "quality_score": "",
                "selection_decision": "resume_backlog",
                "original_decision": "resume_backlog",
                "status": "backlog",
                "zotero_key": key,
                "message": f"resumed from reading backlog; note_status={note_status}; note={note_path or '-'}",
                "mode": "resume_backlog",
                "existing": True,
            }
        )
        read_status = "skipped"
        read_output = ""
        read_attempt_logs: list[dict[str, str]] = []
        read_elapsed_sec: float | str = "-"
        if note_status == "done":
            ingest_status = "success"
            ingest_output = f"already_done:{note_path}"
            read_status = "success_done_already"
        elif note_status != "missing_note":
            ingest_status = "success"
            ingest_output = f"local_note_ready:{note_status}:{note_path}"
        else:
            ingest_status, ingest_output = ingest_zotero_key(key)
            output_note_status, output_key, output_note_path = local_note_from_ingest_output(ingest_output)
            if output_key and output_key != key:
                key = output_key
                note_status, note_path = output_note_status, output_note_path
                imports[-1]["zotero_key"] = output_key
                imports[-1]["message"] = f"{imports[-1].get('message', '')}; canonical_note_key={output_key}; note={output_note_path}"
            note_status, note_path = wait_for_local_note(key)
            ingest_output = f"{ingest_output}\nLOCAL_NOTE_READY: status={note_status} note={note_path or '-'}"
            if ingest_status != "success" and note_status != "missing_note":
                ingest_status = "success"
                ingest_output = f"{ingest_output}\nINGEST_RECOVERED_BY_LOCAL_NOTE: {note_path}"
        if note_status == "done" and ingest_status == "success":
            read_status = "success_done_already"
        elif note_status not in {"done", "missing_note"} and ingest_status == "success" and not args.skip_read and read_attempts < args.max_read:
            read_attempts += 1
            read_status, read_output, read_elapsed_sec, read_attempt_logs = read_zotero_key_timed(
                key,
                timeout=args.read_timeout,
                run_date=run_date,
                max_attempts=args.read_retries + 1,
                retry_delay_sec=args.read_retry_delay,
            )
        elif note_status == "missing_note" and ingest_status == "success" and not args.skip_read:
            read_status = "waiting_local_note"
        elif note_status != "done" and ingest_status == "success" and not args.skip_read:
            read_status = "backlog"
        reads.append(
            {
                "zotero_key": key,
                "ingest_status": ingest_status,
                "ingest_output_tail": ingest_output[-1200:],
                "read_status": read_status,
                "read_elapsed_sec": read_elapsed_sec,
                "read_attempt_logs": read_attempt_logs,
                "read_output_tail": read_output[-1200:],
            }
        )
        if ingest_status != "success":
            errors.append(f"ingest_failed:{key}")
        if read_status == "waiting_local_note":
            errors.append(f"read_pending:{key}:waiting_local_note")
        if read_status not in {"skipped", "backlog", "waiting_local_note"} and not read_status.startswith("success"):
            errors.append(f"read_failed:{key}:{read_status}")

    maintenance_status = "not_run"
    if reads and not args.skip_read:
        try:
            maintenance_code, maintenance_output = run_subprocess(
                [sys.executable, ".claude/scripts/fix_strict_kb_after_read.py"],
                timeout=300,
            )
        except Exception as exc:
            maintenance_code, maintenance_output = 1, str(exc)
        maintenance_status = "success" if maintenance_code == 0 else "failed"
        if maintenance_code != 0:
            errors.append(f"strict_kb_maintenance_failed:{maintenance_output[-400:]}")

    read_by_key = {str(item.get("zotero_key", "")): item for item in reads}
    focus_zotero_keys: list[str] = []
    seen_focus_keys: set[str] = set()
    for item in imports:
        key = str(item.get("zotero_key", ""))
        if key and str(read_by_key.get(key, {}).get("read_status", "")).startswith("success"):
            focus_zotero_keys.append(key)
            seen_focus_keys.add(key)
    for key in prior_success_keys:
        if key and key not in seen_focus_keys:
            focus_zotero_keys.append(key)
            seen_focus_keys.add(key)

    if not focus_zotero_keys and args.idea_mode == "gemini-divergent":
        agenda_command = [
            sys.executable,
            ".claude/scripts/research_agenda_update.py",
            "--run-date",
            run_date,
            "--idea-generator",
            "none",
            "--idea-timeout",
            str(args.idea_timeout),
            "--gemini-model",
            args.gemini_model,
            "--deepseek-model",
            args.deepseek_model,
            "--deepseek-timeout",
            str(args.deepseek_timeout),
            "--raw-candidate-limit",
            str(args.raw_candidate_limit),
            "--min-raw-candidates",
            str(args.min_raw_candidates),
            "--max-generated",
            str(args.max_generated),
        ]
    else:
        agenda_command = [sys.executable, ".claude/scripts/research_agenda_update.py", "--run-date", run_date]
        if focus_zotero_keys:
            agenda_command.extend(["--zotero-keys", ",".join(focus_zotero_keys)])
        agenda_command.extend(
            [
                "--idea-generator",
                args.idea_mode,
                "--idea-timeout",
                str(args.idea_timeout),
                "--gemini-model",
                args.gemini_model,
                "--deepseek-model",
                args.deepseek_model,
                "--deepseek-timeout",
                str(args.deepseek_timeout),
                "--raw-candidate-limit",
                str(args.raw_candidate_limit),
                "--min-raw-candidates",
                str(args.min_raw_candidates),
                "--max-generated",
                str(args.max_generated),
            ]
        )
    try:
        agenda_code, agenda_output = run_subprocess(
            agenda_command,
            timeout=max(900, args.idea_timeout * 2 + args.deepseek_timeout + 300),
        )
    except Exception as exc:
        agenda_code, agenda_output = 1, str(exc)
    if agenda_code == 0:
        agenda_status = "skipped_no_focus_keys" if not focus_zotero_keys and args.idea_mode == "gemini-divergent" else "success"
    else:
        agenda_status = "partial"
        errors.append("research_agenda_update_failed")

    status = "success" if not errors else "partial"
    safe_write(backlog_path, merge_resume_backlog(run_date=run_date, original_records=resume_records, reads=reads), dry_run=False, backup=True)
    safe_write(
        recovery_log_path,
        render_resume_log(
            run_date=run_date,
            status=status,
            imports=imports,
            reads=reads,
            focus_keys=focus_zotero_keys,
            agenda_status=agenda_status,
            errors=errors,
        ),
        dry_run=False,
        backup=True,
    )
    safe_write(
        idea_path,
        render_legacy_idea_pointer(run_date=run_date, agenda_delta_path=agenda_delta_path, focus_keys=focus_zotero_keys, agenda_status=agenda_status),
        dry_run=False,
        backup=True,
    )
    reconciled = reconcile_run_log_after_recovery(
        run_log_path=run_log_path,
        recovery_log_path=recovery_log_path,
        recovery_status=status,
        agenda_status=agenda_status,
    )
    safe_print(f"RECOVERY_LOG: {recovery_log_path.relative_to(vault_path())}")
    safe_print(f"BACKLOG: {backlog_path.relative_to(vault_path())}")
    safe_print(f"AGENDA_DELTA: {agenda_delta_path.relative_to(vault_path())}")
    safe_print(f"AGENDA_UPDATE: research_agenda_update:{agenda_status}")
    safe_print(f"STRICT_KB_MAINTENANCE: {maintenance_status}")
    safe_print(f"RUN_LOG_RECONCILED: {str(reconciled).lower()}")
    if errors:
        safe_print("PIPELINE_STATUS: partial")
        for error in errors:
            safe_print(f"ERROR: {error}")
        return 2
    safe_print("PIPELINE_STATUS: success")
    return 0


def run_pipeline(args: argparse.Namespace) -> int:
    run_date = args.run_date or today_iso()
    if args.resume_backlog:
        return run_resume_backlog(args)
    as_of = datetime.fromisoformat(run_date).replace(tzinfo=timezone.utc) + timedelta(days=1)
    base_dir = vault_path("projects", "arxiv-daily")
    candidates_path = base_dir / f"{run_date}-candidates.jsonl"
    review_path = base_dir / "review_queue" / f"{run_date}-review.md"
    run_log_path = base_dir / f"{run_date}-run.md"
    backlog_path = base_dir / f"{run_date}-reading-backlog.md"
    idea_path = vault_path("projects", "ideas", f"{run_date}-embodied-ai-ideas.md")
    gemini_prompt_path = vault_path("projects", "ideas", f"{run_date}-gemini-idea-prompt.md")
    agenda_delta_path = vault_path("projects", "research-agenda", "daily", f"{run_date}-agenda-delta.md")
    errors: list[str] = []

    queries = args.query or DEFAULT_QUERIES
    papers, source_info = collect_candidates_from_source(
        queries,
        source=args.source,
        max_candidates=args.max_candidates,
        days_back=args.days_back,
        as_of=as_of,
        errors=errors,
        fetch_timeout=args.fetch_timeout,
        fetch_retries=args.fetch_retries,
        query_delay=args.query_delay,
    )
    cache_fallback = False
    ranked_all = rank_papers(papers)
    if not ranked_all:
        cached = load_cached_ranked(candidates_path)
        if cached:
            cache_fallback = True
            ranked_all = cached
            errors.append(f"arxiv_cache_fallback:{candidates_path.relative_to(vault_path())}")
    new_ranked_all, existing_candidates, existing_prefilter = exclude_existing_candidates(
        ranked_all,
        collection_key=args.collection,
    )
    if existing_prefilter.startswith("failed:"):
        errors.append(f"existing_prefilter_{existing_prefilter}")
    ranked = new_ranked_all[: args.max_candidates]
    selection_pool = new_ranked_all[: max(args.max_candidates, args.max_auto_import)]
    records = [item.to_dict() for item in new_ranked_all[: max(args.max_candidates, args.max_auto_import)]]
    import_policy = {
        "min_new_imports": args.min_new_imports,
        "max_auto_import": args.max_auto_import,
        "max_read": args.max_read,
        "fill_import_threshold": args.fill_import_threshold,
        "fetch_timeout": args.fetch_timeout,
        "fetch_retries": args.fetch_retries,
        "query_delay": args.query_delay,
        "days_back": args.days_back,
        "max_candidates": args.max_candidates,
        "arxiv_source": source_info.get("source", "unknown"),
        "mirror_records_total": source_info.get("records_total", source_info.get("mirror_records_total", 0)),
        "mirror_last_success_at": source_info.get("last_success_at", source_info.get("mirror_last_success_at", "")),
        "search_api_fallback_used": source_info.get("search_api_fallback_used", False),
        "arxiv_fetch_errors": sum(1 for error in errors if error.startswith("arxiv_fetch_failed")),
        "existing_prefilter": existing_prefilter,
        "existing_candidates_excluded": len(existing_candidates),
    }
    selected_import_candidates = select_import_candidates(
        selection_pool,
        max_attempts=args.max_auto_import,
        fill_threshold=args.fill_import_threshold,
    )
    quota_summary = selection_quota_summary(selected_import_candidates, target=args.min_new_imports)
    import_policy["selection_quota_summary"] = quota_summary
    existing_note_titles = existing_literature_notes_by_title()

    if args.dry_run:
        primary_count = sum(1 for item, _, _ in selected_import_candidates if item.decision in AUTO_IMPORT_DECISIONS)
        focus_count = sum(1 for _, selection, _ in selected_import_candidates if selection == FOCUS_REVIEW_DECISION)
        fill_count = sum(1 for item, _, _ in selected_import_candidates if item.decision == AUTO_IMPORT_FILL_DECISION)
        safe_print(
            "DRY-RUN "
            f"candidates={len(ranked)} "
            f"source={import_policy['arxiv_source']} "
            f"days_back={args.days_back} "
            f"max_candidates={args.max_candidates} "
            f"top1={sum(1 for item in ranked if item.decision == 'top1_candidate')} "
            f"venue_auto={sum(1 for item in ranked if item.decision == 'venue_auto_import')} "
            f"focus_review={sum(1 for item in ranked if item.decision == FOCUS_REVIEW_DECISION)} "
            f"review={sum(1 for item in ranked if item.decision == 'review_queue')} "
            f"existing_excluded={len(existing_candidates)} "
            f"import_attempts={len(selected_import_candidates)} "
            f"primary_imports={primary_count} "
            f"focus_imports={focus_count} "
            f"fill_imports={fill_count} "
            f"quota={_selection_quota_text(quota_summary)} "
            f"min_new_imports={args.min_new_imports} "
            f"cache={'true' if cache_fallback else 'false'}"
        )
        for item, selection, original_decision in selected_import_candidates[:15]:
            safe_print(f"{item.quality_score:3d} {selection:17s} original={original_decision:12s} {item.paper.arxiv_id} {item.paper.title}")
        if existing_candidates:
            safe_print("EXISTING_EXCLUDED_SAMPLE")
            for item in existing_candidates[:10]:
                safe_print(
                    f"{item.get('quality_score', ''):>3} {item.get('decision', ''):17s} "
                    f"{item.get('arxiv_id')} zotero_key={item.get('zotero_key', '')} {item.get('title', '')}"
                )
        rejected_sample = _non_robotics_rejected_sample(ranked_all)
        if rejected_sample:
            safe_print("REJECTED_NON_ROBOTICS_SAMPLE")
            for item in rejected_sample:
                safe_print(f"{item.quality_score:3d} {'/'.join(item.penalties):24s} {item.paper.arxiv_id} {item.paper.title}")
        for error in errors:
            safe_print(f"WARN: {error}")
        return 0

    write_jsonl(candidates_path, records, dry_run=False)
    safe_write(review_path, render_review_queue(ranked, run_date), dry_run=False, backup=True)

    imports: list[dict[str, Any]] = []
    reads: list[dict[str, Any]] = []
    prior_success_keys = parse_successful_read_keys_with_backups(run_log_path) if args.resume_backlog else []
    resume_records = parse_backlog(backlog_path) if args.resume_backlog else []
    can_import = bool(selected_import_candidates) and not args.resume_backlog
    if can_import:
        pf = preflight(args.collection)
        if not (pf.get("local_read") and pf.get("write_credentials")):
            errors.extend(pf.get("errors", []))
            can_import = False

    new_import_count = 0
    read_attempts = 0
    if can_import:
        for ranked_item, selection_decision, original_decision in selected_import_candidates:
            if new_import_count >= args.min_new_imports:
                break
            paper = ranked_item.paper
            existing_note = existing_note_titles.get(normalize_title(paper.title))
            if existing_note and existing_note.get("zotero_key"):
                result = ImportResult(
                    status="exists",
                    zotero_key=str(existing_note.get("zotero_key", "")),
                    message=(
                        "matched existing local literature note by title; "
                        f"note={existing_note.get('path', '-')}; "
                        f"note_status={existing_note.get('status', '-')}"
                    ),
                    mode="local_note",
                    existing=True,
                )
            else:
                result = None
            try:
                if result is None:
                    result = import_ranked_paper(ranked_item, collection_key=args.collection, dry_run=False)
            except Exception as exc:
                result = ImportResult(status="failed", message=str(exc), mode="web_api")
            if result.status in NEW_IMPORT_STATUSES:
                new_import_count += 1
            import_record = {
                "arxiv_id": paper.arxiv_id,
                "quality_score": ranked_item.quality_score,
                "selection_decision": selection_decision,
                "original_decision": original_decision,
                **result.to_dict(),
            }
            imports.append(import_record)
            if result.status not in INGEST_READY_STATUSES or not result.zotero_key:
                errors.append(f"zotero_import_not_ready:{paper.arxiv_id}:{result.status}:{result.message}")
                continue
            note_status, note_path = local_note_status(result.zotero_key)
            if note_status != "missing_note":
                ingest_status = "success"
                ingest_output = f"local_note_ready:{note_status}:{note_path}"
            else:
                ingest_status, ingest_output = ingest_zotero_key(result.zotero_key)
                output_note_status, output_key, output_note_path = local_note_from_ingest_output(ingest_output)
                if output_key and output_key != result.zotero_key:
                    result.zotero_key = output_key
                    import_record["zotero_key"] = output_key
                    import_record["message"] = f"{import_record.get('message', '')}; canonical_note_key={output_key}; note={output_note_path}"
                    note_status, note_path = output_note_status, output_note_path
            read_status = "skipped"
            read_output = ""
            read_attempt_logs: list[dict[str, str]] = []
            read_elapsed_sec: float | str = "-"
            if not args.skip_read:
                note_status, note_path = wait_for_local_note(result.zotero_key)
                ingest_output = (
                    f"{ingest_output}\nLOCAL_NOTE_READY: status={note_status} note={note_path or '-'}"
                )
                if ingest_status != "success" and note_status != "missing_note":
                    ingest_status = "success"
                    ingest_output = f"{ingest_output}\nINGEST_RECOVERED_BY_LOCAL_NOTE: {note_path}"
                if ingest_status != "success":
                    read_status = "skipped"
                elif note_status == "done":
                    read_status = "success_done_already"
                elif note_status == "missing_note":
                    read_status = "waiting_local_note"
                elif read_attempts < args.max_read:
                    read_attempts += 1
                    read_status, read_output, read_elapsed_sec, read_attempt_logs = read_zotero_key_timed(
                        result.zotero_key,
                        timeout=args.read_timeout,
                        run_date=run_date,
                        max_attempts=args.read_retries + 1,
                        retry_delay_sec=args.read_retry_delay,
                    )
                else:
                    read_status = "backlog"
            reads.append(
                {
                    "zotero_key": result.zotero_key,
                    "ingest_status": ingest_status,
                    "ingest_output_tail": ingest_output[-1200:],
                    "read_status": read_status,
                    "read_elapsed_sec": read_elapsed_sec,
                    "read_attempt_logs": read_attempt_logs,
                    "read_output_tail": read_output[-1200:],
                }
            )
            if ingest_status != "success":
                errors.append(f"ingest_failed:{result.zotero_key}")
            if read_status == "waiting_local_note":
                errors.append(f"read_pending:{result.zotero_key}:waiting_local_note")
            if read_status not in {"skipped", "backlog", "waiting_local_note"} and not read_status.startswith("success"):
                errors.append(f"read_failed:{result.zotero_key}:{read_status}")
    if args.resume_backlog:
        for record in resume_records:
            if record.get("read_status", "").startswith("success"):
                continue
            key = record.get("key", "")
            if not key:
                continue
            note_status, note_path = local_note_status(key)
            imports.append(
                {
                    "arxiv_id": record.get("arxiv", ""),
                    "quality_score": "",
                    "selection_decision": "resume_backlog",
                    "original_decision": "resume_backlog",
                    "status": "backlog",
                    "zotero_key": key,
                    "message": f"resumed from reading backlog; note_status={note_status}; note={note_path or '-'}",
                    "mode": "resume_backlog",
                    "existing": True,
                }
            )
            new_import_count += 1
            read_status = "skipped"
            read_output = ""
            read_attempt_logs: list[dict[str, str]] = []
            read_elapsed_sec: float | str = "-"
            if note_status == "done":
                ingest_status = "success"
                ingest_output = f"already_done:{note_path}"
                read_status = "success_done_already"
            elif note_status != "missing_note":
                ingest_status = "success"
                ingest_output = f"local_note_ready:{note_status}:{note_path}"
            else:
                ingest_status, ingest_output = ingest_zotero_key(key)
                output_note_status, output_key, output_note_path = local_note_from_ingest_output(ingest_output)
                if output_key and output_key != key:
                    key = output_key
                    note_status, note_path = output_note_status, output_note_path
                    imports[-1]["zotero_key"] = output_key
                    imports[-1]["message"] = f"{imports[-1].get('message', '')}; canonical_note_key={output_key}; note={output_note_path}"
                note_status, note_path = wait_for_local_note(key)
                ingest_output = f"{ingest_output}\nLOCAL_NOTE_READY: status={note_status} note={note_path or '-'}"
                if ingest_status != "success" and note_status != "missing_note":
                    ingest_status = "success"
                    ingest_output = f"{ingest_output}\nINGEST_RECOVERED_BY_LOCAL_NOTE: {note_path}"
            if note_status == "done" and ingest_status == "success":
                read_status = "success_done_already"
            elif note_status not in {"done", "missing_note"} and ingest_status == "success" and not args.skip_read and read_attempts < args.max_read:
                read_attempts += 1
                read_status, read_output, read_elapsed_sec, read_attempt_logs = read_zotero_key_timed(
                    key,
                    timeout=args.read_timeout,
                    run_date=args.run_date,
                    max_attempts=args.read_retries + 1,
                    retry_delay_sec=args.read_retry_delay,
                )
            elif note_status == "missing_note" and ingest_status == "success" and not args.skip_read:
                read_status = "waiting_local_note"
            elif note_status != "done" and ingest_status == "success" and not args.skip_read:
                read_status = "backlog"
            reads.append(
                {
                    "zotero_key": key,
                    "ingest_status": ingest_status,
                    "ingest_output_tail": ingest_output[-1200:],
                    "read_status": read_status,
                    "read_elapsed_sec": read_elapsed_sec,
                    "read_attempt_logs": read_attempt_logs,
                    "read_output_tail": read_output[-1200:],
                }
            )
            if ingest_status != "success":
                errors.append(f"ingest_failed:{key}")
            if read_status == "waiting_local_note":
                errors.append(f"read_pending:{key}:waiting_local_note")
            if read_status not in {"skipped", "backlog", "waiting_local_note"} and not read_status.startswith("success"):
                errors.append(f"read_failed:{key}:{read_status}")
    if not args.resume_backlog and new_import_count < args.min_new_imports:
        errors.append(f"min_new_imports_not_met:created={new_import_count}:target={args.min_new_imports}:attempts={len(imports)}")

    maintenance_status = "not_run"
    if reads and not args.skip_read:
        try:
            maintenance_code, maintenance_output = run_subprocess(
                [sys.executable, ".claude/scripts/fix_strict_kb_after_read.py"],
                timeout=300,
            )
        except Exception as exc:
            maintenance_code, maintenance_output = 1, str(exc)
        maintenance_status = "success" if maintenance_code == 0 else "failed"
        if maintenance_code != 0:
            errors.append(f"strict_kb_maintenance_failed:{maintenance_output[-400:]}")
    import_policy["strict_kb_maintenance"] = maintenance_status

    read_by_key = {str(item.get("zotero_key", "")): item for item in reads}
    focus_imports = [
        item
        for item in imports
        if item.get("status") in FOCUS_READY_STATUSES
        and str(read_by_key.get(str(item.get("zotero_key", "")), {}).get("read_status", "")).startswith("success")
    ]
    focus_arxiv_ids = [str(item.get("arxiv_id", "")) for item in focus_imports if item.get("arxiv_id")]
    focus_zotero_keys = [str(item.get("zotero_key", "")) for item in focus_imports if item.get("zotero_key")]
    if args.resume_backlog:
        seen_focus_keys = set(focus_zotero_keys)
        for key in prior_success_keys:
            if key and key not in seen_focus_keys:
                focus_zotero_keys.append(key)
                seen_focus_keys.add(key)
    if not focus_zotero_keys:
        import_policy["no_new_focus_keys_reason"] = "no_new_successfully_read_imports"

    if not focus_zotero_keys and args.idea_mode == "gemini-divergent":
        agenda_command = [
            sys.executable,
            ".claude/scripts/research_agenda_update.py",
            "--run-date",
            run_date,
            "--idea-generator",
            "none",
            "--idea-timeout",
            str(args.idea_timeout),
            "--gemini-model",
            args.gemini_model,
            "--deepseek-model",
            args.deepseek_model,
            "--deepseek-timeout",
            str(args.deepseek_timeout),
            "--raw-candidate-limit",
            str(args.raw_candidate_limit),
            "--min-raw-candidates",
            str(args.min_raw_candidates),
            "--max-generated",
            str(args.max_generated),
        ]
    else:
        agenda_command = [
            sys.executable,
            ".claude/scripts/research_agenda_update.py",
            "--run-date",
            run_date,
        ]
        if focus_zotero_keys:
            agenda_command.extend(["--zotero-keys", ",".join(focus_zotero_keys)])
        agenda_command.extend(
            [
                "--idea-generator",
                args.idea_mode,
                "--idea-timeout",
                str(args.idea_timeout),
                "--gemini-model",
                args.gemini_model,
                "--deepseek-model",
                args.deepseek_model,
                "--deepseek-timeout",
                str(args.deepseek_timeout),
                "--raw-candidate-limit",
                str(args.raw_candidate_limit),
                "--min-raw-candidates",
                str(args.min_raw_candidates),
                "--max-generated",
                str(args.max_generated),
            ]
        )
    try:
        agenda_code, agenda_output = run_subprocess(
            agenda_command,
            timeout=max(900, args.idea_timeout * 2 + args.deepseek_timeout + 300),
        )
    except Exception as exc:
        agenda_code, agenda_output = 1, str(exc)
    if agenda_code == 0:
        status_value = "skipped_no_focus_keys" if not focus_zotero_keys and args.idea_mode == "gemini-divergent" else "success"
        idea_generation = {"mode": "research_agenda_update", "status": status_value, "message": agenda_output[-1200:]}
    else:
        idea_generation = {"mode": "research_agenda_update", "status": "partial", "message": agenda_output[-1200:]}
        errors.append("research_agenda_update_failed")
    safe_write(
        idea_path,
        render_legacy_idea_pointer(
            run_date=run_date,
            agenda_delta_path=agenda_delta_path,
            focus_keys=focus_zotero_keys,
            agenda_status=idea_generation["status"],
        ),
        dry_run=False,
        backup=True,
    )
    safe_write(
        gemini_prompt_path,
        render_gemini_prompt(run_date=run_date, candidates_path=candidates_path, items=records[:12]),
        dry_run=False,
        backup=True,
    )
    idea_result = {"status": "not_applicable", "idea_count": 0, "errors": [], "warnings": []}
    blocking_errors = [error for error in errors if not error.startswith("arxiv_fetch_failed") and not error.startswith("arxiv_mirror_empty")]
    status = "success" if not blocking_errors else "partial"
    safe_write(backlog_path, render_reading_backlog(run_date=run_date, imports=imports, reads=reads), dry_run=False, backup=True)
    safe_write(
        run_log_path,
        render_run_log(
            run_date=run_date,
            status=status,
            ranked=ranked,
            imports=imports,
            reads=reads,
            idea_path=idea_path,
            agenda_delta_path=agenda_delta_path,
            gemini_prompt_path=gemini_prompt_path,
            idea_audit=idea_result,
            idea_generation=idea_generation,
            errors=errors,
            import_policy=import_policy,
            existing_candidates=existing_candidates,
        ),
        dry_run=False,
        backup=True,
    )
    safe_print(f"RUN_LOG: {run_log_path.relative_to(vault_path())}")
    safe_print(f"CANDIDATES: {candidates_path.relative_to(vault_path())}")
    safe_print(f"REVIEW_QUEUE: {review_path.relative_to(vault_path())}")
    safe_print(f"AGENDA_DELTA: {agenda_delta_path.relative_to(vault_path())}")
    safe_print(f"LEGACY_IDEA_POINTER: {idea_path.relative_to(vault_path())}")
    safe_print(f"GEMINI_PROMPT_PATH: {gemini_prompt_path.relative_to(vault_path())}")
    safe_print(f"AGENDA_UPDATE: {idea_generation['mode']}:{idea_generation['status']}")
    safe_print(f"LEGACY_IDEA_AUDIT: {idea_result['status']}")
    if errors:
        safe_print("PIPELINE_STATUS: partial")
        for error in errors:
            safe_print(f"ERROR: {error}")
        return 2
    safe_print("PIPELINE_STATUS: success")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="Run one daily scout pass.")
    parser.add_argument("--run-date", help="Override output date for manual historical reruns.")
    parser.add_argument("--dry-run", action="store_true", help="Fetch and rank only; do not write files or Zotero.")
    parser.add_argument("--query", action="append", help="Override default arXiv query; can be repeated.")
    parser.add_argument("--max-candidates", type=int, default=120)
    parser.add_argument("--source", choices=["mirror-first", "mirror-only", "search-api"], default="mirror-first")
    parser.add_argument("--days-back", type=int, default=60)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION_KEY)
    parser.add_argument("--min-new-imports", type=int, default=10, help="Minimum newly created Zotero items to attempt each run; existing duplicates do not count.")
    parser.add_argument("--max-auto-import", type=int, default=40, help="Maximum Zotero import attempts after local existing-paper prefiltering.")
    parser.add_argument("--fill-import-threshold", type=int, default=60, help="Minimum score for relevant below-review candidates used only to fill the daily new-import floor.")
    parser.add_argument("--fetch-timeout", type=int, default=DEFAULT_FETCH_TIMEOUT, help="Per-query arXiv API timeout in seconds.")
    parser.add_argument("--fetch-retries", type=int, default=DEFAULT_FETCH_RETRIES, help="Retries per arXiv query before recording a fetch warning.")
    parser.add_argument("--query-delay", type=float, default=DEFAULT_QUERY_DELAY, help="Delay between arXiv API queries to avoid rate-limit bursts.")
    parser.add_argument("--max-read", type=int, default=None, help="Maximum newly created imports to deep-read. Defaults to --min-new-imports so every new daily import is read.")
    parser.add_argument("--resume-backlog", action="store_true", help="Resume reading Zotero keys listed in the run-date reading backlog instead of importing new papers.")
    parser.add_argument("--skip-read", action="store_true", help="Import and ingest but do not invoke Claude reading.")
    parser.add_argument("--read-timeout", type=int, default=2700)
    parser.add_argument("--read-retries", type=int, default=1, help="Retry failed Claudian reads this many extra times before marking failed.")
    parser.add_argument("--read-retry-delay", type=int, default=90, help="Seconds to wait between failed Claudian read attempts.")
    parser.add_argument("--idea-mode", choices=["claude", "gemini-cli", "gemini-divergent", "template"], default="gemini-divergent", help="Use Claude Code or Gemini CLI to synthesize final ideas, or keep deterministic template ideas.")
    parser.add_argument("--idea-timeout", type=int, default=1200)
    parser.add_argument("--gemini-model", default="gemini-3.1-pro-preview")
    parser.add_argument("--deepseek-model", default="deepseek/deepseek-v4-pro(max)")
    parser.add_argument("--deepseek-timeout", type=int, default=1200)
    parser.add_argument("--raw-candidate-limit", type=int, default=8)
    parser.add_argument("--min-raw-candidates", type=int, default=6)
    parser.add_argument("--max-generated", type=int, default=3)
    args = parser.parse_args()
    if args.max_read is None:
        args.max_read = args.min_new_imports
    return run_pipeline(args)


if __name__ == "__main__":
    raise SystemExit(main())


