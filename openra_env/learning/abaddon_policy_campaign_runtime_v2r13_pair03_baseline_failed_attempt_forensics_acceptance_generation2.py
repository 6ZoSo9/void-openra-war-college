"""Source-only acceptance of the failed pair-03 baseline forensic record.

This module binds the exact read-only Precision forensic census captured after
the first bounded V2R13 pair-03 baseline attempt failed during fresh-readiness
admission. It preserves the distinction between a started/cleaned runtime and a
successfully admitted controller bout.

No filesystem mutation, runtime action, retry, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action is implemented here.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_worktree_readiness_repair_source_binding_review_generation2
    as repair_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-attempt-forensics-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-attempt-forensics-acceptance.v1"
)

FORENSICS_WRAPPER_SHA256 = (
    "24364e9ea26e67720d1f2e14310426a749cd891bca1564fc73809c78c4431bf3"
)
FORENSICS_SHA256 = (
    "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d"
)
FAILED_ATTEMPT_MAIN_HEAD = "de422ebc1495b34884c8208a8631579a93a12bbf"
FAILED_ARM_ROOT = (
    "/home/zoso/dev/void-war-college-execution/"
    "v2r13-generation2/generation2/pair-03/baseline"
)
FAILED_RUN_DIRECTORY = (
    "runs/warmstart-apollyon-vs-abaddon-20260918T233630Z-feinter-s1990061685"
)
WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
WARM_START_BYTES = 223319

EXPECTED_EVIDENCE = {
    "forensics_wrapper_sha256": FORENSICS_WRAPPER_SHA256,
    "forensics_sha256": FORENSICS_SHA256,
    "repo_head": FAILED_ATTEMPT_MAIN_HEAD,
    "repo_branch": "main",
    "repo_tracked_clean": True,
    "arm_root": FAILED_ARM_ROOT,
    "arm_root_exists": True,
    "run_directory": FAILED_RUN_DIRECTORY,
    "tree_entry_count": 4,
    "directory_count": 3,
    "regular_file_count": 1,
    "symlink_count": 0,
    "warm_start_sha256": WARM_START_SHA256,
    "warm_start_bytes": WARM_START_BYTES,
    "frozen_source_worktree_exists": False,
    "frozen_source_worktree_registered": False,
    "engine_worktree_exists": False,
    "engine_worktree_registered": False,
    "invocation_receipt_exists": False,
    "runtime_execution_receipt_present": False,
    "ollama_active": "inactive",
    "ollama_enabled": "disabled",
    "activation_permit_present": False,
    "matching_runtime_process_count": 0,
    "relevant_listener_count": 0,
    "matching_container_count": 0,
    "automatic_retry_performed": False,
    "forensics_mutation_performed": False,
    "warm_start_completed": True,
    "fresh_readiness_failed_before_controller_inference": True,
    "controller_inference_performed": False,
    "controller_trajectory_present": False,
    "controller_summary_present": False,
}

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_failed_attempt_preservation"


class V2R13Pair03BaselineFailedAttemptForensicsAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineFailedAttemptForensicsAcceptanceHold(message)


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
    reviewed = (
        repair_review
        .v2r13_first_baseline_worktree_readiness_repair_review_contract()
    )
    _require(
        reviewed.get("repair_source_binding_present") is True,
        "readiness repair source binding missing",
    )
    _require(reviewed.get("repair_reviewed") is True, "readiness repair not reviewed")
    _require(
        reviewed.get("runtime_retry_authorized") is False,
        "repair review unexpectedly authorizes retry",
    )
    _require(
        reviewed.get("failed_attempt_forensics_required") is True,
        "failed-attempt forensics requirement lost",
    )
    _require(
        reviewed.get("next_gate")
        == "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_FORENSICS_REQUIRED",
        "repair-review forensic frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair03_baseline_failed_attempt_forensics(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_dependency()
    _require(isinstance(evidence, Mapping), "forensic evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "forensic evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"forensic evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "forensic evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "failed_attempt_forensics_accepted": True,
        "forensics_wrapper_sha256": FORENSICS_WRAPPER_SHA256,
        "forensics_sha256": FORENSICS_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "pair_slot": 3,
        "arm": "baseline",
        "failed_arm_root": FAILED_ARM_ROOT,
        "failed_run_directory": FAILED_RUN_DIRECTORY,
        "warm_start_sha256": WARM_START_SHA256,
        "warm_start_bytes": WARM_START_BYTES,
        "runtime_started": True,
        "warm_start_completed": True,
        "fresh_readiness_failed_before_controller_inference": True,
        "controller_inference_performed": False,
        "controller_trajectory_present": False,
        "controller_summary_present": False,
        "successful_execution_receipt_present": False,
        "runtime_cleanup_completed": True,
        "frozen_source_worktree_cleaned": True,
        "engine_worktree_cleaned": True,
        "ollama_dormant_after_failure": True,
        "runtime_processes_remaining": False,
        "runtime_listeners_remaining": False,
        "runtime_containers_remaining": False,
        "automatic_retry_performed": False,
        "retry_authorized": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "failed_attempt_preservation_required_before_retry": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def v2r13_pair03_baseline_failed_attempt_forensics_acceptance_contract() -> dict[str, Any]:
    dependency = _validate_dependency()
    accepted = accept_pair03_baseline_failed_attempt_forensics(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "forensics_wrapper_sha256": FORENSICS_WRAPPER_SHA256,
        "forensics_sha256": FORENSICS_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "failed_attempt_forensics_accepted": True,
        "runtime_cleanup_completed": True,
        "successful_execution_receipt_present": False,
        "controller_inference_performed": False,
        "automatic_retry_performed": False,
        "retry_authorized": False,
        "failed_attempt_preservation_required_before_retry": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
        "repair_review": dependency,
    }


def preserve_failed_attempt(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineFailedAttemptForensicsAcceptanceHold(NEXT_GATE)
