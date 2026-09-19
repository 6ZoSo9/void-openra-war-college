"""Accept the exact Precision preservation evidence for the consumed retry.

This source binds the successful preservation receipt emitted after the single
authorized V2R13 pair-03 baseline retry failed before controller inference.
It records the archived retry evidence and closes the preservation gate without
granting any additional retry authority.

Importing this module performs no host action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_failed_retry_preservation_guard_repair_source_binding_review_generation2
    as guard_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-retry-preservation-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-retry-preservation-evidence-acceptance.v1"
)

PRESERVATION_LAUNCHER_SHA256 = (
    "e49ae8cab4dba8994172f7d8a0c02549ba9743f2db96f803712c8593f72f8229"
)
PRESERVATION_MAIN_HEAD = "6436b1afcf543566bf55c12895193fb8d1a055f3"
PRESERVATION_RECEIPT_SHA256 = (
    "833fb5bde1bbb96d6e2ceedff615fd86bf3b2522d21687d900355cbe705a0f15"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "007127f4834e3b2c772316f2f65a3b355c308a7a451eca996ad00c21f3f7cd28"
)
FAILED_RETRY_FORENSICS_SHA256 = (
    "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d"
)
FAILED_RETRY_WARM_START_SHA256 = (
    "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
)
FAILED_RETRY_WARM_START_BYTES = 223319
ORIGINAL_WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
ORIGINAL_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)

RETRY_ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/failed-attempts/"
    "baseline-retry-1-20260919T121144Z-71e90fdc"
)
RETRY_PRESERVATION_RECEIPT_PATH = (
    RETRY_ARCHIVE_PATH + "-preservation-receipt.json"
)
CANONICAL_ARM_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/baseline"
)

EXPECTED_EVIDENCE = {
    "preservation_launcher_sha256": PRESERVATION_LAUNCHER_SHA256,
    "preservation_main_head": PRESERVATION_MAIN_HEAD,
    "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
    "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
    "failed_retry_forensics_sha256": FAILED_RETRY_FORENSICS_SHA256,
    "pair_slot": 3,
    "arm": "baseline",
    "retry_index": 1,
    "canonical_arm_path": CANONICAL_ARM_PATH,
    "canonical_arm_path_absent_after_preservation": True,
    "retry_archive_path": RETRY_ARCHIVE_PATH,
    "retry_archive_present_after_preservation": True,
    "retry_preservation_receipt_path": RETRY_PRESERVATION_RECEIPT_PATH,
    "retry_preservation_receipt_present": True,
    "failed_retry_warm_start_sha256": FAILED_RETRY_WARM_START_SHA256,
    "failed_retry_warm_start_bytes": FAILED_RETRY_WARM_START_BYTES,
    "atomic_rename_performed": True,
    "archive_root_inode_preserved": True,
    "retry_warm_start_inode_preserved": True,
    "archived_retry_tree_unchanged": True,
    "original_first_attempt_archive_preserved": True,
    "original_warm_start_sha256": ORIGINAL_WARM_START_SHA256,
    "original_preservation_receipt_file_sha256": (
        ORIGINAL_PRESERVATION_RECEIPT_FILE_SHA256
    ),
    "failed_retry_deleted": False,
    "additional_retry_authorized": False,
    "additional_retry_performed": False,
    "runtime_start_performed": False,
    "model_load_performed": False,
    "model_inference_performed": False,
    "game_execution_performed": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
    "ollama_active_after": "inactive",
    "ollama_enabled_after": "disabled",
}

NEXT_GATE = "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_additional_retry_authorization"


class V2R13Pair03FailedRetryPreservationEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03FailedRetryPreservationEvidenceAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def _validate_dependency() -> dict[str, Any]:
    reviewed = guard_review.v2r13_failed_retry_preservation_guard_repair_review_contract()
    _require(
        reviewed.get("guard_repair_source_binding_present") is True,
        "guard-repair source binding missing",
    )
    _require(reviewed.get("guard_repair_reviewed") is True, "guard repair not reviewed")
    _require(
        reviewed.get("contract_implementation_guard_polarity_correct") is True,
        "preservation guard polarity not accepted",
    )
    _require(
        reviewed.get("preservation_invoked") is False,
        "review source unexpectedly records preservation invocation",
    )
    _require(
        reviewed.get("additional_retry_authorized") is False,
        "guard review unexpectedly authorizes another retry",
    )
    _require(
        reviewed.get("next_gate")
        == "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED",
        "guard review preservation frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair03_failed_retry_preservation_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "preservation evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "preservation evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"preservation evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "preservation evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "preservation_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 1,
        "failed_retry_preserved": True,
        "canonical_arm_path_available_for_future_authorized_execution": True,
        "original_first_attempt_archive_preserved": True,
        "failed_retry_archive_preserved": True,
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
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "dependency_review": dependency,
    }


def v2r13_pair03_failed_retry_preservation_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair03_failed_retry_preservation_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_launcher_sha256": PRESERVATION_LAUNCHER_SHA256,
        "preservation_main_head": PRESERVATION_MAIN_HEAD,
        "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "preservation_evidence_accepted": True,
        "retry_authorization_consumed": True,
        "additional_retry_authorized": False,
        "additional_retry_performed": False,
        "runtime_execution_authorized_now": False,
        "automatic_retry": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def authorize_additional_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03FailedRetryPreservationEvidenceAcceptanceHold(NEXT_GATE)
