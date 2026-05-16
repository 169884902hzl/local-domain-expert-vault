Run a local spaced-review check for the literature vault.

Argument: $ARGUMENTS (optional focus, e.g. diffusion, DLO, VLM)

Steps:
1. Search local notes with `python .claude/scripts/kb_search.py "$ARGUMENTS" --type literature --limit 20`
2. Prefer `status: done` notes; if there are none, use high-priority `stub` notes and label them as not yet deeply read.
3. Generate 5-10 recall prompts from local notes only.
4. Save durable review output to `output/recall/YYYY-MM-DD.md` if the user asks to persist it.

Do not use web search for recall.
