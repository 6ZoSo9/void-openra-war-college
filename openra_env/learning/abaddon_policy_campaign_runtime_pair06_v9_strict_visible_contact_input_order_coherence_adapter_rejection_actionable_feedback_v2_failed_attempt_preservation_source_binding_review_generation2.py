"""Exact-blob review of the consumed actionable-feedback V2 failed-attempt preservation gate.

Pins the preservation source and focused tests. The review confirms exact
binding to the consumed V2 marker and observed run artifacts, exact clean
detached worktree requirements, non-force worktree removal, atomic archive
rename, inode-preserving evidence retention, and a create-only preservation
receipt.

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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_generation2
    as preservation,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "63a5077ba247a974d2696c479972efdf4cd0f6e8"

PRESERVATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_generation2.py"
)
PRESERVATION_GIT_BLOB = "92981d23b580059fd3419cfe95daea561aab6add"

PRESERVATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_generation2.py"
)
PRESERVATION_TEST_GIT_BLOB = "7ce676057d894eb401ab72f502b7507b9827e181"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_authorization_request"
)


class Pair06V9ActionableFeedbackV2FailedAttemptPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2FailedAttemptPreservationReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        preservation
        .pair06_v9_actionable_feedback_v2_failed_attempt_preservation_contract()
    )

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "actionable-feedback V2 failed-attempt preservation scope drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and out.get("attempt_marker_bytes") == 2208,
        "actionable-feedback V2 failed-attempt marker identity drift",
    )
    _require(
        out.get("warm_start_sha256")
        == "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
        and out.get("warm_start_bytes") == 229255,
        "actionable-feedback V2 warm-start identity drift",
    )
    _require(
        out.get("trajectory_sha256")
        == "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
        and out.get("trajectory_bytes") == 58075,
        "actionable-feedback V2 trajectory identity drift",
    )
    _require(
        out.get("authorized_attempt_main_head")
        == "63a5077ba247a974d2696c479972efdf4cd0f6e8"
        and out.get("authorized_attempt_main_tree")
        == "e9a6bdf0423e739f97519515f62bd24ef65cf1a3"
        and out.get("operator_source_sha256")
        == "fcc662cbaaa482651004523b73deb906947a73b296356cc291bb9150dddfc179",
        "actionable-feedback V2 consumed-attempt source lineage drift",
    )
    _require(
        out.get("failure_class")
        == "strict_contact_actionable_feedback_v2_exhausted"
        and out.get("failure_round") == 6
        and out.get("maximum_decision_attempts") == 6,
        "actionable-feedback V2 terminal failure shape drift",
    )
    _require(
        out.get("terminal_feedback")
        == (
            "function_not_offered:"
            "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
            "not_json_array_or_bare_integer__"
        ),
        "actionable-feedback V2 terminal feedback drift",
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
            "actionable-feedback V2 preservation invariant drift: " + field,
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
            "actionable-feedback V2 preservation authority drift: " + field,
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


def pair06_v9_actionable_feedback_v2_failed_attempt_preservation_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "preservation_path": PRESERVATION_PATH,
        "preservation_git_blob": PRESERVATION_GIT_BLOB,
        "preservation_test_path": PRESERVATION_TEST_PATH,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_failed_attempt_preservation_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "attempt_marker_bytes": validated["attempt_marker_bytes"],
        "warm_start_sha256": validated["warm_start_sha256"],
        "warm_start_bytes": validated["warm_start_bytes"],
        "trajectory_sha256": validated["trajectory_sha256"],
        "trajectory_bytes": validated["trajectory_bytes"],
        "failure_class": validated["failure_class"],
        "failure_round": validated["failure_round"],
        "maximum_decision_attempts": validated["maximum_decision_attempts"],
        "terminal_feedback": validated["terminal_feedback"],
        "archive_name": validated["archive_name"],
        "archive_path": validated["archive_path"],
        "preservation_receipt_path": validated["preservation_receipt_path"],
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
    raise Pair06V9ActionableFeedbackV2FailedAttemptPreservationReviewHold(
        NEXT_GATE
    )
