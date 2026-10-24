---
title: "Task and Motion Planning (TAMP)"
tags: [concept, planning, manipulation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "TAMP combines symbolic task search with continuous motion feasibility, making it useful for constraint-heavy manipulation but costly to engineer and scale."
---

## Definition

Task and Motion Planning (TAMP) combines high-level task planning with low-level motion planning. It is relevant when a robot must choose a sequence of symbolic steps while satisfying continuous kinematic, collision, contact, and geometric constraints.

## Key Ideas

- TAMP is strong when predicates, skills, samplers, and feasibility checks can be explicitly defined, but this engineering burden can dominate the method.
- [[huang2026kinder]] uses bilevel planning as a major baseline and shows that planning can perform well on some physical-reasoning tasks while scaling poorly with combinatorial constraints.
- TAMP is a natural interface between VLA intent and low-level control: language can propose goals, while planning enforces geometry and feasibility.
- For DLO manipulation, TAMP needs extra state variables for topology, tension, contact mode, and deformation; ordinary rigid-object predicates are insufficient.
- Closed-loop replanning is necessary because contact-rich tasks often deviate from the planned state during execution.
- A research idea should compare TAMP against learned policies and hybrid controllers rather than assuming explicit planning is always better.

## Method Families

- **Bilevel planning**: symbolic task search alternates with continuous motion feasibility checks, as evaluated in [[huang2026kinder]].
- **LLM/PDDL behavior planning**: [[styrud2025automatic]] connects language-model task decomposition to behavior-tree or PDDL-like execution.
- **Neural-symbolic closed-loop planning**: [[nazarczuk2025closed]] uses symbolic programs and scene graph updates during execution.
- **Hierarchical LLM planning**: [[qiu2025wildlma]] uses high-level planning over learned skills for long-horizon manipulation.
- **Constraint-aware DLO planning**: [[pallar2025optimal]] and [[li2025routing]] provide local DLO evidence where planning and learned policies must respect path/contact constraints.

## Key Papers

- [[huang2026kinder]]
- [[styrud2025automatic]]
- [[nazarczuk2025closed]]
- [[qiu2025wildlma]]
- [[pallar2025optimal]]
- [[li2025routing]]
- [[smith2024steer]]
- [[chen2025coordinated]]

## Evidence Map

- [[huang2026kinder]] is the primary local source for TAMP as a physical-reasoning baseline.
- [[styrud2025automatic]] and [[qiu2025wildlma]] support language- or hierarchy-driven planning over robot skills.
- [[nazarczuk2025closed]] supports closed-loop symbolic/scene-graph updates.
- [[pallar2025optimal]] and [[li2025routing]] connect planning constraints to DLO and path feasibility.
- [[smith2024steer]] suggests a skill-interface route where learned low-level behavior can be composed by a higher-level planner.

## Open Problems

- How to define DLO predicates that capture topology and contact without becoming too brittle.
- How to combine VLA semantic priors with TAMP feasibility checks.
- How to avoid combinatorial explosion when tasks require many contacts or objects.
- How to decide when a TAMP failure should trigger replanning, learned recovery, or human intervention.
- How to benchmark the engineering cost of building TAMP domains against learned-policy baselines.

## Related Concepts

- [[planning]]
- [[physical-reasoning]]
- [[nonprehensile-manipulation]]
- [[tool-use-manipulation]]
- [[deformable-linear-object]]
- [[vision-language-model]]

## Related Papers

- [[huang2026kinder]]
- [[styrud2025automatic]]
- [[nazarczuk2025closed]]
- [[qiu2025wildlma]]
- [[pallar2025optimal]]
- [[li2025routing]]
- [[smith2024steer]]
- [[chen2025coordinated]]
