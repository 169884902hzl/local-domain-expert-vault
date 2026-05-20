from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from candidate_portfolio_select import select_portfolio
from codex_seed_review import execution_review
from arxiv_ranker import ArxivPaper, RankedPaper
from daily_arxiv_pipeline import _filter_import_candidates_by_v2_triage, build_v2_review_stages, resolve_v2_publish_policy, run_research_seed_v2
from deepseek_scientific_review import build_payload as build_deepseek_payload
from paper_intake_triage import build_triage
from publish_research_run import publish
from research_agenda_extract import build_paper_primitives
from research_claim_graph import build_nodes
from research_seed_v2_common import (
    artifact_dir,
    duplicate_guard,
    file_sha256,
    init_manifest,
    read_json,
    run_dir,
    validate_json_file,
    write_json,
    write_run_artifact,
)
from survival_decision import decide
from tension_map import validate_tensions
from validate_research_run import validate_run
from weekly_strategy_review import sanitize_overrides
from audit_daily_automation_quality import _audit_v2_state_machine, _scan_text_for_seed_writer
import research_agenda_review as agenda_review
import novelty_baseline_scan as novelty_scan
import candidate_portfolio_select as portfolio_select
import deepseek_scientific_review as deepseek_review
import codex_seed_review as codex_review


RUN_DATE = "2099-01-02"


class ResearchSeedV2StateMachineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.old_root = os.environ.get("RESEARCH_SEED_V2_AGENDA_ROOT")
        os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.tmp.name
        init_manifest(RUN_DATE, backfill_mode="daily")

    def tearDown(self) -> None:
        if self.old_root is None:
            os.environ.pop("RESEARCH_SEED_V2_AGENDA_ROOT", None)
        else:
            os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.old_root
        self.tmp.cleanup()

    def candidate(self, candidate_id: str = "cand-alpha") -> dict[str, object]:
        return {
            "candidate_id": candidate_id,
            "title": "Anchored Contact Failure Benchmark",
            "problem": "Contact-rich DLO policies fail silently under latent friction shifts.",
            "mechanism": "Instrument the interface boundary and expose recovery triggers.",
            "interface_boundary": "vision-tactile-controller handoff",
            "strongest_baseline": "diffusion policy with fixed recovery threshold",
            "novelty_remaining_delta": "anchored latent failure benchmark",
            "lane": "infrastructure_or_benchmark",
            "supporting_nodes": ["claim-1"],
            "evidence_links": ["wiki/topics/example.md#claim-1"],
        }

    def write_bom_json(self, path: Path, payload: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\ufeff" + json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def provider_deepseek_payload(self, candidate: dict[str, object] | None = None) -> dict[str, object]:
        item = candidate or self.candidate()
        cid = str(item["candidate_id"])
        return {
            "provider_status": {"provider": "deepseek", "provider_backed": True, "mode": "bom-test"},
            "reviews": [
                {
                    "candidate_id": cid,
                    "status": "success",
                    "candidate_title": str(item["title"]),
                    "novelty_attack": "nearest work reviewed",
                    "baseline_attack": "baseline checked",
                    "mechanism_attack": "mechanism checked",
                    "evaluation_attack": "evaluation checked",
                    "scope_attack": "scope checked",
                    "a_plus_b_risk": "low",
                    "fatal_flaw": "",
                    "rescue_mutation": "",
                    "survivability_label": "survives",
                    "allowed_next_stage": "novelty_scan",
                }
            ],
        }

    def provider_codex_payload(self, candidate: dict[str, object] | None = None) -> dict[str, object]:
        item = candidate or self.candidate()
        cid = str(item["candidate_id"])
        return {
            "provider_status": {"provider": "codex", "provider_backed": True, "mode": "bom-test"},
            "reviews": [
                {
                    "candidate_id": cid,
                    "status": "success",
                    "candidate_title": str(item["title"]),
                    "action": "accept_for_user_review",
                    "no_hardware_pilot_feasibility": "feasible",
                    "public_dataset_or_sim_availability": "available",
                    "baseline_training_cost": "single GPU day",
                    "metric_automation": "scriptable",
                    "data_leakage_risk": "low",
                    "minimal_repo_plan": "notebook plus evaluator",
                    "real_robot_pilot_complexity": "low",
                    "reproducibility_path": "public sim",
                    "compute_time_budget": "one day",
                    "blocking_issues": [],
                    "nonblocking_risks": [],
                    "rewrite_request": "",
                    "rescue_signal": "",
                    "confidence": "medium",
                    "field_presence_only": False,
                }
            ],
        }

    def write_review_artifacts(
        self,
        *,
        candidate: dict[str, object] | None = None,
        novelty: str = "likely_open",
        codex_action: str = "accept_for_user_review",
        deepseek_label: str = "survives",
        fatal_flaw: bool = False,
        novelty_candidate_id: str | None = None,
        codex_candidate_id: str | None = None,
        mutations: list[dict[str, object]] | None = None,
        verification_scope: str = "local_only",
        external_providers_used: list[str] | None = None,
        formal_promotion_allowed: bool | None = None,
        deepseek_mode: str = "test",
        codex_mode: str = "test",
    ) -> str:
        item = candidate or self.candidate()
        cid = str(item["candidate_id"])
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {
                "schema_version": "selected_candidates.v1",
                "run_date": RUN_DATE,
                "selected": [item],
                "rejected": [],
                "selection_rules": {},
                "artifact_hashes": {},
            },
            state="portfolio_selected",
        )
        write_run_artifact(
            RUN_DATE,
            "deepseek-review.json",
            {
                "schema_version": "deepseek_review.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "reviews": [
                    {
                        "candidate_id": cid,
                        "status": "success",
                        "novelty_attack": "nearest work reviewed",
                        "baseline_attack": "baseline checked",
                        "mechanism_attack": "mechanism checked",
                        "evaluation_attack": "evaluation checked",
                        "scope_attack": "scope checked",
                        "a_plus_b_risk": "low",
                        "survivability_label": deepseek_label,
                        "fatal_flaw": fatal_flaw,
                        "rescue_mutation": "reframe as a benchmark" if deepseek_label != "survives" else "",
                        "allowed_next_stage": "novelty_scan",
                    }
                ],
                "provider_status": {"provider": "deepseek", "provider_backed": True, "mode": deepseek_mode},
                "artifact_hashes": {},
            },
            state="attacked_by_deepseek",
        )
        if mutations is not None:
            write_run_artifact(
                RUN_DATE,
                "gemini-mutations.json",
                {
                    "schema_version": "gemini_mutations.v1",
                    "run_date": RUN_DATE,
                    "mutations": mutations,
                    "artifact_hashes": {},
                },
                state="rescued_or_mutated",
            )
        external_providers = external_providers_used or ([] if verification_scope == "local_only" else ["arxiv_api"])
        if formal_promotion_allowed is None:
            formal_promotion_allowed = novelty in {"likely_open", "partial_overlap"} and verification_scope != "local_only" and bool(external_providers)
        write_run_artifact(
            RUN_DATE,
            "novelty-scan.json",
            {
                "schema_version": "novelty_scan.v1",
                "run_date": RUN_DATE,
                "status": "completed" if verification_scope != "local_only" else "completed_local_only",
                "scans": [
                    {
                        "candidate_id": novelty_candidate_id or cid,
                        "candidate_title": str(item["title"]),
                        "status": "completed" if verification_scope != "local_only" else "completed_local_only",
                        "novelty_classification": novelty,
                        "promotion_allowed": novelty in {"likely_open", "partial_overlap"},
                        "formal_promotion_allowed": formal_promotion_allowed,
                        "verification_scope": verification_scope,
                        "external_providers_used": external_providers,
                        "formal_publish_risk": "external_scope_arxiv_only_not_full_prior_art" if verification_scope == "local_plus_arxiv_api" else "",
                        "nearest_works": [{"source": "test", "score": 0.1, "title": "Near work"}] if novelty != "unknown" else [],
                        "local_scan_evidence": {},
                        "external_scan_evidence": {"arxiv_api": {"records_scanned": 1}} if external_providers else {},
                        "duplicate_guard": {"status": "pass", "action": "allow_with_lineage", "nearest_candidates": []},
                    }
                ],
                "provider_policy": {},
                "artifact_hashes": {},
            },
            state="novelty_checked",
        )
        write_run_artifact(
            RUN_DATE,
            "codex-execution-review.json",
            {
                "schema_version": "codex_execution_review.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "reviews": [
                    {
                        "candidate_id": codex_candidate_id or cid,
                        "status": "success",
                        "action": codex_action,
                        "no_hardware_pilot_feasibility": "feasible",
                        "public_dataset_or_sim_availability": "available",
                        "baseline_training_cost": "single GPU day",
                        "metric_automation": "scriptable",
                        "data_leakage_risk": "low",
                        "minimal_repo_plan": "notebook plus evaluator",
                        "real_robot_pilot_complexity": "low",
                        "reproducibility_path": "public sim",
                        "compute_time_budget": "one day",
                    }
                ],
                "provider_status": {"provider": "codex", "provider_backed": True, "mode": codex_mode},
                "artifact_hashes": {},
            },
            state="execution_reviewed",
        )
        return cid

    def ranked_paper(self, index: int, *, score: int = 80) -> RankedPaper:
        paper = ArxivPaper(
            arxiv_id=f"2401.{index:05d}",
            title=f"Robot DLO Benchmark {index}",
            authors=["A. Author"],
            summary="A tactile deformable linear object benchmark for robot learning.",
            published="2099-01-01T00:00:00Z",
            updated="2099-01-01T00:00:00Z",
            url=f"https://arxiv.org/abs/2401.{index:05d}",
            pdf_url=f"https://arxiv.org/pdf/2401.{index:05d}",
            categories=["cs.RO"],
            primary_category="cs.RO",
        )
        return RankedPaper(
            paper=paper,
            quality_score=score,
            decision="top1_candidate",
            reasons=[],
            matched_terms=[],
            penalties=[],
            research_value_score=score,
            diversity_features=["dlo"],
        )

    def test_v2_triage_nested_jsonl_selects_default_three_and_caps_four(self) -> None:
        records = [self.ranked_paper(index, score=90 - index).to_dict() for index in range(8)]
        payload = build_triage(records, run_date=RUN_DATE, target_deep_read=3, max_deep_read=4)
        selected = payload["selected_for_deep_read"]
        self.assertEqual(len(selected), 3)
        self.assertLessEqual(payload["counts"]["deep_read"], 4)
        self.assertEqual(selected[0]["arxiv_id"], "2401.00000")
        self.assertEqual(selected[0]["original_index"], 0)

    def test_v2_intake_filter_controls_import_attempts_not_min_new_imports(self) -> None:
        ranked = [self.ranked_paper(index, score=90 - index) for index in range(10)]
        candidates = [(item, item.decision, item.decision) for item in ranked]
        triage = build_triage([item.to_dict() for item in ranked], run_date=RUN_DATE, target_deep_read=3, max_deep_read=4)
        filtered = _filter_import_candidates_by_v2_triage(candidates, triage)
        self.assertEqual(len(filtered), 3)
        self.assertEqual([item.paper.arxiv_id for item, _selection, _original in filtered], [row["arxiv_id"] for row in triage["selected_for_deep_read"]])

    def test_backfill_ingest_only_stops_before_candidates_and_seed(self) -> None:
        candidates = Path(self.tmp.name) / "candidates.jsonl"
        candidates.write_text("", encoding="utf-8")
        args = Namespace(
            backfill_mode="ingest-only",
            backfill_generate_ideas=False,
            backfill_publish="disabled",
            target_deep_read=10,
            max_deep_read=10,
            idea_mode="template",
            idea_timeout=10,
            gemini_model="test",
            raw_candidate_limit=24,
            min_raw_candidates=24,
            max_generated=24,
            deepseek_timeout=10,
            allow_human_override=False,
        )
        errors: list[str] = []
        result = run_research_seed_v2(
            args=args,
            run_date=RUN_DATE,
            candidates_path=candidates,
            focus_zotero_keys=[],
            errors=errors,
        )
        self.assertEqual(result["status"], "success_ingest_only")
        self.assertFalse((artifact_dir(RUN_DATE) / "raw-candidates.json").exists())
        self.assertEqual(list((Path(self.tmp.name) / "idea_bank" / "seed").glob("*")), [])
        self.assertEqual(errors, [])

    def test_paper_primitives_note_only_downgrades_confidence(self) -> None:
        records = [
            {
                "source_note": "wiki/topics/example.md",
                "source_title": "Example",
                "zotero_key": "ABC123",
                "claim_type": "metric",
                "statement": "Baseline reaches 61 percent success.",
                "source_snippet_type": "claim_statement",
                "source_snippet": "",
            }
        ]
        primitive = build_paper_primitives(records)[0]
        self.assertEqual(primitive["confidence"]["strongest_baseline"], "low")
        self.assertEqual(primitive["confidence"]["actual_baseline_result"], "unusable")

    def test_legacy_structured_field_anchor_downgraded_low(self) -> None:
        records = [
            {
                "source_note": "wiki/topics/example.md",
                "source_title": "Example",
                "zotero_key": "ABC123",
                "claim_type": "method",
                "statement": "A structured legacy field claim.",
                "source_snippet_type": "structured_field",
                "source_snippet": "A structured legacy field claim.",
                "anchor_type": "note_only",
                "evidence_anchor": "wiki/topics/example.md#结构化提取",
                "evidence_section": "结构化提取",
            }
        ]
        primitive = build_paper_primitives(records)[0]
        self.assertEqual(primitive["confidence"]["method_assumption"], "low")
        node = build_nodes([{**primitive, "confidence": {"method_assumption": "high"}}])[0]
        self.assertEqual(node["confidence"], "low")

    def test_tension_map_rejects_high_confidence_without_high_anchor(self) -> None:
        node = {"node_id": "claim-1", "confidence": "low"}
        errors = validate_tensions(
            [{"tension_id": "t1", "supporting_nodes": ["claim-1"], "confidence": "high"}],
            {"claim-1"},
            {"claim-1": node},
        )
        self.assertIn("t1:high_confidence_without_high_anchored_node", errors)

    def test_research_agenda_review_apply_cannot_modify_seed(self) -> None:
        idea_bank = Path(self.tmp.name) / "idea_bank"
        seed = idea_bank / "seed" / "legacy-seed"
        seed.mkdir(parents=True, exist_ok=True)
        idea = seed / "idea.md"
        review_log = seed / "review_log.md"
        idea.write_text("idea_state: seed\n- decision_status: seed_pending_review\n", encoding="utf-8")
        review_log.write_text("# Review Log\n", encoding="utf-8")
        old_root = agenda_review.IDEA_BANK_DIR
        old_map = agenda_review.MUTABLE_IDEA_STATE_DIRS
        try:
            agenda_review.IDEA_BANK_DIR = idea_bank
            agenda_review.MUTABLE_IDEA_STATE_DIRS = {
                state: idea_bank / state for state in agenda_review.IDEA_STATES if state != agenda_review.FORMAL_SEED_STATE
            }
            agenda_review.apply_recommendations(
                [
                    {
                        "path": str(seed),
                        "state": "seed",
                        "recommended_state": "rejected",
                        "quality_flags": ["test_flag"],
                    }
                ]
            )
        finally:
            agenda_review.IDEA_BANK_DIR = old_root
            agenda_review.MUTABLE_IDEA_STATE_DIRS = old_map
        self.assertTrue(seed.exists())
        self.assertEqual(idea.read_text(encoding="utf-8"), "idea_state: seed\n- decision_status: seed_pending_review\n")
        self.assertEqual(review_log.read_text(encoding="utf-8"), "# Review Log\n")
        reports = list((idea_bank.parent / "seed-candidates" / "legacy-review").rglob("legacy-seed.json"))
        self.assertEqual(len(reports), 1)

    def test_portfolio_select_keeps_outside_analogy_slot(self) -> None:
        candidates = [
            {**self.candidate(f"cand-{index}"), "lane": "grounded_mechanism", "mechanism_family": f"m{index}"}
            for index in range(4)
        ]
        candidates.append({**self.candidate("cand-outside"), "lane": "outside_analogy", "mechanism_family": "analogy"})
        selected, _ = select_portfolio(candidates, max_selected=4)
        self.assertTrue(any(item.get("lane") == "outside_analogy" for item in selected))

    def test_bom_raw_candidates_json_can_be_portfolio_selected(self) -> None:
        self.write_bom_json(
            artifact_dir(RUN_DATE) / "raw-candidates.json",
            {
                "schema_version": "raw_candidate.v1",
                "run_date": RUN_DATE,
                "candidates": [self.candidate()],
                "generation_config": {},
                "artifact_hashes": {},
            },
        )
        old_argv = sys.argv[:]
        try:
            sys.argv = ["candidate_portfolio_select.py", "--run-date", RUN_DATE, "--max-selected", "8"]
            self.assertEqual(portfolio_select.main(), 0)
        finally:
            sys.argv = old_argv
        selected = read_json(artifact_dir(RUN_DATE) / "selected-candidates.json")
        self.assertEqual(selected["selected"][0]["candidate_id"], "cand-alpha")

    def test_bom_invalid_schema_still_fails_validation(self) -> None:
        path = artifact_dir(RUN_DATE) / "raw-candidates.json"
        self.write_bom_json(path, {"schema_version": "wrong.v1", "run_date": RUN_DATE, "candidates": []})
        errors = validate_json_file(path, "raw_candidate.v1")
        self.assertTrue(any(error.startswith("schema_version_mismatch") for error in errors))

    def test_invalid_nested_codex_action_fails_schema(self) -> None:
        path = artifact_dir(RUN_DATE) / "codex-execution-review.json"
        self.write_bom_json(
            path,
            {
                "schema_version": "codex_execution_review.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "provider_status": {"provider": "codex", "provider_backed": True, "mode": "codex-cli"},
                "reviews": [{**self.provider_codex_payload()["reviews"][0], "action": "accept"}],
            },
        )
        errors = validate_json_file(path, "codex_execution_review.v1")
        self.assertTrue(any("action" in error for error in errors))

    def test_invalid_deepseek_survivability_label_fails_schema(self) -> None:
        path = artifact_dir(RUN_DATE) / "deepseek-review.json"
        payload = self.provider_deepseek_payload()
        payload["schema_version"] = "deepseek_review.v1"
        payload["run_date"] = RUN_DATE
        payload["status"] = "success"
        payload["reviews"][0]["survivability_label"] = "maybe"  # type: ignore[index]
        self.write_bom_json(path, payload)
        errors = validate_json_file(path, "deepseek_review.v1")
        self.assertTrue(any("survivability_label" in error for error in errors))

    def test_missing_nested_candidate_id_fails_schema(self) -> None:
        path = artifact_dir(RUN_DATE) / "novelty-scan.json"
        self.write_bom_json(
            path,
            {
                "schema_version": "novelty_scan.v1",
                "run_date": RUN_DATE,
                "status": "completed_local_only",
                "scans": [
                    {
                        "novelty_classification": "likely_open",
                        "promotion_allowed": True,
                        "formal_promotion_allowed": False,
                        "verification_scope": "local_only",
                        "external_providers_used": [],
                        "nearest_works": [],
                        "duplicate_guard": {},
                    }
                ],
            },
        )
        errors = validate_json_file(path, "novelty_scan.v1")
        self.assertTrue(any("candidate_id" in error for error in errors))

    def test_invalid_novelty_classification_fails_schema(self) -> None:
        path = artifact_dir(RUN_DATE) / "novelty-scan.json"
        self.write_bom_json(
            path,
            {
                "schema_version": "novelty_scan.v1",
                "run_date": RUN_DATE,
                "status": "completed_local_only",
                "scans": [
                    {
                        "candidate_id": "cand-alpha",
                        "novelty_classification": "new",
                        "promotion_allowed": True,
                        "formal_promotion_allowed": False,
                        "verification_scope": "local_only",
                        "external_providers_used": [],
                        "nearest_works": [],
                        "duplicate_guard": {},
                    }
                ],
            },
        )
        errors = validate_json_file(path, "novelty_scan.v1")
        self.assertTrue(any("novelty_classification" in error for error in errors))

    def test_invalid_human_override_cannot_be_consumed(self) -> None:
        cid = self.write_review_artifacts(novelty="unknown")
        override_dir = Path(self.tmp.name) / "overrides" / "human-overrides" / RUN_DATE
        self.write_bom_json(
            override_dir / f"{cid}.json",
            {
                "schema_version": "human_override.v1",
                "candidate_id": cid,
                "run_id": RUN_DATE,
                "override_type": "bad_override",
                "reviewer": "human",
                "created_at": "2099-01-02T00:00:00Z",
                "reason": "test",
                "risk_acceptance": "test",
                "expires_after_days": 7,
                "allowed_publish_target": "seed",
                "cannot_weaken": [],
            },
        )
        payload = decide(run_date=RUN_DATE, allow_human_override=True)
        self.assertEqual(payload["human_overrides_consumed"], [])
        self.assertTrue(payload["human_override_errors"])

    def test_bom_deepseek_provider_json_can_be_loaded_but_invalid_still_blocks(self) -> None:
        item = self.candidate()
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {
                "schema_version": "selected_candidates.v1",
                "run_date": RUN_DATE,
                "selected": [item],
                "rejected": [],
                "selection_rules": {},
                "artifact_hashes": {},
            },
            state="portfolio_selected",
        )
        provider_path = Path(self.tmp.name) / "provider-deepseek.json"
        self.write_bom_json(provider_path, self.provider_deepseek_payload(item))
        old_argv = sys.argv[:]
        try:
            sys.argv = ["deepseek_scientific_review.py", "--run-date", RUN_DATE, "--provider-review-json", str(provider_path)]
            self.assertEqual(deepseek_review.main(), 0)
        finally:
            sys.argv = old_argv
        payload = read_json(artifact_dir(RUN_DATE) / "deepseek-review.json")
        self.assertEqual(payload["status"], "success")
        self.assertTrue(payload["provider_status"]["provider_backed"])

        invalid_path = Path(self.tmp.name) / "provider-deepseek-invalid.json"
        self.write_bom_json(
            invalid_path,
            {
                "provider_status": {"provider": "deepseek", "provider_backed": True},
                "reviews": [{"candidate_id": "cand-alpha", "status": "success"}],
            },
        )
        invalid_payload = deepseek_review._load_provider_payload(str(invalid_path))
        blocked, exit_code = build_deepseek_payload([item], run_date=RUN_DATE, provider_payload=invalid_payload)
        self.assertEqual(exit_code, 2)
        self.assertEqual(blocked["status"], "partial_provider_invalid")
        self.assertFalse(blocked["provider_status"]["provider_backed"])

    def test_deepseek_opencode_provider_success_with_mocked_cli(self) -> None:
        output = {
            "schema_version": "deepseek_review.v1",
            "run_date": RUN_DATE,
            "status": "success",
            "reviews": self.provider_deepseek_payload()["reviews"],
        }
        with patch.object(
            deepseek_review,
            "run_opencode_cli",
            return_value={"exit_code": 0, "timed_out": False, "clean_output": json.dumps(output), "effective_model": "deepseek/deepseek-v4-pro", "event_count": 1},
        ):
            provider_payload = deepseek_review._opencode_provider_payload([self.candidate()], run_date=RUN_DATE, model="deepseek/deepseek-v4-pro", timeout_sec=5)
        payload, exit_code = build_deepseek_payload([self.candidate()], run_date=RUN_DATE, provider_payload=provider_payload)
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["status"], "success")
        self.assertTrue(payload["provider_status"]["provider_backed"])

    def test_deepseek_opencode_invalid_json_fails_closed(self) -> None:
        with patch.object(
            deepseek_review,
            "run_opencode_cli",
            return_value={"exit_code": 0, "timed_out": False, "clean_output": "not json", "effective_model": "deepseek/deepseek-v4-pro", "event_count": 1},
        ):
            provider_payload = deepseek_review._opencode_provider_payload([self.candidate()], run_date=RUN_DATE, model="deepseek/deepseek-v4-pro", timeout_sec=5)
        payload, exit_code = build_deepseek_payload([self.candidate()], run_date=RUN_DATE, provider_payload=provider_payload)
        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "partial_provider_invalid")
        self.assertFalse(payload["provider_status"]["provider_backed"])

    def test_deepseek_opencode_missing_candidate_review_fails_closed(self) -> None:
        output = {
            "schema_version": "deepseek_review.v1",
            "run_date": RUN_DATE,
            "status": "success",
            "reviews": [],
        }
        with patch.object(
            deepseek_review,
            "run_opencode_cli",
            return_value={"exit_code": 0, "timed_out": False, "clean_output": json.dumps(output), "effective_model": "deepseek/deepseek-v4-pro", "event_count": 1},
        ):
            provider_payload = deepseek_review._opencode_provider_payload([self.candidate()], run_date=RUN_DATE, model="deepseek/deepseek-v4-pro", timeout_sec=5)
        payload, exit_code = build_deepseek_payload([self.candidate()], run_date=RUN_DATE, provider_payload=provider_payload)
        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "partial_provider_invalid")
        self.assertFalse(payload["provider_status"]["provider_backed"])

    def test_bom_codex_provider_json_can_be_loaded(self) -> None:
        item = self.candidate()
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {
                "schema_version": "selected_candidates.v1",
                "run_date": RUN_DATE,
                "selected": [item],
                "rejected": [],
                "selection_rules": {},
                "artifact_hashes": {},
            },
            state="portfolio_selected",
        )
        provider_path = Path(self.tmp.name) / "provider-codex.json"
        self.write_bom_json(provider_path, self.provider_codex_payload(item))
        result = execution_review(RUN_DATE, dry_run=False, provider_review_json=str(provider_path))
        self.assertEqual(result["status"], "success")
        payload = read_json(artifact_dir(RUN_DATE) / "codex-execution-review.json")
        self.assertTrue(payload["provider_status"]["provider_backed"])
        self.assertEqual(payload["reviews"][0]["action"], "accept_for_user_review")

    def _fake_codex_popen(self, output: str, *, exit_code: int = 0):
        class FakeProc:
            def __init__(self, command: list[str], **_kwargs: object) -> None:
                self.command = command
                self.pid = 999999
                self.returncode = exit_code

            def communicate(self, _stdin: str | None = None, timeout: int | None = None) -> tuple[str, str]:
                if "--output-last-message" in self.command:
                    path = Path(self.command[self.command.index("--output-last-message") + 1])
                    path.write_text(output, encoding="utf-8")
                return "", ""

        return FakeProc

    def test_codex_cli_provider_success_with_mocked_subprocess(self) -> None:
        self.write_review_artifacts()
        output = {
            "schema_version": "codex_execution_review.v1",
            "run_date": RUN_DATE,
            "status": "success",
            "reviews": self.provider_codex_payload()["reviews"],
        }
        with patch.object(codex_review.shutil, "which", return_value="codex"), patch.object(
            codex_review.subprocess,
            "Popen",
            self._fake_codex_popen(json.dumps(output)),
        ):
            result = execution_review(RUN_DATE, dry_run=False, provider="codex-cli", timeout_sec=5)
        self.assertEqual(result["status"], "success")
        payload = read_json(artifact_dir(RUN_DATE) / "codex-execution-review.json")
        self.assertTrue(payload["provider_status"]["provider_backed"])

    def test_codex_cli_invalid_json_fails_closed(self) -> None:
        self.write_review_artifacts()
        with patch.object(codex_review.shutil, "which", return_value="codex"), patch.object(
            codex_review.subprocess,
            "Popen",
            self._fake_codex_popen("not json"),
        ):
            result = execution_review(RUN_DATE, dry_run=False, provider="codex-cli", timeout_sec=5)
        self.assertEqual(result["status"], "partial_provider_invalid")
        payload = read_json(artifact_dir(RUN_DATE) / "codex-execution-review.json")
        self.assertFalse(payload["provider_status"]["provider_backed"])

    def test_codex_cli_field_presence_accept_fails_closed(self) -> None:
        self.write_review_artifacts()
        provider = self.provider_codex_payload()
        provider["reviews"][0]["field_presence_only"] = True  # type: ignore[index]
        with patch.object(codex_review.shutil, "which", return_value="codex"), patch.object(
            codex_review.subprocess,
            "Popen",
            self._fake_codex_popen(json.dumps(provider)),
        ):
            result = execution_review(RUN_DATE, dry_run=False, provider="codex-cli", timeout_sec=5)
        self.assertEqual(result["status"], "partial_provider_invalid")
        payload = read_json(artifact_dir(RUN_DATE) / "codex-execution-review.json")
        self.assertFalse(payload["provider_status"]["provider_backed"])

    def test_unknown_novelty_cannot_auto_promote(self) -> None:
        self.write_review_artifacts(novelty="unknown")
        payload = decide(run_date=RUN_DATE, allow_human_override=False)
        self.assertEqual(payload["decisions"][0]["decision"], "killed")
        self.assertIn("unknown_novelty_without_human_override", payload["decisions"][0]["blocks"])

    def test_local_only_likely_open_cannot_formal_publish(self) -> None:
        self.write_review_artifacts(novelty="likely_open", verification_scope="local_only")
        payload = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        self.assertEqual(payload["decisions"][0]["decision"], "killed")
        self.assertIn("formal_novelty_promotion_not_allowed", payload["decisions"][0]["blocks"])
        self.assertIn("formal_novelty_requires_external_or_hybrid_scope", payload["decisions"][0]["blocks"])

    def test_local_only_likely_open_can_seed_candidates_only(self) -> None:
        self.write_review_artifacts(novelty="likely_open", verification_scope="local_only")
        survival = decide(run_date=RUN_DATE, allow_human_override=False)
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="seed-candidates-only")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["published"], [])
        self.assertEqual(len(result["bucketed"]), 1)

    def test_external_arxiv_only_novelty_can_formal_publish_with_risk_marker(self) -> None:
        self.write_review_artifacts(
            verification_scope="local_plus_arxiv_api",
            deepseek_mode="opencode",
            codex_mode="codex-cli",
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        self.assertEqual(survival["decisions"][0]["decision"], "accept_for_user_review")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "success")
        manifest = read_json(run_dir(RUN_DATE) / "manifest.json")
        self.assertEqual(manifest["formal_publish_risk"], "external_scope_arxiv_only_not_full_prior_art")

    def test_deepseek_local_adapter_does_not_satisfy_gate(self) -> None:
        payload, exit_code = build_deepseek_payload([self.candidate()], run_date=RUN_DATE, provider_payload={})
        self.assertEqual(exit_code, 2)
        self.assertEqual(payload["status"], "partial_provider_unavailable")
        self.assertFalse(payload["provider_status"]["provider_backed"])

    def test_codex_field_presence_only_does_not_accept(self) -> None:
        self.write_review_artifacts()
        result = execution_review(RUN_DATE, dry_run=False, provider_review_json="")
        self.assertEqual(result["status"], "partial_provider_unavailable")
        payload = json.loads((artifact_dir(RUN_DATE) / "codex-execution-review.json").read_text(encoding="utf-8"))
        self.assertNotEqual(payload["reviews"][0]["action"], "accept_for_user_review")
        self.assertFalse(payload["provider_status"]["provider_backed"])

    def test_novelty_no_nearest_work_defaults_unknown(self) -> None:
        guard = {"status": "pass", "action": "allow_with_lineage"}
        classification, allowed, reason = novelty_scan._classify(
            guard=guard,
            nearest_works=[],
            evidence_summary={
                "local_notes_claim_graph": {"records_scanned": 0},
                "local_arxiv_mirror": {"records_scanned": 0, "error": "missing"},
            },
            remaining_delta="test delta",
            strict_external=False,
        )
        self.assertEqual(classification, "unknown")
        self.assertFalse(allowed)
        self.assertEqual(reason, "insufficient_local_or_external_evidence")

    def test_arxiv_external_provider_timeout_fails_closed(self) -> None:
        with patch.object(novelty_scan.urllib.request, "urlopen", side_effect=TimeoutError("test timeout")):
            hits, summary = novelty_scan._scan_arxiv_api(self.candidate(), max_queries=1, timeout=1, delay_sec=0)
        self.assertEqual(hits, [])
        self.assertIn("TimeoutError", summary["error"])

    def test_bom_claim_graph_jsonl_first_line_is_used_by_novelty_scan(self) -> None:
        graph_path = Path(self.tmp.name) / "evidence" / "research_claim_graph.jsonl"
        graph_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "schema_version": "research_claim_graph.v1",
            "node_id": "claim-1",
            "source_title": "Anchored Contact Failure Benchmark",
            "claim_type": "central_claim",
            "statement": "Contact rich DLO policies fail under latent friction shifts at the vision tactile controller interface boundary.",
            "source_note": "wiki/topics/example.md",
            "zotero_key": "ABC123",
            "anchor": {"anchor_type": "section", "section": "Results", "snippet": "Contact rich DLO policies fail under latent friction shifts."},
            "confidence": "high",
        }
        graph_path.write_text("\ufeff" + json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
        nearest, summary = novelty_scan._scan_claim_graph(self.candidate())
        self.assertEqual(summary["records_scanned"], 1)
        self.assertTrue(nearest)

    def test_codex_reject_goes_to_rescue_or_parked_not_seed(self) -> None:
        self.write_review_artifacts(codex_action="reject_with_rescue")
        payload = decide(run_date=RUN_DATE, allow_human_override=False)
        self.assertNotEqual(payload["decisions"][0]["decision"], "accept_for_user_review")

    def test_mutated_candidate_requires_novelty_and_codex_rescan_for_final_id(self) -> None:
        parent = self.candidate("cand-parent")
        mutation = {**self.candidate("cand-mutated"), "parent_candidate_id": "cand-parent"}
        self.write_review_artifacts(
            candidate=parent,
            deepseek_label="survives_if_mutated",
            mutations=[mutation],
            novelty_candidate_id="cand-parent",
            codex_candidate_id="cand-mutated",
        )
        payload = decide(run_date=RUN_DATE, allow_human_override=False)
        self.assertNotEqual(payload["decisions"][0]["decision"], "accept_for_user_review")
        self.assertIn("unknown_novelty_without_human_override", payload["decisions"][0]["blocks"])

    def test_human_override_cannot_bypass_deepseek_fatal_flaw(self) -> None:
        cid = self.write_review_artifacts(novelty="unknown", fatal_flaw=True)
        override_dir = Path(self.tmp.name) / "overrides" / "human-overrides" / RUN_DATE
        override_dir.mkdir(parents=True, exist_ok=True)
        write_json(
            override_dir / f"{cid}.json",
            {
                "schema_version": "human_override.v1",
                "candidate_id": cid,
                "run_id": RUN_DATE,
                "override_type": "accept_unknown_novelty_risk",
                "reviewer": "human",
                "created_at": "2099-01-02T00:00:00Z",
                "reason": "test override",
                "risk_acceptance": "accept unknown novelty risk only",
                "expires_after_days": 7,
                "allowed_publish_target": "seed",
                "cannot_weaken": ["deepseek_fatal_flaw", "codex_reject", "missing_survival_decision"],
            },
        )
        payload = decide(run_date=RUN_DATE, allow_human_override=True)
        self.assertIn("deepseek_fatal_flaw", payload["decisions"][0]["blocks"])
        self.assertIn("human_override_cannot_bypass_hard_block", payload["decisions"][0]["blocks"])

    def test_bom_human_override_consumed_only_when_allowed(self) -> None:
        cid = self.write_review_artifacts(novelty="unknown")
        override_dir = Path(self.tmp.name) / "overrides" / "human-overrides" / RUN_DATE
        override = {
            "schema_version": "human_override.v1",
            "candidate_id": cid,
            "run_id": RUN_DATE,
            "override_type": "accept_unknown_novelty_risk",
            "reviewer": "human",
            "created_at": "2099-01-02T00:00:00Z",
            "reason": "test override",
            "risk_acceptance": "accept unknown novelty risk only",
            "expires_after_days": 7,
            "allowed_publish_target": "seed",
            "cannot_weaken": ["deepseek_fatal_flaw", "codex_reject", "missing_survival_decision"],
        }
        self.write_bom_json(override_dir / f"{cid}.json", override)
        without_allow = decide(run_date=RUN_DATE, allow_human_override=False)
        self.assertEqual(without_allow["human_overrides_consumed"], [])
        self.assertFalse(without_allow["decisions"][0]["human_override_used"])

        with_allow = decide(run_date=RUN_DATE, allow_human_override=True)
        self.assertEqual(with_allow["human_overrides_consumed"], [cid])
        self.assertTrue(with_allow["decisions"][0]["human_override_used"])
        self.assertEqual(with_allow["decisions"][0]["decision"], "killed")
        self.assertIn("novelty_promotion_not_allowed", with_allow["decisions"][0]["blocks"])

    def test_strategy_override_cannot_weaken_hard_gates(self) -> None:
        safe, errors = sanitize_overrides({"allow_deepseek_fatal_flaw": True, "lane_quota": {"outside_analogy": 2}})
        self.assertIn("attempted_hard_gate_override:allow_deepseek_fatal_flaw", errors)
        self.assertEqual(safe["overrides"], {"lane_quota": {"outside_analogy": 2}})

    def test_missing_survival_decision_blocks_publish(self) -> None:
        self.write_review_artifacts()
        result = publish(RUN_DATE, dry_run=True)
        self.assertEqual(result["status"], "blocked_validation")
        self.assertTrue(any("survival-decision.json" in item for item in result["blocked"]))

    def test_publish_dry_run_writes_no_formal_seed(self) -> None:
        self.write_review_artifacts()
        survival = decide(run_date=RUN_DATE, allow_human_override=False)
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=True)
        self.assertEqual(result["status"], "success")
        seed_root = Path(self.tmp.name) / "idea_bank" / "seed"
        self.assertEqual([path for path in seed_root.glob("*") if path.is_dir()], [])

    def test_default_v2_publish_policy_is_not_formal(self) -> None:
        self.assertEqual(resolve_v2_publish_policy(Namespace()), "seed-candidates-only")

    def test_seed_candidates_only_does_not_write_formal_seed(self) -> None:
        self.write_review_artifacts()
        survival = decide(run_date=RUN_DATE, allow_human_override=False)
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="seed-candidates-only")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["published"], [])
        self.assertEqual(len(result["bucketed"]), 1)
        self.assertIn("seed-candidates", result["bucketed"][0]["target"])
        self.assertEqual(list((Path(self.tmp.name) / "idea_bank" / "seed").glob("*")), [])
        manifest = read_json(run_dir(RUN_DATE) / "manifest.json")
        self.assertFalse(manifest["formal_seed_written"])
        self.assertEqual(manifest["v2_publish_policy"], "seed-candidates-only")

    def test_formal_publish_without_explicit_allow_blocks(self) -> None:
        self.write_review_artifacts()
        survival = decide(run_date=RUN_DATE, allow_human_override=False)
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal")
        self.assertEqual(result["status"], "blocked_formal_publish_not_allowed")
        self.assertEqual(result["published"], [])
        self.assertEqual(list((Path(self.tmp.name) / "idea_bank" / "seed").glob("*")), [])

    def test_formal_provider_json_blocks_by_default(self) -> None:
        self.write_review_artifacts(verification_scope="local_plus_arxiv_api")
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "blocked_formal_provider_provenance")
        self.assertTrue(any("formal_provider_mode_not_production" in item for item in result["blocked"]))

    def test_formal_provider_json_manual_override_records_risk(self) -> None:
        self.write_review_artifacts(verification_scope="local_plus_arxiv_api")
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(
            RUN_DATE,
            dry_run=False,
            target_policy="formal",
            allow_formal_seed_publish=True,
            allow_test_provider_for_formal=True,
        )
        self.assertEqual(result["status"], "success")
        manifest = read_json(run_dir(RUN_DATE) / "manifest.json")
        self.assertTrue(manifest["test_provider_used_for_formal"])
        self.assertIn("test_provider_not_production_provenance", manifest["formal_publish_risk"])

    def test_formal_publish_with_allow_still_requires_existing_gates(self) -> None:
        self.write_review_artifacts(
            codex_action="reject_with_rescue",
            verification_scope="local_plus_arxiv_api",
            deepseek_mode="opencode",
            codex_mode="codex-cli",
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["published"], [])
        self.assertEqual(len(result["bucketed"]), 1)
        self.assertEqual(list((Path(self.tmp.name) / "idea_bank" / "seed").glob("*")), [])

    def test_backfill_cannot_formal_publish(self) -> None:
        manifest = read_json(run_dir(RUN_DATE) / "manifest.json")
        manifest["backfill_mode"] = "ingest-only"
        write_json(run_dir(RUN_DATE) / "manifest.json", manifest)
        self.write_review_artifacts()
        survival = decide(run_date=RUN_DATE, allow_human_override=False)
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "blocked_backfill_formal_publish")
        self.assertEqual(result["published"], [])

    def test_publish_actual_staged_rename_writes_required_artifacts(self) -> None:
        self.write_review_artifacts(
            verification_scope="local_plus_arxiv_api",
            deepseek_mode="opencode",
            codex_mode="codex-cli",
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "success")
        target = Path(result["published"][0]["target"])
        for name in [
            "idea.md",
            "survival-decision.json",
            "deepseek-review.json",
            "novelty-scan.json",
            "codex-execution-review.json",
            "artifact-hashes.json",
        ]:
            self.assertTrue((target / name).exists(), name)
        manifest = json.loads((run_dir(RUN_DATE) / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["formal_seed_written"])

    def test_publish_existing_target_blocks_duplicate_no_overwrite(self) -> None:
        self.write_review_artifacts(
            verification_scope="local_plus_arxiv_api",
            deepseek_mode="opencode",
            codex_mode="codex-cli",
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        seed_dir = Path(self.tmp.name) / "idea_bank" / "seed" / "anchored-contact-failure-benchmark"
        seed_dir.mkdir(parents=True, exist_ok=True)
        marker = seed_dir / "idea.md"
        marker.write_text("existing", encoding="utf-8")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "partial")
        self.assertTrue(any(item.startswith("duplicate_guard_failed") for item in result["blocked"]))
        self.assertEqual(marker.read_text(encoding="utf-8"), "existing")
        duplicate_reports = list((Path(self.tmp.name) / "seed-candidates" / "duplicate-review" / RUN_DATE).glob("*.json"))
        self.assertEqual(len(duplicate_reports), 1)

    def test_concurrent_publish_lock_blocks_same_slug(self) -> None:
        self.write_review_artifacts(
            verification_scope="local_plus_arxiv_api",
            deepseek_mode="opencode",
            codex_mode="codex-cli",
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        lock = Path(self.tmp.name) / "idea_bank" / "seed" / "anchored-contact-failure-benchmark.publish.lock"
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_text("held", encoding="utf-8")
        result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "partial")
        self.assertTrue(any(item.startswith("blocked_concurrent_publish_lock_exists") for item in result["blocked"]))
        self.assertEqual(list((Path(self.tmp.name) / "idea_bank" / "seed").glob("anchored-contact-failure-benchmark")), [])

    def test_missing_required_file_after_publish_moves_to_quarantine(self) -> None:
        self.write_review_artifacts(
            verification_scope="local_plus_arxiv_api",
            deepseek_mode="opencode",
            codex_mode="codex-cli",
        )
        survival = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        with patch("publish_research_run.FORMAL_SEED_REQUIRED_FILES", ["idea.md", "missing-required.txt"]):
            result = publish(RUN_DATE, dry_run=False, target_policy="formal", allow_formal_seed_publish=True)
        self.assertEqual(result["status"], "partial")
        self.assertTrue(any(item.startswith("failed_publish_invariant") for item in result["blocked"]))
        quarantine = Path(self.tmp.name) / "quarantine"
        self.assertTrue(any(path.is_dir() for path in quarantine.glob("anchored-contact-failure-benchmark.*")))

    def test_artifact_hash_mismatch_blocks_validation(self) -> None:
        self.write_review_artifacts()
        survival = decide(run_date=RUN_DATE, allow_human_override=False)
        write_run_artifact(RUN_DATE, "survival-decision.json", survival, state="survival_decided")
        selected_path = artifact_dir(RUN_DATE) / "selected-candidates.json"
        original_hash = file_sha256(selected_path)
        data = json.loads(selected_path.read_text(encoding="utf-8"))
        data["selected"][0]["title"] = "Tampered"
        selected_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assertNotEqual(original_hash, file_sha256(selected_path))
        validation = validate_run(RUN_DATE, strict_publish=True)
        self.assertEqual(validation["status"], "partial_schema_blocked")
        self.assertTrue(any("hash_mismatch:selected-candidates.json" in item for item in validation["errors"]))

    def test_duplicate_guard_blocks_existing_seed_title(self) -> None:
        seed_dir = Path(self.tmp.name) / "idea_bank" / "seed" / "anchored-contact-failure-benchmark"
        seed_dir.mkdir(parents=True, exist_ok=True)
        (seed_dir / "idea.md").write_text("# Anchored Contact Failure Benchmark\n", encoding="utf-8")
        guard = duplicate_guard(self.candidate())
        self.assertEqual(guard["status"], "possible_duplicate")
        self.assertEqual(guard["action"], "block")

    def test_raw_candidate_stage_has_no_legacy_write_seed_function(self) -> None:
        ideate_text = (SCRIPTS_DIR / "research_agenda_ideate.py").read_text(encoding="utf-8")
        update_text = (SCRIPTS_DIR / "research_agenda_update.py").read_text(encoding="utf-8")
        self.assertNotIn("def write_seed_folder", ideate_text)
        self.assertNotIn("write_seed_folder(", update_text)

    def test_audit_detects_variable_path_seed_writer(self) -> None:
        fake = """
from research_agenda_common import IDEA_BANK_DIR
import shutil
def bad(source, recommended):
    target = IDEA_BANK_DIR / recommended / source.name
    shutil.move(str(source), str(target))
"""
        issues = _scan_text_for_seed_writer(Path(self.tmp.name) / "fake.py", fake)
        self.assertTrue(any(issue["code"] == "v2_direct_seed_writer_outside_publish" for issue in issues))

    def test_scheduled_daily_wrapper_does_not_pass_formal_publish_flags(self) -> None:
        wrapper = SCRIPTS_DIR / "run_daily_arxiv_task.ps1"
        text = wrapper.read_text(encoding="utf-8")
        self.assertNotIn("--allow-formal-seed-publish", text)
        self.assertNotIn("--allow-test-provider-for-formal", text)
        self.assertNotRegex(text, r"--v2-publish-policy\s+['\"]?formal\b")

    def test_audit_catches_policy_manifest_mismatch(self) -> None:
        manifest = read_json(run_dir(RUN_DATE) / "manifest.json")
        manifest["v2_publish_policy"] = "formal"
        manifest["formal_seed_publish_allowed"] = True
        manifest["formal_seed_written"] = True
        write_json(run_dir(RUN_DATE) / "manifest.json", manifest)
        write_run_artifact(
            RUN_DATE,
            "publish-result.json",
            {
                "schema_version": "publish_result.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "v2_publish_policy": "seed-candidates-only",
                "formal_seed_publish_allowed": True,
                "formal_seed_written": True,
                "published": [{"candidate_id": "cand-alpha", "target": "x", "status": "seed_written"}],
                "bucketed": [],
                "blocked": [],
                "artifact_hashes": {},
            },
            state="seed_written",
        )
        _summary, issues = _audit_v2_state_machine(RUN_DATE)
        self.assertTrue(any(issue["code"] == "v2_publish_policy_mismatch" for issue in issues))

    def test_audit_catches_formal_seed_written_under_seed_candidates_only(self) -> None:
        manifest = read_json(run_dir(RUN_DATE) / "manifest.json")
        manifest["v2_publish_policy"] = "seed-candidates-only"
        manifest["formal_seed_publish_allowed"] = False
        manifest["formal_seed_written"] = True
        write_json(run_dir(RUN_DATE) / "manifest.json", manifest)
        write_run_artifact(
            RUN_DATE,
            "publish-result.json",
            {
                "schema_version": "publish_result.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "v2_publish_policy": "seed-candidates-only",
                "formal_seed_publish_allowed": False,
                "formal_seed_written": True,
                "published": [{"candidate_id": "cand-alpha", "target": "x", "status": "seed_written"}],
                "bucketed": [],
                "blocked": [],
                "artifact_hashes": {},
            },
            state="seed_written",
        )
        _summary, issues = _audit_v2_state_machine(RUN_DATE)
        self.assertTrue(any(issue["code"] == "v2_formal_seed_written_policy_mismatch" for issue in issues))
        self.assertTrue(any(issue["code"] == "v2_formal_seed_written_without_allow" for issue in issues))

    def test_daily_pipeline_v2_provider_command_assembly(self) -> None:
        args = Namespace(
            deepseek_provider="opencode",
            deepseek_provider_json="",
            deepseek_model="deepseek/test-model",
            deepseek_timeout=123,
            codex_execution_provider="codex-cli",
            codex_execution_provider_json="",
            idea_timeout=45,
            allow_human_override=True,
        )
        stages = build_v2_review_stages(args, RUN_DATE)
        by_name = {name: command for name, command, _timeout in stages}
        self.assertIn("--provider", by_name["deepseek_review"])
        self.assertIn("opencode", by_name["deepseek_review"])
        self.assertIn("--model", by_name["deepseek_review"])
        self.assertIn("deepseek/test-model", by_name["deepseek_review"])
        self.assertIn("--timeout", by_name["deepseek_review"])
        self.assertIn("123", by_name["deepseek_review"])
        self.assertIn("--provider", by_name["codex_execution_review"])
        self.assertIn("codex-cli", by_name["codex_execution_review"])
        self.assertIn("--target-policy", by_name["novelty_scan"])
        self.assertIn("seed-candidates-only", by_name["novelty_scan"])
        self.assertIn("--target-policy", by_name["survival_decision"])
        self.assertIn("--allow-human-override", by_name["survival_decision"])


if __name__ == "__main__":
    unittest.main()
