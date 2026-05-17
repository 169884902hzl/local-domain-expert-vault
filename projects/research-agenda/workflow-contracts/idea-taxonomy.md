---
title: "Idea Taxonomy"
tags: [research-agenda, idea-quality, taxonomy]
created: "2026-05-08"
updated: "2026-05-08"
type: "permanent"
status: "done"
summary: "Taxonomy for classifying raw research idea candidates before scoring or Codex review."
---

# Idea Taxonomy

Classify each raw idea before judging its score. This prevents the system from treating every candidate as a novelty claim or a model-combination claim.

## Candidate Groups

| Group | Use When | Quality Risk |
|---|---|---|
| `evidence_bound` | The idea is tightly linked to today's readings and local evidence. | Can become safe but incremental. |
| `wild_engineering` | The idea makes a larger engineering, mechanism, system, sensing, or interface leap. | Can become vague if pathology, baseline, or experiment is weak. |

## Idea Archetypes

| Archetype | Meaning | Strong Version |
|---|---|---|
| `method_improvement` | Improves an existing method or module. | Names the original method failure and changes an interface, constraint, feedback loop, sensing path, or evaluation signal. |
| `interface_invention` | Introduces a new API, control interface, sensing interface, or representation boundary. | Makes a previously hidden variable controllable or measurable. |
| `failure_model` | Models a failure before recovery or policy update. | Predicts a failure mode that baselines miss and gives a falsifiable detector. |
| `evaluation_metric` | Creates a metric or protocol that exposes hidden failure. | Changes what gets optimized or rejected, not just how results are reported. |
| `closed_loop_system` | Proposes a new robot loop. | Connects sensing, representation, action, feedback, and update in a testable loop. |
| `data_or_labeling_strategy` | Changes what data or labels are collected. | Targets a bottleneck that current data cannot expose. |
| `representation_shift` | Changes the state/action/latent representation. | Explains why the old representation collapses under a concrete pathology. |
| `control_policy_mechanism` | Changes policy mechanics or control logic. | Survives a strong policy baseline through a mechanism, not a bigger model. |
| `instrumentation_or_sensing` | Adds or reconfigures sensing/instrumentation. | Makes an engineering pathology observable or controllable. |

## Contribution Shapes

Use one of:

`architecture / algorithm / control_interface / mechanism / system / method_improvement / evaluation_protocol / benchmark / failure_model / dataset`

## Anti-Misclassification Rules

- Do not demote a method-improvement idea just because it improves an existing method.
- Do demote it if it only adds a loss, swaps a backbone, tunes a threshold, or attaches an LLM without a failure-mechanism argument.
- Do not reward evidence-bound ideas merely for citing many local notes.
- Do not punish wild engineering ideas merely for lighter evidence if they have a sharp pathology, baseline, and killer experiment.
- Do not treat local novelty pressure as confirmed duplication.
