from __future__ import annotations

import unittest
import urllib.error
from unittest.mock import patch

from v03_test_helpers import SCRIPTS_DIR  # noqa: F401

import daily_arxiv_pipeline as pipeline
import historical_arxiv_backfill as backfill
import zotero_import
from arxiv_ranker import ArxivPaper, RankedPaper


def ranked_fixture() -> RankedPaper:
    return RankedPaper(
        paper=ArxivPaper(
            arxiv_id="2606.00001",
            title="Fixture Robot Paper",
            authors=["Ada Example"],
            summary="A fixture abstract.",
            published="2026-06-07",
            updated="2026-06-07",
            url="https://arxiv.org/abs/2606.00001",
            pdf_url="https://arxiv.org/pdf/2606.00001",
            categories=["cs.RO"],
            primary_category="cs.RO",
        ),
        quality_score=91,
        decision="top1_candidate",
        reasons=["fixture"],
        matched_terms=["robot"],
        penalties=[],
    )


class ZoteroImportPdfPendingTest(unittest.TestCase):
    def test_pdf_download_tries_alternate_url_when_first_url_is_not_pdf(self) -> None:
        class FakeResponse:
            def __init__(self, body: bytes) -> None:
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *_args) -> None:
                return None

            def read(self) -> bytes:
                return self.body

        seen_urls: list[str] = []

        def fake_urlopen(req, **_kwargs):
            seen_urls.append(req.full_url)
            if len(seen_urls) == 1:
                return FakeResponse(b"<html>bad gateway</html>")
            return FakeResponse(b"%PDF-1.7\nfixture")

        with patch.object(zotero_import.urllib.request, "urlopen", side_effect=fake_urlopen):
            data = zotero_import._download_pdf_bytes(ranked_fixture(), timeout=1)

        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreaterEqual(len(seen_urls), 2)
        self.assertEqual(seen_urls[0], "https://arxiv.org/pdf/2606.00001")

    def test_local_connector_preserves_created_item_when_pdf_download_fails(self) -> None:
        calls: list[str] = []

        def post_json(path: str, *_args, **_kwargs):
            calls.append(path)
            if path == "/connector/saveItems":
                return 201, {}, b""
            if path == "/connector/updateSession":
                return 200, {}, b""
            raise AssertionError(f"unexpected connector path: {path}")

        http_502 = urllib.error.HTTPError(
            "https://arxiv.org/pdf/2606.00001",
            502,
            "Bad Gateway",
            hdrs=None,
            fp=None,
        )

        with (
            patch.object(
                zotero_import,
                "connector_preflight",
                return_value={"reachable": True, "files_editable": True, "collection_tree_id": "C123", "errors": []},
            ),
            patch.object(zotero_import, "_post_connector_json", side_effect=post_json),
            patch.object(zotero_import, "_download_pdf_bytes", side_effect=http_502),
            patch.object(
                zotero_import,
                "wait_for_existing_paper",
                return_value=zotero_import.ImportResult(
                    status="exists",
                    zotero_key="NEWKEY12",
                    message="matched existing Zotero item",
                    mode="local_read",
                    existing=True,
                ),
            ),
            patch.object(zotero_import, "_post_connector_bytes") as post_bytes,
        ):
            result = zotero_import.create_item_local_connector(ranked_fixture(), collection_key="COLLKEY")

        self.assertEqual(calls, ["/connector/saveItems", "/connector/updateSession"])
        post_bytes.assert_not_called()
        self.assertEqual(result.status, "pdf_pending")
        self.assertEqual(result.zotero_key, "NEWKEY12")
        self.assertEqual(result.mode, "local_connector")
        self.assertIn("created via Zotero local connector", result.message)
        self.assertIn("stored_pdf_required_failed:download:HTTPError:HTTP Error 502: Bad Gateway", result.message)

    def test_pdf_pending_can_enter_daily_and_backfill_read_flow(self) -> None:
        self.assertIn("pdf_pending", pipeline.NEW_IMPORT_STATUSES)
        self.assertIn("pdf_pending", pipeline.INGEST_READY_STATUSES)
        self.assertIn("pdf_pending", backfill.NEW_IMPORT_STATUSES)


if __name__ == "__main__":
    unittest.main()
