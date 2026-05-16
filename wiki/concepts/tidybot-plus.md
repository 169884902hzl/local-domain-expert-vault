---
title: "TidyBot++"
tags: [concept, robot-learning, sim-to-real]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "TidyBot++ is treated as a mobile-manipulation hardware reference for KinDER-style Sim-to-Real and physical-reasoning validation."
---

## Definition

TidyBot++ is an open mobile-manipulation platform referenced in the KinDER note as the real robot used for real-to-sim-to-real validation. In this vault it is a hardware/platform concept, not a method by itself.

## Key Ideas

- [[huang2026kinder]] is the direct local source: KinDER uses TidyBot++ for real-world validation of simulation-to-real correspondence.
- The platform matters because physical reasoning must eventually be checked on real hardware rather than only in procedural simulation.
- Mobile manipulators add base motion, camera calibration, and whole-body reachability constraints that tabletop-only policies can avoid.
- [[fu2024mobile]] is not TidyBot++, but it provides local evidence that mobile bimanual systems change the data collection and deployment problem.
- [[qiu2025wildlma]] and [[nazarczuk2025closed]] broaden the context toward long-horizon mobile manipulation and closed-loop embodied reasoning.
- For DLO research, a TidyBot++-style platform is relevant only if the task benefits from mobility or whole-body manipulation; fixed dual-arm benches may be better for controlled tactile/DLO pilots.

## Method Families

- **Benchmark hardware validation**: [[huang2026kinder]] uses TidyBot++ as the real-world counterpart for selected KinDER environments.
- **Mobile bimanual teleoperation**: [[fu2024mobile]] shows a data-collection and control pattern for whole-body bimanual systems.
- **Long-horizon mobile manipulation**: [[qiu2025wildlma]] connects learned skills and planning in field-like mobile manipulation.
- **Closed-loop embodied reasoning**: [[nazarczuk2025closed]] shows how scene updates and symbolic programs can drive long-horizon manipulation.
- **Dense language skill control**: [[smith2024steer]] is relevant when the platform exposes reusable low-level skills.

## Key Papers

- [[huang2026kinder]]
- [[fu2024mobile]]
- [[qiu2025wildlma]]
- [[nazarczuk2025closed]]
- [[smith2024steer]]
- [[chen2025benchmarking]]
- [[collaboration2025open]]

## Evidence Map

- [[huang2026kinder]] is the only direct local TidyBot++ evidence and should be treated as the authoritative link.
- [[fu2024mobile]] provides a comparison point for mobile bimanual hardware and teleoperation data.
- [[qiu2025wildlma]] and [[nazarczuk2025closed]] support the broader mobile/long-horizon reasoning context.
- [[smith2024steer]] connects hardware execution to reusable skill interfaces.
- [[chen2025benchmarking]] and [[collaboration2025open]] show why platform differences matter for generalization.

## Open Problems

- How to decide whether a proposed experiment needs a mobile platform or a fixed dual-arm setup.
- How to calibrate simulation and real hardware when base pose, camera pose, and arm motion all interact.
- How to reuse TidyBot++ evidence for DLO research without overclaiming beyond the KinDER validation.
- How to log hardware assumptions clearly enough for experiment proposals and reproduction.
- How to compare mobile-manipulator results against tabletop bimanual baselines.

## Related Concepts

- [[physical-reasoning]]
- [[sim-to-real]]
- [[robot-learning]]
- [[bimanual-manipulation]]
- [[task-and-motion-planning]]
- [[robotic-manipulation]]

## Related Papers

- [[huang2026kinder]]
- [[fu2024mobile]]
- [[qiu2025wildlma]]
- [[nazarczuk2025closed]]
- [[smith2024steer]]
- [[chen2025benchmarking]]
- [[collaboration2025open]]
