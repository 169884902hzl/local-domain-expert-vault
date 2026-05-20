"""Run v2 local/low-frequency novelty and baseline scan for final candidates."""
from __future__ import annotations

import argparse
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


def _classify(
    *,
    guard: dict[str, Any],
    nearest_works: list[dict[str, Any]],
    evidence_summary: dict[str, Any],
    remaining_delta: str,
    strict_external: bool,
) -> tuple[str, bool, str]:
    if guard.get("status") == "duplicate_blocked":
        return "duplicate", False, "duplicate_guard_blocked"
    if guard.get("status") == "possible_duplicate":
        if remaining_delta:
            return "partial_overlap", True, "duplicate_guard_possible_with_remaining_delta"
        return "unknown", False, "possible_duplicate_without_remaining_delta"
    scanned = sum(int(item.get("records_scanned", 0) or 0) for item in evidence_summary.values() if isinstance(item, dict))
    provider_errors = [item.get("error") for item in evidence_summary.values() if isinstance(item, dict) and item.get("error")]
    if strict_external or provider_errors or scanned < 10:
        return "unknown", False, "insufficient_local_or_external_evidence"
    if nearest_works:
        high_overlap = nearest_works[0].get("score", 0) >= 0.35
        if high_overlap:
            return ("partial_overlap", bool(remaining_delta), "near_match_requires_remaining_delta")
        return "likely_open", True, "nearest_works_low_overlap"
    return "likely_open", True, "no_near_match_after_local_scan"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--strict-external", action="store_true", help="Require external scan; local-only results become unknown.")
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
        nearest_works = sorted([*claim_nearest, *arxiv_nearest], key=lambda row: row["score"], reverse=True)[:8]
        remaining_delta = str(item.get("novelty_remaining_delta") or item.get("non_obvious_claim") or item.get("core_insight") or "")
        evidence_summary = {
            "local_notes_claim_graph": claim_summary,
            "local_arxiv_mirror": arxiv_summary,
        }
        classification, promotion_allowed, reason = _classify(
            guard=guard,
            nearest_works=nearest_works,
            evidence_summary=evidence_summary,
            remaining_delta=remaining_delta,
            strict_external=args.strict_external,
        )
        scans.append(
            {
                "candidate_id": cid,
                "candidate_title": item.get("title", ""),
                "status": "completed_local_only",
                "novelty_classification": classification,
                "novelty_remaining_delta": remaining_delta,
                "promotion_allowed": promotion_allowed,
                "classification_reason": reason,
                "nearest_works": nearest_works,
                "local_scan_evidence": evidence_summary,
                "no_near_match_evidence": evidence_summary if classification == "likely_open" and not nearest_works else {},
                "duplicate_guard": guard,
                "providers_used": ["local_arxiv_mirror", "local_notes_claim_graph", "local_seed_like_dirs"],
                "requires_human_unknown_override": classification == "unknown",
                "final_candidate_id": cid,
            }
        )
    payload = {
        "schema_version": "novelty_scan.v1",
        "run_date": args.run_date,
        "status": "completed_local_only" if scans else "partial_empty_selection",
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
