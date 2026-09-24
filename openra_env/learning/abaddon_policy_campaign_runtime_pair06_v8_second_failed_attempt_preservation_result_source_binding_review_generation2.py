"""Source-only review of the successful second pair-06 V8 preservation result."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_result_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-preservation-result-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "462d0524324cbe8c69914d004acf03cec54de2e9"
ACCEPTANCE_SOURCE_SHA256 = (
    "8bc1249e6cb069d162745d8956fbc28bc68bf087ef1ef7c3cf108d34b5050269"
)
ACCEPTANCE_TEST_GIT_BLOB = "0d5f2f7f8b7156242d29193ddd755eb593da3933"
ACCEPTANCE_TEST_SHA256 = (
    "a3673208b5e17036e4d035d69c8a60ead6b03c30dda61f8b4dd7c0305dd0f2db"
)

NEXT_GATE = "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_no_offload_baseline_attempt_invocation"


class Pair06V8SecondPreservationResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8SecondPreservationResultReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = acceptance.pair06_v8_second_preservation_result_acceptance_contract()
    _require(
        out.get("pair06_v8_second_preservation_result_accepted") is True,
        "second pair06 preservation result not accepted",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1",
        "second pair06 preservation result marker drift",
    )
    _require(
        out.get("archive_name") == "baseline-20260923T235031Z-446d8f92",
        "second pair06 preservation result archive drift",
    )
    _require(
        out.get("second_failed_attempt_archived") is True
        and out.get("second_failed_attempt_deleted") is False,
        "second pair06 preservation result archive state drift",
    )
    _require(
        out.get("prior_failed_attempt_archive_unchanged") is True,
        "first pair06 archive changed",
    )
    _require(
        out.get("fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt")
        is True,
        "fresh pair06 baseline root not available",
    )
    _require(
        out.get("runtime_retry_authorized") is False
        and out.get("automatic_retry") is False,
        "second pair06 preservation result unexpectedly authorizes retry",
    )
    _require(out.get("next_gate") == NEXT_GATE, "second preservation result frontier drift")
    return deepcopy(out)


def pair06_v8_second_preservation_result_review_contract() -> dict[str, Any]:
    accepted = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "pair06_v8_second_preservation_result_source_binding_present": True,
        "pair06_v8_second_preservation_result_reviewed": True,
        "attempt_marker_sha256": accepted["attempt_marker_sha256"],
        "archive_name": accepted["archive_name"],
        "second_failed_attempt_archived": True,
        "second_failed_attempt_deleted": False,
        "prior_failed_attempt_archive_unchanged": True,
        "fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_acceptance": accepted,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def request_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8SecondPreservationResultReviewHold(NEXT_GATE)
