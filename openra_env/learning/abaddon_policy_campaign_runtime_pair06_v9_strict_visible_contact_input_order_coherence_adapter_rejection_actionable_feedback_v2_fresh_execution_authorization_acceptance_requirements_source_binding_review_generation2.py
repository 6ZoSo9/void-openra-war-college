"""Exact-blob review of actionable-feedback V2 acceptance requirements.

Pins the source-only requirements contract and focused tests. The review proves
that the later acceptance must bind exact request bytes, exact user
authorization text, canonical main at authorization time, and all five
authorization gates.

No authorization is accepted here. The source frontier closes at explicit user
authorization.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_acceptance_requirements_generation2
    as requirements,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "fresh-execution-authorization-acceptance-requirements-review.v1"
)

ACCEPTED_BASE_HEAD = "2554f51d6a658488c83bd7aa886a4984402f8a95"

REQUIREMENTS_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_execution_authorization_"
    "acceptance_requirements_generation2.py"
)
REQUIREMENTS_GIT_BLOB = "873dafa7c43acfa185bbf18618f4df84976f2ea8"

REQUIREMENTS_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_execution_authorization_"
    "acceptance_requirements_generation2.py"
)
REQUIREMENTS_TEST_GIT_BLOB = "fd1d84095ef3f96e71fe7b4fad6f566b8092068b"

REQUEST_REVIEW_GIT_BLOB = "5b550b6378e54d8b8b8efe581f34eb7df0a05ceb"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_EXECUTION_"
    "EXPLICIT_USER_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_acceptance"
)


class Pair06V9ActionableFeedbackV2FreshExecutionAcceptanceRequirementsReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2FreshExecutionAcceptanceRequirementsReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        requirements
        .pair06_v9_actionable_feedback_v2_fresh_execution_acceptance_requirements_contract()
    )

    _require(
        out.get("acceptance_requirements_implemented") is True,
        "actionable-feedback V2 acceptance requirements missing",
    )
    _require(
        out.get("request_review_git_blob") == REQUEST_REVIEW_GIT_BLOB,
        "actionable-feedback V2 request review binding drift",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("policy_id") == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2",
        "actionable-feedback V2 acceptance requirement scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("fresh_actionable_feedback_v2_evidence_namespace_required")
        is True,
        "actionable-feedback V2 acceptance runtime/lineage drift",
    )

    for field in (
        "exact_user_authorization_text_required",
        "authorization_text_sha256_binding_required",
        "authorization_text_byte_length_binding_required",
        "canonical_main_head_binding_required",
        "canonical_main_tree_binding_required",
        "canonical_main_must_be_bound_at_authorization_time",
        "authorization_must_reference_exact_reviewed_request",
        "authorization_must_explicitly_cover_execution",
        "authorization_must_explicitly_cover_policy_activation",
        "authorization_must_explicitly_cover_order_coherence_activation",
        "authorization_must_explicitly_cover_repair_activation",
        "authorization_must_explicitly_cover_actionable_feedback_v2_activation",
        "five_distinct_confirmation_tokens_required",
    ):
        _require(
            out.get(field) is True,
            "actionable-feedback V2 acceptance binding drift: " + field,
        )

    _require(
        out.get("general_source_work_authorization_is_execution_authorization")
        is False
        and out.get("prior_authorization_text_reusable") is False
        and out.get("preservation_authorization_reusable_as_execution_authority")
        is False
        and out.get("matching_request_digest_grants_authority") is False
        and out.get("matching_request_bytes_grant_authority") is False,
        "actionable-feedback V2 acceptance authority-reuse drift",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "attempt_created",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
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
            "actionable-feedback V2 acceptance requirements self-authorized: "
            + field,
        )

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate") == NEXT_GATE,
        "actionable-feedback V2 acceptance requirements frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (REQUIREMENTS_PATH, REQUIREMENTS_GIT_BLOB),
        (REQUIREMENTS_TEST_PATH, REQUIREMENTS_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_fresh_execution_acceptance_requirements_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "requirements_path": REQUIREMENTS_PATH,
        "requirements_git_blob": REQUIREMENTS_GIT_BLOB,
        "requirements_test_path": REQUIREMENTS_TEST_PATH,
        "requirements_test_git_blob": REQUIREMENTS_TEST_GIT_BLOB,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_fresh_execution_acceptance_requirements_reviewed": True,
        "reviewed_request_sha256": validated["reviewed_request_sha256"],
        "reviewed_request_bytes": validated["reviewed_request_bytes"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "prior_attempt_marker_sha256": validated["prior_attempt_marker_sha256"],
        "preservation_receipt_sha256": validated["preservation_receipt_sha256"],
        "fresh_actionable_feedback_v2_evidence_namespace_required": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "exact_user_authorization_text_required": True,
        "authorization_text_sha256_binding_required": True,
        "authorization_text_byte_length_binding_required": True,
        "canonical_main_head_binding_required": True,
        "canonical_main_tree_binding_required": True,
        "canonical_main_must_be_bound_at_authorization_time": True,
        "authorization_must_reference_exact_reviewed_request": True,
        "authorization_must_explicitly_cover_execution": True,
        "authorization_must_explicitly_cover_policy_activation": True,
        "authorization_must_explicitly_cover_order_coherence_activation": True,
        "authorization_must_explicitly_cover_repair_activation": True,
        "authorization_must_explicitly_cover_actionable_feedback_v2_activation": True,
        "five_distinct_confirmation_tokens_required": True,
        "general_source_work_authorization_is_execution_authorization": False,
        "prior_authorization_text_reusable": False,
        "preservation_authorization_reusable_as_execution_authority": False,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "repair_activation_authorization_accepted": False,
        "actionable_feedback_v2_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_requirements": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def accept_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2FreshExecutionAcceptanceRequirementsReviewHold(
        NEXT_GATE
    )
