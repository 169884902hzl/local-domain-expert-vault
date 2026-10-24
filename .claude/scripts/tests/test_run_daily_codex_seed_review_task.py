from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / ".claude" / "scripts" / "run_daily_codex_seed_review_task.ps1"


class TestRunDailyCodexSeedReviewTask(unittest.TestCase):
    def test_wrapper_pins_gpt55_model(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('$CodexModel = "gpt-5.5"', text)
        self.assertIn('"--model"', text)
        self.assertIn('"$CodexModel"', text)

    def test_wrapper_prefers_real_codex_cli_path(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("function Resolve-CodexCliPath", text)
        self.assertIn("CODEX_CLI_PATH", text)
        self.assertIn("OpenAI\\Codex\\bin", text)

    def test_wrapper_logs_selected_model_and_command(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('CODEX model=$CodexModel command=$CodexCommandSource raw_output=$RawOutputPath', text)

    def test_wrapper_uses_mandatory_battle_status_helper(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('codex_seed_review.py" mandatory-battle-status --run-date $ReviewRunDate --json', text)
        self.assertIn('$ExitCode = if ($Wrap.status -eq "done" -and $DebateExit -eq 0) { 0 } else { 1 }', text)

    def test_wrapper_skips_retry_when_output_is_complete(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn('codex_seed_review.py" output-status --run-date $ReviewRunDate --codex-output $Prep.raw_output_path --codex-exit-code $CodexExit --json', text)
        self.assertIn('CODEX nonzero_exit_output_complete exit_code=$CodexExit', text)


if __name__ == "__main__":
    unittest.main()
