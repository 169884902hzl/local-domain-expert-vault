---
title: "Deep Reading Report Example"
tags: [example, deep-reading, local-first]
created: "2026-05-17"
updated: "2026-05-17"
type: "permanent"
status: "done"
summary: "Sanitized example showing how a paper reading is converted into local evidence."
---

# Deep Reading Report Example

This is a sanitized example of the report shape produced after a Claudian `/read-paper` workflow. It is stored under `docs/examples/` rather than `raw/readings/` so the public repository can demonstrate the workflow without publishing private fulltext extracts or local reading logs.

## Evidence Metadata

| Field | Example |
| --- | --- |
| Paper note | `wiki/topics/xu2026token.md` |
| Zotero key | `EXAMPLEKEY` |
| Status after finalize | `done` |
| Evidence boundary | Local note plus cited paper metadata; no new experimental claim is asserted by this example |
| Downstream use | KB answer, concept updates, research-agenda seed generation |

## Problem

VLA and VLM-based robot policies can produce high-level action chunks, but contact-rich manipulation still needs online feedback, task-specific grounding, and measurable recovery behavior. A deep reading report should identify the exact gap a paper addresses and the gap it leaves open for future work.

## Key Contributions

- Identifies the paper's main interface between representation, policy learning, and robot control.
- Extracts the non-obvious mechanism rather than only restating the abstract.
- Separates confirmed claims from open problems and downstream hypotheses.
- Links the paper to local concepts such as `[[RL]]`, `[[VLM]]`, `[[Sim-to-Real]]`, and task-specific manipulation pages.

## Method

The reading report records the model interface, training signal, deployment assumptions, and the part of the system that is actually changed. For a VLA/RL paper, this often means separating:

- representation token or latent state;
- actor / critic / reward signal;
- task family and embodiment assumptions;
- whether the method is offline, online, or test-time adaptation;
- what evidence would falsify the claimed benefit.

## Experiments / Results

The report should capture only what the paper actually evaluates:

- tasks and robot or simulator setting;
- baselines and ablations;
- metrics used by the authors;
- whether results cover the scenario needed by this vault's research agenda;
- missing evaluations, such as DLO manipulation, bimanual coordination, tactile feedback, or Sim-to-Real transfer.

## Limitations

- A paper may validate rigid-object or insertion tasks but not DLO manipulation.
- A reward or token interface may be task-specific and not yet proven across embodiments.
- A result can be promising locally while still needing stronger external novelty search and experimental validation.

## Local Evidence / Citation Notes

- `wiki/topics/xu2026token.md` can support a local answer about RL-token style interfaces.
- `wiki/topics/zhong2026vlaopd.md` can support a comparison with VLA post-training and bimanual execution.
- The final vault answer should cite local note paths and clearly mark unsupported extrapolations.
- Research ideas derived from this report stay in review until evidence, similar-work, experiment-plan, risk, and human approval gates pass.
