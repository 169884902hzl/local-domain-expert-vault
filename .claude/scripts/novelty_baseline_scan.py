"""Run v2 local/low-frequency novelty and baseline scan for final candidates."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from kb_common import safe_print
from arxiv_metadata_sync import DEFAULT_DB as ARXIV_METADATA_DB, connect_readonly
from research_seed_v2_common import (
    agenda_v2_path,
    artifact_dir,
    artifact_hashes,
    candidate_id,
    duplicate_guard,
    ensure_v2_dirs,
    load_jsonl,
    normalize_text,
    read_json,
    write_run_artifact,
)


PROVIDER_POLICY = {
    "local_arxiv_mirror": {"mode": "always"},
    "local_notes_claim_graph": {"mode": "always"},
    "arxiv_api": {"mode": "promotion_only", "delay_sec": 3.2, "max_queries_per_candidate": 5, "requires_cache": True},
    "openalex": {"mode": "promotion_or_strict", "delay_sec": 0.25, "requires_cache": True},
    "semantic_scholar": {"mode": "optional_with_api_key", "delay_sec": 1.0, "requires_cache": True},
    "web_search": {"mode": "strict_only", "max_queries_per_candidate": 2},
}
ARXIV_API = "https://export.arxiv.org/api/query"
OPENALEX_API = "https://api.openalex.org/works"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_ONLY_RISK = "external_scope_arxiv_only_not_full_prior_art"
BROAD_EXTERNAL_PROVIDERS = {"openalex", "semantic_scholar"}
FORMAL_VERIFICATION_SCOPES = {"local_plus_s2_or_openalex", "strict_multi_provider"}
NOVELTY_CACHE_TTL_DAYS = 14
_RATE_LIMIT_LAST: dict[str, float] = {}


def _final_candidates(selected: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated_parent_ids = {str(item.get("parent_candidate_id")) for item in mutations}
    finals = [dict(item) for item in selected if candidate_id(item) not in mutated_parent_ids]
    finals.extend(dict(item) for item in mutations)
    return finals


def _candidate_text(item: dict[str, Any]) -> str:
    return normalize_text(
        " ".join(
            str(item.get(key, ""))
            for key in ["title", "problem", "mechanism", "interface_boundary", "strongest_baseline", "novelty_remaining_delta"]
        )
    )


def _token_set(text: str) -> set[str]:
    return {token for token in normalize_text(text).split() if len(token) >= 4}


def _overlap_score(a: str, b: str) -> float:
    left = _token_set(a)
    right = _token_set(b)
    if not left or not right:
        return 0.0
    return len(left & right) / max(1, min(len(left), len(right)))


def _cache_root() -> Path:
    return agenda_v2_path("cache", "external-novelty")


def _cache_file(provider: str, url: str) -> Path:
    digest = hashlib.sha256(f"{provider}\n{url}".encode("utf-8")).hexdigest()
    return _cache_root() / provider / f"{digest}.json"


def _cache_rel(path: Path) -> str:
    try:
        return str(path.relative_to(agenda_v2_path())).replace("\\", "/")
    except ValueError:
        return path.name


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def _iso(value: datetime) -> str:
    return value.isoformat()


def _query_hash(query: str) -> str:
    return hashlib.sha256(query.encode("utf-8")).hexdigest()


def _rate_limit(provider: str, delay_sec: float) -> None:
    delay_sec = max(0.0, delay_sec)
    if delay_sec <= 0:
        return
    now = time.monotonic()
    last = _RATE_LIMIT_LAST.get(provider)
    if last is not None:
        wait = delay_sec - (now - last)
        if wait > 0:
            time.sleep(wait)
    _RATE_LIMIT_LAST[provider] = time.monotonic()


def _fetch_url_cached(
    provider: str,
    url: str,
    *,
    timeout: int,
    delay_sec: float,
    headers: dict[str, str] | None = None,
    response_type: str = "json",
    query: str = "",
    ttl_days: int = NOVELTY_CACHE_TTL_DAYS,
) -> tuple[Any, dict[str, Any]]:
    cache_path = _cache_file(provider, url)
    now = _utc_now()
    expires_at = now + timedelta(days=ttl_days)
    summary: dict[str, Any] = {
        "provider": provider,
        "status": "provider_unavailable",
        "cached": False,
        "cache_status": "missing",
        "cache_key": cache_path.stem,
        "cache_path": _cache_rel(cache_path),
        "query": query or url,
        "query_hash": _query_hash(query or url),
        "created_at": "",
        "expires_at": "",
        "ttl_days": ttl_days,
        "records_scanned": 0,
        "result_count": 0,
        "rate_limit_observed": "",
        "timeout_sec": timeout,
        "rate_limit_delay_sec": delay_sec,
    }
    if cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text(encoding="utf-8-sig"))
            summary["status"] = "success"
            summary["cached"] = True
            summary["created_at"] = str(cached.get("created_at") or cached.get("cached_at") or "")
            summary["expires_at"] = str(cached.get("expires_at") or "")
            summary["result_count"] = int(cached.get("result_count", 0) or 0)
            expired = False
            if cached.get("expires_at"):
                try:
                    expired = datetime.fromisoformat(str(cached["expires_at"])) <= now
                except ValueError:
                    expired = True
            elif cached.get("cached_at_unix"):
                expired = int(time.time()) - int(cached["cached_at_unix"]) > ttl_days * 86400
            if expired:
                summary["cache_status"] = "stale"
            else:
                summary["cache_status"] = "fresh"
            return cached.get("payload"), summary
        except Exception as exc:
            summary["cache_error"] = f"{type(exc).__name__}:{exc}"
    _rate_limit(provider, delay_sec)
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        summary["status"] = "rate_limited" if exc.code == 429 else "provider_unavailable"
        summary["rate_limit_observed"] = str(exc.code)
        summary["error"] = f"{type(exc).__name__}:{exc}"
        return None, summary
    except TimeoutError as exc:
        summary["status"] = "timeout"
        summary["error"] = f"{type(exc).__name__}:{exc}"
        return None, summary
    except Exception as exc:
        summary["error"] = f"{type(exc).__name__}:{exc}"
        return None, summary
    try:
        payload = json.loads(raw) if response_type == "json" else raw
    except Exception as exc:
        summary["status"] = "invalid_response"
        summary["error"] = f"invalid_{response_type}:{type(exc).__name__}:{exc}"
        return None, summary
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(
            json.dumps(
                {
                    "provider": provider,
                    "created_at": _iso(now),
                    "expires_at": _iso(expires_at),
                    "ttl_days": ttl_days,
                    "query": query or url,
                    "query_hash": _query_hash(query or url),
                    "result_count": len(payload.get("results", payload.get("data", []))) if isinstance(payload, dict) else 0,
                    "cached_at_unix": int(time.time()),
                    "url_sha256": hashlib.sha256(url.encode("utf-8")).hexdigest(),
                    "response_type": response_type,
                    "payload": payload,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        summary["cache_write_error"] = f"{type(exc).__name__}:{exc}"
    summary["status"] = "success"
    summary["cache_status"] = "fresh"
    summary["created_at"] = _iso(now)
    summary["expires_at"] = _iso(expires_at)
    return payload, summary


def _external_text_queries(item: dict[str, Any], max_queries: int) -> list[str]:
    title = str(item.get("title") or "").strip()
    mechanism = str(
        item.get("mechanism")
        or item.get("core_insight")
        or item.get("novelty_remaining_delta")
        or item.get("strongest_baseline")
        or ""
    ).strip()
    queries: list[str] = []
    if title:
        queries.append(title[:180])
    tokens = [token for token in _token_set(mechanism) if token not in {"with", "from", "that", "this", "under"}]
    if tokens:
        queries.append(" ".join(sorted(tokens, key=len, reverse=True)[:7]))
    return queries[: max(0, max_queries)]


def _provider_error(provider: str, summary: dict[str, Any]) -> dict[str, str] | None:
    if summary.get("status") == "success" and not summary.get("error"):
        return None
    error = str(summary.get("error") or summary.get("status") or "provider_unavailable")
    return {"provider": provider, "status": str(summary.get("status") or "provider_unavailable"), "error": error}


def _has_broad_external_provider(providers: list[str]) -> bool:
    return bool(BROAD_EXTERNAL_PROVIDERS & set(providers))


def _normalized_work(
    *,
    source: str,
    score: float,
    title: str,
    work_id: str = "",
    year: Any = None,
    url: str = "",
    abstract: str = "",
    authors: list[str] | None = None,
    venue: str = "",
    evidence: str = "",
) -> dict[str, Any]:
    evidence_text = evidence or abstract[:360]
    return {
        "source": source,
        "score": score,
        "work_id": work_id,
        "title": title,
        "year": year,
        "url": url,
        "abstract": abstract,
        "authors": authors or [],
        "venue": venue,
        "overlap_score": score,
        "overlap_type": "same_problem" if score >= 0.35 else "adjacent",
        "what_is_already_done": evidence_text,
        "remaining_delta": "",
        "locator": work_id,
        "evidence": evidence_text,
    }


def _verification_scope(external_providers_used: list[str]) -> str:
    providers = set(external_providers_used)
    broad = providers & BROAD_EXTERNAL_PROVIDERS
    if broad and len(providers) >= 2:
        return "strict_multi_provider"
    if broad:
        return "local_plus_s2_or_openalex"
    if "arxiv_api" in providers:
        return "local_plus_arxiv_api"
    return "local_only"


def _strongest_baseline(item: dict[str, Any], nearest_works: list[dict[str, Any]]) -> dict[str, Any]:
    if nearest_works:
        top = nearest_works[0]
        return {
            "source": str(top.get("source", "")),
            "score": top.get("score", 0),
            "title": str(top.get("title", "")),
            "locator": str(top.get("locator", "")),
            "evidence": str(top.get("evidence", ""))[:360],
        }
    return {
        "source": "candidate_field",
        "score": 0,
        "title": str(item.get("strongest_baseline") or item.get("baselines") or ""),
        "locator": "",
        "evidence": "",
    }


def _scan_claim_graph(item: dict[str, Any], limit: int = 5) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    query = _candidate_text(item)
    path = agenda_v2_path("evidence", "research_claim_graph.jsonl")
    records = [
        record
        for record in (load_jsonl(path) if path.exists() else [])
        if record.get("record_type", "node") == "node"
    ]
    scored: list[dict[str, Any]] = []
    for record in records:
        text = " ".join(str(record.get(key, "")) for key in ["source_title", "claim_type", "statement"])
        score = _overlap_score(query, text)
        if score >= 0.18:
            scored.append(
                {
                    "source": "local_notes_claim_graph",
                    "score": round(score, 3),
                    "title": str(record.get("source_title", "")),
                    "locator": str(record.get("node_id") or record.get("source_note") or ""),
                    "evidence": str(record.get("statement", ""))[:360],
                }
            )
    return sorted(scored, key=lambda row: row["score"], reverse=True)[:limit], {"records_scanned": len(records), "path": str(path)}


def _scan_arxiv_mirror(item: dict[str, Any], limit: int = 5) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    query = _candidate_text(item)
    if not ARXIV_METADATA_DB.exists():
        return [], {"records_scanned": 0, "path": str(ARXIV_METADATA_DB), "error": "arxiv_metadata_mirror_missing"}
    scored: list[dict[str, Any]] = []
    scanned = 0
    try:
        conn = connect_readonly(ARXIV_METADATA_DB)
        try:
            tokens = sorted(_token_set(query), key=len, reverse=True)[:8]
            clauses = " OR ".join(["lower(title || ' ' || summary) LIKE ?" for _ in tokens]) or "1=1"
            params = [f"%{token.lower()}%" for token in tokens]
            rows = conn.execute(
                f"SELECT arxiv_id,title,summary,updated FROM papers WHERE {clauses} ORDER BY updated DESC LIMIT 400",
                params,
            ).fetchall()
            scanned = len(rows)
            for row in rows:
                text = f"{row['title']} {row['summary']}"
                score = _overlap_score(query, text)
                if score >= 0.18:
                    scored.append(
                        {
                            "source": "local_arxiv_mirror",
                            "score": round(score, 3),
                            "title": str(row["title"]),
                            "locator": str(row["arxiv_id"]),
                            "evidence": str(row["summary"])[:360],
                        }
                    )
        finally:
            conn.close()
    except Exception as exc:
        return [], {"records_scanned": scanned, "path": str(ARXIV_METADATA_DB), "error": f"{type(exc).__name__}:{exc}"}
    return sorted(scored, key=lambda row: row["score"], reverse=True)[:limit], {"records_scanned": scanned, "path": str(ARXIV_METADATA_DB)}


def _entry_text(entry: ET.Element, name: str) -> str:
    node = entry.find(f"atom:{name}", ATOM)
    return "" if node is None or node.text is None else " ".join(node.text.split())


def _arxiv_api_queries(item: dict[str, Any], max_queries: int) -> list[str]:
    title = str(item.get("title") or "").strip()
    mechanism = str(item.get("mechanism") or item.get("core_insight") or item.get("novelty_remaining_delta") or "").strip()
    queries: list[str] = []
    if title:
        queries.append(f'ti:"{title[:120]}"')
    tokens = [token for token in _token_set(mechanism) if token not in {"with", "from", "that", "this", "under"}]
    if tokens:
        terms = " OR ".join(f'all:{token}' for token in sorted(tokens, key=len, reverse=True)[:4])
        queries.append(terms)
    return queries[: max(0, max_queries)]


def _scan_arxiv_api(item: dict[str, Any], *, max_queries: int, timeout: int, delay_sec: float = 3.2, limit: int = 5) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    query_text = _candidate_text(item)
    queries = _arxiv_api_queries(item, max_queries)
    if not queries:
        return [], {"records_scanned": 0, "provider": "arxiv_api", "status": "provider_unavailable", "cached": False, "error": "arxiv_api_no_query_terms"}
    scored: list[dict[str, Any]] = []
    scanned = 0
    errors: list[str] = []
    cached = False
    cache_statuses: list[str] = []
    for index, query in enumerate(queries):
        params = urllib.parse.urlencode({"search_query": query, "start": 0, "max_results": 5})
        raw, request_summary = _fetch_url_cached(
            "arxiv_api",
            f"{ARXIV_API}?{params}",
            timeout=timeout,
            delay_sec=delay_sec if index else 0.0,
            response_type="text",
            query=query,
        )
        cached = cached or bool(request_summary.get("cached"))
        cache_statuses.append(str(request_summary.get("cache_status") or "missing"))
        if request_summary.get("error") or not isinstance(raw, str):
            errors.append(str(request_summary.get("error") or "arxiv_api_empty_response"))
            break
        try:
            root = ET.fromstring(raw)
        except Exception as exc:
            errors.append(f"{type(exc).__name__}:{exc}")
            break
        rows = root.findall("atom:entry", ATOM)
        scanned += len(rows)
        for row in rows:
            title = _entry_text(row, "title")
            summary = _entry_text(row, "summary")
            score = _overlap_score(query_text, f"{title} {summary}")
            if score >= 0.18:
                scored.append(
                    _normalized_work(
                        source="arxiv_api",
                        score=round(score, 3),
                        title=title,
                        work_id=_entry_text(row, "id").rstrip("/").split("/")[-1],
                        url=_entry_text(row, "id"),
                        abstract=summary,
                        evidence=summary[:360],
                    )
                )
    summary: dict[str, Any] = {
        "records_scanned": scanned,
        "provider": "arxiv_api",
        "status": "success" if not errors else "provider_unavailable",
        "cached": cached,
        "cache_status": "stale" if "stale" in cache_statuses else ("fresh" if "fresh" in cache_statuses else "missing"),
        "queries": len(queries),
        "result_count": len(scored),
    }
    if errors:
        summary["error"] = ";".join(errors)
    return sorted(scored, key=lambda row: row["score"], reverse=True)[:limit], summary


def _openalex_abstract(work: dict[str, Any]) -> str:
    inverted = work.get("abstract_inverted_index")
    if not isinstance(inverted, dict):
        return ""
    positions: dict[int, str] = {}
    for word, indexes in inverted.items():
        if not isinstance(indexes, list):
            continue
        for index in indexes:
            if isinstance(index, int):
                positions[index] = str(word)
    return " ".join(positions[index] for index in sorted(positions))


def _scan_openalex(item: dict[str, Any], *, max_queries: int, timeout: int, delay_sec: float = 0.25, limit: int = 5) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    query_text = _candidate_text(item)
    queries = _external_text_queries(item, max_queries)
    if not queries:
        return [], {"records_scanned": 0, "provider": "openalex", "status": "provider_unavailable", "cached": False, "error": "openalex_no_query_terms"}
    scored: list[dict[str, Any]] = []
    scanned = 0
    errors: list[str] = []
    cached = False
    cache_statuses: list[str] = []
    for query in queries:
        params = {"search": query, "per-page": 5}
        mailto = os.environ.get("OPENALEX_MAILTO", "").strip()
        if mailto:
            params["mailto"] = mailto
        url = f"{OPENALEX_API}?{urllib.parse.urlencode(params)}"
        payload, request_summary = _fetch_url_cached("openalex", url, timeout=timeout, delay_sec=delay_sec, query=query)
        cached = cached or bool(request_summary.get("cached"))
        cache_statuses.append(str(request_summary.get("cache_status") or "missing"))
        if request_summary.get("error") or not isinstance(payload, dict):
            errors.append(str(request_summary.get("error") or "openalex_empty_response"))
            continue
        rows = payload.get("results", [])
        if not isinstance(rows, list):
            errors.append("openalex_results_not_array")
            continue
        scanned += len(rows)
        for row in rows:
            if not isinstance(row, dict):
                continue
            title = str(row.get("display_name") or row.get("title") or "")
            abstract = _openalex_abstract(row)
            score = _overlap_score(query_text, f"{title} {abstract}")
            if score >= 0.18:
                scored.append(
                    _normalized_work(
                        source="openalex",
                        score=round(score, 3),
                        title=title,
                        work_id=str(row.get("doi") or row.get("id") or ""),
                        year=row.get("publication_year"),
                        url=str(row.get("id") or ""),
                        abstract=abstract,
                        authors=[str(author.get("author", {}).get("display_name", "")) for author in row.get("authorships", []) if isinstance(author, dict)],
                        venue=str((row.get("primary_location") or {}).get("source", {}).get("display_name", "")) if isinstance(row.get("primary_location"), dict) else "",
                        evidence=(abstract or str(row.get("publication_year") or ""))[:360],
                    )
                )
    summary: dict[str, Any] = {
        "records_scanned": scanned,
        "provider": "openalex",
        "status": "success" if scanned or not errors else "provider_unavailable",
        "cached": cached,
        "cache_status": "stale" if "stale" in cache_statuses else ("fresh" if "fresh" in cache_statuses else "missing"),
        "queries": len(queries),
        "result_count": len(scored),
    }
    if errors and not scanned:
        summary["error"] = ";".join(errors)
    elif errors:
        summary["warnings"] = errors
    return sorted(scored, key=lambda row: row["score"], reverse=True)[:limit], summary


def _semantic_scholar_api_key() -> str:
    return os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip() or os.environ.get("S2_API_KEY", "").strip()


def _scan_semantic_scholar(
    item: dict[str, Any],
    *,
    max_queries: int,
    timeout: int,
    api_key: str,
    delay_sec: float = 1.0,
    limit: int = 5,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not api_key:
        return [], {
            "records_scanned": 0,
            "provider": "semantic_scholar",
            "status": "provider_unavailable",
            "cached": False,
            "error": "semantic_scholar_api_key_missing",
        }
    query_text = _candidate_text(item)
    queries = _external_text_queries(item, max_queries)
    if not queries:
        return [], {"records_scanned": 0, "provider": "semantic_scholar", "status": "provider_unavailable", "cached": False, "error": "semantic_scholar_no_query_terms"}
    scored: list[dict[str, Any]] = []
    scanned = 0
    errors: list[str] = []
    cached = False
    cache_statuses: list[str] = []
    fields = "title,abstract,url,year,venue,authors,externalIds"
    headers = {"x-api-key": api_key}
    for query in queries:
        params = urllib.parse.urlencode({"query": query, "limit": 5, "fields": fields})
        payload, request_summary = _fetch_url_cached(
            "semantic_scholar",
            f"{SEMANTIC_SCHOLAR_API}?{params}",
            timeout=timeout,
            delay_sec=delay_sec,
            headers=headers,
            query=query,
        )
        cached = cached or bool(request_summary.get("cached"))
        cache_statuses.append(str(request_summary.get("cache_status") or "missing"))
        if request_summary.get("error") or not isinstance(payload, dict):
            errors.append(str(request_summary.get("error") or "semantic_scholar_empty_response"))
            continue
        rows = payload.get("data", [])
        if not isinstance(rows, list):
            errors.append("semantic_scholar_data_not_array")
            continue
        scanned += len(rows)
        for row in rows:
            if not isinstance(row, dict):
                continue
            title = str(row.get("title") or "")
            abstract = str(row.get("abstract") or "")
            score = _overlap_score(query_text, f"{title} {abstract}")
            if score >= 0.18:
                scored.append(
                    _normalized_work(
                        source="semantic_scholar",
                        score=round(score, 3),
                        title=title,
                        work_id=str(row.get("paperId") or row.get("url") or ""),
                        year=row.get("year"),
                        url=str(row.get("url") or ""),
                        abstract=abstract,
                        authors=[str(author.get("name", "")) for author in row.get("authors", []) if isinstance(author, dict)],
                        venue=str(row.get("venue") or ""),
                        evidence=abstract[:360],
                    )
                )
    summary = {
        "records_scanned": scanned,
        "provider": "semantic_scholar",
        "status": "success" if scanned or not errors else "provider_unavailable",
        "cached": cached,
        "cache_status": "stale" if "stale" in cache_statuses else ("fresh" if "fresh" in cache_statuses else "missing"),
        "queries": len(queries),
        "api_key_present": True,
        "result_count": len(scored),
    }
    if errors and not scanned:
        summary["error"] = ";".join(errors)
    elif errors:
        summary["warnings"] = errors
    return sorted(scored, key=lambda row: row["score"], reverse=True)[:limit], summary


def _classify(
    *,
    guard: dict[str, Any],
    nearest_works: list[dict[str, Any]],
    evidence_summary: dict[str, Any],
    remaining_delta: str,
    strict_external: bool,
    external_completed: bool = False,
) -> tuple[str, bool, str]:
    if guard.get("status") == "duplicate_blocked":
        return "duplicate", False, "duplicate_guard_blocked"
    if guard.get("status") == "possible_duplicate":
        if remaining_delta:
            return "partial_overlap", True, "duplicate_guard_possible_with_remaining_delta"
        return "unknown", False, "possible_duplicate_without_remaining_delta"
    scanned = sum(int(item.get("records_scanned", 0) or 0) for item in evidence_summary.values() if isinstance(item, dict))
    provider_errors = [item.get("error") for item in evidence_summary.values() if isinstance(item, dict) and item.get("error")]
    if strict_external and not external_completed:
        return "unknown", False, "external_verification_unavailable"
    if provider_errors and not external_completed:
        return "unknown", False, "insufficient_local_or_external_evidence"
    if not external_completed and scanned < 10:
        return "unknown", False, "insufficient_local_or_external_evidence"
    if nearest_works:
        high_overlap = nearest_works[0].get("score", 0) >= 0.35
        if high_overlap:
            return ("partial_overlap", bool(remaining_delta), "near_match_requires_remaining_delta")
        return "likely_open", True, "nearest_works_low_overlap"
    return "likely_open", True, "no_near_match_after_external_scan" if external_completed else "no_near_match_after_local_scan"


def _build_candidate_scan(
    item: dict[str, Any],
    *,
    target_policy: str,
    strict_external: bool,
    max_external_queries: int,
    external_timeout: int,
    semantic_scholar_mode: str = "auto",
) -> dict[str, Any]:
    cid = candidate_id(item)
    guard = duplicate_guard(item)
    claim_nearest, claim_summary = _scan_claim_graph(item)
    arxiv_nearest, arxiv_summary = _scan_arxiv_mirror(item)
    external_nearest: list[dict[str, Any]] = []
    provider_results: dict[str, Any] = {}
    provider_errors: list[dict[str, str]] = []
    external_providers_used: list[str] = []
    should_run_external = target_policy == "formal" or strict_external
    if should_run_external:
        external_scans: list[tuple[str, list[dict[str, Any]], dict[str, Any]]] = []
        external_scans.append(
            (
                "arxiv_api",
                *_scan_arxiv_api(
                    item,
                    max_queries=max_external_queries,
                    timeout=external_timeout,
                ),
            )
        )
        external_scans.append(
            (
                "openalex",
                *_scan_openalex(
                    item,
                    max_queries=max_external_queries,
                    timeout=external_timeout,
                ),
            )
        )
        if semantic_scholar_mode != "never":
            external_scans.append(
                (
                    "semantic_scholar",
                    *_scan_semantic_scholar(
                        item,
                        max_queries=max_external_queries,
                        timeout=external_timeout,
                        api_key=_semantic_scholar_api_key(),
                    ),
                )
            )
        for provider, nearest, summary in external_scans:
            provider_results[provider] = summary
            if summary.get("status") == "success" and not summary.get("error"):
                external_nearest.extend(nearest)
                if summary.get("cache_status") != "stale":
                    external_providers_used.append(provider)
            error = _provider_error(provider, summary)
            if error:
                provider_errors.append(error)
    nearest_works = sorted([*claim_nearest, *arxiv_nearest, *external_nearest], key=lambda row: row["score"], reverse=True)[:8]
    remaining_delta = str(item.get("novelty_remaining_delta") or item.get("non_obvious_claim") or item.get("core_insight") or "")
    local_scan_evidence = {
        "local_notes_claim_graph": claim_summary,
        "local_arxiv_mirror": arxiv_summary,
    }
    evidence_summary = {**local_scan_evidence, **provider_results}
    external_completed = bool(external_providers_used)
    classification, promotion_allowed, reason = _classify(
        guard=guard,
        nearest_works=nearest_works,
        evidence_summary=evidence_summary,
        remaining_delta=remaining_delta,
        strict_external=strict_external or target_policy == "formal",
        external_completed=external_completed,
    )
    verification_scope = _verification_scope(external_providers_used)
    formal_promotion_allowed = (
        promotion_allowed
        and verification_scope in FORMAL_VERIFICATION_SCOPES
        and _has_broad_external_provider(external_providers_used)
        and classification in {"likely_open", "partial_overlap"}
    )
    formal_publish_risk = ARXIV_ONLY_RISK if verification_scope == "local_plus_arxiv_api" else ""
    stale_external_novelty_cache = any(
        isinstance(item, dict) and item.get("cache_status") == "stale"
        for provider, item in provider_results.items()
        if provider in BROAD_EXTERNAL_PROVIDERS
    )
    provider_health_summary = {
        provider: {
            "status": summary.get("status"),
            "cache_status": summary.get("cache_status", "missing"),
            "result_count": summary.get("result_count", summary.get("records_scanned", 0)),
        }
        for provider, summary in provider_results.items()
        if isinstance(summary, dict)
    }
    if stale_external_novelty_cache:
        formal_publish_risk = ";".join(filter(None, [formal_publish_risk, "stale_external_novelty_cache"]))
    return {
        "candidate_id": cid,
        "candidate_title": item.get("title", ""),
        "status": "completed" if external_completed else "completed_local_only",
        "novelty_classification": classification,
        "novelty_remaining_delta": remaining_delta,
        "promotion_allowed": promotion_allowed,
        "formal_promotion_allowed": formal_promotion_allowed,
        "verification_scope": verification_scope,
        "external_providers_used": external_providers_used,
        "provider_results": provider_results,
        "provider_errors": provider_errors,
        "provider_health_summary": provider_health_summary,
        "stale_external_novelty_cache": stale_external_novelty_cache,
        "formal_publish_risk": formal_publish_risk,
        "classification_reason": reason,
        "nearest_works": nearest_works,
        "strongest_baseline": _strongest_baseline(item, nearest_works),
        "local_scan_evidence": local_scan_evidence,
        "external_scan_evidence": provider_results,
        "no_near_match_evidence": evidence_summary if classification == "likely_open" and not nearest_works else {},
        "duplicate_guard": guard,
        "providers_used": ["local_arxiv_mirror", "local_notes_claim_graph", "local_seed_like_dirs", *external_providers_used],
        "requires_human_unknown_override": classification == "unknown",
        "final_candidate_id": cid,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--target-policy", choices=["disabled", "seed-candidates-only", "formal"], default="seed-candidates-only")
    parser.add_argument("--strict-external", action="store_true", help="Require external scan; local-only results become unknown.")
    parser.add_argument("--max-external-queries", type=int, default=1)
    parser.add_argument("--external-timeout", type=int, default=12)
    parser.add_argument("--semantic-scholar-mode", choices=["auto", "never"], default="auto")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    selected = read_json(artifact_dir(args.run_date) / "selected-candidates.json").get("selected", [])
    mutations_path = artifact_dir(args.run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    scans: list[dict[str, Any]] = []
    for item in _final_candidates(selected, mutations):
        scans.append(
            _build_candidate_scan(
                item,
                target_policy=args.target_policy,
                strict_external=args.strict_external,
                max_external_queries=args.max_external_queries,
                external_timeout=args.external_timeout,
                semantic_scholar_mode=args.semantic_scholar_mode,
            )
        )
    payload_status = "partial_empty_selection"
    if scans:
        payload_status = "completed" if any(item.get("verification_scope") != "local_only" for item in scans) else "completed_local_only"
    payload = {
        "schema_version": "novelty_scan.v1",
        "run_date": args.run_date,
        "status": payload_status,
        "scans": scans,
        "provider_policy": PROVIDER_POLICY,
        "artifact_hashes": artifact_hashes(args.run_date, ["selected-candidates.json", "gemini-mutations.json"]),
        "boundary": "Unknown novelty cannot auto-promote; human override may only record accepted novelty risk and cannot bypass fatal flaws.",
    }
    write_run_artifact(args.run_date, "novelty-scan.json", payload, state="novelty_checked", dry_run=args.dry_run)
    safe_print(f"NOVELTY_SCAN: status={payload['status']} scans={len(scans)}")
    return 0 if scans else 2


if __name__ == "__main__":
    raise SystemExit(main())
