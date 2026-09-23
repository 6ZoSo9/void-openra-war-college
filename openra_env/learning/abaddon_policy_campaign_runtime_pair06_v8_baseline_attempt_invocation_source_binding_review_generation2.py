"""Source-only review of pair-06 V8 baseline Git backend and one-shot invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_generation2
    as invocation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_git_backend_generation2
    as git_backend,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-attempt-invocation-review-contract.v1"
)

GIT_BACKEND_GIT_BLOB = "3a405630789528ca5411d04ba9b0fcac0b27e590"
GIT_BACKEND_SOURCE_SHA256 = (
    "8d0291a497c1f87d9cd11bc88a821b11d166d03967f2f611dd143e35bd425f9a"
)
GIT_BACKEND_TEST_GIT_BLOB = "2d8472ea3630f8e9e46159ba9e48e781f8ba7288"
GIT_BACKEND_TEST_SHA256 = (
    "c0444208d94936826ca1ea8ffa30216432053c4a127e23c51763c52e13d3031d"
)
INVOCATION_GIT_BLOB = "eadc2af910ce70b93d78b4370b3511c7a320c610"
INVOCATION_SOURCE_SHA256 = (
    "9129147f8dfbb6214bd8c87dd66871424eb2cf49ba238404c84f10582606aaa5"
)
INVOCATION_TEST_GIT_BLOB = "cff9dcd3450103e2c139addd0c93dc82182c2c22"
INVOCATION_TEST_SHA256 = (
    "5cc335acbd63b00cc243f396a55283c184a1f5d411563d5cf89e2edbc2b2309c"
)

NEXT_GATE = "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_execution_authorization_request"


class Pair06V8BaselineAttemptInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineAttemptInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_cached() -> dict[str, Any]:
    backend = git_backend.pair06_v8_baseline_git_backend_contract()
    invoke = invocation.pair06_v8_baseline_attempt_invocation_contract()

    _require(
        backend.get("pair_slot") == 6
        and backend.get("arm") == "baseline"
        and backend.get("held_out") is False,
        "pair06 Git backend scope drift",
    )
    _require(
        backend.get("fetch_implemented") is False
        and backend.get("canonical_checkout_implemented") is False
        and backend.get("force_remove_implemented") is False
        and backend.get("network_protocol_allowed") is False,
        "pair06 Git backend capability drift",
    )
    _require(
        backend.get("runtime_execution_authorized") is False
        and backend.get("runtime_execution_performed") is False,
        "pair06 Git backend unexpectedly carries runtime authority",
    )

    _require(
        invoke.get("pair06_v8_baseline_attempt_invocation_implemented") is True,
        "pair06 attempt invocation missing",
    )
    _require(
        invoke.get("pair06_v8_baseline_attempt_invocation_reviewed") is False,
        "pair06 attempt invocation unexpectedly self-reviewed",
    )
    _require(
        invoke.get("pair_slot") == 6
        and invoke.get("arm") == "baseline"
        and invoke.get("held_out") is False,
        "pair06 invocation scope drift",
    )

    for field in (
        "exact_v8_python_required",
        "exact_current_main_required",
        "exact_invocation_source_sha256_required",
        "fresh_v8_environment_and_assets_required",
        "reviewed_worktree_materializer_reused",
        "pair06_specific_git_backend_required",
        "preclaim_worktree_materialization_implemented",
        "preclaim_materialization_cleanup_on_hold_implemented",
        "preclaim_empty_runs_root_required",
        "durable_create_only_attempt_marker_implemented",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "marker_sha256_is_attempt_id",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_supervisor",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
        "explicit_authorization_boolean_required",
        "explicit_confirmation_token_required",
    ):
        _require(invoke.get(field) is True, f"pair06 invocation invariant drift: {field}")

    for field in (
        "marker_deletion_api_implemented",
        "reset_api_implemented",
        "resume_api_implemented",
        "automatic_retry",
        "pair06_baseline_specific_authorization_accepted",
        "attempt_consumed",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        _require(invoke.get(field) is False, f"pair06 invocation authority drift: {field}")

    _require(invoke.get("maximum_attempts") == 1, "pair06 maximum attempt count drift")
    _require(
        invoke.get("next_gate")
        == "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 invocation source-review frontier drift",
    )

    return {
        "git_backend": deepcopy(backend),
        "invocation": deepcopy(invoke),
    }


def pair06_v8_baseline_attempt_invocation_review_contract() -> dict[str, Any]:
    validated = _validate_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "git_backend_git_blob": GIT_BACKEND_GIT_BLOB,
        "git_backend_source_sha256": GIT_BACKEND_SOURCE_SHA256,
        "git_backend_test_git_blob": GIT_BACKEND_TEST_GIT_BLOB,
        "git_backend_test_sha256": GIT_BACKEND_TEST_SHA256,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "pair06_v8_baseline_git_backend_source_binding_present": True,
        "pair06_v8_baseline_attempt_invocation_source_binding_present": True,
        "pair06_v8_baseline_attempt_invocation_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "preclaim_materialization_cleanup_on_hold": True,
        "attempt_marker_create_only": True,
        "attempt_marker_precedes_model_load_and_child_spawn": True,
        "postclaim_reset_or_resume_available": False,
        "durable_execution_result_before_cleanup": True,
        "success_only_worktree_cleanup": True,
        "durable_cleanup_closeout": True,
        "runs_preserved": True,
        "explicit_authorization_required": True,
        "pair06_baseline_specific_authorization_accepted": False,
        "attempt_consumed": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_authorize(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineAttemptInvocationReviewHold(NEXT_GATE)
