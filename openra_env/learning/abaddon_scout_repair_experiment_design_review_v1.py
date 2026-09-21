"""Source-only review of the fresh scout-repair experiment design.

This review selects topology, not a live slot, seed, opponent implementation, or
runtime permit. The pair-03 evidence showed an Apollyon model-action divergence
before the relevant late scouting behavior, so the initial causal canary must use
one separately reviewed, source-bound deterministic opponent implementation.
A later model-backed validation is a distinct gate.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import abaddon_scout_repair_experiment_request_v1 as request

SCHEMA = "void.abaddon.scout-repair-experiment-design-review.v1"
NEXT_GATE = "SCOUT_REPAIR_CANARY_SOURCE_AND_AUTHORITY_DESIGN_REQUIRED"


class ScoutRepairExperimentDesignHold(ValueError):
    pass


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutRepairExperimentDesignHold(reason)


def scout_repair_experiment_design_review() -> dict[str, Any]:
    proposal = request.scout_repair_experiment_request_contract()
    record = proposal["request"]
    _require(proposal["request_bytes_valid"] is True, "request_not_validated")
    _require(all(value is False for value in proposal["authority"].values()), "request_carries_authority")
    _require(record["historical_evidence_reference"]["shared_scouting_defect_reproduced"] is True,
             "shared_defect_not_bound")
    _require(record["historical_evidence_reference"]["candidate_252_superiority_established"] is False,
             "candidate252_superiority_unexpected")
    _require(record["proposed_experiment"]["candidate252_policy_mutations_included"] is False,
             "candidate252_mutations_leaked_into_repair_test")
    _require(record["proposed_experiment"]["campaign_pair_slot"] is None,
             "legacy_campaign_slot_prematurely_selected")
    _require(record["proposed_experiment"]["seed"] is None, "seed_prematurely_selected")
    _require(record["proposed_experiment"]["opponent_runtime_identity"] is None,
             "opponent_prematurely_selected")

    design = {
        "schema": SCHEMA,
        "request_sha256": proposal["request_sha256"],
        "repair_reviewed_head": request.PR181_HEAD,
        "repair_reviewed_tree": request.PR181_TREE,
        "experiment_namespace": "abaddon-scout-repair-canary-v1",
        "generation2_candidate_campaign_slot_reused": False,
        "pair03_attempt_or_result_reused": False,
        "held_out_campaign_space_used": False,
        "stage": "initial_causal_canary",
        "arm_count": 2,
        "arms": (
            {
                "arm": "legacy_control",
                "abaddon_doctrine": "FEINTER",
                "controller_policy": "controller_defaults",
                "scout_mission_lifecycle_enabled": False,
                "candidate252_policy_mutations_included": False,
            },
            {
                "arm": "scout_repair_treatment",
                "abaddon_doctrine": "FEINTER",
                "controller_policy": "controller_defaults",
                "scout_mission_lifecycle_enabled": True,
                "candidate252_policy_mutations_included": False,
            },
        ),
        "pair_binding_requirements": {
            "same_seed": True,
            "same_opponent_implementation": True,
            "same_opponent_source_identity": True,
            "same_warm_start_contract": True,
            "same_round_limit": True,
            "same_ticks_per_round": True,
            "same_runtime_image": True,
            "same_engine_source": True,
            "same_war_college_source_except_declared_treatment": True,
        },
        "opponent_requirements": {
            "initial_canary_model_backed_opponent_allowed": False,
            "deterministic_source_bound_opponent_required": True,
            "reason": "pair03_first_action_divergence_was_apollyon_model_choice_before_late_scouting_isolation",
            "specific_opponent_selected": False,
            "later_model_backed_validation_is_separate_gate": True,
        },
        "runner_requirements": {
            "scripted_warm_start_reused": True,
            "unchanged_host_validator_reused": True,
            "unchanged_joint_advance_reused": True,
            "model_service_start_allowed": False,
            "model_inference_allowed": False,
            "explicit_deterministic_opponent_identity_required": True,
            "historical_actual_apollyon_label_accepted": False,
            "controller_rows_training_candidate": False,
            "warm_start_rows_training_candidate": False,
            "automatic_corpus_admission": False,
            "canary_result_schema_must_be_distinct_from_pair03": True,
        },
        "canary_limits": {
            "live_control_runs": 1,
            "live_treatment_runs": 1,
            "maximum_total_game_runs": 2,
            "maximum_automatic_retries": 0,
            "retry_after_consumption_requires_new_explicit_review": True,
            "automatic_training": False,
            "automatic_policy_promotion": False,
        },
        "evidence_to_compare": (
            "outcome_and_rounds",
            "observed_scout_missions_issued_completed_failed_interrupted",
            "unique_observed_scout_arrivals",
            "accepted_shared_clock_noop_decisions",
            "idle_combat_capable_units_during_noop",
            "explored_percent",
            "contact_response_actions",
            "units_killed_and_lost",
            "kills_cost_and_deaths_cost",
            "command_rejections",
            "runtime_cleanup_and_post_run_dormancy",
        ),
        "causal_claim_limits": {
            "one_canary_pair_establishes_general_performance_superiority": False,
            "dispatch_establishes_arrival": False,
            "sampled_arrival_establishes_action_causation": False,
            "successful_cleanup_callback_establishes_runtime_dormancy": False,
        },
        "unresolved": {
            "accepted_main_head_with_repair": None,
            "fresh_seed": None,
            "deterministic_opponent_source_identity": None,
            "runtime_image_identity": None,
            "attempt_directory_and_marker_names": None,
            "control_and_treatment_invocation_sources": None,
            "post_run_evidence_contract": None,
        },
        "authority": deepcopy(record["authority"]),
        "execution_authorized": False,
        "execution_performed": False,
        "next_gate": NEXT_GATE,
    }
    _require(all(value is False for value in design["authority"].values()), "review_authority_drift")
    return design


def authorize_or_execute_canary(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairExperimentDesignHold(NEXT_GATE)
