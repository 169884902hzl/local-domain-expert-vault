"""Import ranked arXiv papers into Zotero with explicit write preflight."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from arxiv_ranker import ArxivPaper, RankedPaper, normalize_title
from kb_common import safe_print


def _env(name: str, default: str = "") -> str:
    value = os.environ.get(name, "").strip()
    if value or os.name != "nt":
        return value or default
    try:
        import winreg
    except ImportError:
        return default
    for root, subkey in (
        (winreg.HKEY_CURRENT_USER, "Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    ):
        try:
            with winreg.OpenKey(root, subkey) as key:
                value, _ = winreg.QueryValueEx(key, name)
        except OSError:
            continue
        if str(value).strip():
            return str(value).strip()
    return default


def _decode_pref_string(raw: str) -> str:
    try:
        return str(json.loads(f'"{raw}"'))
    except json.JSONDecodeError:
        return raw.replace("\\\\", "\\")


def _zotero_profile_dirs() -> list[Path]:
    appdata = os.environ.get("APPDATA", "").strip()
    if not appdata:
        return []
    profiles_root = Path(appdata) / "Zotero" / "Zotero" / "Profiles"
    if not profiles_root.exists():
        return []
    profiles = [path for path in profiles_root.iterdir() if path.is_dir()]
    return sorted(
        profiles,
        key=lambda path: (path / "prefs.js").stat().st_mtime if (path / "prefs.js").exists() else 0,
        reverse=True,
    )


def _zotero_data_dir_from_profile() -> Path | None:
    data_dir_re = re.compile(r'user_pref\("extensions\.zotero\.dataDir",\s*"(?P<value>(?:\\.|[^"])*)"\);')
    use_data_dir_re = re.compile(r'user_pref\("extensions\.zotero\.useDataDir",\s*(?P<value>true|false)\);')
    for profile_dir in _zotero_profile_dirs():
        prefs_path = profile_dir / "prefs.js"
        if not prefs_path.exists():
            continue
        text = prefs_path.read_text(encoding="utf-8", errors="replace")
        use_match = use_data_dir_re.search(text)
        if use_match and use_match.group("value") != "true":
            continue
        data_match = data_dir_re.search(text)
        if not data_match:
            continue
        candidate = Path(_decode_pref_string(data_match.group("value")))
        if candidate.exists():
            return candidate
    return None


LOCAL_API = _env("ZOTERO_LOCAL_API", "http://127.0.0.1:23119/api/users/0")
LOCAL_CONNECTOR_API = _env("ZOTERO_CONNECTOR_API", "http://127.0.0.1:23119")
WEB_API = _env("ZOTERO_WEB_API", "https://api.zotero.org")
DEFAULT_COLLECTION_KEY = _env("ZOTERO_COLLECTION_KEY", "")
DEFAULT_TAGS = ["auto-arxiv", "embodied-ai", "daily-scout"]
PDF_UPLOAD_DISABLED_VALUES = {"0", "false", "no", "off", "disabled"}
PDF_UPLOAD_ENABLED_VALUES = {"1", "true", "yes", "on", "enabled"}
DEFAULT_LOCAL_PDF_CACHE = Path(_env("ZOTERO_LOCAL_PDF_CACHE", r".local\zotero-pdf-cache"))


@dataclass
class ImportResult:
    status: str
    zotero_key: str = ""
    message: str = ""
    mode: str = ""
    existing: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "zotero_key": self.zotero_key,
            "message": self.message,
            "mode": self.mode,
            "existing": self.existing,
        }


class ZoteroError(RuntimeError):
    pass


def _read_json(url: str, timeout: int = 30) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post_json(url: str, payload: Any, headers: dict[str, str], timeout: int = 30) -> Any:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode("utf-8")
        return json.loads(text) if text.strip() else {}


def _post_form(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int = 30) -> tuple[int, dict[str, Any], bytes]:
    body = urllib.parse.urlencode(payload).encode("utf-8")
    req_headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        text = raw.decode("utf-8", errors="replace")
        parsed = json.loads(text) if text.strip() else {}
        return resp.status, parsed, raw


def _post_bytes(url: str, body: bytes, headers: dict[str, str], timeout: int = 120) -> tuple[int, bytes]:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def _connector_url(path: str) -> str:
    return LOCAL_CONNECTOR_API.rstrip("/") + "/" + path.lstrip("/")


def _connector_headers(content_type: str = "application/json") -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": content_type,
        "X-Zotero-Connector-API-Version": "3",
    }


def _post_connector_json(path: str, payload: Any, timeout: int = 30) -> tuple[int, Any, bytes]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(_connector_url(path), data=body, headers=_connector_headers(), method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        text = raw.decode("utf-8", errors="replace")
        parsed = json.loads(text) if text.strip() else {}
        return resp.status, parsed, raw


def _get_connector(path: str, timeout: int = 30) -> tuple[int, bytes]:
    headers = {
        "Accept": "*/*",
        "X-Zotero-Connector-API-Version": "3",
    }
    req = urllib.request.Request(_connector_url(path), headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def _post_connector_bytes(path: str, body: bytes, metadata: dict[str, Any], timeout: int = 240) -> tuple[int, bytes]:
    headers = {
        **_connector_headers("application/pdf"),
        "Content-Length": str(len(body)),
        "X-Metadata": json.dumps(metadata, ensure_ascii=True),
    }
    req = urllib.request.Request(_connector_url(path), data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def _delete_with_headers(url: str, headers: dict[str, str], timeout: int = 30) -> int:
    req = urllib.request.Request(url, headers=headers, method="DELETE")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status


def _get_json_with_headers(url: str, headers: dict[str, str], timeout: int = 30) -> Any:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode("utf-8")
        return json.loads(text) if text.strip() else {}


def _is_transient_http_status(status: int) -> bool:
    return status in {408, 425, 429, 500, 502, 503, 504}


def _is_transient_network_error(exc: BaseException) -> bool:
    if isinstance(exc, (TimeoutError, ConnectionResetError, ssl.SSLError, socket.timeout)):
        return True
    if isinstance(exc, urllib.error.URLError):
        reason = getattr(exc, "reason", exc)
        if isinstance(reason, (TimeoutError, ConnectionResetError, ssl.SSLError, socket.timeout)):
            return True
        text = str(reason).lower()
        return any(marker in text for marker in ["timed out", "unexpected_eof", "eof occurred", "connection reset"])
    text = str(exc).lower()
    return any(marker in text for marker in ["timed out", "unexpected_eof", "eof occurred", "connection reset"])


def _retry_delay_seconds(attempt: int, exc: BaseException | None = None) -> float:
    if isinstance(exc, urllib.error.HTTPError):
        retry_after = exc.headers.get("Retry-After") if exc.headers else None
        if retry_after:
            try:
                return min(60.0, max(1.0, float(retry_after)))
            except ValueError:
                pass
    return min(30.0, 2.0 ** max(0, attempt - 1))


def _web_headers(api_key: str) -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Zotero-API-Version": "3",
        "Zotero-API-Key": api_key,
    }


def require_collection_key(collection_key: str = DEFAULT_COLLECTION_KEY) -> str:
    key = collection_key.strip()
    if not key:
        raise ZoteroError("missing_collection_key")
    return key


def read_collection(collection_key: str = DEFAULT_COLLECTION_KEY) -> dict[str, Any]:
    collection_key = require_collection_key(collection_key)
    url = f"{LOCAL_API}/collections/{urllib.parse.quote(collection_key)}?format=json"
    return _read_json(url, timeout=10)


def local_library_id(collection_key: str = DEFAULT_COLLECTION_KEY) -> str:
    data = read_collection(collection_key)
    return str(data.get("library", {}).get("id") or "")


def iter_local_items(collection_key: str = DEFAULT_COLLECTION_KEY, limit: int = 100) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    start = 0
    while True:
        url = (
            f"{LOCAL_API}/collections/{urllib.parse.quote(collection_key)}/items"
            f"?limit={limit}&start={start}&format=json"
        )
        batch = _read_json(url, timeout=30)
        real_items = [item for item in batch if item.get("data", {}).get("itemType") not in {"attachment", "note"}]
        items.extend(real_items)
        if len(batch) < limit:
            return items
        start += limit


def _item_text(item: dict[str, Any]) -> str:
    data = item.get("data", {})
    values = [
        data.get("title", ""),
        data.get("DOI", ""),
        data.get("url", ""),
        data.get("archiveLocation", ""),
        data.get("extra", ""),
    ]
    return " ".join(str(value) for value in values).lower()


def find_existing_paper_in_items(paper: ArxivPaper, items: list[dict[str, Any]]) -> ImportResult | None:
    normalized = normalize_title(paper.title)
    arxiv_id = paper.arxiv_id.lower()
    doi = paper.doi.lower()
    for item in items:
        data = item.get("data", {})
        text = _item_text(item)
        title_match = normalize_title(str(data.get("title", ""))) == normalized
        arxiv_match = bool(arxiv_id and arxiv_id in text)
        doi_match = bool(doi and doi in text)
        if title_match or arxiv_match or doi_match:
            return ImportResult(
                status="exists",
                zotero_key=item.get("key", ""),
                message="matched existing Zotero item",
                mode="local_read",
                existing=True,
            )
    return None


def find_existing_paper(paper: ArxivPaper, collection_key: str = DEFAULT_COLLECTION_KEY) -> ImportResult | None:
    return find_existing_paper_in_items(paper, iter_local_items(collection_key))


def _creator(author: str) -> dict[str, str]:
    cleaned = re.sub(r"\s+", " ", author).strip()
    if not cleaned:
        return {"creatorType": "author", "firstName": "", "lastName": "Unknown"}
    parts = cleaned.split(" ")
    if len(parts) == 1:
        return {"creatorType": "author", "firstName": "", "lastName": cleaned}
    return {"creatorType": "author", "firstName": " ".join(parts[:-1]), "lastName": parts[-1]}


def zotero_item_from_ranked(ranked: RankedPaper, collection_key: str = DEFAULT_COLLECTION_KEY) -> dict[str, Any]:
    paper = ranked.paper
    doi = paper.doi or (f"10.48550/arXiv.{paper.arxiv_id}" if paper.arxiv_id else "")
    extra_lines = [
        f"arXiv: {paper.arxiv_id}",
        f"quality_score: {ranked.quality_score}",
        f"quality_decision: {ranked.decision}",
        "quality_label: top1_candidate means high-priority candidate, not guaranteed correctness.",
    ]
    if ranked.reasons:
        extra_lines.append("quality_reasons: " + ", ".join(ranked.reasons))
    if ranked.penalties:
        extra_lines.append("quality_penalties: " + ", ".join(ranked.penalties))
    tags = [{"tag": tag} for tag in DEFAULT_TAGS]
    tags.extend({"tag": f"score-{ranked.quality_score}"} for _ in [0])
    return {
        "itemType": "preprint",
        "title": paper.title,
        "creators": [_creator(author) for author in paper.authors[:12]],
        "abstractNote": paper.summary,
        "date": paper.published[:10] if paper.published else "",
        "archive": "arXiv",
        "archiveLocation": paper.arxiv_id,
        "url": paper.url or paper.pdf_url,
        "DOI": doi,
        "extra": "\n".join(extra_lines),
        "tags": tags,
        "collections": [collection_key],
    }


def zotero_connector_item_from_ranked(ranked: RankedPaper, connector_id: str) -> dict[str, Any]:
    item = zotero_item_from_ranked(ranked)
    item.pop("collections", None)
    item["id"] = connector_id
    return item


def zotero_pdf_attachment_from_ranked(ranked: RankedPaper, parent_key: str, *, file_backed: bool = False) -> dict[str, Any] | None:
    paper = ranked.paper
    pdf_url = paper.pdf_url or (f"https://arxiv.org/pdf/{paper.arxiv_id}" if paper.arxiv_id else "")
    if not pdf_url:
        return None
    filename = pdf_filename_from_ranked(ranked)
    title = f"PDF - {paper.title[:180]}"
    return {
        "itemType": "attachment",
        "parentItem": parent_key,
        "linkMode": "imported_file" if file_backed else "imported_url",
        "title": title,
        "accessDate": "CURRENT_TIMESTAMP",
        "url": pdf_url,
        "note": "",
        "contentType": "application/pdf",
        "charset": "",
        "filename": filename,
        "md5": None,
        "mtime": None,
        "tags": [{"tag": "auto-arxiv-pdf"}],
        "relations": {},
    }


def zotero_linked_pdf_attachment_from_ranked(ranked: RankedPaper, parent_key: str, local_pdf_path: str) -> dict[str, Any] | None:
    paper = ranked.paper
    if not local_pdf_path:
        return None
    filename = pdf_filename_from_ranked(ranked)
    title = f"PDF - {paper.title[:180]}"
    return {
        "itemType": "attachment",
        "parentItem": parent_key,
        "linkMode": "linked_file",
        "title": title,
        "accessDate": "CURRENT_TIMESTAMP",
        "note": "",
        "contentType": "application/pdf",
        "charset": "",
        "path": local_pdf_path,
        "tags": [{"tag": "auto-arxiv-pdf"}, {"tag": "local-linked-pdf"}],
        "relations": {},
    }


def _web_user_id(collection_key: str = DEFAULT_COLLECTION_KEY) -> str:
    explicit = _env("ZOTERO_USER_ID") or _env("ZOTERO_LIBRARY_ID")
    if explicit:
        return explicit
    return local_library_id(collection_key)


def pdf_filename_from_ranked(ranked: RankedPaper) -> str:
    arxiv_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", ranked.paper.arxiv_id or "paper").strip("._")
    return f"arxiv-{arxiv_id}.pdf"


def pdf_download_urls(ranked: RankedPaper) -> list[str]:
    paper = ranked.paper
    candidates: list[str] = []
    if paper.pdf_url:
        candidates.append(paper.pdf_url)
        if paper.pdf_url.startswith("http://"):
            candidates.append("https://" + paper.pdf_url.removeprefix("http://"))
    if paper.arxiv_id:
        arxiv_id = paper.arxiv_id
        candidates.extend(
            [
                f"https://arxiv.org/pdf/{arxiv_id}",
                f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                f"https://export.arxiv.org/pdf/{arxiv_id}",
                f"https://export.arxiv.org/pdf/{arxiv_id}.pdf",
            ]
        )
    seen: set[str] = set()
    unique: list[str] = []
    for url in candidates:
        if url and url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def _download_pdf_bytes(ranked: RankedPaper, timeout: int = 120) -> bytes:
    urls = pdf_download_urls(ranked)
    if not urls:
        raise ZoteroError("no PDF URL available")
    errors: list[str] = []
    for pdf_url in urls:
        for attempt in range(1, 4):
            req = urllib.request.Request(
                pdf_url,
                headers={
                    "Accept": "application/pdf,*/*",
                    "User-Agent": "daily-arxiv-zotero-import/1.0",
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    data = resp.read()
                if data.startswith(b"%PDF"):
                    return data
                errors.append(f"{pdf_url}:not_pdf")
                break
            except urllib.error.HTTPError as exc:
                errors.append(f"{pdf_url}:HTTP_{exc.code}")
                if not _is_transient_http_status(exc.code) or attempt >= 3:
                    break
                time.sleep(_retry_delay_seconds(attempt, exc))
            except Exception as exc:
                errors.append(f"{pdf_url}:{type(exc).__name__}:{str(exc)[:80]}")
                if not _is_transient_network_error(exc) or attempt >= 3:
                    break
                time.sleep(_retry_delay_seconds(attempt, exc))
    raise ZoteroError("pdf_download_failed:" + " | ".join(errors)[-500:])


def cached_pdf_path(ranked: RankedPaper, local_dir: Path = DEFAULT_LOCAL_PDF_CACHE) -> Path | None:
    path = local_dir / pdf_filename_from_ranked(ranked)
    if path.exists() and path.stat().st_size > 1000:
        return path
    return None


def read_pdf_bytes_from_cache_or_download(
    ranked: RankedPaper,
    local_dir: Path = DEFAULT_LOCAL_PDF_CACHE,
    *,
    timeout: int = 45,
) -> bytes:
    cached = cached_pdf_path(ranked, local_dir)
    if cached:
        data = cached.read_bytes()
        if data.startswith(b"%PDF"):
            return data
    data = _download_pdf_bytes(ranked, timeout=timeout)
    local_dir.mkdir(parents=True, exist_ok=True)
    (local_dir / pdf_filename_from_ranked(ranked)).write_bytes(data)
    return data


def download_pdf_to_local_cache(ranked: RankedPaper, local_dir: Path = DEFAULT_LOCAL_PDF_CACHE) -> Path:
    local_dir.mkdir(parents=True, exist_ok=True)
    path = local_dir / pdf_filename_from_ranked(ranked)
    if path.exists() and path.stat().st_size > 1000:
        return path
    data = _download_pdf_bytes(ranked, timeout=45)
    path.write_bytes(data)
    return path


def find_pdf_attachment_web(parent_key: str, *, user_id: str, api_key: str) -> str:
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(parent_key)}/children?format=json"
    children = _get_json_with_headers(url, {**_web_headers(api_key), "Accept": "application/json"}, timeout=30)
    if not isinstance(children, list):
        return ""
    for child in children:
        data = child.get("data", {}) if isinstance(child, dict) else {}
        if data.get("itemType") != "attachment":
            continue
        content_type = str(data.get("contentType", "")).lower()
        path_or_url = " ".join(str(data.get(name, "")) for name in ["path", "url", "filename"]).lower()
        if "pdf" in content_type or ".pdf" in path_or_url or "/pdf/" in path_or_url:
            return str(child.get("key") or data.get("key") or "")
    return ""


def find_file_pdf_attachment_web(parent_key: str, *, user_id: str, api_key: str) -> str:
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(parent_key)}/children?format=json"
    children = _get_json_with_headers(url, {**_web_headers(api_key), "Accept": "application/json"}, timeout=30)
    if not isinstance(children, list):
        return ""
    for child in children:
        data = child.get("data", {}) if isinstance(child, dict) else {}
        if data.get("itemType") != "attachment":
            continue
        content_type = str(data.get("contentType", "")).lower()
        filename = str(data.get("filename", "")).lower()
        if (content_type == "application/pdf" or filename.endswith(".pdf")) and data.get("md5") and data.get("filename"):
            return str(child.get("key") or data.get("key") or "")
    return ""


def find_linked_pdf_attachment_web(parent_key: str, *, user_id: str, api_key: str) -> str:
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(parent_key)}/children?format=json"
    children = _get_json_with_headers(url, {**_web_headers(api_key), "Accept": "application/json"}, timeout=30)
    if not isinstance(children, list):
        return ""
    for child in children:
        data = child.get("data", {}) if isinstance(child, dict) else {}
        if data.get("itemType") != "attachment" or data.get("linkMode") != "linked_file":
            continue
        content_type = str(data.get("contentType", "")).lower()
        path = str(data.get("path", "")).lower()
        if content_type == "application/pdf" or path.endswith(".pdf"):
            return str(child.get("key") or data.get("key") or "")
    return ""


def _is_stored_pdf_attachment_data(data: dict[str, Any]) -> bool:
    if data.get("itemType") != "attachment":
        return False
    if str(data.get("linkMode", "")) == "linked_file":
        return False
    content_type = str(data.get("contentType", "")).lower()
    filename = str(data.get("filename", "")).lower()
    path = str(data.get("path", "")).lower()
    if content_type != "application/pdf" and not filename.endswith(".pdf") and not path.endswith(".pdf"):
        return False
    return bool(
        data.get("md5")
        or data.get("filename")
        or path.startswith("storage:")
        or str(data.get("linkMode", "")) == "imported_file"
    )


def find_stored_pdf_attachment_local(parent_key: str) -> str:
    url = f"{LOCAL_API}/items/{urllib.parse.quote(parent_key)}/children?format=json"
    children = _read_json(url, timeout=20)
    if not isinstance(children, list):
        return ""
    for child in children:
        data = child.get("data", {}) if isinstance(child, dict) else {}
        if _is_stored_pdf_attachment_data(data):
            return str(child.get("key") or data.get("key") or "")
    return ""


def wait_for_stored_pdf_attachment_local(parent_key: str, timeout_seconds: int = 90) -> str:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            key = find_stored_pdf_attachment_local(parent_key)
        except Exception:
            key = ""
        if key:
            return key
        time.sleep(3)
    return ""


def create_linked_pdf_attachment_web(
    ranked: RankedPaper,
    parent_key: str,
    local_pdf_path: str,
    *,
    user_id: str,
    api_key: str,
) -> str:
    existing_key = find_linked_pdf_attachment_web(parent_key, user_id=user_id, api_key=api_key)
    if existing_key:
        return f"linked_pdf_attachment_exists:{existing_key}"
    attachment = zotero_linked_pdf_attachment_from_ranked(ranked, parent_key, local_pdf_path)
    if not attachment:
        return "linked_pdf_attachment_skipped:no_local_path"
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items"
    try:
        response = _post_json(url, [attachment], _web_headers(api_key), timeout=30)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return f"linked_pdf_attachment_failed:HTTP_{exc.code}:{detail[:160]}"
    except Exception as exc:
        return f"linked_pdf_attachment_failed:{type(exc).__name__}:{str(exc)[:160]}"
    successful = response.get("successful", {})
    if "0" in successful:
        key = successful["0"].get("key") or successful["0"].get("data", {}).get("key", "")
        return f"linked_pdf_attachment_created:{key}"
    unchanged = response.get("unchanged", {})
    if "0" in unchanged:
        key = unchanged["0"].get("key") or unchanged["0"].get("data", {}).get("key", "")
        return f"linked_pdf_attachment_exists:{key}"
    failed = response.get("failed", {})
    return "linked_pdf_attachment_failed:" + json.dumps(failed, ensure_ascii=False)[:160]


def upload_pdf_file_web(ranked: RankedPaper, attachment_key: str, *, user_id: str, api_key: str) -> str:
    try:
        pdf_bytes = read_pdf_bytes_from_cache_or_download(ranked)
    except Exception as exc:
        return f"pdf_file_upload_failed:download:{type(exc).__name__}:{str(exc)[:120]}"
    filename = pdf_filename_from_ranked(ranked)
    md5 = hashlib.md5(pdf_bytes).hexdigest()
    mtime = str(int(time.time() * 1000))
    file_url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(attachment_key)}/file"
    auth_headers = {**_web_headers(api_key), "If-None-Match": "*"}
    try:
        _, authorization, _ = _post_form(
            file_url,
            {"md5": md5, "filename": filename, "filesize": len(pdf_bytes), "mtime": mtime},
            auth_headers,
            timeout=60,
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return f"pdf_file_upload_failed:auth_HTTP_{exc.code}:{detail[:120]}"
    except Exception as exc:
        return f"pdf_file_upload_failed:auth:{type(exc).__name__}:{str(exc)[:120]}"
    if authorization.get("exists") == 1:
        return "pdf_file_upload_exists"
    upload_url = authorization.get("url")
    upload_key = authorization.get("uploadKey")
    content_type = authorization.get("contentType")
    prefix = authorization.get("prefix")
    suffix = authorization.get("suffix")
    if not all([upload_url, upload_key, content_type, prefix is not None, suffix is not None]):
        return "pdf_file_upload_failed:bad_authorization:" + json.dumps(authorization, ensure_ascii=False)[:120]
    upload_body = str(prefix).encode("utf-8") + pdf_bytes + str(suffix).encode("utf-8")
    try:
        status, _ = _post_bytes(str(upload_url), upload_body, {"Content-Type": str(content_type)}, timeout=180)
        if status != 201:
            return f"pdf_file_upload_failed:upload_status_{status}"
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return f"pdf_file_upload_failed:upload_HTTP_{exc.code}:{detail[:120]}"
    except Exception as exc:
        return f"pdf_file_upload_failed:upload:{type(exc).__name__}:{str(exc)[:120]}"
    try:
        status, _, _ = _post_form(file_url, {"upload": upload_key}, auth_headers, timeout=60)
        return "pdf_file_upload_registered" if status == 204 else f"pdf_file_upload_failed:register_status_{status}"
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return f"pdf_file_upload_failed:register_HTTP_{exc.code}:{detail[:120]}"
    except Exception as exc:
        return f"pdf_file_upload_failed:register:{type(exc).__name__}:{str(exc)[:120]}"


def delete_item_web(item_key: str, *, user_id: str, api_key: str) -> str:
    item_url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items/{urllib.parse.quote(item_key)}"
    try:
        item = _get_json_with_headers(
            item_url + "?format=json",
            {**_web_headers(api_key), "Accept": "application/json"},
            timeout=30,
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "cleanup_not_found"
        detail = exc.read().decode("utf-8", errors="replace")
        return f"cleanup_failed:get_HTTP_{exc.code}:{detail[:120]}"
    except Exception as exc:
        return f"cleanup_failed:get:{type(exc).__name__}:{str(exc)[:120]}"
    version = str(item.get("version") or "")
    if not version:
        return "cleanup_failed:missing_version"
    try:
        status = _delete_with_headers(
            item_url,
            {**_web_headers(api_key), "If-Unmodified-Since-Version": version},
            timeout=30,
        )
        return "cleanup_deleted" if status == 204 else f"cleanup_failed:delete_status_{status}"
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return "cleanup_not_found"
        detail = exc.read().decode("utf-8", errors="replace")
        return f"cleanup_failed:delete_HTTP_{exc.code}:{detail[:120]}"
    except Exception as exc:
        return f"cleanup_failed:delete:{type(exc).__name__}:{str(exc)[:120]}"


def should_upload_pdf_files() -> bool:
    value = _env("ZOTERO_UPLOAD_PDF_FILES")
    if value:
        return value.lower() not in PDF_UPLOAD_DISABLED_VALUES
    return True


def should_fallback_to_linked_pdf() -> bool:
    value = _env("ZOTERO_LINKED_PDF_FALLBACK")
    if value:
        return value.lower() in PDF_UPLOAD_ENABLED_VALUES
    return False


def should_require_stored_pdf() -> bool:
    value = _env("ZOTERO_REQUIRE_STORED_PDF")
    if value:
        return value.lower() not in PDF_UPLOAD_DISABLED_VALUES
    return True


def should_use_local_connector() -> bool:
    mode = (_env("ZOTERO_IMPORT_MODE", "local_connector_first") or "local_connector_first").lower()
    return mode not in {"web", "web_api", "zotero_storage"}


def should_allow_web_api_import_fallback() -> bool:
    value = _env("ZOTERO_ALLOW_WEB_API_IMPORT_FALLBACK")
    return bool(value and value.lower() in PDF_UPLOAD_ENABLED_VALUES)


def _attachment_status_has_stored_pdf(status: str) -> bool:
    ok_markers = [
        "stored_pdf_attachment_created:",
        "stored_pdf_attachment_exists:",
        "pdf_file_upload_registered",
        "pdf_file_upload_exists",
    ]
    return any(marker in status for marker in ok_markers)


def zotero_data_dir() -> Path:
    explicit = _env("ZOTERO_DATA_DIR")
    if explicit:
        return Path(explicit)
    profile_data_dir = _zotero_data_dir_from_profile()
    if profile_data_dir:
        return profile_data_dir
    preferred = Path("H:/zotero")
    if preferred.exists():
        return preferred
    return Path.home() / "Zotero"


def local_collection_tree_id(collection_key: str = DEFAULT_COLLECTION_KEY) -> str:
    db_path = zotero_data_dir() / "zotero.sqlite"
    if not db_path.exists():
        raise ZoteroError(f"Zotero DB not found at {db_path}; set ZOTERO_DATA_DIR")
    uri = "file:" + str(db_path) + "?mode=ro&immutable=1"
    conn: sqlite3.Connection | None = None
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=10)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT collectionID FROM collections WHERE key = ?", (collection_key,)).fetchone()
    finally:
        if conn is not None:
            conn.close()
    if row is None:
        raise ZoteroError(f"cannot map Zotero collection key {collection_key} to local collectionID")
    return f"C{int(row['collectionID'])}"


def connector_preflight(collection_key: str = DEFAULT_COLLECTION_KEY) -> dict[str, Any]:
    result: dict[str, Any] = {
        "connector_api": LOCAL_CONNECTOR_API,
        "reachable": False,
        "files_editable": False,
        "target": "",
        "collection_tree_id": "",
        "errors": [],
    }
    try:
        status, _ = _get_connector("/connector/ping", timeout=10)
        result["reachable"] = status == 200
    except Exception as exc:
        result["errors"].append(f"connector_ping_failed:{type(exc).__name__}:{str(exc)[:160]}")
        return result
    try:
        status, data, _ = _post_connector_json("/connector/getSelectedCollection", {}, timeout=10)
        if status == 200 and isinstance(data, dict):
            result["files_editable"] = bool(data.get("filesEditable"))
            result["target"] = str(data.get("id") or "")
    except Exception as exc:
        result["errors"].append(f"connector_collection_probe_failed:{type(exc).__name__}:{str(exc)[:160]}")
    try:
        result["collection_tree_id"] = local_collection_tree_id(collection_key)
    except Exception as exc:
        result["errors"].append(f"local_collection_tree_id_failed:{type(exc).__name__}:{str(exc)[:160]}")
    return result


def wait_for_existing_paper(paper: ArxivPaper, collection_key: str = DEFAULT_COLLECTION_KEY, timeout_seconds: int = 90) -> ImportResult | None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            existing = find_existing_paper(paper, collection_key)
        except Exception:
            existing = None
        if existing:
            return existing
        time.sleep(3)
    return None


def create_item_local_connector(ranked: RankedPaper, collection_key: str = DEFAULT_COLLECTION_KEY) -> ImportResult:
    pf = connector_preflight(collection_key)
    if not pf.get("reachable"):
        raise ZoteroError("; ".join(pf.get("errors") or ["Zotero local connector is not reachable"]))
    if not pf.get("files_editable"):
        raise ZoteroError("Zotero selected library does not allow file attachments")
    target = str(pf.get("collection_tree_id") or "")
    if not target:
        raise ZoteroError("; ".join(pf.get("errors") or ["cannot resolve Zotero collection target"]))

    paper = ranked.paper
    connector_id = "daily-arxiv-" + re.sub(r"[^A-Za-z0-9_.-]+", "-", paper.arxiv_id or uuid.uuid4().hex)
    session_id = f"{connector_id}-{uuid.uuid4().hex[:12]}"
    uri = paper.url or paper.pdf_url or (f"https://arxiv.org/abs/{paper.arxiv_id}" if paper.arxiv_id else "")
    pdf_url = paper.pdf_url or (f"https://arxiv.org/pdf/{paper.arxiv_id}" if paper.arxiv_id else "")
    item = zotero_connector_item_from_ranked(ranked, connector_id)
    try:
        status, _, _ = _post_connector_json(
            "/connector/saveItems",
            {"sessionID": session_id, "uri": uri, "items": [item]},
            timeout=60,
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ZoteroError(f"Zotero local connector saveItems failed HTTP {exc.code}: {detail[:300]}") from exc
    if status != 201:
        raise ZoteroError(f"Zotero local connector saveItems returned status {status}")

    try:
        status, data, _ = _post_connector_json("/connector/updateSession", {"sessionID": session_id, "target": target}, timeout=30)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ZoteroError(f"Zotero local connector updateSession failed HTTP {exc.code}: {detail[:300]}") from exc
    if status != 200:
        raise ZoteroError(f"Zotero local connector updateSession returned status {status}: {data}")

    if not pdf_url:
        existing = wait_for_existing_paper(paper, collection_key, timeout_seconds=90)
        key = existing.zotero_key if existing else ""
        return ImportResult(
            status="pdf_pending",
            zotero_key=key,
            message="created via Zotero local connector; stored_pdf_required_failed:no_pdf_url",
            mode="local_connector",
        )
    try:
        pdf_bytes = read_pdf_bytes_from_cache_or_download(ranked)
    except Exception as exc:
        existing = wait_for_existing_paper(paper, collection_key, timeout_seconds=90)
        key = existing.zotero_key if existing else ""
        return ImportResult(
            status="pdf_pending",
            zotero_key=key,
            message=f"created via Zotero local connector; stored_pdf_required_failed:download:{type(exc).__name__}:{str(exc)[:180]}",
            mode="local_connector",
        )

    try:
        attachment_title = f"PDF - {paper.title[:180]}"
        metadata = {
            "sessionID": session_id,
            "parentItemID": connector_id,
            "title": attachment_title,
            "url": pdf_url,
        }
        attachment_status, _ = _post_connector_bytes(
            f"/connector/saveAttachment?sessionID={urllib.parse.quote(session_id)}",
            pdf_bytes,
            metadata,
            timeout=240,
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        existing = wait_for_existing_paper(paper, collection_key, timeout_seconds=30)
        key = existing.zotero_key if existing else ""
        return ImportResult(
            status="pdf_pending",
            zotero_key=key,
            message=f"created via Zotero local connector; stored_pdf_required_failed:saveAttachment_HTTP_{exc.code}:{detail[:180]}",
            mode="local_connector",
        )
    except Exception as exc:
        existing = wait_for_existing_paper(paper, collection_key, timeout_seconds=30)
        key = existing.zotero_key if existing else ""
        return ImportResult(
            status="pdf_pending",
            zotero_key=key,
            message=f"created via Zotero local connector; stored_pdf_required_failed:{type(exc).__name__}:{str(exc)[:180]}",
            mode="local_connector",
        )
    if attachment_status != 201:
        existing = wait_for_existing_paper(paper, collection_key, timeout_seconds=30)
        key = existing.zotero_key if existing else ""
        return ImportResult(
            status="pdf_pending",
            zotero_key=key,
            message=f"created via Zotero local connector; stored_pdf_required_failed:saveAttachment_status_{attachment_status}",
            mode="local_connector",
        )

    existing = wait_for_existing_paper(paper, collection_key, timeout_seconds=90)
    if not existing:
        return ImportResult(
            status="sync_pending",
            message="created via Zotero local connector; stored_pdf_attachment_created; local Zotero item key not observed yet",
            mode="local_connector",
        )
    stored_attachment_key = wait_for_stored_pdf_attachment_local(existing.zotero_key, timeout_seconds=90)
    if not stored_attachment_key:
        return ImportResult(
            status="pdf_pending",
            zotero_key=existing.zotero_key,
            message="created via Zotero local connector; stored_pdf_required_failed:attachment_not_observed",
            mode="local_connector",
        )
    return ImportResult(
        status="created",
        zotero_key=existing.zotero_key,
        message=(
            "created via Zotero local connector; "
            f"stored_pdf_attachment_created:{stored_attachment_key}; "
            "pdf_sync=stored_attachment_webdav_managed"
        ),
        mode="local_connector",
    )


def create_item_web(ranked: RankedPaper, collection_key: str = DEFAULT_COLLECTION_KEY) -> ImportResult:
    api_key = _env("ZOTERO_API_KEY")
    if not api_key:
        raise ZoteroError("missing ZOTERO_API_KEY; refusing to write to Zotero")
    user_id = _web_user_id(collection_key)
    if not user_id:
        raise ZoteroError("cannot determine Zotero user id; set ZOTERO_USER_ID")
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items"
    headers = _web_headers(api_key)
    try:
        response = _post_json(url, [zotero_item_from_ranked(ranked, collection_key)], headers=headers, timeout=30)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ZoteroError(f"Zotero write failed HTTP {exc.code}: {detail[:500]}") from exc
    successful = response.get("successful", {})
    if "0" in successful:
        created = successful["0"]
        key = created.get("key") or created.get("data", {}).get("key", "")
        attachment_status = create_pdf_attachment_web(
            ranked,
            key,
            user_id=user_id,
            api_key=api_key,
            upload_file=should_upload_pdf_files(),
            linked_fallback=should_fallback_to_linked_pdf(),
        )
        message = "created via Zotero Web API"
        if attachment_status:
            message += f"; {attachment_status}"
        status_value = "created"
        if should_require_stored_pdf() and not _attachment_status_has_stored_pdf(attachment_status):
            status_value = "pdf_pending"
            message += "; stored_pdf_required_failed:web_api_did_not_create_syncable_pdf"
        return ImportResult(status=status_value, zotero_key=key, message=message, mode="web_api")
    unchanged = response.get("unchanged", {})
    if "0" in unchanged:
        item = unchanged["0"]
        key = item.get("key") or item.get("data", {}).get("key", "")
        return ImportResult(status="exists", zotero_key=key, message="unchanged in Zotero Web API", mode="web_api", existing=True)
    failed = response.get("failed", {})
    raise ZoteroError("Zotero write returned no successful item: " + json.dumps(failed, ensure_ascii=False)[:500])


def create_pdf_attachment_web(
    ranked: RankedPaper,
    parent_key: str,
    *,
    user_id: str,
    api_key: str,
    upload_file: bool = False,
    linked_fallback: bool = True,
) -> str:
    attachment = zotero_pdf_attachment_from_ranked(ranked, parent_key, file_backed=upload_file)
    if not attachment:
        return "pdf_attachment_skipped:no_pdf_url"
    url = f"{WEB_API}/users/{urllib.parse.quote(user_id)}/items"
    headers = _web_headers(api_key)
    errors: list[str] = []
    for attempt in range(1, 4):
        try:
            existing_key = (
                find_file_pdf_attachment_web(parent_key, user_id=user_id, api_key=api_key)
                if upload_file
                else find_pdf_attachment_web(parent_key, user_id=user_id, api_key=api_key)
            )
            if existing_key:
                return f"pdf_attachment_exists:{existing_key}"
        except Exception as exc:
            errors.append(f"precheck{attempt}:{type(exc).__name__}:{str(exc)[:80]}")
        try:
            response = _post_json(url, [attachment], headers, timeout=30)
            break
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if not _is_transient_http_status(exc.code) or attempt >= 3:
                suffix = f"; retry_errors={' | '.join(errors)}" if errors else ""
                return f"pdf_attachment_failed:HTTP_{exc.code}:{detail[:160]}{suffix}"
            errors.append(f"attempt{attempt}:HTTP_{exc.code}:{detail[:80]}")
            time.sleep(_retry_delay_seconds(attempt, exc))
        except Exception as exc:
            if not _is_transient_network_error(exc) or attempt >= 3:
                suffix = f"; retry_errors={' | '.join(errors)}" if errors else ""
                return f"pdf_attachment_failed:{type(exc).__name__}:{str(exc)[:160]}{suffix}"
            errors.append(f"attempt{attempt}:{type(exc).__name__}:{str(exc)[:80]}")
            time.sleep(_retry_delay_seconds(attempt, exc))
    else:
        return "pdf_attachment_failed:retry_exhausted:" + " | ".join(errors)[:160]
    successful = response.get("successful", {})
    if "0" in successful:
        key = successful["0"].get("key") or successful["0"].get("data", {}).get("key", "")
        if not upload_file:
            suffix = f"; attachment_retry_recovered_after={len(errors)}" if errors else ""
            return f"pdf_attachment_created:{key}; pdf_file_upload_skipped:disabled{suffix}"
        upload_status = upload_pdf_file_web(ranked, key, user_id=user_id, api_key=api_key)
        suffix = f"; attachment_retry_recovered_after={len(errors)}" if errors else ""
        if upload_status.startswith("pdf_file_upload_failed"):
            cleanup_status = delete_item_web(key, user_id=user_id, api_key=api_key)
            if linked_fallback:
                try:
                    local_pdf_path = download_pdf_to_local_cache(ranked)
                except Exception as exc:
                    return (
                        f"pdf_attachment_upload_failed:{key}; {upload_status}; {cleanup_status}; "
                        f"linked_pdf_fallback_failed:download:{type(exc).__name__}:{str(exc)[:120]}{suffix}"
                    )
                linked_status = create_linked_pdf_attachment_web(
                    ranked,
                    parent_key,
                    str(local_pdf_path),
                    user_id=user_id,
                    api_key=api_key,
                )
                return (
                    f"pdf_attachment_upload_failed:{key}; {upload_status}; {cleanup_status}; "
                    f"linked_pdf_fallback:{linked_status}; local_pdf_path={local_pdf_path}; "
                    f"webdav_sync_note=linked_file_not_synced_by_webdav{suffix}"
                )
            return f"pdf_attachment_upload_failed:{key}; {upload_status}; {cleanup_status}{suffix}"
        return f"pdf_attachment_created:{key}; {upload_status}{suffix}"
    unchanged = response.get("unchanged", {})
    if "0" in unchanged:
        key = unchanged["0"].get("key") or unchanged["0"].get("data", {}).get("key", "")
        return f"pdf_attachment_exists:{key}"
    failed = response.get("failed", {})
    return "pdf_attachment_failed:" + json.dumps(failed, ensure_ascii=False)[:160]


def wait_for_local_item(zotero_key: str, timeout_seconds: int = 300) -> bool:
    if not zotero_key:
        return False
    deadline = time.time() + timeout_seconds
    url = f"{LOCAL_API}/items/{urllib.parse.quote(zotero_key)}?format=json"
    while time.time() < deadline:
        try:
            _read_json(url, timeout=10)
            return True
        except Exception:
            time.sleep(5)
    return False


def import_ranked_paper(
    ranked: RankedPaper,
    *,
    collection_key: str = DEFAULT_COLLECTION_KEY,
    dry_run: bool = False,
    poll_local: bool = True,
    local_sync_timeout: int = 300,
) -> ImportResult:
    collection_key = require_collection_key(collection_key)
    existing = find_existing_paper(ranked.paper, collection_key)
    if existing:
        if should_require_stored_pdf() and existing.zotero_key:
            try:
                stored_key = find_stored_pdf_attachment_local(existing.zotero_key)
            except Exception:
                stored_key = ""
            if stored_key:
                existing.message += f"; stored_pdf_attachment_exists:{stored_key}"
            else:
                existing.message += "; stored_pdf_missing_existing"
        return existing
    if dry_run:
        mode = "local_connector" if should_use_local_connector() else "web_api"
        return ImportResult(status="dry_run", message=f"would create Zotero item with syncable PDF via {mode}", mode=mode)
    if should_use_local_connector():
        try:
            created = create_item_local_connector(ranked, collection_key)
        except Exception:
            if not should_allow_web_api_import_fallback():
                raise
            created = create_item_web(ranked, collection_key)
    else:
        created = create_item_web(ranked, collection_key)
    if (
        poll_local
        and created.status == "created"
        and created.zotero_key
        and not wait_for_local_item(created.zotero_key, timeout_seconds=local_sync_timeout)
    ):
        created.message += "; local Zotero sync not observed yet"
        created.status = "sync_pending"
    return created


def preflight(collection_key: str = DEFAULT_COLLECTION_KEY) -> dict[str, Any]:
    result: dict[str, Any] = {
        "collection_key": collection_key,
        "local_read": False,
        "write_credentials": False,
        "web_api_credentials": False,
        "pdf_file_upload_enabled": False,
        "stored_pdf_required": should_require_stored_pdf(),
        "local_connector": {},
        "pdf_sync_ready": False,
        "errors": [],
    }
    if not collection_key.strip():
        result["errors"].append("missing_collection_key")
        return result
    try:
        collection = read_collection(collection_key)
        result["local_read"] = True
        result["library_id"] = collection.get("library", {}).get("id")
        result["collection_name"] = collection.get("data", {}).get("name")
        result["item_count"] = len(iter_local_items(collection_key))
    except Exception as exc:
        result["errors"].append(f"local_read_failed:{exc}")
    connector = connector_preflight(collection_key)
    result["local_connector"] = connector
    local_connector_ready = bool(connector.get("reachable") and connector.get("files_editable") and connector.get("collection_tree_id"))
    result["web_api_credentials"] = bool(_env("ZOTERO_API_KEY"))
    result["write_credentials"] = bool(result["web_api_credentials"] or local_connector_ready)
    result["pdf_file_upload_enabled"] = should_upload_pdf_files()
    result["pdf_sync_ready"] = bool(local_connector_ready or (not should_require_stored_pdf()))
    if should_require_stored_pdf() and not local_connector_ready:
        result["write_credentials"] = False
        result["errors"].append("local_connector_not_ready_for_stored_pdf")
        result["errors"].extend(connector.get("errors") or [])
    elif not result["write_credentials"]:
        result["errors"].append("missing_ZOTERO_API_KEY_or_local_connector")
    if not should_use_local_connector() and not (_env("ZOTERO_USER_ID") or _env("ZOTERO_LIBRARY_ID")) and not result.get("library_id"):
        result["errors"].append("missing_ZOTERO_USER_ID")
    return result


def _redact_preflight(result: dict[str, Any]) -> dict[str, Any]:
    collection_key = str(result.get("collection_key") or "")

    def redact_text(value: Any) -> Any:
        if not isinstance(value, str):
            return value
        if collection_key:
            value = value.replace(collection_key, "<collection_key>")
        return value

    redacted = dict(result)
    if collection_key:
        redacted["collection_key"] = "<configured>"
    for key in ("library_id", "collection_name"):
        if key in redacted and redacted[key]:
            redacted[key] = "<redacted>"
    redacted["errors"] = [redact_text(error) for error in result.get("errors", [])]
    connector = dict(result.get("local_connector") or {})
    if connector.get("collection_tree_id"):
        connector["collection_tree_id"] = "<redacted>"
    if connector.get("errors"):
        connector["errors"] = [redact_text(error) for error in connector.get("errors", [])]
    redacted["local_connector"] = connector
    return redacted


def _load_ranked(path: str) -> RankedPaper:
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    return RankedPaper.from_dict(json.loads(text))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", action="store_true", help="Check local Zotero read and write credentials.")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION_KEY)
    parser.add_argument("--paper-json", help="JSON file containing one RankedPaper record, or '-' for stdin.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--unsafe-json", action="store_true", help="Print raw local Zotero metadata. Do not paste this output publicly.")
    args = parser.parse_args()

    if args.preflight:
        result = preflight(args.collection)
        if args.json or args.unsafe_json:
            output = result if args.unsafe_json else _redact_preflight(result)
            safe_print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            safe_print("PASS local Zotero read" if result["local_read"] else "FAIL local Zotero read")
            safe_print("PASS Zotero write credentials" if result["write_credentials"] else "FAIL missing ZOTERO_API_KEY")
            for error in result["errors"]:
                safe_print(f"ERROR: {error}")
        return 0 if result["local_read"] and result["write_credentials"] else 1

    if not args.paper_json:
        parser.error("--paper-json is required unless --preflight is used")
    try:
        result = import_ranked_paper(_load_ranked(args.paper_json), collection_key=args.collection, dry_run=args.dry_run)
    except Exception as exc:
        result = ImportResult(status="failed", message=str(exc), mode="web_api")
    if args.json:
        safe_print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        safe_print(f"{result.status} zotero_key={result.zotero_key} mode={result.mode} {result.message}")
    return 0 if result.status in {"exists", "created", "dry_run"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
