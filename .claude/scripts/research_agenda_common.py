"""Shared helpers for the long-term research agenda workflow."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from kb_common import extract_frontmatter, parse_frontmatter_map, parse_list_value, safe_write, vault_path


AGENDA_ROOT = vault_path("projects", "research-agenda")
EVIDENCE_DIR = AGENDA_ROOT / "evidence"
PROBLEM_POOL_DIR = AGENDA_ROOT / "problem_pool"
IDEA_BANK_DIR = AGENDA_ROOT / "idea_bank"
DAILY_DIR = AGENDA_ROOT / "daily"
REVIEWS_DIR = AGENDA_ROOT / "reviews"
DIVERGENT_DIR = AGENDA_ROOT / "divergent"
CONCEPT_DELTA_DIR = AGENDA_ROOT / "concept-deltas"
MECHANISM_GRAPH_DIR = AGENDA_ROOT / "mechanism-graphs"
WORKFLOW_CONTRACT_DIR = AGENDA_ROOT / "workflow-contracts"
EVIDENCE_MATRIX = EVIDENCE_DIR / "evidence_matrix.jsonl"
IDEA_STATES = ["seed", "developing", "promoted", "pilot-ready", "rejected", "archived"]
REQUIRED_IDEA_FILES = [
    "idea.md",
    "evidence_pack.md",
    "similar_work.md",
    "novelty_argument.md",
    "experiment_plan.md",
    "risk_review.md",
    "review_log.md",
]
REQUIRED_EVIDENCE_FIELDS = [
    "source_note",
    "zotero_key",
    "claim_type",
    "statement",
    "domains",
    "supports",
    "risks",
    "transfer_to_DLO",
    "transfer_to_tactile",
    "transfer_to_bimanual",
    "transfer_to_VLA",
    "transfer_to_sim_to_real",
]


DOMAIN_KEYWORDS = {
    "DLO": ["dlo", "deformable", "rope", "cable", "wire", "linear object", "绳", "线缆", "可变形"],
    "tactile": ["tactile", "touch", "force", "haptic", "contact", "触觉", "力", "接触"],
    "bimanual": ["bimanual", "dual-arm", "two-arm", "coordination", "双臂", "双手", "协同"],
    "VLA": ["vla", "vlm", "vision-language", "language", "world model", "语言", "视觉语言"],
    "diffusion": ["diffusion", "denois", "score", "扩散"],
    "sim-to-real": ["sim-to-real", "sim2real", "real-to-sim", "domain", "simulation", "仿真", "迁移"],
    "planning": ["planning", "planner", "trajectory", "mpc", "routing", "规划", "轨迹"],
    "imitation": ["imitation", "demonstration", "behavior cloning", "teleoperation", "模仿", "示教"],
    "benchmark": ["benchmark", "evaluation", "metric", "dataset", "评测", "指标", "数据集"],
    "failure": ["failure", "risk", "limitation", "uncertain", "失败", "限制", "风险"],
}


def agenda_path(*parts: str) -> Path:
    return AGENDA_ROOT.joinpath(*parts)


def rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def today() -> str:
    return date.today().isoformat()


def slugify(value: str, *, max_len: int = 72) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return (text[:max_len].strip("-") or "untitled")


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def read_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text
    fields, body = parsed
    return parse_frontmatter_map(fields), body


def strip_quotes(value: str) -> str:
    return value.strip().strip('"')


def frontmatter_list(fields: dict[str, str], key: str) -> list[str]:
    return parse_list_value(fields.get(key, ""))


def ensure_agenda_dirs() -> None:
    for directory in [
        EVIDENCE_DIR,
        EVIDENCE_DIR / "paper_cards",
        EVIDENCE_DIR / "method_cards",
        EVIDENCE_DIR / "benchmark_cards",
        EVIDENCE_DIR / "sensor_cards",
        EVIDENCE_DIR / "limitation_cards",
        PROBLEM_POOL_DIR,
        DAILY_DIR,
        REVIEWS_DIR,
        DIVERGENT_DIR,
        CONCEPT_DELTA_DIR,
        MECHANISM_GRAPH_DIR,
        WORKFLOW_CONTRACT_DIR,
        REVIEWS_DIR / "novelty_checks",
        REVIEWS_DIR / "feasibility_checks",
        REVIEWS_DIR / "codex_reviews",
        REVIEWS_DIR / "claude_reviews",
        REVIEWS_DIR / "gemini_prompts",
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    for state in IDEA_STATES:
        (IDEA_BANK_DIR / state).mkdir(parents=True, exist_ok=True)


def iter_topic_notes() -> list[Path]:
    topics = vault_path("wiki", "topics")
    return sorted(topics.glob("*.md")) if topics.exists() else []


def note_is_done_literature(path: Path) -> bool:
    fields, _ = read_frontmatter(path)
    return strip_quotes(fields.get("type", "")) == "literature" and strip_quotes(fields.get("status", "")) == "done"


def detect_domains(text: str, tags: list[str]) -> list[str]:
    haystack = f"{text} {' '.join(tags)}".lower()
    domains = set()
    for tag in tags:
        if tag in {"DLO", "tactile", "bimanual", "diffusion", "sim-to-real", "planning", "imitation"}:
            domains.add(tag)
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword.lower() in haystack for keyword in keywords):
            domains.add(domain)
    return sorted(domains)


def evidence_key(record: dict[str, Any]) -> str:
    return "|".join(
        [
            str(record.get("source_note", "")),
            str(record.get("claim_type", "")),
            str(record.get("statement", ""))[:220],
        ]
    )


def load_evidence_matrix(path: Path = EVIDENCE_MATRIX) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            records.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return records


def merge_evidence_records(existing: list[dict[str, Any]], new_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_key = {evidence_key(record): record for record in existing}
    for record in new_records:
        by_key[evidence_key(record)] = record
    return sorted(by_key.values(), key=lambda item: (item.get("source_note", ""), item.get("claim_type", "")))


def write_jsonl(path: Path, records: list[dict[str, Any]], *, dry_run: bool) -> None:
    content = "\n".join(json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records)
    if content:
        content += "\n"
    safe_write(path, content, dry_run=dry_run, backup=True)


def note_link(source_note: str, title: str | None = None) -> str:
    stem = Path(source_note).stem
    label = title or stem
    return f"[[{stem}|{label}]]"


def render_frontmatter(title: str, tags: list[str], summary: str, *, status: str = "done") -> str:
    tag_text = "[" + ", ".join(tags) + "]"
    now = today()
    return "\n".join(
        [
            "---",
            f'title: "{title}"',
            f"tags: {tag_text}",
            f'created: "{now}"',
            f'updated: "{now}"',
            'type: "permanent"',
            f'status: "{status}"',
            f'summary: "{summary}"',
            "---",
            "",
        ]
    )
