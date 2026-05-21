from __future__ import annotations

import json
from pathlib import Path

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from export_research_run_packet import export_packet
from research_seed_v2_common import publish_dir, read_json, write_json, write_run_artifact


class ExportResearchRunPacketTest(V03TempAgendaTest):
    def test_export_packet_excludes_cache_payload_private_paths_and_secrets(self) -> None:
        fake_secret = "sk-" + "abcdefghijklmnopqrstuvwxyz123456"
        fake_private_path = "H:" + "\\private\\paper.pdf"
        write_run_artifact(
            RUN_DATE,
            "selected-candidates.json",
            {
                "schema_version": "selected_candidates.v1",
                "run_date": RUN_DATE,
                "selected": [
                    {
                        "candidate_id": "cand-alpha",
                        "title": "Packet Candidate",
                        "private_path": fake_private_path,
                        "api_key": fake_secret,
                        "payload": {"cache": "provider body"},
                    }
                ],
                "rejected": [],
                "selection_rules": {},
                "artifact_hashes": {},
            },
            state="portfolio_selected",
        )
        write_json(
            publish_dir(RUN_DATE) / "publish-result.json",
            {
                "schema_version": "publish_result.v1",
                "run_date": RUN_DATE,
                "status": "success",
                "v2_publish_policy": "seed-candidates-only",
                "formal_seed_publish_allowed": False,
                "formal_seed_written": False,
                "formal_rehearsal_written": False,
                "published": [],
                "bucketed": [],
                "blocked": [],
                "artifact_hashes": {},
            },
        )
        write_run_artifact(
            RUN_DATE,
            "active-seed-dashboard.json",
            {
                "schema_version": "active_seed_dashboard.v1",
                "run_date": RUN_DATE,
                "generated_at": "2099-03-04T12:00:00+00:00",
                "source_of_truth": "derived_view_only",
                "rows": [
                    {
                        "candidate_id": "cand-alpha",
                        "title": "Packet Candidate",
                        "current_state": "seed_candidate",
                        "formal_rehearsal_allowed": False,
                        "active_seed_allowed": False,
                        "pilot_ready_allowed": False,
                        "risk_markers": [],
                        "blocking_reasons": [],
                    }
                ],
                "source_artifact_hashes": {},
                "boundary": "derived",
            },
            state="active_seed_dashboard_rendered",
        )
        write_json(
            Path(self.tmp.name) / "pilots" / "packet-candidate" / "feedback-to-strategy.json",
            {
                "schema_version": "pilot_feedback.v1",
                "seed_slug": "packet-candidate",
                "candidate_id": "cand-alpha",
                "strategy_update": {"penalize_patterns": ["weak"], "cannot_weaken_hard_gates": True},
                "raw_payload": {"token": fake_secret},
            },
        )
        manifest = export_packet(RUN_DATE)
        packet_dir = Path(self.tmp.name) / "runs" / RUN_DATE / "publish" / "run-packet"
        self.assertIn("selected-candidates.json", manifest["included"])
        self.assertIn("active-seed-dashboard.json", manifest["included"])
        self.assertIn("pilot-artifacts.json", manifest["included"])
        selected = read_json(packet_dir / "selected-candidates.json")
        text = json.dumps(selected, ensure_ascii=False)
        self.assertNotIn(fake_secret, text)
        self.assertNotIn("provider body", text)
        self.assertNotIn(fake_private_path, text)
        pilot_text = json.dumps(read_json(packet_dir / "pilot-artifacts.json"), ensure_ascii=False)
        self.assertNotIn(fake_secret, pilot_text)
        self.assertIn("[redacted]", pilot_text)
        self.assertIn("[redacted]", text)
        self.assertIn("[redacted-private-path]", text)
        packet_manifest = read_json(packet_dir / "manifest.json")
        self.assertIn("provider cache payloads", packet_manifest["excluded"])

    def test_export_packet_dry_run_writes_nothing(self) -> None:
        manifest = export_packet(RUN_DATE, dry_run=True)
        self.assertNotIn("packet_dir", manifest)
        self.assertFalse((Path(self.tmp.name) / "runs" / RUN_DATE / "publish" / "run-packet").exists())
