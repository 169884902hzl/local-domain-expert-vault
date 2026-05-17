Deep-read a paper and update its existing stub note with full analysis.

Argument: $ARGUMENTS (a zotero_key, e.g. GQ9BVK8N)

Non-negotiable completion gates:
- Do not produce a short summary as a substitute for reading.
- Do not leave `待精读补充`, generic summaries, empty Evidence Notes, or invented evidence.
- Do not mark the note `done` by direct editing. Only `finalize_reading.py` may write the completed analysis back.
- If full text is unavailable, continue with available evidence and set Fulltext Quality to `partial` or `abstract-only`; explicitly record the gap.
- For batch work, process one Zotero item at a time and update progress after each paper. Do not fetch multiple fulltexts in parallel.

Deterministic workflow:
1. Find the existing stub note by searching wiki/topics/ for the zotero_key. If not found, ask user to run `/import-paper` first.
2. Use `mcp__zotero__zotero_item_fulltext` or `python .claude/scripts/read_survey.py prepare --key $ARGUMENTS` for long papers.
3. Write the completed analysis to `raw/readings/$ARGUMENTS-analysis.md`.
4. The analysis file must contain evidence-grounded sections:
   - Evidence Metadata: Fulltext Quality (`fulltext`, `abstract-only`, or `partial`), Evidence Coverage, Confidence (`high`, `medium`, `low`)
     Also include `Summary: ...` as a specific Chinese one-line summary for frontmatter. Do not use generic summaries like “提出基于学习方法的操控方法”.
   - Problem: What problem does this paper solve?
   - Key Contributions: Numbered list of main contributions
   - Method: Core approach, architecture, key technical details
   - Experiments: Datasets, main results table, ablation studies; mark missing evidence explicitly rather than inventing
   - Limitations: Known weaknesses
   - Key Takeaways: Insights relevant to our research (DLO manipulation, VLM-based control)
   - Idea Fuel: Engineering Pathology, Hidden Assumption, Fragile Interface, Strongest Baseline, Baseline Failure/Win Condition, Failure-to-Opportunity, Transfer Hook, Minimum No-hardware Micro-test
     This section feeds downstream Gemini greenhouse, OpenCode/DeepSeek battle, and Codex review. It should extract concrete failure modes and research openings, not generic inspiration. If the paper does not support a field, write `not_evidenced`.
   - 结构化提取: Problem, Method, Tasks, Sensors, Robot Setup, Metrics, Limitations, Evidence Notes
   - 本地引用关系: local [[paper]] links only when supported by the text
5. Apply the completed analysis with:
```powershell
python .claude/scripts/finalize_reading.py $ARGUMENTS --analysis raw/readings/$ARGUMENTS-analysis.md
```
6. Extract key concepts mentioned in the paper. For each concept:
   - Check if wiki/concepts/<concept>.md exists
   - If not, create a concept stub with frontmatter following schema.json type=concept
7. Extract researcher names (first + corresponding authors). For each:
   - Check if wiki/entities/<researcher>.md exists
   - If not, create an entity stub with frontmatter following schema.json type=entity
8. Run maintenance and verification:
```powershell
python .claude/scripts/ensure_literature_structure.py
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
python .claude/scripts/audit_kb.py --strict-reading
python .claude/scripts/kb_search.py "$ARGUMENTS" --limit 5
```
9. Use Chinese for all analysis content, English for technical terms.
10. Do not change `status` to `done` unless `finalize_reading.py` successfully writes the analysis.
11. If `audit_kb.py --strict-reading` reports any issue for this note, fix the note or analysis and rerun the audit before reporting success.

Section template to append after existing content:
```
## Evidence Metadata
- Fulltext Quality:
- Evidence Coverage:
- Confidence:
- Summary:
## Problem
## Key Contributions
## Method
## Experiments
## Limitations
## Key Takeaways
## Idea Fuel
- Engineering Pathology:
- Hidden Assumption:
- Fragile Interface:
- Strongest Baseline:
- Baseline Failure/Win Condition:
- Failure-to-Opportunity:
- Transfer Hook:
- Minimum No-hardware Micro-test:
## 结构化提取
## 本地引用关系
```

Final report must include:
- Zotero key and local note path
- Fulltext Quality, Evidence Coverage, Confidence
- Whether `finalize_reading.py` succeeded
- Whether `audit_kb.py --strict-reading` passed
- Any remaining evidence gaps
