---
title: "Gemini Greenhouse Contract"
tags: [research-agenda, gemini, quality]
created: "2026-05-08"
updated: "2026-05-21"
type: "permanent"
status: "done"
summary: "Contract for divergent Gemini idea generation, raw candidate preservation, taxonomy, and seed promotion boundaries."
---

# Gemini Greenhouse Contract

## Purpose

Gemini is the divergent invention layer after Claudian deep reading. Its job is to generate raw research candidates with mechanism-level imagination. It is not the final reviewer and must not write confirmed novelty claims.

## Candidate Groups

- `evidence_bound`: tighter link to the day's readings and local evidence matrix.
- `wild_engineering`: larger mechanism, interface, architecture, sensing, control, or evaluation leap. It may have lighter evidence if the pathology, baseline, and falsification are sharp.

Both groups should appear from 2026-05-08 onward unless the evidence is too narrow.

## Idea Taxonomy

Each raw candidate should be classified as one of:

- `method_improvement`
- `interface_invention`
- `failure_model`
- `evaluation_metric`
- `closed_loop_system`
- `data_or_labeling_strategy`
- `representation_shift`
- `control_policy_mechanism`
- `instrumentation_or_sensing`

This prevents valuable engineering-method improvements from being misread as trivial patches.

## Required Candidate Fields

Each raw candidate must include:

`title / candidate_group / problem / physical_failure_scene / engineering_pathology / mechanism / interface / interface_innovation / optimization_space / loss_placement / decoder_boundary / manifold_safety / hypothesis / evidence_links / speculative_jump / idea_archetype / contribution_shape / non_obvious_claim / anti_combination_test / top_tier_rationale / engineering_loop / method_improvement_claim / original_method_failure / replacement_or_coupled_technique / why_improvement_not_patch / why_now / strongest_baseline / baseline_failure_mode / killer_experiment / novelty_risk / reviewer_kill_shot / rescue_mutation / claim_compression / online_or_offline_mode / minimum_no_hardware_pilot / baseline_kill_table / what_would_make_this_not_a_paper / reviewer_pre_mortem / falsification_discriminates_mechanism / lab_fit / hardware_assumptions / negative_claim_boundary / version_evolution_story / core_insight / pipeline_steps / defense_patches / baseline_matrix / metric_suite / risk_assumptions / competition_map / two_week_sprint / promotion_reason / rescue_signal / potential_tier / readiness_tier / promotion_decision / nearest_pressure / pilot / baselines / metrics / falsification`

`quality_tier` and `potential_tier` are potential-only signals. They must not be read as seed readiness. Seed readiness is represented by `readiness_tier`, `promotion_decision`, and `greenhouse_label`.

## Final-Idea Structure Reference

HapToken-v3 style is the structural quality reference, not content to copy. A strong candidate should be able to grow into a document with:

- engineering pathology and a concrete physical failure scene;
- negative claim boundary that states what is not being claimed;
- version evolution or a failed naive alternative;
- one core insight that breaks the deadlock;
- runnable training/inference/evaluation pipeline;
- defensive implementation patches;
- baseline matrix with lower bound, strongest direct baseline, simple heuristic, ablation, and oracle/upper bound when possible;
- metric suite beyond success rate;
- falsifiable risk assumptions with failure handling;
- competition map and exact mechanism gap;
- two-week sprint with an early kill test.

## Anti-Combination Rule

Gemini must not begin from "paper A has method X, paper B has interface Y, therefore combine them." The required order is:

1. A concrete physical robot failure scene.
2. The engineering pathology exposed by that scene.
3. The computational/control interface that is missing or wrong.
4. The optimization space and loss placement.
5. Prior papers as tools, pressure, or baselines.

For RL-token ideas, the candidate must explain what information survives token compression, where the signal enters, whether it crosses the decoder/action-head boundary, and how off-manifold latent/token corrections are detected.

## Core Paper Axes

The greenhouse should treat these as first-class research axes for paper ideas, not as mandatory keywords:

- VLA / VLM / RL-token / action-interface;
- tactile / force / contact-rich manipulation;
- Sim-to-Real / robustness / failure recovery;
- DLO / bimanual manipulation.

A strong candidate should state which axis or axis intersection it uses and why. It should not force all four axes into one idea, and it should not produce generic VLA, generic tactile, generic Sim-to-Real, or generic DLO framing without a concrete interface, physical feedback path, robustness mechanism, or bimanual/DLO test.

## Lab Fit

Candidates should exploit, or explicitly reject, this lab's advantages: Franka-quality arms, bimanual manipulation, wrist camera active viewpoints, FlexiTac/tactile sensing, DLO/cable tasks, and local offline logs. Ideas that mainly require low-cost hardware pathologies, large robot fleets, unavailable sensors, or unavailable specialized infrastructure should be marked rewrite/park rather than S/A.

## Quality Bar

Gemini must reason in this order:

1. Concrete physical failure scene.
2. Real robot or engineering pathology.
3. Causal mechanism or interface innovation.
4. Optimization space, loss placement, decoder boundary, and manifold safety.
5. Strongest baseline and why it may kill the idea.
6. Falsification that separates mechanism from engineering patch.
7. Killer experiment.
8. One-sentence falsifiable claim.
9. Title.

## Promotion Boundary

- Raw candidates are preserved even when weak.
- Only S/A candidates may enter seed-candidate review or formal rehearsal; active seed records still require human governance artifacts.
- B candidates go to rewrite or park.
- C candidates keep rescue signals but are not seed candidates, formal rehearsal packets, or active seed records.
- No candidate is deleted because it is speculative; it is parked, rewritten, or rejected with rescue.

## Rescue Triggers

The generation pass should trigger rescue when:

- fewer than `min_raw_candidates` candidates are returned;
- no S/A candidate appears from 2026-05-08 onward;
- candidates collapse into generic RL Token / VLA / Sim-to-Real framing without evidence;
- candidates are only A+B combinations without a new causal interface;
- method-improvement candidates do not name the original method failure.
- candidates lack a concrete physical failure scene.
- candidates add an input/module/residual without interface innovation.
- candidates do not analyze optimization space, loss placement, decoder boundary, or manifold safety.
- falsification cannot distinguish mechanism from engineering patch.
- lab fit is missing or mismatched to available Franka/FlexiTac/wrist-camera/DLO resources.

## Output Package

Gemini greenhouse must write:

- `projects/research-agenda/divergent/YYYY-MM-DD-gemini-raw-candidates.json`
- `projects/research-agenda/divergent/YYYY-MM-DD-gemini-raw-candidates.md`

The JSON archive is the source of truth for Codex daily review and weekly top-tier review.
