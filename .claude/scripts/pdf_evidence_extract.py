"""Build best-effort PDF/table/figure evidence anchors without touching raw files."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from research_seed_v2_common import agenda_v2_path, artifact_dir, artifact_hashes, ensure_v2_dirs, load_jsonl, write_jsonl, write_run_artifact


PDF_VERIFIED_ANCHOR_SOURCES = {"pdf_text", "pdf_table", "pdf_figure_caption", "manual_pdf_locator", "result_row"}


def _anchor_id(paper_id: str, anchor_type: str, text: str) -> str:
    basis = f"{paper_id}|{anchor_type}|{' '.join(text.lower().split())}"
    return "anchor-" + hashlib.sha1(basis.encode("utf-8")).hexdigest()[:16]


def _rel_or_empty(path_text: Any) -> str:
    text = str(path_text or "").strip()
    if not text:
        return ""
    path = Path(text)
    if path.is_absolute():
        try:
            return str(path.relative_to(vault_path())).replace("\\", "/")
        except ValueError:
            return ""
    return text.replace("\\", "/")


def _source_pdf_for_paper(paper: dict[str, Any]) -> str:
    for key in ["source_pdf", "pdf_path", "attachment_pdf"]:
        value = _rel_or_empty(paper.get(key))
        if value:
            return value
    return ""


def _note_anchor(paper_id: str, claim: dict[str, Any]) -> dict[str, Any] | None:
    anchor = claim.get("anchor", {}) if isinstance(claim.get("anchor"), dict) else {}
    snippet = str(anchor.get("snippet") or claim.get("statement") or "").strip()
    section = str(anchor.get("section") or "").strip()
    if not snippet and not section:
        return None
    anchor_type = str(anchor.get("anchor_type") or claim.get("anchor_type") or "snippet")
    if anchor_type == "note_only":
        anchor_type = "snippet"
    return {
        "anchor_id": _anchor_id(paper_id, anchor_type, f"{section} {snippet}"),
        "anchor_type": anchor_type if anchor_type in {"section", "figure", "table", "caption", "result_row", "snippet"} else "snippet",
        "anchor_source": "note_section",
        "section": section,
        "figure": "",
        "table": "",
        "page": anchor.get("pdf_page", None),
        "snippet": snippet[:600],
        "extraction_method": "note_section",
        "confidence": "medium" if anchor_type in {"section", "snippet", "table", "figure"} else "low",
        "requires_human_check": bool(claim.get("requires_human_check", True)),
    }


def is_pdf_verified_anchor(anchor: dict[str, Any]) -> bool:
    if str(anchor.get("anchor_source")) not in PDF_VERIFIED_ANCHOR_SOURCES:
        return False
    if anchor.get("anchor_type") == "result_row":
        return validate_result_row_anchor(anchor) == []
    return bool((anchor.get("page") or anchor.get("section")) and (anchor.get("snippet") or anchor.get("row_text") or anchor.get("row_cells")))


def validate_result_row_anchor(anchor: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in ["page", "row_index", "row_text", "metric_name", "baseline_name", "reported_value", "task_or_dataset"]:
        value = anchor.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append(f"result_row_missing_{field}")
    if str(anchor.get("anchor_source")) not in {"pdf_table", "manual_pdf_locator", "result_row"}:
        errors.append("result_row_anchor_source_not_pdf_or_manual")
    return errors


def _pdf_text_anchors(paper_id: str, source_pdf: str) -> list[dict[str, Any]]:
    path = vault_path(source_pdf) if source_pdf else Path()
    if not source_pdf or not path.exists() or path.suffix.lower() != ".pdf":
        return []
    try:
        import pdfplumber  # type: ignore[import-not-found]
    except Exception:
        return []
    anchors: list[dict[str, Any]] = []
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page_index, page in enumerate(pdf.pages[:3], start=1):
                text = " ".join((page.extract_text() or "").split())
                if text:
                    snippet = text[:600]
                    anchors.append(
                        {
                            "anchor_id": _anchor_id(paper_id, "snippet", f"{page_index}:{snippet}"),
                            "anchor_type": "snippet",
                            "anchor_source": "pdf_text",
                            "section": "",
                            "figure": "",
                            "table": "",
                            "page": page_index,
                            "snippet": snippet,
                            "extraction_method": "pdfplumber",
                            "confidence": "medium",
                            "requires_human_check": True,
                        }
                    )
                for table_index, table in enumerate(page.extract_tables() or [], start=1):
                    for row_index, row in enumerate(table or []):
                        cells = [str(cell or "").strip() for cell in row or []]
                        row_text = " | ".join(cell for cell in cells if cell)
                        if not row_text:
                            continue
                        anchors.append(
                            {
                                "anchor_id": _anchor_id(paper_id, "table", f"{page_index}:{table_index}:{row_index}:{row_text}"),
                                "anchor_type": "table",
                                "anchor_source": "pdf_table",
                                "section": "",
                                "figure": "",
                                "table": f"table-{table_index}",
                                "page": page_index,
                                "snippet": row_text[:600],
                                "row_index": row_index,
                                "row_text": row_text[:600],
                                "row_cells": cells,
                                "extraction_method": "pdfplumber",
                                "confidence": "medium",
                                "requires_human_check": True,
                            }
                        )
    except Exception:
        return anchors
    return anchors


def build_anchor_records(primitives: list[dict[str, Any]], *, run_date: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for paper in primitives:
        paper_id = str(paper.get("paper_key") or Path(str(paper.get("source_note", ""))).stem)
        source_pdf = _source_pdf_for_paper(paper)
        anchors: list[dict[str, Any]] = []
        for claim in paper.get("claims", []):
            if isinstance(claim, dict):
                note_anchor = _note_anchor(paper_id, claim)
                if note_anchor:
                    anchors.append(note_anchor)
        anchors.extend(_pdf_text_anchors(paper_id, source_pdf))
        records.append(
            {
                "schema_version": "pdf_evidence_anchors.v1",
                "run_date": run_date,
                "paper_id": paper_id,
                "source_pdf": source_pdf,
                "source_note": str(paper.get("source_note", "")),
                "anchors": anchors,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    ensure_v2_dirs(args.run_date)
    primitives_path = artifact_dir(args.run_date) / "paper-primitives-snapshot.jsonl"
    primitives = load_jsonl(primitives_path) if primitives_path.exists() else []
    records = build_anchor_records(primitives, run_date=args.run_date)
    payload = {
        "schema_version": "pdf_evidence_anchors.v1",
        "run_date": args.run_date,
        "records": records,
        "artifact_hashes": artifact_hashes(args.run_date, ["paper-primitives-snapshot.jsonl"]),
        "boundary": "Best-effort extraction only; note_section anchors are not PDF/table verified evidence.",
    }
    write_run_artifact(args.run_date, "pdf-evidence-anchors.json", payload, state="pdf_evidence_anchored", dry_run=args.dry_run)
    write_jsonl(agenda_v2_path("evidence", "pdf_evidence_anchors.jsonl"), records, dry_run=args.dry_run)
    safe_print(f"PDF_EVIDENCE_ANCHORS: papers={len(records)} anchors={sum(len(item.get('anchors', [])) for item in records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
