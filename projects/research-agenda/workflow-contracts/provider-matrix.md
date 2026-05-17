---
title: "Daily Provider Matrix"
tags: [research-agenda, workflow-contract, provider-matrix]
created: "2026-05-10"
updated: "2026-05-14"
type: "permanent"
status: "done"
summary: "Provider responsibilities, default models, timeouts, failure semantics, and artifact permissions for daily automation."
---

# Daily Provider Matrix

- schema_version: provider_matrix.v1
- json_contract: `projects/research-agenda/workflow-contracts/provider-matrix.json`
- boundary: provider outputs are role-scoped; no provider may auto-accept a paper claim.

## Providers

| Provider | Role | Default | Timeout | Writes Formal Artifacts | Failure Semantics |
|---|---|---:|---:|---|---|
| Claudian | Deep reading | yolo / configured model | 2700s per paper | yes | Failed paper goes to backlog; later papers continue. |
| Gemini CLI | Divergent greenhouse ideation | OAuth, `gemini-3.1-pro-preview`, fallback auto | 1200s | no | Structured `failed:gemini...`; evidence remains valid. |
| Codex CLI | Second-pass review | yolo-style CLI bypass | 7200s | no | Fallback report can be produced from packet; no deletion or promotion. |
| OpenCode DeepSeek | Mandatory adversarial model battle | `opencode run`, selector `deepseek/deepseek-v4-pro(max)`, provider id `deepseek-v4-pro(max)` | 1200s | no | Required for `gemini-divergent` daily idea success from 2026-05-14; failure makes agenda/daily idea status partial. |
| Local scripts | Mirror, evidence, gate, audit | deterministic | step-specific | yes | Hard validation is explicit; sidecar context failures are WARN. |

## Permission Boundaries

- Claudian may update `wiki/topics/` and reading analysis through the established read-paper workflow.
- Gemini may write greenhouse drafts only through local scripts; it does not directly mutate `idea_bank/`.
- Codex review is read-only triage over packet content.
- OpenCode DeepSeek may write debate drafts only through local scripts; it does not directly mutate `idea_bank/`, raw readings, or Zotero items.
- Local scripts may write evidence matrix, paper cards, daily deltas, concept deltas, and mechanism graph drafts.

## Review Boundaries

- `novelty_pressure` is local pressure, not confirmed novelty.
- `top1_candidate` is high priority, not confirmed top 1.
- `draft_understanding_graph` is an interpretation aid, not a formal claim.
- User remains the final reviewer for any promotion beyond seed status.
- From 2026-05-14 onward, a `gemini-divergent` daily run is not quality-clean unless the mandatory Gemini-DeepSeek battle succeeds.
