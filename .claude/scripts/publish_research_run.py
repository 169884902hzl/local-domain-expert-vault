"""Atomically publish accepted v2 research seeds."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from kb_common import safe_print
from research_agenda_common import slugify
from research_seed_v2_common import (
    DEFAULT_V2_PUBLISH_POLICY,
    FORMAL_SEED_REQUIRED_FILES,
    V2_PUBLISH_POLICIES,
    agenda_root,
    artifact_dir,
    artifact_hashes,
    candidate_id,
    copy_json_artifact,
    ensure_v2_dirs,
    mark_state,
    publish_dir,
    read_json,
    run_dir,
    write_json,
    write_run_artifact,
    write_text,
    utc_now,
)
from validate_research_run import validate_run as validate_run_artifacts


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


def _render_idea(candidate: dict[str, Any], decision: dict[str, Any], run_date: str) -> str:
    title = str(candidate.get("title") or decision.get("candidate_title") or "Untitled Research Seed")
    return "\n".join(
        [
            "---",
            f'title: "{title}"',
            "tags: [research-agenda, idea, seed, v2]",
            f'created: "{run_date}"',
            f'updated: "{run_date}"',
            'type: "permanent"',
            'status: "done"',
            'summary: "Validated v2 research seed published after survival decision."',
            "state_machine_version: research_seed_state_machine.v2",
            "promotion_status: v2_accept_for_user_review",
            f'candidate_id: "{decision["candidate_id"]}"',
            "---",
            "",
            f"# {title}",
            "",
            "- decision_status: v2_accept_for_user_review",
            f"- run_date: {run_date}",
            f"- candidate_id: {decision['candidate_id']}",
            f"- parent_candidate_id: {decision.get('parent_candidate_id') or '-'}",
            f"- novelty_classification: {decision.get('novelty_classification') or '-'}",
            f"- codex_action: {decision.get('codex_action') or '-'}",
            "",
            "## Problem",
            "",
            str(candidate.get("problem") or candidate.get("engineering_pathology") or "Needs problem statement review."),
            "",
            "## Mechanism",
            "",
            str(candidate.get("mechanism") or candidate.get("core_insight") or "Needs mechanism review."),
            "",
            "## Evaluation",
            "",
            f"- no_hardware_pilot: {candidate.get('minimum_no_hardware_pilot') or candidate.get('pilot') or '-'}",
            f"- strongest_baseline: {candidate.get('strongest_baseline') or candidate.get('baselines') or '-'}",
            f"- killer_experiment: {candidate.get('killer_experiment') or '-'}",
            "",
            "## Boundary",
            "",
            "- This seed was written only by `publish_research_run.py`.",
            "- User remains final reviewer before developing/promoted/pilot-ready states.",
            "",
        ]
    )


def _write_seed_stage(run_date: str, slug: str, candidate: dict[str, Any], decision: dict[str, Any], hashes: dict[str, str], *, dry_run: bool) -> Path:
    staging = run_dir(run_date) / "tmp_publish" / f"{slug}.{decision['candidate_id']}"
    _assert_under_root(staging)
    if staging.exists() and not dry_run:
        shutil.rmtree(staging)
    if not dry_run:
        staging.mkdir(parents=True, exist_ok=True)
    write_text(staging / "idea.md", _render_idea(candidate, decision, run_date), dry_run=dry_run)
    for name in ["survival-decision.json", "deepseek-review.json", "novelty-scan.json", "codex-execution-review.json"]:
        copy_json_artifact(artifact_dir(run_date) / name, staging / name, dry_run=dry_run)
    write_json(
        staging / "artifact-hashes.json",
        {
            "schema_version": "artifact_hashes.v1",
            "run_date": run_date,
            "candidate_id": decision["candidate_id"],
            "artifact_hashes": hashes,
        },
        dry_run=dry_run,
    )
    return staging


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
        "boundary": "Non-formal bucket item. Formal seed folders are written only under idea_bank/seed by this script.",
    }
    write_json(target, payload, dry_run=dry_run)
    return {"candidate_id": decision["candidate_id"], "target": str(target), "status": "dry_run" if dry_run else "written"}


def migrate_legacy_status(*, apply: bool) -> int:
    seed_root = agenda_root() / "idea_bank" / "seed"
    count = 0
    if not seed_root.exists():
        return 0
    for folder in sorted(path for path in seed_root.iterdir() if path.is_dir()):
        count += 1
        payload = {
            "schema_version": "legacy_seed_status.v1",
            "state_machine_version": "legacy_pre_v2",
            "promotion_status": "unverified_legacy_seed",
            "requires_revalidation": True,
            "created_at": utc_now(),
            "boundary": "Legacy seed retained in place; not a v2 survival decision.",
        }
        if apply:
            write_json(folder / "legacy-v2-status.json", payload, dry_run=False)
    return count


def _manifest(path_run_date: str) -> dict[str, Any]:
    path = run_dir(path_run_date) / "manifest.json"
    return read_json(path) if path.exists() else {}


def _result(
    *,
    run_date: str,
    status: str,
    target_policy: str,
    allow_formal_seed_publish: bool,
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
        "formal_seed_publish_allowed": bool(allow_formal_seed_publish),
        "scheduled_daily_switched": bool(manifest.get("scheduled_daily_switched", False)),
        "formal_seed_written": any(item.get("status") == "seed_written" for item in (published or [])),
        "published": published or [],
        "bucketed": bucketed or [],
        "blocked": blocked or [],
        "artifact_hashes": artifact_hashes(run_date, artifact_names or []),
    }


def _record_manifest_publish_policy(
    run_date: str,
    *,
    target_policy: str,
    allow_formal_seed_publish: bool,
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
    manifest["formal_seed_publish_allowed"] = bool(allow_formal_seed_publish)
    manifest["scheduled_daily_switched"] = bool(manifest.get("scheduled_daily_switched", False))
    manifest["formal_seed_written"] = bool(formal_seed_written)
    write_json(manifest_path, manifest, dry_run=False)


def publish(
    run_date: str,
    *,
    dry_run: bool,
    target_policy: str = DEFAULT_V2_PUBLISH_POLICY,
    allow_formal_seed_publish: bool = False,
) -> dict[str, Any]:
    ensure_v2_dirs(run_date)
    if target_policy not in V2_PUBLISH_POLICIES:
        raise ValueError(f"invalid_v2_publish_policy:{target_policy}")
    manifest = _manifest(run_date)
    _record_manifest_publish_policy(
        run_date,
        target_policy=target_policy,
        allow_formal_seed_publish=allow_formal_seed_publish,
        formal_seed_written=False,
        dry_run=dry_run,
    )
    if target_policy == "formal" and not allow_formal_seed_publish:
        return _result(
            run_date=run_date,
            status="blocked_formal_publish_not_allowed",
            target_policy=target_policy,
            allow_formal_seed_publish=allow_formal_seed_publish,
            blocked=["formal_publish_requires_allow_formal_seed_publish"],
        )
    if target_policy == "formal" and manifest.get("backfill_mode") != "daily":
        return _result(
            run_date=run_date,
            status="blocked_backfill_formal_publish",
            target_policy=target_policy,
            allow_formal_seed_publish=allow_formal_seed_publish,
            blocked=[f"backfill_mode_cannot_formal_publish:{manifest.get('backfill_mode')}"],
        )
    validation = validate_run_artifacts(run_date, strict_publish=True)
    if validation["status"] != "success":
        return _result(
            run_date=run_date,
            status="blocked_validation",
            target_policy=target_policy,
            allow_formal_seed_publish=allow_formal_seed_publish,
            blocked=validation["errors"],
        )
    if target_policy == "disabled":
        return _result(
            run_date=run_date,
            status="publish_disabled",
            target_policy=target_policy,
            allow_formal_seed_publish=allow_formal_seed_publish,
            blocked=[],
        )
    if target_policy == "formal" and not dry_run:
        (agenda_root() / "idea_bank" / "seed").mkdir(parents=True, exist_ok=True)
    survival = read_json(artifact_dir(run_date) / "survival-decision.json")
    candidates = _load_final_candidates(run_date)
    hashes = artifact_hashes(run_date, ["selected-candidates.json", "deepseek-review.json", "novelty-scan.json", "codex-execution-review.json", "survival-decision.json"])
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
            bucketed.append(
                _write_bucket_item(
                    run_date=run_date,
                    bucket="seed-candidates",
                    slug=slug,
                    candidate=candidate,
                    decision={**decision, "publish_target": "seed-candidates"},
                    hashes=hashes,
                    dry_run=dry_run,
                )
            )
            continue
        target = agenda_root() / "idea_bank" / "seed" / slug
        _assert_under_root(target)
        plan["items"].append({"candidate_id": decision["candidate_id"], "target": str(target)})
        if target.exists():
            duplicate_target = agenda_root() / "seed-candidates" / "duplicate-review" / run_date / f"{slug}.{decision['candidate_id']}.json"
            _assert_under_root(duplicate_target)
            duplicate_payload = {
                "schema_version": "duplicate_review.v1",
                "run_date": run_date,
                "candidate_id": decision["candidate_id"],
                "candidate": candidate,
                "survival_decision": decision,
                "existing_seed_target": str(target),
                "duplicate_review_target": str(duplicate_target),
                "artifact_hashes": hashes,
                "boundary": "Existing formal seed was not overwritten; review this duplicate candidate outside idea_bank/seed.",
            }
            write_json(duplicate_target, duplicate_payload, dry_run=dry_run)
            blocked.append(f"duplicate_guard_failed:{slug}:duplicate_review={duplicate_target}")
            continue
        staging = _write_seed_stage(run_date, slug, candidate, decision, hashes, dry_run=dry_run)
        if dry_run:
            published.append({"candidate_id": decision["candidate_id"], "target": str(target), "status": "dry_run"})
            continue
        try:
            staging.rename(target)
            missing = [name for name in FORMAL_SEED_REQUIRED_FILES if not (target / name).exists()]
            if missing:
                quarantine = agenda_root() / "quarantine" / f"{slug}.{decision['candidate_id']}"
                _assert_under_root(quarantine)
                target.rename(quarantine)
                blocked.append(f"failed_publish_invariant:{slug}:missing={','.join(missing)}")
            else:
                published.append({"candidate_id": decision["candidate_id"], "target": str(target), "status": "seed_written"})
        except Exception as exc:
            quarantine = agenda_root() / "quarantine" / f"{slug}.{decision['candidate_id']}"
            _assert_under_root(quarantine)
            if staging.exists():
                staging.rename(quarantine)
            blocked.append(f"publish_exception:{slug}:{type(exc).__name__}:{exc}")
    write_json(publish_dir(run_date) / "seed-write-plan.json", plan, dry_run=dry_run)
    status = "success" if (published or bucketed) and not blocked else ("nothing_to_publish" if not published and not bucketed and not blocked else "partial")
    if published and not dry_run:
        _record_manifest_publish_policy(
            run_date,
            target_policy=target_policy,
            allow_formal_seed_publish=allow_formal_seed_publish,
            formal_seed_written=True,
            dry_run=False,
        )
        mark_state(run_date, "seed_written", "publish/publish-result.json", dry_run=False)
    elif not dry_run:
        _record_manifest_publish_policy(
            run_date,
            target_policy=target_policy,
            allow_formal_seed_publish=allow_formal_seed_publish,
            formal_seed_written=False,
            dry_run=False,
        )
    return _result(
        run_date=run_date,
        status=status,
        target_policy=target_policy,
        allow_formal_seed_publish=allow_formal_seed_publish,
        published=published,
        bucketed=bucketed,
        blocked=blocked,
        artifact_names=["selected-candidates.json", "deepseek-review.json", "novelty-scan.json", "codex-execution-review.json", "survival-decision.json"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--target-policy", choices=["disabled", "seed-candidates-only", "formal"], default=DEFAULT_V2_PUBLISH_POLICY)
    parser.add_argument("--allow-formal-seed-publish", action="store_true")
    parser.add_argument("--migrate-legacy-status", action="store_true")
    args = parser.parse_args()

    if args.migrate_legacy_status:
        count = migrate_legacy_status(apply=not args.dry_run)
        safe_print(f"PUBLISH_RESEARCH_RUN: legacy_status_migration count={count} apply={str(not args.dry_run).lower()}")
        return 0

    if not args.run_date:
        safe_print("FAIL --run-date is required unless --migrate-legacy-status is used")
        return 1

    result = publish(
        args.run_date,
        dry_run=args.dry_run,
        target_policy=args.target_policy,
        allow_formal_seed_publish=args.allow_formal_seed_publish,
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
