Run a weekly research synthesis for the literature vault.

Scope:
- Read the past 7 days of `daily/YYYY-MM-DD.md`.
- Read `output/recall-queue.md`.
- Use local retrieval only when needed:
  ```powershell
  python .claude/scripts/kb_search.py "$ARGUMENTS" --limit 20
  ```

Output:
- Save one synthesis page to `output/YYYY-WXX-synthesis.md` using the ISO week number.
- Use `templates/weekly-synthesis.md` as the structure.

Interaction rule:
- First select 3-5 high-value recall questions and ask the user to answer from memory.
- Do not inspect local notes before the user provides answers, unless the user explicitly requests a non-interactive synthesis.
- After the user answers, check local notes and fill Evidence / Inference / Open Question.
- If the user requests a non-interactive run, mark recall status as `not-tested` instead of `yes`, `partial`, or `no`.

Template variable handling:
- Replace `{{date:YYYY-MM-DD}}` with today's local date.
- Replace `{{date:GGGG-[W]WW}}` with the ISO week label, e.g. `2026-W22`.
- Do not leave raw `{{date:...}}` placeholders in the output file.

Required content:
1. Answer 3-5 high-value recall questions from `output/recall-queue.md` or recent daily notes.
2. Record whether each answer was `yes`, `partial`, `no`, or `not-tested`.
3. Identify 1-3 mechanisms that genuinely became clearer this week.
4. Keep Evidence / Inference / Open Question separated.
5. Recommend at most 1-3 promotions to `wiki/concepts/`, `wiki/topics/`, paper/system cards, or `projects/`.
6. Pick exactly one priority research question for next week.

Do not:
- Do not summarize every daily note.
- Do not create wiki/entity stubs automatically.
- Do not promote AI-generated text as Evidence unless it is anchored in local notes or cited source material.
- Do not use web search unless the user explicitly asks.
