"""Run v2 local/low-frequency novelty and baseline scan for final candidates."""
from __future__ import annotations

import argparse
import time
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
    "arxiv_api": {"mode": "promotion_only", "delay_sec": 3.2, "max_queries_per_candidate": 5},
    "semantic_scholar": {"mode": "promotion_only", "max_rps": 1, "requires_cache": True},
    "openalex": {"mode": "fallback_or_strict", "requires_cache": True},
    "web_search": {"mode": "strict_only", "max_queries_per_candidate": 2},
}
ARXIV_API = "https://export.arxiv.org/api/query"
ATOM = {"atom": "http://www.w3.org/2005/Atom"}
FORMAL_VERIFICATION_SCOPES = {"local_plus_arxiv_api", "local_plus_s2_or_openalex", "strict_multi_provider"}


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


def _scan_claim_graph(item: dict[str, Any], limit: int = 5) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    query = _candidate_text(item)
    path = agenda_v2_path("evidence", "research_claim_graph.jsonl")
    records = load_jsonl(path) if path.exists() else []
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
        return [], {"records_scanned": 0, "provider": "arxiv_api", "error": "arxiv_api_no_query_terms"}
    scored: list[dict[str, Any]] = []
    scanned = 0
    errors: list[str] = []
    for index, query in enumerate(queries):
        if index:
            time.sleep(max(0.0, delay_sec))
        params = urllib.parse.urlencode({"search_query": query, "start": 0, "max_results": 5})
        try:
            with urllib.request.urlopen(f"{ARXIV_API}?{params}", timeout=timeout) as response:
                root = ET.fromstring(response.read())
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
                    {
                        "source": "arxiv_api",
                        "score": round(score, 3),
                        "title": title,
                        "locator": _entry_text(row, "id").rstrip("/").split("/")[-1],
                        "evidence": summary[:360],
                    }
                )
    summary: dict[str, Any] = {"records_scanned": scanned, "provider": "arxiv_api", "queries": len(queries)}
    if errors:
        summary["error"] = ";".join(errors)
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--target-policy", choices=["disabled", "seed-candidates-only", "formal"], default="seed-candidates-only")
    parser.add_argument("--strict-external", action="store_true", help="Require external scan; local-only results become unknown.")
    parser.add_argument("--max-external-queries", type=int, default=1)
    parser.add_argument("--external-timeout", type=int, default=12)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    selected = read_json(artifact_dir(args.run_date) / "selected-candidates.json").get("selected", [])
    mutations_path = artifact_dir(args.run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    scans: list[dict[str, Any]] = []
    for item in _final_candidates(selected, mutations):
        cid = candidate_id(item)
        guard = duplicate_guard(item)
        claim_nearest, claim_summary = _scan_claim_graph(item)
        arxiv_nearest, arxiv_summary = _scan_arxiv_mirror(item)
        external_nearest: list[dict[str, Any]] = []
        external_summary: dict[str, Any] = {}
        external_providers_used: list[str] = []
        if args.target_policy == "formal" or args.strict_external:
            external_nearest, external_summary = _scan_arxiv_api(
                item,
                max_queries=args.max_external_queries,
                timeout=args.external_timeout,
            )
            if not external_summary.get("error"):
                external_providers_used.append("arxiv_api")
        nearest_works = sorted([*claim_nearest, *arxiv_nearest, *external_nearest], key=lambda row: row["score"], reverse=True)[:8]
        remaining_delta = str(item.get("novelty_remaining_delta") or item.get("non_obvious_claim") or item.get("core_insight") or "")
        evidence_summary = {
            "local_notes_claim_graph": claim_summary,
            "local_arxiv_mirror": arxiv_summary,
        }
        external_completed = bool(external_providers_used)
        classification, promotion_allowed, reason = _classify(
            guard=guard,
            nearest_works=nearest_works,
            evidence_summary=evidence_summary,
            remaining_delta=remaining_delta,
            strict_external=args.strict_external or args.target_policy == "formal",
            external_completed=external_completed,
        )
        verification_scope = "local_plus_arxiv_api" if external_completed else "local_only"
        formal_promotion_allowed = (
            promotion_allowed
            and verification_scope in FORMAL_VERIFICATION_SCOPES
            and bool(external_providers_used)
            and classification in {"likely_open", "partial_overlap"}
        )
        formal_publish_risk = "external_scope_arxiv_only_not_full_prior_art" if verification_scope == "local_plus_arxiv_api" else ""
        scans.append(
            {
                "candidate_id": cid,
                "candidate_title": item.get("title", ""),
                "status": "completed" if external_completed else "completed_local_only",
                "novelty_classification": classification,
                "novelty_remaining_delta": remaining_delta,
                "promotion_allowed": promotion_allowed,
                "formal_promotion_allowed": formal_promotion_allowed,
                "verification_scope": verification_scope,
                "external_providers_used": external_providers_used,
                "formal_publish_risk": formal_publish_risk,
                "classification_reason": reason,
                "nearest_works": nearest_works,
                "local_scan_evidence": evidence_summary,
                "external_scan_evidence": {"arxiv_api": external_summary} if external_summary else {},
                "no_near_match_evidence": evidence_summary if classification == "likely_open" and not nearest_works else {},
                "duplicate_guard": guard,
                "providers_used": ["local_arxiv_mirror", "local_notes_claim_graph", "local_seed_like_dirs", *external_providers_used],
                "requires_human_unknown_override": classification == "unknown",
                "final_candidate_id": cid,
            }
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
