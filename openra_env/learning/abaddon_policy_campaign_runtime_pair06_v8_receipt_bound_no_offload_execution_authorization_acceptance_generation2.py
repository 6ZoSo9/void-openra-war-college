"""Audit-only acceptance of one receipt-bound no-offload pair-06 V8 execution.

This record binds the user's exact explicit authorization to the canonical
replacement request and canonical War College main. It performs no host I/O,
attempt claim, model load, inference, child spawn, game execution, training,
deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from typing import Any

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-receipt-bound-no-offload-execution-authorization-acceptance-contract.v1"
)

AUTHORIZED_REQUEST_SHA256 = (
    "dbfee1aa9d648f81ea58e6c7d2bd99356e1af61b0e1957334ac67137b2d563e3"
)
AUTHORIZED_REQUEST_BYTES = 4828
AUTHORIZED_MAIN_HEAD = "bdb305aeaec8288b817d648dcc86124b26f4b4c4"
AUTHORIZATION_TEXT_SHA256 = (
    "bc898d1349d281a83ee094563f34b7f21d6f4c02891014029d4a8a3fc6d28f0f"
)
AUTHORIZATION_TEXT_BYTES = 966

REQUEST_REVIEW_GIT_BLOB = "f9deb948adde4a59de33e2e4d73cb9485f65f656"
INVOCATION_GIT_BLOB = "f22313cc3481b806a30dee5a7009b62c25293f17"
INVOCATION_SOURCE_SHA256 = (
    "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
)
PARENT_GIT_BLOB = "231758aeced0a57949dc39165df0f994e8473ebc"
LOADER_GIT_BLOB = "02edc92db7823270b521f7429730ee3de230db4e"

SUPERSEDED_REQUEST_SHA256 = (
    "66e85126c5a2d8a7f092ee6e388e4529160cb99791898e0134fa8e086057c8b8"
)
FIRST_SPENT_REQUEST_SHA256 = (
    "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae"
)
SECOND_SPENT_REQUEST_SHA256 = (
    "31c0069869915eb01221d7ea0aa867c0517df0a702eeff58ca69f70dec07a410"
)
FIRST_SPENT_ATTEMPT_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
SECOND_SPENT_ATTEMPT_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)

NEXT_GATE = "PAIR06_V8_RECEIPT_BOUND_NO_OFFLOAD_EXECUTION_AUTHORIZED"


class Pair06V8ReceiptBoundNoOffloadAuthorizationAcceptanceHold(ValueError):
    pass


def pair06_v8_receipt_bound_no_offload_execution_authorization_acceptance_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_record_kind": "explicit_user_authorization",
        "authorization_accepted": True,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_request_bytes": AUTHORIZED_REQUEST_BYTES,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "authorization_text_sha256": AUTHORIZATION_TEXT_SHA256,
        "authorization_text_bytes": AUTHORIZATION_TEXT_BYTES,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "parent_git_blob": PARENT_GIT_BLOB,
        "loader_git_blob": LOADER_GIT_BLOB,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "receipt_bound_no_offload_execution_authorized": True,
        "runtime_load_authorized": True,
        "model_inference_authorized": True,
        "game_execution_authorized": True,
        "single_gpu_cuda0_placement_required": True,
        "cpu_disk_meta_parameter_offload_allowed": False,
        "superseded_request_sha256": SUPERSEDED_REQUEST_SHA256,
        "superseded_request_reusable": False,
        "superseded_request_attempt_consumed": False,
        "first_spent_request_sha256": FIRST_SPENT_REQUEST_SHA256,
        "second_spent_request_sha256": SECOND_SPENT_REQUEST_SHA256,
        "first_spent_attempt_sha256": FIRST_SPENT_ATTEMPT_SHA256,
        "second_spent_attempt_sha256": SECOND_SPENT_ATTEMPT_SHA256,
        "first_spent_request_reusable": False,
        "second_spent_request_reusable": False,
        "first_spent_attempt_reusable": False,
        "second_spent_attempt_reusable": False,
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
        "attempt_marker_created_by_this_record": False,
        "execution_performed_by_this_record": False,
        "authorization_reusable_after_attempt_claim": False,
        "next_gate": NEXT_GATE,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ReceiptBoundNoOffloadAuthorizationAcceptanceHold(NEXT_GATE)
