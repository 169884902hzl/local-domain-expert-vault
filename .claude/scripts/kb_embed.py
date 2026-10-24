"""Local embedding index for stable wiki notes.

The embedding backend is an OpenAI-compatible endpoint configured by
KB_EMBED_API_BASE and KB_EMBED_MODEL. Missing or unavailable services raise
EmbeddingUnavailable so callers can degrade to keyword-only behavior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by CI smoke import path
    np = None  # type: ignore[assignment]
    _NUMPY_IMPORT_ERROR = exc
else:
    _NUMPY_IMPORT_ERROR = None

from kb_common import extract_frontmatter, parse_frontmatter_map, parse_list_value, safe_print, vault_path


class EmbeddingUnavailable(RuntimeError):
    """Raised when the configured embedding backend or local index is unavailable."""


class _MissingNumpy:
    def __getattr__(self, name: str) -> Any:
        raise EmbeddingUnavailable(f"numpy is required for embedding index operations: {_NUMPY_IMPORT_ERROR}") from _NUMPY_IMPORT_ERROR


if np is None:
    np = _MissingNumpy()  # type: ignore[assignment]


def _settings_env() -> dict[str, str]:
    try:
        settings = json.loads(vault_path(".claude", "settings.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    env = settings.get("env", {})
    if not isinstance(env, dict):
        return {}
    return {str(key): str(value) for key, value in env.items() if value is not None}


SETTINGS_ENV = _settings_env()


def _env_value(name: str, default: str = "") -> str:
    value = os.environ.get(name)
    if value is None or not value.strip():
        value = SETTINGS_ENV.get(name, default)
    return str(value).strip()


def _configured_model() -> str:
    return _env_value("KB_EMBED_MODEL", "bge-m3") or "bge-m3"


EMBED_MODEL_NAME = _configured_model()
EMBED_DIM_EXPECTED = 1024
EMBED_TEXT_VERSION = "v2"
STUB_MARKERS = ("待精读补充",)
TOPIC_SECTIONS = ("摘要", "结构化提取")
CONCEPT_SECTIONS = ("Definition", "Key Ideas", "Method Families", "Evidence Map", "Open Problems", "Related Concepts")
ENTITY_SECTIONS = ("基本信息", "研究方向", "Papers", "Related Papers", "Notes")

EMBED_ROOT = vault_path("projects", "research-agenda", "evidence", "embeddings")
VECTORS_PATH = EMBED_ROOT / "kb_vectors.npy"
META_PATH = EMBED_ROOT / "kb_meta.jsonl"
MANIFEST_PATH = EMBED_ROOT / "kb_index_manifest.json"
ANCHOR_VECTORS_PATH = EMBED_ROOT / "read_lib_anchor.npy"
ANCHOR_META_PATH = EMBED_ROOT / "read_lib_anchor.json"

DEFAULT_BATCH_SIZE = 48


def _safe_stderr(message: object) -> None:
    text = str(message)
    encoding = sys.stderr.encoding or "utf-8"
    print(text.encode(encoding, errors="backslashreplace").decode(encoding), file=sys.stderr, flush=True)


def _strip_quotes(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _api_config() -> tuple[str, str, str]:
    base = _env_value("KB_EMBED_API_BASE").rstrip("/")
    if not base:
        raise EmbeddingUnavailable("KB_EMBED_API_BASE is not configured")
    model = _configured_model()
    api_key = _env_value("KB_EMBED_API_KEY")
    return base, model, api_key


def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
    if matrix.ndim != 2:
        raise EmbeddingUnavailable(f"embedding response is not a 2D matrix: shape={matrix.shape}")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms <= 0):
        raise EmbeddingUnavailable("embedding response contains zero-vector rows")
    return (matrix / norms).astype(np.float32, copy=False)


def embed_texts(texts: list[str], *, is_query: bool = False) -> np.ndarray:
    """Embed texts via the configured OpenAI-compatible endpoint.

    bge-m3 does not use E5-style query/passsage prefixes, so is_query is kept
    for API symmetry but intentionally ignored.
    """
    del is_query
    if not texts:
        return np.empty((0, EMBED_DIM_EXPECTED), dtype=np.float32)
    base, model, api_key = _api_config()
    url = f"{base}/embeddings"
    payload = json.dumps({"model": model, "input": texts}, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            status = getattr(response, "status", 200)
            raw = response.read().decode("utf-8")
    except (OSError, TimeoutError, urllib.error.URLError) as exc:
        raise EmbeddingUnavailable(f"embedding request failed:{type(exc).__name__}:{exc}") from exc
    if status != 200:
        raise EmbeddingUnavailable(f"embedding request returned HTTP {status}")
    try:
        data = json.loads(raw)
        rows = data.get("data")
        if not isinstance(rows, list) or len(rows) != len(texts):
            raise ValueError(f"unexpected data rows: {type(rows).__name__}")
        vectors = []
        for index, item in enumerate(rows):
            if not isinstance(item, dict) or not isinstance(item.get("embedding"), list):
                raise ValueError(f"missing embedding at row {index}")
            vectors.append([float(value) for value in item["embedding"]])
        matrix = np.asarray(vectors, dtype=np.float32)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise EmbeddingUnavailable(f"embedding response parse failed:{type(exc).__name__}:{exc}") from exc
    if matrix.shape[1] != EMBED_DIM_EXPECTED:
        raise EmbeddingUnavailable(f"embedding dim mismatch: expected={EMBED_DIM_EXPECTED} got={matrix.shape[1]}")
    return _normalize_rows(matrix)


def _section(body: str, name: str) -> str:
    pattern = rf"(?ms)^##\s+{re.escape(name)}\s*\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, body)
    if not match:
        return ""
    return match.group(1).strip()


def _clean_summary(text: str) -> str:
    return re.sub(r"\[C\d+\]", "", text)


def build_embed_text(fields: dict[str, str], body: str) -> str:
    note_type = _strip_quotes(fields.get("type", ""))
    if note_type == "concept":
        sections = CONCEPT_SECTIONS
    elif note_type == "entity":
        sections = ENTITY_SECTIONS
    else:
        sections = TOPIC_SECTIONS
    parts = [
        _strip_quotes(fields.get("title", "")),
        _clean_summary(_strip_quotes(fields.get("summary", ""))),
        *(_section(body, name) for name in sections),
    ]
    text = "\n\n".join(part.strip() for part in parts if part and part.strip())
    return re.sub(r"\s+", " ", text).strip()[:2000]


def _note_payload(path: Path) -> tuple[dict[str, str], str, str]:
    text = path.read_text(encoding="utf-8")
    parsed = extract_frontmatter(text)
    if not parsed:
        return {}, text, ""
    fields = parse_frontmatter_map(parsed[0])
    return fields, parsed[1], text


def iter_done_topic_notes() -> list[Path]:
    paths: list[Path] = []
    for path in sorted(vault_path("wiki", "topics").glob("*.md")):
        fields, _body, text = _note_payload(path)
        if _strip_quotes(fields.get("status", "")) != "done":
            continue
        if any(marker in text for marker in STUB_MARKERS):
            continue
        paths.append(path)
    return paths


def _entity_has_description(fields: dict[str, str], body: str) -> bool:
    return bool(
        _strip_quotes(fields.get("title", ""))
        and (
            _strip_quotes(fields.get("summary", ""))
            or re.sub(r"\s+", "", body)
        )
    )


def iter_index_notes() -> list[Path]:
    paths = iter_done_topic_notes()
    for folder, expected_type in (("concepts", "concept"), ("entities", "entity")):
        for path in sorted(vault_path("wiki", folder).glob("*.md")):
            fields, body, text = _note_payload(path)
            if _strip_quotes(fields.get("type", "")) != expected_type:
                continue
            status = _strip_quotes(fields.get("status", ""))
            if expected_type == "concept" and status != "done":
                continue
            if expected_type == "entity" and (status == "archived" or not _entity_has_description(fields, body)):
                continue
            if any(marker in text for marker in STUB_MARKERS):
                continue
            paths.append(path)
    return paths


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _rel(path: Path) -> str:
    return str(path.relative_to(vault_path())).replace("\\", "/")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def _read_manifest() -> dict[str, Any] | None:
    if not MANIFEST_PATH.exists():
        return None
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _manifest_compatible(manifest: dict[str, Any] | None) -> bool:
    if not manifest:
        return False
    return (
        str(manifest.get("model_name")) == _configured_model()
        and int(manifest.get("dim") or 0) == EMBED_DIM_EXPECTED
        and str(manifest.get("embed_text_version")) == EMBED_TEXT_VERSION
    )


def _meta_for_note(path: Path, fields: dict[str, str], embed_text: str, row: int) -> dict[str, Any]:
    stat = path.stat()
    return {
        "row": row,
        "path": _rel(path),
        "zotero_key": _strip_quotes(fields.get("zotero_key", "")),
        "title": _strip_quotes(fields.get("title", "")),
        "note_type": _strip_quotes(fields.get("type", "")),
        "year": _strip_quotes(fields.get("year", "")),
        "tags": parse_list_value(fields.get("tags", "")),
        "mtime": stat.st_mtime,
        "text_hash": _text_hash(embed_text),
        "embed_text_version": EMBED_TEXT_VERSION,
        "model_name": _configured_model(),
        "dim": EMBED_DIM_EXPECTED,
    }


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def _write_manifest(rows: list[dict[str, Any]], stats: dict[str, int]) -> dict[str, Any]:
    manifest = {
        "schema_version": "kb_embedding_index.v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model_name": _configured_model(),
        "dim": EMBED_DIM_EXPECTED,
        "embed_text_version": EMBED_TEXT_VERSION,
        "vector_path": _rel(VECTORS_PATH),
        "meta_path": _rel(META_PATH),
        "anchor_vector_path": _rel(ANCHOR_VECTORS_PATH),
        "anchor_meta_path": _rel(ANCHOR_META_PATH),
        "total": len(rows),
        "stats": stats,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    return manifest


def _anchor_indices(meta: list[dict[str, Any]]) -> list[int]:
    indices: list[int] = []
    for index, row in enumerate(meta):
        note_type = str(row.get("note_type", ""))
        path = str(row.get("path", ""))
        if note_type == "literature" or path.startswith("wiki/topics/"):
            indices.append(index)
    return indices


def build_index(*, rebuild: bool = False, dry_run: bool = False) -> dict[str, int]:
    notes = iter_index_notes()
    old_manifest: dict[str, Any] | None = None
    old_meta: list[dict[str, Any]] = []
    old_vectors: np.ndarray | None = None
    compatible = False
    if not rebuild:
        try:
            old_manifest = _read_manifest()
            compatible = _manifest_compatible(old_manifest)
            if compatible and VECTORS_PATH.exists() and META_PATH.exists():
                old_meta = _read_jsonl(META_PATH)
                old_vectors = np.load(VECTORS_PATH)
                if old_vectors.shape[0] != len(old_meta):
                    compatible = False
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            safe_print(f"EMBED_INDEX_REBUILD_REQUIRED: {type(exc).__name__}:{exc}")
            compatible = False
    old_by_path = {str(row.get("path")): row for row in old_meta} if compatible else {}
    old_vector_by_path = {
        str(row.get("path")): old_vectors[int(row.get("row", -1))]
        for row in old_meta
        if old_vectors is not None and 0 <= int(row.get("row", -1)) < old_vectors.shape[0]
    } if compatible else {}

    new_meta: list[dict[str, Any]] = []
    vector_rows: list[np.ndarray | None] = []
    pending_texts: list[str] = []
    pending_rows: list[int] = []
    current_paths: set[str] = set()
    stats = {"added": 0, "updated": 0, "unchanged": 0, "removed": 0, "total": len(notes)}

    for path in notes:
        fields, body, _raw = _note_payload(path)
        embed_text = build_embed_text(fields, body)
        row_index = len(new_meta)
        meta = _meta_for_note(path, fields, embed_text, row_index)
        rel_path = str(meta["path"])
        current_paths.add(rel_path)
        old_row = old_by_path.get(rel_path)
        reusable = False
        if old_row and rel_path in old_vector_by_path:
            old_mtime = float(old_row.get("mtime") or 0.0)
            if abs(old_mtime - float(meta["mtime"])) < 1e-6 or str(old_row.get("text_hash")) == meta["text_hash"]:
                reusable = True
        if reusable:
            stats["unchanged"] += 1
            vector_rows.append(old_vector_by_path[rel_path])
        else:
            if old_row:
                stats["updated"] += 1
            else:
                stats["added"] += 1
            vector_rows.append(None)
            pending_rows.append(row_index)
            pending_texts.append(embed_text)
        new_meta.append(meta)

    stats["removed"] = len(set(old_by_path) - current_paths)
    if dry_run:
        safe_print(json.dumps(stats, ensure_ascii=False, sort_keys=True))
        return stats

    for start in range(0, len(pending_texts), DEFAULT_BATCH_SIZE):
        batch_texts = pending_texts[start : start + DEFAULT_BATCH_SIZE]
        batch_vectors = embed_texts(batch_texts)
        for offset, vector in enumerate(batch_vectors):
            vector_rows[pending_rows[start + offset]] = vector.astype(np.float32, copy=False)

    if any(row is None for row in vector_rows):
        raise EmbeddingUnavailable("internal index build error: missing vector rows")
    matrix = np.vstack([row for row in vector_rows if row is not None]).astype(np.float32, copy=False)
    anchor_indices = _anchor_indices(new_meta)
    anchor_matrix = matrix[anchor_indices] if anchor_indices else np.empty((0, EMBED_DIM_EXPECTED), dtype=np.float32)
    EMBED_ROOT.mkdir(parents=True, exist_ok=True)
    np.save(VECTORS_PATH, matrix)
    _write_jsonl(META_PATH, new_meta)
    np.save(ANCHOR_VECTORS_PATH, anchor_matrix)
    ANCHOR_META_PATH.write_text(
        json.dumps(
            {
                "schema_version": "read_lib_anchor.v1",
                "mode": "topk",
                "top_k": 10,
                "model_name": _configured_model(),
                "dim": EMBED_DIM_EXPECTED,
                "source_manifest": _rel(MANIFEST_PATH),
                "rows": int(anchor_matrix.shape[0]),
                "source_rows": len(new_meta),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    _write_manifest(new_meta, stats)
    safe_print(json.dumps(stats, ensure_ascii=False, sort_keys=True))
    return stats


def load_index() -> tuple[np.ndarray, list[dict[str, Any]], dict[str, Any]] | None:
    try:
        manifest = _read_manifest()
        if not _manifest_compatible(manifest):
            return None
        if not VECTORS_PATH.exists() or not META_PATH.exists():
            return None
        matrix = np.load(VECTORS_PATH)
        meta = _read_jsonl(META_PATH)
        if matrix.ndim != 2 or matrix.shape[0] != len(meta) or matrix.shape[1] != EMBED_DIM_EXPECTED:
            return None
        return matrix.astype(np.float32, copy=False), meta, manifest or {}
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        _safe_stderr(f"EMBED_INDEX_UNAVAILABLE: {type(exc).__name__}:{exc}")
        return None


def _read_anchor_meta() -> dict[str, Any]:
    if not ANCHOR_META_PATH.exists():
        return {}
    try:
        return json.loads(ANCHOR_META_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _anchor_status(
    index: tuple[np.ndarray, list[dict[str, Any]], dict[str, Any]] | None = None,
    anchor_matrix: np.ndarray | None = None,
) -> dict[str, Any]:
    loaded = index if index is not None else load_index()
    if loaded is None:
        return {"status": "index_unavailable", "path": _rel(ANCHOR_VECTORS_PATH)}
    _matrix, meta, _manifest = loaded
    expected_rows = len(_anchor_indices(meta))
    anchor_meta = _read_anchor_meta()
    if anchor_matrix is None:
        if not ANCHOR_VECTORS_PATH.exists():
            return {
                "status": "missing",
                "path": _rel(ANCHOR_VECTORS_PATH),
                "expected_rows": expected_rows,
                "source_rows": len(meta),
            }
        try:
            anchor_matrix = np.load(ANCHOR_VECTORS_PATH)
        except (OSError, ValueError) as exc:
            return {"status": "unreadable", "path": _rel(ANCHOR_VECTORS_PATH), "error": f"{type(exc).__name__}:{exc}"}
    rows = int(anchor_matrix.shape[0]) if anchor_matrix.ndim == 2 else -1
    problems = []
    if anchor_matrix.ndim != 2 or anchor_matrix.shape[1] != EMBED_DIM_EXPECTED:
        problems.append(f"bad_shape:{list(anchor_matrix.shape)}")
    if rows != expected_rows:
        problems.append(f"rows:{rows}!={expected_rows}")
    meta_rows = anchor_meta.get("rows")
    try:
        if meta_rows is not None and int(meta_rows) != expected_rows:
            problems.append(f"meta_rows:{meta_rows}!={expected_rows}")
    except (TypeError, ValueError):
        problems.append(f"bad_meta_rows:{meta_rows}")
    source_rows = anchor_meta.get("source_rows")
    try:
        if source_rows is not None and int(source_rows) != len(meta):
            problems.append(f"source_rows:{source_rows}!={len(meta)}")
    except (TypeError, ValueError):
        problems.append(f"bad_source_rows:{source_rows}")
    return {
        "status": "stale" if problems else "ok",
        "path": _rel(ANCHOR_VECTORS_PATH),
        "rows": rows,
        "expected_rows": expected_rows,
        "source_rows": len(meta),
        "meta": anchor_meta,
        "problems": problems,
    }


def load_read_lib_anchor() -> np.ndarray:
    try:
        if not ANCHOR_VECTORS_PATH.exists():
            raise FileNotFoundError(str(ANCHOR_VECTORS_PATH))
        matrix = np.load(ANCHOR_VECTORS_PATH)
        if matrix.ndim != 2 or matrix.shape[1] != EMBED_DIM_EXPECTED:
            raise ValueError(f"bad anchor shape: {matrix.shape}")
        status = _anchor_status(load_index(), matrix)
        if status.get("status") != "ok":
            raise ValueError(f"stale anchor:{status.get('problems', [status.get('status')])}")
        return matrix.astype(np.float32, copy=False)
    except (OSError, ValueError) as exc:
        raise EmbeddingUnavailable(f"read library anchor unavailable:{type(exc).__name__}:{exc}") from exc


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    av = np.asarray(a, dtype=np.float32).reshape(-1)
    bv = np.asarray(b, dtype=np.float32).reshape(-1)
    denom = float(np.linalg.norm(av) * np.linalg.norm(bv))
    if denom <= 0:
        return 0.0
    return float(np.dot(av, bv) / denom)


def query_vector_similar(qvec: np.ndarray, matrix: np.ndarray, top_k: int = 10) -> list[tuple[int, float]]:
    if matrix.size == 0:
        return []
    vector = np.asarray(qvec, dtype=np.float32).reshape(-1)
    scores = matrix @ vector
    limit = max(0, min(int(top_k), scores.shape[0]))
    order = np.argsort(-scores)[:limit]
    return [(int(index), float(scores[index])) for index in order]


def embed_anchor(matrix: np.ndarray, meta: list[dict[str, Any]], *, mode: str = "topk") -> np.ndarray:
    if mode != "topk":
        raise EmbeddingUnavailable(f"unsupported anchor mode:{mode}")
    source = np.asarray(matrix, dtype=np.float32)
    indices = _anchor_indices(meta)
    if not indices:
        return np.empty((0, EMBED_DIM_EXPECTED), dtype=np.float32)
    return source[indices]


def query_similar(query: str, top_k: int = 10, index: tuple[np.ndarray, list[dict[str, Any]], dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    loaded = index if index is not None else load_index()
    if loaded is None:
        return []
    matrix, meta, _manifest = loaded
    try:
        qvec = embed_texts([query], is_query=True)[0]
    except EmbeddingUnavailable:
        return []
    hits = []
    for row, score in query_vector_similar(qvec, matrix, top_k=top_k):
        item = dict(meta[row])
        item["similarity"] = score
        hits.append(item)
    return hits


def _stats() -> dict[str, Any]:
    index = load_index()
    if index is None:
        return {"status": "missing_or_incompatible", "path": _rel(EMBED_ROOT)}
    matrix, meta, manifest = index
    return {
        "status": "ok",
        "rows": len(meta),
        "shape": list(matrix.shape),
        "anchor": _anchor_status(index),
        "manifest": manifest,
    }


def _ping() -> int:
    try:
        matrix = embed_texts(["robotic manipulation", "机器人操控"])
        sim = cosine(matrix[0], matrix[1])
    except EmbeddingUnavailable as exc:
        safe_print(json.dumps({"status": "unavailable", "error": str(exc)}, ensure_ascii=False))
        return 1
    safe_print(json.dumps({"status": "ok", "shape": list(matrix.shape), "cross_lingual_cosine": sim}, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--rebuild", action="store_true")
    build.add_argument("--dry-run", action="store_true")
    query = sub.add_parser("query")
    query.add_argument("text")
    query.add_argument("--top-k", type=int, default=10)
    anchor = sub.add_parser("anchor")
    anchor.add_argument("--mode", default="topk")
    sub.add_parser("ping")
    sub.add_parser("stats")
    args = parser.parse_args()

    if args.command == "build":
        build_index(rebuild=args.rebuild, dry_run=args.dry_run)
        return 0
    if args.command == "query":
        safe_print(json.dumps(query_similar(args.text, top_k=args.top_k), ensure_ascii=False, indent=2))
        return 0
    if args.command == "anchor":
        loaded = load_index()
        if loaded is None:
            safe_print("EMBED_INDEX_UNAVAILABLE")
            return 1
        matrix, meta, _manifest = loaded
        anchor_matrix = embed_anchor(matrix, meta, mode=args.mode)
        EMBED_ROOT.mkdir(parents=True, exist_ok=True)
        np.save(ANCHOR_VECTORS_PATH, anchor_matrix)
        ANCHOR_META_PATH.write_text(
            json.dumps(
                {
                    "schema_version": "read_lib_anchor.v1",
                    "mode": args.mode,
                    "rows": int(anchor_matrix.shape[0]),
                    "source_rows": len(meta),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        safe_print(f"READ_LIB_ANCHOR: rows={int(anchor_matrix.shape[0])} source_rows={len(meta)} mode={args.mode}")
        return 0
    if args.command == "ping":
        return _ping()
    if args.command == "stats":
        safe_print(json.dumps(_stats(), ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
