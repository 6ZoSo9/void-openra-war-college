"""Explicitly authorized one-shot V2R13 pair-03 baseline retry invocation.

This source composes the repaired first-baseline executor with:
* exact preservation evidence acceptance;
* the independently reviewed one-retry authorization; and
* a live Precision preservation recheck immediately before retry.

Importing this module performs no host action.  The retry requires an exact
confirmation token and can execute only pair slot 03 baseline.  A failed retry
consumes the canonical arm path and therefore fails closed; no second retry is
implemented.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as first_baseline,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_worktree_readiness_repair_source_binding_review_generation2
    as repair_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_preservation_evidence_acceptance_generation2
    as preservation_acceptance,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_authorization_source_binding_review_generation2
    as retry_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry-invocation-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry-invocation-receipt.v1"
)

PAIR_SLOT = 3
ARM = "baseline"
RETRY_INDEX = 1
MAX_RETRY_EXECUTIONS = 1
CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_RETRY_PAIR03_BASELINE_ONCE_564BE959"
)

PAIR_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03"
)
CANONICAL_ARM = PAIR_ROOT / "baseline"
ARCHIVE_ROOT = (
    PAIR_ROOT
    / "failed-attempts"
    / "baseline-20260918T233630Z-98773549"
)
PRESERVATION_RECEIPT = (
    PAIR_ROOT
    / "failed-attempts"
    / "baseline-20260918T233630Z-98773549-preservation-receipt.json"
)
WARM_REL = Path(
    "runs/warmstart-apollyon-vs-abaddon-20260918T233630Z-feinter-s1990061685/"
    "warm-start.jsonl"
)

PRESERVATION_RECEIPT_SHA256 = (
    "564be959096b6895aae3158eb3020d6b2062dcfdbf461e04a7969b8cee815dd9"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)
FORENSICS_SHA256 = (
    "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d"
)
WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
WARM_START_BYTES = 223319

NEXT_GATE = "V2R13_PAIR03_BASELINE_RETRY_EXECUTION_EVIDENCE_ACCEPTANCE_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_retry_execution_evidence_acceptance"


class V2R13Pair03BaselineRetryInvocationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetryInvocationHold(message)


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
    repair = (
        repair_review
        .v2r13_first_baseline_worktree_readiness_repair_review_contract()
    )
    authorization = retry_review.v2r13_pair03_baseline_retry_authorization_review_contract()
    preservation = (
        preservation_acceptance
        .v2r13_pair03_baseline_preservation_evidence_acceptance_contract()
    )

    _require(repair.get("repair_source_binding_present") is True, "repair binding missing")
    _require(repair.get("repair_reviewed") is True, "repair review missing")
    _require(
        repair.get("runtime_retry_authorized") is False,
        "repair review unexpectedly grants retry authority",
    )

    _require(
        authorization.get("authorization_source_binding_present") is True,
        "retry authorization binding missing",
    )
    _require(authorization.get("authorization_reviewed") is True, "retry auth review missing")
    _require(
        authorization.get("single_pair03_baseline_retry_authorized_after_preservation")
        is True,
        "single retry authorization missing",
    )
    _require(authorization.get("max_retry_executions") == 1, "retry count drift")
    _require(authorization.get("automatic_retry") is False, "automatic retry enabled")

    _require(
        preservation.get("preservation_evidence_accepted") is True,
        "preservation evidence not accepted",
    )
    _require(
        preservation.get("retry_execution_authorized_now") is True,
        "retry is not executable after preservation",
    )
    _require(preservation.get("max_retry_executions") == 1, "preservation retry count drift")
    _require(
        preservation.get("remaining_retry_executions") == 1,
        "no retry execution remains",
    )
    _require(preservation.get("automatic_retry") is False, "automatic retry enabled")

    return {
        "repair_review": repair,
        "retry_authorization_review": authorization,
        "preservation_acceptance": preservation,
    }


def _validate_preservation_on_host() -> dict[str, Any]:
    _require(CANONICAL_ARM.exists() is False, "canonical pair-03 baseline path already consumed")
    _require(ARCHIVE_ROOT.is_dir(), "preserved failed-attempt archive missing")
    _require(not ARCHIVE_ROOT.is_symlink(), "preserved failed-attempt archive symlinked")
    _require(PRESERVATION_RECEIPT.is_file(), "preservation receipt missing")
    _require(not PRESERVATION_RECEIPT.is_symlink(), "preservation receipt symlinked")

    receipt_file_sha = _hash_exact_regular_file(PRESERVATION_RECEIPT)
    _require(
        receipt_file_sha == PRESERVATION_RECEIPT_FILE_SHA256,
        "preservation receipt file SHA-256 drift",
    )

    try:
        receipt = json.loads(PRESERVATION_RECEIPT.read_text(encoding="utf-8"))
    except Exception as error:
        raise V2R13Pair03BaselineRetryInvocationHold(
            f"preservation receipt JSON invalid: {error}"
        ) from error

    _require(isinstance(receipt, dict), "preservation receipt must be object")
    _require(receipt.get("pair_slot") == 3, "preservation pair-slot drift")
    _require(receipt.get("arm") == "baseline", "preservation arm drift")
    _require(receipt.get("forensics_sha256") == FORENSICS_SHA256, "forensics SHA drift")
    _require(
        receipt.get("preservation_receipt_sha256") == PRESERVATION_RECEIPT_SHA256,
        "preservation semantic receipt SHA drift",
    )
    _require(receipt.get("atomic_rename_performed") is True, "atomic preservation missing")
    _require(
        receipt.get("source_path_absent_after_preservation") is True,
        "canonical source path not recorded absent",
    )
    _require(
        receipt.get("archive_path_present_after_preservation") is True,
        "archive not recorded present",
    )
    _require(receipt.get("archived_tree_unchanged") is True, "archive tree changed")
    _require(receipt.get("failed_attempt_deleted") is False, "failed attempt marked deleted")
    _require(receipt.get("runtime_retry_performed") is False, "retry already performed")
    _require(receipt.get("runtime_retry_authorized") is False, "preservation itself authorized retry")

    warm = ARCHIVE_ROOT / WARM_REL
    _require(warm.is_file(), "preserved warm-start missing")
    _require(not warm.is_symlink(), "preserved warm-start symlinked")
    warm_sha = _hash_exact_regular_file(warm, WARM_START_BYTES)
    _require(warm_sha == WARM_START_SHA256, "preserved warm-start SHA drift")

    return {
        "preservation_receipt_file_sha256": receipt_file_sha,
        "preservation_receipt_sha256": receipt["preservation_receipt_sha256"],
        "warm_start_sha256": warm_sha,
    }


def execute_pair03_baseline_retry(*, confirm: str) -> dict[str, Any]:
    _require(confirm == CONFIRM_TOKEN, "PAIR03_BASELINE_RETRY_CONFIRMATION_REQUIRED")
    dependencies = _validate_dependencies()
    preserved = _validate_preservation_on_host()

    invocation = first_baseline.execute_first_baseline(
        confirm=first_baseline.CONFIRM_TOKEN,
    )

    _require(invocation.get("pair_slot") == 3, "retry invocation pair-slot drift")
    _require(invocation.get("arm") == "baseline", "retry invocation arm drift")
    _require(invocation.get("held_out") is False, "retry unexpectedly held-out")
    _require(
        invocation.get("runtime_execution_performed") is True,
        "retry runtime execution not completed",
    )
    _require(
        invocation.get("fresh_runtime_readiness_admitted") is True,
        "retry fresh readiness not admitted",
    )
    _require(
        invocation.get("runtime_cleanup_completed") is True,
        "retry runtime cleanup incomplete",
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
        _require(invocation.get(field) is False, f"retry boundary crossed: {field}")

    body = {
        "schema": RECEIPT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "retry_index": RETRY_INDEX,
        "max_retry_executions": MAX_RETRY_EXECUTIONS,
        "retry_authorization_consumed": True,
        "retry_execution_performed": True,
        "remaining_retry_executions": 0,
        "automatic_retry": False,
        "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "preserved_warm_start_sha256": WARM_START_SHA256,
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
        "retry_invocation_receipt_sha256": _digest(body),
        "preservation_host_recheck": preserved,
        "underlying_invocation": invocation,
        "dependencies": dependencies,
    }


def v2r13_pair03_baseline_retry_invocation_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "retry_index": RETRY_INDEX,
        "max_retry_executions": MAX_RETRY_EXECUTIONS,
        "confirm_token": CONFIRM_TOKEN,
        "preservation_receipt_sha256": PRESERVATION_RECEIPT_SHA256,
        "preservation_receipt_file_sha256": PRESERVATION_RECEIPT_FILE_SHA256,
        "preserved_warm_start_sha256": WARM_START_SHA256,
        "live_preservation_recheck_required": True,
        "repaired_first_baseline_executor_reused": True,
        "retry_execution_authorized": True,
        "retry_execution_performed_by_contract_inspection": False,
        "remaining_retry_executions_before_invocation": 1,
        "automatic_retry": False,
        "candidate_arm_implemented_by_this_source": False,
        "held_out_arm_implemented_by_this_source": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "next_change_class": (
            "source_only_v2r13_pair03_baseline_retry_invocation_source_binding_review"
        ),
        "dependencies": dependencies,
    }
