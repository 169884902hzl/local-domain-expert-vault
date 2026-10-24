---
title: "Physical Reasoning"
tags: [concept, planning, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Physical reasoning is the ability to choose actions that respect kinematic, dynamic, contact, and embodiment constraints in the physical world."
---

## Definition

Physical Reasoning in robotics means reasoning about how robot embodiment, objects, contacts, and dynamics constrain feasible action. It is broader than visual recognition or language reasoning: the output must work under continuous geometry, force, contact, and timing constraints.

## Key Ideas

- [[huang2026kinder]] defines physical reasoning around five challenge families: spatial relations, nonprehensile manipulation, tool use, combinatorial geometry, and dynamic constraints.
- Physical reasoning must be disentangled from perception and language if we want to know whether a method truly understands physical constraints.
- Planning methods can perform well when symbolic skills and samplers are available, but their engineering cost and scaling behavior remain open issues.
- Learning methods such as RL, IL, diffusion policy, and VLA can generalize in some settings but still fail under long-horizon or out-of-distribution physical constraints.
- Closed-loop systems such as [[nazarczuk2025closed]] are important because physical reasoning errors often appear during execution, not only at planning time.
- For bimanual DLO work, physical reasoning should include tension, topology, contact location, and recovery triggers rather than only object pose.

## Method Families

- **Benchmark isolation**: [[huang2026kinder]] uses procedurally generated tasks to isolate physical-reasoning challenges.
- **Task and motion planning**: TAMP-style approaches explicitly model skills, predicates, samplers, and motion feasibility.
- **Neural-symbolic closed-loop reasoning**: [[nazarczuk2025closed]] links language, scene graph state, symbolic programs, and action planning.
- **VLA or VLM-guided manipulation**: [[brohan2023rt2]], [[kim2024openvla]], and [[smith2024steer]] connect high-level semantic priors to robot actions.
- **Long-horizon embodied planning**: [[qiu2025wildlma]] demonstrates hierarchical planning and learned skills in field-like settings.
- **Runtime-constrained VLA control**: [[ma2025running]] shows that real-time deployment is part of physical reasoning, not a separate implementation detail.

## Key Papers

- [[huang2026kinder]]
- [[nazarczuk2025closed]]
- [[brohan2023rt2]]
- [[kim2024openvla]]
- [[smith2024steer]]
- [[qiu2025wildlma]]
- [[ma2025running]]
- [[chen2025benchmarking]]

## Evidence Map

- [[huang2026kinder]] is the primary local source for the definition, task taxonomy, and baseline comparison.
- [[nazarczuk2025closed]] supports the need for closed-loop interactive reasoning when observations and physical properties must be updated.
- [[brohan2023rt2]], [[kim2024openvla]], and [[smith2024steer]] provide VLA/VLM evidence, but also motivate checking whether semantic priors translate into physical feasibility.
- [[qiu2025wildlma]] connects physical reasoning to long-horizon skill execution outside simple tabletop settings.
- [[ma2025running]] supplies deployment evidence that latency and frequency constraints affect whether physical reasoning can be used online.

## Open Problems

- How to evaluate physical reasoning independently from perception and language ability.
- How to combine symbolic constraints with learned policies without hand-engineering every skill.
- How to represent DLO-specific physical constraints such as topology, tension, and self-contact.
- How to detect physical reasoning failure early enough for recovery.
- How to make benchmark insights transfer to real bimanual hardware and tactile sensing.

## Related Concepts

- [[robotic-manipulation]]
- [[vision-language-model]]
- [[grasping]]
- [[deformable-linear-object]]
## Related Papers

- [[yokomizo2026physquantagent]]