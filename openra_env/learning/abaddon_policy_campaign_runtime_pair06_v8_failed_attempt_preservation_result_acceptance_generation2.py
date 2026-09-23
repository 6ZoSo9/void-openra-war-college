"""Source-only acceptance of successful pair-06 V8 failed-attempt preservation.

Binds the exact Precision preservation terminal after the consumed pair-06
baseline attempt was archived. This record grants no retry or execution
authority.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-result-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-result-acceptance.v1"
)

AUTHORIZED_MAIN_HEAD = "344f6e146e839582aa600b11ca5d1c31e46b124a"
ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    "baseline-20260923T221259Z-56c02591"
)
PRESERVATION_RECEIPT_LOGICAL_SHA256 = (
    "29af061dbf3362eb2d5e79b0c94cd8f2be7d89d7dc271f72cf1fbd775913094f"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "d32cc7779fb1570ac2085031e296817059ce51d35de43ca3875becf9d032ccff"
)
WARM_START_SHA256 = (
    "1a6bbd544aca9f111a0961948771c24f9e2e36eda7559cf78acac1df24411333"
)
TRAJECTORY_SHA256 = (
    "89971bc284dab4424900eb7c27a73504e2acad067a59227dfdf37503475888ca"
)

EXPECTED_EVIDENCE = {
    "authorized_main_head": AUTHORIZED_MAIN_HEAD,
    "pair_slot": 6,
    "arm": "baseline",
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "failed_arm_source_present_after_preservation": False,
    "archive_present_after_preservation": True,
    "archive_path": ARCHIVE_PATH,
    "preservation_receipt_present": True,
    "preservation_receipt_logical_sha256": PRESERVATION_RECEIPT_LOGICAL_SHA256,
    "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
    "frozen_source_worktree_removed_non_force": True,
    "engine_worktree_removed_non_force": True,
    "failed_arm_inode_preserved": True,
    "attempt_marker_inode_preserved": True,
    "warm_start_inode_preserved": True,
    "trajectory_inode_preserved": True,
    "warm_start_sha256": WARM_START_SHA256,
    "trajectory_sha256": TRAJECTORY_SHA256,
    "failed_attempt_deleted": False,
    "runtime_retry_performed": False,
    "automatic_retry": False,
    "model_load_performed": False,
    "model_inference_performed": False,
    "game_execution_performed": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
}

NEXT_GATE = "PAIR06_V8_REPAIRED_BASELINE_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_repaired_baseline_execution_authorization_request"


class Pair06V8FailedAttemptPreservationResultAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8FailedAttemptPreservationResultAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def accept_pair06_v8_failed_attempt_preservation_result(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
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
        "pair06_v8_failed_attempt_preservation_result_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "archive_path": ARCHIVE_PATH,
        "preservation_receipt_logical_sha256": PRESERVATION_RECEIPT_LOGICAL_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "failed_attempt_archived": True,
        "failed_attempt_deleted": False,
        "old_baseline_arm_root_available": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def pair06_v8_failed_attempt_preservation_result_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_failed_attempt_preservation_result(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_failed_attempt_preservation_result_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "failed_attempt_archived": True,
        "failed_attempt_deleted": False,
        "fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def request_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8FailedAttemptPreservationResultAcceptanceHold(NEXT_GATE)
