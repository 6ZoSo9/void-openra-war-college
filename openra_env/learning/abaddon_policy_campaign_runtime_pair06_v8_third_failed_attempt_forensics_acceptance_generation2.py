"""Source-only acceptance of the third consumed pair-06 V8 baseline failure.

Binds the exact read-only Precision forensic census for the receipt-bound
attempt consumed by the Transformers caching-allocator OOM. The residual tree
contains only the durable attempt marker plus two exact clean detached frozen
worktrees; the runs tree is empty and result/closeout/revocation are absent.

No cleanup, retry, runtime action, model action, game action, training,
deployment, VOID-chain mutation, or wallet/funds action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-forensics-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-forensics-acceptance.v1"
)

OBSERVER_SHA256 = (
    "e6ecf1527675bb2b80069bc1bd2d6771e306a7550a4947dbb7115210611e838b"
)
FAILED_MAIN_HEAD = "bdb305aeaec8288b817d648dcc86124b26f4b4c4"
FAILED_MAIN_TREE = "3af27c16689b1077fbf88395451cb5ea416e8a03"
ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)
PRIOR_ATTEMPT_MARKER_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)
INVOCATION_SOURCE_SHA256 = (
    "cd363ebc606fe83f2d5675a8af43d1a098b7fe27184fa33fba4a27522f47652b"
)
MATERIALIZATION_SHA256 = (
    "7733a01d9d60b70232f91b7ab123513efbc1c01345adc6fbcea2f53dc4a32b74"
)

MARKER_DEV = 2050
MARKER_INODE = 209756174
MARKER_BYTES = 974
MARKER_MODE = 600
MARKER_UID = 1000

FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
FROZEN_SOURCE_DEV = 2050
FROZEN_SOURCE_INODE = 209754014

ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"
ENGINE_DEV = 2050
ENGINE_INODE = 209754126

PRIOR_ARCHIVE_NAMES = (
    "baseline-20260923T221259Z-56c02591",
    "baseline-20260923T235031Z-446d8f92",
)
PRIOR_PRESERVATION_RECEIPT_NAMES = (
    "baseline-20260923T221259Z-56c02591-preservation-receipt.json",
    "baseline-20260923T235031Z-446d8f92-preservation-receipt.json",
)

EXPECTED_EVIDENCE = {
    "observer_sha256": OBSERVER_SHA256,
    "pair_slot": 6,
    "arm": "baseline",
    "held_out": False,
    "attempt_marker_present": True,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "attempt_marker_dev": MARKER_DEV,
    "attempt_marker_inode": MARKER_INODE,
    "attempt_marker_bytes": MARKER_BYTES,
    "attempt_marker_mode": MARKER_MODE,
    "attempt_marker_uid": MARKER_UID,
    "expected_main_head": FAILED_MAIN_HEAD,
    "main_tree": FAILED_MAIN_TREE,
    "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
    "materialization_sha256": MATERIALIZATION_SHA256,
    "maximum_attempts": 1,
    "automatic_retry": False,
    "pair06_baseline_specific_authorization_accepted": True,
    "runtime_load_authorized": True,
    "model_inference_authorized": True,
    "game_execution_authorized": True,
    "candidate_execution_authorized": False,
    "pair15_execution_authorized": False,
    "training_authorized": False,
    "weights_update_authorized": False,
    "automatic_policy_promotion_authorized": False,
    "deployment_authorized": False,
    "void_chain_mutation_authorized": False,
    "wallet_or_funds_action_authorized": False,
    "result_present": False,
    "closeout_present": False,
    "revocation_present": False,
    "baseline_top_level": ("claims-v1", "engine", "frozen-source", "runs-v1"),
    "claims_entries": ("pair06-v8-baseline-game-attempt-v1.json",),
    "runs_empty": True,
    "frozen_source_present": True,
    "frozen_source_clean": True,
    "frozen_source_detached": True,
    "frozen_source_commit": FROZEN_SOURCE_COMMIT,
    "frozen_source_tree": FROZEN_SOURCE_TREE,
    "frozen_source_dev": FROZEN_SOURCE_DEV,
    "frozen_source_inode": FROZEN_SOURCE_INODE,
    "engine_present": True,
    "engine_clean": True,
    "engine_detached": True,
    "engine_commit": ENGINE_COMMIT,
    "engine_tree": ENGINE_TREE,
    "engine_dev": ENGINE_DEV,
    "engine_inode": ENGINE_INODE,
    "prior_archive_names": PRIOR_ARCHIVE_NAMES,
    "prior_preservation_receipt_names": PRIOR_PRESERVATION_RECEIPT_NAMES,
    "failure_type": "OutOfMemoryError",
    "failure_stage": "transformers.caching_allocator_warmup",
    "preclaim_free_memory_bytes": 5756354560,
    "foreign_compute_pid": 2850305,
    "successful_game_result_present": False,
    "attempt_consumed": True,
    "runtime_retry_authorized": False,
}

NEXT_GATE = "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_third_failed_attempt_preservation"


class Pair06V8ThirdFailedAttemptForensicsAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ThirdFailedAttemptForensicsAcceptanceHold(message)


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


def _validate_reviewed_failure_lineage() -> dict[str, Any]:
    reviewed = (
        request_review
        .pair06_v8_preclaim_gpu_baseline_execution_authorization_request_review_contract()
    )
    validated = reviewed.get("validated_request")
    proposal = validated.get("request") if isinstance(validated, dict) else None
    lineage = proposal.get("lineage") if isinstance(proposal, dict) else None
    _require(isinstance(lineage, dict), "third failed-attempt lineage missing")
    _require(
        lineage.get("spent_oom_attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "third failed-attempt marker lineage drift",
    )
    _require(
        lineage.get("spent_oom_attempt_reusable") is False
        and lineage.get("spent_receipt_bound_attempt_consumed") is True,
        "third failed-attempt consumed/reuse state drift",
    )
    _require(
        lineage.get("spent_oom_failure_type") == "OutOfMemoryError"
        and lineage.get("spent_oom_failure_stage")
        == "transformers.caching_allocator_warmup",
        "third failed-attempt failure lineage drift",
    )
    _require(
        lineage.get("spent_oom_preclaim_free_memory_bytes") == 5756354560
        and lineage.get("spent_oom_foreign_compute_pid") == 2850305,
        "third failed-attempt GPU evidence lineage drift",
    )
    return deepcopy(reviewed)


def accept_pair06_v8_third_failed_attempt_forensics(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    reviewed = _validate_reviewed_failure_lineage()
    _require(
        isinstance(evidence, Mapping),
        "third failed-attempt evidence must be object",
    )
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "third failed-attempt evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"third failed-attempt evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "third failed-attempt evidence digest drift",
    )
    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_third_failed_attempt_forensics_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
        "attempt_distinct_from_prior": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "attempt_consumed": True,
        "automatic_retry": False,
        "failure_type": "OutOfMemoryError",
        "failure_stage": "transformers.caching_allocator_warmup",
        "successful_game_result_present": False,
        "residual_frozen_worktrees_present": True,
        "runs_empty": True,
        "prior_archives_preserved": True,
        "runtime_retry_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "third_failed_attempt_preservation_required": True,
        "reviewed_failure_lineage": reviewed,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def pair06_v8_third_failed_attempt_forensics_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_third_failed_attempt_forensics(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_third_failed_attempt_forensics_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
        "attempt_distinct_from_prior": True,
        "attempt_consumed": True,
        "successful_game_result_present": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "third_failed_attempt_preservation_required": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def preserve_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ThirdFailedAttemptForensicsAcceptanceHold(NEXT_GATE)
