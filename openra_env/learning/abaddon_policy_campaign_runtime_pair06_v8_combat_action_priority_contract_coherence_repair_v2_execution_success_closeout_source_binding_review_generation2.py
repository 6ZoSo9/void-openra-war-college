"""Source-only review of the successful pair-06 V8 V2 coherent closeout.

Pins the exact merged success-closeout source/tests and closes this execution
lineage. The successful attempt marker and authorization are permanently spent.

This review grants no retry, replay, training, promotion, deployment,
VOID-chain mutation, or wallet/funds authority and does not open a new
execution request frontier.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_generation2
    as closeout,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-coherent-v2-success-closeout-review.v1"
)

CLOSEOUT_MAIN_HEAD = "c28dbbfaa750da6405be7a2557ce32ae1ad4d810"
CLOSEOUT_GIT_BLOB = "6a12d64061cf449f40fb2e6fae4201ba6fff3d27"
CLOSEOUT_SOURCE_SHA256 = (
    "a6026a7dff86b98e57572dddb0c6388aaeffd6ba3c3d612e8f1b3a4616ae1b2c"
)
CLOSEOUT_TEST_GIT_BLOB = "221cf2a24777c2d0ca8e58a8fbc5c64116c5cdf1"
CLOSEOUT_TEST_SHA256 = (
    "488f55c0ebf5f2d5f8fc6007c28ba31f50744deefa43d73459d9211e7d4e4171"
)

ATTEMPT_MARKER_SHA256 = (
    "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207"
)
RESULT_FILE_SHA256 = (
    "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4"
)
CLOSEOUT_FILE_SHA256 = (
    "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1"
)
RUN_ID = "warmstart-apollyon-vs-abaddon-20260927T183337Z-feinter-s208354846"

NEXT_GATE = "PAIR06_V8_COHERENT_V2_SUCCESS_LINEAGE_CLOSED"
NEXT_CHANGE_CLASS = "none"


class Pair06V8CombatPriorityCoherentV2SuccessReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2SuccessReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()

    _require(
        out.get("record_kind") == "source_only_runtime_success_closeout",
        "success closeout record kind drift",
    )
    _require(
        out.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256
        and out.get("result_file_sha256") == RESULT_FILE_SHA256
        and out.get("closeout_file_sha256") == CLOSEOUT_FILE_SHA256,
        "success artifact identity drift",
    )
    _require(
        out.get("run_id") == RUN_ID
        and out.get("rounds_completed") == 36
        and out.get("final_tick") == 3551
        and out.get("outcome") == "DRAW_OR_UNFINISHED",
        "success run identity drift",
    )
    _require(
        out.get("attempt_consumed") is True
        and out.get("attempt_reusable") is False
        and out.get("authorization_reusable") is False
        and out.get("automatic_retry") is False,
        "success single-use boundary drift",
    )

    for field in (
        "game_execution_performed",
        "model_inference_performed",
        "contract_coherence_repair_v2_used",
        "combat_priority_policy_activation_performed",
        "post_run_frozen_worktrees_green",
        "engine_container_removed",
        "session_destroyed",
    ):
        _require(out.get(field) is True, "success invariant drift: " + field)

    for field in (
        "candidate_execution_performed",
        "held_out_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "runtime_execution_authorized_by_this_record",
        "retry_authorized_by_this_record",
        "replay_authorized_by_this_record",
        "training_authorized_by_this_record",
        "promotion_authorized_by_this_record",
        "deployment_authorized_by_this_record",
        "void_chain_mutation_authorized_by_this_record",
        "wallet_or_funds_action_authorized_by_this_record",
    ):
        _require(out.get(field) is False, "success closeout authority drift: " + field)

    _require(
        out.get("next_gate") == "PAIR06_V8_COHERENT_V2_SUCCESS_REVIEW_REQUIRED",
        "success closeout review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_v2_success_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "closeout_main_head": CLOSEOUT_MAIN_HEAD,
        "closeout_git_blob": CLOSEOUT_GIT_BLOB,
        "closeout_source_sha256": CLOSEOUT_SOURCE_SHA256,
        "closeout_test_git_blob": CLOSEOUT_TEST_GIT_BLOB,
        "closeout_test_sha256": CLOSEOUT_TEST_SHA256,
        "pair06_v8_combat_priority_coherent_v2_success_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds_completed": 36,
        "final_tick": 3551,
        "outcome": "DRAW_OR_UNFINISHED",
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "result_file_sha256": RESULT_FILE_SHA256,
        "closeout_file_sha256": CLOSEOUT_FILE_SHA256,
        "run_id": RUN_ID,
        "attempt_consumed": True,
        "attempt_reusable": False,
        "authorization_reusable": False,
        "automatic_retry": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "retry_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "new_execution_request_opened": False,
        "lineage_closed": True,
        "validated_closeout": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_reopen(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityCoherentV2SuccessReviewHold(NEXT_GATE)
