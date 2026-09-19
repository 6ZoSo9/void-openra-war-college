"""Source-only acceptance of one explicit V2R13 pair-03 baseline retry.

The user has explicitly authorized continuation after the failed first attempt.
This source records that authorization without bypassing the preservation gate.

The retry is NOT executable until the failed-attempt preservation receipt is
accepted by a later evidence gate.  No runtime action occurs on import or
contract inspection.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry-authorization-acceptance-contract.v1"
)

PAIR_SLOT = 3
ARM = "baseline"
MAX_RETRY_EXECUTIONS = 1

NEXT_GATE = "V2R13_PAIR03_BASELINE_PRESERVATION_EVIDENCE_ACCEPTANCE_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_preservation_evidence_acceptance"


class V2R13Pair03BaselineRetryAuthorizationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetryAuthorizationHold(message)


def v2r13_pair03_baseline_retry_authorization_acceptance_contract() -> dict[str, Any]:
    preservation = (
        preservation_review
        .v2r13_pair03_baseline_failed_attempt_preservation_review_contract()
    )

    _require(
        preservation.get("preservation_source_binding_present") is True,
        "failed-attempt preservation source binding missing",
    )
    _require(
        preservation.get("preservation_reviewed") is True,
        "failed-attempt preservation not reviewed",
    )
    _require(
        preservation.get("preservation_invoked") is False,
        "source review unexpectedly claims preservation invocation",
    )
    _require(
        preservation.get("runtime_retry_authorized") is False,
        "preservation review unexpectedly grants retry authority",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "retry_authorization_accepted": True,
        "retry_authorization_scope": "single_pair03_baseline_retry_after_preservation",
        "max_retry_executions": MAX_RETRY_EXECUTIONS,
        "automatic_retry": False,
        "preservation_must_complete_before_retry": True,
        "preservation_receipt_must_be_accepted_before_retry": True,
        "retry_execution_authorized_now": False,
        "runtime_retry_performed": False,
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


def execute_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineRetryAuthorizationHold(NEXT_GATE)
