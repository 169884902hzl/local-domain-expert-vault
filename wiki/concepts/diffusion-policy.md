---
title: "Diffusion Policy"
tags: [concept, diffusion, imitation]
created: "2026-04-29"
updated: "2026-04-29"
type: "concept"
status: "done"
summary: "Diffusion Policy models robot action generation as conditional denoising, useful for multimodal manipulation but still limited by latency, OOD failure, and data quality."
---

## Definition

Diffusion Policy is a robot imitation-learning family that treats action sequence generation as a conditional denoising process. In this vault it is mainly relevant as a visuomotor policy backbone for bimanual manipulation, tactile manipulation, DLO manipulation, and preference- or uncertainty-aware policy refinement.

## Key Ideas

- The central benefit is multimodal action generation: [[chi2024diffusion]] shows that conditional diffusion can represent several plausible action trajectories without collapsing to a single averaged motion.
- Closed-loop receding-horizon execution matters because a diffusion model usually predicts an action chunk, then the controller executes only part of it before replanning.
- Diffusion Policy is not automatically robust: [[lee2025diffdagger]] treats diffusion loss itself as an uncertainty signal because OOD states can still cause silent failures.
- Scaling helps but changes the bottleneck: [[zhu2024scaling]] focuses on transformer-scale diffusion policies, while robot deployment still depends on inference latency, data quality, and sensor grounding.
- For contact-rich manipulation, the action domain can shift from pose to force or wrench; [[wu2025tacdiffusion]] and [[zhao2025polytouch]] connect diffusion policies to tactile and force-conditioned control.
- For DLO tasks, diffusion policies are promising but must be paired with shape/state representations, contact modeling, and Sim-to-Real checks, as suggested by [[li2025routing]] and [[scheikl620movement]].

## Method Families

- **Visuomotor action diffusion**: [[chi2024diffusion]] uses visual observations and robot state to denoise action chunks for closed-loop manipulation.
- **Bimanual state/action decomposition**: [[chen2025coordinated]] separates future state prediction from inverse dynamics to improve dual-arm coordination.
- **Tactile or force-domain diffusion**: [[zhao2025polytouch]], [[wu2025tacdiffusion]], and [[liu2025forcemimic]] condition policy generation on contact, force, or tactile observations.
- **Scale-oriented diffusion transformer**: [[zhu2024scaling]] studies architectural changes needed to scale diffusion policies in transformer backbones.
- **Uncertainty- and preference-aware diffusion**: [[lee2025diffdagger]] uses diffusion loss for intervention, while [[moletta2026preference]] aligns deformable-object diffusion policies with preferences.
- **DLO/deformable-object diffusion**: [[li2025routing]] and [[scheikl620movement]] adapt diffusion-style learning to rope, cable, or other deformable manipulation tasks.

## Key Papers

- [[chi2024diffusion]]
- [[chen2025coordinated]]
- [[zhu2024scaling]]
- [[lee2025diffdagger]]
- [[zhao2025polytouch]]
- [[wu2025tacdiffusion]]
- [[li2025routing]]
- [[scheikl620movement]]
- [[moletta2026preference]]

## Evidence Map

- [[chi2024diffusion]] is the baseline reference for action diffusion as a visuomotor policy.
- [[chen2025coordinated]] links diffusion modeling to bimanual coordination through future state prediction and inverse dynamics.
- [[zhao2025polytouch]], [[wu2025tacdiffusion]], and [[liu2025forcemimic]] provide local evidence that contact, tactile, and force signals can change the policy interface.
- [[lee2025diffdagger]] shows that diffusion policies still need failure detection and intervention logic under OOD states.
- [[li2025routing]] and [[scheikl620movement]] are the local bridge to DLO and deformable-object manipulation.

## Open Problems

- How to represent DLO state compactly enough for diffusion while preserving topology and contact information.
- How to run diffusion policies at real-time control frequencies without losing closed-loop responsiveness.
- How to decide when diffusion loss signals recoverable uncertainty rather than inherent task ambiguity.
- How to combine tactile/force conditioning with visual DLO state estimation in a way that transfers to real hardware.
- How to evaluate diffusion-policy ideas with baselines, ablations, and failure taxonomies rather than only aggregate success rates.

## Related Concepts

- [[imitation-learning]]
- [[diffusion-model]]
- [[bimanual-manipulation]]
- [[deformable-linear-object]]
- [[tactile-sensing]]
- [[sim-to-real]]
- [[robot-learning]]

## Related Papers

- [[chi2024diffusion]]
- [[chen2025coordinated]]
- [[zhu2024scaling]]
- [[lee2025diffdagger]]
- [[zhao2025polytouch]]
- [[wu2025tacdiffusion]]
- [[liu2025forcemimic]]
- [[li2025routing]]
- [[scheikl620movement]]
- [[moletta2026preference]]
