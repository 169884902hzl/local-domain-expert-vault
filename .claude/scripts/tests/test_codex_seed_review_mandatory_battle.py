from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import codex_seed_review as codex_review
from research_seed_v2_common import artifact_dir


RUN_DATE = "2099-01-02"


class CodexSeedReviewMandatoryBattleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.old_root = os.environ.get("RESEARCH_SEED_V2_AGENDA_ROOT")
        os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = str(self.root)
        self.review_dir = self.root / "reviews"
        self.model_debates_dir = self.root / "model-debates"
        self.review_dir.mkdir(parents=True, exist_ok=True)
        self.model_debates_dir.mkdir(parents=True, exist_ok=True)
        artifact_dir(RUN_DATE).mkdir(parents=True, exist_ok=True)
        self._patches = [
            patch.object(codex_review, "REVIEWS_DIR", self.review_dir),
            patch.object(codex_review, "DAILY_DIR", self.root / "projects" / "arxiv-daily"),
            patch.object(codex_review, "vault_path", side_effect=self._agenda_path),
            patch.object(codex_review, "agenda_path", side_effect=self._agenda_path),
            patch.object(codex_review, "rel", side_effect=self._rel),
        ]
        for handle in self._patches:
            handle.start()

    def tearDown(self) -> None:
        for handle in reversed(self._patches):
            handle.stop()
        if self.old_root is None:
            os.environ.pop("RESEARCH_SEED_V2_AGENDA_ROOT", None)
        else:
            os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = self.old_root
        self.tmp.cleanup()

    def _agenda_path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    def _rel(self, path: Path) -> str:
        target = Path(path).resolve()
        root = self.root.resolve()
        try:
            return str(target.relative_to(root)).replace("\\", "/")
        except ValueError:
            return str(target).replace("\\", "/")

    def _write_json(self, path: Path, payload: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_accepts_legacy_battle_packet_success(self) -> None:
        packet = self.model_debates_dir / f"{RUN_DATE}-gemini-deepseek-debate-packet.json"
        self._write_json(
            packet,
            {
                "status": "success",
                "counts": {
                    "selected_items": 3,
                    "deepseek_reviews": 3,
                    "gemini_mutations": 2,
                },
            },
        )
        result = codex_review.mandatory_battle_status(RUN_DATE)
        self.assertEqual(result["allow_for_codex_completion"], "true")
        self.assertEqual(result["effective_mode"], "legacy_mandatory_battle_packet")
        self.assertEqual(result["status"], "success")

    def test_accepts_moved_to_v2_with_provider_backed_deepseek(self) -> None:
        pending = self.review_dir / f"{RUN_DATE}-codex-review-pending.json"
        self._write_json(
            pending,
            {
                "mandatory_model_battle_status": "moved_to_v2_state_machine",
            },
        )
        deepseek = artifact_dir(RUN_DATE) / "deepseek-review.json"
        self._write_json(
            deepseek,
            {
                "status": "success",
                "provider_status": {
                    "mode": "opencode",
                    "provider_backed": True,
                },
                "reviews": [{"candidate_id": "cand-1"}],
            },
        )
        result = codex_review.mandatory_battle_status(RUN_DATE)
        self.assertEqual(result["allow_for_codex_completion"], "true")
        self.assertEqual(result["effective_mode"], "moved_to_v2_state_machine")
        self.assertEqual(result["reason"], "moved_to_v2_covered_by_v2_deepseek_review")
        self.assertTrue(result["effective_evidence_path"].endswith("runs/2099-01-02/artifacts/deepseek-review.json"))

    def test_accepts_moved_to_v2_from_daily_run_when_pending_missing(self) -> None:
        daily_run = self.root / "projects" / "arxiv-daily" / f"{RUN_DATE}-run.md"
        daily_run.parent.mkdir(parents=True, exist_ok=True)
        daily_run.write_text(
            "MANDATORY_MODEL_BATTLE: moved_to_v2_state_machine report=-\n",
            encoding="utf-8",
        )
        deepseek = artifact_dir(RUN_DATE) / "deepseek-review.json"
        self._write_json(
            deepseek,
            {
                "status": "success",
                "provider_status": {
                    "mode": "opencode",
                    "provider_backed": True,
                },
                "reviews": [{"candidate_id": "cand-1"}],
            },
        )
        result = codex_review.mandatory_battle_status(RUN_DATE)
        self.assertEqual(result["status"], "moved_to_v2_state_machine")
        self.assertEqual(result["allow_for_codex_completion"], "true")
        self.assertEqual(result["reason"], "moved_to_v2_covered_by_v2_deepseek_review")

    def test_rejects_moved_to_v2_without_v2_deepseek_review(self) -> None:
        pending = self.review_dir / f"{RUN_DATE}-codex-review-pending.json"
        self._write_json(
            pending,
            {
                "mandatory_model_battle_status": "moved_to_v2_state_machine",
            },
        )
        result = codex_review.mandatory_battle_status(RUN_DATE)
        self.assertEqual(result["allow_for_codex_completion"], "false")
        self.assertEqual(result["effective_mode"], "moved_to_v2_state_machine")
        self.assertEqual(result["reason"], "moved_to_v2_missing_v2_deepseek_review")

    def test_output_status_treats_complete_raw_with_telemetry_tail_as_done(self) -> None:
        raw = self.review_dir / f"{RUN_DATE}-codex-seed-review.raw.md"
        raw.write_text(
            "\n".join(
                [
                    "# Daily Codex Seed Review - 2099-01-02",
                    "",
                    "## Executive Verdict",
                    "",
                    "- status: `done`",
                    "- boundary: no paper claim is accepted; user remains final reviewer.",
                    "",
                    "## Shortlist For User",
                    "",
                    "1. Example Candidate",
                    "   - action: `rewrite`",
                    "",
                    "## Creativity Preservation",
                    "",
                    "- Example Candidate: rescue_signal: keep the mechanism.",
                    "",
                    "## Next 24 Hours",
                    "",
                    "1. Keep the rewrite path.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        err = self.review_dir / f"{RUN_DATE}-codex-seed-review.err.log"
        err.write_text(
            "2026-05-28T09:24:01Z ERROR opentelemetry_sdk: 127.0.0.1:4318 connect refused",
            encoding="utf-8",
        )
        result = codex_review.codex_output_status(RUN_DATE, raw, 1)
        self.assertEqual(result["status"], "done")
        self.assertEqual(result["raw_output_exists"], "true")
        self.assertEqual(result["output_complete"], "true")
        self.assertEqual(result["codex_exit_nonblocking"], "true")
        self.assertEqual(result["codex_nonblocking_exit_reason"], "post_output_telemetry_error")

    def test_resolve_mandatory_battle_note_rewrites_stale_partial_text(self) -> None:
        pending = self.review_dir / f"{RUN_DATE}-codex-review-pending.json"
        self._write_json(
            pending,
            {
                "mandatory_model_battle_status": "moved_to_v2_state_machine",
            },
        )
        deepseek = artifact_dir(RUN_DATE) / "deepseek-review.json"
        self._write_json(
            deepseek,
            {
                "status": "success",
                "provider_status": {
                    "mode": "opencode",
                    "provider_backed": True,
                },
                "reviews": [{"candidate_id": "cand-1"}],
            },
        )
        body = "\n".join(
            [
                "## Executive Verdict",
                "",
                "- daily_idea_stage: `partial`, because `mandatory_model_battle` is required but the packet only reports `moved_to_v2_state_machine` with no battle packet, report, DeepSeek reviews, provider status, or mutation actions.",
                "",
                "## Watchlist",
                "",
                "- Mandatory battle is unverified in this packet; acceptance should wait for DeepSeek novelty, baseline, mechanism, evaluation, and scope attacks.",
                "",
            ]
        )
        updated = codex_review._resolve_mandatory_battle_note(RUN_DATE, body)
        self.assertIn("- daily_idea_stage: `done`, because `mandatory_model_battle` is satisfied by provider-backed v2 DeepSeek review coverage under `moved_to_v2_state_machine`.", updated)
        self.assertIn("- Mandatory battle is satisfied via provider-backed v2 DeepSeek review; acceptance still requires human review and no-hardware pilot pressure.", updated)

    def test_resolve_mandatory_battle_note_rewrites_legacy_packet_language(self) -> None:
        daily_run = self.root / "projects" / "arxiv-daily" / f"{RUN_DATE}-run.md"
        daily_run.parent.mkdir(parents=True, exist_ok=True)
        daily_run.write_text(
            "MANDATORY_MODEL_BATTLE: moved_to_v2_state_machine report=-\n",
            encoding="utf-8",
        )
        deepseek = artifact_dir(RUN_DATE) / "deepseek-review.json"
        self._write_json(
            deepseek,
            {
                "status": "success",
                "provider_status": {
                    "mode": "opencode",
                    "provider_backed": True,
                },
                "reviews": [{"candidate_id": "cand-1"}],
            },
        )
        body = "\n".join(
            [
                "## Executive Verdict",
                "",
                "- top_decision: `no_accept_today`; daily idea stage is partial because the mandatory DeepSeek/OpenCode battle has no embedded review artifacts in the packet.",
                "The daily idea stage is `partial` because the packet contains zero raw Gemini candidates, zero today mechanism seed candidates, empty greenhouse metadata, and no readable mandatory DeepSeek/OpenCode battle artifact.",
                "",
                "## Watchlist",
                "",
                "- Mandatory battle is not evidenced in the packet. The field says required, but review/report/provider fields are empty. Treat the daily idea stage as partial and do not accept seeds today.",
                "- mandatory battle risk: `mandatory_model_battle.required` is true, but the packet only reports `status: moved_to_v2_state_machine` and has empty paths, reviews, mutations, provider status, and excerpt. This is not a clean daily idea stage.",
                "",
            ]
        )
        updated = codex_review._resolve_mandatory_battle_note(RUN_DATE, body)
        self.assertIn("- top_decision: `no_accept_today`; mandatory battle is satisfied via provider-backed v2 DeepSeek review, but no candidate clears acceptance today.", updated)
        self.assertIn("The daily idea stage remains `partial` because the packet contains zero raw Gemini candidates, zero today mechanism seed candidates, and empty greenhouse metadata; mandatory battle itself is satisfied via provider-backed v2 DeepSeek review.", updated)
        self.assertIn("- Mandatory battle is satisfied via provider-backed v2 DeepSeek review. The packet still omits embedded legacy battle fields, so acceptance should remain conservative and human-reviewed.", updated)
        self.assertIn("- mandatory battle is satisfied via provider-backed v2 DeepSeek review, but the packet still omits embedded legacy battle fields; treat this as a packet completeness issue, not a failed adversarial review.", updated)

    def test_resolve_mandatory_battle_note_rewrites_packet_scope_partial_language(self) -> None:
        daily_run = self.root / "projects" / "arxiv-daily" / f"{RUN_DATE}-run.md"
        daily_run.parent.mkdir(parents=True, exist_ok=True)
        daily_run.write_text(
            "MANDATORY_MODEL_BATTLE: moved_to_v2_state_machine report=-\n",
            encoding="utf-8",
        )
        deepseek = artifact_dir(RUN_DATE) / "deepseek-review.json"
        self._write_json(
            deepseek,
            {
                "status": "success",
                "provider_status": {
                    "mode": "opencode",
                    "provider_backed": True,
                },
                "reviews": [{"candidate_id": "cand-1"}],
            },
        )
        body = "\n".join(
            [
                "## Executive Verdict",
                "",
                "- top_decision: daily idea stage is `partial`, not clean. The packet has 8 raw Gemini survivors, 0 promoted mechanism seeds, and the required DeepSeek battle has no report path, selected items, review excerpt, provider status, or mutation trace in this packet. Therefore no candidate should be accepted as a paper claim today. Best outcome is one rewrite cluster for contact-topology interruption, one merge into the existing critic-memory focus track, and several parked rescue signals.",
                "",
                "## Watchlist",
                "",
                "- Mandatory DeepSeek battle is not evidenced in the packet; daily stage remains `partial`.",
                "- why_not_now: duplicate pressure from existing critic-memory seeds and no clean mandatory battle trace.",
                "",
                "## Next 24 Hours",
                "",
                "5. Do not promote any seed until the DeepSeek battle trace is present or explicitly marked unavailable with a recovery path.",
                "",
            ]
        )
        updated = codex_review._resolve_mandatory_battle_note(RUN_DATE, body)
        self.assertIn(
            "- top_decision: daily idea stage remains `partial` because the packet has 8 raw Gemini survivors and 0 promoted mechanism seeds; mandatory battle itself is satisfied via provider-backed v2 DeepSeek review, but the packet omits embedded legacy battle fields such as selected items, review excerpt, provider status, and mutation trace.",
            updated,
        )
        self.assertIn(
            "- Mandatory DeepSeek battle is satisfied via provider-backed v2 DeepSeek review; daily stage remains `partial` only because the packet is missing embedded legacy battle fields and promoted mechanism seeds.",
            updated,
        )
        self.assertIn(
            "- why_not_now: duplicate pressure from existing critic-memory seeds and no embedded legacy battle trace in the packet, even though provider-backed v2 DeepSeek review exists.",
            updated,
        )
        self.assertIn(
            "5. Do not promote any seed until the packet embeds the v2 DeepSeek review trace or explicitly records the fallback recovery path; treat missing embedded legacy fields as a packet completeness issue, not a failed adversarial review.",
            updated,
        )


if __name__ == "__main__":
    unittest.main()
