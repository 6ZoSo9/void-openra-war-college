"""Fail-closed Abaddon reviewed-campaign policy contract.

This mirrors the recovered deterministic Abaddon refiner review/promotion
requirements.  It does not execute matches, admit training data, mutate weights,
or promote a genome.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from typing import Any

from .apollyon_opponent_snapshots import reviewed_snapshot_set

CONTRACT_SCHEMA = "void.abaddon.policy-campaign-contract.v1"
DUEL_REVIEW_SCHEMA = "void.abaddon.duel-generation-review.v1"
PROMOTION_SCHEMA = "void.abaddon.policy-promotion-recommendation.v1"

# Exact recovered refiner source identity already bound by the candidate wrapper.
ABADDON_REFINER_SHA256 = (
    "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
)

MIN_REVIEWED_MATCHES = 12
MIN_VARIED_SEEDS = 6
MIN_APOLLYON_SNAPSHOTS = 2
MIN_COMPOSITE_GAIN = 0.02
MAX_SINGLE_FUNDAMENTAL_REGRESSION = 0.08

FUNDAMENTALS = (
    "intelligence",
    "economy",
    "tempo",
    "force_preservation",
    "micro",
    "adaptation",
    "command_efficiency",
    "outcome",
)


class CampaignContractError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CampaignContractError(message)


def _finite_number(value: Any, label: str) -> float:
    _require(
        type(value) in (int, float) and math.isfinite(float(value)),
        f"{label} must be finite number",
    )
    return float(value)


def _int(value: Any, label: str, minimum: int = 0) -> int:
    _require(
        type(value) is int and value >= minimum,
        f"{label} must be integer >= {minimum}",
    )
    return value


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be object")
    return value


def stable_json(value: Mapping[str, Any]) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"


def reviewed_plan() -> dict[str, Any]:
    """Return the frozen pre-execution requirements for one Abaddon generation."""
    snapshots = reviewed_snapshot_set()
    return {
        "schema": CONTRACT_SCHEMA,
        "abaddon_refiner_sha256": ABADDON_REFINER_SHA256,
        "candidate_only": True,
        "status": "BLOCKED_PENDING_PREVIOUS_CHAMPION_PROOF",
        "opponent_snapshot_set": snapshots,
        "requirements": {
            "full_abaddon_controller_active": True,
            "safety_invariants_green": True,
            "minimum_reviewed_matches": MIN_REVIEWED_MATCHES,
            "minimum_varied_seeds": MIN_VARIED_SEEDS,
            "minimum_apollyon_snapshots": MIN_APOLLYON_SNAPSHOTS,
            "infrastructure_failures_required": 0,
            "minimum_composite_gain": MIN_COMPOSITE_GAIN,
            "maximum_single_fundamental_regression":
                MAX_SINGLE_FUNDAMENTAL_REGRESSION,
            "fundamentals": list(FUNDAMENTALS),
        },
        "anti_overfit": {
            "evaluate_against_current_apollyon": True,
            "evaluate_against_previous_apollyon_champion": True,
            "retain_baseline_opponents": True,
            "held_out_seed_evaluation": True,
        },
        "pre_execution_gates": {
            "opponent_snapshot_binding_required": True,
            "opponent_snapshot_source_binding_complete": True,
            "previous_champion_binding_required": True,
            "previous_champion_binding_complete": False,
            "campaign_attempt_ledger_required": True,
            "pair_evidence_required": True,
            "manual_review_required": True,
        },
        "authority": {
            "runtime_execution_authorized": False,
            "training_use_approved": False,
            "automatic_training_admission": False,
            "automatic_weight_mutation": False,
            "automatic_policy_promotion": False,
        },
    }


def validate_generation_review(review: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the exact recovered refiner's reviewed-generation prerequisites."""
    review = _obj(review, "review")
    _require(
        review.get("schema") == DUEL_REVIEW_SCHEMA,
        "unexpected duel review schema",
    )
    _require(
        review.get("full_abaddon_controller_active") is True,
        "proxy matches cannot qualify reviewed Abaddon policy",
    )
    _require(review.get("review_complete") is True, "review not complete")
    _require(
        review.get("safety_invariants_green") is True,
        "safety invariants not green",
    )

    matches = _int(review.get("matches"), "matches")
    varied_seed_count = _int(review.get("varied_seed_count"), "varied_seed_count")
    opponent_snapshot_count = _int(
        review.get("opponent_snapshot_count"),
        "opponent_snapshot_count",
    )
    infra_failures = _int(review.get("infra_failures"), "infra_failures")

    _require(
        matches >= MIN_REVIEWED_MATCHES,
        f"at least {MIN_REVIEWED_MATCHES} reviewed matches required",
    )
    _require(
        varied_seed_count >= MIN_VARIED_SEEDS,
        f"at least {MIN_VARIED_SEEDS} varied seeds required",
    )
    _require(
        opponent_snapshot_count >= MIN_APOLLYON_SNAPSHOTS,
        f"at least {MIN_APOLLYON_SNAPSHOTS} Apollyon snapshots required",
    )
    _require(infra_failures == 0, "infrastructure failures must be zero")

    composite_score = _finite_number(
        review.get("composite_score"),
        "composite_score",
    )
    fundamentals_raw = _obj(review.get("fundamentals"), "fundamentals")
    fundamentals = {
        name: _finite_number(fundamentals_raw.get(name), f"fundamentals.{name}")
        for name in FUNDAMENTALS
    }

    return {
        "schema": DUEL_REVIEW_SCHEMA,
        "full_abaddon_controller_active": True,
        "review_complete": True,
        "safety_invariants_green": True,
        "matches": matches,
        "varied_seed_count": varied_seed_count,
        "opponent_snapshot_count": opponent_snapshot_count,
        "infra_failures": 0,
        "composite_score": composite_score,
        "fundamentals": fundamentals,
    }


def promotion_recommendation(
    champion_review: Mapping[str, Any],
    candidate_review: Mapping[str, Any],
    *,
    min_gain: float = MIN_COMPOSITE_GAIN,
    max_dimension_regression: float = MAX_SINGLE_FUNDAMENTAL_REGRESSION,
) -> dict[str, Any]:
    """Mirror the recovered refiner's recommendation logic; never promote."""
    champion = validate_generation_review(champion_review)
    candidate = validate_generation_review(candidate_review)

    min_gain = _finite_number(min_gain, "min_gain")
    max_dimension_regression = _finite_number(
        max_dimension_regression,
        "max_dimension_regression",
    )
    _require(min_gain >= 0.0, "min_gain must be >= 0")
    _require(
        max_dimension_regression >= 0.0,
        "max_dimension_regression must be >= 0",
    )

    regressions: dict[str, float] = {}
    for name in FUNDAMENTALS:
        amount = champion["fundamentals"][name] - candidate["fundamentals"][name]
        if amount > max_dimension_regression:
            regressions[name] = amount

    gain = candidate["composite_score"] - champion["composite_score"]
    recommend = gain >= min_gain and not regressions

    return {
        "schema": PROMOTION_SCHEMA,
        "recommend_promotion": recommend,
        "automatic_promotion": False,
        "composite_gain": gain,
        "minimum_required_gain": min_gain,
        "dimension_regressions": regressions,
        "max_dimension_regression": max_dimension_regression,
        "reason": (
            "CANDIDATE_BEATS_CHAMPION_WITHOUT_MATERIAL_REGRESSION"
            if recommend
            else "PROMOTION_GATE_NOT_MET"
        ),
    }
