"""Audit-only acceptance of the exact no-offload pair-06 execution authorization.

The authorization was accepted but intentionally held pre-claim after a
canonical receipt-schema mismatch was discovered before any attempt marker,
model load, inference, child spawn, or game execution occurred.

This record grants no authority by itself and performs no host I/O.
"""

from __future__ import annotations

from typing import Any

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-no-offload-baseline-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
)
AUTHORIZED_MAIN_HEAD = "d0fec8faabe34a13ab530fb73d1ce21cad1b79f7"
AUTHORIZATION_TEXT_SHA256 = (
    "1159b0b9f8e1914c69343ee2091f72bac573ce11a04b1543bd3b44b65b1722f5"
)
AUTHORIZATION_TEXT_BYTES = 827

PRECLAIM_HOLD_REASON = (
    "no_offload_parent_receipt_schema_vs_invocation_validator_mismatch"
)
EXPECTED_PARENT_RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-launcher-supervisor-no-offload-receipt.v1"
)
OBSERVED_INVOCATION_EXPECTED_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-launcher-supervisor-receipt.v1"
)

NEXT_GATE = "PAIR06_V8_NO_OFFLOAD_RECEIPT_SCHEMA_BINDING_REPAIR_REQUIRED"


class Pair06V8NoOffloadAuthorizationAcceptanceHold(ValueError):
    pass


def pair06_v8_no_offload_execution_authorization_acceptance_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "preclaim_hold": True,
        "preclaim_hold_reason": PRECLAIM_HOLD_REASON,
        "expected_parent_receipt_schema": EXPECTED_PARENT_RECEIPT_SCHEMA,
        "observed_invocation_expected_schema": OBSERVED_INVOCATION_EXPECTED_SCHEMA,
        "attempt_marker_created": False,
        "attempt_consumed": False,
        "runtime_load_performed": False,
        "model_inference_performed": False,
        "child_spawn_performed": False,
        "game_execution_performed": False,
        "automatic_retry": False,
        "authorization_reusable_after_main_or_request_change": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": NEXT_GATE,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8NoOffloadAuthorizationAcceptanceHold(NEXT_GATE)
