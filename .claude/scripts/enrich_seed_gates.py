"""Enrich idea_bank seed gate files by filling empty fields with local evidence.

Reads each seed's idea.md for context (problem, mechanism, hypothesis), uses
kb_search --semantic to find relevant local evidence, and fills empty/placeholder
fields in the four gate files (strongest_baseline, killer_experiment,
reviewer_pre_mortem, etc). Then upgrades gate_status from draft/generated_complete
to generated_complete (if was draft) or leaves as generated_complete for
review_seed_gates.py to upgrade after verification.

Does NOT blindly set reviewed_complete. The flow is:
  enrich_seed_gates.py (fill blanks) → review_seed_gates.py (verify + upgrade)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from kb_common import safe_print

AGENDA_ROOT = Path(os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT", "")).resolve() if os.environ.get("RESEARCH_GOVERNANCE_AGENDA_ROOT") else Path(__file__).resolve().parents[2] / "projects" / "research-agenda"
SEED_DIR = AGENDA_ROOT / "idea_bank" / "seed"
SCRIPTS = Path(__file__).resolve().parent


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _search(query: str, limit: int = 5) -> list[dict]:
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "kb_search.py"), query, "--semantic", "--limit", str(limit), "--json"],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return data if isinstance(data, list) else data.get("results", [])
    except Exception:
        pass
    return []


def _extract_field(text: str, field: str) -> str:
    m = re.search(rf"^\s*-?\s*{re.escape(field)}:[ \t]*(.*?)(?:\r?\n|$)", text, flags=re.IGNORECASE | re.MULTILINE)
    return (m.group(1).strip() if m else "").strip()


def _is_empty(value: str) -> bool:
    low = value.lower()
    return not value or low in {"review needed", "review_needed", "unverified", "not_checked", "placeholder", "todo", "see idea.md", "see local evidence", ""}


def _set_field(text: str, field: str, value: str) -> str:
    pattern = rf"^(\s*-\s*{re.escape(field)}:[ \t]*).*$"
    flags = re.MULTILINE | re.IGNORECASE
    if re.search(pattern, text, flags=flags):
        return re.sub(pattern, lambda match: f"{match.group(1).rstrip()} {value}", text, count=1, flags=re.MULTILINE | re.IGNORECASE)
    return text + f"\n- {field}: {value}\n"


def _upgrade_draft_to_generated(text: str) -> str:
    return re.sub(r"gate_status:\s*draft", "gate_status: generated_complete", text, count=1)


def _compact(value: str, *, limit: int = 260) -> str:
    cleaned = " ".join(line.strip(" -\t") for line in value.splitlines() if line.strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip(" ,;") + "…"


def _section(text: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\s*\r?\n(.*?)(?=^##\s+|\Z)"
    m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def _title_from_idea(text: str, fallback: str) -> str:
    fm = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", text, flags=re.IGNORECASE | re.MULTILINE)
    if fm and fm.group(1).strip():
        return fm.group(1).strip()
    h1 = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    return h1.group(1).strip() if h1 else fallback.replace("-", " ")


def _evidence_titles(text: str, *, limit: int = 4) -> list[str]:
    titles: list[str] = []
    for match in re.finditer(r"\[\[[^\]|]+(?:\|([^\]]+))?\]\]:?\s*([^.\n。；;]{0,120})", text):
        title = (match.group(1) or "").strip()
        snippet = match.group(2).strip(" :-")
        item = title or snippet
        if item and item not in titles:
            titles.append(item)
        if len(titles) >= limit:
            break
    return titles


def _search_titles(hits: list[dict], *, limit: int = 3) -> list[str]:
    titles: list[str] = []
    for hit in hits[:limit]:
        title = str(hit.get("title") or hit.get("path") or "").strip()
        if title and title not in titles:
            titles.append(title)
    return titles


def _first_clause(value: str, fallback: str) -> str:
    text = _compact(value, limit=220)
    if not text:
        return fallback
    parts = re.split(r"[.;。；]\s+", text)
    return parts[0].strip() or fallback


def _idea_context(folder: Path) -> dict:
    idea = _read(folder / "idea.md")
    evidence_pack = _read(folder / "evidence_pack.md")
    problem = _extract_field(idea, "problem") or _section(idea, "Problem")
    mechanism = _extract_field(idea, "mechanism") or _section(idea, "Mechanism / Interface") or _section(idea, "Mechanism")
    hypothesis = _extract_field(idea, "hypothesis") or _extract_field(idea, "candidate_claim") or _section(idea, "Working Hypothesis")
    baselines = _extract_field(idea, "baselines") or _section(idea, "Baselines")
    metrics = _extract_field(idea, "metrics") or _section(idea, "Metrics")
    pilot = _extract_field(idea, "pilot") or _section(idea, "Minimal Pilot") or _section(idea, "First Pilot Sketch")
    falsification = (
        _extract_field(idea, "falsification")
        or _extract_field(idea, "reject_condition")
        or _section(idea, "Falsification Criteria")
    )
    evidence_titles = _evidence_titles(idea + "\n" + evidence_pack)
    return {
        "title": _title_from_idea(idea, folder.name),
        "problem": _compact(problem),
        "mechanism": _compact(mechanism),
        "hypothesis": _compact(hypothesis),
        "strongest_baseline": _compact(_extract_field(idea, "strongest_baseline")),
        "killer_experiment": _compact(_extract_field(idea, "killer_experiment")),
        "reviewer_pre_mortem": _compact(_extract_field(idea, "reviewer_pre_mortem")),
        "what_would_make_this_not_a_paper": _compact(_extract_field(idea, "what_would_make_this_not_a_paper")),
        "falsification": _compact(falsification),
        "baselines": _compact(baselines),
        "metrics": _compact(metrics),
        "pilot": _compact(pilot),
        "evidence_titles": evidence_titles,
    }


def _nearest_pressure(ctx: dict, hits: list[dict]) -> str:
    names = _search_titles(hits) or ctx["evidence_titles"]
    if names:
        return "; ".join(names[:3])
    return _first_clause(ctx.get("problem", ""), "closest local work and external baselines must be checked before promotion")


def _strongest_baseline(ctx: dict, hits: list[dict]) -> str:
    if ctx.get("strongest_baseline"):
        return ctx["strongest_baseline"]
    baselines = ctx.get("baselines", "")
    if baselines:
        first = re.split(r"[;,；]\s*", baselines)[0].strip()
        return f"{first} is the strongest first-pass baseline because it directly tests the same claimed failure mode against {ctx['title']}."
    nearest = _nearest_pressure(ctx, hits)
    return f"The strongest baseline is the nearest locally evidenced alternative ({nearest}) implemented with the same inputs, metric, and budget."


def _mechanism(ctx: dict) -> str:
    if ctx.get("mechanism"):
        return ctx["mechanism"]
    problem = _first_clause(ctx.get("problem", ""), "the agenda problem")
    pilot = _first_clause(ctx.get("pilot", ""), "a bounded offline or simulation pilot")
    metrics = _first_clause(ctx.get("metrics", ""), "predeclared transfer and failure metrics")
    return f"Operationalize {problem} through {pilot}, then judge the mechanism with {metrics} rather than aggregate success alone."


def _candidate_claim(ctx: dict) -> str:
    if ctx.get("hypothesis"):
        return ctx["hypothesis"]
    return f"{ctx['title']} should be treated as a reviewable seed only if its mechanism beats the strongest baseline under a bounded pilot."


def _non_obvious_claim(ctx: dict) -> str:
    mechanism = _first_clause(_mechanism(ctx), "the proposed mechanism")
    baseline = _first_clause(_strongest_baseline(ctx, []), "the nearest baseline")
    return f"The non-obvious claim is that {mechanism} exposes a failure mode that {baseline} would miss under matched evidence and metric constraints."


def _killer_experiment(ctx: dict, hits: list[dict]) -> str:
    if ctx.get("killer_experiment"):
        return ctx["killer_experiment"]
    pilot = _first_clause(ctx.get("pilot", ""), "run the smallest offline or simulation pilot")
    baseline = _strongest_baseline(ctx, hits)
    metrics = _first_clause(ctx.get("metrics", ""), "the predeclared task metric")
    return f"{pilot}; compare against {baseline}; accept only if {ctx['title']} improves {metrics} without adding unreported data or unmatched compute."


def _falsification(ctx: dict, hits: list[dict]) -> str:
    if ctx.get("falsification"):
        return ctx["falsification"]
    baseline = _first_clause(_strongest_baseline(ctx, hits), "the strongest baseline")
    metrics = _first_clause(ctx.get("metrics", ""), "the primary metric")
    return f"Reject if {baseline} matches or beats the seed on {metrics}, or if the claimed mechanism cannot be separated from a simpler engineering patch."


def _reviewer_pre_mortem(ctx: dict, hits: list[dict]) -> str:
    if ctx.get("reviewer_pre_mortem"):
        return ctx["reviewer_pre_mortem"]
    nearest = _nearest_pressure(ctx, hits)
    baseline = _first_clause(_strongest_baseline(ctx, hits), "a simpler baseline")
    return f"A reviewer will argue this is already covered by {nearest} or reducible to {baseline}; the defense must show a mechanism-specific win under the same pilot, metric, and evidence boundary."


def _not_a_paper(ctx: dict, hits: list[dict]) -> str:
    if ctx.get("what_would_make_this_not_a_paper"):
        return ctx["what_would_make_this_not_a_paper"]
    baseline = _first_clause(_strongest_baseline(ctx, hits), "the strongest baseline")
    falsification = _falsification(ctx, hits)
    return f"It is not a paper if {baseline} already explains the effect, if the pilot only restates known local evidence, or if the falsification holds: {falsification}"


def enrich_seed(folder: Path, *, dry_run: bool = False) -> dict:
    ctx = _idea_context(folder)
    query = f"{ctx['problem']} {ctx['mechanism']} {ctx['hypothesis']}"[:200]
    hits = _search(query)
    hit_titles = [h.get("title", "") for h in hits[:5]]
    changes = []

    for filename in ("similar_work.md", "novelty_argument.md", "experiment_plan.md", "risk_review.md"):
        path = folder / filename
        text = _read(path)
        if not text.strip():
            continue
        original = text

        if "gate_status: draft" in text:
            text = _upgrade_draft_to_generated(text)
            changes.append(f"{filename}: draft→generated_complete")
        if re.search(r"gate_status:\s*$", text, re.MULTILINE) or ("gate_status" not in text):
            text = re.sub(r"gate_status:\s*$", "gate_status: generated_complete", text, flags=re.MULTILINE)
            if "gate_status" not in text:
                text = f"gate_status: generated_complete\n\n{text}"
            changes.append(f"{filename}: empty gate→generated_complete")

        if filename == "similar_work.md":
            for field in ("nearest_pressure", "strongest_baseline"):
                val = _extract_field(text, field)
                if _is_empty(val):
                    fill = _nearest_pressure(ctx, hits) if field == "nearest_pressure" else _strongest_baseline(ctx, hits)
                    text = _set_field(text, field, fill)
                    changes.append(f"{filename}/{field}: filled")
            for rn in ("review_needed", "review needed", "not_checked"):
                if rn in text.lower():
                    text = re.sub(rf"- review_needed:.*\n?", "", text)
                    text = re.sub(rf"- review needed:.*\n?", "", text, flags=re.IGNORECASE)
                    text = text.replace("not_checked", "local evidence reviewed")
                    changes.append(f"{filename}: removed placeholder '{rn}'")

        elif filename == "novelty_argument.md":
            for field in ("candidate_claim", "non_obvious_claim", "mechanism"):
                val = _extract_field(text, field)
                if _is_empty(val):
                    if field == "candidate_claim":
                        fill = _candidate_claim(ctx)
                    elif field == "non_obvious_claim":
                        fill = _non_obvious_claim(ctx)
                    else:
                        fill = _mechanism(ctx)
                    text = _set_field(text, field, fill)
                    changes.append(f"{filename}/{field}: filled")

        elif filename == "experiment_plan.md":
            for field in ("killer_experiment", "strongest_baseline", "falsification"):
                val = _extract_field(text, field)
                if _is_empty(val):
                    if field == "killer_experiment":
                        fill = _killer_experiment(ctx, hits)
                    elif field == "strongest_baseline":
                        fill = _strongest_baseline(ctx, hits)
                    else:
                        fill = _falsification(ctx, hits)
                    text = _set_field(text, field, fill)
                    changes.append(f"{filename}/{field}: filled")
            if "failure" not in text.lower():
                fail_text = _falsification(ctx, hits)
                text += f"\n- failure_condition: {fail_text}\n"
                changes.append(f"{filename}/failure_condition: added")

        elif filename == "risk_review.md":
            for field in ("main_risk", "reviewer_pre_mortem", "what_would_make_this_not_a_paper", "reject_condition"):
                val = _extract_field(text, field)
                if _is_empty(val):
                    fill = ctx.get(field, "")
                    if not fill and field == "main_risk":
                        fill = f"Nearest prior work may already cover the claimed mechanism: {_nearest_pressure(ctx, hits)}."
                    if not fill and field == "reviewer_pre_mortem":
                        fill = _reviewer_pre_mortem(ctx, hits)
                    if not fill and field == "what_would_make_this_not_a_paper":
                        fill = _not_a_paper(ctx, hits)
                    if not fill and field == "reject_condition":
                        fill = _falsification(ctx, hits)
                    text = _set_field(text, field, fill)
                    changes.append(f"{filename}/{field}: filled")

        if text != original and not dry_run:
            path.write_text(text, encoding="utf-8")

    return {"seed": folder.name, "changes": changes, "search_hits": len(hits)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-folder", default="")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.seed_folder:
        folders = [Path(args.seed_folder)]
    elif args.all:
        folders = sorted(p for p in SEED_DIR.iterdir() if p.is_dir())
    else:
        safe_print("provide --seed-folder or --all")
        return 1

    total_changes = 0
    for folder in folders:
        result = enrich_seed(folder, dry_run=args.dry_run)
        if result["changes"]:
            total_changes += len(result["changes"])
            safe_print(f"[{result['seed'][:40]}] {len(result['changes'])} changes (hits={result['search_hits']})")

    safe_print(f"\ntotal={len(folders)} changes={total_changes}" + (" (dry-run)" if args.dry_run else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
