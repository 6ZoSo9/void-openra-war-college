"""Source-only combat-utility and rejection diagnostic for pair-06 V8.

This contract binds the successful 36-round GPU-gated pair-06 baseline result
and the exact operator terminal captured for that run. It records only
trace-supported diagnostic facts.

Observed distinction:
- the Apollyon tool contract accepted one action on the first attempt in every
  controller round, so the trace does not support tool rejection/retry failure
  as the explanation for the result;
- the accepted Apollyon action mix was structure-heavy early and then mostly
  advance, while its combat-unit count fell from four to zero by round seven
  and remained zero through round 36.

This does not prove why the controller chose that action mix. Tool-availability,
policy-ranking, reward-shaping, state interpretation, or other deeper causes
remain separate hypotheses. No policy change, retry, training, promotion,
deployment, or runtime execution is authorized here.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_result_source_binding_review_generation2
    as result_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-post-run-combat-utility-rejection-diagnostic-contract.v1"
)

RESULT_REVIEW_MAIN_HEAD = "4d666f0157c09a002b3d9897d09f550dc55e3656"
RESULT_REVIEW_GIT_BLOB = "2ca3aa48919193ed57703a6446372cb4ae6414c7"

RUN_TERMINAL_SHA256 = (
    "25378d215a7bd5cf8e3192030d8bb3b89b429dacda7bb61c2ff4c58090a2f5a8"
)
RUN_TERMINAL_BYTES = 23772

ATTEMPT_MARKER_SHA256 = (
    "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
)
TRAJECTORY_SHA256 = (
    "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
)
SUMMARY_SHA256 = (
    "ae9692fbddd48fb95b9ee1d4737b1ad6ed1aae3ddb2eff80c45a7efde548b6f8"
)

APOLLYON_ACTION_COUNTS = {
    "advance": 25,
    "build_structure_dome": 1,
    "build_structure_gun": 2,
    "build_structure_hbox": 1,
    "build_structure_pbox": 1,
    "build_structure_powr": 1,
    "build_structure_proc": 1,
    "build_structure_silo": 2,
    "build_structure_tent": 1,
    "build_structure_weap": 1,
}
ABADDON_ACTION_COUNTS = {
    "advance": 23,
    "attack_target": 5,
    "build_and_place": 1,
    "build_unit": 1,
    "move_units": 6,
}

NEXT_GATE = "PAIR06_V8_COMBAT_ACTION_PRIORITY_HYPOTHESIS_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_combat_action_priority_hypothesis"


class Pair06V8PostRunCombatUtilityRejectionDiagnosticHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PostRunCombatUtilityRejectionDiagnosticHold(message)


@lru_cache(maxsize=1)
def _validated_result() -> dict[str, Any]:
    out = result_review.pair06_v8_preclaim_gpu_execution_result_review_contract()

    _require(
        out.get("pair06_v8_preclaim_gpu_execution_result_reviewed") is True,
        "pair06 result review missing",
    )
    _require(
        out.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "pair06 attempt marker drift",
    )
    _require(
        out.get("outcome") == "DRAW_OR_UNFINISHED"
        and out.get("rounds_completed") == 36
        and out.get("final_tick") == 3551
        and out.get("model_inference_count") == 36,
        "pair06 terminal drift",
    )
    _require(
        out.get("attempt_consumed") is True
        and out.get("authorization_reusable") is False,
        "pair06 one-shot closeout drift",
    )
    for field in (
        "candidate_execution_performed",
        "held_out_execution_performed",
        "automatic_retry_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(out.get(field) is False, "pair06 boundary drift: " + field)

    _require(
        out.get("next_gate")
        == "PAIR06_V8_POST_RUN_COMBAT_UTILITY_AND_REJECTION_DIAGNOSTIC_REQUIRED",
        "pair06 diagnostic frontier drift",
    )
    return deepcopy(out)


def pair06_v8_post_run_combat_utility_rejection_diagnostic_contract() -> dict[str, Any]:
    reviewed = _validated_result()
    return {
        "schema": CONTRACT_SCHEMA,
        "result_review_main_head": RESULT_REVIEW_MAIN_HEAD,
        "result_review_git_blob": RESULT_REVIEW_GIT_BLOB,
        "run_terminal_sha256": RUN_TERMINAL_SHA256,
        "run_terminal_bytes": RUN_TERMINAL_BYTES,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "controller_rounds": 36,
        "apollyon_tool_contract_accepted_rounds": 36,
        "apollyon_total_tool_attempts": 36,
        "apollyon_max_attempts_for_accepted_action": 1,
        "apollyon_rounds_requiring_tool_retry": 0,
        "tool_rejection_or_retry_failure_observed": False,
        "apollyon_offered_tool_count_max": 30,
        "apollyon_offered_tool_count_min": 16,
        "apollyon_action_counts": deepcopy(APOLLYON_ACTION_COUNTS),
        "abaddon_action_counts": deepcopy(ABADDON_ACTION_COUNTS),
        "apollyon_structure_build_actions": 11,
        "apollyon_advance_actions": 25,
        "apollyon_explicit_attack_target_actions": 0,
        "apollyon_explicit_move_units_actions": 0,
        "apollyon_explicit_unit_build_actions": 0,
        "first_controller_visibility_round": 2,
        "peak_mutual_visibility_round": 3,
        "peak_mutual_visibility": (4, 4),
        "first_apollyon_combat_count_drop_round": 4,
        "apollyon_combat_count_at_controller_start": 4,
        "abaddon_combat_count_at_controller_start": 4,
        "apollyon_combat_count_zero_round": 7,
        "combat_counts_at_round_7": (0, 6),
        "apollyon_zero_combat_rounds_7_through_36": 30,
        "combat_counts_at_round_36": (0, 6),
        "reported_kills_field_at_round_36": (0, 400),
        "outcome": "DRAW_OR_UNFINISHED",
        "diagnostic_classification": (
            "combat_utility_action_mix_not_tool_rejection"
        ),
        "trace_supports_combat_utility_deficit": True,
        "trace_supports_protocol_rejection_failure": False,
        "causal_root_cause_proven": False,
        "tool_availability_root_cause_proven": False,
        "policy_ranking_root_cause_proven": False,
        "reward_shaping_root_cause_proven": False,
        "state_interpretation_root_cause_proven": False,
        "policy_change_authorized": False,
        "new_runtime_execution_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_result": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def change_policy_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PostRunCombatUtilityRejectionDiagnosticHold(NEXT_GATE)
