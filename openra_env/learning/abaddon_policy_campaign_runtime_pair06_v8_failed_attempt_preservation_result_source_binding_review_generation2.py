"""Source-only review of successful pair-06 V8 failed-attempt preservation result."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_preservation_result_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-result-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "81de2f81579ce96669e3341d19ac242d556a4568"
ACCEPTANCE_SOURCE_SHA256 = (
    "cadfee2343a2ec8fb00cc7a01c954472dd2afe1f01eb6dc86030e3d58f6cb67f"
)
ACCEPTANCE_TEST_GIT_BLOB = "989168e73534ddd2096f498bf0e7ae19e4351022"
ACCEPTANCE_TEST_SHA256 = (
    "7869b65afd1ff1ee2264364750bd01676e64f4ac8b223e983bfa5b9a5f0c3611"
)

NEXT_GATE = "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_repaired_baseline_execution_authorization_request"


class Pair06V8FailedAttemptPreservationResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8FailedAttemptPreservationResultReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = acceptance.pair06_v8_failed_attempt_preservation_result_acceptance_contract()
    _require(
        out.get("pair06_v8_failed_attempt_preservation_result_accepted") is True,
        "pair06 preservation result not accepted",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930",
        "pair06 preservation result marker drift",
    )
    _require(out.get("failed_attempt_archived") is True, "pair06 failed attempt not archived")
    _require(out.get("failed_attempt_deleted") is False, "pair06 failed attempt unexpectedly deleted")
    _require(
        out.get("fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt") is True,
        "fresh baseline root not available for later authorized attempt",
    )
    _require(out.get("runtime_retry_authorized") is False, "pair06 retry unexpectedly authorized")
    _require(out.get("automatic_retry") is False, "pair06 automatic retry unexpectedly enabled")
    _require(out.get("next_gate") == NEXT_GATE, "pair06 preservation result frontier drift")
    return deepcopy(out)


def pair06_v8_failed_attempt_preservation_result_review_contract() -> dict[str, Any]:
    accepted = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "pair06_v8_failed_attempt_preservation_result_source_binding_present": True,
        "pair06_v8_failed_attempt_preservation_result_reviewed": True,
        "attempt_marker_sha256": accepted["attempt_marker_sha256"],
        "failed_attempt_archived": True,
        "failed_attempt_deleted": False,
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
    raise Pair06V8FailedAttemptPreservationResultReviewHold(NEXT_GATE)
