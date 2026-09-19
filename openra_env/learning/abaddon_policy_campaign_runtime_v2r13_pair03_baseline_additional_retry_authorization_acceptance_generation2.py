"""Accept exactly one additional V2R13 pair-03 baseline retry authorization.

The previous retry authorization has been consumed and its failed execution has
been preserved with accepted evidence. The user has now explicitly authorized
continued work. This source records authorization for exactly one additional
pair-03 baseline retry (retry index 2).

Importing or inspecting this module performs no host action and does not make
the retry executable until the authorization is independently source-reviewed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_evidence_source_binding_review_generation2
    as preservation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-additional-retry-authorization-acceptance-contract.v1"
)

PAIR_SLOT = 3
ARM = "baseline"
RETRY_INDEX = 2
MAX_ADDITIONAL_RETRY_EXECUTIONS = 1
TOTAL_RETRY_EXECUTIONS_AUTHORIZED = 2

NEXT_GATE = (
    "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair03_baseline_additional_retry_authorization_review"
)


class V2R13Pair03BaselineAdditionalRetryAuthorizationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineAdditionalRetryAuthorizationHold(message)


def v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract() -> dict[str, Any]:
    preservation = (
        preservation_review
        .v2r13_pair03_failed_retry_preservation_evidence_review_contract()
    )

    _require(
        preservation.get("preservation_evidence_source_binding_present") is True,
        "failed-retry preservation evidence binding missing",
    )
    _require(
        preservation.get("preservation_evidence_reviewed") is True,
        "failed-retry preservation evidence not reviewed",
    )
    _require(
        preservation.get("retry_authorization_consumed") is True,
        "prior retry authorization is not recorded consumed",
    )
    _require(
        preservation.get("additional_retry_authorized") is False,
        "preservation review already authorizes an additional retry",
    )
    _require(
        preservation.get("additional_retry_performed") is False,
        "preservation review unexpectedly records additional retry execution",
    )
    _require(
        preservation.get("runtime_execution_authorized_now") is False,
        "preservation review unexpectedly authorizes runtime execution",
    )
    _require(
        preservation.get("automatic_retry") is False,
        "automatic retry unexpectedly enabled",
    )
    _require(
        preservation.get("next_gate")
        == "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED",
        "additional-retry authorization frontier drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "retry_index": RETRY_INDEX,
        "additional_retry_authorization_accepted": True,
        "authorization_scope": "exactly_one_additional_pair03_baseline_retry",
        "max_additional_retry_executions": MAX_ADDITIONAL_RETRY_EXECUTIONS,
        "total_retry_executions_authorized": TOTAL_RETRY_EXECUTIONS_AUTHORIZED,
        "prior_retry_authorization_consumed": True,
        "failed_retry_preservation_evidence_reviewed": True,
        "canonical_arm_available_only_after_preservation": True,
        "automatic_retry": False,
        "additional_retry_execution_authorized_now": False,
        "additional_retry_execution_performed": False,
        "candidate_arm_authorized": False,
        "held_out_arm_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "preservation_review": deepcopy(preservation),
    }


def execute_additional_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineAdditionalRetryAuthorizationHold(NEXT_GATE)
