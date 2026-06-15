"""Run a real external novelty screen for one candidate and package it as a v1 artifact.

Reuses the external retrieval clients in novelty_baseline_scan (_build_candidate_scan
with target_policy="formal") to actually query arXiv / OpenAlex / Semantic Scholar for a
single candidate, then maps the scan into the governance novelty_screen.v1 artifact.
Honest status machine -- screen_status is "success" only when an external provider really
returned without error; timeouts / unavailability fall to the true failure enum. This is a
screening input only and never replaces the human manual prior-art dossier.
"""
from __future__ import annotations

import argparse
import json

from novelty_baseline_scan import _build_candidate_scan
from research_governance_common import (
    candidate_dir,
    novelty_screen_dir,
    read_json,
    validate_governance_payload,
    write_json,
)

_BOUNDARY = "External novelty screening input only; does not replace the human manual prior-art dossier."


def _flatten(err) -> str:
    if isinstance(err, dict):
        provider = str(err.get("provider") or err.get("source") or "")
        message = str(err.get("error") or err.get("message") or err.get("status") or "")
        return f"{provider}:{message}".strip(":") or "provider_error"
    return str(err)


def _screen(cid: str, *, screen_status: str, api_status: str, provider_errors: list, stale: bool, metadata: dict) -> dict:
    return {
        "schema_version": "novelty_screen.v1",
        "candidate_id": cid,
        "screen_status": screen_status,
        "screening_only": True,
        "stale": bool(stale),
        "stale_external_novelty_cache": bool(stale),
        "replaces_manual_prior_art_dossier": False,
        "api_provider_status": api_status,
        "provider_errors": provider_errors,
        "artifact_hashes": [],
        "metadata": {"boundary": _BOUNDARY, **metadata},
    }


def _build_payload(args: argparse.Namespace) -> dict:
    cid = args.candidate_id
    rec = read_json(candidate_dir(cid) / "candidate-record.json")
    if not rec:
        return _screen(cid, screen_status="blocked", api_status="missing_candidate_record", provider_errors=["missing_candidate_record"], stale=False, metadata={"block_reason": "missing_candidate_record"})

    item = {**(rec.get("metadata") or {}), "candidate_id": cid, "title": str(rec.get("title") or "")}
    try:
        scan = _build_candidate_scan(
            item,
            target_policy="formal",
            strict_external=True,
            max_external_queries=int(getattr(args, "max_external_queries", 1) or 1),
            external_timeout=int(getattr(args, "external_timeout", 12) or 12),
            semantic_scholar_mode=getattr(args, "semantic_scholar_mode", "auto") or "auto",
        )
    except Exception as exc:  # network failure etc. -- fail closed, never fake success
        return _screen(cid, screen_status="provider_unavailable", api_status="provider_unavailable", provider_errors=[f"scan_exception:{type(exc).__name__}:{exc}"], stale=False, metadata={"block_reason": "scan_exception"})

    external = list(scan.get("external_providers_used") or [])
    errors = [_flatten(err) for err in (scan.get("provider_errors") or [])]
    stale = bool(scan.get("stale_external_novelty_cache"))

    if stale:
        screen_status, api_status, errs = "blocked", "stale_external_novelty_cache", errors
    elif external and not errors:
        screen_status, api_status, errs = "success", "success", []
    elif external and errors:
        screen_status, api_status, errs = "partial_provider_unavailable", "partial_provider_unavailable", errors
    else:
        screen_status, api_status, errs = "provider_unavailable", "provider_unavailable", errors or ["no_external_provider_succeeded"]

    metadata = {
        "verification_scope": scan.get("verification_scope", ""),
        "external_providers_used": external,
        "novelty_classification": scan.get("novelty_classification", ""),
        "nearest_work_count": len(scan.get("nearest_works") or []),
        "scan_status": scan.get("status", ""),
    }
    return _screen(cid, screen_status=screen_status, api_status=api_status, provider_errors=errs, stale=stale, metadata=metadata)


def write_screen(args: argparse.Namespace) -> dict:
    payload = _build_payload(args)
    write_json(novelty_screen_dir(args.candidate_id) / "novelty-screen.json", payload, dry_run=args.dry_run)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--max-external-queries", type=int, default=1)
    parser.add_argument("--external-timeout", type=int, default=12)
    parser.add_argument("--semantic-scholar-mode", default="auto")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.validate:
        payload = read_json(novelty_screen_dir(args.candidate_id) / "novelty-screen.json")
        errors = validate_governance_payload(payload, "novelty_screen.v1") if payload else ["missing_novelty_screen"]
        result = {"candidate_id": args.candidate_id, "status": "success" if not errors else "failed", "errors": errors}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 1
    payload = write_screen(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["screen_status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
