"""Audit-only acceptance of the exact no-offload pair-06 execution authorization.

The authorization was accepted but intentionally held pre-claim after a
canonical receipt-schema mismatch was discovered before any attempt marker,
model load, inference, child spawn, or game execution occurred.

The receipt-schema repair is now canonical as an additive generation: the
historical no-offload invocation remains byte-identical and a separate
receipt-bound invocation carries the repaired schema/placement validation.

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

REPAIR_CANONICAL_MAIN_HEAD = "9c0b5ecea847abe5b9d997b1cda4f86bbe3e9287"
HISTORICAL_INVOCATION_GIT_BLOB = "b93255245f4d622dfb2cf0ddd6f97c3592f87cdc"
HISTORICAL_INVOCATION_SOURCE_SHA256 = (
    "4be25b850afc45cd34b977308add5cd288ce95411c683ca6545e0fb2fd6a0529"
)
RECEIPT_BOUND_INVOCATION_GIT_BLOB = "f22313cc3481b806a30dee5a7009b62c25293f17"
RECEIPT_BOUND_INVOCATION_SOURCE_SHA256 = (
    "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
)
RECEIPT_BOUND_INVOCATION_REVIEW_GIT_BLOB = (
    "dbe0390492520ec3307e4c9238136f5637962bbb"
)
RECEIPT_BOUND_INVOCATION_REVIEW_SOURCE_SHA256 = (
    "f5b7e9ceeddf07a98b74a8701802851fb46587a95aba7e6d3f866b1128c3b475"
)

NEXT_GATE = (
    "PAIR06_V8_NO_OFFLOAD_RECEIPT_BOUND_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)


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
        "receipt_schema_binding_repair_canonical": True,
        "repair_canonical_main_head": REPAIR_CANONICAL_MAIN_HEAD,
        "historical_no_offload_invocation_preserved": True,
        "historical_invocation_git_blob": HISTORICAL_INVOCATION_GIT_BLOB,
        "historical_invocation_source_sha256": HISTORICAL_INVOCATION_SOURCE_SHA256,
        "receipt_bound_invocation_git_blob": RECEIPT_BOUND_INVOCATION_GIT_BLOB,
        "receipt_bound_invocation_source_sha256": (
            RECEIPT_BOUND_INVOCATION_SOURCE_SHA256
        ),
        "receipt_bound_invocation_review_git_blob": (
            RECEIPT_BOUND_INVOCATION_REVIEW_GIT_BLOB
        ),
        "receipt_bound_invocation_review_source_sha256": (
            RECEIPT_BOUND_INVOCATION_REVIEW_SOURCE_SHA256
        ),
        "held_authorization_superseded": True,
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
