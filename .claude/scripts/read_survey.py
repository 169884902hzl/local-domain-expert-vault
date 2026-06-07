"""Progressive reading pipeline for long survey papers.

Splits fulltext into overlapping chunks for incremental analysis.
Every N chunks Claudian generates an interval summary, providing
context anchors that prevent information loss across sections.

Workflow:
  1. prepare  - fetch fulltext from Zotero, save chunks to raw/chunks/
  2. Claudian reads each chunk, writes analysis_NNN.md back
  3. Claudian writes interval_NNN.md every N chunks
  4. status   - check reading progress and next action
  5. assemble - merge all analyses + summaries into one document

Usage:
  python read_survey.py prepare  --key ZOTERO_KEY [--chunk-size 4000] [--interval 5]
  python read_survey.py status   --key ZOTERO_KEY
  python read_survey.py assemble --key ZOTERO_KEY
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path

from kb_common import (
    parse_args_with_write_options,
    safe_print,
    safe_write,
    today_iso,
    vault_path,
)

CHUNKS_DIR = vault_path("raw", "chunks")
DEFAULT_CHUNK_SIZE = 4000
DEFAULT_OVERLAP = 500
DEFAULT_INTERVAL = 5


def _meta_path(zotero_key: str) -> Path:
    return CHUNKS_DIR / zotero_key / "meta.json"


def _load_meta(zotero_key: str) -> dict | None:
    path = _meta_path(zotero_key)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _save_meta(zotero_key: str, meta: dict, *, dry_run: bool, backup: bool) -> None:
    path = _meta_path(zotero_key)
    safe_write(path, json.dumps(meta, indent=2, ensure_ascii=False) + "\n", dry_run=dry_run, backup=backup)


def fetch_fulltext(zotero_key: str) -> str:
    url = f"http://127.0.0.1:23119/api/users/0/items/{zotero_key}/fulltext"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("content", "")
    except Exception as exc:
        safe_print(f"ERROR: Cannot fetch fulltext for {zotero_key}: {exc}")
        safe_print("  Make sure Zotero is running with the built-in API enabled.")
        return ""


def split_into_chunks(
    text: str, chunk_size: int, overlap: int
) -> list[dict[str, str | int]]:
    """Split text into overlapping chunks, preferring section boundaries."""
    section_split = re.compile(r"\n(?=#{1,3}\s)")
    raw_sections = section_split.split(text)

    chunks: list[dict[str, str | int]] = []
    buffer = ""
    buffer_start = 0

    for section in raw_sections:
        if len(buffer) + len(section) <= chunk_size:
            buffer += section
        else:
            if buffer.strip():
                chunks.append(
                    {"text": buffer, "start": buffer_start, "end": buffer_start + len(buffer)}
                )
                buffer_start += len(buffer) - overlap
                buffer = buffer[-overlap:] if overlap > 0 else ""
            for para in re.split(r"\n{2,}", section):
                if len(buffer) + len(para) + 2 <= chunk_size:
                    buffer += ("\n\n" if buffer else "") + para
                else:
                    if buffer.strip():
                        chunks.append(
                            {"text": buffer, "start": buffer_start, "end": buffer_start + len(buffer)}
                        )
                        buffer_start += len(buffer) - overlap
                        buffer = buffer[-overlap:] if overlap > 0 else ""
                    buffer = para

    if buffer.strip():
        chunks.append(
            {"text": buffer, "start": buffer_start, "end": buffer_start + len(buffer)}
        )

    for i, chunk in enumerate(chunks):
        chunk["index"] = i + 1
    return chunks


def cmd_prepare(args: argparse.Namespace) -> int:
    text = fetch_fulltext(args.key)
    if not text:
        safe_print(f"No fulltext available for {args.key}")
        return 1

    chunks = split_into_chunks(text, args.chunk_size, args.overlap)
    out_dir = CHUNKS_DIR / args.key
    out_dir.mkdir(parents=True, exist_ok=True)

    for chunk in chunks:
        path = out_dir / f"chunk_{chunk['index']:03d}.md"
        header = f"---\nchunk: {chunk['index']}/{len(chunks)}\nstart: {chunk['start']}\nend: {chunk['end']}\n---\n\n"
        safe_write(path, header + chunk["text"] + "\n", dry_run=args.dry_run, backup=not args.no_backup)

    meta = {
        "zotero_key": args.key,
        "total_chunks": len(chunks),
        "chunk_size": args.chunk_size,
        "overlap": args.overlap,
        "interval": args.interval,
        "total_chars": len(text),
        "prepared": today_iso(),
    }
    _save_meta(args.key, meta, dry_run=args.dry_run, backup=not args.no_backup)

    safe_print(f"Prepared {len(chunks)} chunks for {args.key}")
    safe_print(f"  Chunk size: {args.chunk_size} chars, overlap: {args.overlap}")
    safe_print(f"  Interval summary every {args.interval} chunks")
    safe_print(f"  Directory: {out_dir}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    out_dir = CHUNKS_DIR / args.key
    if not out_dir.exists():
        safe_print(f"No chunks found for {args.key}. Run 'prepare' first.")
        return 1

    chunks = sorted(out_dir.glob("chunk_*.md"))
    analyses = sorted(out_dir.glob("analysis_*.md"))
    intervals = sorted(out_dir.glob("interval_*.md"))

    analyzed_nums = set()
    for f in analyses:
        m = re.search(r"(\d+)", f.stem)
        if m:
            analyzed_nums.add(int(m.group(1)))

    total = len(chunks)
    analyzed = len(analyzed_nums)

    safe_print(f"Paper: {args.key}")
    safe_print(f"  Total chunks: {total}")
    safe_print(f"  Analyzed: {analyzed}/{total}")

    meta = _load_meta(args.key)
    if meta:
        interval = meta.get("interval", DEFAULT_INTERVAL)
        safe_print(f"  Interval size: {interval}")
        safe_print(f"  Prepared: {meta.get('prepared', '?')}")
        expected_intervals = analyzed // interval
        safe_print(f"  Interval summaries: {len(intervals)} (expected ~{expected_intervals})")

    if analyzed == 0:
        safe_print("  Next: Read chunk_001.md and write analysis_001.md")
    elif analyzed < total:
        last = max(analyzed_nums)
        safe_print(f"  Next: Read chunk_{last + 1:03d}.md and write analysis_{last + 1:03d}.md")
        if meta and (analyzed) % meta.get("interval", DEFAULT_INTERVAL) == 0:
            safe_print(f"  >>> Time to write interval summary #{analyzed // meta.get('interval', DEFAULT_INTERVAL)}")
    else:
        safe_print("  Status: ALL CHUNKS ANALYZED — ready to assemble")
    return 0


def cmd_assemble(args: argparse.Namespace) -> int:
    out_dir = CHUNKS_DIR / args.key
    if not out_dir.exists():
        safe_print(f"No chunks found for {args.key}. Run 'prepare' first.")
        return 1

    analyses = sorted(out_dir.glob("analysis_*.md"))
    intervals = sorted(out_dir.glob("interval_*.md"))
    chunks = sorted(out_dir.glob("chunk_*.md"))

    if len(analyses) != len(chunks):
        safe_print(
            f"Incomplete: {len(analyses)}/{len(chunks)} chunks analyzed."
        )
        safe_print("  Run 'status' to see which chunks are missing.")
        return 1

    parts: list[str] = []

    if intervals:
        parts.append("## Progressive Summaries\n")
        for f in intervals:
            parts.append(f"### {f.stem}\n")
            parts.append(f.read_text(encoding="utf-8"))
            parts.append("")

    parts.append("## Chunk Analyses\n")
    for f in analyses:
        m = re.search(r"(\d+)", f.stem)
        label = f"Chunk {m.group(1)}" if m else f.stem
        parts.append(f"### {label}\n")
        parts.append(f.read_text(encoding="utf-8"))
        parts.append("")

    assembled = "\n".join(parts)
    output_path = out_dir / "assembled.md"
    safe_write(output_path, assembled, dry_run=args.dry_run, backup=not args.no_backup)
    safe_print(f"Assembled {len(analyses)} analyses + {len(intervals)} summaries")
    safe_print(f"  Output: {output_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    prep = sub.add_parser("prepare", help="Fetch fulltext and split into chunks")
    prep.add_argument("--key", required=True, help="Zotero item key")
    prep.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    prep.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)
    prep.add_argument("--interval", type=int, default=DEFAULT_INTERVAL)

    stat = sub.add_parser("status", help="Show reading progress")
    stat.add_argument("--key", required=True, help="Zotero item key")

    asm = sub.add_parser("assemble", help="Combine analyses into assembled output")
    asm.add_argument("--key", required=True, help="Zotero item key")

    args = parse_args_with_write_options(parser)

    if not args.command:
        parser.print_help()
        return 1

    commands = {
        "prepare": cmd_prepare,
        "status": cmd_status,
        "assemble": cmd_assemble,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
