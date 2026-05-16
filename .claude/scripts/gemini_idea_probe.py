"""Probe: test gemini-cli idea generation with a single evidence cluster."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from gemini_cli_adapter import run_gemini_cli
from research_agenda_common import load_evidence_matrix, split_csv
from research_agenda_ideate import (
    _mechanism_candidates,
    _normalize_mechanism_axis,
    _render_divergent_prompt,
    _source_count,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=1200, help="Gemini CLI timeout in seconds.")
    parser.add_argument("--matrix", default=None, help="Evidence matrix JSONL path.")
    parser.add_argument("--dry-run", action="store_true", help="Only show the prompt, don't call Gemini.")
    args = parser.parse_args()

    if args.matrix:
        matrix_path = Path(args.matrix)
    else:
        from research_agenda_common import EVIDENCE_MATRIX
        matrix_path = EVIDENCE_MATRIX

    if not matrix_path.exists():
        print(f"FAIL matrix not found: {matrix_path}")
        return 1

    records = load_evidence_matrix(matrix_path)
    print(f"EVIDENCE_RECORDS: {len(records)}")

    focus_keys = {
        str(record.get("zotero_key", "")).upper()
        for record in records
        if str(record.get("zotero_key", "")).strip()
    }
    candidates = _mechanism_candidates(records, focus_keys=focus_keys)
    if not candidates:
        print("NO_CANDIDATES: no mechanism cluster met the minimum threshold.")
        return 0

    print(f"CANDIDATES: {len(candidates)}")
    for score, axis, evidence, recent in candidates[:3]:
        print(f"  {score:5d} sources={_source_count(evidence)} {axis['title']}")

    prompt = _render_divergent_prompt(
        candidates,
        records=records,
        focus_keys=focus_keys,
        limit=8,
        min_candidates=6,
        free_divergence=True,
    )
    if args.dry_run:
        print("\n=== PROMPT (dry-run) ===")
        print(prompt[:3000])
        print("...(truncated)" if len(prompt) > 3000 else "")
        return 0

    print(f"\nCALLING gemini-cli (timeout={args.timeout}s)...")
    result = run_gemini_cli(prompt, timeout_sec=args.timeout)

    print(f"\nPROVIDER: {result['provider']}")
    print(f"EXIT_CODE: {result['exit_code']}")
    print(f"TIMED_OUT: {result['timed_out']}")
    print(f"ERROR: {result['error'] or 'none'}")
    clean = result["clean_output"]
    if clean:
        print(f"\nCLEAN_OUTPUT ({len(clean)} chars):")
        print(clean[:3000])
    else:
        print("\nNO_CLEAN_OUTPUT")
        if result["raw_stdout"]:
            print(f"RAW_STDOUT (first 500 chars): {result['raw_stdout'][:500]}")
        if result["raw_stderr"]:
            print(f"RAW_STDERR (first 500 chars): {result['raw_stderr'][:500]}")

    if result["error"]:
        print(f"\nVERDICT: fail ({result['error']})")
        return 1

    if clean:
        from research_agenda_ideate import _extract_json_object
        parsed = _extract_json_object(clean)
        if parsed and isinstance(parsed.get("candidates"), list):
            for item in parsed["candidates"]:
                if isinstance(item, dict):
                    axis = _normalize_mechanism_axis({**item, "generator_status": "gemini-cli"})
                    print(f"\nIDEA: {axis['title']}")
                    print(f"  problem: {axis.get('problem', '')[:120]}")
                    print(f"  mechanism: {axis.get('mechanism', '')[:120]}")
            print(f"\nVERDICT: success ({len(parsed['candidates'])} candidates)")
            return 0
        else:
            print("\nVERDICT: partial (output received but JSON parse failed)")
            return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
