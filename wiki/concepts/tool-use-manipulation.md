---
title: "Tool Use in Manipulation"
tags: [concept, manipulation, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Tool-use manipulation studies how robots use external objects as functional intermediates for reaching, pushing, pulling, sweeping, or transporting targets."
---

## Definition

Tool Use in Manipulation is the ability to choose, grasp, position, and use an external object as a functional intermediary. It includes canonical tools, improvised tools, and task-specific objects used for pushing, pulling, sweeping, hooking, transporting, or constraining motion.

## Key Ideas

- Tool use requires affordance reasoning: the robot must infer what an object can do, not only where it is.
- [[huang2026kinder]] treats tool use as one of the core physical-reasoning challenge families, including tasks where the tool changes reachable effects.
- Tool use often overlaps with nonprehensile manipulation because the useful action is mediated by contact rather than direct grasping.
- VLM and VLA systems can propose tool choices, but execution still needs geometry, collision, and contact feasibility checks.
- [[nazarczuk2025closed]] and [[smith2024steer]] provide local evidence that language or symbolic structure can organize tool-like actions, but they do not remove the need for low-level control.
- For DLO work, tool use may become relevant when hooks, guides, fixtures, or compliant tools help route a cable or maintain topology.

## Method Families

- **Benchmark tool-use tasks**: [[huang2026kinder]] provides structured evaluation environments for tool-mediated physical reasoning.
- **Closed-loop symbolic reasoning**: [[nazarczuk2025closed]] uses scene graphs and symbolic programs that can support tool selection and execution.
- **Dense language skill grounding**: [[smith2024steer]] exposes lower-level manipulation primitives through structured language.
- **VLA/VLM semantic transfer**: [[brohan2023rt2]] and [[kim2024openvla]] are relevant when tool semantics come from pretrained vision-language priors.
- **Long-horizon manipulation planning**: [[qiu2025wildlma]] and [[styrud2025automatic]] connect tool-like skill composition with hierarchical planning.

## Key Papers

- [[huang2026kinder]]
- [[nazarczuk2025closed]]
- [[smith2024steer]]
- [[brohan2023rt2]]
- [[kim2024openvla]]
- [[qiu2025wildlma]]
- [[styrud2025automatic]]
- [[dai2024racer]]

## Evidence Map

- [[huang2026kinder]] is the main local evidence for tool-use manipulation as a physical-reasoning category.
- [[nazarczuk2025closed]] and [[smith2024steer]] provide evidence for structured reasoning or language grounding around reusable manipulation skills.
- [[brohan2023rt2]] and [[kim2024openvla]] show why VLA priors may help with tool semantics, while still requiring physical validation.
- [[qiu2025wildlma]] and [[styrud2025automatic]] support long-horizon composition of tool-like skills.
- [[dai2024racer]] is relevant for language-guided recovery when tool-mediated manipulation fails.

## Open Problems

- How to represent tool affordances in a way that supports both language reasoning and contact planning.
- How to evaluate improvised tool use separately from memorized object categories.
- How to combine VLA tool proposals with TAMP or MPC feasibility checks.
- How to use fixtures or guide tools for DLO manipulation without making the setup too task-specific.
- How to recover when the selected tool slips, jams, or violates the intended contact mode.

## Related Concepts

- [[physical-reasoning]]
- [[nonprehensile-manipulation]]
- [[task-and-motion-planning]]
- [[vision-language-model]]
- [[robotic-manipulation]]
- [[deformable-linear-object]]

## Related Papers

- [[huang2026kinder]]
- [[nazarczuk2025closed]]
- [[smith2024steer]]
- [[brohan2023rt2]]
- [[kim2024openvla]]
- [[qiu2025wildlma]]
- [[styrud2025automatic]]
- [[dai2024racer]]
