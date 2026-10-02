"""Exact-blob review of the consumed Pair-06 V9 failed-attempt preservation gate.

Pins the preservation source and focused tests. The review confirms exact
binding to the consumed marker and observed run artifacts, exact clean detached
worktree requirements, non-force worktree removal, atomic archive rename,
inode-preserving evidence retention, and a create-only preservation receipt.

No preservation is performed by review. No runtime retry or execution request
is opened, and no runtime, training, deployment, chain, wallet/funds, or
scheduler authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_preservation_generation2
    as preservation,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "preservation-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "ce94ace8f914b505ff74bfc9f7d769aed785c6de"

PRESERVATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_generation2.py"
)
PRESERVATION_GIT_BLOB = "342118e0e9edbba7472820ae99ff4c05203143d0"

PRESERVATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_preservation_generation2.py"
)
PRESERVATION_TEST_GIT_BLOB = "b3dbf0d648e53f35865ee909d5462090eb96b9b3"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_preservation_authorization_request"
)


class Pair06V9AdapterRejectionFailedAttemptPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionFailedAttemptPreservationReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        preservation
        .pair06_v9_input_order_adapter_rejection_failed_attempt_preservation_contract()
    )

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "failed-attempt preservation scope drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d",
        "failed-attempt marker identity drift",
    )
    _require(
        out.get("warm_start_sha256")
        == "9ad33940dcc8199a61b6fa8bb5fb68f2eb8cc846fb745cf7e64c27e6e053b0e1"
        and out.get("warm_start_bytes") == 229255,
        "failed-attempt warm-start identity drift",
    )
    _require(
        out.get("trajectory_sha256")
        == "4aaa1e944a2004b87c420d6a25d361bcd5316d992479d9a934cc1b10739b867a"
        and out.get("trajectory_bytes") == 58075,
        "failed-attempt trajectory identity drift",
    )

    for field in (
        "exact_consumed_marker_required",
        "exact_run_artifacts_required",
        "result_must_be_absent",
        "closeout_must_be_absent",
        "summary_must_be_absent",
        "exact_clean_detached_registered_worktrees_required",
        "non_force_worktree_removal_only",
        "engine_removed_before_source",
        "remaining_evidence_manifest_hashed",
        "atomic_baseline_archive_rename_implemented",
        "attempt_marker_inode_preserved",
        "run_artifact_inode_preserved",
        "create_only_preservation_receipt_implemented",
        "preservation_requires_explicit_authority",
        "preservation_confirmation_token_required",
    ):
        _require(
            out.get(field) is True,
            "failed-attempt preservation invariant drift: " + field,
        )

    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "new_execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ):
        _require(
            out.get(field) is False,
            "failed-attempt preservation authority drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (PRESERVATION_PATH, PRESERVATION_GIT_BLOB),
        (PRESERVATION_TEST_PATH, PRESERVATION_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_adapter_rejection_failed_attempt_preservation_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "preservation_path": PRESERVATION_PATH,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_test_path": PRESERVATION_TEST_PATH,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_failed_attempt_preservation_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "warm_start_sha256": validated["warm_start_sha256"],
        "warm_start_bytes": validated["warm_start_bytes"],
        "trajectory_sha256": validated["trajectory_sha256"],
        "trajectory_bytes": validated["trajectory_bytes"],
        "non_force_worktree_removal_only": True,
        "atomic_baseline_archive_rename_reviewed": True,
        "evidence_inode_preservation_reviewed": True,
        "create_only_preservation_receipt_reviewed": True,
        "preservation_authorization_accepted": False,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "new_execution_request_opened": False,
        "runtime_execution_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_preservation": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def request_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionFailedAttemptPreservationReviewHold(
        NEXT_GATE
    )
