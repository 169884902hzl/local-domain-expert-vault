Ask a domain question using local vault evidence first.

Argument: $ARGUMENTS (natural-language question)

Use this command when the user wants an answer, synthesis, comparison, trend summary, or research direction from the local literature knowledge base.

Required workflow:
1. Run local search before answering:
```powershell
python .claude/scripts/kb_search.py "$ARGUMENTS" --semantic --limit 12
```
2. Open and read the most relevant returned notes. Use topic notes first, then concept pages, then entity pages.
3. Answer only from local evidence unless the user explicitly approves external search.
4. Cite local paths in the answer, for example `wiki/topics/zhu2024scaling.md`.
5. If the result is `NO_LOCAL_MATCHES`, say the vault has no local evidence and ask whether to search externally.

Answer format:
- Direct answer in 3-8 bullets.
- Evidence table with local path, paper/concept, and why it matters.
- Gaps or uncertainty.
- Suggested next local action, if useful.

Do not:
- Do not answer from general model memory before search.
- Do not cite external papers that are not in the vault unless external search was approved.
- Do not hide weak evidence; label it clearly.
