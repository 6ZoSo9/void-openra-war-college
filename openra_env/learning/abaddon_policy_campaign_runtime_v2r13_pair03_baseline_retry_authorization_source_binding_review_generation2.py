"""Source-only review of one explicit pair-03 baseline retry authorization."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_authorization_acceptance_generation2
    as authorization,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry-authorization-review-contract.v1"
)

AUTHORIZATION_GIT_BLOB = "083d41c66838e6795b4536253cd9546d3224e97c"
AUTHORIZATION_SOURCE_SHA256 = (
    "fc2b05c74feb95f5827e5d7e7e9785f4ca76724635c71ca41f74e03f765a84db"
)
AUTHORIZATION_TEST_GIT_BLOB = "d2cc15422681acf866697634942433bdc501c6f9"
AUTHORIZATION_TEST_SHA256 = (
    "55b0863b076603565d3f23f1543d16e09ce76c45ebfac7779002e1ce6a68cd44"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_PRESERVATION_EVIDENCE_ACCEPTANCE_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_preservation_evidence_acceptance"


class V2R13Pair03BaselineRetryAuthorizationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetryAuthorizationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_authorization_cached() -> dict[str, Any]:
    contract = authorization.v2r13_pair03_baseline_retry_authorization_acceptance_contract()

    _require(contract.get("pair_slot") == 3, "retry pair-slot drift")
    _require(contract.get("arm") == "baseline", "retry arm drift")
    _require(contract.get("held_out") is False, "retry baseline became held-out")
    _require(contract.get("retry_authorization_accepted") is True, "retry authorization missing")
    _require(contract.get("max_retry_executions") == 1, "retry count drift")
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("preservation_must_complete_before_retry") is True,
        "preservation dependency missing",
    )
    _require(
        contract.get("preservation_receipt_must_be_accepted_before_retry") is True,
        "preservation receipt dependency missing",
    )
    _require(
        contract.get("retry_execution_authorized_now") is False,
        "retry prematurely executable",
    )

    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"retry scope expanded: {field}")

    return deepcopy(contract)


def v2r13_pair03_baseline_retry_authorization_review_contract() -> dict[str, Any]:
    validated = _validate_authorization_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_git_blob": AUTHORIZATION_GIT_BLOB,
        "authorization_source_sha256": AUTHORIZATION_SOURCE_SHA256,
        "authorization_test_git_blob": AUTHORIZATION_TEST_GIT_BLOB,
        "authorization_test_sha256": AUTHORIZATION_TEST_SHA256,
        "authorization_source_binding_present": True,
        "authorization_reviewed": True,
        "single_pair03_baseline_retry_authorized_after_preservation": True,
        "max_retry_executions": 1,
        "automatic_retry": False,
        "retry_execution_authorized_now": False,
        "preservation_evidence_acceptance_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_authorization": validated,
    }


def execute_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineRetryAuthorizationReviewHold(NEXT_GATE)
