"""Fail-closed Abaddon Generation-2 reviewed-campaign policy contract.

Parallel to the frozen Generation-1 contract. It imports only the frozen
Generation-2 candidate-252 plan and does not execute matches, admit training
data, mutate weights, or promote a genome.
"""

from __future__ import annotations

from .abaddon_policy_campaign_contract import (
    ABADDON_REFINER_SHA256,
    CONTRACT_SCHEMA,
    FUNDAMENTALS,
    MAX_SINGLE_FUNDAMENTAL_REGRESSION,
    MIN_APOLLYON_SNAPSHOTS,
    MIN_COMPOSITE_GAIN,
    MIN_REVIEWED_MATCHES,
    MIN_VARIED_SEEDS,
    promotion_recommendation,
    stable_json,
    validate_generation_review,
)
from .abaddon_policy_campaign_plan_generation2 import precommitted_campaign_plan
from .apollyon_opponent_runtime_realizations import (
    reviewed_opponent_runtime_realizations,
)
from .apollyon_opponent_snapshots import reviewed_snapshot_set


def reviewed_plan() -> dict:
    """Return frozen pre-execution requirements for Generation 2 candidate 252."""
    snapshots = reviewed_snapshot_set()
    campaign_plan = precommitted_campaign_plan()
    runtime_realizations = reviewed_opponent_runtime_realizations()
    return {
        "schema": CONTRACT_SCHEMA,
        "abaddon_refiner_sha256": ABADDON_REFINER_SHA256,
        "candidate_only": True,
        "status": (
            "READY_PENDING_RUNTIME_EXECUTION_AUTHORIZATION"
            if snapshots["previous_champion_proven"]
            and runtime_realizations["opponent_runtime_realization_complete"]
            else "BLOCKED_PENDING_OPPONENT_RUNTIME_REALIZATION"
            if snapshots["previous_champion_proven"]
            else "BLOCKED_PENDING_PREVIOUS_CHAMPION_PROOF"
        ),
        "opponent_snapshot_set": snapshots,
        "opponent_runtime_realizations": runtime_realizations,
        "precommitted_campaign_plan": campaign_plan,
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
            "previous_champion_binding_complete": snapshots["previous_champion_proven"],
            "campaign_attempt_ledger_required": True,
            "campaign_attempt_ledger_complete": True,
            "candidate_frozen_before_campaign_evidence": True,
            "pair_arms_precommitted": True,
            "opponent_runtime_realization_source_binding_complete": True,
            "opponent_runtime_realization_complete": (
                runtime_realizations["opponent_runtime_realization_complete"]
            ),
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
