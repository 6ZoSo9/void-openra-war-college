"""One-shot invocation for the additionally authorized V2R13 pair-03 baseline retry.

This source consumes the independently reviewed retry-index-2 authorization,
reuses the repaired preload-capable first-baseline executor, and re-verifies
both preserved failed-attempt archives before any runtime action.

Importing or inspecting this module performs no host action. A failed execution
fails closed and no automatic or recursive retry is implemented.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as first_baseline,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_worktree_readiness_repair_source_binding_review_generation2
    as worktree_repair_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_model_preload_repair_source_binding_review_generation2
    as preload_repair_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_authorization_source_binding_review_generation2
    as authorization_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_evidence_source_binding_review_generation2
    as preservation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-additional-retry-invocation-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-additional-retry-invocation-receipt.v1"
)

PAIR_SLOT = 3
ARM = "baseline"
RETRY_INDEX = 2
MAX_ADDITIONAL_RETRY_EXECUTIONS = 1
TOTAL_RETRY_EXECUTIONS_AUTHORIZED = 2
CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE_RETRY2_833FB5BD"
)

PAIR_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03"
)
CANONICAL_ARM = PAIR_ROOT / "baseline"
ARCHIVE_PARENT = PAIR_ROOT / "failed-attempts"

FIRST_ARCHIVE = ARCHIVE_PARENT / "baseline-20260918T233630Z-98773549"
FIRST_RECEIPT = (
    ARCHIVE_PARENT
    / "baseline-20260918T233630Z-98773549-preservation-receipt.json"
)
FIRST_WARM_REL = Path(
    "runs/warmstart-apollyon-vs-abaddon-20260918T233630Z-feinter-s1990061685/"
    "warm-start.jsonl"
)
FIRST_WARM_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
FIRST_WARM_BYTES = 223319
FIRST_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)

RETRY1_ARCHIVE = (
    ARCHIVE_PARENT / "baseline-retry-1-20260919T121144Z-71e90fdc"
)
RETRY1_RECEIPT = (
    ARCHIVE_PARENT
    / "baseline-retry-1-20260919T121144Z-71e90fdc-preservation-receipt.json"
)
RETRY1_WARM_REL = Path(
    "runs/warmstart-apollyon-vs-abaddon-20260919T121144Z-feinter-s1990061685/"
    "warm-start.jsonl"
)
RETRY1_WARM_SHA256 = (
    "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
)
RETRY1_WARM_BYTES = 223319
RETRY1_RECEIPT_SHA256 = (
    "833fb5bde1bbb96d6e2ceedff615fd86bf3b2522d21687d900355cbe705a0f15"
)
RETRY1_RECEIPT_FILE_SHA256 = (
    "007127f4834e3b2c772316f2f65a3b355c308a7a451eca996ad00c21f3f7cd28"
)
RETRY1_FORENSICS_SHA256 = (
    "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d"
)

NEXT_GATE = (
    "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_EXECUTION_EVIDENCE_ACCEPTANCE_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair03_baseline_additional_retry_execution_evidence_acceptance"
)


class V2R13Pair03BaselineAdditionalRetryInvocationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineAdditionalRetryInvocationHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=str,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _hash_exact_regular_file(path: Path, expected_bytes: int | None = None) -> str:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        _require(stat.S_ISREG(before.st_mode), f"not regular file: {path}")
        if expected_bytes is not None:
            _require(before.st_size == expected_bytes, f"byte-count drift: {path}")
        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            digest.update(chunk)
        after = os.fstat(fd)
        _require(
            (
                before.st_dev,
                before.st_ino,
                before.st_mode,
                before.st_size,
                before.st_mtime_ns,
                before.st_ctime_ns,
            )
            == (
                after.st_dev,
                after.st_ino,
                after.st_mode,
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ),
            f"file generation changed during hash: {path}",
        )
        if expected_bytes is not None:
            _require(total == expected_bytes, f"read byte-count drift: {path}")
        return digest.hexdigest()
    finally:
        os.close(fd)


def _validate_dependencies() -> dict[str, Any]:
    worktree = (
        worktree_repair_review
        .v2r13_first_baseline_worktree_readiness_repair_review_contract()
    )
    preload = (
        preload_repair_review
        .v2r13_model_preload_repair_source_binding_review_contract()
    )
    authorization = (
        authorization_review
        .v2r13_pair03_baseline_additional_retry_authorization_review_contract()
    )
    preservation = (
        preservation_review
        .v2r13_pair03_failed_retry_preservation_evidence_review_contract()
    )

    _require(worktree.get("repair_source_binding_present") is True, "worktree repair binding missing")
    _require(worktree.get("repair_reviewed") is True, "worktree repair review missing")
    _require(worktree.get("runtime_retry_authorized") is False, "worktree repair grants retry authority")

    _require(preload.get("repair_source_binding_present") is True, "preload repair binding missing")
    _require(preload.get("repair_reviewed") is True, "preload repair review missing")
    _require(preload.get("exact_v2r13_model_preload_reviewed") is True, "exact model preload review missing")
    _require(preload.get("model_inference_during_preload") is False, "preload crosses inference boundary")

    _require(authorization.get("authorization_source_binding_present") is True, "additional retry authorization binding missing")
    _require(authorization.get("authorization_reviewed") is True, "additional retry authorization review missing")
    _require(authorization.get("retry_index") == RETRY_INDEX, "additional retry authorization index drift")
    _require(
        authorization.get("single_additional_pair03_baseline_retry_authorized") is True,
        "single additional retry authorization missing",
    )
    _require(
        authorization.get("max_additional_retry_executions")
        == MAX_ADDITIONAL_RETRY_EXECUTIONS,
        "additional retry execution count drift",
    )
    _require(
        authorization.get("total_retry_executions_authorized")
        == TOTAL_RETRY_EXECUTIONS_AUTHORIZED,
        "total retry authorization count drift",
    )
    _require(
        authorization.get("additional_retry_execution_authorized_now") is True,
        "additional retry is not executable after review",
    )
    _require(
        authorization.get("additional_retry_execution_performed") is False,
        "additional retry already recorded executed",
    )
    _require(authorization.get("automatic_retry") is False, "automatic retry enabled")

    _require(
        preservation.get("preservation_evidence_source_binding_present") is True,
        "failed-retry preservation evidence binding missing",
    )
    _require(
        preservation.get("preservation_evidence_reviewed") is True,
        "failed-retry preservation evidence review missing",
    )
    _require(
        preservation.get("retry_authorization_consumed") is True,
        "prior retry authorization not consumed",
    )
    _require(
        preservation.get("additional_retry_authorized") is False,
        "preservation review itself grants additional retry authority",
    )
    _require(
        preservation.get("runtime_execution_authorized_now") is False,
        "preservation review itself authorizes runtime execution",
    )

    return {
        "worktree_repair_review": worktree,
        "model_preload_repair_review": preload,
        "additional_retry_authorization_review": authorization,
        "failed_retry_preservation_evidence_review": preservation,
    }


def _validate_preserved_history_on_host() -> dict[str, Any]:
    _require(CANONICAL_ARM.exists() is False, "canonical pair-03 baseline path already consumed")

    for archive, label in (
        (FIRST_ARCHIVE, "first failed-attempt archive"),
        (RETRY1_ARCHIVE, "retry-1 failed-attempt archive"),
    ):
        _require(archive.is_dir(), f"{label} missing")
        _require(not archive.is_symlink(), f"{label} symlinked")

    _require(FIRST_RECEIPT.is_file(), "first preservation receipt missing")
    _require(not FIRST_RECEIPT.is_symlink(), "first preservation receipt symlinked")
    first_receipt_file_sha = _hash_exact_regular_file(FIRST_RECEIPT)
    _require(
        first_receipt_file_sha == FIRST_RECEIPT_FILE_SHA256,
        "first preservation receipt file SHA drift",
    )

    first_warm = FIRST_ARCHIVE / FIRST_WARM_REL
    _require(first_warm.is_file(), "first archived warm-start missing")
    _require(not first_warm.is_symlink(), "first archived warm-start symlinked")
    first_warm_sha = _hash_exact_regular_file(first_warm, FIRST_WARM_BYTES)
    _require(first_warm_sha == FIRST_WARM_SHA256, "first archived warm-start SHA drift")

    _require(RETRY1_RECEIPT.is_file(), "retry-1 preservation receipt missing")
    _require(not RETRY1_RECEIPT.is_symlink(), "retry-1 preservation receipt symlinked")
    retry1_receipt_file_sha = _hash_exact_regular_file(RETRY1_RECEIPT)
    _require(
        retry1_receipt_file_sha == RETRY1_RECEIPT_FILE_SHA256,
        "retry-1 preservation receipt file SHA drift",
    )
    try:
        retry1_receipt = json.loads(RETRY1_RECEIPT.read_text(encoding="utf-8"))
    except Exception as error:
        raise V2R13Pair03BaselineAdditionalRetryInvocationHold(
            f"retry-1 preservation receipt JSON invalid: {error}"
        ) from error
    _require(isinstance(retry1_receipt, dict), "retry-1 preservation receipt must be object")
    _require(retry1_receipt.get("pair_slot") == 3, "retry-1 preservation pair-slot drift")
    _require(retry1_receipt.get("arm") == "baseline", "retry-1 preservation arm drift")
    _require(retry1_receipt.get("retry_index") == 1, "retry-1 preservation index drift")
    _require(
        retry1_receipt.get("failed_retry_forensics_sha256") == RETRY1_FORENSICS_SHA256,
        "retry-1 forensics SHA drift",
    )
    _require(
        retry1_receipt.get("preservation_receipt_sha256") == RETRY1_RECEIPT_SHA256,
        "retry-1 preservation semantic SHA drift",
    )
    _require(retry1_receipt.get("atomic_rename_performed") is True, "retry-1 atomic preservation missing")
    _require(retry1_receipt.get("source_path_absent_after_preservation") is True, "retry-1 source path not recorded absent")
    _require(retry1_receipt.get("archive_path_present_after_preservation") is True, "retry-1 archive not recorded present")
    _require(retry1_receipt.get("archived_retry_tree_unchanged") is True, "retry-1 archive tree changed")
    _require(retry1_receipt.get("failed_retry_deleted") is False, "retry-1 marked deleted")
    _require(retry1_receipt.get("additional_retry_authorized") is False, "retry-1 preservation grants retry authority")
    _require(retry1_receipt.get("additional_retry_performed") is False, "retry-1 preservation records another retry")

    retry1_warm = RETRY1_ARCHIVE / RETRY1_WARM_REL
    _require(retry1_warm.is_file(), "retry-1 archived warm-start missing")
    _require(not retry1_warm.is_symlink(), "retry-1 archived warm-start symlinked")
    retry1_warm_sha = _hash_exact_regular_file(retry1_warm, RETRY1_WARM_BYTES)
    _require(retry1_warm_sha == RETRY1_WARM_SHA256, "retry-1 archived warm-start SHA drift")

    return {
        "first_preservation_receipt_file_sha256": first_receipt_file_sha,
        "first_warm_start_sha256": first_warm_sha,
        "retry1_preservation_receipt_file_sha256": retry1_receipt_file_sha,
        "retry1_preservation_receipt_sha256": retry1_receipt["preservation_receipt_sha256"],
        "retry1_warm_start_sha256": retry1_warm_sha,
    }


def execute_pair03_baseline_additional_retry(*, confirm: str) -> dict[str, Any]:
    _require(
        confirm == CONFIRM_TOKEN,
        "PAIR03_BASELINE_ADDITIONAL_RETRY_CONFIRMATION_REQUIRED",
    )
    dependencies = _validate_dependencies()
    preserved = _validate_preserved_history_on_host()

    invocation = first_baseline.execute_first_baseline(
        confirm=first_baseline.CONFIRM_TOKEN,
    )

    _require(invocation.get("pair_slot") == 3, "additional retry invocation pair-slot drift")
    _require(invocation.get("arm") == "baseline", "additional retry invocation arm drift")
    _require(invocation.get("held_out") is False, "additional retry unexpectedly held-out")
    _require(
        invocation.get("runtime_execution_performed") is True,
        "additional retry runtime execution not completed",
    )
    _require(
        invocation.get("fresh_runtime_readiness_admitted") is True,
        "additional retry fresh readiness not admitted",
    )
    _require(
        invocation.get("runtime_cleanup_completed") is True,
        "additional retry runtime cleanup incomplete",
    )
    _require(invocation.get("automatic_retry") is False, "underlying automatic retry enabled")
    _require(invocation.get("candidate_arm_executed") is False, "candidate arm executed")
    _require(invocation.get("held_out_arm_executed") is False, "held-out arm executed")

    for field in (
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(invocation.get(field) is False, f"additional retry boundary crossed: {field}")

    body = {
        "schema": RECEIPT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "retry_index": RETRY_INDEX,
        "max_additional_retry_executions": MAX_ADDITIONAL_RETRY_EXECUTIONS,
        "total_retry_executions_authorized": TOTAL_RETRY_EXECUTIONS_AUTHORIZED,
        "additional_retry_authorization_consumed": True,
        "additional_retry_execution_performed": True,
        "remaining_additional_retry_executions": 0,
        "automatic_retry": False,
        "retry1_preservation_receipt_sha256": RETRY1_RECEIPT_SHA256,
        "retry1_preservation_receipt_file_sha256": RETRY1_RECEIPT_FILE_SHA256,
        "retry1_preserved_warm_start_sha256": RETRY1_WARM_SHA256,
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "candidate_arm_executed": False,
        "held_out_arm_executed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "underlying_invocation_receipt_sha256": invocation.get(
            "invocation_receipt_sha256"
        ),
        "underlying_executor_receipt_sha256": (
            invocation.get("executor_receipt") or {}
        ).get("execution_receipt_sha256"),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }
    return {
        **body,
        "additional_retry_invocation_receipt_sha256": _digest(body),
        "preserved_history_host_recheck": preserved,
        "underlying_invocation": invocation,
        "dependencies": dependencies,
    }


def v2r13_pair03_baseline_additional_retry_invocation_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "retry_index": RETRY_INDEX,
        "max_additional_retry_executions": MAX_ADDITIONAL_RETRY_EXECUTIONS,
        "total_retry_executions_authorized": TOTAL_RETRY_EXECUTIONS_AUTHORIZED,
        "confirm_token": CONFIRM_TOKEN,
        "live_preserved_history_recheck_required": True,
        "first_failed_attempt_archive_recheck_required": True,
        "retry1_failed_attempt_archive_recheck_required": True,
        "retry1_preservation_receipt_sha256": RETRY1_RECEIPT_SHA256,
        "retry1_preservation_receipt_file_sha256": RETRY1_RECEIPT_FILE_SHA256,
        "retry1_preserved_warm_start_sha256": RETRY1_WARM_SHA256,
        "repaired_first_baseline_executor_reused": True,
        "worktree_readiness_repair_review_required": True,
        "model_preload_repair_review_required": True,
        "exact_v2r13_model_preload_before_readiness_required": True,
        "model_preload_inference_forbidden": True,
        "additional_retry_execution_authorized": True,
        "additional_retry_execution_performed_by_contract_inspection": False,
        "remaining_additional_retry_executions_before_invocation": 1,
        "automatic_retry": False,
        "recursive_retry_implemented": False,
        "candidate_arm_implemented_by_this_source": False,
        "held_out_arm_implemented_by_this_source": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": (
            "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "next_change_class": (
            "source_only_v2r13_pair03_baseline_additional_retry_invocation_source_binding_review"
        ),
        "dependencies": dependencies,
    }
