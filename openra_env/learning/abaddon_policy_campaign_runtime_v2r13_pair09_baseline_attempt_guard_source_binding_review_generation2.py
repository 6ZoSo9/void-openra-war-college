"""Source-only review of the V2R13 pair-09 baseline attempt guard.

This review pins the exact guard and tests, confirms create-only single-use
consumption semantics, and preserves the boundary that the marker is not an
authorization token or execution receipt.

It advances only to pair-09 baseline invocation implementation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_generation2
    as guard,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-attempt-guard-source-binding-review-contract.v1"
)

GUARD_GIT_BLOB = "4f3a470247196dde8fd7b7ad4807f1025adfb9b8"
GUARD_SOURCE_SHA256 = (
    "9e2c65cca456549efd6904d5a8b8745364398b52dcd5836ecc62fa52f43c3ef9"
)
GUARD_TEST_GIT_BLOB = "399175c091e4671e2a2ea435149cb0321c8df164"
GUARD_TEST_SHA256 = (
    "efa53c929f58635e520026095b5696d3497fbd86654d6cf9019dc854d87bed7e"
)
REQUEST_REVIEW_GIT_BLOB = "8342290da226a053e56a328885bd80bb5a77587f"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "50c4acaf6bdf1bbba063cf4670caaa8f23118fccfabbf917243b2cd71d2253a7"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_baseline_invocation_implementation"


class V2R13Pair09BaselineAttemptGuardReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineAttemptGuardReviewHold(message)


@lru_cache(maxsize=1)
def _validate_guard_cached() -> dict[str, Any]:
    contract = guard.pair09_baseline_attempt_guard_contract()
    reviewed_request = (
        request_review
        .v2r13_pair09_baseline_authorization_request_review_contract()
    )

    _require(
        reviewed_request.get(
            "pair09_baseline_authorization_request_reviewed"
        )
        is True,
        "pair09 authorization request review missing",
    )
    _require(
        reviewed_request.get("proposal_only_not_authorization") is True,
        "pair09 request authority drift",
    )
    _require(contract.get("pair_slot") == 9, "guard pair-slot drift")
    _require(contract.get("arm") == "baseline", "guard arm drift")
    _require(contract.get("held_out") is False, "guard held-out drift")
    _require(
        contract.get("single_use_attempt_consumption_implemented") is True,
        "single-use consumption missing",
    )
    _require(
        contract.get("create_only_marker_required") is True,
        "create-only marker requirement missing",
    )
    _require(
        contract.get("existing_or_uncertain_marker_holds") is True,
        "existing marker hold requirement missing",
    )
    _require(
        contract.get("marker_deletion_api_implemented") is False,
        "marker deletion API unexpectedly present",
    )
    _require(
        contract.get("reset_api_implemented") is False,
        "attempt reset API unexpectedly present",
    )
    _require(
        contract.get("resume_api_implemented") is False,
        "attempt resume API unexpectedly present",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")

    for field in (
        "pair09_baseline_specific_authorization_accepted",
        "pair09_baseline_execution_authorized",
        "pair09_baseline_execution_performed",
        "pair09_candidate_execution_authorized",
        "held_out_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"guard authority drift: {field}")

    _require(
        contract.get("next_gate")
        == (
            "V2R13_PAIR09_BASELINE_ATTEMPT_GUARD_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "guard review frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair09_baseline_attempt_guard_review_contract() -> dict[str, Any]:
    validated = _validate_guard_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "guard_git_blob": GUARD_GIT_BLOB,
        "guard_source_sha256": GUARD_SOURCE_SHA256,
        "guard_test_git_blob": GUARD_TEST_GIT_BLOB,
        "guard_test_sha256": GUARD_TEST_SHA256,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "separate_review_instrument": True,
        "pair09_baseline_attempt_guard_reviewed": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "single_use_attempt_consumption_reviewed": True,
        "create_only_marker_reviewed": True,
        "existing_or_uncertain_marker_holds": True,
        "marker_is_execution_authority": False,
        "marker_is_execution_evidence": False,
        "marker_deletion_api_implemented": False,
        "reset_api_implemented": False,
        "resume_api_implemented": False,
        "automatic_retry": False,
        "pair09_baseline_specific_authorization_accepted": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "pair09_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_guard": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineAttemptGuardReviewHold(
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
