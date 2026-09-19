"""Source-only acceptance of the failed pair-03 baseline retry forensic record.

This gate binds the exact read-only Precision census captured after the single
authorized retry failed during fresh readiness at the Ollama /api/ps residency
check. It records that warm-start completed, controller inference did not occur,
cleanup completed, and the original first-attempt archive remained unchanged.

No filesystem mutation, service action, runtime start, model load/inference,
game execution, training, promotion, deployment, VOID-chain mutation, funds
action, or additional retry authority is implemented here.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_preload_rebind_source_binding_review_generation2
    as rebind_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-retry-forensics-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-retry-forensics-acceptance.v1"
)

FORENSICS_WRAPPER_SHA256 = (
    "9922da0e8d696bfde713c871924d3d27375776226965ac4bf15a3fb2a708f7dd"
)
FORENSICS_SHA256 = (
    "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d"
)
FAILED_RETRY_MAIN_HEAD = "8c9fdf60d83c004591684030958137d3db2545d5"
FAILED_RETRY_ARM_ROOT = (
    "/home/zoso/dev/void-war-college-execution/"
    "v2r13-generation2/generation2/pair-03/baseline"
)
FAILED_RETRY_RUN_DIRECTORY = (
    "runs/warmstart-apollyon-vs-abaddon-20260919T121144Z-feinter-s1990061685"
)
FAILED_RETRY_WARM_START_SHA256 = (
    "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
)
FAILED_RETRY_WARM_START_BYTES = 223319

FIRST_ATTEMPT_ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/failed-attempts/"
    "baseline-20260918T233630Z-98773549"
)
FIRST_ATTEMPT_WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
FIRST_ATTEMPT_WARM_START_BYTES = 223319
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)

EXPECTED_EVIDENCE = {
    "forensics_wrapper_sha256": FORENSICS_WRAPPER_SHA256,
    "forensics_sha256": FORENSICS_SHA256,
    "repo_head": FAILED_RETRY_MAIN_HEAD,
    "repo_branch": "main",
    "repo_tracked_clean": True,
    "pair_slot": 3,
    "arm": "baseline",
    "retry_index": 1,
    "max_retry_executions": 1,
    "arm_root": FAILED_RETRY_ARM_ROOT,
    "arm_root_exists": True,
    "run_directory": FAILED_RETRY_RUN_DIRECTORY,
    "tree_entry_count": 4,
    "directory_count": 3,
    "regular_file_count": 1,
    "symlink_count": 0,
    "retry_warm_start_sha256": FAILED_RETRY_WARM_START_SHA256,
    "retry_warm_start_bytes": FAILED_RETRY_WARM_START_BYTES,
    "retry_warm_start_present": True,
    "source_worktree_exists": False,
    "source_worktree_registered": False,
    "engine_worktree_exists": False,
    "engine_worktree_registered": False,
    "execution_receipt_exists": False,
    "retry_execution_receipt_present": False,
    "retry_failure_stage": (
        "fresh_readiness_ollama_ps_before_controller_inference"
    ),
    "retry_model_alias_catalog_verified": True,
    "retry_model_digest_catalog_verified": True,
    "retry_controller_inference_performed": False,
    "ollama_active": "inactive",
    "ollama_enabled": "disabled",
    "activation_permit_present": False,
    "matching_runtime_process_count": 0,
    "relevant_listener_count": 0,
    "matching_container_count": 0,
    "first_attempt_archive_path": FIRST_ATTEMPT_ARCHIVE_PATH,
    "first_attempt_archive_present": True,
    "first_attempt_archived_warm_start_sha256": (
        FIRST_ATTEMPT_WARM_START_SHA256
    ),
    "first_attempt_archived_warm_start_bytes": FIRST_ATTEMPT_WARM_START_BYTES,
    "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
    "additional_retry_performed": False,
    "forensics_mutation_performed": False,
}

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_failed_retry_preservation"


class V2R13Pair03BaselineFailedRetryForensicsAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineFailedRetryForensicsAcceptanceHold(message)


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
        rebind_review
        .v2r13_pair03_baseline_retry_preload_rebind_review_contract()
    )
    _require(
        reviewed.get("retry_preload_rebind_source_binding_present") is True,
        "retry preload rebind source binding missing",
    )
    _require(
        reviewed.get("retry_preload_rebind_reviewed") is True,
        "retry preload rebind review missing",
    )
    _require(
        reviewed.get("additional_retry_authorized") is False,
        "retry preload review unexpectedly authorizes another retry",
    )
    _require(
        reviewed.get("failed_retry_forensics_required") is True,
        "failed-retry forensic requirement lost",
    )
    _require(
        reviewed.get("next_gate")
        == "V2R13_PAIR03_BASELINE_FAILED_RETRY_FORENSICS_REQUIRED",
        "retry preload review forensic frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair03_baseline_failed_retry_forensics(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "failed-retry evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "failed-retry evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"failed-retry evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "failed-retry evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "failed_retry_forensics_accepted": True,
        "forensics_wrapper_sha256": FORENSICS_WRAPPER_SHA256,
        "forensics_sha256": FORENSICS_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 1,
        "runtime_started": True,
        "warm_start_completed": True,
        "fresh_readiness_failed_before_controller_inference": True,
        "failure_was_ollama_ps_residency_gate": True,
        "catalog_model_alias_verified": True,
        "catalog_model_digest_verified": True,
        "controller_inference_performed": False,
        "controller_trajectory_present": False,
        "controller_summary_present": False,
        "successful_execution_receipt_present": False,
        "runtime_cleanup_completed": True,
        "source_worktree_cleaned": True,
        "engine_worktree_cleaned": True,
        "ollama_dormant_after_failure": True,
        "runtime_processes_remaining": False,
        "runtime_listeners_remaining": False,
        "runtime_containers_remaining": False,
        "first_attempt_archive_preserved": True,
        "first_attempt_preservation_receipt_preserved": True,
        "retry_authorization_consumed": True,
        "additional_retry_authorized": False,
        "additional_retry_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "failed_retry_preservation_required": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "dependency_review": dependency,
    }


def v2r13_pair03_baseline_failed_retry_forensics_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair03_baseline_failed_retry_forensics(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "forensics_wrapper_sha256": FORENSICS_WRAPPER_SHA256,
        "forensics_sha256": FORENSICS_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "failed_retry_forensics_accepted": True,
        "retry_authorization_consumed": True,
        "additional_retry_authorized": False,
        "additional_retry_performed": False,
        "failed_retry_preservation_required": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def preserve_failed_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineFailedRetryForensicsAcceptanceHold(NEXT_GATE)
