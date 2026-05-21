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
WEAK_EVIDENCE_CLASSES = {"note_derived", "abstract_only", "not_evidenced"}
ANCHOR_REQUIRED_EVIDENCE_CLASSES = {
    "pdf_verified",
    "table_verified",
    "figure_verified",
    "appendix_verified",
    "result_row_unconfirmed",
}
ALLOWED_EVIDENCE_CLASSES = ANCHOR_REQUIRED_EVIDENCE_CLASSES | WEAK_EVIDENCE_CLASSES
ALLOWED_ANCHOR_TYPES = {"section", "table", "figure", "appendix", "result_row", "snippet", "abstract", "note_only"}
REVIEW_ONLY_DOWNSTREAM_USES = {"screening_only", "requires_human_check"}
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
    next_heading = re.search(r"^###\s+", markdown[start:], flags=re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def remove_subsection(markdown: str, heading: str) -> str:
    match = re.search(rf"^###\s+{re.escape(heading)}\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return markdown
    start = match.start()
    after_heading = match.end()
    next_heading = re.search(r"^###\s+", markdown[after_heading:], flags=re.MULTILINE)
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
    return re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")


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
        "prohibit",
        "forbid",
        "禁止",
        "不得",
        "不能",
        "无需",
        "不需要",
        "不依赖",
        "不使用",
        "不包含",
        "不做",
    ]
    hits = []
    for token in tokens:
        token_lower = token.lower()
        for match in re.finditer(re.escape(token_lower), lowered):
            start = max(0, match.start() - 36)
            context = lowered[start : match.start()]
            clause_context = re.split(r"[.;。；\n]", context)[-1]
            if any(negator in clause_context for negator in negators):
                continue
            hits.append(token)
            break
    return hits


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


def validate_baseline_pressure(section: str) -> list[str]:
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
        "cabinet",
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
        "柜门",
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
        "protocol": ["protocol", "procedure", "steps", "步骤", "流程"],
        "metric": ["metric", "指标"],
        "pass_condition": ["pass condition", "通过条件", "pass:"],
        "fail_or_kill_condition": ["fail condition", "kill condition", "失败条件", "kill:"],
    }
    lowered = section.lower()
    for code, tokens in required_fields.items():
        if not any(token.lower() in lowered for token in tokens):
            issues.append(f"no_hardware_micro_test_missing_{code}")
    return issues


def validate_transfer_risk(section: str, idea_fuel: str) -> list[str]:
    values = parse_key_values(section)
    source_domain = first_key_value(values, "Source domain")
    target_domain = first_key_value(values, "Target domain")
    combined = f"{section}\n{idea_fuel}"
    lowered = combined.lower()
    source_lower = source_domain.lower()
    target_lower = target_domain.lower()
    issues: list[str] = []
    dlo_transfer = "dlo" in lowered and "dlo" not in source_lower
    if dlo_transfer:
        required = {
            "source_domain": ("Source domain",),
            "target_domain": ("Target domain",),
            "transfer_distance": ("Transfer distance",),
            "why_transfer_may_fail": ("Why transfer may fail",),
            "negative_transfer_risk": ("Negative transfer risk",),
            "dlo_replacement_baseline": ("DLO replacement baseline",),
            "kill_condition": ("Kill condition", "DLO-specific kill condition"),
        }
        for label, aliases in required.items():
            if blank_or_placeholder(first_key_value(values, *aliases)):
                issues.append(f"transfer_risk_missing:{label}")

    distance = normalize_token(first_key_value(values, "Transfer distance"))
    if distance:
        allowed = {"none": 0, "low": 1, "medium": 2, "high": 3, "extreme": 4}
        if distance not in allowed:
            issues.append(f"transfer_risk_bad_distance:{distance}")
        generation_source = any(token in source_lower for token in ["animation", "video", "generation", "generative", "language-only", "pure perception"])
        physical_eval = any(token in lowered for token in ["physical closed-loop", "closed-loop manipulation", "contact dynamics", "dlo control", "physical control"])
        if generation_source and ("dlo" in target_lower or "dlo" in lowered) and distance in allowed and allowed[distance] < allowed["high"] and not physical_eval:
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
    if sections.get("## Baseline Pressure"):
        issues.extend(validate_baseline_pressure(sections["## Baseline Pressure"]))
    if sections.get("## No-hardware Micro-test"):
        issues.extend(validate_no_hardware_micro_test(sections["## No-hardware Micro-test"]))
    if sections.get("## Transfer Risk"):
        issues.extend(validate_transfer_risk(sections["## Transfer Risk"], sections.get("## Idea Fuel", "")))
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
