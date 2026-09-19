"""Bounded preservation contract for the failed pair-03 baseline retry.

The implementation is limited to preserving the consumed retry arm under a
separate deterministic archive. It grants no additional retry authority and
performs no runtime/model/game/training/deployment/VOID/funds action on import.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_forensics_acceptance_generation2
    as forensics_acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-retry-preservation-contract.v1"
)

FAILED_RETRY_FORENSICS_SHA256 = (
    "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d"
)
FAILED_RETRY_ARM_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/baseline"
)
RETRY_ARCHIVE_NAME = "baseline-retry-1-20260919T121144Z-71e90fdc"
RETRY_ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/failed-attempts/"
    + RETRY_ARCHIVE_NAME
)
RETRY_PRESERVATION_RECEIPT_PATH = (
    RETRY_ARCHIVE_PATH + "-preservation-receipt.json"
)
FAILED_RETRY_WARM_START_SHA256 = (
    "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
)
FAILED_RETRY_WARM_START_BYTES = 223319
ORIGINAL_ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/failed-attempts/"
    "baseline-20260918T233630Z-98773549"
)
ORIGINAL_WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
ORIGINAL_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)

NEXT_GATE = (
    "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair03_baseline_failed_retry_preservation_review"
)


class V2R13Pair03BaselineFailedRetryPreservationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineFailedRetryPreservationHold(message)


def _validate_forensics() -> dict[str, Any]:
    accepted = (
        forensics_acceptance
        .v2r13_pair03_baseline_failed_retry_forensics_acceptance_contract()
    )
    _require(
        accepted.get("failed_retry_forensics_accepted") is True,
        "failed-retry forensics not accepted",
    )
    _require(
        accepted.get("forensics_sha256") == FAILED_RETRY_FORENSICS_SHA256,
        "failed-retry forensic identity drift",
    )
    _require(
        accepted.get("additional_retry_authorized") is False,
        "forensics unexpectedly authorize another retry",
    )
    return deepcopy(accepted)


def v2r13_pair03_baseline_failed_retry_preservation_contract() -> dict[str, Any]:
    accepted = _validate_forensics()
    return {
        "schema": CONTRACT_SCHEMA,
        "failed_retry_forensics_sha256": FAILED_RETRY_FORENSICS_SHA256,
        "failed_retry_arm_path": FAILED_RETRY_ARM_PATH,
        "retry_archive_name": RETRY_ARCHIVE_NAME,
        "retry_archive_path": RETRY_ARCHIVE_PATH,
        "retry_preservation_receipt_path": RETRY_PRESERVATION_RECEIPT_PATH,
        "failed_retry_warm_start_sha256": FAILED_RETRY_WARM_START_SHA256,
        "failed_retry_warm_start_bytes": FAILED_RETRY_WARM_START_BYTES,
        "original_archive_path": ORIGINAL_ARCHIVE_PATH,
        "original_warm_start_sha256": ORIGINAL_WARM_START_SHA256,
        "original_preservation_receipt_file_sha256": (
            ORIGINAL_PRESERVATION_RECEIPT_FILE_SHA256
        ),
        "exact_failed_retry_tree_required": True,
        "same_filesystem_atomic_rename_required": True,
        "archived_retry_tree_must_remain_unchanged": True,
        "original_first_attempt_archive_must_remain_unchanged": True,
        "failed_retry_deletion_authorized": False,
        "additional_retry_authorized": False,
        "automatic_retry": False,
        "runtime_start_authorized": False,
        "model_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "preservation_implemented": True,
        "precision_preservation_tool_present": True,
        "precision_preservation_tool_source_binding_present": False,
        "preservation_invoked": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_forensics": accepted,
    }


def preserve_failed_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineFailedRetryPreservationHold(NEXT_GATE)
