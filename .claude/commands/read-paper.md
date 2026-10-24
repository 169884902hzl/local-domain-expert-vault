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
  `pdf_verified`, `table_verified`, `figure_verified`, `appendix_verified`, `result_row_unconfirmed`, `figure_approximation`, `note_derived`, `abstract_only`, `not_evidenced`
- Allowed `anchor_type`:
  `section`, `table`, `figure`, `appendix`, `result_row`, `snippet`, `abstract`, `note_only`
- Required coverage:
  at least one row for `problem`, `contribution` or `method`, `experiment` or `result` (or explicit `not_evidenced`), `limitation`, and `baseline` (or explicit `not_evidenced`).
- Baseline coverage is machine-checked by the `claim_type` cell. At least one Evidence Ledger row must use `claim_type` exactly `baseline` or `strongest_baseline`; mentioning baselines inside a `result` or `experiment` row is not enough.
- Exact paper numbers require page/section/table/figure/result_row anchors. Prefer table/result_row anchors for numeric result claims when the paper provides them.
- Every sentence or bullet outside the Evidence Ledger that contains a numeric result, percentage, score, baseline comparison, metric, ablation value, dataset count, frame count, or error value must cite an existing Evidence Ledger claim_id in the same sentence, for example `[C7]` or `(C7)`. Do not write bare phrases such as `见C7`; use bracketed or parenthesized claim IDs.
- Key claims in Problem, Contributions, Method, Experiments, Limitations, Baseline, and Transfer must not use `abstract` as a strong anchor. Use a concrete section/table/figure/appendix/snippet/result_row anchor, or downgrade to `abstract_only` with `screening_only`.
- If a value is visually estimated from a figure, use `evidence_class: figure_approximation`, `anchor_type: figure`, a concrete figure/page anchor, and `downstream_use: requires_human_check`; never present it as exact.
- If a machine-extracted row is not manually confirmed, use `evidence_class: result_row_unconfirmed`, `anchor_type: result_row`, and `downstream_use: requires_human_check`.
- For `pdf_verified`, `table_verified`, `figure_verified`, `appendix_verified`, `result_row_unconfirmed`, and `figure_approximation`, `anchor` must be non-empty and concrete.
- For `note_derived`, `abstract_only`, `not_evidenced`, and `figure_approximation`, `downstream_use` must be `screening_only` or `requires_human_check`; never treat these as strong evidence.
- `result_row_unconfirmed` must use `anchor_type: result_row` and `downstream_use: requires_human_check`.

Strict Idea Fuel contract:
- `Idea Fuel` is mandatory adversarial review pressure, not a loose inspiration list and not confirmed evidence.
- Use packets `IF-1`, `IF-2`, and `IF-3` when the paper has enough material; at minimum `IF-1` must exist.
- Each packet must include all fields:
  Hypothesis / research opening; Evidence anchor; Evidence class; Engineering pathology; Hidden assumption; Fragile interface; Failure mode; Strongest baseline; Why this baseline is strongest; Paper win condition; Idea kill condition; DLO replacement baseline; Transfer distance to DLO; Why transfer may fail; Negative transfer risk; Minimum no-hardware micro-test; Downstream review target.
- Each required IF packet field must be a separate `- Field name:` bullet. Do not merge labels, such as `Paper win condition and idea kill condition`; the parser treats merged labels as missing fields.
- `Evidence anchor` must be existing Evidence Ledger `claim_id` values or exactly `not_evidenced`.
- `Strongest baseline` must name a concrete comparator or a concrete missing comparator; do not write only `not_evidenced`. If the paper does not report the comparator, write the comparator that would be needed and state that it is missing.
- `Downstream review target` must state what DeepSeek should attack and what Codex should verify.
- Treat all Idea Fuel packets as `screening_only=true` and `requires_human_check=true`; never use them as accepted paper evidence.

No-hardware Micro-test hard rule:
- Must explicitly state: no robot, no real scene, no new data collection.
- Must not require robot arm, gripper, cabinet, rope/cable hardware, tactile sensor, depth camera, motion capture, physical reset, teleoperation, human data collection, new video capture, real-world deployment, real cabinet/rope/cloth evaluation, or any physical hardware.
- Inside micro-test field values, avoid the English word `hardware`; use `reported platform specification`, `runtime setting`, or `measurement setup` instead when auditing paper-reported compute or latency details.
- Do not write non-negated phrases such as `independent of new data collection`; write `independent of newly collected data` instead.
- Allowed tests only:
  paper tables/figures/results; public code/repo cited by paper; public dataset/simulator already used by paper; existing videos/images from paper/public dataset; synthetic toy arrays/graphs/trajectories; static metric calculation; pseudo-code or logic check.
- Must include: artifact, input, deterministic 3-6 step protocol, metric, threshold, pass condition, fail/kill condition, compute/data cap, and no-hardware confirmation.

Cross-domain Transfer Risk audit:
- Mandatory when source domain is not DLO/robot manipulation and any downstream relevance to DLO is claimed, or when Idea Fuel contains a Transfer Hook.
- Required fields:
  source domain; target domain; transfer distance (`none | low | medium | high | extreme`); why transfer may fail; negative transfer risk; misleading direct-copy risk; DLO replacement baseline; DLO-specific kill condition; Evidence Ledger `claim_id`.
- Explicitly state the direct-copy assumption that would be misleading, why transfer to bimanual DLO/control/Sim-to-Real may fail, and the DLO-specific baseline that would kill the idea.
- For animation/video/generation to DLO manipulation, transfer distance must be at least `high` unless physical closed-loop manipulation, contact dynamics, or DLO control is directly evaluated.

Section template to append after existing content:
```
## Evidence Metadata
- Fulltext Quality:
- Evidence Coverage:
- Confidence:
- Summary: one specific Chinese sentence; if it contains any number, percentage, table result, baseline comparison, or model score, cite the relevant Evidence Ledger claim_id in the same sentence.

## Problem

## Key Contributions

## Method

## Experiments

## Limitations

## Key Takeaways

## Evidence Ledger
Table safety rules:
- Do not put the raw `|` character inside any table cell. Replace formulas such as `A||B` with `A double-bar B` or prose.
- `evidence_class` must be exactly one allowed token, never a combined value.
- Allowed evidence_class values: `pdf_verified`, `table_verified`, `figure_verified`, `appendix_verified`, `result_row_unconfirmed`, `figure_approximation`, `note_derived`, `abstract_only`, `not_evidenced`.
- `anchor_type` must be exactly one allowed token: `section`, `table`, `figure`, `appendix`, `result_row`, `snippet`, `abstract`, `note_only`.

| claim_id | claim_type | claim | evidence_class | anchor_type | anchor | page/section/table/figure/appendix | confidence | downstream_use |
|---|---|---|---|---|---|---|---|---|
| C1 | problem | ... | pdf_verified | section | Section 1 | Section 1 | medium | screening_only |

## Idea Fuel
IF packet safety rules:
- `Evidence class` must be exactly one allowed token from the Evidence Ledger list. If evidence is mixed, choose the weakest applicable token and mention the mixed anchors in `Evidence anchor`.
- Never write combined evidence classes such as `pdf_verified + table_verified`, `pdf_verified/table_verified`, or any other combined evidence class.
- In each `Protocol`, write 3-6 numbered steps on separate lines. Do not place all steps on one semicolon-separated line.
- In no-hardware micro-test text, use the exact English confirmation `no robot; no real scene; no new data collection`; avoid Chinese hardware words such as `机器人`, `实机`, `机械臂`, `真实场景`.
- Use `no new data collection` only as an explicit negation. In `Input`, `Artifact`, or `Compute/data cap` fields, prefer `newly collected data` when describing the absence of fresh data.

### IF-1
- Hypothesis / research opening:
- Evidence anchor: C-...
- Evidence class:
- Engineering pathology:
- Hidden assumption:
- Fragile interface:
- Failure mode:
- Strongest baseline:
- Why this baseline is strongest:
- Paper win condition:
- Idea kill condition:
- DLO replacement baseline:
- Transfer distance to DLO:
- Why transfer may fail:
- Negative transfer risk:
- Minimum no-hardware micro-test:
  - Artifact:
  - Input:
  - Protocol:
    1. ...
    2. ...
    3. ...
  - Metric:
  - Threshold:
  - Pass condition:
  - Fail/kill condition:
  - Compute/data cap:
  - No-hardware confirmation: no robot; no real scene; no new data collection.
- Downstream review target: DeepSeek should attack ...; Codex should verify ...

### IF-2
- Hypothesis / research opening:
- Evidence anchor: C-... or not_evidenced
- Evidence class:
- Engineering pathology:
- Hidden assumption:
- Fragile interface:
- Failure mode:
- Strongest baseline:
- Why this baseline is strongest:
- Paper win condition:
- Idea kill condition:
- DLO replacement baseline:
- Transfer distance to DLO:
- Why transfer may fail:
- Negative transfer risk:
- Minimum no-hardware micro-test:
  - Artifact:
  - Input:
  - Protocol:
    1. ...
    2. ...
    3. ...
  - Metric:
  - Threshold:
  - Pass condition:
  - Fail/kill condition:
  - Compute/data cap:
  - No-hardware confirmation: no robot; no real scene; no new data collection.
- Downstream review target: DeepSeek should attack ...; Codex should verify ...

### IF-3
- Hypothesis / research opening:
- Evidence anchor: C-... or not_evidenced
- Evidence class:
- Engineering pathology:
- Hidden assumption:
- Fragile interface:
- Failure mode:
- Strongest baseline:
- Why this baseline is strongest:
- Paper win condition:
- Idea kill condition:
- DLO replacement baseline:
- Transfer distance to DLO:
- Why transfer may fail:
- Negative transfer risk:
- Minimum no-hardware micro-test:
  - Artifact:
  - Input:
  - Protocol:
    1. ...
    2. ...
    3. ...
  - Metric:
  - Threshold:
  - Pass condition:
  - Fail/kill condition:
  - Compute/data cap:
  - No-hardware confirmation: no robot; no real scene; no new data collection.
- Downstream review target: DeepSeek should attack ...; Codex should verify ...

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
- DLO-specific kill condition:
- Evidence anchor / claim_id:

## No-hardware Micro-test
- Explicit exclusions: no robot; no real scene; no new data collection.
- Test artifact:
- Input:
- Protocol:
  1. ...
  2. ...
  3. ...
- Metric:
- Threshold:
- Pass condition:
- Fail/kill condition:
- Compute/data cap:
- No-hardware confirmation: no robot; no real scene; no new data collection.

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
