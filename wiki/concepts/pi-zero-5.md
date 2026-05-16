---
title: "pi-zero-point-five VLA"
tags: [concept, VLM, robot-learning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "pi-zero-point-five is treated in this vault as a VLA-style robot policy family relevant to real-time, cross-embodiment, and physical-reasoning evaluation."
---

## Definition

pi-zero-point-five VLA refers to a Physical Intelligence style Vision-Language-Action policy family discussed in relation to robot foundation models. In this vault it is used as a concept node for VLA deployment, cross-embodiment transfer, and KinDER-style physical reasoning, not as a claim that the model is automatically correct for DLO or bimanual tasks.

## Key Ideas

- A VLA policy maps visual context and language instruction into robot actions, so its deployment quality depends on the action interface and the control frequency.
- [[ma2025running]] is the strongest local evidence for pi0-level real-time deployment constraints because it focuses on running VLA inference at control-relevant speed.
- [[huang2026kinder]] connects VLA-style policies to physical-reasoning evaluation, where general semantic ability is not enough to guarantee physical feasibility.
- [[brohan2023rt2]], [[team2024octo]], and [[kim2024openvla]] are local VLA references that frame how web-scale or robot-scale pretraining transfers into action.
- For bimanual manipulation, VLA models must still solve coordination and contact grounding; [[chen2025benchmarking]] shows that generalizable dual-arm manipulation remains difficult.
- For this research agenda, pi-zero-point-five should be treated as a candidate backbone or evaluator, not as a replacement for experiment design, baselines, and pilot validation.

## Method Families

- **VLA pretraining and action decoding**: [[brohan2023rt2]], [[team2024octo]], and [[kim2024openvla]] represent the broader VLA family.
- **Real-time VLA acceleration**: [[ma2025running]] studies inference-stack changes needed to run pi0-level models online.
- **Physical-reasoning benchmark use**: [[huang2026kinder]] gives a structured way to test whether VLA behavior satisfies physical constraints.
- **Cross-embodiment adaptation**: [[collaboration2025open]] links robot foundation models to heterogeneous embodiment data.
- **Bimanual deployment checks**: [[chen2025benchmarking]] and [[fu2024mobile]] show that dual-arm systems need coordination-specific evaluation.

## Key Papers

- [[ma2025running]]
- [[huang2026kinder]]
- [[brohan2023rt2]]
- [[team2024octo]]
- [[kim2024openvla]]
- [[collaboration2025open]]
- [[chen2025benchmarking]]
- [[fu2024mobile]]

## Evidence Map

- [[ma2025running]] anchors the real-time pi0-level deployment evidence.
- [[huang2026kinder]] anchors physical-reasoning evaluation of VLA-style methods.
- [[brohan2023rt2]], [[team2024octo]], and [[kim2024openvla]] provide broader VLA context.
- [[collaboration2025open]] supports the cross-embodiment pretraining angle.
- [[chen2025benchmarking]] and [[fu2024mobile]] warn that bimanual tasks need separate coordination evidence.

## Open Problems

- How to adapt VLA action outputs to bimanual DLO tasks with tension and topology constraints.
- How to evaluate whether a VLA understands physical constraints rather than exploiting benchmark shortcuts.
- How to keep VLA inference fast enough for closed-loop tactile or force feedback.
- How to combine a VLA planner with a lower-level diffusion, MPC, or TAMP controller.
- How to determine when VLA priors help DLO manipulation versus when they introduce unsafe hallucinated actions.

## Related Concepts

- [[vision-language-model]]
- [[robot-learning]]
- [[cross-embodiment-transfer]]
- [[physical-reasoning]]
- [[bimanual-manipulation]]
- [[sim-to-real]]

## Related Papers

- [[ma2025running]]
- [[huang2026kinder]]
- [[brohan2023rt2]]
- [[team2024octo]]
- [[kim2024openvla]]
- [[collaboration2025open]]
- [[chen2025benchmarking]]
- [[fu2024mobile]]
