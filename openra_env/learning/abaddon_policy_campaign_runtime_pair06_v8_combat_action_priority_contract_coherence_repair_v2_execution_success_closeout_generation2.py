"""Source-only closeout record for the successful pair-06 V8 V2 coherent run.

This record captures the exact terminal identities printed by the reviewed
single-use Precision execution. It does not read host runtime state and does
not grant retry, replay, training, promotion, deployment, chain mutation, or
wallet/funds authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-coherent-v2-success-closeout.v1"
)

AUTHORIZED_MAIN_HEAD = "d8b16f1c23a74803ac4ace94045fed147c3c69fe"
ACCEPTANCE_MERGE = "1dfbed07a95b2a5cf60eed8af49e8a3355810f17"
AUTHORIZED_REQUEST_SHA256 = (
    "de3d60e2395192a976f14fe055d27981a9c7dd31560e67eda0fbe08f6b8f917c"
)
AUTHORIZATION_TEXT_SHA256 = (
    "6cfe4dd78c02a55c2499163b01de6f5714e0b8573100b7a888177ff1a568d139"
)
INVOCATION_SOURCE_SHA256 = (
    "309ea6f83d7129cb1dcccd61d1451c604098860154780e545ac8139f56a1403c"
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
TRAJECTORY_SHA256 = (
    "afc57351991c90dc21e4d2316ddd23fce8b01b9132a3435a9252de7227001ddc"
)
SUMMARY_SHA256 = (
    "a5d72287487849164e727836eee82dd5821ddb46f5803b995b1d67cc289075ab"
)
WARM_START_SHA256 = (
    "f36f2717d34e028d02d1b7076d7de1cff65dce1ffed59710110f2adbf4ad700d"
)

PRIOR_CONSUMED_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
PRIOR_FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = "PAIR06_V8_COHERENT_V2_SUCCESS_REVIEW_REQUIRED"


def pair06_v8_combat_priority_coherent_v2_success_closeout_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "record_kind": "source_only_runtime_success_closeout",
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "acceptance_merge": ACCEPTANCE_MERGE,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds_limit": 36,
        "rounds_completed": 36,
        "ticks_per_round": 25,
        "final_tick": 3551,
        "outcome": "DRAW_OR_UNFINISHED",
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "attempt_consumed": True,
        "attempt_reusable": False,
        "authorization_reusable": False,
        "result_file_sha256": RESULT_FILE_SHA256,
        "closeout_file_sha256": CLOSEOUT_FILE_SHA256,
        "run_id": RUN_ID,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "warm_start_sha256": WARM_START_SHA256,
        "game_execution_performed": True,
        "model_inference_performed": True,
        "model_inference_count": 36,
        "contract_coherence_repair_v2_used": True,
        "combat_priority_policy_activation_performed": True,
        "post_run_frozen_worktrees_green": True,
        "engine_container_removed": True,
        "session_destroyed": True,
        "automatic_retry": False,
        "candidate_execution_performed": False,
        "held_out_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "prior_consumed_marker_sha256": PRIOR_CONSUMED_MARKER_SHA256,
        "prior_consumed_marker_reusable": False,
        "prior_failed_run_id": PRIOR_FAILED_RUN_ID,
        "prior_failed_run_reusable_as_authority": False,
        "runtime_output_observed": True,
        "repo_side_local_artifact_rehash_performed": False,
        "runtime_execution_authorized_by_this_record": False,
        "retry_authorized_by_this_record": False,
        "replay_authorized_by_this_record": False,
        "training_authorized_by_this_record": False,
        "promotion_authorized_by_this_record": False,
        "deployment_authorized_by_this_record": False,
        "void_chain_mutation_authorized_by_this_record": False,
        "wallet_or_funds_action_authorized_by_this_record": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
    }


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise RuntimeError(NEXT_GATE)
