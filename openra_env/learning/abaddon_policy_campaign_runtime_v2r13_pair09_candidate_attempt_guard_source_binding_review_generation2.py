"""Source-only review of the pair-09 candidate single-use attempt guard."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_attempt_guard_generation2
    as guard,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-attempt-guard-review-contract.v1"
)

GUARD_GIT_BLOB = "0540e4472af8b7da11e16b118b3bd373e7e9b92c"
GUARD_SOURCE_SHA256 = (
    "aa025315c94dd2c25a9faa6cdb5d44e1f1314dc2b67c42e781801cd6695f7982"
)
GUARD_TEST_GIT_BLOB = "9113245d666657e2a3cbf19f6598011c0b9a2696"
GUARD_TEST_SHA256 = (
    "420618367caeadd1080997912bd77983f0cb1eb1450917610cec6e6afd399de8"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_HOST_PREFLIGHT_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_host_preflight"


class V2R13Pair09CandidateAttemptGuardReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateAttemptGuardReviewHold(message)


@lru_cache(maxsize=1)
def _validate_guard_cached() -> dict[str, Any]:
    contract = guard.pair09_candidate_attempt_guard_contract()
    _require(
        contract.get("pair09_candidate_attempt_guard_implemented") is True,
        "candidate attempt guard missing",
    )
    _require(
        contract.get("pair09_candidate_attempt_guard_reviewed") is False,
        "candidate attempt guard self-reviewed",
    )
    _require(contract.get("pair_slot") == 9, "candidate guard pair-slot drift")
    _require(contract.get("arm") == "candidate", "candidate guard arm drift")
    _require(contract.get("held_out") is False, "candidate guard held-out drift")
    _require(contract.get("marker_name") == guard.MARKER_NAME, "candidate marker-name drift")
    _require(contract.get("create_only_marker") is True, "candidate marker not create-only")
    _require(contract.get("single_use_attempt") is True, "candidate attempt not single-use")
    _require(contract.get("maximum_attempts") == 1, "candidate attempt cardinality drift")
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(contract.get("reset_api_present") is False, "reset API appeared")
    _require(contract.get("delete_api_present") is False, "delete API appeared")
    _require(contract.get("resume_api_present") is False, "resume API appeared")
    _require(
        contract.get("marker_is_execution_authority") is False,
        "candidate marker became execution authority",
    )
    for field in (
        "pair09_candidate_specific_authorization_accepted",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "held_out_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"candidate guard authority drift: {field}")
    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_ATTEMPT_GUARD_SOURCE_BINDING_REVIEW_REQUIRED",
        "candidate guard review frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair09_candidate_attempt_guard_review_contract() -> dict[str, Any]:
    validated = _validate_guard_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "guard_git_blob": GUARD_GIT_BLOB,
        "guard_source_sha256": GUARD_SOURCE_SHA256,
        "guard_test_git_blob": GUARD_TEST_GIT_BLOB,
        "guard_test_sha256": GUARD_TEST_SHA256,
        "separate_review_instrument": True,
        "pair09_candidate_attempt_guard_reviewed": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "single_use_attempt_consumption_reviewed": True,
        "create_only_marker_reviewed": True,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "marker_is_execution_authority": False,
        "reset_api_present": False,
        "delete_api_present": False,
        "resume_api_present": False,
        "pair09_candidate_specific_authorization_accepted": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_candidate_execution_performed": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_guard": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateAttemptGuardReviewHold(
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
