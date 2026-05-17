---
title: "Daily Provider Matrix"
tags: [research-agenda, workflow-contract, provider-matrix]
created: "2026-05-10"
updated: "2026-05-14"
type: "permanent"
status: "done"
summary: "Provider responsibilities, public-safe defaults, private high-autonomy profiles, timeouts, failure semantics, and artifact permissions for daily automation."
---

# Daily Provider Matrix

- schema_version: provider_matrix.v1
- json_contract: `projects/research-agenda/workflow-contracts/provider-matrix.json`
- boundary: provider outputs are role-scoped; no provider may auto-accept a paper claim.
- public_default_profile: conservative, explicit opt-in, no dangerous bypass.
- private_high_autonomy_profile: maintainer-only local deployment profile; not the public default.

## Deployment Profiles

| Profile | Intended User | Permission Posture | Public Default |
|---|---|---|---|
| `public_safe_profile` | Fresh clone users and public templates | Normal permissions, no dangerous bypass, explicit local configuration required | yes |
| `private_high_autonomy_profile` | Maintainer's own workstation after local risk acceptance | High-autonomy modes such as Claudian `yolo` or CLI sandbox bypass may be used locally | no |

The public repository ships the safe profile. Any `yolo`, `dangerously-bypass-approvals-and-sandbox`, or equivalent high-autonomy mode is a private deployment profile, not a recommendation for new users.

## Providers

| Provider | Role | Public Default | Private Profile | Timeout | Writes Formal Artifacts | Failure Semantics |
|---|---|---|---|---:|---|---|
| Claudian | Deep reading | normal permissions / configured model | yolo / maintainer-configured model | 2700s per paper | yes | Failed paper goes to backlog; later papers continue. |
| Gemini CLI | Divergent greenhouse ideation | OAuth or user-configured auth, `gemini-3.1-pro-preview`, fallback auto | same provider with maintainer local timeout and account settings | 1200s | no | Structured `failed:gemini...`; evidence remains valid. |
| Codex CLI | Second-pass review | sandboxed/default approvals | dangerously-bypass-approvals-and-sandbox after local risk acceptance | 7200s | no | Fallback report can be produced from packet; no deletion or promotion. |
| OpenCode DeepSeek | Mandatory adversarial model battle | `opencode run`, selector `deepseek/deepseek-v4-pro(max)`, provider id `deepseek-v4-pro(max)` | maintainer local provider profile | 1200s | no | Required for `gemini-divergent` daily idea success from 2026-05-14; failure makes agenda/daily idea status partial. |
| Local scripts | Mirror, evidence, gate, audit | deterministic | deterministic | step-specific | yes | Hard validation is explicit; sidecar context failures are WARN. |

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
