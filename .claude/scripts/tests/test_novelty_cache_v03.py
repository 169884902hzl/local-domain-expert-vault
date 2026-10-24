from __future__ import annotations

import json
import urllib.error
from datetime import timedelta
from unittest.mock import patch

from v03_test_helpers import RUN_DATE, V03TempAgendaTest
from novelty_baseline_scan import _cache_file, _fetch_url_cached, _normalized_work, _utc_now
from survival_decision import decide


class NoveltyCacheV03Test(V03TempAgendaTest):
    def test_stale_cache_blocks_active_seed(self) -> None:
        self.write_base_reviews(stale_cache=True)
        self.write_manual_review()
        self.write_baseline_table()
        self.write_pilot_plan()
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="formal")["decisions"][0]
        self.assertFalse(decision["active_seed_allowed"])
        self.assertIn("stale_external_novelty_cache", decision["risks"] + decision["blocks"])

    def test_stale_cache_allowed_only_as_seed_candidate_risk(self) -> None:
        self.write_base_reviews(stale_cache=True)
        decision = decide(run_date=RUN_DATE, allow_human_override=False, target_policy="seed-candidates-only")["decisions"][0]
        self.assertEqual(decision["publish_target"], "seed-candidates")
        self.assertIn("stale_external_novelty_cache", decision["risks"])

    def test_provider_429_and_timeout_fail_closed(self) -> None:
        url = "https://example.test/query"
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(url, 429, "rate", {}, None)):
            payload, summary = _fetch_url_cached("openalex", url, timeout=1, delay_sec=0, query="x")
        self.assertIsNone(payload)
        self.assertEqual(summary["status"], "rate_limited")
        with patch("urllib.request.urlopen", side_effect=TimeoutError("slow")):
            payload, summary = _fetch_url_cached("semantic_scholar", url + "2", timeout=1, delay_sec=0, query="x")
        self.assertIsNone(payload)
        self.assertEqual(summary["status"], "timeout")

    def test_normalized_provider_results_have_required_fields(self) -> None:
        work = _normalized_work(
            source="openalex",
            score=0.4,
            title="A Work",
            work_id="W1",
            year=2099,
            url="https://example.test/W1",
            abstract="Abstract",
            authors=["A"],
            venue="Venue",
        )
        for field in ["work_id", "title", "source", "year", "url", "abstract", "authors", "venue", "overlap_score", "overlap_type", "what_is_already_done", "remaining_delta"]:
            self.assertIn(field, work)

    def test_stale_cache_metadata_is_detected(self) -> None:
        url = "https://example.test/cached"
        path = _cache_file("arxiv_api", url)
        expired = _utc_now() - timedelta(days=1)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"provider": "arxiv_api", "created_at": "2099-01-01T00:00:00+00:00", "expires_at": expired.isoformat(), "ttl_days": 14, "result_count": 1, "payload": {"entries": []}}),
            encoding="utf-8",
        )
        _payload, summary = _fetch_url_cached("arxiv_api", url, timeout=1, delay_sec=0, query="cached")
        self.assertTrue(summary["cached"])
        self.assertEqual(summary["cache_status"], "stale")
