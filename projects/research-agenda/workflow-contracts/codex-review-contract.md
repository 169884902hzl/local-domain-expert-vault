---
title: "Codex Review Contract"
tags: [research-agenda, codex, quality]
created: "2026-05-08"
updated: "2026-05-08"
type: "permanent"
status: "done"
summary: "Contract for daily Codex second-pass review of raw Gemini candidates and formal seeds."
---

# Codex Review Contract

## Purpose

Codex is the daily second-pass reviewer. It reviews raw Gemini candidates, formal seeds, local evidence briefs, and quality labels. It is not the final reviewer and cannot delete, promote, or claim novelty.

## Required Packet Contents

The daily packet must include:

- `raw_gemini_candidates`
- `today_mechanism_seed_candidates`
- `parked_or_rewrite_candidates`
- `top_tier_rubric`
- `quality_boundary`
- potential/readiness boundary (`quality_tier` is potential only; `readiness_tier` and `promotion_decision` indicate seed-readiness)
- `local_evidence_briefs`
- `formal_seed_titles`
- allowed actions and forbidden actions

## Allowed Actions

- `accept_for_user_review`
- `rewrite`
- `park`
- `reject_with_rescue`

`reject_no_trace` is only allowed in the prose report when a candidate has no mechanism, no evidence fit, and no rescue signal. It must never be the default.

## Judgment Rules

Codex must judge:

- Is the idea more than A+B?
- Does it name a real robot pathology?
- Does it change a mechanism, interface, feedback loop, constraint, evaluation signal, or system loop?
- What is the strongest baseline?
- What is the smallest killer experiment?
- Is the candidate truly seed-ready, or merely high-potential but still rewrite/park?
- Is the novelty pressure local-only and unconfirmed?
- What rescue signal should be preserved?

## Method Improvement Rule

Method-improvement ideas are not automatically incremental. A method-improvement candidate can be strong when it:

- names the original method being improved;
- explains the original method's failure mechanism;
- changes a key interface, constraint, feedback loop, representation, sensing path, or evaluation signal;
- survives a ruthless baseline;
- has a decisive pilot.

If it only swaps a module, adds a loss, or changes a parameter without failure-mechanism logic, it should be `rewrite` or `reject_with_rescue`.

## Readiness Labels

- `ready_for_user_review`: can be shown to the user as a serious candidate.
- `rewrite_for_mechanism`: useful but needs a sharper mechanism or interface.
- `park_for_weekly_followup`: promising but not current or not sufficiently grounded.
- `reject_with_rescue`: not viable as written, but contains a reusable pathology, interface, experiment, or baseline insight.

## Red Lines

- Do not review stale daily results when a newer completed run is pending.
- Do not collapse support, originality, and engineering value into one evidence-volume score.
- Do not demote a wild engineering idea only because evidence is lighter.
- Do not treat local novelty pressure as confirmed novelty or confirmed duplication.
