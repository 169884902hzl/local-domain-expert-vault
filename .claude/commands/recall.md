Run a local active-recall session for the literature vault.

Argument: `$ARGUMENTS` is optional focus text, for example `DLO`, `diffusion policy`, `VLA`, or a recall question ID such as `R003`.

Primary source:
- Start from `output/recall-queue.md`.
- If the queue is empty or the user gives a focus, search local notes only:
  ```powershell
  python .claude/scripts/kb_search.py "$ARGUMENTS" --semantic --limit 20
  ```

Session rules:
1. Select 1-5 high-value research questions, not bare concept names.
2. Ask the user to answer from memory first when interaction is possible.
3. Then check local notes and separate:
   - Evidence: supported by local notes or source material.
   - Inference: reasoned but not directly proven.
   - Open Question: still unresolved.
4. Update the `Answer Log` in `output/recall-queue.md` when the user asks to persist the session.
5. Recommend one result per question: keep, promote to `wiki/concepts/`, promote to `wiki/topics/`, move to `projects/`, or discard.

Do not:
- Do not use web search for recall.
- Do not generate long summaries.
- Do not add more than 0-2 new questions to the queue from a daily note.
- Do not treat AI-generated recall answers as Evidence without local/source support.
