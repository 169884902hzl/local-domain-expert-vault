"""Batch-import Zotero collection items as literature stub notes."""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

from kb_common import (
    frontmatter_status,
    load_schema,
    parse_args_with_write_options,
    render_frontmatter,
    safe_print,
    safe_write,
    today_iso,
    vault_path,
)


SCRIPT_DIR = Path(__file__).resolve().parent
OUT_DIR = vault_path("wiki", "topics")
CONFIG_PATH = SCRIPT_DIR / "config.json"

DEFAULT_COLLECTION_KEY = "ZJK4PK4G"
DEFAULT_LIMIT = 500

SKIP_WORDS = {
    "the",
    "for",
    "and",
    "with",
    "from",
    "based",
    "using",
    "learning",
    "robot",
    "robotic",
    "towards",
    "toward",
    "novel",
    "new",
    "policy",
    "object",
    "task",
    "a",
    "an",
    "of",
    "in",
    "on",
    "to",
    "via",
}


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    with CONFIG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def fetch_items(collection_key: str, limit: int) -> list[dict[str, Any]]:
    url = (
        "http://localhost:23119/api/users/0/collections/"
        f"{collection_key}/items?limit={limit}&format=json&start=0"
    )
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        safe_print("ERROR: Cannot connect to Zotero on localhost:23119.")
        safe_print("  Make sure Zotero is running and the built-in API is enabled.")
        safe_print(f"  Detail: {exc}")
        sys.exit(1)
    return [item for item in data if item["data"].get("itemType") not in ("attachment", "note")]


def make_cn_summary(title: str, abstract: str) -> str:
    text = (title + " " + abstract).lower()

    task = ""
    task_map = [
        ("deformable linear", "可变形物体"),
        ("dlo", "可变形物体"),
        ("rope", "绳索操控"),
        ("cable", "线缆操控"),
        ("grasp", "抓取"),
        ("prehensile", "非抓取式操控"),
        ("bimanual", "双臂"),
        ("dual-arm", "双臂"),
        ("dexterous", "灵巧手"),
        ("multi-finger", "多指"),
        ("mobile manipulation", "移动操控"),
        ("navigation", "导航"),
        ("pushing", "推动"),
        ("insertion", "插入"),
    ]
    for keyword, label in task_map:
        if keyword in text:
            task = label
            break
    if not task:
        task = "操控"

    method = ""
    method_map = [
        ("diffusion policy", "扩散策略"),
        ("diffusion", "扩散模型"),
        ("reinforcement learning", "强化学习"),
        ("imitation", "模仿学习"),
        ("behavioral cloning", "行为克隆"),
        ("action chunking", "Action Chunking"),
        ("vision-language", "视觉-语言"),
        ("gpt", "GPT"),
        ("large language model", "大语言模型"),
        ("representation learning", "表征学习"),
        ("pretrain", "预训练"),
        ("transformer", "Transformer"),
        ("gaussian process", "高斯过程"),
        ("behavior tree", "行为树"),
        ("tactile", "触觉感知"),
        ("force", "力控制"),
        ("point cloud", "点云"),
    ]
    for keyword, label in method_map:
        if keyword in text:
            method = label
            break
    if not method:
        method = "学习方法"

    feature = ""
    feature_map = [
        ("sim-to-real", "仿真到真实迁移"),
        ("sim2real", "仿真到真实迁移"),
        ("zero-shot", "零样本泛化"),
        ("generaliz", "泛化能力"),
        ("few-shot", "少样本学习"),
        ("one-shot", "单样本学习"),
        ("self-supervis", "自监督"),
        ("human video", "人类视频学习"),
        ("web video", "网络视频学习"),
        ("closed-loop", "闭环控制"),
        ("end-to-end", "端到端"),
        ("multi-task", "多任务"),
        ("long-horizon", "长时序任务"),
        ("data-efficient", "数据高效"),
        ("contact", "接触丰富"),
    ]
    for keyword, label in feature_map:
        if keyword in text:
            feature = label
            break

    parts = [f"提出基于{method}的{task}方法"]
    if feature:
        parts.append(f"，具有{feature}特点")
    parts.append("。")
    return "".join(parts)


def publication_year(date_text: str) -> str:
    match = re.search(r"(20\d{2})", date_text or "")
    return match.group(1) if match else "unknown"


def item_venue(data: dict[str, Any]) -> str:
    venue = data.get("publicationTitle", "") or data.get("proceedingsTitle", "") or ""
    if venue:
        return venue
    item_type = data.get("itemType", "unknown")
    if item_type == "conferencePaper":
        return data.get("publisher", "Conference")
    if item_type == "preprint":
        return "arXiv Preprint"
    return item_type


def item_authors(data: dict[str, Any]) -> tuple[str, str]:
    authors: list[str] = []
    first_author_last = "unknown"
    for creator in data.get("creators", []):
        if creator.get("creatorType") != "author":
            continue
        last = creator.get("lastName", "")
        first = creator.get("firstName", "")
        name = f"{last}, {first}" if last and first else (last or first or "")
        if name:
            authors.append(name)
        if first_author_last == "unknown" and last:
            first_author_last = re.sub(r"[^a-zA-Z]", "", last).lower()[:20]
    authors_str = "; ".join(authors[:5])
    if len(authors) > 5:
        authors_str += " et al."
    return first_author_last, authors_str


def note_filename(first_author_last: str, year: str, title: str) -> str:
    title_words = re.sub(r"[^a-zA-Z0-9\s]", "", title).split()
    first_word = ""
    for word in title_words:
        if len(word) > 2 and word.lower() not in SKIP_WORDS:
            first_word = word.lower()
            break
    if not first_word and title_words:
        first_word = title_words[0].lower()
    return re.sub(r'[<>:"/\\|?*]', "", f"{first_author_last}{year}{first_word}.md")


def auto_tags(title: str, abstract: str, taxonomy: dict[str, Any]) -> list[str]:
    text = (title + " " + abstract).lower()
    tags = []
    for tag, info in taxonomy.items():
        if any(keyword in text for keyword in info["keywords"]):
            tags.append(tag)
    if not tags:
        tags = ["manipulation"]
    return tags[:5]


def should_write_existing(path: Path, *, force_overwrite_stub: bool) -> bool:
    if not path.exists():
        return True
    status = frontmatter_status(path.read_text(encoding="utf-8"))
    if force_overwrite_stub and status == "stub":
        return True
    safe_print(f"SKIP existing ({status or 'unknown status'}): {path.name}")
    return False


def existing_notes_by_zotero_key() -> dict[str, Path]:
    notes = {}
    for path in sorted(OUT_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        match = re.search(r'^zotero_key:\s*"?([A-Za-z0-9]+)"?\s*$', text, re.MULTILINE)
        if match:
            notes.setdefault(match.group(1), path)
    return notes


def build_note(item: dict[str, Any], schema: dict[str, Any], run_date: str) -> tuple[str, str]:
    data = item["data"]
    key = item["key"]
    title = data.get("title", "Untitled")
    year = publication_year(data.get("date", ""))
    venue = item_venue(data)
    first_author_last, authors = item_authors(data)
    abstract = data.get("abstractNote", "").strip()
    tags = auto_tags(title, abstract, schema["literature"]["tag_taxonomy"])
    cn_tags = [schema["literature"]["tag_taxonomy"].get(tag, {}).get("cn", tag) for tag in tags]
    summary = make_cn_summary(title, abstract)

    frontmatter = render_frontmatter(
        "literature",
        {
            "title": title,
            "tags": tags,
            "created": run_date,
            "updated": run_date,
            "type": "literature",
            "status": "stub",
            "summary": summary,
            "authors": authors,
            "year": year,
            "venue": venue,
            "zotero_key": key,
        },
        schema,
    )
    body = (
        "## 摘要\n\n"
        f"{abstract if abstract else '暂无摘要，待精读时补充'}\n\n"
        "## 中文简述\n\n"
        f"{summary}\n\n"
        f"**研究方向**: {'、'.join(cn_tags)}\n\n"
        "## 关键贡献\n\n"
        f"（待精读 - 在 Claudian 中说 \"精读 {key}\" 即可生成完整分析）\n"
        "\n## 结构化提取\n\n"
        "- Problem: 待精读补充\n"
        "- Method: 待精读补充\n"
        "- Tasks: 待精读补充\n"
        "- Sensors: 待精读补充\n"
        "- Robot Setup: 待精读补充\n"
        "- Metrics: 待精读补充\n"
        "- Limitations: 待精读补充\n"
        "- Evidence Notes: 待精读补充\n"
        "\n## 本地引用关系\n\n"
        "-\n"
    )
    return note_filename(first_author_last, year, title), frontmatter + body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force-overwrite-stub",
        action="store_true",
        help="Overwrite existing files only when their status is stub.",
    )
    args = parse_args_with_write_options(parser)

    config = load_config()
    collection_key = config.get("collection_key", DEFAULT_COLLECTION_KEY)
    limit = int(config.get("limit", DEFAULT_LIMIT))
    schema = load_schema()
    items = fetch_items(collection_key, limit)
    safe_print(f"Top-level items: {len(items)}")

    written = 0
    skipped = 0
    errors = 0
    run_date = today_iso()
    existing_by_key = existing_notes_by_zotero_key()
    for item in items:
        try:
            filename, content = build_note(item, schema, run_date)
            path = existing_by_key.get(item["key"], OUT_DIR / filename)
            if not should_write_existing(path, force_overwrite_stub=args.force_overwrite_stub):
                skipped += 1
                continue
            if safe_write(path, content, dry_run=args.dry_run, backup=not args.no_backup):
                written += 1
        except Exception as exc:
            errors += 1
            safe_print(f"ERROR: {item.get('key', 'unknown')}: {exc}")

    safe_print(f"Done. Written: {written}, Skipped: {skipped}, Errors: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
