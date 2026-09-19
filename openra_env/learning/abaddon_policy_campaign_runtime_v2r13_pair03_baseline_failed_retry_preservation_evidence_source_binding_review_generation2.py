"""Source-only review of accepted failed-retry preservation evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-retry-preservation-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "6e35f4603cc2870d743193e78e977fedeb586c38"
ACCEPTANCE_SOURCE_SHA256 = (
    "00e358ed9d0fc6b4c408d875a8ca716f50028e744360b59392e70c90d53ea8e1"
)
ACCEPTANCE_TEST_GIT_BLOB = "24e1025b4f800fa4502269e2ce92c79495368757"
ACCEPTANCE_TEST_SHA256 = (
    "6154677d27a221ea5ec309a6fe5a5d20375e9aa69f5a636056d84257c693beb8"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_additional_retry_authorization"


class V2R13Pair03FailedRetryPreservationEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03FailedRetryPreservationEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = (
        acceptance
        .v2r13_pair03_failed_retry_preservation_evidence_acceptance_contract()
    )

    _require(
        contract.get("preservation_evidence_accepted") is True,
        "preservation evidence acceptance missing",
    )
    _require(
        contract.get("preservation_receipt_sha256")
        == "833fb5bde1bbb96d6e2ceedff615fd86bf3b2522d21687d900355cbe705a0f15",
        "preservation semantic receipt SHA drift",
    )
    _require(
        contract.get("preservation_receipt_file_sha256")
        == "007127f4834e3b2c772316f2f65a3b355c308a7a451eca996ad00c21f3f7cd28",
        "preservation receipt file SHA drift",
    )
    _require(
        contract.get("retry_authorization_consumed") is True,
        "retry authorization consumption lost",
    )
    _require(
        contract.get("additional_retry_authorized") is False,
        "acceptance unexpectedly authorizes an additional retry",
    )
    _require(
        contract.get("additional_retry_performed") is False,
        "acceptance unexpectedly records an additional retry",
    )
    _require(
        contract.get("runtime_execution_authorized_now") is False,
        "runtime execution unexpectedly authorized",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("next_gate") == NEXT_GATE,
        "additional-retry authorization frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair03_failed_retry_preservation_evidence_review_contract() -> dict[str, Any]:
    validated = _validate_acceptance_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_source_git_blob": ACCEPTANCE_SOURCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "preservation_evidence_source_binding_present": True,
        "preservation_evidence_reviewed": True,
        "retry_authorization_consumed": True,
        "additional_retry_authorized": False,
        "additional_retry_performed": False,
        "runtime_execution_authorized_now": False,
        "automatic_retry": False,
        "candidate_arm_authorized": False,
        "held_out_arm_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_acceptance_contract": validated,
    }


def authorize_additional_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03FailedRetryPreservationEvidenceReviewHold(NEXT_GATE)
