"""Source-only acceptance of successful second pair-06 V8 failed-attempt preservation.

This binds the exact Precision preservation terminal for consumed attempt
446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1.
It grants no retry or execution authority.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-preservation-result-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-preservation-result-acceptance.v1"
)

AUTHORIZED_MAIN_HEAD = "88edd6d4b69e6d6869b74dca85df3fc3b0bd5a23"
ATTEMPT_MARKER_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)
ARCHIVE_NAME = "baseline-20260923T235031Z-446d8f92"
ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    + ARCHIVE_NAME
)
PRESERVATION_RECEIPT_LOGICAL_SHA256 = (
    "d14d65eb507a8d86c55e866cf227c96989e0ee327ce62955cf958183bb51572b"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bb0bbfe5c7441706ce61924a718c4055a8e2c991c117f699ad5aa0c7863339b4"
)
WARM_START_SHA256 = (
    "2266fb31a1b78b9dee950bcc1ce2eb77ebf961856e2df4b257a3c83309ee10e5"
)
TRAJECTORY_SHA256 = (
    "955545e7b29377362da2e0f6cd58a113a802aba2ade3a0a32532066944a9d897"
)
PRIOR_ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
PRIOR_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "d32cc7779fb1570ac2085031e296817059ce51d35de43ca3875becf9d032ccff"
)

EXPECTED_EVIDENCE = {
    "authorized_main_head": AUTHORIZED_MAIN_HEAD,
    "pair_slot": 6,
    "arm": "baseline",
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "archive_name": ARCHIVE_NAME,
    "archive_path": ARCHIVE_PATH,
    "failed_arm_source_present_after_preservation": False,
    "archive_present_after_preservation": True,
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
    "prior_failed_attempt_archive_unchanged": True,
    "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
    "prior_preservation_receipt_file_sha256": (
        PRIOR_PRESERVATION_RECEIPT_FILE_SHA256
    ),
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

NEXT_GATE = "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_no_offload_baseline_attempt_invocation"


class Pair06V8SecondPreservationResultAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8SecondPreservationResultAcceptanceHold(message)


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


def accept_pair06_v8_second_preservation_result(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _require(isinstance(evidence, Mapping), "second preservation evidence must be object")
    supplied = dict(evidence)
    _require(set(supplied) == set(EXPECTED_EVIDENCE), "second preservation evidence field-set drift")
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"second preservation evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "second preservation evidence digest drift",
    )
    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_second_preservation_result_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "archive_name": ARCHIVE_NAME,
        "preservation_receipt_logical_sha256": PRESERVATION_RECEIPT_LOGICAL_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "second_failed_attempt_archived": True,
        "second_failed_attempt_deleted": False,
        "prior_failed_attempt_archive_unchanged": True,
        "fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt": True,
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


def pair06_v8_second_preservation_result_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_second_preservation_result(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_second_preservation_result_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "archive_name": ARCHIVE_NAME,
        "second_failed_attempt_archived": True,
        "second_failed_attempt_deleted": False,
        "prior_failed_attempt_archive_unchanged": True,
        "fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def request_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8SecondPreservationResultAcceptanceHold(NEXT_GATE)
