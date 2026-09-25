"""Source-only acceptance of the successful third pair-06 failed-attempt preservation.

Binds the exact Precision preservation terminal for consumed attempt
3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3.
It grants no retry or execution authority.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-preservation-result-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-preservation-result-acceptance.v1"
)

REVIEWED_MAIN_HEAD = "81d3ca253b2c383e6868a387cdcb14b36b5f9d8d"
AUTHORIZED_EXECUTION_HEAD = "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)
ARCHIVE_NAME = "baseline-3ad564f9"
ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    + ARCHIVE_NAME
)
PRESERVATION_RECEIPT_LOGICAL_SHA256 = (
    "9a7ec01af0f80d7a0d0333c91fd5c07d9ae24e04eaf87455fb143385ec76070b"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "12a2da73143db442f5620065f8c270ef8026a641da2afa938203e51ceeaa43f4"
)
PRESERVATION_RECEIPT_BYTES = 3130

PRIOR_ATTEMPT_MARKERS = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930",
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1",
)

EXPECTED_EVIDENCE = {
    "reviewed_main_head": REVIEWED_MAIN_HEAD,
    "authorized_execution_head_preserved": AUTHORIZED_EXECUTION_HEAD,
    "pair_slot": 6,
    "arm": "baseline",
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "archive_name": ARCHIVE_NAME,
    "archive_path": ARCHIVE_PATH,
    "baseline_path_freed": True,
    "third_attempt_archive_present": True,
    "archived_marker_sha256": ATTEMPT_MARKER_SHA256,
    "frozen_source_worktree_removed_non_force": True,
    "engine_worktree_removed_non_force": True,
    "failed_arm_inode_preserved": True,
    "attempt_marker_inode_preserved": True,
    "prior_failed_attempt_archives_unchanged": True,
    "preservation_receipt_logical_sha256": PRESERVATION_RECEIPT_LOGICAL_SHA256,
    "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
    "preservation_receipt_bytes": PRESERVATION_RECEIPT_BYTES,
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

NEXT_GATE = (
    "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_RESULT_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_third_failed_attempt_preservation_result_review"
)


class Pair06V8ThirdPreservationResultAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ThirdPreservationResultAcceptanceHold(message)


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


def accept_pair06_v8_third_preservation_result(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _require(
        isinstance(evidence, Mapping),
        "third preservation evidence must be object",
    )
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "third preservation evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"third preservation evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "third preservation evidence digest drift",
    )
    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_third_preservation_result_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "archive_name": ARCHIVE_NAME,
        "preservation_receipt_logical_sha256": (
            PRESERVATION_RECEIPT_LOGICAL_SHA256
        ),
        "preservation_receipt_file_sha256": (
            PRESERVATION_RECEIPT_FILE_SHA256
        ),
        "preservation_receipt_bytes": PRESERVATION_RECEIPT_BYTES,
        "third_failed_attempt_archived": True,
        "third_failed_attempt_deleted": False,
        "prior_failed_attempt_archives_unchanged": True,
        "fresh_baseline_arm_root_available": True,
        "authorized_execution_head_preserved": AUTHORIZED_EXECUTION_HEAD,
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


def pair06_v8_third_preservation_result_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_third_preservation_result(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_third_preservation_result_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "archive_name": ARCHIVE_NAME,
        "third_failed_attempt_archived": True,
        "third_failed_attempt_deleted": False,
        "prior_failed_attempt_archives_unchanged": True,
        "fresh_baseline_arm_root_available": True,
        "authorized_execution_head_preserved": AUTHORIZED_EXECUTION_HEAD,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def request_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ThirdPreservationResultAcceptanceHold(NEXT_GATE)
