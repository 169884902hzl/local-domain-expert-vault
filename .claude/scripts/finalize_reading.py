"""Write a completed reading analysis back into a literature note."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from kb_common import (
    extract_frontmatter,
    load_schema,
    parse_args_with_write_options,
    parse_frontmatter_map,
    parse_list_value,
    render_frontmatter,
    safe_print,
    safe_write,
    today_iso,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")
PLACEHOLDER_TEXT = "待精读补充"
WAITING_TEXT = "待精读"
WEAK_EVIDENCE_CLASSES = {"note_derived", "abstract_only", "not_evidenced", "figure_approximation"}
ANCHOR_REQUIRED_EVIDENCE_CLASSES = {
    "pdf_verified",
    "table_verified",
    "figure_verified",
    "appendix_verified",
    "result_row_unconfirmed",
    "figure_approximation",
}
ALLOWED_EVIDENCE_CLASSES = ANCHOR_REQUIRED_EVIDENCE_CLASSES | WEAK_EVIDENCE_CLASSES
ALLOWED_ANCHOR_TYPES = {"section", "table", "figure", "appendix", "result_row", "snippet", "abstract", "note_only"}
REVIEW_ONLY_DOWNSTREAM_USES = {"screening_only", "requires_human_check"}
DLO_TARGET_TERMS = {
    "dlo",
    "deformable linear object",
    "deformable object",
    "rope",
    "cable",
    "wire",
    "cloth",
    "tether",
    "柔性线状物",
    "柔性物体",
    "线缆",
    "绳",
    "绳索",
    "布料",
    "bimanual",
    "dual-arm",
    "dual arm",
    "closed-loop",
    "closed loop",
    "control",
    "sim-to-real",
    "sim to real",
    "robot manipulation",
    "双臂",
    "双手",
    "控制",
    "闭环",
    "迁移",
}
DEFORMABLE_SOURCE_TERMS = {
    "dlo",
    "dlo manipulation",
    "dlo control",
    "deformable manipulation",
    "deformable object manipulation",
    "deformable linear object manipulation",
    "rope manipulation",
    "rope control",
    "cable manipulation",
    "cable control",
    "wire manipulation",
    "wire control",
    "cloth manipulation",
    "cloth control",
    "tether manipulation",
    "tether control",
    "柔性线状物操控",
    "柔性物体操控",
    "线缆操控",
    "绳索操控",
    "布料操控",
}
GENERATION_SOURCE_TERMS = {
    "animation",
    "video",
    "generation",
    "generative",
    "language-only",
    "pure perception",
}
TRANSFER_CONTEXT_TERMS = {
    "transfer",
    "sim-to-real",
    "sim to real",
    "generalization",
    "direct-copy",
    "direct copy",
    "negative transfer",
    "迁移",
    "泛化",
}
PHYSICAL_EVAL_TERMS = {
    "physical closed-loop",
    "closed-loop manipulation",
    "closed loop manipulation",
    "contact dynamics",
    "dlo control",
    "physical control",
}
STRICT_SECTION_HEADINGS = [
    "## Evidence Ledger",
    "## Idea Fuel",
    "## Baseline Pressure",
    "## Transfer Risk",
    "## No-hardware Micro-test",
    "## Evidence Gaps",
]
REQUIRED_ANALYSIS_SECTIONS = [
    "## 证据元数据",
    "## Problem",
    "## 关键贡献",
    "## Method",
    "## Experiments",
    "## Limitations",
    "## Key Takeaways",
    *STRICT_SECTION_HEADINGS,
    "## 结构化提取",
    "## 本地引用关系",
]

SECTION_ALIASES = {
    "## 证据元数据": ["Evidence Metadata", "证据元数据"],
    "## Problem": ["Problem", "问题"],
    "## 关键贡献": ["Key Contributions", "关键贡献"],
    "## Method": ["Method", "方法"],
    "## Experiments": ["Experiments", "实验"],
    "## Limitations": ["Limitations", "局限性"],
    "## Key Takeaways": ["Key Takeaways", "启发", "要点"],
    "## Evidence Ledger": ["Evidence Ledger", "证据台账", "证据账本"],
    "## Idea Fuel": ["Idea Fuel"],
    "## Baseline Pressure": ["Baseline Pressure"],
    "## Transfer Risk": ["Transfer Risk"],
    "## No-hardware Micro-test": ["No-hardware Micro-test", "Minimum No-hardware Micro-test"],
    "## Evidence Gaps": ["Evidence Gaps"],
    "## 结构化提取": ["结构化提取", "Structured Extraction"],
    "## 本地引用关系": ["本地引用关系", "Local Citation Links", "Related Papers"],
}
SECTION_WRITE_ORDER = list(SECTION_ALIASES)


def find_note_by_key(zotero_key: str) -> Path | None:
    pattern = re.compile(rf'^zotero_key:\s*"?{re.escape(zotero_key)}"?\s*$', re.MULTILINE)
    for path in sorted(TOPICS_DIR.glob("*.md")):
        if pattern.search(path.read_text(encoding="utf-8")):
            return path
    return None


def extract_sections(markdown: str) -> dict[str, str]:
    sections = {}
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE))
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        body = markdown[start:end].strip()
        for canonical, aliases in SECTION_ALIASES.items():
            if heading in aliases:
                sections[canonical] = body
    nested_idea = extract_subsection(sections.get("## Key Takeaways", ""), "Idea Fuel")
    top_idea = sections.get("## Idea Fuel", "")
    if nested_idea:
        if top_idea and materially_different(top_idea, nested_idea):
            sections["__strict_issue__"] = "duplicate_idea_fuel_conflict"
        elif not top_idea:
            sections["## Idea Fuel"] = nested_idea
            sections["## Key Takeaways"] = remove_subsection(sections.get("## Key Takeaways", ""), "Idea Fuel")
    return sections


def extract_subsection(markdown: str, heading: str) -> str:
    match = re.search(rf"^###\s+{re.escape(heading)}\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^###\s+(?!IF-\d+\b)", markdown[start:], flags=re.MULTILINE | re.IGNORECASE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def remove_subsection(markdown: str, heading: str) -> str:
    match = re.search(rf"^###\s+{re.escape(heading)}\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return markdown
    start = match.start()
    after_heading = match.end()
    next_heading = re.search(r"^###\s+(?!IF-\d+\b)", markdown[after_heading:], flags=re.MULTILINE | re.IGNORECASE)
    end = after_heading + next_heading.start() if next_heading else len(markdown)
    return (markdown[:start].rstrip() + "\n\n" + markdown[end:].lstrip()).strip()


def normalize_material(value: str) -> str:
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", value.lower())


def materially_different(left: str, right: str) -> bool:
    left_norm = normalize_material(left)
    right_norm = normalize_material(right)
    if not left_norm or not right_norm:
        return False
    if right_norm in {"sameastoplevel", "not_evidenced"}:
        return False
    return left_norm != right_norm


def structured_field_name(line: str) -> str | None:
    if not line.startswith("-") or ":" not in line:
        return None
    name = line[1:].split(":", 1)[0].strip().strip("*").strip()
    return name or None


def extract_metadata_summary(metadata: str) -> str | None:
    for line in metadata.splitlines():
        stripped = line.strip().lstrip("-").strip()
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        normalized = key.strip().strip("*").strip().lower()
        if normalized in {"summary", "one-line summary", "一句话总结", "中文摘要"}:
            summary = value.strip().strip('"')
            return summary or None
    return None


def normalize_field_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip().strip("`").strip("*").strip() for cell in stripped.split("|")]


def is_separator_row(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def parse_evidence_ledger(ledger: str) -> tuple[list[dict[str, str]], set[str]]:
    table_lines = [line for line in ledger.splitlines() if line.strip().startswith("|") and line.strip().endswith("|")]
    if len(table_lines) >= 3 and is_separator_row(table_lines[1]):
        headers = split_table_row(table_lines[0])
        normalized_headers = [normalize_field_name(header) for header in headers]
        rows = []
        for line in table_lines[2:]:
            if is_separator_row(line):
                continue
            cells = split_table_row(line)
            if not any(cell.strip() for cell in cells):
                continue
            row = {
                normalized_headers[index]: cells[index].strip()
                for index in range(min(len(normalized_headers), len(cells)))
            }
            rows.append(row)
        return rows, set(normalized_headers)

    rows = []
    current: dict[str, str] = {}
    headers: set[str] = set()
    for line in ledger.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                rows.append(current)
                current = {}
            continue
        if not stripped.startswith("-") or ":" not in stripped:
            continue
        key, value = stripped.lstrip("-").split(":", 1)
        normalized = normalize_field_name(key.strip())
        headers.add(normalized)
        current[normalized] = value.strip()
    if current:
        rows.append(current)
    return rows, headers


def ledger_value(row: dict[str, str], *aliases: str) -> str:
    for alias in aliases:
        value = row.get(normalize_field_name(alias), "")
        if value:
            return value.strip()
    return ""


def normalize_token(value: str) -> str:
    return re.sub(r"[^\w]+", "_", value.lower(), flags=re.UNICODE).strip("_")


def split_tokens(value: str) -> set[str]:
    return {normalize_token(item) for item in re.split(r"[,;/\s]+", value) if normalize_token(item)}


def parse_key_values(section: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in section.splitlines():
        stripped = line.strip()
        if ":" not in stripped:
            continue
        if stripped.startswith("|"):
            continue
        stripped = stripped.lstrip("-").strip()
        key, value = stripped.split(":", 1)
        key = key.strip().strip("*").strip()
        if key:
            values[normalize_field_name(key)] = value.strip()
    return values


def first_key_value(values: dict[str, str], *aliases: str) -> str:
    for alias in aliases:
        value = values.get(normalize_field_name(alias), "")
        if value:
            return value.strip()
    return ""


IDEA_FUEL_FIELD_ALIASES = {
    "Hypothesis / research opening": ("Hypothesis / research opening", "Hypothesis", "Research opening"),
    "Evidence anchor": ("Evidence anchor", "Evidence anchor / claim_id", "claim_id", "Evidence Ledger claim_ids"),
    "Evidence class": ("Evidence class",),
    "Engineering pathology": ("Engineering pathology",),
    "Hidden assumption": ("Hidden assumption",),
    "Fragile interface": ("Fragile interface",),
    "Failure mode": ("Failure mode",),
    "Strongest baseline": ("Strongest baseline",),
    "Why this baseline is strongest": ("Why this baseline is strongest", "Why strongest"),
    "Paper win condition": ("Paper win condition",),
    "Idea kill condition": ("Idea kill condition",),
    "DLO replacement baseline": ("DLO replacement baseline",),
    "Transfer distance to DLO": ("Transfer distance to DLO", "Transfer distance"),
    "Why transfer may fail": ("Why transfer may fail",),
    "Negative transfer risk": ("Negative transfer risk",),
    "Minimum no-hardware micro-test": ("Minimum no-hardware micro-test", "No-hardware micro-test"),
    "Downstream review target": ("Downstream review target",),
}
NO_HARDWARE_FIELD_ALIASES = {
    "Artifact": ("Artifact", "Test artifact", "测试产物", "产物"),
    "Input": ("Input", "Inputs", "输入"),
    "Protocol": ("Protocol", "Procedure", "Steps", "步骤", "流程"),
    "Metric": ("Metric", "指标"),
    "Threshold": ("Threshold", "阈值"),
    "Pass condition": ("Pass condition", "Pass", "通过条件"),
    "Fail/kill condition": ("Fail/kill condition", "Fail condition", "Kill condition", "Fail", "Kill", "失败条件"),
    "Compute/data cap": ("Compute/data cap", "Compute cap", "Data cap", "Budget cap", "计算上限", "数据上限"),
}


def parse_known_fields(section: str, aliases_by_label: dict[str, tuple[str, ...]]) -> dict[str, str]:
    alias_to_label = {
        normalize_field_name(alias): label
        for label, aliases in aliases_by_label.items()
        for alias in aliases
    }
    values: dict[str, list[str]] = {}
    current_label: str | None = None
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        candidate = stripped.lstrip("-").strip()
        if ":" in candidate:
            key, value = candidate.split(":", 1)
            label = alias_to_label.get(normalize_field_name(key.strip().strip("*").strip()))
            if label:
                current_label = label
                values.setdefault(label, []).append(value.strip())
                continue
        if current_label:
            values.setdefault(current_label, []).append(stripped)
    return {label: "\n".join(part for part in parts if part).strip() for label, parts in values.items()}


def blank_or_placeholder(value: str) -> bool:
    normalized = normalize_token(value)
    return not normalized or normalized in {"not_evidenced", "todo", "tbd", "unknown", "n_a", "na", "none", "missing"}


def has_negated_phrase(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in patterns)


def non_negated_hits(text: str, tokens: list[str]) -> list[str]:
    lowered = text.lower()
    negators = [
        "no",
        "not",
        "without",
        "must not",
        "do not",
        "does not",
        "invalid",
        "fail/kill condition",
        "fail / kill condition",
        "fail condition",
        "kill condition",
        "prohibit",
        "forbid",
        "禁止",
        "失败条件",
        "失败",
        "不得",
        "不能",
        "无需",
        "不需要",
        "不依赖",
        "不使用",
        "不包含",
        "不做",
        "不宣称",
        "不声称",
        "不评估",
        "不验证",
        "无",
        "没有",
        "未",
        "不含",
        "不采集",
        "不产生",
        "不生成",
        "不引入",
        "不加入",
        "不用",
    ]
    synthetic_context_markers = [
        "synthetic",
        "toy",
        "token",
        "tokens",
        "label",
        "labels",
        "array",
        "arrays",
        "graph",
        "static",
        "proxy",
        "placeholder",
        "合成",
        "玩具",
        "标签",
        "数组",
        "静态",
        "代理",
    ]
    gripper_proxy_markers = [
        "binary",
        "count",
        "counts",
        "coordination",
        "definition",
        "definitions",
        "frequency",
        "threshold",
        "mismatch",
        "smoothness",
        "stability",
        "sequence",
        "sequences",
        "timing",
        "transition",
        "transitions",
        "pose",
        "poses",
        "state",
        "states",
        "feature",
        "features",
        "metric",
        "metrics",
        "retargeting",
        "symbolic",
        "二值",
        "计数",
        "协调",
        "频率",
        "平滑",
        "序列",
        "过渡",
    ]
    requirement_context_markers = [
        "real",
        "use",
        "run",
        "collect",
        "deploy",
        "evaluate",
        "require",
        "requires",
        "physical",
        "真实",
        "使用",
        "运行",
        "采集",
        "部署",
        "评估",
        "需要",
        "物理",
    ]
    hits = []
    for token in tokens:
        token_lower = token.lower()
        for match in re.finditer(re.escape(token_lower), lowered):
            context_start = max(0, match.start() - 96)
            window_start = max(0, match.start() - 36)
            end = min(len(lowered), match.end() + 36)
            window = lowered[window_start:end]
            context = lowered[context_start : match.start()]
            surrounding = lowered[context_start:end]
            clause_context = re.split(r"[.;。；\n]", context)[-1]
            if any(negator in clause_context for negator in negators):
                continue
            context_markers = synthetic_context_markers
            if token_lower in {"gripper", "夹爪"}:
                context_markers = synthetic_context_markers + gripper_proxy_markers
            if any(marker in surrounding for marker in context_markers) and not any(
                marker in window or marker in clause_context for marker in requirement_context_markers
            ):
                continue
            hits.append(token)
            break
    return hits


def contains_any_term(text: str, terms: set[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def evidence_ledger_claim_ids(ledger: str) -> set[str]:
    rows, _headers = parse_evidence_ledger(ledger)
    return {claim_id for row in rows if (claim_id := ledger_value(row, "claim_id"))}


def claim_id_references(value: str) -> list[str]:
    ignored = {
        "table",
        "figure",
        "section",
        "appendix",
        "page",
        "row",
        "claim",
        "id",
        "evidence",
        "anchor",
        "no_hardware",
        "dlo_specific",
        "direct_copy",
        "sim_to_real",
    }
    refs: list[str] = []
    for token in re.findall(r"\b[A-Za-z][A-Za-z0-9_-]*\b", value):
        normalized = normalize_token(token)
        if normalized in ignored:
            continue
        if normalized.startswith("if_"):
            continue
        if re.fullmatch(r"C(?:\d+|-[A-Za-z0-9][A-Za-z0-9_-]*)", token):
            refs.append(token)
    return refs


def unknown_claim_id_refs(text: str, known_claim_ids: set[str]) -> list[str]:
    return [ref for ref in claim_id_references(text) if ref not in known_claim_ids]


def extract_idea_fuel_packets(section: str) -> dict[str, str]:
    pattern = re.compile(r"^(?:#{3,6}\s+|[-*]\s*)?(IF-\d+)\b[^\n]*$", flags=re.MULTILINE | re.IGNORECASE)
    matches = list(pattern.finditer(section))
    packets: dict[str, str] = {}
    for index, match in enumerate(matches):
        label = match.group(1).upper()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        title_tail = match.group(0)[match.group(0).upper().find(label) + len(label) :].strip(" :-")
        body = section[start:end].strip()
        if title_tail:
            body = f"- Hypothesis / research opening: {title_tail}\n{body}".strip()
        packets[label] = body
    return packets


def enough_material_for_three_idea_packets(evidence_ledger: str, idea_fuel: str) -> bool:
    rows, _headers = parse_evidence_ledger(evidence_ledger)
    evidenced_rows = [
        row
        for row in rows
        if ledger_value(row, "claim")
        and normalize_token(ledger_value(row, "evidence_class")) not in {"not_evidenced", "abstract_only"}
    ]
    return len(evidenced_rows) >= 3 or len(idea_fuel) >= 1200


def protocol_step_count(protocol: str) -> int:
    numbered = re.findall(r"(?:^|[;；\n]\s*)(?:step\s*)?\d{1,2}[\).:]", protocol, flags=re.IGNORECASE)
    if numbered:
        return len(numbered)
    semicolon_steps = [part for part in re.split(r"[;；]", protocol) if part.strip()]
    return len(semicolon_steps) if len(semicolon_steps) >= 3 else 0


def micro_test_executability_issues(section: str, *, prefix: str = "no_hardware_micro_test") -> list[str]:
    issues: list[str] = []
    fields = parse_known_fields(section, NO_HARDWARE_FIELD_ALIASES)
    for label in NO_HARDWARE_FIELD_ALIASES:
        if blank_or_placeholder(fields.get(label, "")):
            issues.append(f"{prefix}_missing_{normalize_token(label)}")
    protocol = fields.get("Protocol", "")
    if protocol and not 3 <= protocol_step_count(protocol) <= 6:
        issues.append(f"{prefix}_protocol_not_3_to_6_steps")
    return issues


def validate_idea_fuel(section: str, evidence_ledger: str) -> list[str]:
    issues: list[str] = []
    packets = extract_idea_fuel_packets(section)
    if "IF-1" not in packets:
        issues.append("idea_fuel_missing_if_packet:IF-1")
    if enough_material_for_three_idea_packets(evidence_ledger, section):
        for required_packet in ["IF-1", "IF-2", "IF-3"]:
            if required_packet not in packets:
                issues.append(f"idea_fuel_missing_if_packet:{required_packet}")

    known_claim_ids = evidence_ledger_claim_ids(evidence_ledger)
    for packet_id, packet_text in packets.items():
        values = parse_known_fields(packet_text, IDEA_FUEL_FIELD_ALIASES)
        for label in IDEA_FUEL_FIELD_ALIASES:
            value = values.get(label, "")
            if label in {"Evidence anchor", "Evidence class"} and normalize_token(value) == "not_evidenced":
                continue
            if label == "Transfer distance to DLO" and normalize_token(value) == "none":
                continue
            if blank_or_placeholder(value):
                issues.append(f"idea_fuel_packet_missing:{packet_id}:{label}")

        anchor = values.get("Evidence anchor", "")
        if not blank_or_placeholder(anchor):
            if normalize_token(anchor) == "not_evidenced":
                pass
            else:
                refs = claim_id_references(anchor)
                if not refs:
                    issues.append(f"idea_fuel_packet_missing_claim_id_reference:{packet_id}")
                for ref in refs:
                    if ref not in known_claim_ids:
                        issues.append(f"idea_fuel_packet_unknown_claim_id:{packet_id}:{ref}")

        evidence_class = normalize_token(values.get("Evidence class", ""))
        if evidence_class and evidence_class not in ALLOWED_EVIDENCE_CLASSES:
            issues.append(f"idea_fuel_packet_bad_evidence_class:{packet_id}:{evidence_class}")

        review_target = values.get("Downstream review target", "").lower()
        if review_target:
            if "deepseek" not in review_target:
                issues.append(f"idea_fuel_packet_review_target_missing_deepseek:{packet_id}")
            if "codex" not in review_target:
                issues.append(f"idea_fuel_packet_review_target_missing_codex:{packet_id}")

        micro_test = values.get("Minimum no-hardware micro-test", "")
        if micro_test:
            issues.extend(micro_test_executability_issues(micro_test, prefix=f"idea_fuel_packet_micro_test:{packet_id}"))
            issues.extend(
                issue.replace("no_hardware_micro_test_", f"idea_fuel_packet_micro_test:{packet_id}:")
                for issue in validate_no_hardware_micro_test(micro_test)
            )
    return issues


NUMERIC_RESULT_TERMS = {
    "result",
    "metric",
    "score",
    "success",
    "rate",
    "accuracy",
    "error",
    "improvement",
    "outperform",
    "baseline",
    "ablation",
    "reported",
    "performance",
    "结果",
    "指标",
    "成功率",
    "误差",
    "提升",
    "基线",
}


def line_has_numeric_result_claim(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("|") or stripped.startswith("#"):
        return False
    metadata_prefixes = (
        "- Fulltext Quality:",
        "- Evidence Coverage:",
        "- Confidence:",
        "- Anchor Coverage:",
        "- Evidence Boundary:",
    )
    if any(stripped.startswith(prefix) for prefix in metadata_prefixes):
        return False
    if re.match(r"^\*{0,2}\s*(step|步骤|阶段)\s*\d+", stripped, flags=re.IGNORECASE):
        return False
    text_without_ids = re.sub(r"\b[A-Za-z]+-[A-Za-z0-9_-]*\b", "", stripped)
    has_number = bool(re.search(r"\b\d+(?:\.\d+)?\s*(?:%|x|ms|s|m|cm|mm|points?|pts)?\b", text_without_ids))
    if not has_number:
        return False
    lowered = stripped.lower()
    return any(term in lowered for term in NUMERIC_RESULT_TERMS)


def line_has_claim_id_or_anchor(line: str, known_claim_ids: set[str]) -> bool:
    refs = claim_id_references(line)
    if any(ref in known_claim_ids for ref in refs):
        return True
    return bool(
        re.search(
            r"\b(tables?|figures?|figs?\.?|result_rows?|sections?|appendices|appendix|pages?|p\.)\s*(?:[a-z]?\d+(?:\s*[-–]\s*[a-z]?\d+)?|[ivxlcdm]+)\b",
            line,
            flags=re.IGNORECASE,
        )
    )


def validate_numeric_claims(sections: dict[str, str]) -> list[str]:
    known_claim_ids = evidence_ledger_claim_ids(sections.get("## Evidence Ledger", ""))
    issues: list[str] = []
    for heading, body in sections.items():
        if heading in {"## Evidence Ledger", "## Idea Fuel", "## No-hardware Micro-test", "__strict_issue__"}:
            continue
        section_claim_refs = set(claim_id_references(body))
        has_section_level_claim_anchor = heading in {"## Baseline Pressure", "## Transfer Risk"} and bool(section_claim_refs & known_claim_ids)
        for line in body.splitlines():
            if (
                line_has_numeric_result_claim(line)
                and not line_has_claim_id_or_anchor(line, known_claim_ids)
                and not has_section_level_claim_anchor
            ):
                snippet = " ".join(line.strip().split())[:80]
                issues.append(f"numeric_claim_missing_claim_id_or_anchor:{heading.removeprefix('## ')}:{snippet}")
    return issues


def validate_evidence_ledger(ledger: str) -> list[str]:
    issues: list[str] = []
    rows, headers = parse_evidence_ledger(ledger)
    required_headers = {
        "claimid": "claim_id",
        "claimtype": "claim_type",
        "claim": "claim",
        "evidenceclass": "evidence_class",
        "anchortype": "anchor_type",
        "anchor": "anchor",
        "pagesectiontablefigureappendix": "page/section/table/figure/appendix",
        "confidence": "confidence",
        "downstreamuse": "downstream_use",
    }
    missing_headers = [label for key, label in required_headers.items() if key not in headers]
    if missing_headers:
        issues.append("evidence_ledger_missing_required_columns:" + ",".join(missing_headers))
    if not rows:
        issues.append("evidence_ledger_missing_rows")
        return issues

    coverage = {
        "problem": False,
        "contribution_or_method": False,
        "experiment_or_result": False,
        "limitation": False,
        "baseline": False,
    }
    for index, row in enumerate(rows, 1):
        claim_id = ledger_value(row, "claim_id")
        claim_type = normalize_token(ledger_value(row, "claim_type"))
        claim = ledger_value(row, "claim")
        evidence_class = normalize_token(ledger_value(row, "evidence_class"))
        anchor_type = normalize_token(ledger_value(row, "anchor_type"))
        anchor = ledger_value(row, "anchor")
        downstream_use = ledger_value(row, "downstream_use")
        row_label = claim_id or f"row_{index}"

        if not claim_id:
            issues.append(f"evidence_ledger_missing_claim_id:{index}")
        if not claim_type:
            issues.append(f"evidence_ledger_missing_claim_type:{row_label}")
        if not claim:
            issues.append(f"evidence_ledger_missing_claim:{row_label}")
        if evidence_class not in ALLOWED_EVIDENCE_CLASSES:
            issues.append(f"evidence_ledger_bad_evidence_class:{row_label}:{evidence_class or 'missing'}")
        if anchor_type not in ALLOWED_ANCHOR_TYPES:
            issues.append(f"evidence_ledger_bad_anchor_type:{row_label}:{anchor_type or 'missing'}")
        if evidence_class in ANCHOR_REQUIRED_EVIDENCE_CLASSES and not anchor:
            issues.append(f"evidence_ledger_missing_anchor:{row_label}")
        if evidence_class in WEAK_EVIDENCE_CLASSES and not (split_tokens(downstream_use) & REVIEW_ONLY_DOWNSTREAM_USES):
            issues.append(f"evidence_ledger_weak_claim_not_screening_only:{row_label}")
        if evidence_class == "figure_approximation":
            if anchor_type != "figure":
                issues.append(f"evidence_ledger_figure_approximation_wrong_anchor_type:{row_label}")
            if "requires_human_check" not in split_tokens(downstream_use):
                issues.append(f"evidence_ledger_figure_approximation_requires_human_check:{row_label}")
        if (
            claim_type in {"problem", "contribution", "method", "experiment", "result", "limitation", "baseline", "strongest_baseline"}
            and evidence_class not in WEAK_EVIDENCE_CLASSES
            and (anchor_type in {"note_only", "abstract"} or not anchor)
        ):
            issues.append(f"evidence_ledger_anchorless_key_claim:{row_label}")
        if evidence_class == "result_row_unconfirmed":
            if anchor_type != "result_row":
                issues.append(f"evidence_ledger_result_row_wrong_anchor_type:{row_label}")
            if "requires_human_check" not in split_tokens(downstream_use):
                issues.append(f"evidence_ledger_result_row_requires_human_check:{row_label}")

        if "problem" in claim_type:
            coverage["problem"] = True
        if "contribution" in claim_type or "method" in claim_type:
            coverage["contribution_or_method"] = True
        if any(token in claim_type for token in ["experiment", "result", "metric", "evaluation"]):
            coverage["experiment_or_result"] = True
        if "limitation" in claim_type:
            coverage["limitation"] = True
        if "baseline" in claim_type:
            coverage["baseline"] = True

    for name, present in coverage.items():
        if not present:
            issues.append(f"evidence_ledger_missing_coverage:{name}")
    return issues


def validate_baseline_pressure(section: str, evidence_ledger: str = "") -> list[str]:
    values = parse_key_values(section)
    required = {
        "Strongest Baseline": ("Strongest Baseline",),
        "Why strongest": ("Why strongest",),
        "Evidence anchor / claim_id": ("Evidence anchor / claim_id", "Evidence anchor", "claim_id"),
        "Paper win condition": ("Paper win condition",),
        "Idea kill condition": ("Idea kill condition",),
        "DLO replacement baseline": ("DLO replacement baseline",),
        "No-hardware proxy baseline": ("No-hardware proxy baseline",),
    }
    issues = []
    for label, aliases in required.items():
        if blank_or_placeholder(first_key_value(values, *aliases)):
            issues.append(f"baseline_pressure_missing:{label}")
    known_claim_ids = evidence_ledger_claim_ids(evidence_ledger)
    anchor_claim = first_key_value(values, "Evidence anchor / claim_id", "Evidence anchor", "claim_id")
    if not blank_or_placeholder(anchor_claim):
        refs = claim_id_references(anchor_claim)
        if not refs:
            issues.append("baseline_pressure_missing_claim_id_reference")
        for ref in refs:
            if ref not in known_claim_ids:
                issues.append(f"baseline_pressure_unknown_claim_id:{ref}")
    for ref in sorted(set(unknown_claim_id_refs(section, known_claim_ids))):
        issues.append(f"baseline_pressure_unknown_claim_id:{ref}")
    return issues


def validate_no_hardware_micro_test(section: str) -> list[str]:
    issues: list[str] = []
    required_negations = {
        "no_robot": [r"\bno\s+(real\s+)?robot\b", r"\bwithout\s+(a\s+)?(real\s+)?robot\b", r"不需要.*机器人", r"无需.*机器人", r"不使用.*机器人"],
        "no_real_scene": [r"\bno\s+(real\s+)?scene\b", r"\bno\s+real[-\s]?world\b", r"不需要.*真实场景", r"无需.*真实环境", r"不做.*真实"],
        "no_new_data_collection": [r"\bno\s+new\s+data\s+collection\b", r"\bno\s+new\s+video\s+capture\b", r"不需要.*新采集", r"无需.*新数据", r"不做.*新视频"],
    }
    for code, patterns in required_negations.items():
        if not has_negated_phrase(section, patterns):
            issues.append(f"no_hardware_micro_test_missing_explicit_{code}")

    invalid_tokens = [
        "real robot",
        "robot arm",
        "gripper",
        "real cabinet",
        "real environment",
        "real scene",
        "physical hardware",
        "hardware",
        "tactile sensor",
        "depth camera",
        "motion capture",
        "physical reset",
        "teleoperation",
        "human data collection",
        "new video capture",
        "new data collection",
        "real-world deployment",
        "physical experiment",
        "真实机器人",
        "机器人",
        "机械臂",
        "夹爪",
        "真实柜子",
        "硬件",
        "触觉传感器",
        "深度相机",
        "动捕",
        "运动捕捉",
        "物理复位",
        "遥操作",
        "人工采集",
        "新视频",
        "新采集",
        "新数据",
        "真实场景",
        "真实环境",
        "实机",
        "物理实验",
    ]
    hits = non_negated_hits(section, invalid_tokens)
    if hits:
        issues.append("no_hardware_micro_test_invalid_hardware_requirement:" + ",".join(sorted(set(hits))[:5]))

    required_fields = {
        "artifact": ["artifact", "test artifact", "测试产物", "产物"],
        "input": ["input", "inputs", "输入"],
        "protocol": ["protocol", "procedure", "steps", "步骤", "流程"],
        "metric": ["metric", "指标"],
        "threshold": ["threshold", "阈值"],
        "pass_condition": ["pass condition", "通过条件", "pass:"],
        "fail_or_kill_condition": ["fail condition", "kill condition", "失败条件", "kill:"],
        "compute_data_cap": ["compute/data cap", "compute cap", "data cap", "计算上限", "数据上限"],
    }
    lowered = section.lower()
    for code, tokens in required_fields.items():
        if not any(token.lower() in lowered for token in tokens):
            issues.append(f"no_hardware_micro_test_missing_{code}")
    issues.extend(micro_test_executability_issues(section))
    return issues


def validate_transfer_risk(section: str, idea_fuel: str) -> list[str]:
    values = parse_key_values(section)
    source_domain = first_key_value(values, "Source domain")
    target_domain = first_key_value(values, "Target domain")
    combined = f"{section}\n{idea_fuel}"
    lowered = combined.lower()
    source_lower = source_domain.lower()
    target_context = f"{target_domain}\n{combined}"
    issues: list[str] = []
    deformable_target = contains_any_term(target_context, DLO_TARGET_TERMS)
    generation_source = contains_any_term(source_lower, GENERATION_SOURCE_TERMS)
    deformable_source = contains_any_term(source_lower, DEFORMABLE_SOURCE_TERMS) and not generation_source
    deformable_transfer = deformable_target and not deformable_source
    transfer_present = (
        bool(source_domain or target_domain or first_key_value(values, "Transfer distance"))
        or contains_any_term(combined, TRANSFER_CONTEXT_TERMS)
    )
    if deformable_transfer or (transfer_present and deformable_target):
        required = {
            "source_domain": ("Source domain",),
            "target_domain": ("Target domain",),
            "transfer_distance": ("Transfer distance",),
            "why_transfer_may_fail": ("Why transfer may fail",),
            "negative_transfer_risk": ("Negative transfer risk",),
            "misleading_direct_copy_risk": ("Misleading direct-copy risk", "Direct-copy risk"),
            "dlo_replacement_baseline": ("DLO replacement baseline",),
            "dlo_specific_kill_condition": ("DLO-specific kill condition",),
        }
        for label, aliases in required.items():
            if blank_or_placeholder(first_key_value(values, *aliases)):
                issues.append(f"transfer_risk_missing:{label}")

    distance = normalize_token(first_key_value(values, "Transfer distance"))
    if distance:
        allowed = {"none": 0, "low": 1, "medium": 2, "high": 3, "extreme": 4}
        if distance not in allowed:
            issues.append(f"transfer_risk_bad_distance:{distance}")
        physical_eval = contains_any_term(section.lower(), PHYSICAL_EVAL_TERMS)
        if generation_source and deformable_target and distance in allowed and allowed[distance] < allowed["high"] and not physical_eval:
            issues.append("transfer_risk_generation_to_dlo_distance_too_low")
    return issues


def strict_contract_issues(sections: dict[str, str]) -> list[str]:
    issues: list[str] = []
    if sections.get("__strict_issue__"):
        issues.append(str(sections["__strict_issue__"]))
    for heading in STRICT_SECTION_HEADINGS:
        if not sections.get(heading, "").strip():
            issues.append(f"missing_strict_section:{heading.removeprefix('## ')}")
    if sections.get("## Evidence Ledger"):
        issues.extend(validate_evidence_ledger(sections["## Evidence Ledger"]))
    if sections.get("## Idea Fuel"):
        issues.extend(validate_idea_fuel(sections["## Idea Fuel"], sections.get("## Evidence Ledger", "")))
    if sections.get("## Baseline Pressure"):
        issues.extend(validate_baseline_pressure(sections["## Baseline Pressure"], sections.get("## Evidence Ledger", "")))
    if sections.get("## No-hardware Micro-test"):
        issues.extend(validate_no_hardware_micro_test(sections["## No-hardware Micro-test"]))
    if sections.get("## Transfer Risk"):
        issues.extend(validate_transfer_risk(sections["## Transfer Risk"], sections.get("## Idea Fuel", "")))
    issues.extend(validate_numeric_claims(sections))
    return issues


def validate_analysis(sections: dict[str, str], schema: dict) -> None:
    missing = [heading for heading in REQUIRED_ANALYSIS_SECTIONS if heading not in sections]
    if missing:
        raise ValueError("analysis missing required sections: " + ", ".join(missing))

    structured_body = sections["## 结构化提取"]
    if PLACEHOLDER_TEXT in structured_body or WAITING_TEXT in structured_body:
        raise ValueError("analysis structured extraction still contains waiting placeholders")
    names = [
        name
        for line in structured_body.splitlines()
        if (name := structured_field_name(line.strip()))
    ]
    required_fields = schema["literature"].get("structured_fields", [])
    missing_fields = [field for field in required_fields if field not in names]
    if missing_fields:
        raise ValueError("analysis missing structured fields: " + ", ".join(missing_fields))

    metadata = sections["## 证据元数据"]
    for required in ["Fulltext Quality", "Evidence Coverage", "Confidence", "Summary"]:
        if required not in metadata:
            raise ValueError(f"analysis Evidence Metadata missing: {required}")

    strict_issues = strict_contract_issues(sections)
    if strict_issues:
        raise ValueError("analysis strict contract issues: " + ", ".join(strict_issues))


def replace_or_insert_section(body: str, heading: str, section_body: str) -> str:
    new_section = f"{heading}\n\n{section_body.strip()}\n"
    pattern = re.compile(rf"(?:^|\n){re.escape(heading)}\n\n.*?(?=\n## |\Z)", re.DOTALL)
    match = pattern.search(body)
    if match:
        prefix = "\n" if match.group(0).startswith("\n") else ""
        return body[: match.start()] + prefix + new_section.rstrip() + body[match.end() :]
    related = re.search(r"\n## 相关概念\n", body)
    if related:
        return body[: related.start()] + "\n\n" + new_section + body[related.start() :]
    return body.rstrip() + "\n\n" + new_section


def update_frontmatter(fm_text: str, schema: dict, analysis_summary: str | None = None) -> str:
    fields = parse_frontmatter_map(fm_text)
    for key, value in list(fields.items()):
        if key == "tags":
            fields[key] = parse_list_value(value)
        else:
            fields[key] = value.strip('"')
    fields["status"] = "done"
    fields["updated"] = today_iso()
    if analysis_summary:
        fields["summary"] = analysis_summary
    return render_frontmatter("literature", fields, schema)


def finalize_content(content: str, analysis: str, schema: dict) -> str:
    parsed = extract_frontmatter(content)
    if not parsed:
        raise ValueError("target note has no frontmatter")
    sections = extract_sections(analysis)
    validate_analysis(sections, schema)

    fm_text, body = parsed
    for heading in SECTION_WRITE_ORDER:
        if heading in sections:
            body = replace_or_insert_section(body, heading, sections[heading])
    frontmatter = update_frontmatter(fm_text, schema, extract_metadata_summary(sections["## 证据元数据"]))
    return frontmatter + body.lstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zotero_key", help="Zotero item key for the target literature note.")
    parser.add_argument("--analysis", required=True, type=Path, help="Markdown file containing the completed reading analysis.")
    args = parse_args_with_write_options(parser)

    target = find_note_by_key(args.zotero_key)
    if not target:
        safe_print(f"ERROR: No literature note found for zotero_key={args.zotero_key}")
        return 1
    if not args.analysis.exists():
        safe_print(f"ERROR: Analysis file not found: {args.analysis}")
        return 1

    schema = load_schema()
    content = target.read_text(encoding="utf-8")
    analysis = args.analysis.read_text(encoding="utf-8")
    try:
        new_content = finalize_content(content, analysis, schema)
    except ValueError as exc:
        safe_print(f"ERROR: {exc}")
        return 1
    safe_write(target, new_content, dry_run=args.dry_run, backup=not args.no_backup)
    safe_print(f"FINALIZED: {target.relative_to(vault_path())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
