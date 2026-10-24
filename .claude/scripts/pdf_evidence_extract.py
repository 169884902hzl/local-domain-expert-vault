"""Build best-effort PDF/table/figure evidence anchors without touching raw files."""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from kb_common import safe_print, vault_path
from research_seed_v2_common import agenda_v2_path, artifact_dir, artifact_hashes, ensure_v2_dirs, load_jsonl, write_jsonl, write_run_artifact


PDF_VERIFIED_ANCHOR_SOURCES = {"pdf_text", "pdf_table", "pdf_figure_caption", "manual_pdf_locator", "result_row"}

SECTION_PATTERNS: list[tuple[str, list[str]]] = [
    ("Abstract", [r"abstract"]),
    ("Introduction", [r"(?:\d+|i)\.?\s+introduction", r"introduction"]),
    ("Method", [
        r"(?:\d+|ii|iii|iv)\.?\s+(?!related|background|preliminar|dataset|experiment|evaluation|result)(method|methodology|approach|framework|model|system)",
        r"(?!related|background|preliminar|dataset|experiment|evaluation|result)(method|methodology|approach|proposed method|framework)",
    ]),
    ("Experiments", [r"(?:\d+|iv|v)\.?\s+(experiments?|evaluation|results?)", r"experiments?", r"evaluation", r"results?"]),
    ("Conclusion", [r"(?:\d+|v|vi)\.?\s+(conclusion|discussion)", r"conclusion", r"discussion"]),
]


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
        "anchor_type": anchor_type if anchor_type in {"section", "figure", "table", "appendix", "caption", "result_row", "snippet"} else "snippet",
        "anchor_source": "note_section",
        "section": section,
        "figure": "",
        "table": "",
        "page": anchor.get("pdf_page", None),
        "snippet": snippet[:600],
        "extraction_method": "note_section",
        "confidence": "medium" if anchor_type in {"section", "snippet", "table", "figure", "appendix"} else "low",
        "requires_human_check": bool(claim.get("requires_human_check", True)),
        "manual_confirmed": False,
        "confirmed_by": "",
        "confirmed_at": "",
        "validated_metric": "",
        "validated_baseline": "",
        "validated_task": "",
        "confirmation_note": "",
    }


def is_pdf_verified_anchor(anchor: dict[str, Any]) -> bool:
    if str(anchor.get("anchor_source")) not in PDF_VERIFIED_ANCHOR_SOURCES:
        return False
    if anchor.get("anchor_type") == "result_row":
        return validate_result_row_anchor(anchor) == [] and result_row_manual_confirmed(anchor)
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


def result_row_manual_confirmed(anchor: dict[str, Any]) -> bool:
    return bool(
        anchor.get("manual_confirmed") is True
        and str(anchor.get("confirmed_by", "")).strip()
        and str(anchor.get("confirmed_at", "")).strip()
        and str(anchor.get("confirmation_note", "")).strip()
    )


def _pdf_text_anchors(paper_id: str, source_pdf: str) -> list[dict[str, Any]]:
    path = vault_path(source_pdf) if source_pdf else Path()
    if not source_pdf or not path.exists() or path.suffix.lower() != ".pdf":
        return []
    try:
        anchors = _fitz_text_anchors(paper_id, path)
    except (ImportError, ModuleNotFoundError):
        anchors = []
    except Exception as exc:
        _pdf_extract_warning("pymupdf_text", exc)
        anchors = []
    if anchors:
        anchors.extend(_pdfplumber_table_anchors(paper_id, path))
        return anchors
    return _pdfplumber_text_and_table_anchors(paper_id, path)


def _pdf_extract_warning(stage: str, exc: Exception) -> None:
    print(f"PDF_EXTRACT_DEGRADED:{stage}:{type(exc).__name__}:{exc}", file=sys.stderr)


def _normalize_line(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _noise_key(text: str) -> str:
    return re.sub(r"\d+", "#", _normalize_line(text).lower())


def _fitz_blocks(path: Path) -> tuple[list[dict[str, Any]], int]:
    import fitz  # type: ignore[import-not-found]

    blocks: list[dict[str, Any]] = []
    with fitz.open(str(path)) as doc:
        page_count = len(doc)
        for page_index, page in enumerate(doc, start=1):
            data = page.get_text("dict")
            for block in data.get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    spans = line.get("spans", [])
                    text = _normalize_line(" ".join(str(span.get("text", "")) for span in spans))
                    if not text:
                        continue
                    sizes = [float(span.get("size") or 0.0) for span in spans]
                    fonts = " ".join(str(span.get("font", "")).lower() for span in spans)
                    flags = [int(span.get("flags") or 0) for span in spans]
                    bbox = line.get("bbox") or block.get("bbox") or [0, 0, 0, 0]
                    blocks.append(
                        {
                            "page": page_index,
                            "text": text,
                            "font_size": max(sizes) if sizes else 0.0,
                            "is_bold": "bold" in fonts or any(flag & 2 for flag in flags),
                            "y0": float(bbox[1]) if len(bbox) > 1 else 0.0,
                        }
                    )
    return blocks, page_count


def _drop_repeated_noise(blocks: list[dict[str, Any]], page_count: int) -> list[dict[str, Any]]:
    counts = Counter(_noise_key(block["text"]) for block in blocks if len(block["text"]) >= 4)
    threshold = max(2, page_count // 2)
    cleaned = []
    for block in blocks:
        key = _noise_key(block["text"])
        if block["page"] != 1 and counts.get(key, 0) >= threshold and len(key) < 120:
            continue
        cleaned.append(block)
    return cleaned


def _section_label(text: str, *, font_ok: bool, structural_ok: bool) -> str:
    if not (font_ok or structural_ok):
        return ""
    normalized = re.sub(r"\s+", " ", text.strip().lower().rstrip(":"))
    if len(normalized) > 120 or normalized.endswith("."):
        return ""
    for label, patterns in SECTION_PATTERNS:
        for pattern in patterns:
            if re.fullmatch(pattern, normalized, flags=re.IGNORECASE):
                return label
    return ""


def _classified_sections(blocks: list[dict[str, Any]]) -> list[tuple[int, str]]:
    sections: list[tuple[int, str]] = []
    for index, block in enumerate(blocks):
        text = str(block["text"])
        font_ok = float(block.get("font_size") or 0.0) >= 11.0 or bool(block.get("is_bold"))
        structural_ok = len(text) < 100 and not text.endswith(".")
        label = _section_label(text, font_ok=font_ok, structural_ok=structural_ok)
        if label:
            sections.append((index, label))
    return sections


def _fitz_text_anchors(paper_id: str, path: Path) -> list[dict[str, Any]]:
    blocks, page_count = _fitz_blocks(path)
    blocks = _drop_repeated_noise(blocks, page_count)
    sections = _classified_sections(blocks)
    anchors: list[dict[str, Any]] = []
    seen_sections: set[str] = set()
    for position, label in sections:
        if label in seen_sections:
            continue
        next_position = next((next_pos for next_pos, _next_label in sections if next_pos > position), len(blocks))
        body_blocks = blocks[position + 1 : next_position]
        lines = [str(block["text"]) for block in body_blocks if len(str(block["text"])) >= 8]
        if not lines:
            continue
        snippet = " ".join(lines)[:600]
        page = int(blocks[position].get("page") or 1)
        anchors.append(
            {
                "anchor_id": _anchor_id(paper_id, "section", f"{label}:{page}:{snippet}"),
                "anchor_type": "section",
                "anchor_source": "pdf_text",
                "section": label,
                "figure": "",
                "table": "",
                "page": page,
                "snippet": snippet,
                "extraction_method": "pdf_text",
                "confidence": "medium",
                "requires_human_check": True,
                "extension_metadata": {"section_extractor": "pymupdf_font_or_structure"},
            }
        )
        seen_sections.add(label)
    if anchors:
        return anchors
    page_lines: dict[int, list[str]] = {}
    for block in blocks:
        text = str(block["text"])
        if len(text) >= 8:
            page_lines.setdefault(int(block.get("page") or 1), []).append(text)
    for page, lines in sorted(page_lines.items()):
        snippet = " ".join(lines)[:600]
        if not snippet:
            continue
        anchors.append(
            {
                "anchor_id": _anchor_id(paper_id, "snippet", f"fallback:{page}:{snippet}"),
                "anchor_type": "snippet",
                "anchor_source": "pdf_text",
                "section": "Full Text (non-standard format fallback)",
                "figure": "",
                "table": "",
                "page": page,
                "snippet": snippet,
                "extraction_method": "pdf_text",
                "confidence": "low",
                "requires_human_check": True,
                "extension_metadata": {"degraded": "non_standard_full_text_fallback"},
            }
        )
    return anchors


def _pdfplumber_table_anchors(paper_id: str, path: Path) -> list[dict[str, Any]]:
    try:
        import pdfplumber  # type: ignore[import-not-found]
    except (ImportError, ModuleNotFoundError):
        return []
    anchors: list[dict[str, Any]] = []
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page_index, page in enumerate(pdf.pages, start=1):
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
                                "manual_confirmed": False,
                                "confirmed_by": "",
                                "confirmed_at": "",
                                "validated_metric": "",
                                "validated_baseline": "",
                                "validated_task": "",
                                "confirmation_note": "",
                            }
                        )
    except Exception as exc:
        _pdf_extract_warning("pdfplumber_table", exc)
        return anchors
    return anchors


def _pdfplumber_text_and_table_anchors(paper_id: str, path: Path) -> list[dict[str, Any]]:
    try:
        import pdfplumber  # type: ignore[import-not-found]
    except (ImportError, ModuleNotFoundError):
        return []
    anchors: list[dict[str, Any]] = []
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page_index, page in enumerate(pdf.pages, start=1):
                text = " ".join((page.extract_text() or "").split())
                if text:
                    snippet = text[:600]
                    anchors.append(
                        {
                            "anchor_id": _anchor_id(paper_id, "snippet", f"{page_index}:{snippet}"),
                            "anchor_type": "snippet",
                            "anchor_source": "pdf_text",
                            "section": "Full Text (pdfplumber fallback)",
                            "figure": "",
                            "table": "",
                            "page": page_index,
                            "snippet": snippet,
                            "extraction_method": "pdfplumber",
                            "confidence": "low",
                            "requires_human_check": True,
                            "extension_metadata": {"degraded": "pymupdf_unavailable_or_empty"},
                        }
                    )
        anchors.extend(_pdfplumber_table_anchors(paper_id, path))
    except Exception as exc:
        _pdf_extract_warning("pdfplumber_text", exc)
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
