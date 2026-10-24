"""Publish v2 review results into non-formal candidate buckets."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from kb_common import safe_print
from research_agenda_common import slugify
from research_seed_v2_common import (
    DEFAULT_V2_PUBLISH_POLICY,
    agenda_root,
    artifact_dir,
    artifact_hashes,
    candidate_id,
    ensure_v2_dirs,
    mark_state,
    publish_dir,
    read_json,
    run_dir,
    write_json,
    write_run_artifact,
)
from validate_research_run import validate_run as validate_run_artifacts


ENABLED_TARGET_POLICIES = {"disabled", "seed-candidates-only"}


def _assert_under_root(path: Path) -> None:
    root = agenda_root().resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RuntimeError(f"unsafe_publish_path_outside_agenda_root:{resolved}") from exc


def _load_final_candidates(run_date: str) -> dict[str, dict[str, Any]]:
    selected = read_json(artifact_dir(run_date) / "selected-candidates.json").get("selected", [])
    mutations_path = artifact_dir(run_date) / "gemini-mutations.json"
    mutations = read_json(mutations_path).get("mutations", []) if mutations_path.exists() else []
    by_id: dict[str, dict[str, Any]] = {}
    mutated_parent_ids = {str(item.get("parent_candidate_id")) for item in mutations}
    for item in selected:
        cid = candidate_id(item)
        if cid not in mutated_parent_ids:
            by_id[cid] = item
    for item in mutations:
        by_id[candidate_id(item)] = item
    return by_id


def _write_bucket_item(
    *,
    run_date: str,
    bucket: str,
    slug: str,
    candidate: dict[str, Any],
    decision: dict[str, Any],
    hashes: dict[str, str],
    dry_run: bool,
) -> dict[str, str]:
    target = agenda_root() / bucket / run_date / f"{slug}.json"
    _assert_under_root(target)
    if target.exists():
        target = agenda_root() / bucket / run_date / f"{slug}.{decision['candidate_id']}.json"
        _assert_under_root(target)
    payload = {
        "schema_version": "research_seed_bucket_item.v1",
        "run_date": run_date,
        "bucket": bucket,
        "candidate_id": decision["candidate_id"],
        "candidate": candidate,
        "survival_decision": decision,
        "artifact_hashes": hashes,
        "boundary": "Non-formal bucket item. Active seed promotion is governed by v1 human governance artifacts and active_seed_commit.py.",
    }
    write_json(target, payload, dry_run=dry_run)
    return {"candidate_id": decision["candidate_id"], "target": str(target), "status": "dry_run" if dry_run else "written"}


def _manifest(path_run_date: str) -> dict[str, Any]:
    path = run_dir(path_run_date) / "manifest.json"
    return read_json(path) if path.exists() else {}


def _result(
    *,
    run_date: str,
    status: str,
    target_policy: str,
    published: list[dict[str, str]] | None = None,
    bucketed: list[dict[str, str]] | None = None,
    blocked: list[str] | None = None,
    artifact_names: list[str] | None = None,
) -> dict[str, Any]:
    manifest = _manifest(run_date)
    return {
        "schema_version": "publish_result.v1",
        "run_date": run_date,
        "status": status,
        "v2_publish_policy": target_policy,
        "formal_seed_publish_allowed": False,
        "scheduled_daily_switched": bool(manifest.get("scheduled_daily_switched", False)),
        "formal_seed_written": any(item.get("status") == "seed_written" for item in (published or [])),
        "formal_rehearsal_written": any("formal-rehearsal" in item.get("target", "") for item in (bucketed or [])),
        "test_provider_used_for_formal": False,
        "formal_publish_risk": "",
        "published": published or [],
        "bucketed": bucketed or [],
        "blocked": blocked or [],
        "artifact_hashes": artifact_hashes(run_date, artifact_names or []),
    }


def _record_manifest_publish_policy(
    run_date: str,
    *,
    target_policy: str,
    formal_seed_written: bool,
    dry_run: bool,
) -> None:
    if dry_run:
        return
    manifest_path = run_dir(run_date) / "manifest.json"
    if not manifest_path.exists():
        return
    manifest = read_json(manifest_path)
    manifest["v2_publish_policy"] = target_policy
    manifest["formal_seed_publish_allowed"] = False
    manifest["scheduled_daily_switched"] = bool(manifest.get("scheduled_daily_switched", False))
    manifest["formal_seed_written"] = bool(formal_seed_written)
    manifest["test_provider_used_for_formal"] = False
    manifest["formal_publish_risk"] = ""
    write_json(manifest_path, manifest, dry_run=False)


def publish(
    run_date: str,
    *,
    dry_run: bool,
    target_policy: str = DEFAULT_V2_PUBLISH_POLICY,
) -> dict[str, Any]:
    if target_policy == "formal":
        return _result(
            run_date=run_date,
            status="legacy_formal_publish_disabled_use_formal_rehearsal_packet",
            target_policy=target_policy,
            blocked=["v1_disables_legacy_formal_seed_writing"],
        )
    ensure_v2_dirs(run_date)
    if target_policy not in ENABLED_TARGET_POLICIES:
        raise ValueError(f"invalid_v2_publish_policy:{target_policy}")
    manifest = _manifest(run_date)
    _record_manifest_publish_policy(
        run_date,
        target_policy=target_policy,
        formal_seed_written=False,
        dry_run=dry_run,
    )
    validation = validate_run_artifacts(run_date, strict_publish=True, skip_hash_artifacts={"publish-result.json"})
    if validation["status"] != "success":
        return _result(
            run_date=run_date,
            status="blocked_validation",
            target_policy=target_policy,
            blocked=validation["errors"],
        )
    if target_policy == "disabled":
        return _result(
            run_date=run_date,
            status="publish_disabled",
            target_policy=target_policy,
            blocked=[],
        )
    survival = read_json(artifact_dir(run_date) / "survival-decision.json")
    candidates = _load_final_candidates(run_date)
    hashes = artifact_hashes(
        run_date,
        [
            "selected-candidates.json",
            "deepseek-review.json",
            "novelty-scan.json",
            "codex-execution-review.json",
            "manual-prior-art-review.json",
            "baseline-table.json",
            "survival-decision.json",
        ],
    )
    plan = {"schema_version": "seed_write_plan.v1", "run_date": run_date, "items": []}
    published: list[dict[str, str]] = []
    bucketed: list[dict[str, str]] = []
    blocked: list[str] = []
    for decision in survival.get("decisions", []):
        action = str(decision.get("decision") or "")
        if action != "accept_for_user_review":
            bucket = "parked" if action in {"parked", "killed"} else ("rescue" if action == "rescue" else "seed-candidates")
            candidate = candidates.get(str(decision.get("candidate_id")))
            if candidate:
                slug = slugify(str(candidate.get("title") or decision.get("candidate_title") or decision.get("candidate_id")))
                bucketed.append(
                    _write_bucket_item(
                        run_date=run_date,
                        bucket=bucket,
                        slug=slug,
                        candidate=candidate,
                        decision=decision,
                        hashes=hashes,
                        dry_run=dry_run,
                    )
                )
            continue
        candidate = candidates.get(str(decision.get("candidate_id")))
        if not candidate:
            blocked.append(f"missing_candidate:{decision.get('candidate_id')}")
            continue
        slug = slugify(str(candidate.get("title") or decision.get("candidate_title") or decision.get("candidate_id")))
        if target_policy == "seed-candidates-only":
            target_bucket = "seed-candidates/formal-rehearsal" if decision.get("publish_target") == "formal-rehearsal" else "seed-candidates/accepted"
            bucketed.append(
                _write_bucket_item(
                    run_date=run_date,
                    bucket=target_bucket,
                    slug=slug,
                    candidate=candidate,
                    decision={**decision, "publish_target": decision.get("publish_target") or target_bucket},
                    hashes=hashes,
                    dry_run=dry_run,
                )
            )
            continue
        blocked.append(f"legacy_formal_publish_disabled:{decision.get('candidate_id')}")
        continue
    write_json(publish_dir(run_date) / "seed-write-plan.json", plan, dry_run=dry_run)
    status = "success" if (published or bucketed) and not blocked else ("nothing_to_publish" if not published and not bucketed and not blocked else "partial")
    if published and not dry_run:
        _record_manifest_publish_policy(
            run_date,
            target_policy=target_policy,
            formal_seed_written=True,
            dry_run=False,
        )
        mark_state(run_date, "seed_written", "publish/publish-result.json", dry_run=False)
    elif not dry_run:
        _record_manifest_publish_policy(
            run_date,
            target_policy=target_policy,
            formal_seed_written=False,
            dry_run=False,
        )
    return _result(
        run_date=run_date,
        status=status,
        target_policy=target_policy,
        published=published,
        bucketed=bucketed,
        blocked=blocked,
        artifact_names=["selected-candidates.json", "deepseek-review.json", "novelty-scan.json", "codex-execution-review.json", "survival-decision.json"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--target-policy", choices=["disabled", "seed-candidates-only"], default=DEFAULT_V2_PUBLISH_POLICY)
    args = parser.parse_args()

    if not args.run_date:
        safe_print("FAIL --run-date is required")
        return 1

    result = publish(
        args.run_date,
        dry_run=args.dry_run,
        target_policy=args.target_policy,
    )
    state = "seed_written" if result["published"] and not args.dry_run else "publish_checked"
    write_json(publish_dir(args.run_date) / "publish-result.json", result, dry_run=args.dry_run)
    write_run_artifact(args.run_date, "publish-result.json", result, state=state, dry_run=args.dry_run)
    safe_print(
        "PUBLISH_RESEARCH_RUN: "
        f"status={result['status']} published={len(result['published'])} "
        f"bucketed={len(result.get('bucketed', []))} blocked={len(result['blocked'])}"
    )
    return 0 if result["status"] in {"success", "nothing_to_publish", "publish_disabled"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
