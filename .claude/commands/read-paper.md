Deep-read a paper and update its existing stub note with strict evidence-grounded analysis.

Argument: $ARGUMENTS (a zotero_key, e.g. GQ9BVK8N)

Non-negotiable completion gates:
- Do not produce a short summary as a substitute for reading.
- Do not leave `待精读补充`, generic summaries, empty Evidence Notes, or invented evidence.
- Do not mark the note `done` by direct editing. Only `finalize_reading.py` may write the completed analysis back.
- If full text is unavailable, continue with available evidence and set Fulltext Quality to `partial` or `abstract-only`; explicitly record the gap and keep unsupported claims screening-only.
- For batch work, process one Zotero item at a time and update progress after each paper. Do not fetch multiple fulltexts in parallel.
- This workflow prepares strict reading input for downstream review. It is not active seed promotion and must not write formal seeds or active seeds.

Deterministic workflow:
1. Find the existing stub note by searching `wiki/topics/` for the zotero_key. If not found, ask user to run `/import-paper` first.
2. Use `mcp__zotero__zotero_item_fulltext` or `python .claude/scripts/read_survey.py prepare --key $ARGUMENTS` for long papers.
3. Write the completed analysis to `raw/readings/$ARGUMENTS-analysis.md`.
4. The analysis file must contain evidence-grounded sections:
   - Evidence Metadata: Fulltext Quality (`fulltext`, `abstract-only`, or `partial`), Evidence Coverage, Confidence (`high`, `medium`, `low`), and `Summary: ...` as a specific Chinese one-line summary.
   - Problem: reference Evidence Ledger `claim_id` for each key problem claim.
   - Key Contributions: numbered list; every contribution must reference Evidence Ledger `claim_id`.
   - Method: core approach, architecture, key technical details; key method claims must reference Evidence Ledger `claim_id`.
   - Experiments: datasets, main result tables, ablations; result claims must reference Evidence Ledger `claim_id`; mark missing evidence explicitly.
   - Limitations: known weaknesses; key limitation claims must reference Evidence Ledger `claim_id`.
   - Key Takeaways: insights relevant to DLO manipulation, VLM/VLA control, RL, Sim-to-Real, or bimanual manipulation.
   - Evidence Ledger: structured claim-level evidence ledger using the required columns below.
   - Idea Fuel: adversarial research-pressure packet, not inspiration.
   - Baseline Pressure: strongest baseline and kill conditions.
   - Transfer Risk: cross-domain transfer audit.
   - No-hardware Micro-test: strictly no real hardware, no real scene, no new data collection.
   - Evidence Gaps: missing anchors, unconfirmed rows, missing ablations, unavailable appendix/table/figure evidence.
   - 结构化提取: Problem, Method, Tasks, Sensors, Robot Setup, Metrics, Limitations, Evidence Notes.
   - 本地引用关系: local [[paper]] links only when supported by the text.
5. Apply the completed analysis with:
```powershell
python .claude/scripts/finalize_reading.py $ARGUMENTS --analysis raw/readings/$ARGUMENTS-analysis.md
```
6. Extract key concepts mentioned in the paper. For each concept:
   - Check if `wiki/concepts/<concept>.md` exists.
   - If not, create a concept stub with frontmatter following `schema.json` type=concept.
7. Extract researcher names (first + corresponding authors). For each:
   - Check if `wiki/entities/<researcher>.md` exists.
   - If not, create an entity stub with frontmatter following `schema.json` type=entity.
8. Run maintenance and target-note verification:
```powershell
python .claude/scripts/ensure_literature_structure.py
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
python .claude/scripts/audit_kb.py --strict-reading --zotero-key $ARGUMENTS --json
python .claude/scripts/kb_search.py "$ARGUMENTS" --limit 5
```
9. Use Chinese for all analysis content, English for technical terms.
10. Do not change `status` to `done` unless `finalize_reading.py` successfully writes the analysis.
11. If target-note audit reports any `target_note.issues`, fix the note or analysis and rerun the target audit before reporting success. Unrelated `global_warnings` are warnings, not target failure.

Strict Evidence Ledger contract:
- Required columns:
  `claim_id`, `claim_type`, `claim`, `evidence_class`, `anchor_type`, `anchor`, `page/section/table/figure/appendix`, `confidence`, `downstream_use`
- Allowed `evidence_class`:
  `pdf_verified`, `table_verified`, `figure_verified`, `appendix_verified`, `result_row_unconfirmed`, `note_derived`, `abstract_only`, `not_evidenced`
- Allowed `anchor_type`:
  `section`, `table`, `figure`, `appendix`, `result_row`, `snippet`, `abstract`, `note_only`
- Required coverage:
  at least one row for `problem`, `contribution` or `method`, `experiment` or `result` (or explicit `not_evidenced`), `limitation`, and `baseline` (or explicit `not_evidenced`).
- For `pdf_verified`, `table_verified`, `figure_verified`, `appendix_verified`, and `result_row_unconfirmed`, `anchor` must be non-empty and concrete.
- For `note_derived`, `abstract_only`, and `not_evidenced`, `downstream_use` must be `screening_only` or `requires_human_check`; never treat these as strong evidence.
- `result_row_unconfirmed` must use `anchor_type: result_row` and `downstream_use: requires_human_check`.

No-hardware Micro-test hard rule:
- Must explicitly state: no robot, no real scene, no new data collection.
- Must not require robot arm, gripper, cabinet, rope/cable hardware, tactile sensor, depth camera, motion capture, physical reset, teleoperation, human data collection, new video capture, real-world deployment, real cabinet/rope/cloth evaluation, or any physical hardware.
- Allowed tests only:
  paper tables/figures/results; public code/repo cited by paper; public dataset/simulator already used by paper; existing videos/images from paper/public dataset; synthetic toy arrays/graphs/trajectories; static metric calculation; pseudo-code or logic check.
- Must include: test artifact, protocol, metric, pass condition, and fail/kill condition.

Cross-domain Transfer Risk audit:
- Mandatory when source domain is not DLO/robot manipulation and any downstream relevance to DLO is claimed, or when Idea Fuel contains a Transfer Hook.
- Required fields:
  source domain; target domain; transfer distance (`none | low | medium | high | extreme`); why transfer may fail; negative transfer risk; misleading direct-copy risk; DLO replacement baseline; DLO-specific kill condition; Evidence Ledger `claim_id`.
- For animation/video/generation to DLO manipulation, transfer distance must be at least `high` unless physical closed-loop manipulation, contact dynamics, or DLO control is directly evaluated.

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

## Evidence Ledger
| claim_id | claim_type | claim | evidence_class | anchor_type | anchor | page/section/table/figure/appendix | confidence | downstream_use |
|---|---|---|---|---|---|---|---|---|
| C1 | problem | ... | pdf_verified | section | Section 1 | Section 1 | medium | screening_only |

## Idea Fuel
- Engineering Pathology:
- Hidden Assumption:
- Fragile Interface:
- Strongest Baseline:
- Failure-to-Opportunity:
- Transfer Hook:
- Evidence Ledger claim_ids:

## Baseline Pressure
- Strongest Baseline:
- Why strongest:
- Evidence anchor / claim_id:
- Paper win condition:
- Idea kill condition:
- DLO replacement baseline:
- No-hardware proxy baseline:
- Baseline unavailable / unverified fields:

## Transfer Risk
- Source domain:
- Target domain:
- Transfer distance:
- Why transfer may fail:
- Negative transfer risk:
- Misleading direct-copy risk:
- DLO-specific missing variable:
- DLO replacement baseline:
- Kill condition:
- Evidence anchor / claim_id:

## No-hardware Micro-test
- Explicit exclusions: no robot; no real scene; no new data collection.
- Test artifact:
- Protocol:
- Metric:
- Pass condition:
- Fail/kill condition:

## Evidence Gaps
- Missing anchors:
- Unconfirmed result rows:
- Missing ablations:
- Unavailable appendix/table/figure evidence:

## 结构化提取

## 本地引用关系
```

Final report must include:
- Zotero key and local note path
- Fulltext Quality, Evidence Coverage, Confidence
- Whether `finalize_reading.py` succeeded
- Whether target-note `audit_kb.py --strict-reading --zotero-key $ARGUMENTS --json` passed
- Any remaining evidence gaps
