from __future__ import annotations

from argparse import Namespace

import kb_search


def test_kb_search_returns_local_evidence_paths() -> None:
    args = Namespace(
        query="diffusion policy DLO",
        tag=[],
        must_tag=[],
        type=None,
        status=None,
        year_from=None,
        year_to=None,
        limit=5,
        json=False,
    )
    results = kb_search.search(args)
    assert results
    assert len(results) <= 5
    assert all(str(item.path.relative_to(kb_search.vault_path())).startswith("wiki") for item in results)
    assert any(str(item.path.relative_to(kb_search.vault_path())).replace("\\", "/").startswith("wiki/topics/") for item in results)
