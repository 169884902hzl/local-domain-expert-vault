"""Generate high-quality research-agenda seed candidates from local evidence."""
from __future__ import annotations

import argparse
import json
import itertools
import re
import sqlite3
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from gemini_cli_adapter import run_gemini_cli
from kb_common import safe_print, safe_write, vault_path
from research_agenda_common import (
    CONCEPT_DELTA_DIR,
    DIVERGENT_DIR,
    IDEA_BANK_DIR,
    MECHANISM_GRAPH_DIR,
    REQUIRED_IDEA_FILES,
    agenda_path,
    ensure_agenda_dirs,
    load_evidence_matrix,
    note_link,
    rel,
    slugify,
    split_csv,
    today,
)


MIN_MECHANISM_SOURCES = 5
MIN_STRONG_MECHANISM_SOURCES = 2
PLACEHOLDER_TOKENS = ["todo", "tbd", "need_to_verify", "seed_pending_review", "cross-gap between"]
STRONG_CLAIM_TYPES = {"paper_summary", "problem", "limitation", "open_question", "method"}
SUPPORT_CLAIM_TYPES = {"metric", "sensor", "robot_setup", "task", "evidence_note"}
SOURCE_AVAILABILITY_PATTERNS = [
    "arxiv html",
    "abstract/html",
    "pdf 入口",
    "全文；依据",
    "fulltext",
    "full text",
    "candidate 记录",
]
QUANT_OR_MECHANISM_MARKERS = [
    "%",
    " vs ",
    "table",
    "fig.",
    "figure",
    "成功率",
    "提升",
    "actor",
    "critic",
    "token",
    "anchor",
    "ppo",
    "rl",
    "diffusion",
    "contact",
    "tactile",
    "topology",
    "constraint",
    "failure",
    "memory",
]
RESULT_MARKERS = ["%", " vs ", "table", "fig.", "figure", "成功率", "提升", "降低", "epoch", "f1", "3x"]
DIVERGENT_REQUIRED_FIELDS = [
    "title",
    "problem",
    "engineering_pathology",
    "mechanism",
    "interface",
    "hypothesis",
    "evidence_links",
    "speculative_jump",
    "nearest_pressure",
    "pilot",
    "baselines",
    "metrics",
    "falsification",
]
DIVERGENT_QUALITY_FIELDS = [
    "candidate_group",
    "origin_type",
    "research_claim_type",
    "bottleneck_type",
    "evidence_mode",
    "risk_class",
    "world_model_role",
    "portfolio_slot",
    "idea_archetype",
    "contribution_shape",
    "physical_failure_scene",
    "non_obvious_claim",
    "naive_combination_version",
    "strongest_baseline_kill_path",
    "post_kill_mutation",
    "anti_combination_test",
    "top_tier_rationale",
    "engineering_loop",
    "interface_innovation",
    "optimization_space",
    "loss_placement",
    "decoder_boundary",
    "manifold_safety",
    "method_improvement_claim",
    "original_method_failure",
    "replacement_or_coupled_technique",
    "why_improvement_not_patch",
    "why_now",
    "strongest_baseline",
    "baseline_failure_mode",
    "killer_experiment",
    "novelty_risk",
    "reviewer_kill_shot",
    "rescue_mutation",
    "claim_compression",
    "online_or_offline_mode",
    "minimum_no_hardware_pilot",
    "baseline_kill_table",
    "what_would_make_this_not_a_paper",
    "reviewer_pre_mortem",
    "falsification_discriminates_mechanism",
    "lab_fit",
    "hardware_assumptions",
    "negative_claim_boundary",
    "version_evolution_story",
    "core_insight",
    "pipeline_steps",
    "defense_patches",
    "baseline_matrix",
    "metric_suite",
    "risk_assumptions",
    "competition_map",
    "two_week_sprint",
    "promotion_reason",
    "rescue_signal",
    "sharpness_score",
    "evidence_execution_score",
    "ordinaryness_penalty",
]
QUALITY_RUBRIC_WEIGHTS = {
    "mechanism_nonobviousness": 20,
    "engineering_pathology": 18,
    "baseline_killer": 16,
    "originality": 16,
    "experimentability": 12,
    "generalizable_contribution": 12,
    "evidence_fit": 6,
}
FREE_DIVERGENCE_START_DATE = "2026-05-08"
QUALITY_PROMOTION_TIERS = {"S", "A"}
DEFAULT_MIN_RAW_CANDIDATES = 6
MIN_TOP_TIER_RAW_CANDIDATES = 1
MAX_REJECTED_DRAFT_SUMMARY = 12
WORKFLOW_CONTRACTS = {
    "daily_pipeline": "projects/research-agenda/workflow-contracts/daily-pipeline-contract.md",
    "gemini_greenhouse": "projects/research-agenda/workflow-contracts/gemini-greenhouse-contract.md",
    "codex_review": "projects/research-agenda/workflow-contracts/codex-review-contract.md",
    "weekly_top_tier": "projects/research-agenda/workflow-contracts/weekly-top-tier-contract.md",
    "failure_recovery": "projects/research-agenda/workflow-contracts/failure-recovery-contract.md",
    "idea_quality_source_basis": "projects/research-agenda/workflow-contracts/idea-quality-source-basis.md",
    "idea_taxonomy": "projects/research-agenda/workflow-contracts/idea-taxonomy.md",
    "daily_quality_checklist": "projects/research-agenda/workflow-contracts/daily-quality-checklist.md",
    "intake_and_routing": "projects/research-agenda/workflow-contracts/intake-and-routing.md",
    "daily_readable_workflow": "projects/research-agenda/workflow-contracts/daily-readable-workflow.md",
    "provider_matrix": "projects/research-agenda/workflow-contracts/provider-matrix.md",
}
DIVERGENT_STOPWORDS = {
    "about",
    "after",
    "against",
    "already",
    "before",
    "between",
    "candidate",
    "compare",
    "could",
    "driven",
    "during",
    "exactly",
    "failure",
    "from",
    "interface",
    "learning",
    "local",
    "mechanism",
    "paper",
    "policy",
    "problem",
    "research",
    "should",
    "signal",
    "state",
    "their",
    "these",
    "this",
    "through",
    "using",
    "with",
    "without",
}
QUALITY_STOPWORDS = DIVERGENT_STOPWORDS | {
    "action",
    "based",
    "candidate",
    "constraint",
    "control",
    "data",
    "different",
    "evidence",
    "experiment",
    "generated",
    "method",
    "model",
    "robot",
    "robotic",
    "robots",
    "seed",
    "system",
    "task",
}
GENERIC_COMBINATION_MARKERS = [
    "combine",
    "integrate",
    "apply ",
    "plug ",
    "replace ",
    "transfer ",
    "use an llm",
    "use a vlm",
    "add ",
    "with ",
    "framework",
]
NON_OBVIOUS_MARKERS = [
    "instead of",
    "only",
    "critic-side",
    "residual",
    "projection",
    "interface",
    "trigger",
    "counterfactual",
    "failure-conditioned",
    "high-rate",
    "1-nfe",
    "closed-loop",
    "before terminal",
]
ENGINEERING_PATHOLOGY_MARKERS = [
    "wrist",
    "camera",
    "occlusion",
    "self-occlusion",
    "latency",
    "contact",
    "calibration",
    "drift",
    "depth",
    "noise",
    "collision",
    "reset",
    "failure",
    "sim-to-real",
    "viewpoint",
    "slip",
    "force",
    "torque",
    "gripper",
    "franka",
    "flextac",
    "bimanual",
    "cable",
    "rope",
    "topology",
    "bottleneck",
]
PHYSICAL_SCENE_MARKERS = ENGINEERING_PATHOLOGY_MARKERS + [
    "milliseconds",
    "millisecond",
    "mm",
    "centimeter",
    "table",
    "peg",
    "hole",
    "handover",
    "routing",
    "wrap",
    "around",
    "near",
    "under",
]
INTERFACE_INNOVATION_MARKERS = [
    "latent-to-latent",
    "latent",
    "token",
    "decoder",
    "critic",
    "actor",
    "adapter",
    "gate",
    "projection",
    "constraint",
    "residual",
    "interface",
    "readout",
    "state",
    "risk",
]
OPTIMIZATION_SPACE_MARKERS = [
    "latent space",
    "token space",
    "action space",
    "observation space",
    "loss",
    "decoder",
    "pre-decoder",
    "post-decoder",
    "manifold",
    "regularizer",
    "constraint",
    "gradient",
    "critic",
]
BASELINE_KILLER_MARKERS = [
    "strongest",
    "baseline",
    "ablation",
    "without",
    "direct",
    "standard",
    "receding",
    "impedance",
    "reject if",
    "match",
    "beats",
]
EXPERIMENT_MARKERS = [
    "compare",
    "ablation",
    "metric",
    "rate",
    "f1",
    "success",
    "latency",
    "correlation",
    "false",
    "reject if",
    "pilot",
]
GENERALIZABLE_SHAPES = {
    "architecture",
    "algorithm",
    "control_interface",
    "mechanism",
    "system",
    "method_improvement",
    "evaluation_protocol",
    "benchmark",
    "failure_model",
    "dataset",
}
VALID_IDEA_ARCHETYPES = {
    "method_improvement",
    "interface_invention",
    "failure_model",
    "evaluation_metric",
    "closed_loop_system",
    "data_or_labeling_strategy",
    "representation_shift",
    "control_policy_mechanism",
    "instrumentation_or_sensing",
}
VALID_ORIGIN_TYPES = {
    "physical_scene",
    "engineering_bottleneck",
    "scientific_deadlock",
    "representation_mismatch",
    "objective_mismatch",
    "evaluation_blind_spot",
    "paper_assumption_contradiction",
}
VALID_RESEARCH_CLAIM_TYPES = {
    "representation",
    "interface_boundary",
    "objective_optimization",
    "data_curriculum",
    "evaluation_benchmark",
    "sensing_observability",
    "world_model_simulation",
    "embodiment_control_codesign",
    "continual_transfer",
    "safety_recovery",
}
VALID_BOTTLENECK_TYPES = {
    "partial_observability",
    "contact_topology",
    "action_multimodality",
    "distribution_shift",
    "evaluation_blindness",
    "data_sparsity_bias",
    "latency_real_time",
    "irreversibility_safety",
    "objective_mismatch",
    "system_boundary_mismatch",
}
VALID_EVIDENCE_MODES = {
    "offline_replay",
    "simulation",
    "public_dataset",
    "small_real_robot_test",
    "human_study_teleop",
    "synthetic_benchmark",
    "negative_result_diagnostic",
}
VALID_RISK_CLASSES = {"grounded", "mechanism", "breakthrough"}
VALID_WORLD_MODEL_ROLES = {
    "none",
    "counterfactual_evaluator",
    "latent_state_teacher",
    "planning_critic_or_shield",
    "data_generator_or_curriculum",
    "digital_twin_calibration_loop",
    "evaluation_surrogate",
}
NON_FAILURE_ORIGIN_TYPES = {
    "scientific_deadlock",
    "representation_mismatch",
    "objective_mismatch",
    "evaluation_blind_spot",
    "paper_assumption_contradiction",
}
SCIENTIFIC_DEADLOCK_MARKERS = [
    "assumption",
    "latent",
    "representation",
    "objective",
    "loss",
    "metric",
    "benchmark",
    "evaluation",
    "boundary",
    "distribution",
    "transfer",
    "generalization",
    "deadlock",
    "blind spot",
    "unmodeled",
]


def _taxonomy_token(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _taxonomy_or_default(value: Any, valid: set[str], default: str) -> str:
    token = _taxonomy_token(value)
    return token if token in valid else default


def _normalize_idea_archetype(axis: dict[str, Any]) -> str:
    archetype = _taxonomy_token(axis.get("idea_archetype"))
    if archetype in VALID_IDEA_ARCHETYPES:
        return archetype
    text = " ".join(
        str(axis.get(field, ""))
        for field in [
            "title",
            "mechanism",
            "interface",
            "engineering_loop",
            "contribution_shape",
            "method_improvement_claim",
            "killer_experiment",
        ]
    ).lower()
    if archetype in {"architecture", "model_architecture"}:
        if any(token in text for token in ["interface", "routing", "gate", "gating", "api", "boundary"]):
            return "interface_invention"
        if any(token in text for token in ["closed-loop", "closed loop", "sense", "act", "feedback", "system"]):
            return "closed_loop_system"
        if any(token in text for token in ["policy", "control", "critic", "residual", "controller"]):
            return "control_policy_mechanism"
        return "representation_shift"
    shape = _taxonomy_token(axis.get("contribution_shape"))
    if shape in {"evaluation_protocol", "benchmark"}:
        return "evaluation_metric"
    if shape == "failure_model":
        return "failure_model"
    if shape == "dataset":
        return "data_or_labeling_strategy"
    if shape == "method_improvement":
        return "method_improvement"
    if shape == "control_interface":
        return "interface_invention"
    if shape in {"algorithm", "mechanism"}:
        return "control_policy_mechanism"
    if shape in {"architecture", "system"}:
        return "closed_loop_system"
    return ""


def _axis_text(axis: dict[str, Any]) -> str:
    return " ".join(str(axis.get(field, "")) for field in [*DIVERGENT_REQUIRED_FIELDS, *DIVERGENT_QUALITY_FIELDS]).lower()


def _infer_research_claim_type(axis: dict[str, Any]) -> str:
    token = _taxonomy_token(axis.get("research_claim_type"))
    if token in VALID_RESEARCH_CLAIM_TYPES:
        return token
    text = _axis_text(axis)
    shape = _taxonomy_token(axis.get("contribution_shape"))
    archetype = _taxonomy_token(axis.get("idea_archetype"))
    if "world model" in text or "digital twin" in text or "simulator" in text:
        return "world_model_simulation"
    if shape in {"evaluation_protocol", "benchmark"} or archetype == "evaluation_metric":
        return "evaluation_benchmark"
    if shape == "dataset" or archetype == "data_or_labeling_strategy":
        return "data_curriculum"
    if archetype == "instrumentation_or_sensing" or any(token in text for token in ["tactile", "sensor", "observability", "calibration"]):
        return "sensing_observability"
    if archetype == "representation_shift" or any(token in text for token in ["latent", "representation", "belief state", "contact topology"]):
        return "representation"
    if archetype == "interface_invention" or shape == "control_interface" or any(token in text for token in ["boundary", "contract", "interface"]):
        return "interface_boundary"
    if any(token in text for token in ["loss", "objective", "optimization", "critic training"]):
        return "objective_optimization"
    if any(token in text for token in ["transfer", "continual", "lifelong", "cross-embodiment", "cross task"]):
        return "continual_transfer"
    if any(token in text for token in ["embodiment", "controller", "co-design", "latency"]):
        return "embodiment_control_codesign"
    if archetype == "failure_model" or any(token in text for token in ["recovery", "shield", "safety", "irreversible"]):
        return "safety_recovery"
    return "interface_boundary"


def _infer_origin_type(axis: dict[str, Any], claim_type: str) -> str:
    token = _taxonomy_token(axis.get("origin_type"))
    if token in VALID_ORIGIN_TYPES:
        return token
    text = _axis_text(axis)
    if claim_type == "evaluation_benchmark" or any(token in text for token in ["metric blind", "evaluation blind", "success rate hides", "benchmark gap"]):
        return "evaluation_blind_spot"
    if claim_type == "objective_optimization" or any(token in text for token in ["loss", "objective mismatch", "optimization space"]):
        return "objective_mismatch"
    if claim_type == "representation" or any(token in text for token in ["latent mismatch", "representation mismatch", "unmodeled latent"]):
        return "representation_mismatch"
    if any(token in text for token in ["assumption conflict", "contradiction", "paper assumption"]):
        return "paper_assumption_contradiction"
    if any(token in text for token in ["deadlock", "sota", "cannot tell", "science question"]):
        return "scientific_deadlock"
    if any(token in text for token in ["occlusion", "slip", "collision", "drift", "failure", "contact"]):
        return "physical_scene"
    return "engineering_bottleneck"


def _infer_bottleneck_type(axis: dict[str, Any]) -> str:
    token = _taxonomy_token(axis.get("bottleneck_type"))
    if token in VALID_BOTTLENECK_TYPES:
        return token
    text = _axis_text(axis)
    if any(token in text for token in ["occlusion", "hidden", "partial observ", "unobserv"]):
        return "partial_observability"
    if any(token in text for token in ["contact", "topology", "rope", "cable", "dlo", "tangle"]):
        return "contact_topology"
    if any(token in text for token in ["multimodal", "bimanual", "coordination", "diffusion"]):
        return "action_multimodality"
    if any(token in text for token in ["shift", "sim-to-real", "cross-task", "cross embodiment", "transfer"]):
        return "distribution_shift"
    if any(token in text for token in ["metric", "benchmark", "evaluation", "success rate"]):
        return "evaluation_blindness"
    if any(token in text for token in ["data", "demo", "rare", "bias", "curriculum"]):
        return "data_sparsity_bias"
    if any(token in text for token in ["latency", "real-time", "rate", "milliseconds"]):
        return "latency_real_time"
    if any(token in text for token in ["irreversible", "unsafe", "safety", "damage", "recovery"]):
        return "irreversibility_safety"
    if any(token in text for token in ["loss", "objective", "critic", "optimization"]):
        return "objective_mismatch"
    return "system_boundary_mismatch"


def _infer_evidence_mode(axis: dict[str, Any]) -> str:
    token = _taxonomy_token(axis.get("evidence_mode"))
    if token in VALID_EVIDENCE_MODES:
        return token
    text = _axis_text(axis)
    if any(token in text for token in ["offline", "replay", "logs", "log replay"]):
        return "offline_replay"
    if any(token in text for token in ["simulation", "simulator", "toy dynamics", "synthetic"]):
        return "simulation"
    if any(token in text for token in ["public dataset", "open x", "droid", "bridge", "dataset"]):
        return "public_dataset"
    if any(token in text for token in ["teleop", "human study", "operator"]):
        return "human_study_teleop"
    if any(token in text for token in ["negative result", "diagnostic", "falsify"]):
        return "negative_result_diagnostic"
    if any(token in text for token in ["benchmark", "stress suite", "synthetic benchmark"]):
        return "synthetic_benchmark"
    return "small_real_robot_test"


def _infer_risk_class(axis: dict[str, Any], claim_type: str, origin_type: str) -> str:
    token = _taxonomy_token(axis.get("risk_class"))
    if token in VALID_RISK_CLASSES:
        return token
    text = _axis_text(axis)
    if any(token in text for token in ["breakthrough", "anti-roadmap", "field-changing", "new research line", "violates"]):
        return "breakthrough"
    if claim_type in {"representation", "interface_boundary", "objective_optimization", "world_model_simulation"} or origin_type in NON_FAILURE_ORIGIN_TYPES:
        return "mechanism"
    return "grounded"


def _infer_world_model_role(axis: dict[str, Any]) -> str:
    token = _taxonomy_token(axis.get("world_model_role"))
    if token in VALID_WORLD_MODEL_ROLES:
        return token
    text = _axis_text(axis)
    if not any(token in text for token in ["world model", "digital twin", "simulator", "simulation", "generative video"]):
        return "none"
    if any(token in text for token in ["counterfactual", "rank", "evaluate", "evaluator"]):
        return "counterfactual_evaluator"
    if any(token in text for token in ["teacher", "distill", "latent state", "belief"]):
        return "latent_state_teacher"
    if any(token in text for token in ["critic", "shield", "reject", "deny", "safety"]):
        return "planning_critic_or_shield"
    if any(token in text for token in ["data", "curriculum", "rare transition", "generate"]):
        return "data_generator_or_curriculum"
    if any(token in text for token in ["calibration", "friction", "material", "delay"]):
        return "digital_twin_calibration_loop"
    return "evaluation_surrogate"


def _portfolio_slot(claim_type: str, risk_class: str) -> str:
    if risk_class == "breakthrough":
        return "breakthrough_anti_roadmap"
    if claim_type in {"representation", "interface_boundary", "objective_optimization"}:
        return "mechanism"
    if claim_type in {"data_curriculum", "evaluation_benchmark"}:
        return "measurement_data"
    if claim_type == "world_model_simulation":
        return "world_model"
    if claim_type in {"continual_transfer", "embodiment_control_codesign"}:
        return "transfer_embodiment"
    return "grounded_engineering"


AXES = [
    {
        "title": "Tactile topology recovery for bimanual DLO manipulation",
        "domains": ["DLO", "tactile", "bimanual", "planning"],
        "problem": "Vision-only DLO policies often miss contact, occlusion, and topology changes that appear before terminal failure.",
        "pilot": "Use a small DLO routing or handover task with vision-only, tactile-only, and vision+tactile variants.",
        "baselines": "vision-only Diffusion Policy; topology-aware planner; fixed-threshold contact recovery.",
        "metrics": "topology violation count; task success; contact-loss events; recovery attempts.",
    },
    {
        "title": "Reactive diffusion policies for high-frequency contact correction",
        "domains": ["diffusion", "tactile", "failure", "imitation"],
        "problem": "Action chunking is expressive but often too slow to react to contact-rich disturbances.",
        "pilot": "Compare open-loop action chunks with feedback-conditioned action corrections on a contact-rich manipulation task.",
        "baselines": "standard Diffusion Policy; receding-horizon diffusion; impedance control with hand-tuned feedback.",
        "metrics": "reaction latency; disturbance recovery; contact stability; denoising budget.",
    },
    {
        "title": "Evidence-driven Sim-to-Real evaluation for contact-rich manipulation",
        "domains": ["sim-to-real", "benchmark", "tactile", "failure"],
        "problem": "Sim-to-Real papers often use incomparable task setups, sensors, and failure definitions.",
        "pilot": "Define a compact evaluation sheet for one DLO/tactile task and compare one simulation-only policy against one real-finetuned policy.",
        "baselines": "Monte Carlo estimator; domain randomization; real-data finetuning; no-tactile transfer.",
        "metrics": "transfer gap; per-factor robustness; failure taxonomy; confidence interval width.",
    },
    {
        "title": "VLA intent constrained by local geometry and contact rules",
        "domains": ["VLA", "planning", "bimanual", "DLO"],
        "problem": "VLA systems can produce plausible intents while ignoring geometric, contact, or topology constraints.",
        "pilot": "Translate language intent into local constraints before control and compare against direct VLA action prediction.",
        "baselines": "direct VLA action; language-conditioned Diffusion Policy; symbolic task-and-motion planning.",
        "metrics": "constraint satisfaction; completion rate; intervention count; planning latency.",
    },
    {
        "title": "Failure memory for long-horizon embodied manipulation",
        "domains": ["VLA", "failure", "planning", "imitation"],
        "problem": "Embodied agents often repeat recoverable failures because success/failure experience is not converted into reusable control constraints.",
        "pilot": "Build a failure memory from failed rollouts and test whether retrieval changes recovery decisions.",
        "baselines": "no memory; prompt-only reflection; fixed recovery script; learned failure classifier.",
        "metrics": "repeat failure rate; recovery success; false recovery triggers; human intervention count.",
    },
    {
        "title": "Reusable contact primitives for low-data deformable manipulation",
        "domains": ["DLO", "imitation", "bimanual", "diffusion"],
        "problem": "Demonstrations for deformable manipulation are expensive and often do not transfer across layouts.",
        "pilot": "Segment demonstrations into contact primitives and train a primitive-conditioned policy under a small data budget.",
        "baselines": "behavior cloning; Diffusion Policy; nearest-neighbor primitive retrieval.",
        "metrics": "few-shot success; primitive reuse; layout generalization; contact-slip failure rate.",
    },
    {
        "title": "Real-to-sim scene reconstruction for fast manipulation policy iteration",
        "domains": ["sim-to-real", "diffusion", "planning", "benchmark"],
        "problem": "High-fidelity simulation can help policy iteration, but reconstruction quality and control-relevant fidelity are rarely separated.",
        "pilot": "Use reconstructed scenes for policy pretraining and compare against real-only finetuning on one manipulation task.",
        "baselines": "real-only training; domain randomized simulator; reconstructed-scene simulator.",
        "metrics": "sample efficiency; transfer gap; visual fidelity proxy; control success.",
    },
    {
        "title": "Sensor placement as an experimental variable for tactile robot learning",
        "domains": ["tactile", "benchmark", "failure", "imitation"],
        "problem": "Tactile papers often change sensor hardware and policy together, making it hard to know what sensing actually contributes.",
        "pilot": "Fix the policy architecture and vary tactile placement or modality on a simple contact-rich task.",
        "baselines": "vision-only; fingertip tactile; palm/contact patch tactile; force-torque only.",
        "metrics": "success; slip/contact detection; calibration burden; robustness to unseen objects.",
    },
]


MECHANISM_SPECS = [
    {
        "cluster_id": "rl_token_failure_memory_critic",
        "title": "Critic-side failure memory over RL-token interfaces",
        "domains": ["VLA", "failure", "planning", "imitation"],
        "keywords": ["rl token", "online rl", "failure recovery", "recovery", "critic", "actor-critic", "anchor", "risk", "memory"],
        "strong_keywords": ["rl token", "online rl", "critic", "actor-critic", "anchor", "memory", "failure recovery"],
        "core_source_notes": ["wiki/topics/xu2026token.md", "wiki/topics/jie2026omnivlarl.md", "wiki/topics/dai2024racer.md"],
        "active_focus_tracks": ["rl-token-vla-online-rl"],
        "priority": 5,
        "problem": "Online VLA fine-tuning can repeat recoverable failures because failed trajectories are not exposed through a stable value-risk interface.",
        "mechanism": "retrieve failed or recovered traces and feed their embedding only to a value-risk critic over frozen VLA/RL-token features.",
        "interface": "critic_input: Q_fail(z_rl, action, retrieved_failure_trace)",
        "hypothesis": "A critic-side failure-memory interface should reduce repeated failures without destabilizing the anchored VLA actor.",
        "nearest_pressure": "RL Token, OmniVLA-RL, OpenVLA, RACER, long-horizon VLA planning, and prompt/reflection memory baselines.",
        "pilot": "Use a replay-buffer or simulator setup with frozen VLA-like tokens and compare no-memory, real retrieval, random retrieval, prompt memory, actor memory, and actor+critic memory.",
        "baselines": "RL head without memory; random retrieved memory; actor-side memory; prompt-only memory; fixed recovery script.",
        "metrics": "sample efficiency; repeated failure rate; recovery success; policy drift; critic calibration; intervention count.",
        "falsification": "Reject if real failure retrieval does not beat no-memory and random-memory controls, or if actor-side memory explains the gains.",
    },
    {
        "cluster_id": "dlo_contact_topology_state",
        "title": "Contact-state recovery before bimanual DLO topology failure",
        "domains": ["DLO", "tactile", "bimanual", "failure"],
        "keywords": ["dlo", "rope", "cable", "contact loss", "contact", "topology", "slip", "tactile", "bimanual"],
        "strong_keywords": ["dlo", "rope", "cable", "contact loss", "topology", "slip", "tactile", "bimanual"],
        "priority": 3,
        "problem": "DLO manipulation failures often become visible only after contact loss, crossing, slack, or topology violation has already happened.",
        "mechanism": "estimate a compact contact/topology state before terminal failure and use it as a recovery trigger or policy condition.",
        "interface": "state_estimator: s_contact = f(vision, tactile, gripper state, short history)",
        "hypothesis": "A low-dimensional contact/topology state can improve bimanual DLO recovery more reliably than adding raw tactile streams to the actor.",
        "nearest_pressure": "Tube Diffusion Policy, PolyTouch, tactile sensing papers, DLO planners, and topology-aware manipulation baselines.",
        "pilot": "Define one DLO state variable such as contact loss, slip, crossing, slack, or knot precursor, then test detection and recovery on a small routing or handover task.",
        "baselines": "vision-only policy; raw tactile policy; fixed contact threshold; topology-aware planner; nearest-neighbor recovery.",
        "metrics": "state detection F1; topology violation count; contact-loss events; recovery success; task success; false trigger rate.",
        "falsification": "Reject if the state cannot be labeled reliably or if raw tactile/vision policies match recovery after controlling for task stage.",
    },
    {
        "cluster_id": "reactive_contact_correction",
        "title": "Reactive contact correction for action-chunk policies",
        "domains": ["diffusion", "tactile", "failure", "imitation"],
        "keywords": ["diffusion", "action chunk", "contact", "tactile", "reactive", "latency", "disturbance", "correction"],
        "strong_keywords": ["diffusion", "action chunk", "tactile", "reactive", "latency", "disturbance", "correction"],
        "priority": 3,
        "problem": "Long action chunks can be expressive but too slow to correct unexpected contact changes during manipulation.",
        "mechanism": "keep the nominal chunk policy fixed while adding a high-rate correction interface driven by contact or tactile events.",
        "interface": "residual_controller: a_t = a_chunk_t + delta_contact(obs_contact)",
        "hypothesis": "A narrow contact residual can improve disturbance recovery without retraining the whole diffusion/action-chunk policy.",
        "nearest_pressure": "Tube Diffusion Policy, Diffusion Policy, reactive control, impedance control, and tactile feedback policies.",
        "pilot": "Run a contact-rich task with open-loop chunks, receding-horizon chunks, and event-triggered residual correction.",
        "baselines": "standard Diffusion Policy; receding-horizon diffusion; hand-tuned impedance control; tactile-conditioned full policy.",
        "metrics": "reaction latency; recovery after disturbance; contact stability; denoising budget; task success; overshoot rate.",
        "falsification": "Reject if receding-horizon diffusion or impedance control matches performance at the same latency and reset budget.",
    },
    {
        "cluster_id": "sensor_observation_prior",
        "title": "Sensor signal design as an observation prior for robot learning",
        "domains": ["tactile", "benchmark", "failure", "imitation"],
        "keywords": ["sensor", "tactile", "proximity", "observation prior", "placement", "coverage", "sample efficiency", "signal"],
        "strong_keywords": ["sensor", "tactile", "proximity", "observation prior", "placement", "coverage", "sample efficiency"],
        "priority": 2,
        "problem": "Robot learning papers often change sensor hardware, signal encoding, and policy architecture together, hiding what sensing actually contributes.",
        "mechanism": "hold the learner fixed and vary only sensor coverage, signal type, or placement to measure observation-prior effects.",
        "interface": "observation_design: policy(obs_fixed + sensor_variant)",
        "hypothesis": "Low-dimensional, task-aligned tactile/proximity signals can beat denser signals in sample efficiency and robustness.",
        "nearest_pressure": "Egocentric tactile/proximity collision avoidance, tactile placement studies, PolyTouch, and tactile benchmark papers.",
        "pilot": "Fix one manipulation or avoidance policy and compare field/proximity, ray/depth, contact-only, and force-torque signals.",
        "baselines": "vision-only; dense tactile/depth signal; sparse proximity/contact signal; force-torque only.",
        "metrics": "sample efficiency; success; slip/contact detection; robustness; calibration burden; false positive rate.",
        "falsification": "Reject if gains disappear under equal observation dimension or if policy capacity explains the effect.",
    },
    {
        "cluster_id": "control_relevant_sim_to_real_evaluation",
        "title": "Control-relevant Sim-to-Real evaluation for contact-rich manipulation",
        "domains": ["sim-to-real", "benchmark", "failure", "tactile"],
        "keywords": ["sim-to-real", "real-to-sim", "transfer gap", "domain randomization", "real-finetuned", "contact-rich", "failure taxonomy", "reconstruction"],
        "strong_keywords": ["sim-to-real", "real-to-sim", "transfer gap", "domain randomization", "real-finetuned", "failure taxonomy", "reconstruction"],
        "priority": 1,
        "problem": "Sim-to-Real evaluations often mix visual fidelity, dynamics fidelity, and control success into one score.",
        "mechanism": "separate control-relevant transfer factors and report failure-conditioned metrics instead of only final success.",
        "interface": "evaluation_protocol: transfer_gap(task, factor, failure_mode)",
        "hypothesis": "Failure-conditioned transfer metrics will better predict real manipulation performance than aggregate success or visual-fidelity proxies.",
        "nearest_pressure": "Sim-to-Real benchmarks, real-to-sim reconstruction, contact-rich manipulation evaluations, and domain randomization baselines.",
        "pilot": "Choose one contact-rich task and compare simulation-only, domain-randomized, reconstructed-scene, and small real-finetuned policies.",
        "baselines": "aggregate success; domain randomization; real-only finetuning; simulation-only policy; no-tactile transfer.",
        "metrics": "transfer gap; failure taxonomy; confidence interval width; intervention count; per-factor robustness; real success.",
        "falsification": "Reject if factor-conditioned metrics do not predict real failure better than aggregate success.",
    },
    {
        "cluster_id": "vla_local_constraint_interface",
        "title": "Local constraint interface for VLA manipulation intents",
        "domains": ["VLA", "planning", "DLO", "bimanual"],
        "keywords": ["constraint", "geometry", "contact", "planning", "intent", "local constraint", "trajectory", "long-horizon"],
        "strong_keywords": ["constraint", "geometry", "planning", "intent", "local constraint", "trajectory", "long-horizon"],
        "priority": 2,
        "problem": "VLA outputs can be semantically plausible while violating local geometry, contact, or topology constraints.",
        "mechanism": "translate VLA intent into local constraints that gate or reshape low-level actions before execution.",
        "interface": "constraint_filter: action = project(pi_vla(obs, text), local_constraints)",
        "hypothesis": "A local constraint interface should reduce geometric/contact violations more cleanly than prompting or direct action finetuning.",
        "nearest_pressure": "VLA planning, CodeGraphVLP, LoHo-Manip, task-and-motion planning, and language-conditioned diffusion baselines.",
        "pilot": "Use one manipulation task with explicit local constraints and compare direct VLA action, prompt constraints, planner constraints, and action projection.",
        "baselines": "direct VLA action; prompt-only constraint; symbolic planner; language-conditioned Diffusion Policy.",
        "metrics": "constraint violation rate; task success; intervention count; planning latency; recovery success.",
        "falsification": "Reject if prompt-only or planner-only constraints match the action-interface gains at similar latency.",
    },
]


def _matches(record: dict[str, Any], domains: list[str]) -> bool:
    record_domains = set(record.get("domains", []))
    return bool(record_domains.intersection(domains))


def _source_count(records: list[dict[str, Any]]) -> int:
    return len({record.get("source_note") for record in records})


def _recent_count(records: list[dict[str, Any]], focus_keys: set[str]) -> int:
    return len({record.get("source_note") for record in records if str(record.get("zotero_key", "")).upper() in focus_keys})


def _record_text(record: dict[str, Any]) -> str:
    # Use only direct evidence text for mechanism matching. Transfer fields are useful metadata,
    # but they are too broad and can make unrelated notes look like mechanism support.
    return " ".join(
        str(record.get(key, ""))
        for key in ["source_title", "statement", "risks"]
    ).lower()


def _keyword_hits(text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if keyword.lower() in text)


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in re.split(r"[,;/]", value) if item.strip()]
    return []


def _compact_candidate(axis: dict[str, Any], *, max_chars: int = 700) -> dict[str, Any]:
    compact: dict[str, Any] = {}
    for key in [
        "title",
        "problem",
        "engineering_pathology",
        "mechanism",
        "interface",
        "hypothesis",
        "evidence_links",
        "speculative_jump",
        "nearest_pressure",
        "pilot",
        "baselines",
        "metrics",
        "falsification",
        "domains",
        "keywords",
        "strong_keywords",
    ]:
        value = axis.get(key)
        compact[key] = value[:max_chars] if isinstance(value, str) else value
    return compact


def _text_keywords(text: str, *, max_keywords: int = 16) -> list[str]:
    counts: Counter[str] = Counter()
    for token in re.findall(r"[a-z][a-z0-9-]{2,}", text.lower()):
        if token in DIVERGENT_STOPWORDS:
            continue
        if token.endswith("ing") and len(token) > 6:
            token = token[:-3]
        counts[token] += 1
    return [token for token, _ in counts.most_common(max_keywords)]


def _idea_keywords(axis: dict[str, Any]) -> list[str]:
    explicit = _as_string_list(axis.get("keywords")) + _as_string_list(axis.get("strong_keywords"))
    if explicit:
        return sorted({item.lower() for item in explicit})
    text = " ".join(str(axis.get(field, "")) for field in [*DIVERGENT_REQUIRED_FIELDS, *DIVERGENT_QUALITY_FIELDS])
    return _text_keywords(text)


def _quality_keywords(axis: dict[str, Any], *, max_keywords: int = 18) -> list[str]:
    text = " ".join(
        str(axis.get(field, ""))
        for field in [
            "title",
            "problem",
            "engineering_pathology",
            "mechanism",
            "interface",
            "hypothesis",
            "non_obvious_claim",
            "strongest_baseline",
            "killer_experiment",
            "contribution_shape",
        ]
    ).lower()
    counts: Counter[str] = Counter()
    for token in re.findall(r"[a-z][a-z0-9-]{2,}", text):
        if token in QUALITY_STOPWORDS:
            continue
        if token.endswith("ing") and len(token) > 6:
            token = token[:-3]
        counts[token] += 1
    return [token for token, _ in counts.most_common(max_keywords)]


def _is_source_availability_note(record: dict[str, Any]) -> bool:
    if record.get("claim_type") != "evidence_note":
        return False
    text = _record_text(record)
    if not any(pattern in text for pattern in SOURCE_AVAILABILITY_PATTERNS):
        return False
    return not any(marker in text for marker in RESULT_MARKERS)


def _strong_mechanism_record(record: dict[str, Any], spec: dict[str, Any]) -> bool:
    if _is_source_availability_note(record):
        return False
    text = _record_text(record)
    keywords = [item.lower() for item in spec.get("strong_keywords", spec.get("keywords", []))]
    keyword_hits = _keyword_hits(text, keywords)
    required_hits = int(spec.get("min_strong_keyword_hits", 2))
    if str(record.get("source_note", "")) in set(spec.get("core_source_notes", [])):
        return keyword_hits >= 1 or record.get("claim_type") in STRONG_CLAIM_TYPES
    if record.get("claim_type") in STRONG_CLAIM_TYPES:
        return keyword_hits >= required_hits
    if record.get("claim_type") == "evidence_note":
        return keyword_hits >= 2 and any(marker in text for marker in QUANT_OR_MECHANISM_MARKERS)
    return keyword_hits >= 2


def _strong_source_count(records: list[dict[str, Any]], spec: dict[str, Any]) -> int:
    return len({record.get("source_note") for record in records if _strong_mechanism_record(record, spec)})


def _focus_track_bonus(spec: dict[str, Any]) -> int:
    bonus = 0
    root = vault_path("projects", "focus-tracks")
    for track_id in spec.get("active_focus_tracks", []):
        track_root = root / track_id
        if not track_root.exists():
            continue
        dashboard = track_root / "track-dashboard.md"
        text = dashboard.read_text(encoding="utf-8", errors="replace").lower() if dashboard.exists() else ""
        if 'status: "archived"' in text or "current_state: `blocked`" in text:
            continue
        bonus += 300
    return bonus


def _focus_track_evidence_records() -> list[dict[str, Any]]:
    root = vault_path("projects", "focus-tracks")
    if not root.exists():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(root.glob("*/evidence/track_evidence.jsonl")):
        track_id = path.parts[-3]
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not raw.strip():
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                records.append({**record, "focus_track_id": track_id, "from_focus_track": True})
    return records


def _merge_focus_track_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [*records]
    seen = {
        (
            str(record.get("source_note", "")),
            str(record.get("claim_type", "")),
            str(record.get("statement", ""))[:220],
        )
        for record in records
    }
    for record in _focus_track_evidence_records():
        key = (
            str(record.get("source_note", "")),
            str(record.get("claim_type", "")),
            str(record.get("statement", ""))[:220],
        )
        if key in seen:
            continue
        merged.append(record)
        seen.add(key)
    return merged


def _supporting(records: list[dict[str, Any]], domains: list[str], *, focus_keys: set[str], limit: int = 12) -> list[dict[str, Any]]:
    ranked = []
    for record in records:
        if not _matches(record, domains):
            continue
        score = len(set(record.get("domains", [])).intersection(domains)) * 10
        if str(record.get("zotero_key", "")).upper() in focus_keys:
            score += 25
        if record.get("claim_type") in {"problem", "limitation", "open_question", "metric", "method"}:
            score += 5
        ranked.append((score, record))
    return _dedupe_sources([record for _, record in sorted(ranked, key=lambda item: -item[0])], limit=limit)


def _dedupe_sources(records: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in records:
        source = str(record.get("source_note", ""))
        if source in seen:
            continue
        selected.append(record)
        seen.add(source)
        if len(selected) >= limit:
            break
    return selected


def _evidence_lines(records: list[dict[str, Any]], limit: int = 10) -> list[str]:
    if not records:
        return ["- evidence_gap: no supporting matrix records found."]
    lines = []
    for record in _dedupe_sources(records, limit=limit):
        lines.append(
            f"- {note_link(record.get('source_note', ''), record.get('source_title'))}: "
            f"{record.get('claim_type')}: {record.get('statement', '')[:260]}"
        )
    return lines


def _focus_track_context(max_chars: int = 4000) -> str:
    root = vault_path("projects", "focus-tracks")
    if not root.exists():
        return ""
    chunks: list[str] = []
    for path in sorted(root.glob("*/*.md")) + sorted(root.glob("*/*/*.md")):
        if path.name == "accepted_claims.jsonl":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        chunks.append(f"FILE: {rel(path)}\n{body[:900]}")
        if sum(len(chunk) for chunk in chunks) >= max_chars:
            break
    return "\n\n".join(chunks)[:max_chars]


def _mechanism_supporting(records: list[dict[str, Any]], spec: dict[str, Any], *, focus_keys: set[str], limit: int = 14) -> list[dict[str, Any]]:
    ranked: list[tuple[int, dict[str, Any]]] = []
    keywords = [item.lower() for item in spec.get("keywords", [])]
    strong_keywords = [item.lower() for item in spec.get("strong_keywords", keywords)]
    domains = set(spec.get("domains", []))
    core_sources = set(spec.get("core_source_notes", []))
    for record in records:
        if _is_source_availability_note(record):
            continue
        record_domains = set(record.get("domains", []))
        domain_hits = len(record_domains.intersection(domains))
        text = _record_text(record)
        keyword_hits = _keyword_hits(text, keywords)
        strong_keyword_hits = _keyword_hits(text, strong_keywords)
        if not keyword_hits:
            continue
        if not domain_hits and str(record.get("source_note", "")) not in core_sources:
            continue
        if record.get("claim_type") in SUPPORT_CLAIM_TYPES and strong_keyword_hits < 2 and str(record.get("source_note", "")) not in core_sources:
            continue
        score = domain_hits * 10 + keyword_hits * 6 + strong_keyword_hits * 12
        if _strong_mechanism_record(record, spec):
            score += 45
        if record.get("from_focus_track"):
            score += 30
        if str(record.get("source_note", "")) in core_sources:
            score += 35
        if str(record.get("zotero_key", "")).upper() in focus_keys:
            score += 30
        if record.get("claim_type") in STRONG_CLAIM_TYPES:
            score += 12
        elif record.get("claim_type") in SUPPORT_CLAIM_TYPES:
            score += 6
        ranked.append((score, record))
    return _dedupe_sources([record for _, record in sorted(ranked, key=lambda item: -item[0])], limit=limit)


def _keyword_source_count(axis: dict[str, Any], evidence: list[dict[str, Any]], *, min_hits: int = 2) -> int:
    cluster_id = axis.get("cluster_id")
    spec = next((item for item in MECHANISM_SPECS if item["cluster_id"] == cluster_id), None)
    keywords = [item.lower() for item in (spec or axis).get("keywords", [])]
    if not keywords:
        keywords = _idea_keywords(axis)
    count = 0
    for record in evidence:
        text = _record_text(record)
        if _keyword_hits(text, keywords) >= min_hits:
            count += 1
    return count


def _legacy_dynamic_axes(records: list[dict[str, Any]], *, max_axes: int) -> list[dict[str, Any]]:
    domain_counts: Counter[tuple[str, str]] = Counter()
    for record in records:
        domains = sorted(domain for domain in record.get("domains", []) if domain not in {"failure"})
        for left, right in itertools.combinations(domains[:6], 2):
            domain_counts[(left, right)] += 1
    axes = []
    for (left, right), count in domain_counts.most_common(max_axes):
        if count < 6:
            continue
        axes.append(
            {
                "title": f"Cross-gap between {left} and {right}",
                "domains": [left, right],
                "problem": f"The evidence matrix repeatedly connects {left} and {right}, but the exact unresolved experiment has not been promoted yet.",
                "pilot": f"Choose one local task where {left} and {right} both appear, then isolate the smallest controllable experimental variable.",
                "baselines": "current local strongest method; ablated variant without the cross-domain component; simple rule-based baseline.",
                "metrics": "task success; failure category; sample efficiency; robustness under controlled perturbation.",
            }
        )
    return axes


def _as_str(value: Any) -> str:
    """Coerce list or other types to string for Gemini divergent normalization."""
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if str(item).strip())
    return str(value) if value is not None else ""


def _compact_rejected_drafts(value: Any, *, limit: int = MAX_REJECTED_DRAFT_SUMMARY) -> list[dict[str, str]]:
    """Keep a short trace of Gemini's source-level self-filtering without promoting rejected drafts."""
    if not isinstance(value, list):
        return []
    compact: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        row: dict[str, str] = {}
        for key in ["draft_title", "failure_reason", "strongest_baseline", "mutation_attempted", "why_not_candidate"]:
            text = _as_str(item.get(key, "")).strip()
            if text:
                row[key] = text[:500]
        if row:
            compact.append(row)
        if len(compact) >= limit:
            break
    return compact


def _normalize_mechanism_axis(axis: dict[str, Any]) -> dict[str, Any]:
    domains = _as_string_list(axis.get("domains"))
    keywords = _as_string_list(axis.get("keywords"))
    strong_keywords = _as_string_list(axis.get("strong_keywords")) or keywords
    claim_type = _infer_research_claim_type(axis)
    origin_type = _infer_origin_type(axis, claim_type)
    bottleneck_type = _infer_bottleneck_type(axis)
    evidence_mode = _infer_evidence_mode(axis)
    risk_class = _infer_risk_class(axis, claim_type, origin_type)
    world_model_role = _infer_world_model_role(axis)
    portfolio_slot = _as_str(axis.get("portfolio_slot", "")).strip() or _portfolio_slot(claim_type, risk_class)
    return {
        "generation_rule": axis.get("generation_rule", "mechanism_cluster"),
        "generator_status": axis.get("generator_status", "template"),
        "cluster_id": axis.get("cluster_id", slugify(axis.get("title", "mechanism"))),
        "title": _as_str(axis.get("title", "Untitled mechanism seed")).strip(),
        "domains": domains,
        "keywords": keywords,
        "strong_keywords": strong_keywords,
        "min_strong_sources": int(axis.get("min_strong_sources", MIN_STRONG_MECHANISM_SOURCES)),
        "problem": _as_str(axis.get("problem", "")).strip(),
        "engineering_pathology": _as_str(axis.get("engineering_pathology", "")).strip(),
        "mechanism": _as_str(axis.get("mechanism", "")).strip(),
        "interface": _as_str(axis.get("interface", "")).strip(),
        "hypothesis": _as_str(axis.get("hypothesis", axis.get("working_hypothesis", ""))).strip(),
        "evidence_links": _as_str(axis.get("evidence_links", "")).strip(),
        "speculative_jump": _as_str(axis.get("speculative_jump", "")).strip(),
        "origin_type": origin_type,
        "research_claim_type": claim_type,
        "bottleneck_type": bottleneck_type,
        "evidence_mode": evidence_mode,
        "risk_class": risk_class,
        "world_model_role": world_model_role,
        "portfolio_slot": portfolio_slot,
        "idea_archetype": _as_str(axis.get("idea_archetype", "")).strip(),
        "contribution_shape": _as_str(axis.get("contribution_shape", "")).strip(),
        "physical_failure_scene": _as_str(axis.get("physical_failure_scene", "")).strip(),
        "non_obvious_claim": _as_str(axis.get("non_obvious_claim", "")).strip(),
        "naive_combination_version": _as_str(axis.get("naive_combination_version", "")).strip(),
        "strongest_baseline_kill_path": _as_str(axis.get("strongest_baseline_kill_path", "")).strip(),
        "post_kill_mutation": _as_str(axis.get("post_kill_mutation", "")).strip(),
        "anti_combination_test": _as_str(axis.get("anti_combination_test", "")).strip(),
        "top_tier_rationale": _as_str(axis.get("top_tier_rationale", "")).strip(),
        "engineering_loop": _as_str(axis.get("engineering_loop", "")).strip(),
        "interface_innovation": _as_str(axis.get("interface_innovation", "")).strip(),
        "optimization_space": _as_str(axis.get("optimization_space", "")).strip(),
        "loss_placement": _as_str(axis.get("loss_placement", "")).strip(),
        "decoder_boundary": _as_str(axis.get("decoder_boundary", "")).strip(),
        "manifold_safety": _as_str(axis.get("manifold_safety", "")).strip(),
        "method_improvement_claim": _as_str(axis.get("method_improvement_claim", "")).strip(),
        "original_method_failure": _as_str(axis.get("original_method_failure", "")).strip(),
        "replacement_or_coupled_technique": _as_str(axis.get("replacement_or_coupled_technique", "")).strip(),
        "why_improvement_not_patch": _as_str(axis.get("why_improvement_not_patch", "")).strip(),
        "why_now": _as_str(axis.get("why_now", "Recent local evidence connects the mechanism, failure mode, and evaluation pressure.")).strip(),
        "strongest_baseline": _as_str(axis.get("strongest_baseline", "")).strip(),
        "baseline_failure_mode": _as_str(axis.get("baseline_failure_mode", "")).strip(),
        "killer_experiment": _as_str(axis.get("killer_experiment", "")).strip(),
        "novelty_risk": _as_str(axis.get("novelty_risk", "")).strip(),
        "reviewer_kill_shot": _as_str(axis.get("reviewer_kill_shot", "")).strip(),
        "rescue_mutation": _as_str(axis.get("rescue_mutation", "")).strip(),
        "claim_compression": _as_str(axis.get("claim_compression", "")).strip(),
        "online_or_offline_mode": _as_str(axis.get("online_or_offline_mode", "")).strip(),
        "minimum_no_hardware_pilot": _as_str(axis.get("minimum_no_hardware_pilot", "")).strip(),
        "baseline_kill_table": _as_str(axis.get("baseline_kill_table", "")).strip(),
        "what_would_make_this_not_a_paper": _as_str(axis.get("what_would_make_this_not_a_paper", "")).strip(),
        "reviewer_pre_mortem": _as_str(axis.get("reviewer_pre_mortem", "")).strip(),
        "falsification_discriminates_mechanism": _as_str(axis.get("falsification_discriminates_mechanism", "")).strip(),
        "lab_fit": _as_str(axis.get("lab_fit", "")).strip(),
        "hardware_assumptions": _as_str(axis.get("hardware_assumptions", "")).strip(),
        "negative_claim_boundary": _as_str(axis.get("negative_claim_boundary", "")).strip(),
        "version_evolution_story": _as_str(axis.get("version_evolution_story", "")).strip(),
        "core_insight": _as_str(axis.get("core_insight", "")).strip(),
        "pipeline_steps": _as_str(axis.get("pipeline_steps", "")).strip(),
        "defense_patches": _as_str(axis.get("defense_patches", "")).strip(),
        "baseline_matrix": _as_str(axis.get("baseline_matrix", "")).strip(),
        "metric_suite": _as_str(axis.get("metric_suite", "")).strip(),
        "risk_assumptions": _as_str(axis.get("risk_assumptions", "")).strip(),
        "competition_map": _as_str(axis.get("competition_map", "")).strip(),
        "two_week_sprint": _as_str(axis.get("two_week_sprint", "")).strip(),
        "promotion_reason": _as_str(axis.get("promotion_reason", "")).strip(),
        "rescue_signal": _as_str(axis.get("rescue_signal", "")).strip(),
        "nearest_pressure": _as_str(axis.get("nearest_pressure", "")).strip(),
        "pilot": _as_str(axis.get("pilot", axis.get("minimal_pilot", ""))).strip(),
        "baselines": _as_str(axis.get("baselines", "")).strip(),
        "metrics": _as_str(axis.get("metrics", "")).strip(),
        "falsification": _as_str(axis.get("falsification", axis.get("falsification_criteria", ""))).strip(),
        "status_boundary": _as_str(axis.get(
            "status_boundary",
            "Generated seed for user review only; no paper claim is accepted and no automatic promotion is allowed.",
        )).strip(),
        "candidate_group": axis.get("candidate_group"),
        "evidence_support_score": axis.get("evidence_support_score"),
        "support_score": axis.get("support_score"),
        "originality_score": axis.get("originality_score"),
        "engineering_value_score": axis.get("engineering_value_score"),
        "research_quality_score": axis.get("research_quality_score"),
        "research_quality_components": axis.get("research_quality_components", {}),
        "sharpness_score": axis.get("sharpness_score"),
        "evidence_execution_score": axis.get("evidence_execution_score"),
        "ordinaryness_penalty": axis.get("ordinaryness_penalty"),
        "quality_tier": axis.get("quality_tier"),
        "potential_score": axis.get("potential_score", axis.get("research_quality_score")),
        "potential_tier": axis.get("potential_tier", axis.get("quality_tier")),
        "quality_tier_semantics": axis.get("quality_tier_semantics", QUALITY_TIER_SEMANTICS),
        "readiness_tier": axis.get("readiness_tier", "untriaged"),
        "promotion_decision": axis.get("promotion_decision", "not_ready"),
        "novelty_pressure": axis.get("novelty_pressure", {}),
        "novelty_hits": axis.get("novelty_hits", []),
    }


def _gate_mechanism_candidate(axis: dict[str, Any], evidence: list[dict[str, Any]], recent: int, *, focus_keys: set[str]) -> list[str]:
    issues: list[str] = []
    spec = next((item for item in MECHANISM_SPECS if item["cluster_id"] == axis.get("cluster_id")), axis)
    required = ["title", "problem", "mechanism", "interface", "hypothesis", "nearest_pressure", "pilot", "baselines", "metrics", "falsification"]
    for field in required:
        if not str(axis.get(field, "")).strip():
            issues.append(f"missing_{field}")
    lowered = " ".join(str(axis.get(field, "")) for field in required).lower()
    for token in PLACEHOLDER_TOKENS:
        if token in lowered:
            issues.append(f"placeholder_token:{token}")
    if axis.get("title", "").lower().startswith("cross-gap between"):
        issues.append("generic_cross_gap_title")
    has_active_focus_track = _focus_track_bonus(spec) > 0
    min_sources = 4 if has_active_focus_track else MIN_MECHANISM_SOURCES
    if _source_count(evidence) < min_sources:
        issues.append(f"too_few_local_sources:{_source_count(evidence)}")
    strong_sources = _strong_source_count(evidence, spec)
    required_strong_sources = max(MIN_STRONG_MECHANISM_SOURCES, int(spec.get("min_strong_sources", MIN_STRONG_MECHANISM_SOURCES)))
    if strong_sources < required_strong_sources:
        issues.append(f"too_few_strong_mechanism_sources:{strong_sources}")
    if _keyword_source_count(axis, evidence) < 2:
        issues.append(f"too_few_mechanism_keyword_sources:{_keyword_source_count(axis, evidence)}")
    min_recent_focus = 1 if axis.get("candidate_group") == "wild_engineering" else 2
    if axis.get("generation_rule") == "gemini_divergent" and focus_keys and recent < min_recent_focus:
        issues.append(f"too_few_daily_focus_sources:{recent}")
    if focus_keys and recent < 1 and not has_active_focus_track:
        issues.append("no_recent_focus_evidence")
    if "baseline" not in axis.get("baselines", "").lower() and ";" not in axis.get("baselines", ""):
        issues.append("baseline_not_concrete")
    if "reject" not in axis.get("falsification", "").lower() and "if " not in axis.get("falsification", "").lower():
        issues.append("falsification_not_concrete")
    if axis.get("generation_rule") == "gemini_divergent":
        origin_type = str(axis.get("origin_type", "engineering_bottleneck"))
        claim_type = str(axis.get("research_claim_type", ""))
        physical_scene = axis.get("physical_failure_scene", "").strip().lower()
        if origin_type in {"physical_scene", "engineering_bottleneck"}:
            if len(physical_scene) < 80 or _component_from_markers(physical_scene, PHYSICAL_SCENE_MARKERS, 6, min_hits_for_full=2) < 3:
                issues.append("physical_failure_scene_missing_or_abstract")
        elif len(physical_scene) < 80 or _component_from_markers(physical_scene, SCIENTIFIC_DEADLOCK_MARKERS, 6, min_hits_for_full=2) < 3:
            issues.append("non_physical_origin_not_grounded")
        pathology = axis.get("engineering_pathology", "").strip().lower()
        pathology_markers = ENGINEERING_PATHOLOGY_MARKERS if origin_type in {"physical_scene", "engineering_bottleneck"} else SCIENTIFIC_DEADLOCK_MARKERS
        if len(pathology) < 80 or _component_from_markers(pathology, pathology_markers, 6, min_hits_for_full=2) < 3:
            issues.append("engineering_pathology_missing_or_abstract")
        if claim_type == "world_model_simulation":
            if str(axis.get("world_model_role", "none")) == "none":
                issues.append("world_model_role_missing")
            wm_text = " ".join(
                axis.get(field, "").strip().lower()
                for field in [
                    "mechanism",
                    "interface_innovation",
                    "killer_experiment",
                    "what_would_make_this_not_a_paper",
                    "falsification_discriminates_mechanism",
                ]
            )
            if not any(marker in wm_text for marker in ["latent", "invariant", "decision boundary", "hallucination", "critic", "teacher", "calibration"]):
                issues.append("world_model_role_under_specified")
        non_obvious = axis.get("non_obvious_claim", "").strip().lower()
        if len(non_obvious) < 45 or not any(marker in non_obvious for marker in ["instead", "not ", "only", "before", "because", "unlike", "rather than", "interface"]):
            issues.append("non_obvious_claim_missing_or_weak")
        naive = axis.get("naive_combination_version", "").strip().lower()
        if len(naive) < 60 or not any(marker in naive for marker in ["add", "combine", "module", "baseline", "naive", "simply", "just"]):
            issues.append("naive_combination_version_missing")
        kill_path = axis.get("strongest_baseline_kill_path", "").strip().lower()
        if len(kill_path) < 80 or not any(marker in kill_path for marker in ["kill", "baseline", "match", "outperform", "nbv", "information", "heuristic", "classic", "analytical"]):
            issues.append("strongest_baseline_kill_path_missing")
        mutation = axis.get("post_kill_mutation", "").strip().lower()
        if len(mutation) < 80 or not any(marker in mutation for marker in ["instead", "shift", "boundary", "feedback", "representation", "loss", "interface", "gate", "mutation"]):
            issues.append("post_kill_mutation_missing")
        active_view_text = " ".join(
            axis.get(field, "").strip().lower()
            for field in [
                "title",
                "physical_failure_scene",
                "mechanism",
                "interface_innovation",
                "strongest_baseline",
                "baseline_failure_mode",
                "baseline_matrix",
            ]
        )
        if any(marker in active_view_text for marker in ["viewpoint", "active vision", "camera orbit", "wrist-camera", "wrist camera"]):
            if not any(marker in active_view_text for marker in ["nbv", "next-best-view", "information gain", "occupancy", "geometric active vision"]):
                issues.append("active_viewpoint_missing_nbv_baseline")
        interface_innovation = axis.get("interface_innovation", "").strip().lower()
        if len(interface_innovation) < 70 or _component_from_markers(interface_innovation, INTERFACE_INNOVATION_MARKERS, 6, min_hits_for_full=2) < 3:
            issues.append("interface_innovation_missing_or_shallow")
        optimization_space = " ".join(
            axis.get(field, "").strip().lower()
            for field in ["optimization_space", "loss_placement", "decoder_boundary", "manifold_safety"]
        )
        if len(optimization_space) < 120 or _component_from_markers(optimization_space, OPTIMIZATION_SPACE_MARKERS, 8, min_hits_for_full=3) < 4:
            issues.append("optimization_space_not_analyzed")
        if len(axis.get("strongest_baseline", "").strip()) < 20:
            issues.append("strongest_baseline_missing")
        if len(axis.get("killer_experiment", "").strip()) < 30:
            issues.append("killer_experiment_missing")
        discriminates = axis.get("falsification_discriminates_mechanism", "").strip().lower()
        if len(discriminates) < 80 or not any(marker in discriminates for marker in ["mechanism", "patch", "baseline", "ablation", "because", "distinguish"]):
            issues.append("falsification_does_not_separate_mechanism_from_patch")
        lab_fit = axis.get("lab_fit", "").strip().lower()
        if len(lab_fit) < 60 or not any(marker in lab_fit for marker in ["franka", "flextac", "wrist", "camera", "bimanual", "dlo", "cable", "lab"]):
            issues.append("lab_fit_missing")
        if len(axis.get("negative_claim_boundary", "").strip()) < 80:
            issues.append("negative_claim_boundary_missing")
        if len(axis.get("core_insight", "").strip()) < 70:
            issues.append("core_insight_missing")
        if len(axis.get("pipeline_steps", "").strip()) < 120:
            issues.append("pipeline_steps_missing")
        if len(axis.get("defense_patches", "").strip()) < 80:
            issues.append("defense_patches_missing")
        if len(axis.get("baseline_matrix", "").strip()) < 120:
            issues.append("baseline_matrix_missing")
        if len(axis.get("metric_suite", "").strip()) < 80:
            issues.append("metric_suite_missing")
        if len(axis.get("risk_assumptions", "").strip()) < 100:
            issues.append("risk_assumptions_missing")
        if len(axis.get("two_week_sprint", "").strip()) < 80:
            issues.append("two_week_sprint_missing")
        shape = axis.get("contribution_shape", "").strip().lower().replace("-", "_").replace(" ", "_")
        if shape not in GENERALIZABLE_SHAPES:
            issues.append("contribution_shape_missing")
    return issues


RESCUEABLE_GATE_ISSUES = {
    "baseline_not_concrete",
    "falsification_not_concrete",
    "physical_failure_scene_missing_or_abstract",
    "non_physical_origin_not_grounded",
    "engineering_pathology_missing_or_abstract",
    "world_model_role_missing",
    "world_model_role_under_specified",
    "portfolio_failure_recovery_cap_exceeded",
    "non_obvious_claim_missing_or_weak",
    "naive_combination_version_missing",
    "strongest_baseline_kill_path_missing",
    "post_kill_mutation_missing",
    "active_viewpoint_missing_nbv_baseline",
    "interface_innovation_missing_or_shallow",
    "optimization_space_not_analyzed",
    "strongest_baseline_missing",
    "killer_experiment_missing",
    "falsification_does_not_separate_mechanism_from_patch",
    "lab_fit_missing",
    "negative_claim_boundary_missing",
    "core_insight_missing",
    "pipeline_steps_missing",
    "defense_patches_missing",
    "baseline_matrix_missing",
    "metric_suite_missing",
    "risk_assumptions_missing",
    "two_week_sprint_missing",
    "contribution_shape_missing",
}


def _is_rescueable_gate_failure(issues: list[str]) -> bool:
    return bool(issues) and all(issue in RESCUEABLE_GATE_ISSUES for issue in issues)


def _rescue_reason(issues: list[str]) -> str:
    if issues == ["baseline_not_concrete"]:
        return "needs_concrete_baseline_rescue"
    if issues == ["falsification_not_concrete"]:
        return "needs_concrete_falsification_rescue"
    if issues == ["non_obvious_claim_missing_or_weak"]:
        return "needs_non_obvious_claim_rescue"
    return "needs_concrete_baseline_and_falsification_rescue"


def _mechanism_candidates(records: list[dict[str, Any]], *, focus_keys: set[str]) -> list[tuple[int, dict[str, Any], list[dict[str, Any]], int]]:
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]] = []
    for spec in MECHANISM_SPECS:
        evidence = _mechanism_supporting(records, spec, focus_keys=focus_keys)
        if _source_count(evidence) < 3:
            continue
        recent = _recent_count(evidence, focus_keys)
        axis = _normalize_mechanism_axis(spec)
        strong_sources = _strong_source_count(evidence, spec)
        score = (
            strong_sources * 55
            + _source_count(evidence) * 6
            + recent * 18
            + int(spec.get("priority", 1)) * 30
            + _focus_track_bonus(spec)
            + len(axis["domains"]) * 2
        )
        if int(spec.get("priority", 1)) <= 1 and strong_sources < 4:
            score -= 80
        candidates.append((score, axis, evidence, recent))
    return sorted(candidates, key=lambda item: -item[0])


def _jsonable_candidate(axis: dict[str, Any], evidence: list[dict[str, Any]], recent: int, *, issues: list[str] | None = None) -> dict[str, Any]:
    spec = next((item for item in MECHANISM_SPECS if item["cluster_id"] == axis.get("cluster_id")), axis)
    return {
        "title": axis.get("title"),
        "cluster_id": axis.get("cluster_id"),
        "domains": axis.get("domains", []),
        "problem": axis.get("problem"),
        "engineering_pathology": axis.get("engineering_pathology"),
        "mechanism": axis.get("mechanism"),
        "interface": axis.get("interface"),
        "hypothesis": axis.get("hypothesis"),
        "evidence_links": axis.get("evidence_links"),
        "speculative_jump": axis.get("speculative_jump"),
        "origin_type": axis.get("origin_type"),
        "research_claim_type": axis.get("research_claim_type"),
        "bottleneck_type": axis.get("bottleneck_type"),
        "evidence_mode": axis.get("evidence_mode"),
        "risk_class": axis.get("risk_class"),
        "world_model_role": axis.get("world_model_role"),
        "portfolio_slot": axis.get("portfolio_slot"),
        "idea_archetype": axis.get("idea_archetype"),
        "contribution_shape": axis.get("contribution_shape"),
        "physical_failure_scene": axis.get("physical_failure_scene"),
        "non_obvious_claim": axis.get("non_obvious_claim"),
        "naive_combination_version": axis.get("naive_combination_version"),
        "strongest_baseline_kill_path": axis.get("strongest_baseline_kill_path"),
        "post_kill_mutation": axis.get("post_kill_mutation"),
        "anti_combination_test": axis.get("anti_combination_test"),
        "top_tier_rationale": axis.get("top_tier_rationale"),
        "engineering_loop": axis.get("engineering_loop"),
        "interface_innovation": axis.get("interface_innovation"),
        "optimization_space": axis.get("optimization_space"),
        "loss_placement": axis.get("loss_placement"),
        "decoder_boundary": axis.get("decoder_boundary"),
        "manifold_safety": axis.get("manifold_safety"),
        "method_improvement_claim": axis.get("method_improvement_claim"),
        "original_method_failure": axis.get("original_method_failure"),
        "replacement_or_coupled_technique": axis.get("replacement_or_coupled_technique"),
        "why_improvement_not_patch": axis.get("why_improvement_not_patch"),
        "why_now": axis.get("why_now"),
        "strongest_baseline": axis.get("strongest_baseline"),
        "baseline_failure_mode": axis.get("baseline_failure_mode"),
        "killer_experiment": axis.get("killer_experiment"),
        "novelty_risk": axis.get("novelty_risk"),
        "reviewer_kill_shot": axis.get("reviewer_kill_shot"),
        "rescue_mutation": axis.get("rescue_mutation"),
        "claim_compression": axis.get("claim_compression"),
        "online_or_offline_mode": axis.get("online_or_offline_mode"),
        "minimum_no_hardware_pilot": axis.get("minimum_no_hardware_pilot"),
        "baseline_kill_table": axis.get("baseline_kill_table"),
        "what_would_make_this_not_a_paper": axis.get("what_would_make_this_not_a_paper"),
        "reviewer_pre_mortem": axis.get("reviewer_pre_mortem"),
        "falsification_discriminates_mechanism": axis.get("falsification_discriminates_mechanism"),
        "lab_fit": axis.get("lab_fit"),
        "hardware_assumptions": axis.get("hardware_assumptions"),
        "negative_claim_boundary": axis.get("negative_claim_boundary"),
        "version_evolution_story": axis.get("version_evolution_story"),
        "core_insight": axis.get("core_insight"),
        "pipeline_steps": axis.get("pipeline_steps"),
        "defense_patches": axis.get("defense_patches"),
        "baseline_matrix": axis.get("baseline_matrix"),
        "metric_suite": axis.get("metric_suite"),
        "risk_assumptions": axis.get("risk_assumptions"),
        "competition_map": axis.get("competition_map"),
        "two_week_sprint": axis.get("two_week_sprint"),
        "quality_tier": axis.get("quality_tier"),
        "potential_score": axis.get("potential_score", axis.get("research_quality_score")),
        "potential_tier": axis.get("potential_tier", axis.get("quality_tier")),
        "quality_tier_semantics": axis.get("quality_tier_semantics", QUALITY_TIER_SEMANTICS),
        "readiness_tier": axis.get("readiness_tier", "untriaged"),
        "promotion_decision": axis.get("promotion_decision", "not_ready"),
        "candidate_group": axis.get("candidate_group"),
        "promotion_reason": axis.get("promotion_reason"),
        "rescue_signal": axis.get("rescue_signal"),
        "research_quality_score": axis.get("research_quality_score"),
        "research_quality_components": axis.get("research_quality_components", {}),
        "support_score": axis.get("support_score"),
        "originality_score": axis.get("originality_score"),
        "engineering_value_score": axis.get("engineering_value_score"),
        "sharpness_score": axis.get("sharpness_score"),
        "evidence_execution_score": axis.get("evidence_execution_score"),
        "ordinaryness_penalty": axis.get("ordinaryness_penalty"),
        "novelty_pressure": axis.get("novelty_pressure", {}),
        "novelty_hits": axis.get("novelty_hits", []),
        "evidence_support_score": axis.get("evidence_support_score"),
        "nearest_pressure": axis.get("nearest_pressure"),
        "pilot": axis.get("pilot"),
        "baselines": axis.get("baselines"),
        "metrics": axis.get("metrics"),
        "falsification": axis.get("falsification"),
        "evidence_sources": _source_count(evidence),
        "strong_mechanism_sources": _strong_source_count(evidence, spec),
        "recent_sources": recent,
        "issues": issues or [],
        "evidence": [
            {
                "source_note": record.get("source_note"),
                "source_title": record.get("source_title"),
                "claim_type": record.get("claim_type"),
                "statement": record.get("statement"),
                "focus_track_id": record.get("focus_track_id"),
            }
            for record in _dedupe_sources(evidence, limit=8)
        ],
    }


def _render_generation_prompt(candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]]) -> str:
    packet = {
        "task": "Rewrite local evidence clusters into 0-3 high-quality research idea candidates.",
        "rules": [
            "Return JSON only with key candidates.",
            "Use only local evidence in the packet.",
            "Do not create generic cross-gap titles.",
            "Each candidate needs title, problem, mechanism, interface, hypothesis, nearest_pressure, pilot, baselines, metrics, falsification.",
            "If no candidate is strong, return an empty candidates array.",
        ],
        "focus_track_context": _focus_track_context(),
        "clusters": [
            _jsonable_candidate(axis, evidence, recent)
            for _, axis, evidence, recent in candidates[:6]
        ],
    }
    return json.dumps(packet, ensure_ascii=False, indent=2)


def _record_packet(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_note": record.get("source_note"),
        "source_title": record.get("source_title"),
        "zotero_key": record.get("zotero_key"),
        "claim_type": record.get("claim_type"),
        "domains": record.get("domains", []),
        "statement": str(record.get("statement", ""))[:420],
        "evidence_section": record.get("evidence_section", ""),
        "source_snippet": str(record.get("source_snippet", ""))[:260],
        "source_snippet_type": record.get("source_snippet_type", ""),
        "evidence_anchor": record.get("evidence_anchor", ""),
        "extraction_confidence": record.get("extraction_confidence", ""),
    }


def _existing_seed_titles(*, max_titles: int = 80) -> list[str]:
    root = IDEA_BANK_DIR / "seed"
    if not root.exists():
        return []
    titles: list[str] = []
    for folder in sorted(root.iterdir(), key=lambda item: item.name):
        idea = folder / "idea.md"
        if not idea.exists():
            continue
        text = idea.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"^title:\s*\"?(.+?)\"?\s*$", text, flags=re.MULTILINE)
        titles.append(match.group(1).strip() if match else folder.name.replace("-", " "))
        if len(titles) >= max_titles:
            break
    return titles


def _existing_seed_pressure_items(*, max_items: int = 120) -> list[dict[str, str]]:
    root = IDEA_BANK_DIR / "seed"
    if not root.exists():
        return []
    items: list[dict[str, str]] = []
    for folder in sorted(root.iterdir(), key=lambda item: item.name):
        idea = folder / "idea.md"
        if not idea.exists():
            continue
        text = idea.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"^title:\s*\"?(.+?)\"?\s*$", text, flags=re.MULTILINE)
        title = match.group(1).strip() if match else folder.name.replace("-", " ")
        excerpt = " ".join(line.strip() for line in text.splitlines() if line.strip())[:900]
        items.append({"source": rel(idea), "title": title, "text": excerpt, "kind": "existing_seed"})
        if len(items) >= max_items:
            break
    return items


def _done_note_pressure_items(*, max_items: int = 180) -> list[dict[str, str]]:
    topics = vault_path("wiki", "topics")
    if not topics.exists():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(topics.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if 'status: "done"' not in text and "status: done" not in text:
            continue
        title_match = re.search(r"^title:\s*\"?(.+?)\"?\s*$", text, flags=re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        body = " ".join(line.strip() for line in text.splitlines() if line.strip())[:1000]
        items.append({"source": rel(path), "title": title, "text": body, "kind": "done_note"})
        if len(items) >= max_items:
            break
    return items


def _mirror_pressure_items(*, max_items: int = 220) -> list[dict[str, str]]:
    db_path = vault_path("projects", "arxiv-daily", "metadata", "arxiv_metadata.sqlite")
    if not db_path.exists():
        return []
    items: list[dict[str, str]] = []
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT arxiv_id, title, summary, primary_category, categories_json, published
                FROM papers
                ORDER BY published DESC
                LIMIT ?
                """,
                (max_items,),
            ).fetchall()
    except sqlite3.Error:
        return []
    for row in rows:
        title = str(row["title"] or "").strip()
        summary = str(row["summary"] or "").strip()
        source = f"arxiv:{row['arxiv_id']}"
        text = " ".join([title, summary, str(row["primary_category"] or ""), str(row["categories_json"] or "")])[:1000]
        items.append({"source": source, "title": title, "text": text, "kind": "arxiv_mirror"})
    return items


def _novelty_pressure_corpus() -> list[dict[str, str]]:
    return [
        *_existing_seed_pressure_items(),
        *_done_note_pressure_items(),
        *_mirror_pressure_items(),
    ]


def _novelty_pressure(axis: dict[str, Any], corpus: list[dict[str, str]]) -> dict[str, Any]:
    keywords = _quality_keywords(axis, max_keywords=16)
    if not keywords:
        return {"status": "not_checked", "reason": "no_candidate_keywords", "hits": [], "max_overlap": 0}
    title_norm = _normalize_text_for_overlap(str(axis.get("title", "")))
    hits: list[dict[str, Any]] = []
    for item in corpus:
        text = f"{item.get('title', '')} {item.get('text', '')}".lower()
        overlap = [keyword for keyword in keywords if keyword in text]
        if len(overlap) < 3:
            continue
        item_title_norm = _normalize_text_for_overlap(item.get("title", ""))
        title_overlap = bool(title_norm and item_title_norm and (title_norm in item_title_norm or item_title_norm in title_norm))
        score = len(overlap) + (4 if title_overlap else 0)
        hits.append(
            {
                "source": item.get("source", ""),
                "title": item.get("title", ""),
                "kind": item.get("kind", ""),
                "overlap_keywords": overlap[:8],
                "overlap_score": score,
            }
        )
    hits = sorted(hits, key=lambda item: -int(item.get("overlap_score", 0)))[:6]
    max_overlap = int(hits[0]["overlap_score"]) if hits else 0
    pressure = "high" if max_overlap >= 8 else ("medium" if max_overlap >= 5 else ("low" if hits else "none"))
    return {
        "status": "checked_local_only",
        "boundary": "novelty pressure is local and unverified; it is not a confirmed novelty search.",
        "pressure": pressure,
        "max_overlap": max_overlap,
        "hits": hits,
    }


def _normalize_text_for_overlap(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _top_domains(records: list[dict[str, Any]], *, limit: int = 5) -> list[str]:
    counts: Counter[str] = Counter()
    for record in records:
        for domain in record.get("domains", []):
            counts[str(domain)] += 1
    return [domain for domain, _ in counts.most_common(limit)]


def _sidecar_context(run_date: str) -> dict[str, Any]:
    concept_path = CONCEPT_DELTA_DIR / f"{run_date}-concept-delta.json"
    concepts: list[dict[str, Any]] = []
    if concept_path.exists():
        try:
            data = json.loads(concept_path.read_text(encoding="utf-8"))
            raw_concepts = data.get("concepts", [])
            if isinstance(raw_concepts, list):
                concepts = [
                    {
                        "label": item.get("label", ""),
                        "status": item.get("status", ""),
                        "focus_paper_count": item.get("focus_paper_count", 0),
                    }
                    for item in raw_concepts[:20]
                    if isinstance(item, dict)
                ]
        except (OSError, json.JSONDecodeError):
            concepts = []
    graph_dir = MECHANISM_GRAPH_DIR / run_date
    graph_files = sorted(graph_dir.glob("*.md")) if graph_dir.exists() else []
    graph_summaries: list[dict[str, str]] = []
    for path in graph_files[:12]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip().startswith(("problem[", "inputs[", "method[", "evaluation[", "metrics[", "limits["))
        ]
        graph_summaries.append({"path": rel(path), "graph_brief": " | ".join(lines)[:900]})
    return {
        "concept_delta_path": rel(concept_path) if concept_path.exists() else "",
        "mechanism_graph_dir": rel(graph_dir) if graph_dir.exists() else "",
        "concepts": concepts,
        "mechanism_graph_files": [rel(path) for path in graph_files[:20]],
        "mechanism_graph_briefs": graph_summaries,
        "boundary": "Concept deltas and mechanism graphs are draft sidecars for context compression, not formal claims.",
    }


def _render_divergent_prompt(
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]],
    *,
    records: list[dict[str, Any]],
    focus_keys: set[str],
    limit: int,
    min_candidates: int = DEFAULT_MIN_RAW_CANDIDATES,
    retry_context: str = "",
    free_divergence: bool = False,
    run_date: str | None = None,
) -> str:
    focus_records = [
        record
        for record in records
        if str(record.get("zotero_key", "")).upper() in focus_keys and not _is_source_availability_note(record)
    ]
    packet = {
        "task": "Generate top-tier-pressure-test robotics research idea seeds after today's deep reading.",
        "role": (
            "You are a severe robotics PhD advisor and invention partner. Your job is not to summarize papers. "
            "Your job is to find mechanisms that could become a top robotics conference/journal contribution, "
            "or a concrete engineering-system idea with a real closed-loop pathology."
        ),
        "output_schema": {
            "candidates": "Only surviving ideas after the internal adversarial survival filter.",
            "rejected_drafts_summary": "Optional short list of drafts killed before output. These are not candidates.",
            "source_filter_policy": "Low-quality drafts must be killed before candidates are emitted, not emitted with optimistic wording.",
        },
        "internal_survival_filter": [
            "Generate v0 naive drafts privately before final output. Do not put v0 drafts in candidates.",
            "For each v0 draft, run a death review: strongest baseline, reviewer kill shot, physical implausibility, lab mismatch, and what_would_make_this_not_a_paper.",
            "If the death review cannot be answered with a concrete mutation, move the draft to rejected_drafts_summary and do not output it as a candidate.",
            "Only output a candidate after it has a post_kill_mutation that changes a representation, optimization space, decoder/action boundary, controlled variable, feedback loop, evaluation signal, or deployment contract.",
            "If all drafts die, return fewer candidates or an empty candidates list. Do not fill the quota with polished weak ideas.",
        ],
        "rules": [
            "Return JSON only with key candidates.",
            "Top-level JSON may contain only candidates and rejected_drafts_summary.",
            f"Try to return {min_candidates}-{limit} surviving candidates, but survival quality overrides count. Return fewer candidates if the internal survival filter kills weak drafts.",
            "Each candidate needs exactly these fields: title, candidate_group, origin_type, research_claim_type, bottleneck_type, evidence_mode, risk_class, world_model_role, portfolio_slot, problem, physical_failure_scene, engineering_pathology, mechanism, interface, interface_innovation, optimization_space, loss_placement, decoder_boundary, manifold_safety, hypothesis, evidence_links, speculative_jump, idea_archetype, contribution_shape, non_obvious_claim, naive_combination_version, strongest_baseline_kill_path, post_kill_mutation, anti_combination_test, top_tier_rationale, engineering_loop, method_improvement_claim, original_method_failure, replacement_or_coupled_technique, why_improvement_not_patch, why_now, strongest_baseline, baseline_failure_mode, killer_experiment, novelty_risk, reviewer_kill_shot, rescue_mutation, claim_compression, online_or_offline_mode, minimum_no_hardware_pilot, baseline_kill_table, what_would_make_this_not_a_paper, reviewer_pre_mortem, falsification_discriminates_mechanism, lab_fit, hardware_assumptions, negative_claim_boundary, version_evolution_story, core_insight, pipeline_steps, defense_patches, baseline_matrix, metric_suite, risk_assumptions, competition_map, two_week_sprint, promotion_reason, rescue_signal, nearest_pressure, pilot, baselines, metrics, falsification.",
            "candidate_group must be either evidence_bound or wild_engineering.",
            "origin_type must be one of physical_scene, engineering_bottleneck, scientific_deadlock, representation_mismatch, objective_mismatch, evaluation_blind_spot, paper_assumption_contradiction.",
            "research_claim_type must be one of representation, interface_boundary, objective_optimization, data_curriculum, evaluation_benchmark, sensing_observability, world_model_simulation, embodiment_control_codesign, continual_transfer, safety_recovery.",
            "bottleneck_type must be one of partial_observability, contact_topology, action_multimodality, distribution_shift, evaluation_blindness, data_sparsity_bias, latency_real_time, irreversibility_safety, objective_mismatch, system_boundary_mismatch.",
            "evidence_mode must be one of offline_replay, simulation, public_dataset, small_real_robot_test, human_study_teleop, synthetic_benchmark, negative_result_diagnostic.",
            "risk_class must be one of grounded, mechanism, breakthrough. world_model_role must be none unless research_claim_type is world_model_simulation.",
            "Generate both groups: about half evidence_bound candidates tightly grounded in today's papers, and about half wild_engineering candidates that make a larger engineering, architecture, control-interface, or evaluation leap while still naming evidence and falsification.",
            "Before generating candidates, privately extract paper-level research primitives: central claim, hidden assumption, strongest baseline, unmodeled latent variable, evaluation blind spot, interface boundary, transfer failure, reusable primitive. Do not output this primitive table unless it is embedded compactly in candidate fields.",
            "Before final candidates, privately build a tension map: assumption conflicts, evaluation gaps, missing latent variables, interface boundary mismatches, strong baselines that kill naive drafts, benchmark opportunities, representation/action-abstraction opportunities, and anti-roadmap bets.",
            "Generate 16 private drafts across grounded, mechanism, measurement/data, world-model, transfer/embodiment, and breakthrough passes, then output only the best 6-8 as a balanced portfolio.",
            "Treat the daily set as a research portfolio, not a single theme. Target this mix: 2 grounded engineering ideas, 2 mechanism ideas, 1 measurement/data idea, 1 world-model idea, 1 transfer/embodiment idea, and 1 breakthrough/anti-roadmap bet. Overlap is allowed, but portfolio_slot must say the primary slot.",
            "Hard cap: no more than 2 candidates may start from visible physical failure/recovery. At least 3 candidates must use origin_type scientific_deadlock, representation_mismatch, objective_mismatch, evaluation_blind_spot, or paper_assumption_contradiction.",
            "A breakthrough bet is high-risk and high-upside: it should change a representation, memory/world-model abstraction, planning interface, optimization objective, dataset/evaluation paradigm, or robot-system contract. It must not be just another safety shield, failure detector, or recovery trigger.",
            "Think in this order: concrete robot episode or experimental bottleneck -> causal mechanism/interface -> why obvious baselines fail -> killer experiment -> only then title.",
            "Before writing the final mechanism, do an adversarial generation protocol inside each candidate: naive_combination_version -> strongest_baseline_kill_path -> post_kill_mutation. The final mechanism must be the post-kill mutation, not the naive A+B version.",
            "Use cross-cluster recombination, engineering-system imagination, and mechanism-level reasoning. You may make a speculative jump if you label it explicitly and make it testable.",
            "Use real robotics pathologies such as occlusion, latency, contact instability, calibration drift, depth noise, viewpoint failure, reset cost, and sim-to-real mismatch as grounding, but also deliberately explore non-recovery contributions: memory composition, planning abstraction, representation learning, loss placement, dataset design, benchmark design, and evaluation metrics.",
            "For evidence_bound candidates, connect at least two newly_read_evidence sources with local evidence from the matrix clusters.",
            "For wild_engineering candidates, at least one newly_read_evidence source is enough if the engineering_pathology is sharp and the speculative_jump is explicit.",
            "At least two wild_engineering candidates should deliberately avoid RL Token / VLA / Sim-to-Real unless those topics are truly central in today's evidence.",
            "Use examples like active sensing with a wrist camera, bimanual viewpoint servoing, tactile topology recovery, wrench envelopes, latent force recovery, or hidden-stiffness evaluation only as inspiration; do not copy them.",
            "For any active-viewpoint, active-vision, wrist-camera orbit, or view servo idea, the strongest baseline is usually classical next-best-view, information gain, occupancy/geometry-driven active vision, or a simple depth-discontinuity heuristic; do not use end-to-end RL active vision as the strongest baseline unless those classical baselines are explicitly inapplicable.",
            "Do not produce 'add module X to model Y', 'combine A with B', 'use LLM to reason over Z', or 'stack SOTA methods' unless the anti_combination_test explains the new causal interface that makes it nontrivial.",
            "Do not start from 'paper A has method X, paper B has interface Y'. Start from a robot episode, experimental bottleneck, or scientific deadlock first; only then decide which papers provide tools or pressure.",
            "For RL-token candidates, do not assume the token space supports prediction, planning, memory, or correction. First state what information is preserved, what is compressed away, and how errors or off-manifold deltas would be detected.",
            "The physical_failure_scene field must describe a concrete robot episode in physical terms: sensors, object, contact/occlusion/latency/noise, timing or geometry, and how the robot actually fails or where the experimental bottleneck appears. For breakthrough candidates, this may be a concrete limitation in memory, planning, representation, data, or evaluation, not necessarily a terminal safety failure.",
            "The engineering_pathology field must name the concrete robot-system failure, bottleneck, measurement gap, scaling limit, or evaluation deadlock that makes the idea worth testing.",
            "If origin_type is not physical_scene, physical_failure_scene must still describe the concrete experimental bottleneck, scientific deadlock, representation mismatch, objective mismatch, evaluation blind spot, or paper-assumption contradiction. Do not invent a visible robot failure just to fill the field.",
            "World-model candidates are legal only when world_model_role is one of counterfactual_evaluator, latent_state_teacher, planning_critic_or_shield, data_generator_or_curriculum, digital_twin_calibration_loop, or evaluation_surrogate. They must state predicted state, physical invariant, decision boundary, hallucination test, strongest baseline kill, no-hardware pilot, and minimal real-world test.",
            "The interface_innovation field must say what changes at the VLA/RL-token/control interface. A new input, residual, or module is insufficient unless the boundary, information flow, and controlled variable are changed.",
            "The optimization_space field must choose where learning/control happens: latent/token/action/observation/critic/evaluation space, and why that space is the right one.",
            "The loss_placement field must say where the objective is applied and what it avoids; for RL-token ideas, discuss whether the loss is pre-decoder, post-decoder, critic-only, actor-side, or latent-to-latent.",
            "The decoder_boundary field must say whether the mechanism crosses the VLA/RL-token decoder/action-head boundary, and why crossing or not crossing it matters.",
            "The manifold_safety field must state how the idea avoids pushing latent/token states off-manifold or breaking the pretrained VLA motion prior.",
            "The idea_archetype field must be one of method_improvement, interface_invention, failure_model, evaluation_metric, closed_loop_system, data_or_labeling_strategy, representation_shift, control_policy_mechanism, instrumentation_or_sensing.",
            "The contribution_shape field must be one of architecture, algorithm, control_interface, mechanism, system, method_improvement, evaluation_protocol, benchmark, failure_model, or dataset.",
            "The non_obvious_claim field must explain why this is not a simple combination or wrapper around known components.",
            "The naive_combination_version field must state the bad A+B version plainly, for example 'put pruning module X before planner Y' or 'add tactile signal Z to critic Q'.",
            "The strongest_baseline_kill_path field must explain exactly how a ruthless baseline could kill the naive version; name the real strongest baseline, not a weak strawman.",
            "The post_kill_mutation field must state the decisive mutation after the baseline kills the naive idea: change representation, boundary, feedback loop, controlled variable, loss placement, evaluation signal, or commit/release gate.",
            "The anti_combination_test field must answer: if a skeptical reviewer says this is just A+B, what is the precise mechanism or experiment that proves otherwise?",
            "The top_tier_rationale field must say which contribution shape could survive an RSS/CoRL/ICRA/RA-L style review and what would still make it fail.",
            "The engineering_loop field must describe the sense-plan-act-learn/evaluate loop or robot-system loop affected by the idea.",
            "For breakthrough candidates, top_tier_rationale must explicitly say why the idea could open a new research line rather than merely improve reliability; reviewer_pre_mortem must still be ruthless.",
            "For method_improvement candidates, method_improvement_claim must state the original method being improved, original_method_failure must name the failure mechanism, replacement_or_coupled_technique must state the new technique or coupling, and why_improvement_not_patch must explain why this is not a trivial engineering patch.",
            "Do not reject a candidate merely because it improves an existing method. Method improvement can be strong if it changes a failure mechanism, interface, constraint, feedback loop, or evaluation signal under a ruthless baseline.",
            "The strongest_baseline field must name the baseline most likely to kill the idea.",
            "The baseline_failure_mode field must explain why the strongest baseline should fail, or admit that the candidate should be rewritten if it probably will not fail.",
            "The killer_experiment field must name the smallest test that could decisively upgrade, rewrite, or kill the idea.",
            "The novelty_risk field must name the closest likely prior-work overlap; do not claim confirmed novelty.",
            "The reviewer_kill_shot field must name the strongest skeptical reviewer objection that could reject the idea.",
            "The rescue_mutation field must explain how to mutate the idea if the strongest baseline kills the first version.",
            "The claim_compression field must compress the idea into one falsifiable paper-claim sentence; avoid vague 'we combine' language.",
            "The online_or_offline_mode field must choose online_control, offline_replay, benchmark, dataset, analysis_tool, or hybrid, and explain why this mode is the right first version.",
            "The minimum_no_hardware_pilot field must state the first no-real-robot test using logs, existing datasets, ablations, toy dynamics, or paper-derived examples. Do not require new robot experiments for the first pilot.",
            "The baseline_kill_table field must be a compact semicolon-separated table: baseline -> how it could kill us -> what measurement would show we survive.",
            "The what_would_make_this_not_a_paper field must name the condition under which the idea collapses into an engineering patch or simple combination.",
            "The reviewer_pre_mortem field must first try to reject the candidate. If the pre-mortem kills the core claim, mark promotion_reason as rewrite_needed rather than seed-worthy.",
            "The falsification_discriminates_mechanism field must explain how the test distinguishes a real mechanism from a mere engineering patch. It is not enough to say one network beats another.",
            "The lab_fit field must explicitly say whether the idea uses this lab's likely advantages: Franka-quality arms, bimanual manipulation, wrist cameras/active viewpoints, FlexiTac/tactile sensing, DLO/cable tasks, and local offline logs. If it mainly needs low-cost hardware or large-fleet resources, mark it weak or rewrite.",
            "The hardware_assumptions field must list required robot, sensors, compute, dataset/logs, and whether each is available, substitutable, or unavailable.",
            "Use the HapToken-v3 style as a structural reference, not as content to copy: an excellent seed has problem pathology, negative claim boundary, core insight, executable pipeline, defensive patches, baseline matrix, metric suite, risk assumptions, competition map, and a short sprint plan.",
            "The negative_claim_boundary field must say what the idea does NOT claim, so it does not overclaim architecture novelty, end-to-end training, hardware availability, or confirmed results.",
            "The version_evolution_story field must explain the failed earlier versions or naive alternatives and the decisive turn that creates the current mechanism. If there is no evolution, state the obvious naive solution and why it fails.",
            "The version_evolution_story must include a compact v0/v1/v2-style death table in prose: naive version -> why it dies -> mutated version -> what changed in optimization space, decoder boundary, representation, or feedback loop.",
            "The core_insight field must name the one insight that breaks the deadlock, like replacing an impossible oracle target with black-box RL or moving correction from action space to latent space.",
            "The pipeline_steps field must outline a runnable training/inference/evaluation pipeline with 4-8 ordered steps. It may be pseudocode-like but must not be vague prose.",
            "The defense_patches field must list concrete failure-prevention patches, for example zero initialization, bounded delta, asymmetric gating, privileged critic, manifold tests, dead-zone penalties, or fallback controls when relevant.",
            "The baseline_matrix field must list at least 5 controls or baselines, including a lower bound, strongest direct baseline, simple heuristic, ablation without the proposed mechanism, and upper/oracle bound when possible.",
            "The metric_suite field must list measurable metrics beyond success rate, including latency/smoothness/calibration/risk/manifold or failure-mode metrics when relevant.",
            "The risk_assumptions field must list falsifiable assumptions and what to do if each fails.",
            "The competition_map field must name nearby work classes and the exact mechanism gap, not just paper names.",
            "The two_week_sprint field must list the first 3-6 work packages and identify the day-1 or day-3 kill test.",
            "The promotion_reason field must explain why this deserves seed status if it does; otherwise name what needs rewriting.",
            "The rescue_signal field must preserve the useful engineering pathology, interface, or experiment even if the idea is too risky today.",
            "The evidence_links field must list the local source titles or note IDs that directly inspired the candidate.",
            "The speculative_jump field must explain what is not yet proven by the evidence, so review can preserve risky but creative ideas.",
            "The baselines field must list concrete experimental controls separated by semicolons, for example: strongest local method; ablation without the proposed mechanism; simple rule-based baseline.",
            "The falsification field must start with Reject if ... and name a measurable condition that would narrow or reject the seed.",
            "Avoid duplicating existing_seed_titles; if the idea is only a rename of an existing seed, return fewer candidates.",
            "Use rejected_drafts_summary for killed drafts. Each rejected draft can contain draft_title, failure_reason, strongest_baseline, mutation_attempted, and why_not_candidate. Never include full weak drafts there.",
            "Keep candidates as seed hypotheses, not confirmed claims.",
            "If the evidence does not support a strong seed, return {\"candidates\": []}.",
        ],
        "workflow_contracts": {
            "gemini_greenhouse": WORKFLOW_CONTRACTS["gemini_greenhouse"],
            "idea_quality_source_basis": WORKFLOW_CONTRACTS["idea_quality_source_basis"],
            "idea_taxonomy": WORKFLOW_CONTRACTS["idea_taxonomy"],
            "daily_readable_workflow": WORKFLOW_CONTRACTS["daily_readable_workflow"],
            "provider_matrix": WORKFLOW_CONTRACTS["provider_matrix"],
        },
        "notemd_inspired_context": {
            "source_snippet_policy": "Use source_snippet and evidence_anchor as compact local evidence, not as quoted paper text.",
            "mechanism_graph_policy": "Daily mechanism graphs are draft_understanding_graph sidecars; use them only as structure compression when present in the agenda delta.",
            "concept_delta_policy": "Concept deltas show local concept pressure and missing concept pages; they are not novelty proof.",
        },
        "free_divergence_policy": {
            "enabled": free_divergence,
            "boundary": "From 2026-05-08 onward, do not force candidates toward RL Token or Sim-to-Real unless today's evidence actually supports it.",
            "instruction": "Use focus tracks as optional background only. They must not dominate candidate selection. Prefer the strongest engineering pathology over historical user curiosity.",
        },
        "quality_target": {
            "bar": "doctoral research seed, not daily idea dump",
            "reject_simple_combinations": True,
            "prefer": [
                "research_claim_type diversity over topic-name diversity",
                "ideas that change representation, interface, objective, metric, data distribution, or system boundary",
                "new causal mechanism",
                "new control or sensing interface",
                "1-2 high-risk breakthrough bets that could open a research line",
                "portfolio diversity across representation, memory/world-models, planning, objectives, evaluation, and engineering systems",
                "new evaluation protocol that exposes hidden failure",
                "method improvement that changes a failure mechanism or interface",
                "engineering pathology with a closed-loop system fix",
                "small killer experiment with a ruthless baseline",
                "one-sentence claim that is falsifiable and not a vague combination",
                "offline or no-hardware pilot before expensive robot validation",
                "pre-mortem that tries to reject the idea before assigning S/A",
                "explicit optimization-space choice: latent/token/action/critic/evaluation",
                "lab-fit advantage using Franka, bimanual setup, wrist cameras, FlexiTac, or DLO/cable tasks",
            ],
            "avoid": [
                "failure/recovery mode collapse",
                "visible physical failure as the origin for every candidate",
                "incremental loss addition",
                "parameter tweak without a failure mechanism",
                "generic VLA/RL-token framing",
                "LLM reasoner as a magic box",
                "benchmark without a new failure metric",
                "world model future prediction without latent state, invariant, decision boundary, and hallucination test",
                "idea that cannot be killed by a pilot",
                "online robot system when an offline replay, benchmark, or analysis-tool version is the correct first paper",
                "S/A tier assignment when the strongest reviewer objection already kills the paper claim",
                "resource-mismatched idea that needs low-cost hardware, humanoid fleets, or unavailable sensors while ignoring local Franka/FlexiTac/wrist-camera strengths",
            ],
        },
        "focus_track_context": "" if free_divergence else _focus_track_context(),
        "existing_seed_titles": _existing_seed_titles(),
        "retry_context": retry_context,
        "newly_read_evidence": [_record_packet(record) for record in _dedupe_sources(focus_records, limit=28)],
        "sidecar_context": _sidecar_context(run_date or today()),
        "matrix_clusters": [
            _jsonable_candidate(axis, evidence, recent)
            for _, axis, evidence, recent in candidates[:8]
        ],
    }
    return json.dumps(packet, ensure_ascii=False, indent=2)


def _render_quality_rescue_prompt(
    previous_prompt: str,
    previous_candidates: list[dict[str, Any]],
    *,
    raw_limit: int,
    min_raw_candidates: int,
) -> str:
    packet = json.loads(previous_prompt)
    packet["task"] = "Rescue low-quality automated Gemini ideation by doing a stricter manual-style divergent pass."
    packet["quality_rescue_context"] = {
        "trigger": "The first automated pass produced no S/A-tier candidates after local rubric scoring.",
        "goal": "Do not polish weak candidates. Generate a new set with sharper engineering pathologies, stronger baselines, and more non-obvious mechanisms.",
        "previous_candidate_titles": [
            str(item.get("title", "")) for item in previous_candidates if isinstance(item, dict)
        ],
        "manual_style_reference": [
            "Start from a robot failure, experimental bottleneck, or scientific deadlock that would annoy an experimentalist.",
            "Use origin_type to prevent mode collapse: physical_scene is allowed, but representation_mismatch, objective_mismatch, evaluation_blind_spot, and paper_assumption_contradiction are equally valid origins.",
            "Classify every candidate by research_claim_type, bottleneck_type, evidence_mode, risk_class, and portfolio_slot before writing the title.",
            "Invent or alter the sensing/control/evaluation interface, not just the model name.",
            "Describe the concrete robot episode or bottleneck before naming any source paper.",
            "Choose the optimization space and loss placement before choosing the network module.",
            "For RL-token ideas, decide whether the signal enters latent/token/action/critic space and whether it crosses the decoder boundary.",
            "Reject A+B ideas unless the interface_innovation and falsification_discriminates_mechanism fields prove a new causal mechanism.",
            "For every candidate, first write the bad naive A+B version, then let the strongest baseline kill it, then mutate the mechanism. The final candidate must be the mutation.",
            "For active-viewpoint/wrist-camera ideas, include NBV, information gain, occupancy/geometric active vision, or depth-discontinuity heuristics as the baseline pressure before claiming novelty.",
            "Use the local lab advantage: Franka arms, bimanual setup, wrist camera viewpoint control, FlexiTac/tactile sensing, and DLO/cable tasks.",
            "Use HapToken-v3 style as structure: negative boundary, core insight, runnable pipeline, defense patches, baseline matrix, metric suite, risks, competition map, and two-week sprint.",
            "Add a v0/v1/v2-style death table inside version_evolution_story: each row must say what failed and which boundary, space, representation, or feedback loop changed in the surviving version.",
            "Name the strongest baseline that could kill the idea.",
            "Try to reject the idea before giving it S/A; if the objection wins, rewrite instead of promoting.",
            "Prefer the first no-hardware pilot that can separate mechanism from engineering polish.",
            "Choose online_control only when online execution is the actual contribution; otherwise use offline_replay, benchmark, dataset, or analysis_tool.",
            "Compress the claim into one falsifiable sentence.",
            "Keep risky ideas alive via rescue_mutation instead of deleting them.",
            "World-model ideas must state their role, predicted state, physical invariant, decision boundary, and hallucination test; otherwise kill or rewrite them.",
        ],
    }
    packet["rules"] = [
        rule
        for rule in packet.get("rules", [])
        if "If the evidence does not support a strong seed" not in str(rule)
    ]
    packet["rules"].extend(
        [
            f"Return {min_raw_candidates}-{raw_limit} new candidates; do not repeat previous_candidate_titles.",
            "At least half should be wild_engineering unless the evidence truly forbids it.",
            "Keep the portfolio diverse: preserve 2-3 failure/recovery ideas if they are strong, but include 1-2 breakthrough bets that change representation, memory/world-model abstraction, planning interface, objective/loss placement, dataset design, or evaluation paradigm.",
            "Hard cap the rescue pass: at most 2 visible physical failure/recovery candidates; at least 3 candidates must originate from scientific deadlock, representation mismatch, objective mismatch, evaluation blind spot, or paper-assumption contradiction.",
            "A breakthrough bet must not be another failure detector or recovery shield with stronger language; it needs a different research object or contribution shape.",
            "Avoid the automatic-run failure mode: generic RL Token, generic VLA, generic Sim-to-Real, shallow module replacement, shallow extra-input critic, and simple A+B stacking.",
            "Avoid the newly observed failure mode: calling an uncertainty mask plus camera orbit an interface innovation while ignoring classical next-best-view and information-gain active vision.",
            "Do not assign S/A unless physical_failure_scene, interface_innovation, optimization_space, falsification_discriminates_mechanism, and lab_fit are all specific.",
            "Do not assign S/A unless baseline_matrix, risk_assumptions, and two_week_sprint are concrete enough for a researcher to start tomorrow.",
            "If you cannot make a top-tier candidate, still return raw rescue candidates with explicit reviewer_kill_shot and rescue_mutation so Codex can judge them.",
        ]
    )
    return json.dumps(packet, ensure_ascii=False, indent=2)


def _extract_json_object(text: str) -> dict[str, Any] | None:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def _refine_with_claude(
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]], *, timeout: int
) -> tuple[list[dict[str, Any]], str]:
    prompt = _render_generation_prompt(candidates)
    command = ["claude", "--dangerously-skip-permissions", "-p", prompt]
    try:
        proc = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True, timeout=timeout)
    except FileNotFoundError:
        return [], "failed:claude_cli_not_found"
    except subprocess.TimeoutExpired:
        return [], f"failed:claude_timeout:{timeout}"
    if proc.returncode != 0:
        return [], f"failed:claude_exit_{proc.returncode}"
    parsed = _extract_json_object(proc.stdout or "")
    if not parsed or not isinstance(parsed.get("candidates"), list):
        return [], "failed:claude_invalid_json"
    refined = [_normalize_mechanism_axis({**item, "generator_status": "claude"}) for item in parsed["candidates"] if isinstance(item, dict)]
    return refined, "claude:success"


def _refine_with_gemini_cli(
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]], *, timeout: int
) -> tuple[list[dict[str, Any]], str]:
    prompt = _render_generation_prompt(candidates)
    result = run_gemini_cli(prompt, timeout_sec=timeout)
    if result["error"]:
        return [], f"failed:gemini_cli:{result['error']}"
    parsed = _extract_json_object(result["clean_output"])
    if not parsed or not isinstance(parsed.get("candidates"), list):
        return [], "failed:gemini_cli_invalid_json"
    refined = [_normalize_mechanism_axis({**item, "generator_status": "gemini-cli"}) for item in parsed["candidates"] if isinstance(item, dict)]
    return refined, "gemini-cli:success"


def _score_divergent_evidence(record: dict[str, Any], axis: dict[str, Any], *, focus_keys: set[str]) -> int:
    if _is_source_availability_note(record):
        return -1
    keywords = _idea_keywords(axis)
    text = _record_text(record)
    keyword_hits = _keyword_hits(text, keywords)
    domain_hits = len(set(record.get("domains", [])).intersection(axis.get("domains", [])))
    if keyword_hits == 0 and domain_hits == 0:
        return -1
    score = keyword_hits * 14 + domain_hits * 10
    if str(record.get("zotero_key", "")).upper() in focus_keys:
        score += 45
    if record.get("claim_type") in STRONG_CLAIM_TYPES:
        score += 12
    elif record.get("claim_type") in SUPPORT_CLAIM_TYPES:
        score += 6
    return score


def _divergent_supporting(records: list[dict[str, Any]], axis: dict[str, Any], *, focus_keys: set[str]) -> list[dict[str, Any]]:
    ranked_focus: list[tuple[int, dict[str, Any]]] = []
    ranked_global: list[tuple[int, dict[str, Any]]] = []
    for record in records:
        score = _score_divergent_evidence(record, axis, focus_keys=focus_keys)
        if score < 0:
            continue
        if str(record.get("zotero_key", "")).upper() in focus_keys:
            ranked_focus.append((score, record))
        else:
            ranked_global.append((score, record))
    focus = _dedupe_sources([record for _, record in sorted(ranked_focus, key=lambda item: -item[0])], limit=5)
    global_records = _dedupe_sources([record for _, record in sorted(ranked_global, key=lambda item: -item[0])], limit=max(0, 12 - len(focus)))
    return _dedupe_sources([*focus, *global_records], limit=12)


def _normalize_divergent_axis(item: dict[str, Any], *, fallback_domains: list[str]) -> dict[str, Any]:
    text = " ".join(str(item.get(field, "")) for field in [*DIVERGENT_REQUIRED_FIELDS, *DIVERGENT_QUALITY_FIELDS])
    candidate_group = str(item.get("candidate_group", "")).strip().lower().replace("-", "_").replace(" ", "_")
    if candidate_group not in {"evidence_bound", "wild_engineering"}:
        candidate_group = "evidence_bound"
    normalized_item = {
        **item,
        "idea_archetype": _normalize_idea_archetype(item),
    }
    axis = {
        **normalized_item,
        "candidate_group": candidate_group,
        "generation_rule": "gemini_divergent",
        "generator_status": "gemini-divergent",
        "cluster_id": f"gemini-divergent-{slugify(str(item.get('title', 'seed')))}",
        "domains": _as_string_list(item.get("domains")) or fallback_domains,
        "keywords": _as_string_list(item.get("keywords")) or _text_keywords(text),
        "strong_keywords": _as_string_list(item.get("strong_keywords")) or _text_keywords(text, max_keywords=10),
        "min_strong_sources": 2,
        "status_boundary": "Gemini-divergent seed for user review only; no automatic promotion or paper claim is allowed.",
    }
    return _normalize_mechanism_axis(axis)


def _greenhouse_label(issues: list[str], promoted: bool, parked_reason: str = "") -> str:
    if promoted:
        return "promoted_to_seed"
    if not issues and parked_reason == "daily_high_quality_limit":
        return "parked_for_weekly_review"
    if _is_rescueable_gate_failure(issues):
        return "rewrite_needed"
    return "blocked_with_rescue_signal" if issues else "parked_for_weekly_review"


def _bounded_component(raw: int, weight: int) -> int:
    return max(0, min(weight, raw))


def _component_from_markers(text: str, markers: list[str], weight: int, *, min_hits_for_full: int = 3) -> int:
    lowered = text.lower()
    hits = sum(1 for marker in markers if marker in lowered)
    if hits <= 0:
        return 0
    return _bounded_component(round(weight * min(hits, min_hits_for_full) / min_hits_for_full), weight)


def _evidence_component(evidence: list[dict[str, Any]], recent: int, axis: dict[str, Any]) -> int:
    sources = _source_count(evidence)
    strong = _strong_source_count(evidence, axis)
    raw = 0
    if sources >= 2:
        raw += 2
    if sources >= 5:
        raw += 1
    if strong >= 2:
        raw += 2
    if recent >= 2:
        raw += 1
    return min(QUALITY_RUBRIC_WEIGHTS["evidence_fit"], raw)


def _originality_component(axis: dict[str, Any], novelty: dict[str, Any]) -> int:
    weight = QUALITY_RUBRIC_WEIGHTS["originality"]
    text = " ".join(
        str(axis.get(field, ""))
        for field in [
            "candidate_group",
            "idea_archetype",
            "physical_failure_scene",
            "non_obvious_claim",
            "anti_combination_test",
            "top_tier_rationale",
            "engineering_loop",
            "interface_innovation",
            "optimization_space",
            "loss_placement",
            "decoder_boundary",
            "manifold_safety",
            "method_improvement_claim",
            "original_method_failure",
            "replacement_or_coupled_technique",
            "why_improvement_not_patch",
            "speculative_jump",
            "mechanism",
            "interface",
            "strongest_baseline",
            "baseline_failure_mode",
            "killer_experiment",
            "reviewer_kill_shot",
            "rescue_mutation",
            "claim_compression",
            "online_or_offline_mode",
            "minimum_no_hardware_pilot",
            "baseline_kill_table",
            "what_would_make_this_not_a_paper",
            "reviewer_pre_mortem",
            "falsification_discriminates_mechanism",
            "lab_fit",
            "hardware_assumptions",
            "negative_claim_boundary",
            "version_evolution_story",
            "core_insight",
            "pipeline_steps",
            "defense_patches",
            "baseline_matrix",
            "metric_suite",
            "risk_assumptions",
            "competition_map",
            "two_week_sprint",
        ]
    ).lower()
    score = 0
    if str(axis.get("candidate_group", "")) == "wild_engineering":
        score += 4
    if len(str(axis.get("non_obvious_claim", "")).strip()) >= 80:
        score += 4
    if len(str(axis.get("speculative_jump", "")).strip()) >= 60:
        score += 3
    if len(str(axis.get("anti_combination_test", "")).strip()) >= 80:
        score += 3
    if len(str(axis.get("top_tier_rationale", "")).strip()) >= 80:
        score += 2
    if len(str(axis.get("reviewer_kill_shot", "")).strip()) >= 60:
        score += 2
    if len(str(axis.get("claim_compression", "")).strip()) >= 50:
        score += 2
    if len(str(axis.get("physical_failure_scene", "")).strip()) >= 100:
        score += 2
    if len(str(axis.get("interface_innovation", "")).strip()) >= 80:
        score += 2
    if len(str(axis.get("falsification_discriminates_mechanism", "")).strip()) >= 80:
        score += 2
    if len(str(axis.get("lab_fit", "")).strip()) >= 70:
        score += 1
    if len(str(axis.get("negative_claim_boundary", "")).strip()) >= 80:
        score += 1
    if len(str(axis.get("core_insight", "")).strip()) >= 70:
        score += 2
    if len(str(axis.get("pipeline_steps", "")).strip()) >= 120:
        score += 2
    if len(str(axis.get("defense_patches", "")).strip()) >= 80:
        score += 2
    if len(str(axis.get("baseline_matrix", "")).strip()) >= 120:
        score += 2
    if len(str(axis.get("risk_assumptions", "")).strip()) >= 100:
        score += 2
    if str(axis.get("contribution_shape", "")).strip().lower().replace("-", "_").replace(" ", "_") == "method_improvement":
        if len(str(axis.get("method_improvement_claim", "")).strip()) >= 60:
            score += 2
        if len(str(axis.get("why_improvement_not_patch", "")).strip()) >= 70:
            score += 2
    if any(marker in text for marker in ["instead of", "rather than", "not just", "before", "because", "unlike"]):
        score += 3
    if str(novelty.get("pressure", "")) == "low":
        score += 2
    return min(weight, score)


def _field_depth_score(axis: dict[str, Any], checks: list[tuple[str, int, int]], weight: int) -> int:
    raw = 0
    for field, min_chars, points in checks:
        if len(str(axis.get(field, "")).strip()) >= min_chars:
            raw += points
    return min(weight, raw)


def _generalizable_component(axis: dict[str, Any]) -> int:
    weight = QUALITY_RUBRIC_WEIGHTS["generalizable_contribution"]
    shape = str(axis.get("contribution_shape", "")).strip().lower().replace("-", "_").replace(" ", "_")
    if shape in GENERALIZABLE_SHAPES:
        return weight
    text = f"{axis.get('mechanism', '')} {axis.get('interface', '')} {axis.get('hypothesis', '')}".lower()
    return _component_from_markers(text, ["interface", "architecture", "algorithm", "protocol", "state", "residual", "critic"], weight)


def _quality_tier(score: int) -> str:
    if score >= 82:
        return "S"
    if score >= 68:
        return "A"
    if score >= 52:
        return "B"
    return "C"


def _quality_label_from_tier(tier: str, issues: list[str], promoted: bool) -> str:
    if promoted:
        return "promoted_to_seed"
    if issues and _is_rescueable_gate_failure(issues):
        return "rewrite_needed"
    if issues:
        return "blocked_with_rescue_signal"
    if tier == "B":
        return "rewrite_needed"
    if tier == "C":
        return "blocked_with_rescue_signal"
    return "parked_for_weekly_review"


def _is_visible_failure_recovery_candidate(axis: dict[str, Any]) -> bool:
    text = _axis_text(axis)
    return (
        str(axis.get("origin_type", "")) == "physical_scene"
        and (
            str(axis.get("research_claim_type", "")) == "safety_recovery"
            or any(marker in text for marker in ["failure", "recovery", "shield", "irreversible", "unsafe"])
        )
    )


QUALITY_TIER_SEMANTICS = "potential_only_not_seed_readiness"


def _readiness_tier_from_label(label: str) -> str:
    if label == "promoted_to_seed":
        return "seed_ready"
    if label == "speculative_preserve":
        return "speculative_weekly_review"
    if label == "rewrite_needed":
        return "rewrite_required"
    if label == "parked_for_weekly_review":
        return "weekly_review"
    if label == "blocked_with_rescue_signal":
        return "rescue_only"
    return "untriaged"


def _promotion_decision_from_label(label: str) -> str:
    if label == "promoted_to_seed":
        return "promote_to_seed"
    if label == "speculative_preserve":
        return "preserve_for_weekly_breakthrough_review"
    if label == "rewrite_needed":
        return "rewrite_before_seed"
    if label == "parked_for_weekly_review":
        return "park_for_weekly_review"
    if label == "blocked_with_rescue_signal":
        return "rescue_signal_only"
    return "not_ready"


def _annotate_readiness(item: dict[str, Any], tier: str | None = None) -> dict[str, Any]:
    potential_tier = str(item.get("potential_tier") or tier or item.get("quality_tier") or "unrated")
    item["potential_tier"] = potential_tier
    item["potential_score"] = item.get("potential_score", item.get("research_quality_score", 0))
    item["quality_tier_semantics"] = QUALITY_TIER_SEMANTICS
    label = str(item.get("greenhouse_label", "unlabeled"))
    item["readiness_tier"] = _readiness_tier_from_label(label)
    item["promotion_decision"] = _promotion_decision_from_label(label)
    return item


def _quality_sort_key(item: tuple[int, dict[str, Any], list[dict[str, Any]], int]) -> tuple[int, int, int, int, int, int]:
    score, axis, evidence, recent = item
    return (
        int(axis.get("research_quality_score", 0)),
        int(axis.get("sharpness_score", 0)),
        int(axis.get("evidence_execution_score", 0)),
        _strong_source_count(evidence, axis),
        recent,
        score,
    )


def _sharpness_score(axis: dict[str, Any]) -> int:
    claim_type = str(axis.get("research_claim_type", ""))
    risk_class = str(axis.get("risk_class", ""))
    text = _axis_text(axis)
    score = 0
    if len(str(axis.get("claim_compression", "")).strip()) >= 50 or len(str(axis.get("non_obvious_claim", "")).strip()) >= 80:
        score += 4
    if claim_type in {"representation", "interface_boundary", "objective_optimization", "evaluation_benchmark", "world_model_simulation"}:
        score += 5
    elif claim_type in {"data_curriculum", "sensing_observability", "embodiment_control_codesign"}:
        score += 3
    if str(axis.get("origin_type", "")) in NON_FAILURE_ORIGIN_TYPES:
        score += 3
    if any(marker in text for marker in ["blind spot", "deadlock", "assumption", "boundary", "metric", "evaluation", "unmodeled"]):
        score += 1
    if risk_class == "breakthrough" or any(marker in text for marker in ["new research line", "field", "paradigm", "anti-roadmap"]):
        score += 4
    if len(str(axis.get("anti_combination_test", "")).strip()) >= 80 and len(str(axis.get("post_kill_mutation", "")).strip()) >= 80:
        score += 3
    return min(20, score)


def _evidence_execution_score(axis: dict[str, Any], evidence: list[dict[str, Any]], recent: int) -> int:
    score = 0
    if len(str(axis.get("strongest_baseline", "")).strip()) >= 35 or len(str(axis.get("strongest_baseline_kill_path", "")).strip()) >= 80:
        score += 4
    if len(str(axis.get("killer_experiment", "")).strip()) >= 60 or len(str(axis.get("falsification_discriminates_mechanism", "")).strip()) >= 80:
        score += 4
    if len(str(axis.get("minimum_no_hardware_pilot", "")).strip()) >= 60:
        score += 3
    if any(marker in str(axis.get("online_or_offline_mode", "")).lower() for marker in ["offline", "benchmark", "dataset", "analysis_tool", "hybrid"]):
        score += 1
    if len(str(axis.get("lab_fit", "")).strip()) >= 70 and len(str(axis.get("hardware_assumptions", "")).strip()) >= 50:
        score += 3
    if _source_count(evidence) >= 3:
        score += 2
    if recent >= 1:
        score += 1
    if len(str(axis.get("rescue_mutation", "")).strip()) >= 60 or len(str(axis.get("post_kill_mutation", "")).strip()) >= 80:
        score += 3
    return min(20, score)


def _ordinaryness_penalty(axis: dict[str, Any]) -> int:
    text = _axis_text(axis)
    penalty = 0
    if any(marker in text for marker in ["combine", "integrate", "plug", "add module", "wrapper"]) and len(str(axis.get("anti_combination_test", "")).strip()) < 100:
        penalty -= 5
    if str(axis.get("world_model_role", "none")) != "none":
        wm_support = " ".join(
            str(axis.get(field, ""))
            for field in ["mechanism", "interface_innovation", "killer_experiment", "what_would_make_this_not_a_paper"]
        ).lower()
        if not any(marker in wm_support for marker in ["latent", "invariant", "decision boundary", "hallucination", "critic", "teacher", "calibration"]):
            penalty -= 4
    if any(marker in text for marker in ["add tactile", "add camera", "add sensor"]) and "observability" not in text:
        penalty -= 4
    if str(axis.get("research_claim_type", "")) == "evaluation_benchmark" and not any(marker in text for marker in ["blind spot", "metric", "stress", "protocol"]):
        penalty -= 4
    if str(axis.get("research_claim_type", "")) == "safety_recovery" and not any(marker in text for marker in ["risk model", "control boundary", "contract", "irreversible"]):
        penalty -= 3
    if any(marker in text for marker in ["fine-tune vla", "finetune vla", "fine tune vla"]) and not any(marker in text for marker in ["objective", "interface", "distribution", "metric"]):
        penalty -= 5
    return max(-10, penalty)


def _apply_research_quality(
    axis: dict[str, Any],
    evidence: list[dict[str, Any]],
    recent: int,
    *,
    evidence_score: int,
    novelty_corpus: list[dict[str, str]],
) -> dict[str, Any]:
    novelty = _novelty_pressure(axis, novelty_corpus)
    pathology_text = str(axis.get("engineering_pathology", ""))
    physical_scene_text = str(axis.get("physical_failure_scene", ""))
    mechanism_text = " ".join(
        str(axis.get(field, ""))
        for field in [
            "mechanism",
            "interface",
            "interface_innovation",
            "optimization_space",
            "loss_placement",
            "decoder_boundary",
            "manifold_safety",
            "non_obvious_claim",
            "anti_combination_test",
            "top_tier_rationale",
            "engineering_loop",
            "method_improvement_claim",
            "original_method_failure",
            "replacement_or_coupled_technique",
            "why_improvement_not_patch",
            "reviewer_kill_shot",
            "rescue_mutation",
            "claim_compression",
            "speculative_jump",
            "falsification_discriminates_mechanism",
            "lab_fit",
            "negative_claim_boundary",
            "version_evolution_story",
            "core_insight",
            "pipeline_steps",
            "defense_patches",
            "baseline_matrix",
            "metric_suite",
            "risk_assumptions",
            "competition_map",
            "two_week_sprint",
        ]
    )
    baseline_text = " ".join(str(axis.get(field, "")) for field in ["baselines", "strongest_baseline", "baseline_failure_mode", "falsification", "falsification_discriminates_mechanism"])
    experiment_text = " ".join(
        str(axis.get(field, ""))
        for field in [
            "pilot",
            "minimum_no_hardware_pilot",
            "killer_experiment",
            "metrics",
            "baseline_failure_mode",
            "baseline_kill_table",
            "falsification",
        ]
    )
    mechanism_depth = _field_depth_score(
        axis,
        [
            ("mechanism", 70, 5),
            ("interface", 35, 4),
            ("interface_innovation", 80, 4),
            ("optimization_space", 70, 3),
            ("loss_placement", 55, 3),
            ("decoder_boundary", 55, 2),
            ("manifold_safety", 55, 2),
            ("non_obvious_claim", 90, 6),
            ("anti_combination_test", 80, 3),
            ("engineering_loop", 60, 2),
            ("method_improvement_claim", 60, 2),
            ("why_improvement_not_patch", 70, 2),
            ("reviewer_kill_shot", 60, 2),
            ("claim_compression", 50, 2),
            ("speculative_jump", 70, 3),
            ("strongest_baseline", 40, 2),
            ("minimum_no_hardware_pilot", 60, 2),
            ("baseline_kill_table", 70, 2),
            ("what_would_make_this_not_a_paper", 55, 2),
            ("reviewer_pre_mortem", 60, 2),
            ("falsification_discriminates_mechanism", 80, 3),
            ("lab_fit", 70, 1),
            ("negative_claim_boundary", 80, 2),
            ("core_insight", 70, 3),
            ("pipeline_steps", 120, 3),
            ("defense_patches", 80, 2),
            ("baseline_matrix", 120, 2),
            ("metric_suite", 80, 1),
            ("risk_assumptions", 100, 2),
            ("two_week_sprint", 80, 1),
        ],
        QUALITY_RUBRIC_WEIGHTS["mechanism_nonobviousness"],
    )
    components = {
        "mechanism_nonobviousness": min(
            QUALITY_RUBRIC_WEIGHTS["mechanism_nonobviousness"],
            round(
                0.7 * mechanism_depth
                + 0.3
                * _component_from_markers(
                    mechanism_text,
                    NON_OBVIOUS_MARKERS,
                    QUALITY_RUBRIC_WEIGHTS["mechanism_nonobviousness"],
                    min_hits_for_full=4,
                )
            ),
        ),
        "engineering_pathology": _component_from_markers(
            f"{physical_scene_text} {pathology_text}",
            ENGINEERING_PATHOLOGY_MARKERS,
            QUALITY_RUBRIC_WEIGHTS["engineering_pathology"],
            min_hits_for_full=3,
        ),
        "baseline_killer": _component_from_markers(
            baseline_text,
            BASELINE_KILLER_MARKERS,
            QUALITY_RUBRIC_WEIGHTS["baseline_killer"],
            min_hits_for_full=4,
        ),
        "originality": _originality_component(axis, novelty),
        "experimentability": _component_from_markers(
            experiment_text,
            EXPERIMENT_MARKERS,
            QUALITY_RUBRIC_WEIGHTS["experimentability"],
            min_hits_for_full=4,
        ),
        "generalizable_contribution": _generalizable_component(axis),
        "evidence_fit": _evidence_component(evidence, recent, axis),
    }
    text = " ".join(str(axis.get(field, "")) for field in [*DIVERGENT_REQUIRED_FIELDS, *DIVERGENT_QUALITY_FIELDS]).lower()
    if any(marker in text for marker in GENERIC_COMBINATION_MARKERS) and components["mechanism_nonobviousness"] < 10:
        components["mechanism_nonobviousness"] = max(0, components["mechanism_nonobviousness"] - 4)
    if len(str(axis.get("physical_failure_scene", "")).strip()) < 90:
        components["engineering_pathology"] = max(0, components["engineering_pathology"] - 6)
    if len(str(axis.get("interface_innovation", "")).strip()) < 70:
        components["mechanism_nonobviousness"] = max(0, components["mechanism_nonobviousness"] - 5)
    if len(
        " ".join(
            str(axis.get(field, "")).strip()
            for field in ["optimization_space", "loss_placement", "decoder_boundary", "manifold_safety"]
        )
    ) < 120:
        components["mechanism_nonobviousness"] = max(0, components["mechanism_nonobviousness"] - 4)
    if len(str(axis.get("reviewer_pre_mortem", "")).strip()) < 60:
        components["baseline_killer"] = max(0, components["baseline_killer"] - 2)
    if len(str(axis.get("falsification_discriminates_mechanism", "")).strip()) < 80:
        components["baseline_killer"] = max(0, components["baseline_killer"] - 4)
    lab_fit_text = str(axis.get("lab_fit", "")).lower()
    if not any(marker in lab_fit_text for marker in ["franka", "flextac", "wrist", "camera", "bimanual", "dlo", "cable", "lab"]):
        components["experimentability"] = max(0, components["experimentability"] - 3)
    if len(str(axis.get("minimum_no_hardware_pilot", "")).strip()) < 50:
        components["experimentability"] = max(0, components["experimentability"] - 2)
    support_score = min(100, evidence_score)
    originality_score = min(
        100,
        components["mechanism_nonobviousness"] * 3
        + components["originality"] * 3
        + components["generalizable_contribution"] * 2,
    )
    engineering_value_score = min(
        100,
        components["engineering_pathology"] * 3
        + components["baseline_killer"] * 2
        + components["experimentability"] * 3,
    )
    sharpness = _sharpness_score(axis)
    evidence_execution = _evidence_execution_score(axis, evidence, recent)
    ordinaryness = _ordinaryness_penalty(axis)
    quality_score = max(0, sum(components.values()) + ordinaryness)
    if str(axis.get("candidate_group", "")) == "wild_engineering":
        quality_score = min(100, quality_score + 4)
    if sharpness < 8:
        quality_score = min(quality_score, 81)
    if evidence_execution < 6 and sharpness >= 16:
        quality_score = min(quality_score, 67)
    tier = _quality_tier(quality_score)
    return {
        **axis,
        "evidence_support_score": evidence_score,
        "support_score": support_score,
        "originality_score": originality_score,
        "engineering_value_score": engineering_value_score,
        "sharpness_score": sharpness,
        "evidence_execution_score": evidence_execution,
        "ordinaryness_penalty": ordinaryness,
        "research_quality_score": quality_score,
        "research_quality_components": components,
        "quality_tier": tier,
        "potential_score": quality_score,
        "potential_tier": tier,
        "quality_tier_semantics": QUALITY_TIER_SEMANTICS,
        "readiness_tier": "untriaged",
        "promotion_decision": "not_ready",
        "novelty_pressure": {key: value for key, value in novelty.items() if key != "hits"},
        "novelty_hits": novelty.get("hits", []),
    }


def _refine_with_gemini_divergent(
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]],
    *,
    records: list[dict[str, Any]],
    focus_keys: set[str],
    timeout: int,
    limit: int,
    raw_limit: int,
    min_raw_candidates: int,
    gemini_model: str,
    free_divergence: bool,
    run_date: str,
) -> tuple[list[tuple[int, dict[str, Any], list[dict[str, Any]], int]], str, dict[str, Any]]:
    if not focus_keys:
        return [], "failed:gemini_divergent_requires_focus_keys", {}
    focus_records = [record for record in records if str(record.get("zotero_key", "")).upper() in focus_keys]
    if _source_count(focus_records) < 2:
        return [], f"failed:gemini_divergent_too_few_focus_sources:{_source_count(focus_records)}", {}
    prompt = _render_divergent_prompt(
        candidates,
        records=records,
        focus_keys=focus_keys,
        limit=max(1, raw_limit),
        min_candidates=min_raw_candidates,
        free_divergence=free_divergence,
        run_date=run_date,
    )
    result = run_gemini_cli(prompt, timeout_sec=timeout, model=gemini_model)
    generator_meta: dict[str, Any] = {
        "source_filter_policy": "candidates_only_include_survivors_after_internal_adversarial_filter",
        "rejected_drafts_summary": [],
    }
    model_suffix = (
        f":model={result.get('requested_model') or 'auto'}"
        f":effective={result.get('effective_model') or 'auto'}"
        f":fallback={str(bool(result.get('effective_fallback'))).lower()}"
    )
    if result["error"]:
        return [], f"failed:gemini_divergent:{result['error']}{model_suffix}", generator_meta
    parsed = _extract_json_object(result["clean_output"])
    if not parsed or not isinstance(parsed.get("candidates"), list):
        return [], f"failed:gemini_divergent_invalid_json{model_suffix}", generator_meta
    generator_meta["rejected_drafts_summary"] = _compact_rejected_drafts(parsed.get("rejected_drafts_summary"))
    raw_items = [item for item in parsed["candidates"] if isinstance(item, dict)]
    under_generated = len(raw_items) < min_raw_candidates
    retry_status = ""
    if under_generated and len(raw_items) > 0:
        retry_prompt = _render_divergent_prompt(
            candidates,
            records=records,
            focus_keys=focus_keys,
            limit=max(1, raw_limit),
            min_candidates=min_raw_candidates,
            free_divergence=free_divergence,
            run_date=run_date,
            retry_context=(
                f"First pass returned only {len(raw_items)} candidates. "
                "Generate additional non-duplicate high-variance candidates, especially mechanism-sharp or engineering-pathology ideas. "
                "Do not repeat these titles: "
                + "; ".join(str(item.get("title", "")) for item in raw_items)
            ),
        )
        retry = run_gemini_cli(retry_prompt, timeout_sec=timeout, model=gemini_model)
        retry_suffix = (
            f":retry_model={retry.get('requested_model') or 'auto'}"
            f":retry_effective={retry.get('effective_model') or 'auto'}"
            f":retry_fallback={str(bool(retry.get('effective_fallback'))).lower()}"
        )
        if retry.get("error"):
            retry_status = f":under_generated_warning:first={len(raw_items)}:retry_failed={retry['error']}{retry_suffix}"
        else:
            retry_parsed = _extract_json_object(retry.get("clean_output", ""))
            retry_items = retry_parsed.get("candidates", []) if isinstance(retry_parsed, dict) else []
            if isinstance(retry_parsed, dict):
                generator_meta.setdefault("retry_rejected_drafts_summary", [])
                generator_meta["retry_rejected_drafts_summary"] = _compact_rejected_drafts(
                    retry_parsed.get("rejected_drafts_summary")
                )
            seen_titles = {str(item.get("title", "")).strip().lower() for item in raw_items}
            added = 0
            for item in retry_items:
                if not isinstance(item, dict):
                    continue
                title = str(item.get("title", "")).strip().lower()
                if not title or title in seen_titles:
                    continue
                raw_items.append(item)
                seen_titles.add(title)
                added += 1
                if len(raw_items) >= raw_limit:
                    break
            retry_status = f":under_generated_warning:first={len(parsed['candidates'])}:retry_added={added}{retry_suffix}"
            under_generated = len(raw_items) < min_raw_candidates
    if not raw_items:
        return [], f"gemini-divergent:empty{model_suffix}", generator_meta

    fallback_domains = _top_domains(focus_records)
    novelty_corpus = _novelty_pressure_corpus()

    def score_raw_items(items: list[dict[str, Any]]) -> list[tuple[int, dict[str, Any], list[dict[str, Any]], int]]:
        scored: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]] = []
        for item in items[: max(1, raw_limit)]:
            if not isinstance(item, dict):
                continue
            axis = _normalize_divergent_axis(item, fallback_domains=fallback_domains)
            evidence = _divergent_supporting(records, axis, focus_keys=focus_keys)
            recent = _recent_count(evidence, focus_keys)
            evidence_score = (
                _strong_source_count(evidence, axis) * 55
                + _source_count(evidence) * 6
                + recent * 25
                + len(_idea_keywords(axis))
            )
            axis = _apply_research_quality(
                axis,
                evidence,
                recent,
                evidence_score=evidence_score,
                novelty_corpus=novelty_corpus,
            )
            scored.append((evidence_score, axis, evidence, recent))
        return scored

    refined = score_raw_items(raw_items)
    top_tier_count = sum(
        1 for _, axis, _, _ in refined if str(axis.get("quality_tier", "")) in QUALITY_PROMOTION_TIERS
    )
    if free_divergence and top_tier_count < MIN_TOP_TIER_RAW_CANDIDATES and raw_items:
        rescue_prompt = _render_quality_rescue_prompt(
            prompt,
            raw_items,
            raw_limit=raw_limit,
            min_raw_candidates=min_raw_candidates,
        )
        rescue = run_gemini_cli(rescue_prompt, timeout_sec=timeout, model=gemini_model)
        rescue_suffix = (
            f":quality_rescue_model={rescue.get('requested_model') or 'auto'}"
            f":quality_rescue_effective={rescue.get('effective_model') or 'auto'}"
            f":quality_rescue_fallback={str(bool(rescue.get('effective_fallback'))).lower()}"
        )
        if rescue.get("error"):
            retry_status += f":quality_rescue_failed={rescue['error']}{rescue_suffix}"
        else:
            rescue_parsed = _extract_json_object(rescue.get("clean_output", ""))
            rescue_items = rescue_parsed.get("candidates", []) if isinstance(rescue_parsed, dict) else []
            if isinstance(rescue_parsed, dict):
                generator_meta["quality_rescue_rejected_drafts_summary"] = _compact_rejected_drafts(
                    rescue_parsed.get("rejected_drafts_summary")
                )
            if isinstance(rescue_items, list) and rescue_items:
                seen_titles = {str(item.get("title", "")).strip().lower() for item in raw_items}
                added = 0
                for item in rescue_items:
                    if not isinstance(item, dict):
                        continue
                    title = str(item.get("title", "")).strip().lower()
                    if not title or title in seen_titles:
                        continue
                    raw_items.append(item)
                    seen_titles.add(title)
                    added += 1
                    if len(raw_items) >= raw_limit * 2:
                        break
                refined = score_raw_items(raw_items)
                top_tier_count = sum(
                    1
                    for _, axis, _, _ in refined
                    if str(axis.get("quality_tier", "")) in QUALITY_PROMOTION_TIERS
                )
                retry_status += (
                    f":quality_rescue_triggered:first_top_tier=0:rescue_added={added}:"
                    f"final_top_tier={top_tier_count}{rescue_suffix}"
                )
            else:
                retry_status += f":quality_rescue_invalid_json{rescue_suffix}"

    refined = score_raw_items(raw_items)
    suffix = retry_status
    if under_generated and not retry_status:
        suffix = f":under_generated_warning:raw={len(raw_items)}:min={min_raw_candidates}"
    if len(raw_items) < min_raw_candidates:
        suffix += f":source_filter_under_min_warning:survivors={len(raw_items)}:min={min_raw_candidates}"
    generator_meta["surviving_candidate_count"] = len(raw_items)
    generator_meta["source_rejected_draft_count"] = len(generator_meta.get("rejected_drafts_summary", []))
    return sorted(refined, key=_quality_sort_key, reverse=True), f"gemini-divergent:success{model_suffix}{suffix}", generator_meta


def generate_seed_report(
    records: list[dict[str, Any]],
    *,
    focus_keys: list[str],
    limit: int = 3,
    include_dynamic: bool = False,
    mode: str = "mechanism",
    generator: str = "template",
    generator_timeout: int = 1200,
    raw_candidate_limit: int = 8,
    min_raw_candidates: int = DEFAULT_MIN_RAW_CANDIDATES,
    gemini_model: str = "gemini-3.1-pro-preview",
    run_date: str | None = None,
) -> dict[str, Any]:
    records = _merge_focus_track_records(records)
    focus = {key.upper() for key in focus_keys}
    run_date = run_date or today()
    free_divergence = generator == "gemini-divergent" and run_date >= FREE_DIVERGENCE_START_DATE
    high_quality: list[tuple[dict[str, Any], list[dict[str, Any]], int]] = []
    parked: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    greenhouse: list[dict[str, Any]] = []
    generator_status = "not_run"
    generator_metadata: dict[str, Any] = {}

    def base_report(status: str) -> dict[str, Any]:
        return {
            "mode": mode,
            "generator": generator,
            "generator_status": status,
            "high_quality": [],
            "parked": [],
            "blocked": [{"title": "generator_failed", "issues": [status]}],
            "greenhouse": [],
            "raw_candidate_limit": raw_candidate_limit,
            "min_raw_candidates": min_raw_candidates,
            "quality_rubric_weights": QUALITY_RUBRIC_WEIGHTS,
            "workflow_contracts": WORKFLOW_CONTRACTS,
            "generator_metadata": {},
            "portfolio_summary": {},
            "free_divergence": free_divergence,
            "free_divergence_start_date": FREE_DIVERGENCE_START_DATE,
            "gemini_model": gemini_model,
            "no_high_quality_seed_today_reason": "generator_failed",
        }

    if mode == "curated":
        candidates = _curated_candidates(records, focus_keys=focus, include_dynamic=include_dynamic)
    else:
        candidates = _mechanism_candidates(records, focus_keys=focus)
        if generator == "claude" and candidates:
            refined, generator_status = _refine_with_claude(candidates, timeout=generator_timeout)
            if not refined:
                return base_report(generator_status)
            by_cluster = {axis.get("cluster_id"): (score, axis, evidence, recent) for score, axis, evidence, recent in candidates}
            candidates = []
            for axis in refined:
                original = by_cluster.get(axis.get("cluster_id"))
                if not original:
                    continue
                score, _, evidence, recent = original
                candidates.append((score, axis, evidence, recent))
        elif generator == "gemini-cli" and candidates:
            refined, generator_status = _refine_with_gemini_cli(candidates, timeout=generator_timeout)
            if not refined:
                return base_report(generator_status)
            by_cluster = {axis.get("cluster_id"): (score, axis, evidence, recent) for score, axis, evidence, recent in candidates}
            candidates = []
            for axis in refined:
                original = by_cluster.get(axis.get("cluster_id"))
                if not original:
                    continue
                score, _, evidence, recent = original
                candidates.append((score, axis, evidence, recent))
        elif generator == "gemini-divergent" and candidates:
            divergent, generator_status, generator_metadata = _refine_with_gemini_divergent(
                candidates,
                records=records,
                focus_keys=focus,
                timeout=generator_timeout,
                limit=limit,
                raw_limit=raw_candidate_limit,
                min_raw_candidates=min_raw_candidates,
                gemini_model=gemini_model,
                free_divergence=free_divergence,
                run_date=run_date,
            )
            if not divergent and generator_status.startswith("failed:"):
                return base_report(generator_status)
            candidates = divergent
        elif generator == "gemini-divergent":
            generator_status = "gemini-divergent:not_run_no_mechanism_candidates"
            candidates = []
        elif generator == "template":
            generator_status = "template:success"
        elif generator == "none":
            generator_status = "skipped:none"
            candidates = []
        else:
            generator_status = f"failed:unknown_generator:{generator}"
            candidates = []

    preserve_greenhouse = generator == "gemini-divergent"
    visible_failure_recovery_seen = 0
    for score, axis, evidence, recent in candidates:
        axis = _normalize_mechanism_axis(axis) if mode == "mechanism" else axis
        issues = _gate_mechanism_candidate(axis, evidence, recent, focus_keys=focus) if mode == "mechanism" else []
        if preserve_greenhouse and _is_visible_failure_recovery_candidate(axis):
            visible_failure_recovery_seen += 1
            if visible_failure_recovery_seen > 2:
                issues.append("portfolio_failure_recovery_cap_exceeded")
        item = _jsonable_candidate(axis, evidence, recent, issues=issues)
        item["score"] = score
        item["evidence_support_score"] = axis.get("evidence_support_score", score)
        tier = str(axis.get("quality_tier", "B" if generator != "gemini-divergent" else "C"))
        speculative_preserve = (
            preserve_greenhouse
            and int(axis.get("sharpness_score") or 0) >= 16
            and int(axis.get("evidence_execution_score") or 0) < 6
        )
        if issues:
            if speculative_preserve and all(
                issue.startswith("too_few_") or issue in {"no_recent_focus_evidence", "portfolio_failure_recovery_cap_exceeded"}
                for issue in issues
            ):
                item["park_reason"] = "speculative_preserve_high_sharpness_low_evidence"
                item["greenhouse_label"] = "speculative_preserve"
                _annotate_readiness(item, tier)
                if preserve_greenhouse:
                    greenhouse.append(item)
                parked.append(item)
                continue
            if _is_rescueable_gate_failure(issues):
                item["park_reason"] = _rescue_reason(issues)
                item["greenhouse_label"] = _quality_label_from_tier(tier, issues, promoted=False)
                _annotate_readiness(item, tier)
                if preserve_greenhouse:
                    greenhouse.append(item)
                parked.append(item)
                continue
            item["greenhouse_label"] = _quality_label_from_tier(tier, issues, promoted=False)
            _annotate_readiness(item, tier)
            if preserve_greenhouse:
                greenhouse.append(item)
            blocked.append(item)
            continue
        eligible_for_seed = generator != "gemini-divergent" or tier in QUALITY_PROMOTION_TIERS
        if preserve_greenhouse and int(axis.get("sharpness_score") or 0) < 8:
            eligible_for_seed = False
        if eligible_for_seed and len(high_quality) < limit:
            axis["greenhouse_label"] = _quality_label_from_tier(tier, [], promoted=True)
            _annotate_readiness(axis, tier)
            high_quality.append((axis, evidence, recent))
            item["greenhouse_label"] = _quality_label_from_tier(tier, [], promoted=True)
            _annotate_readiness(item, tier)
            if preserve_greenhouse:
                greenhouse.append(item)
        else:
            if speculative_preserve:
                item["park_reason"] = "speculative_preserve_high_sharpness_low_evidence"
                item["greenhouse_label"] = "speculative_preserve"
                _annotate_readiness(item, tier)
                if preserve_greenhouse:
                    greenhouse.append(item)
                parked.append(item)
                continue
            if not eligible_for_seed:
                item["park_reason"] = f"quality_tier_{tier}_not_promotable"
            else:
                item["park_reason"] = "daily_high_quality_limit"
            item["greenhouse_label"] = _quality_label_from_tier(tier, [], promoted=False)
            _annotate_readiness(item, tier)
            if preserve_greenhouse:
                greenhouse.append(item)
            parked.append(item)

    reason = ""
    if not high_quality:
        if generator == "none":
            reason = "idea_generation_disabled"
        elif preserve_greenhouse and greenhouse:
            reason = "no_top_tier_seed_today"
        else:
            reason = "no_candidate_passed_mechanism_gate" if blocked else "no_evidence_cluster_met_minimum_threshold"
    portfolio_summary = _portfolio_summary(greenhouse)
    return {
        "mode": mode,
        "generator": generator,
        "generator_status": generator_status,
        "high_quality": high_quality,
        "parked": parked,
        "blocked": blocked,
        "greenhouse": greenhouse,
        "raw_candidate_limit": raw_candidate_limit,
        "min_raw_candidates": min_raw_candidates,
        "quality_rubric_weights": QUALITY_RUBRIC_WEIGHTS,
        "workflow_contracts": WORKFLOW_CONTRACTS,
        "generator_metadata": generator_metadata,
        "portfolio_summary": portfolio_summary,
        "free_divergence": free_divergence,
        "free_divergence_start_date": FREE_DIVERGENCE_START_DATE,
        "gemini_model": gemini_model,
        "no_high_quality_seed_today_reason": reason,
    }


def _curated_candidates(
    records: list[dict[str, Any]], *, focus_keys: set[str], include_dynamic: bool = False
) -> list[tuple[int, dict[str, Any], list[dict[str, Any]], int]]:
    axes = [*AXES]
    if include_dynamic:
        axes.extend(_legacy_dynamic_axes(records, max_axes=8))
    candidates: list[tuple[int, dict[str, Any], list[dict[str, Any]], int]] = []
    seen_titles: set[str] = set()
    for axis in axes:
        if axis["title"] in seen_titles:
            continue
        seen_titles.add(axis["title"])
        evidence = _supporting(records, axis["domains"], focus_keys=focus_keys)
        sources = _source_count(evidence)
        if sources < 3:
            continue
        recent = _recent_count(evidence, focus_keys)
        score = sources * 10 + recent * 20 + len(axis["domains"])
        axis = {**axis, "generation_rule": "curated_axis", "generator_status": "template"}
        candidates.append((score, axis, evidence, recent))
    return sorted(candidates, key=lambda item: -item[0])


def generate_seed_candidates(
    records: list[dict[str, Any]],
    *,
    focus_keys: list[str],
    limit: int,
    include_dynamic: bool = False,
    mode: str = "mechanism",
    generator: str = "template",
    generator_timeout: int = 240,
) -> list[tuple[dict[str, Any], list[dict[str, Any]], int]]:
    report = generate_seed_report(
        records,
        focus_keys=focus_keys,
        limit=limit,
        include_dynamic=include_dynamic,
        mode=mode,
        generator=generator,
        generator_timeout=generator_timeout,
        run_date=today(),
    )
    return report["high_quality"]


def _render_idea(axis: dict[str, Any], evidence: list[dict[str, Any]], *, recent_count: int) -> str:
    title = axis["title"]
    now = today()
    mechanism_mode = axis.get("generation_rule") in {"mechanism_cluster", "gemini_divergent"}
    spec = next((item for item in MECHANISM_SPECS if item["cluster_id"] == axis.get("cluster_id")), axis)
    strong_sources = _strong_source_count(evidence, spec)
    evidence_level = "strong" if strong_sources >= 3 and (_source_count(evidence) >= 4 or recent_count >= 2) else "partial"
    lines = [
        "---",
        f'title: "{title}"',
        "tags: [research-agenda, idea, seed]",
        f'created: "{now}"',
        f'updated: "{now}"',
        'type: "permanent"',
        'status: "done"',
        'summary: "Mechanism-level research idea seed, generated for review only."',
        "idea_state: seed",
        f"evidence_count: {_source_count(evidence)}",
        f"strong_mechanism_evidence_count: {strong_sources}",
        f"recent_evidence_count: {recent_count}",
        f'generation_rule: "{axis.get("generation_rule", "curated_axis")}"',
        f'generator_status: "{axis.get("generator_status", "template")}"',
        f'quality_tier: "{axis.get("quality_tier", "unrated")}"',
        f'quality_tier_semantics: "{axis.get("quality_tier_semantics", QUALITY_TIER_SEMANTICS)}"',
        f'potential_tier: "{axis.get("potential_tier", axis.get("quality_tier", "unrated"))}"',
        f'potential_score: {axis.get("potential_score", axis.get("research_quality_score", 0))}',
        f'readiness_tier: "{axis.get("readiness_tier", "untriaged")}"',
        f'promotion_decision: "{axis.get("promotion_decision", "not_ready")}"',
        f'candidate_group: "{axis.get("candidate_group", "")}"',
        f'origin_type: "{axis.get("origin_type", "")}"',
        f'research_claim_type: "{axis.get("research_claim_type", "")}"',
        f'bottleneck_type: "{axis.get("bottleneck_type", "")}"',
        f'evidence_mode: "{axis.get("evidence_mode", "")}"',
        f'risk_class: "{axis.get("risk_class", "")}"',
        f'world_model_role: "{axis.get("world_model_role", "")}"',
        f'portfolio_slot: "{axis.get("portfolio_slot", "")}"',
        f"research_quality_score: {axis.get('research_quality_score', 0)}",
        f"sharpness_score: {axis.get('sharpness_score', 0)}",
        f"evidence_execution_score: {axis.get('evidence_execution_score', 0)}",
        f"ordinaryness_penalty: {axis.get('ordinaryness_penalty', 0)}",
        f"evidence_support_score: {axis.get('evidence_support_score', 0)}",
        f"support_score: {axis.get('support_score', 0)}",
        f"originality_score: {axis.get('originality_score', 0)}",
        f"engineering_value_score: {axis.get('engineering_value_score', 0)}",
        f'contribution_shape: "{axis.get("contribution_shape", "")}"',
        "---",
        "",
        f"# {title}",
        "",
        "- decision_status: generated_for_review" if mechanism_mode else "- decision_status: seed_draft",
        f"- evidence_level: {evidence_level}",
        f"- quality_tier: {axis.get('quality_tier', 'unrated')}",
        f"- quality_tier_semantics: {axis.get('quality_tier_semantics', QUALITY_TIER_SEMANTICS)}",
        f"- potential_tier: {axis.get('potential_tier', axis.get('quality_tier', 'unrated'))}",
        f"- readiness_tier: {axis.get('readiness_tier', 'untriaged')}",
        f"- promotion_decision: {axis.get('promotion_decision', 'not_ready')}",
        f"- candidate_group: {axis.get('candidate_group', '-')}",
        f"- origin_type: {axis.get('origin_type', '-')}",
        f"- research_claim_type: {axis.get('research_claim_type', '-')}",
        f"- bottleneck_type: {axis.get('bottleneck_type', '-')}",
        f"- evidence_mode: {axis.get('evidence_mode', '-')}",
        f"- risk_class: {axis.get('risk_class', '-')}",
        f"- world_model_role: {axis.get('world_model_role', '-')}",
        f"- portfolio_slot: {axis.get('portfolio_slot', '-')}",
        f"- research_quality_score: {axis.get('research_quality_score', 0)}",
        f"- sharpness_score: {axis.get('sharpness_score', 0)}",
        f"- evidence_execution_score: {axis.get('evidence_execution_score', 0)}",
        f"- ordinaryness_penalty: {axis.get('ordinaryness_penalty', 0)}",
        f"- evidence_support_score: {axis.get('evidence_support_score', 0)}",
        f"- support_score: {axis.get('support_score', 0)}",
        f"- originality_score: {axis.get('originality_score', 0)}",
        f"- engineering_value_score: {axis.get('engineering_value_score', 0)}",
        "- claim_status: unverified",
        "- final_reviewer: user",
        "",
        "## Problem",
        "",
        axis["problem"],
        "",
        "## Engineering Pathology",
        "",
        axis.get("engineering_pathology") or "Not specified; reviewer should identify the concrete robot-system bottleneck before promotion.",
        "",
        "## Mechanism / Interface",
        "",
        f"- mechanism: {axis.get('mechanism', 'unverified mechanism')}",
        f"- interface: {axis.get('interface', 'unverified interface')}",
        "",
        "## Working Hypothesis",
        "",
        axis.get("hypothesis") or "This is a hypothesis scaffold, not proof that the idea will work.",
        "",
        "## Why Now",
        "",
        axis.get("why_now", "Recent local evidence creates enough pressure to test this mechanism."),
        "",
        "## Contribution Shape",
        "",
        f"- idea_archetype: {axis.get('idea_archetype') or 'Not specified.'}",
        f"- contribution_shape: {axis.get('contribution_shape') or 'Not classified; reviewer should decide whether this is architecture, algorithm, control_interface, mechanism, system, method_improvement, evaluation_protocol, benchmark, failure_model, or dataset.'}",
        "",
        "## Non-obvious Claim",
        "",
        axis.get("non_obvious_claim") or "Not specified; rewrite before treating this as a strong seed.",
        "",
        "## Adversarial Generation Trace",
        "",
        f"- naive_combination_version: {axis.get('naive_combination_version') or 'Missing; rewrite because the bad A+B version was not made explicit.'}",
        f"- strongest_baseline_kill_path: {axis.get('strongest_baseline_kill_path') or 'Missing; rewrite because the strongest baseline kill path was not tested.'}",
        f"- post_kill_mutation: {axis.get('post_kill_mutation') or 'Missing; rewrite because the final mechanism was not mutated after the kill test.'}",
        "- boundary: final mechanism should be the post-kill mutation, not the naive combination.",
        "",
        "## Anti-combination Test",
        "",
        axis.get("anti_combination_test") or "Not specified; reviewer should test whether this is merely A+B before promotion.",
        "",
        "## Top-tier Rationale",
        "",
        axis.get("top_tier_rationale") or "Not specified; reviewer should identify the top-tier contribution shape and failure risk.",
        "",
        "## Engineering Loop",
        "",
        axis.get("engineering_loop") or "Not specified; reviewer should identify the robot sense-plan-act-learn/evaluate loop.",
        "",
        "## Method Improvement Claim",
        "",
        f"- method_improvement_claim: {axis.get('method_improvement_claim') or 'Not a method-improvement candidate, or not specified.'}",
        f"- original_method_failure: {axis.get('original_method_failure') or 'Not specified.'}",
        f"- replacement_or_coupled_technique: {axis.get('replacement_or_coupled_technique') or 'Not specified.'}",
        f"- why_improvement_not_patch: {axis.get('why_improvement_not_patch') or 'Not specified; reviewer should verify this is not a trivial patch.'}",
        "",
        "## Strongest Baseline / Killer Experiment",
        "",
        f"- strongest_baseline: {axis.get('strongest_baseline') or axis.get('baselines', 'review needed')}",
        f"- baseline_failure_mode: {axis.get('baseline_failure_mode') or 'review needed'}",
        f"- killer_experiment: {axis.get('killer_experiment') or axis.get('falsification', 'review needed')}",
        f"- reviewer_kill_shot: {axis.get('reviewer_kill_shot') or 'review needed'}",
        f"- rescue_mutation: {axis.get('rescue_mutation') or 'review needed'}",
        f"- claim_compression: {axis.get('claim_compression') or 'review needed'}",
        "",
        "## Execution Mode / No-hardware Pilot",
        "",
        f"- online_or_offline_mode: {axis.get('online_or_offline_mode') or 'review needed'}",
        f"- minimum_no_hardware_pilot: {axis.get('minimum_no_hardware_pilot') or axis.get('pilot', 'review needed')}",
        f"- baseline_kill_table: {axis.get('baseline_kill_table') or 'review needed'}",
        f"- what_would_make_this_not_a_paper: {axis.get('what_would_make_this_not_a_paper') or 'review needed'}",
        f"- reviewer_pre_mortem: {axis.get('reviewer_pre_mortem') or axis.get('reviewer_kill_shot') or 'review needed'}",
        "",
        "## Novelty Pressure",
        "",
        f"- novelty_pressure: {axis.get('novelty_pressure', {}).get('pressure', 'not_checked') if isinstance(axis.get('novelty_pressure'), dict) else 'not_checked'}",
        f"- novelty_risk: {axis.get('novelty_risk') or 'Not specified; local pressure only, not confirmed novelty.'}",
        "- boundary: local novelty pressure is not a live external novelty search.",
        "",
        "## Promotion / Rescue Signal",
        "",
        f"- promotion_reason: {axis.get('promotion_reason') or 'Generated for review only.'}",
        f"- rescue_signal: {axis.get('rescue_signal') or axis.get('engineering_pathology') or axis.get('mechanism') or 'No rescue signal recorded.'}",
        "",
        "## Speculative Jump",
        "",
        axis.get("speculative_jump") or "No explicit speculative jump recorded.",
        "",
        "## Local Evidence",
        "",
        *_evidence_lines(evidence, 8),
        "",
        "## Nearest Pressure",
        "",
        axis.get("nearest_pressure", "Nearest prior work must be checked before promotion."),
        "",
        "## Minimal Pilot",
        "",
        axis["pilot"],
        "",
        "## Baselines",
        "",
        axis["baselines"],
        "",
        "## Metrics",
        "",
        axis["metrics"],
        "",
        "## Falsification Criteria",
        "",
        axis.get("falsification", "Reject or narrow this seed if the pilot cannot isolate the claimed mechanism."),
        "",
        "## Status Boundary",
        "",
        axis.get("status_boundary", "Generated seed for user review only; no paper claim is accepted."),
        "",
        "## Promotion Gate",
        "",
        "- [ ] Codex/Claudian second-pass review accepts this for user review",
        "- [ ] similar_work.md is upgraded from generated_complete to reviewed_complete",
        "- [ ] experiment_plan.md is upgraded from generated_complete to reviewed_complete",
        "- [ ] risk_review.md is upgraded from generated_complete to reviewed_complete",
        "- [ ] at least one low-cost pilot or explicit no-go decision is recorded",
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _render_evidence_pack(axis: dict[str, Any], evidence: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            f"# Evidence Pack - {axis['title']}",
            "",
            "Evidence is pulled from local `wiki/topics/` notes with `status: done`.",
            "",
            "## Supporting Local Evidence",
            "",
            *_evidence_lines(evidence, 12),
            "",
            "## Evidence Boundary",
            "",
            "- generated_complete: this pack supports a seed candidate, not a paper claim.",
            "- review_needed: verify exact nearest-prior overlap before promotion.",
            "",
        ]
    )


def _render_aux_file(axis: dict[str, Any], kind: str) -> str:
    mechanism_mode = axis.get("generation_rule") in {"mechanism_cluster", "gemini_divergent"}
    gate = "generated_complete" if mechanism_mode else "draft"
    if kind == "similar_work.md":
        body = "\n".join(
            [
                f"gate_status: {gate}",
                "",
                "## Similar Work Pressure",
                "",
                f"- nearest_pressure: {axis.get('nearest_pressure', 'review needed')}",
                f"- novelty_pressure: {axis.get('novelty_pressure', {}).get('pressure', 'not_checked') if isinstance(axis.get('novelty_pressure'), dict) else 'not_checked'}",
                f"- strongest_baseline: {axis.get('strongest_baseline', 'review needed')}",
                "- review_needed: classify each close paper as already solved, partially solved, or still open.",
                "- review_needed: upgrade this file to `gate_status: reviewed_complete` before developing/promotion.",
                "",
            ]
        )
    elif kind == "novelty_argument.md":
        body = "\n".join(
            [
                f"gate_status: {gate}",
                "",
                "## Novelty Argument",
                "",
                f"- candidate_claim: {axis.get('hypothesis', 'unverified hypothesis')}",
                f"- non_obvious_claim: {axis.get('non_obvious_claim', 'review needed')}",
                f"- novelty_risk: {axis.get('novelty_risk', 'review needed')}",
                f"- mechanism: {axis.get('mechanism', 'unverified mechanism')}",
                f"- interface: {axis.get('interface', 'unverified interface')}",
                "- boundary: generated argument only; not a formal paper claim.",
                "",
            ]
        )
    elif kind == "experiment_plan.md":
        body = "\n".join(
            [
                f"gate_status: {gate}",
                "",
                "## Experiment Plan",
                "",
                f"- pilot: {axis['pilot']}",
                f"- online_or_offline_mode: {axis.get('online_or_offline_mode', 'review needed')}",
                f"- minimum_no_hardware_pilot: {axis.get('minimum_no_hardware_pilot', axis['pilot'])}",
                f"- killer_experiment: {axis.get('killer_experiment', axis.get('falsification', 'review needed'))}",
                f"- baseline_kill_table: {axis.get('baseline_kill_table', 'review needed')}",
                f"- strongest_baseline: {axis.get('strongest_baseline', axis.get('baselines', 'review needed'))}",
                f"- baselines: {axis['baselines']}",
                f"- metrics: {axis['metrics']}",
                f"- falsification: {axis.get('falsification', 'reject if the pilot cannot isolate the mechanism')}",
                "- minimum_viable_test: prefer offline, simulation, or replay-buffer tests before real-robot work.",
                "",
            ]
        )
    elif kind == "risk_review.md":
        body = "\n".join(
            [
                f"gate_status: {gate}",
                "",
                "## Risk Review",
                "",
                "- main_risk: nearest prior work may already cover the claimed mechanism.",
                "- main_risk: local evidence may support the problem but not the proposed interface.",
                f"- reviewer_pre_mortem: {axis.get('reviewer_pre_mortem', axis.get('reviewer_kill_shot', 'review needed'))}",
                f"- what_would_make_this_not_a_paper: {axis.get('what_would_make_this_not_a_paper', 'review needed')}",
                "- fallback: narrow to one task, one signal, one baseline, and one measurable failure mode.",
                f"- reject_condition: {axis.get('falsification', 'reject if the mechanism cannot be isolated')}",
                "",
            ]
        )
    elif kind == "review_log.md":
        status = "generated_pending_codex_review" if mechanism_mode else "seed_pending_review"
        body = f"## Review Log\n\n- created_by: research_agenda_ideate.py\n- status: {status}\n"
    else:
        body = ""
    return f"# {kind.replace('.md', '').replace('_', ' ').title()} - {axis['title']}\n\n{body}".rstrip() + "\n"


def write_seed_folder(axis: dict[str, Any], evidence: list[dict[str, Any]], *, recent_count: int, dry_run: bool) -> Path:
    slug = slugify(axis["title"])
    folder = IDEA_BANK_DIR / "seed" / slug
    if not dry_run:
        folder.mkdir(parents=True, exist_ok=True)
    safe_write(folder / "idea.md", _render_idea(axis, evidence, recent_count=recent_count), dry_run=dry_run, backup=True)
    safe_write(folder / "evidence_pack.md", _render_evidence_pack(axis, evidence), dry_run=dry_run, backup=True)
    for name in REQUIRED_IDEA_FILES:
        if name in {"idea.md", "evidence_pack.md"}:
            continue
        safe_write(folder / name, _render_aux_file(axis, name), dry_run=dry_run, backup=True)
    return folder


def _greenhouse_counts(items: list[dict[str, Any]]) -> Counter[str]:
    return Counter(str(item.get("greenhouse_label", "unlabeled")) for item in items)


def _portfolio_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    origin_counts = Counter(str(item.get("origin_type", "unclassified") or "unclassified") for item in items)
    claim_counts = Counter(str(item.get("research_claim_type", "unclassified") or "unclassified") for item in items)
    bottleneck_counts = Counter(str(item.get("bottleneck_type", "unclassified") or "unclassified") for item in items)
    evidence_mode_counts = Counter(str(item.get("evidence_mode", "unclassified") or "unclassified") for item in items)
    risk_counts = Counter(str(item.get("risk_class", "unclassified") or "unclassified") for item in items)
    slot_counts = Counter(str(item.get("portfolio_slot", "unclassified") or "unclassified") for item in items)
    world_model_roles = Counter(str(item.get("world_model_role", "none") or "none") for item in items)
    visible_failure_recovery = sum(1 for item in items if _is_visible_failure_recovery_candidate(item))
    non_failure_origins = sum(1 for item in items if str(item.get("origin_type", "")) in NON_FAILURE_ORIGIN_TYPES)
    warnings: list[str] = []
    if visible_failure_recovery > 2:
        warnings.append(f"visible_failure_recovery_cap_exceeded:{visible_failure_recovery}")
    if non_failure_origins < 3 and items:
        warnings.append(f"non_failure_origin_under_target:{non_failure_origins}")
    if not any(str(item.get("risk_class", "")) == "breakthrough" for item in items) and items:
        warnings.append("missing_breakthrough_bet")
    if not any(str(item.get("research_claim_type", "")) == "world_model_simulation" for item in items) and items:
        warnings.append("missing_world_model_slot")
    if not any(str(item.get("research_claim_type", "")) in {"data_curriculum", "evaluation_benchmark"} for item in items) and items:
        warnings.append("missing_measurement_data_slot")
    return {
        "origin_type_counts": dict(origin_counts),
        "research_claim_type_counts": dict(claim_counts),
        "bottleneck_type_counts": dict(bottleneck_counts),
        "evidence_mode_counts": dict(evidence_mode_counts),
        "risk_class_counts": dict(risk_counts),
        "portfolio_slot_counts": dict(slot_counts),
        "world_model_role_counts": dict(world_model_roles),
        "visible_failure_recovery_candidates": visible_failure_recovery,
        "non_failure_origin_candidates": non_failure_origins,
        "warnings": warnings,
    }


def render_greenhouse_markdown(run_date: str, report: dict[str, Any]) -> str:
    items = report.get("greenhouse", [])
    counts = _greenhouse_counts(items)
    portfolio = report.get("portfolio_summary") or _portfolio_summary(items)
    lines = [
        f"# Gemini Divergent Greenhouse - {run_date}",
        "",
        f"- generator: {report.get('generator', '-')}",
        f"- generator_status: {report.get('generator_status', '-')}",
        f"- gemini_model: {report.get('gemini_model', '-')}",
        f"- raw_candidate_limit: {report.get('raw_candidate_limit', '-')}",
        f"- min_raw_candidates: {report.get('min_raw_candidates', '-')}",
        f"- free_divergence: {report.get('free_divergence', False)}",
        f"- free_divergence_start_date: {report.get('free_divergence_start_date', FREE_DIVERGENCE_START_DATE)}",
        f"- raw_candidates: {len(items)}",
        f"- evidence_bound_candidates: {sum(1 for item in items if item.get('candidate_group') == 'evidence_bound')}",
        f"- wild_engineering_candidates: {sum(1 for item in items if item.get('candidate_group') == 'wild_engineering')}",
        f"- promoted_to_seed: {counts.get('promoted_to_seed', 0)}",
        f"- speculative_preserve: {counts.get('speculative_preserve', 0)}",
        f"- parked_for_weekly_review: {counts.get('parked_for_weekly_review', 0)}",
        f"- rewrite_needed: {counts.get('rewrite_needed', 0)}",
        f"- blocked_with_rescue_signal: {counts.get('blocked_with_rescue_signal', 0)}",
        f"- quality_tier_semantics: {QUALITY_TIER_SEMANTICS}",
        f"- readiness_seed_ready: {sum(1 for item in items if item.get('readiness_tier') == 'seed_ready')}",
        f"- readiness_rewrite_required: {sum(1 for item in items if item.get('readiness_tier') == 'rewrite_required')}",
        f"- readiness_weekly_review: {sum(1 for item in items if item.get('readiness_tier') == 'weekly_review')}",
        f"- readiness_speculative_weekly_review: {sum(1 for item in items if item.get('readiness_tier') == 'speculative_weekly_review')}",
        f"- readiness_rescue_only: {sum(1 for item in items if item.get('readiness_tier') == 'rescue_only')}",
        f"- quality_tier_S: {sum(1 for item in items if item.get('quality_tier') == 'S')}",
        f"- quality_tier_A: {sum(1 for item in items if item.get('quality_tier') == 'A')}",
        f"- quality_tier_B: {sum(1 for item in items if item.get('quality_tier') == 'B')}",
        f"- quality_tier_C: {sum(1 for item in items if item.get('quality_tier') == 'C')}",
        f"- quality_rubric_weights: {json.dumps(report.get('quality_rubric_weights', QUALITY_RUBRIC_WEIGHTS), ensure_ascii=False, sort_keys=True)}",
        f"- portfolio_summary: {json.dumps(portfolio, ensure_ascii=False, sort_keys=True)}",
        "",
        "## Source Filter",
        "",
        f"- policy: {report.get('generator_metadata', {}).get('source_filter_policy', 'not_reported')}",
        f"- source_rejected_draft_count: {report.get('generator_metadata', {}).get('source_rejected_draft_count', 0)}",
        f"- surviving_candidate_count: {report.get('generator_metadata', {}).get('surviving_candidate_count', len(items))}",
        "",
        "### Rejected Drafts Summary",
        "",
    ]
    rejected_drafts = report.get("generator_metadata", {}).get("rejected_drafts_summary", [])
    if not rejected_drafts:
        lines.append("- none reported")
    for draft in rejected_drafts:
        if not isinstance(draft, dict):
            continue
        lines.append(
            f"- {draft.get('draft_title', 'untitled')}: "
            f"{draft.get('failure_reason', 'no failure reason')} "
            f"| strongest_baseline={draft.get('strongest_baseline', '-')}"
        )
    lines.extend(
        [
            "",
            "## Candidates",
            "",
        ]
    )
    if not items:
        lines.append("- none")
    for item in items:
        issues = ", ".join(item.get("issues", [])) or "-"
        lines.extend(
            [
                f"### {item.get('title', 'Untitled')}",
                "",
                f"- greenhouse_label: {item.get('greenhouse_label', 'unlabeled')}",
                f"- candidate_group: {item.get('candidate_group', '-')}",
                f"- origin_type: {item.get('origin_type', '-')}",
                f"- research_claim_type: {item.get('research_claim_type', '-')}",
                f"- bottleneck_type: {item.get('bottleneck_type', '-')}",
                f"- evidence_mode: {item.get('evidence_mode', '-')}",
                f"- risk_class: {item.get('risk_class', '-')}",
                f"- world_model_role: {item.get('world_model_role', '-')}",
                f"- portfolio_slot: {item.get('portfolio_slot', '-')}",
                f"- evidence_support_score: {item.get('evidence_support_score', item.get('score', '-'))}",
                f"- support_score: {item.get('support_score', '-')}",
                f"- originality_score: {item.get('originality_score', '-')}",
                f"- engineering_value_score: {item.get('engineering_value_score', '-')}",
                f"- sharpness_score: {item.get('sharpness_score', '-')}",
                f"- evidence_execution_score: {item.get('evidence_execution_score', '-')}",
                f"- ordinaryness_penalty: {item.get('ordinaryness_penalty', '-')}",
                f"- research_quality_score: {item.get('research_quality_score', '-')}",
                f"- research_quality_components: {json.dumps(item.get('research_quality_components', {}), ensure_ascii=False, sort_keys=True)}",
                f"- quality_tier: {item.get('quality_tier', '-')}",
                f"- quality_tier_semantics: {item.get('quality_tier_semantics', QUALITY_TIER_SEMANTICS)}",
                f"- potential_tier: {item.get('potential_tier', item.get('quality_tier', '-'))}",
                f"- readiness_tier: {item.get('readiness_tier', 'untriaged')}",
                f"- promotion_decision: {item.get('promotion_decision', 'not_ready')}",
                f"- idea_archetype: {item.get('idea_archetype') or '-'}",
                f"- contribution_shape: {item.get('contribution_shape') or '-'}",
                f"- issues: {issues}",
                f"- engineering_pathology: {item.get('engineering_pathology') or '-'}",
                f"- mechanism: {item.get('mechanism') or '-'}",
                f"- interface: {item.get('interface') or '-'}",
                f"- non_obvious_claim: {item.get('non_obvious_claim') or '-'}",
                f"- naive_combination_version: {item.get('naive_combination_version') or '-'}",
                f"- strongest_baseline_kill_path: {item.get('strongest_baseline_kill_path') or '-'}",
                f"- post_kill_mutation: {item.get('post_kill_mutation') or '-'}",
                f"- anti_combination_test: {item.get('anti_combination_test') or '-'}",
                f"- top_tier_rationale: {item.get('top_tier_rationale') or '-'}",
                f"- engineering_loop: {item.get('engineering_loop') or '-'}",
                f"- method_improvement_claim: {item.get('method_improvement_claim') or '-'}",
                f"- original_method_failure: {item.get('original_method_failure') or '-'}",
                f"- replacement_or_coupled_technique: {item.get('replacement_or_coupled_technique') or '-'}",
                f"- why_improvement_not_patch: {item.get('why_improvement_not_patch') or '-'}",
                f"- strongest_baseline: {item.get('strongest_baseline') or '-'}",
                f"- baseline_failure_mode: {item.get('baseline_failure_mode') or '-'}",
                f"- killer_experiment: {item.get('killer_experiment') or '-'}",
                f"- reviewer_kill_shot: {item.get('reviewer_kill_shot') or '-'}",
                f"- rescue_mutation: {item.get('rescue_mutation') or '-'}",
                f"- claim_compression: {item.get('claim_compression') or '-'}",
                f"- online_or_offline_mode: {item.get('online_or_offline_mode') or '-'}",
                f"- minimum_no_hardware_pilot: {item.get('minimum_no_hardware_pilot') or '-'}",
                f"- baseline_kill_table: {item.get('baseline_kill_table') or '-'}",
                f"- what_would_make_this_not_a_paper: {item.get('what_would_make_this_not_a_paper') or '-'}",
                f"- reviewer_pre_mortem: {item.get('reviewer_pre_mortem') or '-'}",
                f"- novelty_pressure: {item.get('novelty_pressure', {}).get('pressure', '-') if isinstance(item.get('novelty_pressure'), dict) else '-'}",
                f"- novelty_risk: {item.get('novelty_risk') or '-'}",
                f"- promotion_reason: {item.get('promotion_reason') or '-'}",
                f"- rescue_signal: {item.get('rescue_signal') or '-'}",
                f"- speculative_jump: {item.get('speculative_jump') or '-'}",
                f"- pilot: {item.get('pilot') or '-'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "- Greenhouse candidates preserve creative raw ideas for review.",
            "- Only promoted_to_seed candidates are written to `idea_bank/seed/`.",
            "- speculative_preserve means high-sharpness / low-evidence candidates are kept for weekly breakthrough review, not accepted.",
            "- Parked/rewrite/blocked candidates are not paper claims and are not deleted.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_greenhouse_archive(report: dict[str, Any], *, run_date: str, dry_run: bool) -> tuple[Path, Path]:
    json_path = DIVERGENT_DIR / f"{run_date}-gemini-raw-candidates.json"
    md_path = DIVERGENT_DIR / f"{run_date}-gemini-raw-candidates.md"
    payload = {
        "run_date": run_date,
        "generator": report.get("generator"),
        "generator_status": report.get("generator_status"),
        "gemini_model": report.get("gemini_model"),
        "raw_candidate_limit": report.get("raw_candidate_limit"),
        "min_raw_candidates": report.get("min_raw_candidates"),
        "free_divergence": report.get("free_divergence", False),
        "free_divergence_start_date": report.get("free_divergence_start_date", FREE_DIVERGENCE_START_DATE),
        "quality_rubric_weights": report.get("quality_rubric_weights", QUALITY_RUBRIC_WEIGHTS),
        "workflow_contracts": report.get("workflow_contracts", WORKFLOW_CONTRACTS),
        "generator_metadata": report.get("generator_metadata", {}),
        "portfolio_summary": report.get("portfolio_summary", _portfolio_summary(report.get("greenhouse", []))),
        "raw_gemini_candidates": report.get("greenhouse", []),
        "high_quality_seed_candidates": [
            _jsonable_candidate(axis, evidence, recent)
            for axis, evidence, recent in report.get("high_quality", [])
        ],
        "parked_candidates": report.get("parked", []),
        "blocked_candidates": report.get("blocked", []),
    }
    safe_write(json_path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n", dry_run=dry_run, backup=True)
    safe_write(md_path, render_greenhouse_markdown(run_date, report), dry_run=dry_run, backup=True)
    return json_path, md_path


def _report_json(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "mode": report["mode"],
        "generator": report["generator"],
        "generator_status": report["generator_status"],
        "high_quality_seed_candidates": [
            _jsonable_candidate(axis, evidence, recent)
            for axis, evidence, recent in report["high_quality"]
        ],
        "parked_candidates": report["parked"],
        "blocked_candidates": report["blocked"],
        "greenhouse_candidates": report.get("greenhouse", []),
        "raw_candidate_limit": report.get("raw_candidate_limit", 0),
        "min_raw_candidates": report.get("min_raw_candidates", 0),
        "quality_rubric_weights": report.get("quality_rubric_weights", QUALITY_RUBRIC_WEIGHTS),
        "workflow_contracts": report.get("workflow_contracts", WORKFLOW_CONTRACTS),
        "generator_metadata": report.get("generator_metadata", {}),
        "portfolio_summary": report.get("portfolio_summary", _portfolio_summary(report.get("greenhouse", []))),
        "free_divergence": report.get("free_divergence", False),
        "free_divergence_start_date": report.get("free_divergence_start_date", FREE_DIVERGENCE_START_DATE),
        "gemini_model": report.get("gemini_model", ""),
        "no_high_quality_seed_today_reason": report["no_high_quality_seed_today_reason"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", default=str(agenda_path("evidence", "evidence_matrix.jsonl")))
    parser.add_argument("--focus-zotero-keys", default="")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--max-generated", type=int, default=3)
    parser.add_argument("--raw-candidate-limit", type=int, default=8)
    parser.add_argument("--min-raw-candidates", type=int, default=DEFAULT_MIN_RAW_CANDIDATES)
    parser.add_argument("--mode", choices=["mechanism", "curated"], default="mechanism")
    parser.add_argument("--generator", choices=["template", "claude", "gemini-cli", "gemini-divergent", "none"], default="template")
    parser.add_argument("--generator-timeout", type=int, default=1200)
    parser.add_argument("--gemini-model", default="gemini-3.1-pro-preview")
    parser.add_argument("--run-date", default=today())
    parser.add_argument("--include-dynamic", action="store_true", help="Deprecated: also generate generic cross-domain gap candidates in curated mode.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ensure_agenda_dirs()
    records = load_evidence_matrix(Path(args.matrix))
    focus_keys = split_csv(args.focus_zotero_keys)
    limit = min(args.limit, args.max_generated)
    report = generate_seed_report(
        records,
        focus_keys=focus_keys,
        limit=limit,
        include_dynamic=args.include_dynamic,
        mode=args.mode,
        generator=args.generator,
        generator_timeout=args.generator_timeout,
        raw_candidate_limit=args.raw_candidate_limit,
        min_raw_candidates=args.min_raw_candidates,
        gemini_model=args.gemini_model,
        run_date=args.run_date,
    )
    if args.json:
        safe_print(json.dumps(_report_json(report), ensure_ascii=False, indent=2))
    else:
        safe_print(
            "IDEATE "
            f"mode={report['mode']} generator={report['generator']} status={report['generator_status']} "
            f"high_quality={len(report['high_quality'])} parked={len(report['parked'])} blocked={len(report['blocked'])} "
            f"greenhouse={len(report.get('greenhouse', []))} "
            f"quality_tiers={dict(Counter(item.get('quality_tier', 'unrated') for item in report.get('greenhouse', [])))} "
            f"readiness_tiers={dict(Counter(item.get('readiness_tier', 'untriaged') for item in report.get('greenhouse', [])))} "
            f"matrix_records={len(records)} focus_keys={len(focus_keys)}"
        )
        if report["no_high_quality_seed_today_reason"]:
            safe_print(f"NO_HIGH_QUALITY_SEED_TODAY: {report['no_high_quality_seed_today_reason']}")
        for axis, evidence, recent in report["high_quality"]:
            folder = IDEA_BANK_DIR / "seed" / slugify(axis["title"])
            safe_print(f"  seed={rel(folder)} evidence_sources={_source_count(evidence)} recent={recent}")
    if not args.dry_run:
        if report.get("generator") == "gemini-divergent":
            write_greenhouse_archive(report, run_date=args.run_date, dry_run=False)
        for axis, evidence, recent in report["high_quality"]:
            write_seed_folder(axis, evidence, recent_count=recent, dry_run=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
