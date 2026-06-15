"""Rank arXiv papers for the daily embodied-AI scout pipeline."""
from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from typing import Any

from kb_embed import EmbeddingUnavailable


TOP1_THRESHOLD = 85
REVIEW_THRESHOLD = 70
FOCUS_REVIEW_THRESHOLD = 55
BELOW_REVIEW_DECISION = "below_review_threshold"
LEGACY_REJECT_DECISION = "reject"
FOCUS_REVIEW_DECISION = "focus_review_queue"
AUTO_IMPORT_DECISIONS = {"top1_candidate", "venue_auto_import"}
# Personalised scout: rank daily candidates partly by how similar they are to
# the papers you have actually finished reading (the read-library anchor).
# On by default; set KB_RANKER_READ_LIB=0 to fall back to keyword-only ranking.
ENABLE_READ_LIB_SIMILARITY = os.environ.get("KB_RANKER_READ_LIB", "1").strip().lower() not in {"0", "false", "no", "off"}

DEFAULT_QUERIES = [
    'all:"embodied AI" OR all:"embodied artificial intelligence" OR all:"robot learning"',
    'all:"robotic manipulation" OR all:"robot manipulation"',
    'all:"vision-language-action" OR all:"vision language action" OR all:"VLA"',
    'all:"RL token" OR all:"action interface" OR all:"action head" OR all:"VLA anchoring"',
    'all:"sim-to-real" OR all:"sim2real" OR all:"real-to-sim"',
    'all:"failure recovery" OR all:"out-of-distribution" OR all:"robot robustness"',
    'all:"tactile" AND all:"robot"',
    'all:"bimanual" AND all:"manipulation"',
    'all:"deformable linear object" OR all:"DLO" OR all:"deformable object manipulation"',
    'cat:cs.RO AND all:"diffusion" AND all:"policy"',
]

DOMAIN_TERMS = {
    "embodied_ai": [
        "embodied ai",
        "embodied artificial intelligence",
        "embodied agent",
        "physical ai",
        "robot foundation model",
    ],
    "robot_learning": ["robot learning", "policy learning", "imitation learning", "reinforcement learning"],
    "manipulation": ["robotic manipulation", "robot manipulation", "manipulation", "grasp", "dexterous"],
    "vla_vlm": ["vision-language-action", "vision language action", "vla", "vision-language", "vlm"],
    "action_interface": ["rl token", "action interface", "action head", "decoder boundary", "token interface", "vla anchoring"],
    "sim_to_real": ["sim-to-real", "sim2real", "real-to-sim", "domain randomization"],
    "robustness_recovery": ["robustness", "failure recovery", "out-of-distribution", "ood", "recovery", "safety recovery"],
    "tactile": ["tactile", "touch", "force", "force-torque", "haptic", "contact-rich", "contact rich", "visuotactile"],
    "bimanual": ["bimanual", "dual-arm", "dual arm", "two-arm"],
    "dlo": ["deformable linear object", "dlo", "rope", "cable", "thread", "deformable object"],
    "diffusion": ["diffusion policy", "diffusion model", "diffusion"],
    "planning": ["planning", "planner", "trajectory optimization", "task and motion planning"],
}

EXPERIMENT_TERMS = [
    "benchmark",
    "dataset",
    "evaluation",
    "experiment",
    "real robot",
    "hardware",
    "ablation",
    "baseline",
    "comparison",
    "success rate",
    "sim-to-real",
    "generalization",
    "task suite",
]

REPRO_TERMS = ["code", "github", "open-source", "open source", "dataset", "benchmark", "project page"]
RESEARCH_VALUE_TERMS = [
    "failure",
    "limitation",
    "negative result",
    "benchmark",
    "ablation",
    "baseline",
    "real robot",
    "contact-rich",
    "failure recovery",
    "out-of-distribution",
    "action interface",
    "rl token",
    "sim-to-real",
    "generalization",
    "long-horizon",
    "closed-loop",
]
DIVERSITY_FEATURE_TERMS = {
    "infrastructure_or_benchmark": ["benchmark", "dataset", "evaluation", "metric", "protocol"],
    "interface_or_control_boundary": ["interface", "control", "closed-loop", "controller", "policy"],
    "vla_action_interface": ["vla", "rl token", "action interface", "action head", "decoder boundary"],
    "physical_feedback_contact": ["tactile", "force", "force-torque", "haptic", "contact-rich"],
    "sim_to_real_robustness": ["sim-to-real", "real-to-sim", "domain randomization", "failure recovery", "ood"],
    "dlo_bimanual_manipulation": ["dlo", "rope", "cable", "bimanual", "dual-arm"],
    "outside_analogy": ["biology", "cognitive", "human", "physics", "mechanics"],
    "failure_or_negative_result": ["failure", "limitation", "negative result", "blind spot"],
}

VENUE_TERMS = [
    "icra",
    "iros",
    "rss",
    "corl",
    "ral",
    "ra-l",
    "neurips",
    "iclr",
    "cvpr",
    "icml",
    "science robotics",
    "ijrr",
    "hri",
    "wafr",
    "iser",
    "robosoft",
    "auro",
    "jfr",
    "eccv",
    "iccv",
    "aaai",
    "ijcai",
    "siggraph",
]
ROBOTICS_TOP_VENUES = {
    "rss": ["rss", "robotics science and systems", "robotics: science and systems"],
    "icra": ["icra", "international conference on robotics and automation"],
    "iros": ["iros", "intelligent robots and systems"],
    "corl": ["corl", "conference on robot learning"],
    "ra-l": ["ra-l", "ral", "robotics and automation letters"],
    "t-ro": ["t-ro", "tro", "transactions on robotics"],
    "ijrr": ["ijrr", "international journal of robotics research"],
    "science robotics": ["science robotics"],
    "hri": ["hri", "human-robot interaction"],
    "wafr": ["wafr", "algorithmic foundations of robotics"],
    "iser": ["iser", "international symposium on experimental robotics"],
    "robosoft": ["robosoft", "soft robotics"],
    "auro": ["auro", "autonomous robots"],
    "jfr": ["jfr", "journal of field robotics"],
}
ML_VISION_TOP_VENUES = {
    "neurips": ["neurips", "neural information processing systems"],
    "iclr": ["iclr", "international conference on learning representations"],
    "icml": ["icml", "international conference on machine learning"],
    "cvpr": ["cvpr", "computer vision and pattern recognition"],
    "eccv": ["eccv", "european conference on computer vision"],
    "iccv": ["iccv", "international conference on computer vision"],
    "aaai": ["aaai", "association for the advancement of artificial intelligence"],
    "ijcai": ["ijcai", "international joint conference on artificial intelligence"],
    "siggraph": ["siggraph"],
}
ACCEPTED_TERMS = [
    "accepted",
    "to appear",
    "in proceedings",
    "proceedings of",
    "published",
    "robotics: science and systems",
    "robotics science and systems",
    "science robotics",
]
NON_ACCEPTED_TERMS = ["submitted", "under review", "workshop", "arxiv preprint"]

PENALTY_TERMS = ["survey", "review", "position paper", "perspective"]
ROBOTICS_ANCHOR_TERMS = [
    "robot",
    "robotic",
    "embodied",
    "tactile",
    "bimanual",
    "dual-arm",
    "dual arm",
    "dlo",
    "deformable linear object",
    "deformable object",
    "grasp",
    "dexterous",
    "sim-to-real",
    "sim2real",
    "vision-language-action",
    "vision language action",
    "vla",
    "rl token",
    "action interface",
    "action head",
    "failure recovery",
    "contact-rich",
    "visuomotor",
    "policy learning",
    "imitation learning",
    "reinforcement learning",
]
STRONG_ROBOTICS_ANCHOR_TERMS = [
    "robot",
    "robotic",
    "embodied",
    "tactile",
    "bimanual",
    "dual-arm",
    "dual arm",
    "dlo",
    "deformable linear object",
    "deformable object",
    "grasp",
    "dexterous",
    "sim-to-real",
    "sim2real",
    "vision-language-action",
    "vision language action",
    "vla",
    "rl token",
    "failure recovery",
    "contact-rich",
    "visuomotor",
]
NON_ROBOTICS_CV_TERMS = [
    "deepfake",
    "forgery detection",
    "image manipulation",
    "video manipulation",
    "face manipulation",
    "facial manipulation",
    "audio-visual detection",
    "audio visual detection",
    "synthetic videos",
]

FOCUS_TRACK_TERMS = {
    "rl-token-vla-online-rl": {
        "terms": [
            "rl token",
            "bootstrapping online rl",
            "online rl",
            "online reinforcement learning",
            "actor-critic",
            "actor critic",
            "small actor-critic",
            "pretrained vla",
            "pretrained vlas",
            "vla anchoring",
            "action interface",
            "action head",
            "decoder boundary",
            "token interface",
            "anchoring",
            "real-world practice",
            "rl fine-tuning",
            "online rl fine-tuning",
            "flow-gspo",
            "gspo",
        ],
        "anchor_terms": [
            "rl token",
            "bootstrapping online rl",
            "online rl",
            "online reinforcement learning",
            "actor-critic",
            "actor critic",
            "vla anchoring",
            "action interface",
            "action head",
            "decoder boundary",
            "flow-gspo",
            "gspo",
        ],
    }
}


@dataclass
class ArxivPaper:
    arxiv_id: str
    title: str
    authors: list[str]
    summary: str
    published: str
    updated: str
    url: str
    pdf_url: str
    categories: list[str] = field(default_factory=list)
    primary_category: str = ""
    doi: str = ""
    journal_ref: str = ""
    comment: str = ""
    query_sources: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ArxivPaper":
        return cls(
            arxiv_id=str(data.get("arxiv_id", "")),
            title=str(data.get("title", "")),
            authors=list(data.get("authors", []) or []),
            summary=str(data.get("summary") or data.get("abstract", "")),
            published=str(data.get("published", "")),
            updated=str(data.get("updated", "")),
            url=str(data.get("url", "")),
            pdf_url=str(data.get("pdf_url", "")),
            categories=list(data.get("categories", []) or []),
            primary_category=str(data.get("primary_category", "")),
            doi=str(data.get("doi", "")),
            journal_ref=str(data.get("journal_ref", "")),
            comment=str(data.get("comment", "")),
            query_sources=list(data.get("query_sources", []) or []),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RankedPaper:
    paper: ArxivPaper
    quality_score: int
    decision: str
    reasons: list[str]
    matched_terms: list[str]
    penalties: list[str]
    focus_tracks: list[str] = field(default_factory=list)
    focus_matches: dict[str, list[str]] = field(default_factory=dict)
    research_value_score: int = 0
    diversity_features: list[str] = field(default_factory=list)
    read_lib_similarity: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "paper": self.paper.to_dict(),
            "quality_score": self.quality_score,
            "decision": self.decision,
            "reasons": self.reasons,
            "matched_terms": self.matched_terms,
            "penalties": self.penalties,
            "focus_tracks": self.focus_tracks,
            "focus_matches": self.focus_matches,
            "research_value_score": self.research_value_score,
            "diversity_features": self.diversity_features,
            "read_lib_similarity": self.read_lib_similarity,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RankedPaper":
        return cls(
            paper=ArxivPaper.from_dict(data.get("paper", {})),
            quality_score=int(data.get("quality_score", 0)),
            decision=str(data.get("decision", BELOW_REVIEW_DECISION)),
            reasons=list(data.get("reasons", []) or []),
            matched_terms=list(data.get("matched_terms", []) or []),
            penalties=list(data.get("penalties", []) or []),
            focus_tracks=list(data.get("focus_tracks", []) or []),
            focus_matches=dict(data.get("focus_matches", {}) or {}),
            research_value_score=int(data.get("research_value_score", 0)),
            diversity_features=list(data.get("diversity_features", []) or []),
            read_lib_similarity=float(data.get("read_lib_similarity", 0.0) or 0.0),
        )


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()


def paper_text(paper: ArxivPaper) -> str:
    values = [
        paper.title,
        paper.summary,
        paper.comment,
        paper.journal_ref,
        " ".join(paper.categories),
        paper.primary_category,
    ]
    return " ".join(values).lower()


def _count_matches(text: str, terms: list[str]) -> list[str]:
    return [term for term in terms if term and term.lower() in text]


def _focus_track_matches(text: str) -> dict[str, list[str]]:
    matches_by_track: dict[str, list[str]] = {}
    for track, config in FOCUS_TRACK_TERMS.items():
        matches = _count_matches(text, config["terms"])
        if len(matches) < 2:
            continue
        anchors = set(config["anchor_terms"])
        if not any(match in anchors for match in matches):
            continue
        matches_by_track[track] = matches
    return matches_by_track


def _parse_date(value: str) -> date | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def _recency_score(paper: ArxivPaper) -> tuple[int, str | None]:
    paper_date = _parse_date(paper.updated) or _parse_date(paper.published)
    if paper_date is None:
        return 0, None
    age_days = (datetime.now(timezone.utc).date() - paper_date).days
    if age_days <= 7:
        return 5, "very_recent"
    if age_days <= 30:
        return 3, "recent"
    if age_days <= 90:
        return 1, "recent_quarter"
    return 0, None


def _venue_hit(venue_text: str, venues: dict[str, list[str]]) -> str | None:
    for label, aliases in venues.items():
        for alias in aliases:
            if re.search(rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])", venue_text):
                return label
    return None


def _confirmed_venue(venue_text: str) -> bool:
    if not venue_text:
        return False
    if any(term in venue_text for term in NON_ACCEPTED_TERMS):
        return False
    return any(term in venue_text for term in ACCEPTED_TERMS) or bool(re.search(r"\b20\d{2}\b", venue_text))


def _robotics_anchor_hits(text: str, paper: ArxivPaper) -> list[str]:
    hits = _count_matches(text, ROBOTICS_ANCHOR_TERMS)
    categories = " ".join(paper.categories).lower()
    if paper.primary_category == "cs.RO" or "cs.ro" in categories:
        hits.append("cs.RO")
    return sorted(set(hits))


def _strong_robotics_anchor_hits(text: str, paper: ArxivPaper) -> list[str]:
    hits = _count_matches(text, STRONG_ROBOTICS_ANCHOR_TERMS)
    categories = " ".join(paper.categories).lower()
    if paper.primary_category == "cs.RO" or "cs.ro" in categories:
        hits.append("cs.RO")
    return sorted(set(hits))


def _non_robotics_cv_hits(text: str) -> list[str]:
    return _count_matches(text, NON_ROBOTICS_CV_TERMS)


def _research_value_features(text: str) -> tuple[int, list[str]]:
    matches = _count_matches(text, RESEARCH_VALUE_TERMS)
    score = min(30, len(matches) * 5)
    features = [
        label
        for label, terms in DIVERSITY_FEATURE_TERMS.items()
        if _count_matches(text, terms)
    ]
    return score, sorted(set(features))


def _is_robotics_related(domain_labels: set[str], text: str, paper: ArxivPaper) -> bool:
    anchor_hits = _robotics_anchor_hits(text, paper)
    strong_anchor_hits = _strong_robotics_anchor_hits(text, paper)
    if not anchor_hits:
        return False
    if _non_robotics_cv_hits(text) and not strong_anchor_hits:
        return False
    if domain_labels & {"embodied_ai", "robot_learning", "bimanual", "dlo", "tactile", "planning", "action_interface", "robustness_recovery"}:
        return True
    return bool(domain_labels & {"manipulation", "vla_vlm", "sim_to_real", "diffusion"})


def _venue_auto_import_label(paper: ArxivPaper, domain_labels: set[str], text: str) -> str | None:
    venue_text = f"{paper.comment} {paper.journal_ref}".lower()
    if not _confirmed_venue(venue_text):
        return None
    robotics_hit = _venue_hit(venue_text, ROBOTICS_TOP_VENUES)
    if robotics_hit and _is_robotics_related(domain_labels, text, paper):
        return robotics_hit
    ml_vision_hit = _venue_hit(venue_text, ML_VISION_TOP_VENUES)
    if ml_vision_hit and domain_labels & {"vla_vlm", "robot_learning", "embodied_ai", "manipulation"}:
        return ml_vision_hit
    return None


def _batch_read_lib_similarity(papers: list[ArxivPaper]) -> dict[int, float]:
    """Embed all candidate papers in one batch and score each against the read
    library anchor. Returns {id(paper): similarity}. If the embedding backend is
    unavailable the whole batch degrades to an empty dict -- a single failure,
    never a per-paper timeout walked across the entire candidate list."""
    if not ENABLE_READ_LIB_SIMILARITY or not papers:
        return {}
    try:
        from kb_embed import embed_texts, load_read_lib_anchor, query_vector_similar

        matrix = load_read_lib_anchor()
        qvecs = embed_texts([f"{paper.title}\n\n{paper.summary}" for paper in papers], is_query=True)
    except EmbeddingUnavailable:
        return {}
    sims: dict[int, float] = {}
    for paper, qvec in zip(papers, qvecs):
        hits = query_vector_similar(qvec, matrix, top_k=10)
        if hits:
            sims[id(paper)] = float(sum(score for _row, score in hits) / len(hits))
    return sims


def rank_paper(paper: ArxivPaper, read_lib_sim: float = 0.0) -> RankedPaper:
    text = paper_text(paper)
    matched_terms: list[str] = []
    reasons: list[str] = []
    penalties: list[str] = []
    domain_labels: set[str] = set()
    score = 0
    robotics_anchor_hits = _robotics_anchor_hits(text, paper)
    strong_robotics_anchor_hits = _strong_robotics_anchor_hits(text, paper)
    non_robotics_cv_hits = _non_robotics_cv_hits(text)
    research_value_score, diversity_features = _research_value_features(text)

    domain_score = 0
    for label, terms in DOMAIN_TERMS.items():
        matches = _count_matches(text, terms)
        if not matches:
            continue
        domain_labels.add(label)
        matched_terms.extend(matches[:3])
        if label == "manipulation" and not robotics_anchor_hits:
            domain_score += 2
        elif label in {"embodied_ai", "robot_learning", "manipulation"}:
            domain_score += 8
        elif label in {"vla_vlm", "action_interface", "sim_to_real", "robustness_recovery", "tactile", "bimanual", "dlo", "diffusion", "planning"}:
            domain_score += 6
        reasons.append(f"domain:{label}")
    score += min(domain_score, 35)

    fit_score = 0
    for label in ("vla_vlm", "action_interface", "tactile", "sim_to_real", "robustness_recovery", "dlo", "bimanual", "diffusion", "planning"):
        if _count_matches(text, DOMAIN_TERMS[label]):
            fit_score += 5
    if _count_matches(text, DOMAIN_TERMS["manipulation"]) and robotics_anchor_hits:
        fit_score += 5
    score += min(fit_score, 20)
    if fit_score:
        reasons.append("research_direction_fit")

    experiment_matches = _count_matches(text, EXPERIMENT_TERMS)
    if experiment_matches:
        matched_terms.extend(experiment_matches[:5])
        score += min(5 + len(experiment_matches) * 3, 20)
        reasons.append("experiment_signal")

    repro_matches = _count_matches(text, REPRO_TERMS)
    if repro_matches:
        matched_terms.extend(repro_matches[:3])
        score += min(4 + len(repro_matches) * 2, 10)
        reasons.append("reproducibility_signal")
    if research_value_score:
        reasons.append(f"research_value_signal:{research_value_score}")

    venue_text = f"{paper.comment} {paper.journal_ref}".lower()
    venue_matches = _count_matches(venue_text, VENUE_TERMS)
    confirmed_top_venue = bool(venue_matches) and _confirmed_venue(venue_text)
    if confirmed_top_venue:
        matched_terms.extend(venue_matches[:3])
        score += 25
        reasons.append("confirmed_top_venue_accepted")
    elif venue_matches:
        matched_terms.extend(venue_matches[:3])
        score += min(6 + len(venue_matches), 10)
        reasons.append("venue_or_comment_signal")
    elif "cs.ro" in " ".join(paper.categories).lower() or paper.primary_category == "cs.RO":
        score += 4
        reasons.append("cs_ro_category")

    recency_points, recency_reason = _recency_score(paper)
    score += recency_points
    if recency_reason:
        reasons.append(recency_reason)

    if not robotics_anchor_hits:
        score -= 20
        penalties.append("weak_robotics_signal")
    if non_robotics_cv_hits and not strong_robotics_anchor_hits:
        score -= 30
        penalties.append("non_robotics_cv_context")
        matched_terms.extend(non_robotics_cv_hits[:5])
    if len(paper.summary) < 300:
        score -= 5
        penalties.append("short_abstract")
    if _count_matches(text, PENALTY_TERMS) and "benchmark" not in text:
        score -= 8
        penalties.append("survey_or_review")

    focus_matches = _focus_track_matches(text)
    if focus_matches:
        for track, matches in focus_matches.items():
            bonus = min(18, 8 + len(matches) * 2)
            score += bonus
            reasons.append(f"focus_track:{track}")
            reasons.append(f"focus_track_bonus:{track}:{bonus}")
            matched_terms.extend(matches[:8])

    read_lib_similarity = 0.0
    if ENABLE_READ_LIB_SIMILARITY and read_lib_sim > 0.0:
        read_lib_similarity = read_lib_sim
        score += min(15, round(read_lib_similarity * 25))
        reasons.append(f"read_lib_similarity:{read_lib_similarity:.2f}")

    score = max(0, min(100, score))
    venue_auto_label = _venue_auto_import_label(paper, domain_labels, text)
    if venue_auto_label:
        decision = "venue_auto_import"
        reasons.append(f"venue_auto_import:{venue_auto_label}")
        if score >= TOP1_THRESHOLD:
            reasons.append("top1_score")
    elif score >= TOP1_THRESHOLD:
        decision = "top1_candidate"
    elif focus_matches and score >= FOCUS_REVIEW_THRESHOLD:
        decision = FOCUS_REVIEW_DECISION
    elif score >= REVIEW_THRESHOLD:
        decision = "review_queue"
    else:
        decision = BELOW_REVIEW_DECISION

    return RankedPaper(
        paper=paper,
        quality_score=score,
        decision=decision,
        reasons=sorted(set(reasons)),
        matched_terms=sorted(set(matched_terms)),
        penalties=sorted(set(penalties)),
        focus_tracks=sorted(focus_matches),
        focus_matches={track: sorted(set(matches)) for track, matches in focus_matches.items()},
        research_value_score=research_value_score,
        diversity_features=diversity_features,
        read_lib_similarity=read_lib_similarity,
    )


def rank_papers(papers: list[ArxivPaper]) -> list[RankedPaper]:
    read_lib_sims = _batch_read_lib_similarity(papers)
    ranked = [rank_paper(paper, read_lib_sims.get(id(paper), 0.0)) for paper in papers]
    return sorted(ranked, key=lambda item: (-item.quality_score, item.paper.updated, item.paper.title))
