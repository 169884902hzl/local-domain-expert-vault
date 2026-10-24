One-click router for this literature vault: use `/expert <your request>` for import, deep reading, local Q&A, paper comparison, concept maintenance, or audit.

Argument: $ARGUMENTS (the user's natural-language request)

Purpose:
Turn a short user request into the correct high-quality workflow for this vault. Do not answer from memory first. Classify the request, run the required local tools, read the returned notes, then report with local evidence.

Examples:
- `/expert What are the latest diffusion policy works for bimanual manipulation?`
- `/expert Deep-read Zotero key ABCD1234.`
- `/expert Compare ScaleDP and 3D Diffuser Actor.`
- `/expert Audit whether the vault can answer DLO manipulation questions.`

Non-negotiable rules:
- Local evidence first. For any domain question, run `python .claude/scripts/kb_search.py "$ARGUMENTS" --semantic --limit 12` before answering.
- Cite local note paths such as `wiki/topics/...md` and `wiki/concepts/...md` in the answer.
- If `kb_search.py` returns `NO_LOCAL_MATCHES`, say the vault has no local evidence and ask before using web/arXiv/PubMed.
- Do not produce shallow summaries, generic summaries, empty Evidence Notes, or unverified numbers.
- Do not mark literature notes as `done` by direct editing. Only `finalize_reading.py` may apply a completed reading.
- Process Zotero full text one item at a time. Do not fetch multiple Zotero fulltexts in parallel.

Intent router:
1. Import or ingest request
   - Trigger words or meaning: import, ingest, add paper, new paper, Zotero key, or a Chinese request that means importing/adding a paper.
   - Confirm or infer the Zotero key from the user request.
   - Run:
```powershell
python .claude/scripts/ingest_paper.py ZOTERO_KEY --force-overwrite-stub
python .claude/scripts/fix_wikilinks.py
python .claude/scripts/backfill_concepts.py
python .claude/scripts/extract_citation_links.py
python .claude/scripts/audit_kb.py --strict-reading
```
   - Verify with `python .claude/scripts/kb_search.py "ZOTERO_KEY" --limit 5`.

2. Deep-read request
   - Trigger words or meaning: read-paper, deep read, detailed reading, or a Chinese request that means deep-reading a paper.
   - Follow `.claude/commands/read-paper.md` exactly.
   - Required output file before applying: `raw/readings/ZOTERO_KEY-analysis.md`.
   - Required apply command:
```powershell
python .claude/scripts/finalize_reading.py ZOTERO_KEY --analysis raw/readings/ZOTERO_KEY-analysis.md
```
   - Then run the maintenance and audit commands from `/read-paper`.

3. Domain question or synthesis request
   - Trigger words or meaning: progress, latest work, what papers, how, why, survey, synthesis, comparison, difference, or an equivalent Chinese domain question.
   - Run:
```powershell
python .claude/scripts/kb_search.py "$ARGUMENTS" --semantic --limit 12
```
   - Open and read the top relevant topic/concept/entity notes.
   - Answer only from local evidence unless the user explicitly permits external search.
   - Structure the answer as: direct answer, evidence table, gaps/uncertainty, next useful local action.

4. Paper comparison request
   - Trigger words or meaning: compare, difference, vs, versus, or an equivalent Chinese comparison request.
   - Use local notes only.
   - If both paper notes are identifiable, follow `/compare-papers`.
   - Compare problem, method, representation, robot/sensor setup, experiments, metrics, limitations, and when to cite each paper.

5. Concept maintenance request
   - Trigger words or meaning: concept page, graph, Related Papers, stub, complete concepts, or an equivalent Chinese concept-maintenance request.
   - Follow `/update-concepts`.
   - Concept pages must contain: Definition, Key Ideas, Method Families, Key Papers, Evidence Map, Open Problems, Related Concepts, Related Papers.
   - Finish with:
```powershell
python .claude/scripts/backfill_concepts.py
python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
```

6. System audit request
   - Trigger words or meaning: audit, test, quality, eval, expert system, or an equivalent Chinese audit/testing request.
   - Run strict audit first:
```powershell
python .claude/scripts/audit_kb.py --strict-reading --strict-concepts
```
   - Then run at least three `kb_search.py` smoke tests covering diffusion, bimanual/ACT, and VLM/DLO.
   - Report PASS/WARN/FAIL with concrete file paths and commands.

Completion report:
- State which intent route was used.
- List commands run.
- List files read or changed.
- Give PASS/WARN/FAIL status.
- If anything was not verified, label it `unverified`.
