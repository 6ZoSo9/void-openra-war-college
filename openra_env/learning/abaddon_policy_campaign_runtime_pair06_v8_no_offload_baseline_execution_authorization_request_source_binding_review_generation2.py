"""Source-only review of the fresh no-offload pair-06 V8 baseline execution request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_baseline_execution_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-baseline-execution-authorization-request-review-contract.v1"
)

REQUEST_GIT_BLOB = "7ed5b11d66518a2eecd3d4a28f680b111ee5d624"
REQUEST_SOURCE_SHA256 = (
    "55c197d0622572eced045dca8b1c86a11a4bf2a74beed7f4e3e2bed3c3449ed7"
)
REQUEST_TEST_GIT_BLOB = "9f2f37f2ef0fd9ac3885daf063fd50894893cbca"
REQUEST_TEST_SHA256 = (
    "7783ebbbd597d644f7855c3f0ec3b429413009ec82b01354bd8b6974db22c2ae"
)
REQUEST_BYTES_SHA256 = (
    "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
)
REQUEST_BYTE_LENGTH = 4118

NEXT_GATE = "PAIR06_V8_NO_OFFLOAD_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "explicit_pair06_v8_no_offload_baseline_execution_authorization"


class Pair06V8NoOffloadBaselineExecutionAuthorizationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8NoOffloadBaselineExecutionAuthorizationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.pair06_v8_no_offload_baseline_execution_authorization_request_contract()
    proposal = out.get("request")
    _require(isinstance(proposal, dict), "no-offload pair06 request missing")
    _require(
        proposal.get("record_kind") == "proposal_only_not_authorization",
        "no-offload pair06 request is not proposal-only",
    )

    lineage = proposal.get("repair_lineage")
    _require(isinstance(lineage, dict), "no-offload pair06 repair lineage missing")
    _require(
        lineage.get("first_spent_attempt_sha256")
        == "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930",
        "first spent attempt drift",
    )
    _require(
        lineage.get("second_spent_attempt_sha256")
        == "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1",
        "second spent attempt drift",
    )
    for field in (
        "first_spent_request_reusable",
        "second_spent_request_reusable",
        "first_spent_attempt_reusable",
        "second_spent_attempt_reusable",
        "cpu_disk_meta_parameter_offload_allowed",
    ):
        _require(lineage.get(field) is False, f"no-offload lineage boundary drift: {field}")

    for field in (
        "both_failed_attempts_archived",
        "prior_archives_must_remain_unchanged",
        "fresh_attempt_required",
        "no_offload_parent_generation_required",
        "single_gpu_cuda0_placement_required",
    ):
        _require(lineage.get(field) is True, f"no-offload lineage invariant drift: {field}")

    scope = proposal.get("proposed_scope")
    _require(isinstance(scope, dict), "no-offload pair06 proposed scope missing")
    expected_scope = {
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "candidate_arm_included": False,
        "held_out_pair15_included": False,
        "pair03_replay_included": False,
        "pair09_replay_included": False,
    }
    _require(scope == expected_scope, "no-offload pair06 proposed scope drift")

    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "no-offload request byte digest drift",
    )
    _require(
        out.get("request_byte_length") == REQUEST_BYTE_LENGTH,
        "no-offload request byte length drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "no-offload request digest unexpectedly grants authority",
    )
    _require(
        out.get("pair06_no_offload_baseline_specific_authorization_accepted") is False
        and out.get("pair06_no_offload_baseline_execution_authorized") is False
        and out.get("pair06_no_offload_baseline_execution_performed") is False,
        "no-offload pair06 request prematurely authorizes execution",
    )
    authority = out.get("authority")
    _require(
        isinstance(authority, dict)
        and authority
        and all(value is False for value in authority.values()),
        "no-offload pair06 authority map drift",
    )
    _require(out.get("next_gate") == NEXT_GATE, "no-offload pair06 request next gate drift")
    return deepcopy(out)


def pair06_v8_no_offload_baseline_execution_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "request_bytes_sha256": REQUEST_BYTES_SHA256,
        "request_byte_length": REQUEST_BYTE_LENGTH,
        "pair06_v8_no_offload_baseline_execution_authorization_request_source_binding_present": True,
        "pair06_v8_no_offload_baseline_execution_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "both_failed_attempts_archived": True,
        "first_spent_attempt_reusable": False,
        "second_spent_attempt_reusable": False,
        "no_offload_parent_generation_required": True,
        "single_gpu_cuda0_placement_required": True,
        "cpu_disk_meta_parameter_offload_allowed": False,
        "matching_request_digest_grants_authority": False,
        "pair06_no_offload_baseline_specific_authorization_accepted": False,
        "pair06_no_offload_baseline_execution_authorized": False,
        "pair06_no_offload_baseline_execution_performed": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8NoOffloadBaselineExecutionAuthorizationRequestReviewHold(NEXT_GATE)
