"""Source-only runner requirements for a future scout-repair causal canary.

This module is a contract, not a runner. It does not import the historical duel
runner, open a file, start a model/service, create a session, dispatch a command,
or grant execution authority. It binds the already reviewed canary seed and
opponent identity to a minimal set of runner requirements that a later source
implementation must satisfy before any live authorization can be considered.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import abaddon_scout_canary_opponent_source_binding_review_v1 as opponent_review
from openra_env.learning import abaddon_scout_repair_canary_source_design_v1 as source_design

SCHEMA = "void.abaddon.scout-repair-canary-runner-requirements.v1"
NEXT_GATE = "SCOUT_REPAIR_CANARY_RUNNER_IMPLEMENTATION_SOURCE_REVIEW_REQUIRED"
ARMS = ("legacy_control", "scout_repair_treatment")


class ScoutRepairCanaryRunnerRequirementsHold(ValueError):
    pass


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutRepairCanaryRunnerRequirementsHold(reason)


def scout_repair_canary_runner_requirements() -> dict[str, Any]:
    design = source_design.scout_repair_canary_source_design()
    opponent = opponent_review.scout_repair_opponent_source_binding_review()
    seed = design["seed_derivation"]["seed"]
    source_identity = opponent["opponent"]["source_identity"]
    _require(type(seed) is int and seed > 0, "seed_not_bound")
    _require(type(source_identity) is dict and source_identity.get("sha256"), "opponent_not_bound")
    _require(opponent["opponent"].get("model_backed") is False, "model_backed_opponent_forbidden")
    _require(opponent.get("execution_authorized") is False, "prior_stage_carries_authority")
    return {
        "schema": SCHEMA,
        "experiment_namespace": design["experiment_namespace"],
        "arms": ARMS,
        "seed": seed,
        "opponent_source_identity": deepcopy(source_identity),
        "shared_arm_bindings": {
            "same_seed": True,
            "same_deterministic_opponent_source": True,
            "same_warm_start_recipe": True,
            "same_runtime_image_required": True,
            "same_engine_commit_required": True,
            "same_war_college_commit_required": True,
            "same_ticks_per_round_required": True,
        },
        "control": {
            "abaddon_doctrine": "FEINTER",
            "controller_defaults_only": True,
            "candidate252_mutations_included": False,
            "scout_lifecycle_repair_enabled": False,
        },
        "treatment": {
            "abaddon_doctrine": "FEINTER",
            "controller_defaults_only": True,
            "candidate252_mutations_included": False,
            "scout_lifecycle_repair_enabled": True,
        },
        "opponent_execution_contract": {
            "proposal_function": "propose_deterministic_pressure_action",
            "typed_current_turn_tool_contract_required": True,
            "proposal_called_once_per_controller_round": True,
            "unchanged_host_validator_required": True,
            "invalid_proposal_becomes_advance": False,
            "invalid_proposal_retried_automatically": False,
            "world_mutated_before_host_validation": False,
            "model_service_start_required": False,
            "model_service_start_forbidden": True,
            "model_inference_required": False,
            "model_inference_forbidden": True,
            "historical_actual_apollyon_label_allowed": False,
            "deterministic_opponent_identity_must_be_logged": True,
        },
        "evidence_label_contract": {
            "controller_rows_training_candidate": False,
            "warm_start_rows_training_candidate": False,
            "automatic_corpus_admission": False,
            "automatic_policy_promotion": False,
            "canary_only": True,
            "historical_pair03_result_schema_reuse_allowed": False,
        },
        "attempt_contract": {
            "control_attempts": 1,
            "treatment_attempts": 1,
            "maximum_total_game_runs": 2,
            "automatic_retries": 0,
            "separate_create_only_arm_markers_required": True,
            "shared_marker_between_arms_allowed": False,
            "pair03_marker_reuse_allowed": False,
            "uncertain_or_consumed_arm_may_rerun_without_new_review": False,
        },
        "post_run_contract": {
            "independent_runtime_dormancy_observation_required": True,
            "independent_container_absence_observation_required": True,
            "source_and_baseline_preservation_observation_required": True,
            "callback_return_counts_as_cleanup_proof": False,
            "descriptive_result_contract_required": True,
        },
        "accepted_main_head_with_repair": None,
        "runtime_image_identity": None,
        "runner_implementation_source_identity": None,
        "attempt_guard_source_identity": None,
        "invocation_source_identities": None,
        "execution_authorized": False,
        "execution_performed": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "next_gate": NEXT_GATE,
    }


def validate_runner_implementation_claim(claim: Mapping[str, Any]) -> dict[str, Any]:
    """Validate only a source-review claim shape; success grants no authority."""
    _require(type(claim) is dict, "implementation_claim_object_required")
    expected = scout_repair_canary_runner_requirements()
    _require(claim.get("schema") == "void.abaddon.scout-repair-canary-runner-implementation-review.v1",
             "implementation_claim_schema")
    _require(claim.get("experiment_namespace") == expected["experiment_namespace"], "namespace_drift")
    _require(claim.get("seed") == expected["seed"], "seed_drift")
    _require(claim.get("opponent_source_sha256") == expected["opponent_source_identity"]["sha256"],
             "opponent_source_drift")
    for field in (
        "model_service_start_implemented", "model_inference_implemented",
        "automatic_retry_implemented", "training_admission_implemented",
        "automatic_policy_promotion_implemented", "execution_authority_created",
    ):
        _require(claim.get(field) is False, "forbidden_capability:" + field)
    for field in (
        "typed_current_turn_tool_contract_used", "unchanged_host_validator_used",
        "deterministic_opponent_identity_logged", "controller_rows_nontraining",
        "separate_arm_attempt_markers_designed", "independent_post_run_observation_required",
    ):
        _require(claim.get(field) is True, "missing_requirement:" + field)
    return {
        "schema": "void.abaddon.scout-repair-canary-runner-implementation-admission.v1",
        "source_review_claim_valid": True,
        "execution_authorized": False,
        "execution_performed": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairCanaryRunnerRequirementsHold(NEXT_GATE)
