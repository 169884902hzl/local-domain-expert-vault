---
title: "Nonprehensile Manipulation"
tags: [concept, manipulation, planning]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Nonprehensile manipulation moves objects through pushing, sweeping, pulling, sliding, or tool-mediated contact rather than stable grasping."
---

## Definition

Nonprehensile Manipulation is a manipulation mode where the robot controls objects without fully grasping them. It includes pushing, pulling, sweeping, scooping, sliding, toppling, and tool-mediated contact. The concept is important for DLO routing because cables and ropes often require contact guidance rather than stable pick-and-place.

## Key Ideas

- Nonprehensile actions use environmental contact and object dynamics as part of the control strategy, so they are more sensitive to friction, geometry, and timing than grasp-centric manipulation.
- [[huang2026kinder]] treats nonprehensile multi-object manipulation as one of the core physical-reasoning challenges in KinDER.
- Bimanual nonprehensile tasks require temporal coordination between arms, which links this concept to [[grotz2025twin]] and [[chen2025benchmarking]].
- For DLO, nonprehensile routing can be useful when one or both arms guide the rope or cable by pushing, sliding, or constraining contact instead of holding fixed grasp points.
- Learning-only methods need explicit failure categories because nonprehensile contact can fail by slip, jam, loss of contact, or unintended object coupling.
- TAMP, MPC, and learned dynamics can complement each other: symbolic goals specify contact intent, while low-level planners handle continuous interaction.

## Method Families

- **Benchmark-driven evaluation**: [[huang2026kinder]] isolates nonprehensile tasks to compare planning, RL, IL, and foundation-model baselines.
- **Bimanual benchmark tasks**: [[grotz2025twin]] and [[chen2025benchmarking]] include dual-arm manipulation settings where non-grasp contact and coordination matter.
- **DLO routing and deformable contact**: [[li2025routing]] connects rope routing to learned policies under friction and contact uncertainty.
- **Implicit physical modeling**: [[wang2025implicit]] provides local evidence for manipulating rigid objects through soft or deformable tools.
- **Constraint and safety planning**: [[pallar2025optimal]] is relevant when contact-rich manipulation must avoid obstacles or maintain safe paths.

## Key Papers

- [[huang2026kinder]]
- [[grotz2025twin]]
- [[chen2025benchmarking]]
- [[li2025routing]]
- [[wang2025implicit]]
- [[pallar2025optimal]]
- [[chen2025coordinated]]

## Evidence Map

- [[huang2026kinder]] gives the strongest local benchmark evidence for nonprehensile physical reasoning.
- [[grotz2025twin]] and [[chen2025benchmarking]] show that nonprehensile behavior becomes harder in bimanual settings.
- [[li2025routing]] ties the concept to DLO routing and contact/friction randomization.
- [[wang2025implicit]] extends the local evidence base toward soft-tool and indirect contact manipulation.
- [[pallar2025optimal]] connects nonprehensile or contact-rich motion to safety constraints and path feasibility.

## Open Problems

- How to model stick-slip and loss-of-contact events well enough for closed-loop DLO routing.
- How to combine nonprehensile contact planning with tactile sensing on real bimanual hardware.
- How to evaluate nonprehensile success beyond final object pose, including contact stability and recovery.
- How to transfer learned nonprehensile strategies from simulation to real cables, ropes, or soft tools.
- How to decide when a task should use grasping, nonprehensile contact, or a hybrid strategy.

## Related Concepts

- [[physical-reasoning]]
- [[task-and-motion-planning]]
- [[tool-use-manipulation]]
- [[deformable-linear-object]]
- [[bimanual-manipulation]]
- [[sim-to-real]]

## Related Papers

- [[huang2026kinder]]
- [[grotz2025twin]]
- [[chen2025benchmarking]]
- [[li2025routing]]
- [[wang2025implicit]]
- [[pallar2025optimal]]
- [[chen2025coordinated]]
