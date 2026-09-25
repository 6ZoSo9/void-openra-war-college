"""Source-only review of the successful GPU-gated pair-06 V8 execution result.

Pins the exact accepted result source/test identities and closes the one-shot
execution lineage. This review performs no host I/O, retry, attempt claim,
model load, inference, game execution, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_result_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-preclaim-gpu-execution-result-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "9af8a4afc676946ff470852438a3ecda854399e1"
ACCEPTANCE_SOURCE_SHA256 = (
    "2f16dd723d97d40b424f8b18abcd529ea93115b7b0a1807c2d826b0974669efc"
)
ACCEPTANCE_TEST_GIT_BLOB = "6c49b1bf366a1cbec54a2a30fbd22323f973a9a6"
ACCEPTANCE_TEST_SHA256 = (
    "47f661a44a814034c4426f9d5ba33236ad7750dd90c50eb9dd16101f57506c22"
)

AUTHORIZED_REQUEST_SHA256 = (
    "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
)
AUTHORIZED_MAIN_HEAD = "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
ATTEMPT_MARKER_SHA256 = (
    "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
)
RESULT_FILE_SHA256 = (
    "f1a3a1ffec2957b984212e5c11067a477934a1c484020dcb2e6398764a117440"
)
CLOSEOUT_FILE_SHA256 = (
    "f0227597d44ecfc5ae07fdc473a2ca9bda71085fba9970279dedf31d5ac24920"
)

NEXT_GATE = (
    "PAIR06_V8_POST_RUN_COMBAT_UTILITY_AND_REJECTION_DIAGNOSTIC_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_post_run_combat_utility_and_rejection_diagnostic"
)


class Pair06V8PreclaimGpuExecutionResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PreclaimGpuExecutionResultReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = acceptance.pair06_v8_preclaim_gpu_execution_result_acceptance_contract()

    _require(
        out.get("pair06_v8_preclaim_gpu_execution_result_accepted") is True,
        "GPU-gated execution result not accepted",
    )
    _require(
        out.get("authorized_request_sha256") == AUTHORIZED_REQUEST_SHA256
        and out.get("authorized_main_head") == AUTHORIZED_MAIN_HEAD,
        "authorized execution identity drift",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("doctrine") == "FEINTER"
        and out.get("seed") == 208354846,
        "pair06 result scope drift",
    )
    _require(
        out.get("round_limit") == 36
        and out.get("rounds_completed") == 36
        and out.get("ticks_per_round") == 25,
        "pair06 completion cardinality drift",
    )
    _require(
        out.get("attempt_consumed") is True
        and out.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "pair06 attempt marker state drift",
    )
    _require(
        out.get("result_file_sha256") == RESULT_FILE_SHA256
        and out.get("closeout_file_sha256") == CLOSEOUT_FILE_SHA256,
        "pair06 durable result/closeout drift",
    )
    _require(
        out.get("execution_result_green") is True
        and out.get("post_run_frozen_worktrees_green") is True
        and out.get("session_destroyed") is True
        and out.get("engine_container_removed") is True
        and out.get("warm_start_spar_cleanup_complete") is True,
        "pair06 execution closeout drift",
    )
    _require(
        out.get("preclaim_gpu_compute_process_count") == 0
        and out.get("fresh_preclaim_gpu_admitted") is True
        and out.get("model_inference_count") == 36
        and out.get("child_retirement_terminal") == "natural_exit",
        "pair06 GPU/inference completion drift",
    )
    _require(
        out.get("runtime_output_candidate_only") is True
        and out.get("candidate_execution_performed") is False
        and out.get("held_out_execution_performed") is False,
        "pair06 candidate classification/scope drift",
    )
    for field in (
        "automatic_corpus_admission",
        "automatic_retry_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "authorization_reusable_after_attempt_claim",
    ):
        _require(out.get(field) is False, "pair06 boundary drift: " + field)

    _require(
        out.get("next_gate")
        == "PAIR06_V8_PRECLAIM_GPU_EXECUTION_RESULT_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 result-review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_preclaim_gpu_execution_result_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "pair06_v8_preclaim_gpu_execution_result_reviewed": True,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "result_file_sha256": RESULT_FILE_SHA256,
        "closeout_file_sha256": CLOSEOUT_FILE_SHA256,
        "outcome": validated["outcome"],
        "rounds_completed": validated["rounds_completed"],
        "final_tick": validated["final_tick"],
        "model_inference_count": validated["model_inference_count"],
        "attempt_consumed": True,
        "authorization_reusable": False,
        "candidate_execution_performed": False,
        "held_out_execution_performed": False,
        "automatic_retry_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "validated_result": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_promote(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PreclaimGpuExecutionResultReviewHold(NEXT_GATE)
