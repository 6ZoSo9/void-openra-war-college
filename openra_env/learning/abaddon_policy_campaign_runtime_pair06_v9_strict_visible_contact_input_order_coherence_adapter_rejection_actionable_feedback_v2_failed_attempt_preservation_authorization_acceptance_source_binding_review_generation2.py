"""Exact-blob review of the explicit actionable-feedback V2 preservation authorization acceptance.

Pins the accepted authorization contract and focused tests to exact Git blobs,
then revalidates the exact reviewed request, user authorization digest/length,
canonical main authorization-time head/tree, and exact preservation scope.

This review performs no preservation or host mutation. It grants no runtime
retry, new execution, model/game execution, training, deployment, chain,
wallet/funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_authorization_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-authorization-acceptance-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "000a8a01c29a8b42e91cb30f935ef63b72407f02"
ACCEPTED_BASE_TREE = "49b201ba723bcd4b8cab162f2d2d954534da6621"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_authorization_"
    "acceptance_generation2.py"
)
ACCEPTANCE_GIT_BLOB = "8dab754b5619ce28933675960174977fd4dee2f7"

ACCEPTANCE_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_failed_attempt_preservation_authorization_"
    "acceptance_generation2.py"
)
ACCEPTANCE_TEST_GIT_BLOB = "bcf13c6172556711add125d652038a078d214de2"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "authorized_host_only_pair06_v9_strict_visible_contact_input_order_"
    "coherence_adapter_rejection_actionable_feedback_v2_failed_attempt_"
    "preservation_execution"
)


class Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        acceptance
        .pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_contract()
    )

    _require(
        out.get("reviewed_request_sha256")
        == "61fc33cef6c122edfc4d0e2d177656a882e3d4ad64745f7aa70d588ce8e6c107"
        and out.get("reviewed_request_bytes") == 3288,
        "V2 accepted reviewed-request identity drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "d48d8dbd83d30e12ff54129510ea082a5c21e30cb7ea012a70ac479276b2ffb3"
        and out.get("authorization_text_bytes") == 186,
        "V2 accepted explicit authorization identity drift",
    )
    _require(
        out.get("canonical_main_head_at_authorization") == ACCEPTED_BASE_HEAD
        and out.get("canonical_main_tree_at_authorization") == ACCEPTED_BASE_TREE,
        "V2 authorization-time canonical main binding drift",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and out.get("attempt_marker_bytes") == 2208
        and out.get("archive_path")
        == (
            "/home/zoso/dev/void-war-college-execution/v8-generation2/"
            "generation2/pair-06/failed-attempts/"
            "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
        )
        and out.get("preservation_receipt_path")
        == (
            "/home/zoso/dev/void-war-college-execution/v8-generation2/"
            "generation2/pair-06/failed-attempts/"
            "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
            "-preservation-receipt.json"
        ),
        "V2 accepted preservation scope drift",
    )

    for field in (
        "preservation_authorization_accepted",
        "preservation_authorized",
        "filesystem_mutation_authorized",
        "git_worktree_mutation_authorized",
        "archive_rename_authorized",
        "preservation_receipt_creation_authorized",
        "authority_scope_exact_reviewed_preservation_only",
    ):
        _require(out.get(field) is True, "V2 preservation authority drift: " + field)

    for field in (
        "preservation_performed",
        "runtime_retry_authorized",
        "execution_request_opened",
        "runtime_load_authorized",
        "model_inference_authorized",
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
        _require(out.get(field) is False, "V2 non-preservation authority drift: " + field)

    _require(
        out.get("next_gate") == NEXT_GATE,
        "V2 preservation host execution frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (ACCEPTANCE_PATH, ACCEPTANCE_GIT_BLOB),
        (ACCEPTANCE_TEST_PATH, ACCEPTANCE_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "accepted_base_tree": ACCEPTED_BASE_TREE,
        "acceptance_path": ACCEPTANCE_PATH,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_test_path": ACCEPTANCE_TEST_PATH,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_preservation_authorization_acceptance_reviewed": True,
        "reviewed_request_sha256": validated["reviewed_request_sha256"],
        "reviewed_request_bytes": validated["reviewed_request_bytes"],
        "authorization_text_sha256": validated["authorization_text_sha256"],
        "authorization_text_bytes": validated["authorization_text_bytes"],
        "canonical_main_head_at_authorization": (
            validated["canonical_main_head_at_authorization"]
        ),
        "canonical_main_tree_at_authorization": (
            validated["canonical_main_tree_at_authorization"]
        ),
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "attempt_marker_bytes": validated["attempt_marker_bytes"],
        "archive_path": validated["archive_path"],
        "preservation_receipt_path": validated["preservation_receipt_path"],
        "preservation_authorization_accepted": True,
        "preservation_authorized": True,
        "authority_scope_exact_reviewed_preservation_only": True,
        "preservation_performed": False,
        "runtime_retry_authorized": False,
        "execution_request_opened": False,
        "runtime_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_acceptance": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PreservationAuthorizationAcceptanceReviewHold(
        NEXT_GATE
    )
