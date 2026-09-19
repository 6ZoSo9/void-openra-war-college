"""Source-only acceptance of exact pair-03 baseline preservation evidence.

This gate composes the independently reviewed one-retry authorization with the
exact completed failed-attempt preservation receipt. Only after both are valid
does exactly one pair-03 baseline retry become executable.

Importing this module performs no host I/O or runtime action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_source_binding_review_generation2
    as preservation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_authorization_source_binding_review_generation2
    as retry_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-preservation-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-preservation-evidence-acceptance.v1"
)

PRESERVATION_LAUNCHER_SHA256 = (
    "3980af4eefd8d3cbeb8e5f4d635ad9765444173714fba74012e0f4e089bfa6b4"
)
PRESERVATION_RECEIPT_SHA256 = (
    "564be959096b6895aae3158eb3020d6b2062dcfdbf461e04a7969b8cee815dd9"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)
PRESERVATION_MAIN_HEAD = "b51137277ab5b17631712ecd035af85d4b8d81c8"
FORENSICS_SHA256 = (
    "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d"
)
ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/failed-attempts/"
    "baseline-20260918T233630Z-98773549"
)
PRESERVATION_RECEIPT_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/failed-attempts/"
    "baseline-20260918T233630Z-98773549-preservation-receipt.json"
)
CANONICAL_ARM_PATH = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/baseline"
)
WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
WARM_START_BYTES = 223319

EXPECTED_EVIDENCE = {
    "preservation_launcher_sha256": PRESERVATION_LAUNCHER_SHA256,
    "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
    "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
    "preservation_main_head": PRESERVATION_MAIN_HEAD,
    "forensics_sha256": FORENSICS_SHA256,
    "pair_slot": 3,
    "arm": "baseline",
    "canonical_arm_path": CANONICAL_ARM_PATH,
    "canonical_arm_path_absent_after_preservation": True,
    "archive_path": ARCHIVE_PATH,
    "archive_path_present_after_preservation": True,
    "preservation_receipt_path": PRESERVATION_RECEIPT_PATH,
    "preservation_receipt_present": True,
    "atomic_rename_performed": True,
    "archived_tree_unchanged": True,
    "arm_root_inode_preserved": True,
    "warm_start_inode_preserved": True,
    "failed_attempt_deleted": False,
    "warm_start_sha256": WARM_START_SHA256,
    "warm_start_bytes": WARM_START_BYTES,
    "runtime_retry_performed": False,
    "runtime_retry_authorized_by_preservation": False,
    "runtime_start_performed": False,
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

NEXT_GATE = "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_retry_invocation"


class V2R13Pair03BaselinePreservationEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselinePreservationEvidenceAcceptanceHold(message)


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


def _validate_dependencies() -> dict[str, Any]:
    preservation = (
        preservation_review
        .v2r13_pair03_baseline_failed_attempt_preservation_review_contract()
    )
    authorization = retry_review.v2r13_pair03_baseline_retry_authorization_review_contract()

    _require(
        preservation.get("preservation_source_binding_present") is True,
        "preservation source binding missing",
    )
    _require(preservation.get("preservation_reviewed") is True, "preservation review missing")
    _require(
        preservation.get("runtime_retry_authorized") is False,
        "preservation review unexpectedly authorizes retry",
    )

    _require(
        authorization.get("authorization_source_binding_present") is True,
        "retry authorization source binding missing",
    )
    _require(authorization.get("authorization_reviewed") is True, "retry authorization review missing")
    _require(
        authorization.get("single_pair03_baseline_retry_authorized_after_preservation") is True,
        "single retry authorization missing",
    )
    _require(authorization.get("max_retry_executions") == 1, "retry-count drift")
    _require(authorization.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        authorization.get("retry_execution_authorized_now") is False,
        "retry became executable before preservation acceptance",
    )
    _require(
        authorization.get("preservation_evidence_acceptance_required") is True,
        "preservation evidence dependency lost",
    )

    return {
        "preservation_review": deepcopy(preservation),
        "retry_authorization_review": deepcopy(authorization),
    }


def accept_pair03_baseline_preservation_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependencies = _validate_dependencies()
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
        "held_out": False,
        "failed_attempt_preserved": True,
        "canonical_arm_path_available_for_retry": True,
        "retry_authorization_accepted": True,
        "retry_execution_authorized_now": True,
        "max_retry_executions": 1,
        "remaining_retry_executions": 1,
        "automatic_retry": False,
        "candidate_arm_authorized": False,
        "held_out_arm_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "runtime_retry_performed": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "dependencies": dependencies,
    }


def v2r13_pair03_baseline_preservation_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair03_baseline_preservation_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_launcher_sha256": PRESERVATION_LAUNCHER_SHA256,
        "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "preservation_evidence_accepted": True,
        "pair_slot": 3,
        "arm": "baseline",
        "retry_execution_authorized_now": True,
        "max_retry_executions": 1,
        "remaining_retry_executions": 1,
        "automatic_retry": False,
        "runtime_retry_performed": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def execute_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselinePreservationEvidenceAcceptanceHold(NEXT_GATE)
