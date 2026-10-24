"""Package real DeepSeek + Codex per-candidate reviews into a governance provider-review packet.

Thin packaging only: maps already-existing real provider reviews from a daily run's
artifacts (deepseek-review.json + codex-execution-review.json) into the v1
provider_review_packet artifact. It never calls a model. Honest status machine --
review_status is "success" only when real success reviews for the candidate exist in the
run; a missing review yields "blocked", a timed-out/unavailable provider yields the true
failure enum. Mutation candidates resolve their reviews via --parent-candidate-id.
"""
from __future__ import annotations

import argparse
import hashlib
import json

from research_governance_common import (
    artifact_hash,
    file_sha256,
    provider_review_dir,
    read_json,
    utc_now,
    validate_governance_payload,
    write_json,
)
from research_seed_v2_common import artifact_dir

_UNAVAILABLE = {"timeout", "provider_unavailable", "partial_provider_unavailable"}


def _resolve_run_date(args: argparse.Namespace) -> str:
    run_date = (getattr(args, "run_date", "") or "").strip()
    if run_date:
        return run_date
    run_id = (getattr(args, "run_id", "") or "").strip()
    return run_id[:10] if len(run_id) >= 10 else run_id


def _sha(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _by_candidate(doc: dict) -> dict:
    return {str(r.get("candidate_id") or ""): r for r in doc.get("reviews", []) if r.get("candidate_id")}


def _reviews(lookup_id: str, ds_rev: dict, cx_rev: dict) -> list:
    out = []
    if ds_rev:
        out.append({
            "provider": "deepseek",
            "candidate_id": lookup_id,
            "status": str(ds_rev.get("status") or "unknown"),
            "summary": str(ds_rev.get("survivability_label") or ""),
            "metadata": {
                "survivability_label": ds_rev.get("survivability_label", ""),
                "allowed_next_stage": ds_rev.get("allowed_next_stage", ""),
                "a_plus_b_risk": ds_rev.get("a_plus_b_risk", ""),
            },
        })
    if cx_rev:
        out.append({
            "provider": "codex",
            "candidate_id": lookup_id,
            "status": str(cx_rev.get("status") or "unknown"),
            "summary": str(cx_rev.get("action") or ""),
            "metadata": {
                "action": cx_rev.get("action", ""),
                "confidence": cx_rev.get("confidence", ""),
            },
        })
    return out


def _build_payload(args: argparse.Namespace) -> dict:
    candidate_id = args.candidate_id
    lookup_id = (getattr(args, "parent_candidate_id", "") or "").strip() or candidate_id
    run_date = _resolve_run_date(args)
    art_dir = artifact_dir(run_date) if run_date else None

    ds_path = art_dir / "deepseek-review.json" if art_dir else None
    cx_path = art_dir / "codex-execution-review.json" if art_dir else None
    ds_doc = read_json(ds_path) if ds_path else {}
    cx_doc = read_json(cx_path) if cx_path else {}

    ds_by, cx_by = _by_candidate(ds_doc), _by_candidate(cx_doc)
    ds_rev, cx_rev = ds_by.get(lookup_id, {}), cx_by.get(lookup_id, {})
    available = sorted(set(ds_by) | set(cx_by))

    ds_ps, cx_ps = ds_doc.get("provider_status", {}), cx_doc.get("provider_status", {})
    backed = bool(ds_ps.get("provider_backed")) and bool(cx_ps.get("provider_backed"))
    test_used = bool(ds_ps.get("test_provider_used")) or bool(cx_ps.get("test_provider_used"))
    timed_out = bool(ds_ps.get("timed_out")) or bool(cx_ps.get("timed_out"))
    mode = f"{ds_ps.get('mode') or 'openai-compatible'}+{cx_ps.get('mode') or 'codex-cli'}"

    reviews = _reviews(lookup_id, ds_rev, cx_rev)
    metadata = {"lookup_id": lookup_id, "available_candidate_ids": available}

    if not ds_rev or not cx_rev:
        review_status = status_detail = "blocked"
        backed = False
        reviews = []
        metadata["block_reason"] = "no_provider_review_for_candidate_in_run"
    elif timed_out or str(ds_rev.get("status")) in _UNAVAILABLE or str(cx_rev.get("status")) in _UNAVAILABLE:
        review_status = status_detail = "timeout" if timed_out else "provider_unavailable"
        metadata["block_reason"] = "provider_unavailable_in_run"
    elif not backed or str(ds_rev.get("status")) != "success" or str(cx_rev.get("status")) != "success":
        review_status = status_detail = "provider_unavailable"
        metadata["block_reason"] = "provider_not_backed_or_not_success"
    else:
        review_status = status_detail = "success"
        metadata["deepseek_label"] = ds_rev.get("survivability_label", "")
        metadata["codex_action"] = cx_rev.get("action", "")

    source_run_id = (getattr(args, "source_run_id", "") or "").strip()
    if not source_run_id and art_dir:
        source_run_id = str(read_json(art_dir.parent / "manifest.json").get("run_id") or "")
    if not source_run_id:
        source_run_id = run_date or "unknown-run"

    log_basis = "".join(file_sha256(p) for p in (ds_path, cx_path) if p and p.exists())
    artifact_hashes = [artifact_hash(p) for p in (ds_path, cx_path) if p and p.exists()]

    return {
        "schema_version": "provider_review_packet.v1",
        "candidate_id": candidate_id,
        "review_status": review_status,
        "provider_backed": backed,
        "test_provider_used": test_used,
        "generated_by_script": "provider_review_packet.py",
        "source_run_id": source_run_id,
        "provider_mode": mode,
        "provider_status": {"provider": "deepseek+codex", "provider_backed": backed, "mode": mode, "status": status_detail, "test_provider_used": test_used},
        "command_hash": _sha(f"provider_review_packet.py|{candidate_id}|{lookup_id}|{run_date}"),
        "provider_log_hash": _sha(log_basis or f"no-source|{candidate_id}|{lookup_id}"),
        "created_at": utc_now(),
        "reviews": reviews,
        "artifact_hashes": artifact_hashes,
        "metadata": metadata,
    }


def write_packet(args: argparse.Namespace) -> dict:
    payload = _build_payload(args)
    write_json(provider_review_dir(args.candidate_id) / "provider-review-packet.json", payload, dry_run=args.dry_run)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--run-date", default="")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--parent-candidate-id", default="")
    parser.add_argument("--source-run-id", default="")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.validate:
        payload = read_json(provider_review_dir(args.candidate_id) / "provider-review-packet.json")
        errors = validate_governance_payload(payload, "provider_review_packet.v1") if payload else ["missing_provider_review_packet"]
        result = {"candidate_id": args.candidate_id, "status": "success" if not errors else "failed", "errors": errors}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if not errors else 1
    payload = write_packet(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["review_status"] == "success" else 2


if __name__ == "__main__":
    raise SystemExit(main())
