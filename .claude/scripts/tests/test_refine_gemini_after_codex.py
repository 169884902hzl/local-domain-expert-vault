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

import refine_gemini_after_codex as refine


class RefineGeminiAfterCodexPathResolutionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.old_root = os.environ.get("RESEARCH_SEED_V2_AGENDA_ROOT")
        os.environ["RESEARCH_SEED_V2_AGENDA_ROOT"] = str(self.root)
        self.reviews_dir = self.root / "projects" / "research-agenda" / "reviews"
        self.reviews_dir.mkdir(parents=True, exist_ok=True)
        self._patches = [
            patch.object(refine, "REVIEWS_DIR", self.reviews_dir),
            patch.object(refine, "vault_path", side_effect=self._vault_path),
            patch.object(refine, "rel", side_effect=self._rel),
            patch.object(refine, "safe_write", side_effect=self._safe_write),
            patch.object(
                refine,
                "run_gemini_cli",
                return_value={
                    "provider": "gemini-cli",
                    "requested_model": "gemini-test",
                    "effective_model": "gemini-test",
                    "effective_fallback": False,
                    "exit_code": 1,
                    "timed_out": False,
                    "error": "stubbed_failure",
                    "clean_output": "",
                },
            ),
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

    def _vault_path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    def _rel(self, path: Path) -> str:
        target = Path(path).resolve()
        root = self.root.resolve()
        try:
            return str(target.relative_to(root)).replace("\\", "/")
        except ValueError:
            return str(target).replace("\\", "/")

    def _safe_write(self, path: Path, content: str, backup: bool = True) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def test_run_refinement_resolves_relative_cli_paths(self) -> None:
        input_packet = self.root / "projects" / "research-agenda" / "reviews" / "input-packet.json"
        codex_report = self.root / "projects" / "research-agenda" / "reviews" / "codex-report.md"
        input_packet.write_text(
            json.dumps(
                {
                    "raw_gemini_candidates": [
                        {
                            "title": "Example Candidate",
                            "title_zh": "示例候选",
                            "greenhouse_label": "rewrite_needed",
                            "mechanism": "Mechanism summary.",
                            "hypothesis": "If pathology P exists, then mechanism M should help.",
                            "physical_failure_scene": "Contact failure.",
                            "core_insight": "Core insight.",
                            "interface_innovation": "Interface.",
                            "optimization_space": "Optimization.",
                            "anti_combination_test": "This is not a simple A+B combination because it changes the control interface.",
                            "strongest_baseline": "Strong baseline.",
                            "baseline_kill_table": "Kill table.",
                            "minimum_no_hardware_pilot": "Pilot.",
                            "reviewer_pre_mortem": "Decision.",
                            "negative_claim_boundary": "Boundary.",
                            "lab_fit": "DLO tactile lab fit.",
                            "what_would_make_this_not_a_paper": "Risk.",
                            "rescue_mutation": "Mutation.",
                        }
                    ]
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        codex_report.write_text("# Codex Report\n", encoding="utf-8")

        result = refine.run_refinement(
            input_packet=Path("projects/research-agenda/reviews/input-packet.json"),
            output_root=Path("projects/research-agenda/post-codex-gemini-refinements"),
            actions={"rewrite"},
            max_items=1,
            model="gemini-test",
            timeout_sec=1,
            dry_run=False,
            codex_report=Path("projects/research-agenda/reviews/codex-report.md"),
        )

        self.assertTrue(str(result["status"]).startswith("fallback:"))
        self.assertEqual(result["selected_items"], 1)
        self.assertTrue((self.root / "projects" / "research-agenda" / "post-codex-gemini-refinements").exists())
        self.assertTrue(str(result["packet_path"]).startswith("projects/research-agenda/post-codex-gemini-refinements/"))


if __name__ == "__main__":
    unittest.main()
