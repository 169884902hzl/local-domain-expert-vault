---
title: "Idea Quality Source Basis"
tags: [research-agenda, idea-quality, rubric]
created: "2026-05-08"
updated: "2026-05-08"
type: "permanent"
status: "done"
summary: "Basis for idea scoring dimensions, novelty-pressure boundaries, and creativity-preservation policy."
---

# Idea Quality Source Basis

## Source Map

| Rule | Basis |
|---|---|
| Separate support, originality, and engineering value. | Evidence volume can make an ordinary idea look safe; top-tier research also needs non-obvious mechanism and engineering relevance. |
| Do not auto-demote on local novelty pressure. | Local mirror, Zotero notes, and seed titles are incomplete. They indicate pressure, not confirmed duplication. |
| Require strongest baseline and killer experiment. | A credible robotics idea must be falsifiable against the method most likely to make it unnecessary. |
| Preserve raw candidates even when weak. | Creative ideas often arrive as flawed sketches. Deleting them loses the pathology, interface, or experiment that may be useful after mutation. |
| Treat method improvement as a valid contribution shape. | Engineering research often advances by changing a failure mechanism, interface, feedback loop, constraint, sensing path, or evaluation signal inside an existing method. |
| Do not promote C-tier ideas. | Weak candidates should not pollute the formal seed bank. They belong in greenhouse, rewrite, park, or rescue. |
| Require one-sentence falsifiable claim compression. | A vague combination cannot be pressure-tested; a compressed claim exposes the mechanism, measurement, and rejection condition. |

## Rubric Dimensions

- `mechanism_nonobviousness`: the candidate states why the mechanism or interface is not obvious and not just A+B.
- `engineering_pathology`: the candidate starts from a real robot failure or bottleneck.
- `baseline_killer`: the candidate names the strongest baseline and a likely failure mode.
- `originality`: the candidate has a credible contribution shape and is not only a rename of existing work.
- `experimentability`: the candidate can be upgraded, rewritten, or killed by a small pilot.
- `generalizable_contribution`: the candidate is not only a local hack; it has a reusable mechanism, protocol, interface, or system lesson.
- `evidence_fit`: the candidate is traceable to local readings without pretending the evidence proves the idea.

## Quality Tiers

- `S`: strong top-tier candidate; still needs human review and novelty search.
- `A`: plausible top-tier candidate after tightening.
- `B`: rewrite or park; may contain a strong rescue signal.
- `C`: do not promote; preserve rescue signal only.

## Honesty Boundary

The system may say:

- local evidence supports exploration;
- local novelty pressure is low, medium, or high;
- a candidate has a top-tier contribution shape;
- a pilot could falsify the idea.

The system must not say:

- novelty is confirmed;
- a paper claim is accepted;
- an experiment has succeeded;
- the user has approved the seed;
- a candidate is top-tier only because a script score is high.
