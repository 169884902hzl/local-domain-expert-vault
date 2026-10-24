#!/usr/bin/env python3
"""Audit a nonstandard Zotero import batch without mutating Zotero.

This script copies zotero.sqlite to a temporary file and reads only the copy.
It is intended for the 2026-06-04 Codex awesome-embodied import batch, whose
items were intentionally tagged as partial metadata and queued for repair.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any


DEFAULT_BATCH_TAG = "codex-awesome-embodied-full-import-20260604-172607"
DEFAULT_RUN_DIR = Path("output/import_runs/20260604-172607-awesome-embodied-full-import")
DEFAULT_ZOTERO_DB = Path(os.environ.get("ZOTERO_DB_PATH", Path.home() / "Zotero" / "zotero.sqlite"))
DEFAULT_ZOTERO_STORAGE = Path(os.environ.get("ZOTERO_STORAGE_DIR", Path.home() / "Zotero" / "storage"))

ARXIV_RE = re.compile(
    r"(?:arxiv[:/\.\-a-zA-Z]*|arXiv:\s*)/?(?:abs/|pdf/)?([0-9]{4}\.[0-9]{4,5})(?:v\d+)?",
)
ARXIV_DOI_RE = re.compile(r"10\.48550/arXiv\.([0-9]{4}\.[0-9]{4,5})")
OPENREVIEW_RE = re.compile(r"openreview\.net/(?:forum|pdf)\?id=([A-Za-z0-9_\-]+)")


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def vault_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                rows.append({"_parse_error": str(exc), "_line_no": line_no, "_raw": stripped[:500]})
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def normalize_title(title: str | None) -> str:
    text = (title or "").strip()
    text = re.sub(r"[\]\[]+$", "", text)
    text = re.sub(r"\s+", " ", text)
    return re.sub(r"\W+", " ", text.lower()).strip()


def extract_arxiv_id(*parts: str | None) -> str:
    for part in parts:
        if not part:
            continue
        doi = ARXIV_DOI_RE.search(part)
        if doi:
            return doi.group(1)
        match = ARXIV_RE.search(part)
        if match:
            return match.group(1)
        file_match = re.search(r"arxiv-([0-9]{4}\.[0-9]{4,5})(?:v\d+)?", part, re.IGNORECASE)
        if file_match:
            return file_match.group(1)
    return ""


def extract_openreview_id(*parts: str | None) -> str:
    for part in parts:
        if not part:
            continue
        match = OPENREVIEW_RE.search(part)
        if match:
            return match.group(1)
    return ""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class ZoteroCopy:
    def __init__(self, db_path: Path, storage_dir: Path) -> None:
        if not db_path.exists():
            raise FileNotFoundError(f"Missing Zotero database: {db_path}")
        self.source_db = db_path
        self.storage_dir = storage_dir
        self.temp_dir = Path(tempfile.mkdtemp(prefix="zotero-manual-batch-audit-"))
        self.copy_path = self.temp_dir / "zotero.sqlite"
        shutil.copy2(db_path, self.copy_path)
        self.con = sqlite3.connect(self.copy_path)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.fields = self._field_ids()

    def close(self) -> None:
        self.con.close()

    def _field_ids(self) -> dict[str, int | None]:
        wanted = [
            "title",
            "date",
            "DOI",
            "url",
            "abstractNote",
            "extra",
            "archive",
            "archiveLocation",
            "publicationTitle",
            "proceedingsTitle",
        ]
        out: dict[str, int | None] = {}
        for name in wanted:
            row = self.cur.execute("select fieldID from fields where fieldName=?", (name,)).fetchone()
            out[name] = int(row[0]) if row else None
        return out

    def value(self, item_id: int, field: str) -> str:
        field_id = self.fields.get(field)
        if field_id is None:
            return ""
        row = self.cur.execute(
            """
            select v.value
            from itemData d
            join itemDataValues v on v.valueID = d.valueID
            where d.itemID=? and d.fieldID=?
            """,
            (item_id, field_id),
        ).fetchone()
        return str(row[0]) if row else ""

    def creator_names(self, item_id: int) -> list[str]:
        rows = self.cur.execute(
            """
            select c.firstName, c.lastName
            from itemCreators ic
            join creators c on c.creatorID = ic.creatorID
            where ic.itemID=?
            order by ic.orderIndex
            """,
            (item_id,),
        ).fetchall()
        names: list[str] = []
        for row in rows:
            names.append(f"{row['firstName'] or ''} {row['lastName'] or ''}".strip())
        return [name for name in names if name]

    def attachments(self, item_id: int) -> list[dict[str, Any]]:
        url_field = self.fields.get("url")
        rows = self.cur.execute(
            """
            select child.itemID, child.key, child.dateAdded, it.typeName, ia.contentType, ia.path,
                   v.value as attachment_url
            from itemAttachments ia
            join items child on child.itemID = ia.itemID
            join itemTypes it on it.itemTypeID = child.itemTypeID
            left join itemData d on d.itemID = child.itemID and d.fieldID = ?
            left join itemDataValues v on v.valueID = d.valueID
            where ia.parentItemID=?
            order by child.itemID
            """,
            (url_field, item_id),
        ).fetchall()
        out: list[dict[str, Any]] = []
        for row in rows:
            cache_path = self.storage_dir / str(row["key"]) / ".zotero-ft-cache"
            cache_chars = 0
            if cache_path.exists():
                try:
                    cache_chars = len(cache_path.read_text(encoding="utf-8", errors="ignore"))
                except OSError:
                    cache_chars = 0
            fulltext_indexed = self.cur.execute(
                "select 1 from fulltextItems where itemID=?",
                (row["itemID"],),
            ).fetchone()
            out.append(
                {
                    "item_id": row["itemID"],
                    "key": row["key"],
                    "date_added": row["dateAdded"],
                    "type": row["typeName"],
                    "content_type": row["contentType"] or "",
                    "path": row["path"] or "",
                    "url": row["attachment_url"] or "",
                    "is_pdf": row["contentType"] == "application/pdf"
                    or str(row["path"] or "").lower().endswith(".pdf"),
                    "fulltext_indexed": bool(fulltext_indexed),
                    "ft_cache_chars": cache_chars,
                },
            )
        return out

    def batch_items(self, batch_tag: str) -> list[dict[str, Any]]:
        rows = self.cur.execute(
            """
            select i.itemID, i.key, i.dateAdded, i.dateModified, it.typeName
            from items i
            join itemTypes it on it.itemTypeID = i.itemTypeID
            left join itemAttachments parent_attachment on parent_attachment.itemID = i.itemID
            left join deletedItems di on di.itemID = i.itemID
            join itemData extra_data on extra_data.itemID = i.itemID and extra_data.fieldID = ?
            join itemDataValues extra_value on extra_value.valueID = extra_data.valueID
            where parent_attachment.itemID is null
              and di.itemID is null
              and extra_value.value like ?
            order by i.dateAdded, i.itemID
            """,
            (self.fields["extra"], f"%{batch_tag}%"),
        ).fetchall()
        return [self.item_record(row) for row in rows]

    def all_normal_items(self, batch_tag: str) -> list[dict[str, Any]]:
        rows = self.cur.execute(
            """
            select i.itemID, i.key, i.dateAdded, i.dateModified, it.typeName
            from items i
            join itemTypes it on it.itemTypeID = i.itemTypeID
            left join itemAttachments parent_attachment on parent_attachment.itemID = i.itemID
            left join deletedItems di on di.itemID = i.itemID
            left join itemData extra_data on extra_data.itemID = i.itemID and extra_data.fieldID = ?
            left join itemDataValues extra_value on extra_value.valueID = extra_data.valueID
            where parent_attachment.itemID is null
              and di.itemID is null
              and (extra_value.value is null or extra_value.value not like ?)
            order by i.dateAdded, i.itemID
            """,
            (self.fields["extra"], f"%{batch_tag}%"),
        ).fetchall()
        return [self.item_record(row) for row in rows]

    def item_record(self, row: sqlite3.Row) -> dict[str, Any]:
        item_id = int(row["itemID"])
        attachments = self.attachments(item_id)
        values = {field: self.value(item_id, field) for field in self.fields}
        creators = self.creator_names(item_id)
        arxiv_id = extract_arxiv_id(
            values.get("DOI"),
            values.get("url"),
            values.get("extra"),
            values.get("archiveLocation"),
            *[att["url"] for att in attachments],
            *[att["path"] for att in attachments],
        )
        openreview_id = extract_openreview_id(
            values.get("url"),
            values.get("extra"),
            *[att["url"] for att in attachments],
        )
        pdf_count = sum(1 for att in attachments if att["is_pdf"])
        ft_indexed_count = sum(1 for att in attachments if att["fulltext_indexed"])
        ft_cache_count = sum(1 for att in attachments if att["ft_cache_chars"] >= 500)
        return {
            "zotero_key": row["key"],
            "item_id": item_id,
            "item_type": row["typeName"],
            "date_added": row["dateAdded"],
            "date_modified": row["dateModified"],
            "title": values["title"],
            "normalized_title": normalize_title(values["title"]),
            "creators": creators,
            "creator_count": len(creators),
            "date": values["date"],
            "doi": values["DOI"],
            "url": values["url"],
            "abstract_len": len(values["abstractNote"]),
            "extra": values["extra"],
            "archive": values["archive"],
            "archive_location": values["archiveLocation"],
            "publication_title": values["publicationTitle"],
            "proceedings_title": values["proceedingsTitle"],
            "arxiv_id": arxiv_id,
            "openreview_id": openreview_id,
            "attachments": attachments,
            "attachment_count": len(attachments),
            "pdf_attachment_count": pdf_count,
            "fulltext_indexed_attachment_count": ft_indexed_count,
            "ft_cache_attachment_count": ft_cache_count,
            "has_usable_fulltext_cache": ft_cache_count > 0,
        }


def queue_maps(run_dir: Path) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], list[dict[str, Any]]]:
    queue_rows = read_jsonl(run_dir / "automation_queue.jsonl")
    connector_rows = read_jsonl(run_dir / "connector_items.jsonl")
    by_key = {
        str(row.get("zotero_key")): row
        for row in queue_rows
        if row.get("zotero_key") and not row.get("_parse_error")
    }
    by_queue_id = {
        str(row.get("queue_id")): row
        for row in queue_rows
        if row.get("queue_id") and not row.get("_parse_error")
    }
    connector_by_queue_id = {
        str(row.get("queue_id")): row
        for row in connector_rows
        if row.get("queue_id") and not row.get("_parse_error")
    }
    for queue_id, row in connector_by_queue_id.items():
        if queue_id in by_queue_id:
            by_queue_id[queue_id]["connector_item"] = row.get("item", {})
    return by_key, by_queue_id, queue_rows


def duplicate_index(records: list[dict[str, Any]]) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[dict[str, Any]]]]:
    by_title: dict[str, list[dict[str, Any]]] = {}
    by_arxiv: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        is_usable = record["creator_count"] > 0 or record["abstract_len"] > 200
        if not is_usable:
            continue
        title = record["normalized_title"]
        if title:
            by_title.setdefault(title, []).append(record)
        arxiv_id = record["arxiv_id"]
        if arxiv_id:
            by_arxiv.setdefault(arxiv_id, []).append(record)
    return by_title, by_arxiv


def repair_bucket(record: dict[str, Any], duplicate_hits: list[dict[str, Any]]) -> str:
    if duplicate_hits:
        return "duplicate_candidate_review"
    if record["arxiv_id"]:
        return "arxiv_metadata_reimport_or_enrich"
    if record["openreview_id"]:
        return "openreview_metadata_resolve"
    url = record["url"] or ""
    if "icml.cc" in url:
        return "venue_page_metadata_resolve"
    if record["pdf_attachment_count"] > 0 or url.lower().endswith(".pdf"):
        return "direct_pdf_metadata_resolve"
    return "manual_source_verification_required"


def enrich_records(
    batch_records: list[dict[str, Any]],
    normal_records: list[dict[str, Any]],
    queue_by_key: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    by_title, by_arxiv = duplicate_index(normal_records)
    enriched: list[dict[str, Any]] = []
    for record in batch_records:
        hits: list[dict[str, Any]] = []
        if record["arxiv_id"]:
            hits.extend(by_arxiv.get(record["arxiv_id"], []))
        if record["normalized_title"]:
            hits.extend(by_title.get(record["normalized_title"], []))
        seen = set()
        unique_hits: list[dict[str, Any]] = []
        for hit in hits:
            key = hit["zotero_key"]
            if key in seen:
                continue
            seen.add(key)
            unique_hits.append(
                {
                    "zotero_key": hit["zotero_key"],
                    "title": hit["title"],
                    "date_added": hit["date_added"],
                    "creator_count": hit["creator_count"],
                    "abstract_len": hit["abstract_len"],
                    "arxiv_id": hit["arxiv_id"],
                    "url": hit["url"],
                },
            )
        queue_row = queue_by_key.get(record["zotero_key"], {})
        out = dict(record)
        out["queue_id"] = queue_row.get("queue_id", "")
        out["queue_import_quality"] = queue_row.get("import_quality", "")
        out["queue_ingest_status"] = queue_row.get("ingest_status", "")
        out["queue_read_status"] = queue_row.get("read_status", "")
        out["source_ids"] = queue_row.get("source_ids", [])
        out["duplicate_candidates"] = unique_hits
        out["repair_bucket"] = repair_bucket(record, unique_hits)
        out["metadata_defects"] = [
            defect
            for defect, is_defect in {
                "missing_creators": record["creator_count"] == 0,
                "missing_abstract": record["abstract_len"] == 0,
                "missing_identifier": not record["arxiv_id"] and not record["openreview_id"] and not record["doi"],
                "missing_pdf_attachment": record["pdf_attachment_count"] == 0,
                "missing_zotero_fulltext": record["fulltext_indexed_attachment_count"] == 0
                and record["ft_cache_attachment_count"] == 0,
            }.items()
            if is_defect
        ]
        enriched.append(out)
    return enriched


def summarize(items: list[dict[str, Any]], queue_rows: list[dict[str, Any]], summary_json: dict[str, Any]) -> dict[str, Any]:
    buckets = Counter(item["repair_bucket"] for item in items)
    types = Counter(item["item_type"] for item in items)
    sources = Counter(src for item in items for src in item.get("source_ids", []))
    defects = Counter(defect for item in items for defect in item["metadata_defects"])
    return {
        "batch_items_in_zotero": len(items),
        "queue_rows": len([row for row in queue_rows if not row.get("_parse_error")]),
        "summary_active_songwxuan_records": summary_json.get("active_songwxuan_records"),
        "summary_active_songwxuan_new_batch_tagged_records": summary_json.get(
            "active_songwxuan_new_batch_tagged_records",
        ),
        "by_item_type": dict(types),
        "by_repair_bucket": dict(buckets),
        "by_source_id": dict(sources),
        "metadata_defects": dict(defects),
        "missing_creators": sum(1 for item in items if item["creator_count"] == 0),
        "missing_abstract": sum(1 for item in items if item["abstract_len"] == 0),
        "with_arxiv_id": sum(1 for item in items if item["arxiv_id"]),
        "with_openreview_id": sum(1 for item in items if item["openreview_id"]),
        "with_pdf_attachment": sum(1 for item in items if item["pdf_attachment_count"] > 0),
        "with_zotero_fulltext_or_cache": sum(
            1
            for item in items
            if item["fulltext_indexed_attachment_count"] > 0 or item["ft_cache_attachment_count"] > 0
        ),
        "duplicate_candidates": sum(1 for item in items if item["duplicate_candidates"]),
    }


def markdown_report(data: dict[str, Any], items: list[dict[str, Any]]) -> str:
    summary = data["summary"]
    bucket_lines = "\n".join(
        f"- `{name}`: {count}" for name, count in sorted(summary["by_repair_bucket"].items())
    )
    defect_lines = "\n".join(f"- `{name}`: {count}" for name, count in sorted(summary["metadata_defects"].items()))
    samples: list[str] = []
    for item in items[:40]:
        samples.append(
            "| {key} | {bucket} | {arxiv} | {pdf} | {ft} | {title} |".format(
                key=item["zotero_key"],
                bucket=item["repair_bucket"],
                arxiv=item["arxiv_id"] or item["openreview_id"] or "",
                pdf=item["pdf_attachment_count"],
                ft=item["fulltext_indexed_attachment_count"] + item["ft_cache_attachment_count"],
                title=(item["title"] or "").replace("|", "\\|")[:120],
            ),
        )
    sample_table = "\n".join(samples)
    return f"""# Zotero Manual Import Batch Audit

- generated_at: `{data["generated_at"]}`
- batch_tag: `{data["batch_tag"]}`
- source_db: `{data["zotero_db"]}`
- sqlite_copy: `{data["sqlite_copy"]}`
- run_dir: `{data["run_dir"]}`

## Summary

- batch_items_in_zotero: `{summary["batch_items_in_zotero"]}`
- queue_rows: `{summary["queue_rows"]}`
- summary_active_songwxuan_records: `{summary["summary_active_songwxuan_records"]}`
- summary_active_songwxuan_new_batch_tagged_records: `{summary["summary_active_songwxuan_new_batch_tagged_records"]}`
- missing_creators: `{summary["missing_creators"]}`
- missing_abstract: `{summary["missing_abstract"]}`
- with_arxiv_id: `{summary["with_arxiv_id"]}`
- with_openreview_id: `{summary["with_openreview_id"]}`
- with_pdf_attachment: `{summary["with_pdf_attachment"]}`
- with_zotero_fulltext_or_cache: `{summary["with_zotero_fulltext_or_cache"]}`
- duplicate_candidates: `{summary["duplicate_candidates"]}`

## Repair Buckets

{bucket_lines}

## Metadata Defects

{defect_lines}

## Recommended Repair Order

1. Do not delete or reimport the whole batch blindly.
2. First repair `duplicate_candidate_review` by selecting the normal canonical item and mapping the bad key to it.
3. Then repair `arxiv_metadata_reimport_or_enrich` from arXiv metadata and preserve old-key to new-key mapping.
4. Resolve `openreview_metadata_resolve` and `venue_page_metadata_resolve` separately because those are not guaranteed to have arXiv metadata.
5. Only after canonical metadata is stable, rerun ingest/read for repaired keys.

## Sample Items

| zotero_key | repair_bucket | identifier | pdf_children | fulltext_or_cache | title |
|---|---|---:|---:|---:|---|
{sample_table}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-tag", default=DEFAULT_BATCH_TAG)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--zotero-db", type=Path, default=DEFAULT_ZOTERO_DB)
    parser.add_argument("--zotero-storage", type=Path, default=DEFAULT_ZOTERO_STORAGE)
    parser.add_argument("--out-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = vault_root()
    run_dir = args.run_dir if args.run_dir.is_absolute() else root / args.run_dir
    out_dir = args.out_dir or run_dir / "repair_audit"
    out_dir = out_dir if out_dir.is_absolute() else root / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    summary_json = read_json(run_dir / "summary.json")
    queue_by_key, _queue_by_id, queue_rows = queue_maps(run_dir)
    zotero = ZoteroCopy(args.zotero_db, args.zotero_storage)
    try:
        batch_records = zotero.batch_items(args.batch_tag)
        normal_records = zotero.all_normal_items(args.batch_tag)
        enriched = enrich_records(batch_records, normal_records, queue_by_key)
        data = {
            "generated_at": utc_now(),
            "batch_tag": args.batch_tag,
            "run_dir": str(run_dir),
            "zotero_db": str(args.zotero_db),
            "zotero_db_sha256": sha256_file(args.zotero_db),
            "sqlite_copy": str(zotero.copy_path),
            "summary": summarize(enriched, queue_rows, summary_json),
            "outputs": {
                "items_jsonl": str(out_dir / "manual_import_batch_items.jsonl"),
                "summary_json": str(out_dir / "manual_import_batch_summary.json"),
                "repair_plan_md": str(out_dir / "repair_plan.md"),
            },
        }
        write_json(out_dir / "manual_import_batch_summary.json", data)
        write_jsonl(out_dir / "manual_import_batch_items.jsonl", enriched)
        (out_dir / "repair_plan.md").write_text(markdown_report(data, enriched), encoding="utf-8")
        print(json.dumps(data, ensure_ascii=False, indent=2))
    finally:
        zotero.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
