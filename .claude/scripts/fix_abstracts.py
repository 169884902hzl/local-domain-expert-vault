"""Clean and annotate English abstracts in topic notes."""
from __future__ import annotations

import argparse
import re

from kb_common import (
    extract_frontmatter,
    parse_args_with_write_options,
    parse_frontmatter_map,
    safe_write,
    vault_path,
)


TOPICS_DIR = vault_path("wiki", "topics")

# Terms: no duplicates, will be sorted by length for single-pass matching.
TERMS = [
    ("deformable linear object", "可变形物体"),
    ("deformable object", "可变形物体"),
    ("reinforcement learning", "强化学习"),
    ("imitation learning", "模仿学习"),
    ("behavioral cloning", "行为克隆"),
    ("diffusion policy", "扩散策略"),
    ("diffusion model", "扩散模型"),
    ("vision-language model", "视觉-语言模型"),
    ("large language model", "大语言模型"),
    ("robotic manipulation", "机器人操控"),
    ("robot manipulation", "机器人操控"),
    ("mobile manipulation", "移动操控"),
    ("bimanual manipulation", "双臂操控"),
    ("dual-arm manipulation", "双臂操控"),
    ("dexterous manipulation", "灵巧操控"),
    ("state-of-the-art", "现有最优方法"),
    ("sim-to-real", "仿真到真实迁移"),
    ("domain adaptation", "领域适应"),
    ("behavior tree", "行为树"),
    ("gaussian process", "高斯过程"),
    ("representation learning", "表征学习"),
    ("inverse dynamics", "逆动力学"),
    ("point cloud", "点云"),
    ("self-supervised", "自监督"),
    ("end-to-end", "端到端"),
    ("zero-shot", "零样本"),
    ("few-shot", "少样本"),
    ("one-shot", "单样本"),
    ("multi-task", "多任务"),
    ("long-horizon", "长时序"),
    ("closed-loop", "闭环"),
    ("open-loop", "开环"),
    ("multi-modal", "多模态"),
    ("multimodal", "多模态"),
    ("data-efficient", "数据高效"),
    ("contact-rich", "接触丰富"),
    ("manipulation", "操控"),
    ("demonstration", "示范数据"),
    ("grasping", "抓取"),
    ("bimanual", "双臂"),
    ("dual-arm", "双臂"),
    ("dexterous", "灵巧"),
    ("tactile", "触觉"),
    ("diffusion", "扩散"),
    ("reward", "奖励"),
    ("affordance", "可供性"),
    ("embodiment", "具身"),
    ("pretraining", "预训练"),
    ("assembly", "装配"),
    ("DLO", "可变形物体"),
    ("outperform", "优于"),
]


def build_term_pattern() -> tuple[dict[str, str], re.Pattern[str], re.Pattern[str]]:
    seen = set()
    unique_terms = []
    for english, chinese in TERMS:
        key = english.lower()
        if key not in seen:
            seen.add(key)
            unique_terms.append((english, chinese))

    term_lookup = {english.lower(): chinese for english, chinese in unique_terms}
    sorted_terms = sorted(unique_terms, key=lambda item: -len(item[0]))
    term_pattern = re.compile(
        r"\b(" + "|".join(re.escape(english) for english, _ in sorted_terms) + r")\b",
        re.IGNORECASE,
    )
    strip_pattern = re.compile(r"（[^）]*）")
    return term_lookup, term_pattern, strip_pattern


TERM_LOOKUP, TERM_PATTERN, STRIP_PATTERN = build_term_pattern()


def annotate_abstract(text: str) -> str:
    """Strip old annotations, then apply clean single-pass annotations."""
    clean = STRIP_PATTERN.sub("", text)
    urls: list[str] = []

    def protect_url(match: re.Match[str]) -> str:
        urls.append(match.group(0))
        return f"__URL_PLACEHOLDER_{len(urls) - 1}__"

    protected = re.sub(r"https?://\S+", protect_url, clean)

    def replace_match(match: re.Match[str]) -> str:
        matched = match.group(0)
        chinese = TERM_LOOKUP.get(matched.lower())
        if chinese:
            return matched + f"（{chinese}）"
        return matched

    annotated = TERM_PATTERN.sub(replace_match, protected)
    for index, url in enumerate(urls):
        annotated = annotated.replace(f"__URL_PLACEHOLDER_{index}__", url)
    return annotated


def fix_content(content: str) -> str:
    parsed = extract_frontmatter(content)
    summary = ""
    if parsed:
        fields = parse_frontmatter_map(parsed[0])
        summary = fields.get("summary", "").strip().strip('"')

    content = re.sub(
        r"\n## 中文摘要\n\n.*?\n\n## 中文简述",
        "\n\n## 中文简述",
        content,
        flags=re.DOTALL,
    )
    content = content.replace("## Abstract", "## 摘要")
    content = content.replace("## 摘要（English）", "## 摘要")
    content = content.replace("## Key Contributions", "## 关键贡献")

    if "## 中文简述" not in content and summary:
        content = re.sub(
            r"(\n## 摘要\n\n.*?)(\n\n## )",
            rf"\1\n\n## 中文简述\n\n{summary}\n\2",
            content,
            count=1,
            flags=re.DOTALL,
        )

    parts = content.split("## 摘要\n\n", 1)
    if len(parts) != 2:
        return content
    after = parts[1].split("\n\n## ", 1)
    english_abstract = after[0]
    if not english_abstract.strip():
        english_abstract = "暂无摘要，待精读时补充"
    rest = after[1] if len(after) > 1 else ""
    annotated = annotate_abstract(english_abstract)
    return parts[0] + "## 摘要\n\n" + annotated + "\n\n## " + rest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    args = parse_args_with_write_options(parser)

    changed = 0
    for path in sorted(TOPICS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        new_content = fix_content(content)
        if new_content != content:
            if safe_write(path, new_content, dry_run=args.dry_run, backup=not args.no_backup):
                changed += 1
    print(f"Done. Cleaned and annotated: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
