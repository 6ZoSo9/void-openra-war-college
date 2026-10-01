"""Exact-blob review of the fresh-lineage Pair-06 V9 adapter-rejection operator.

Pins the fresh-lineage operator source and focused tests. The review confirms a
new evidence namespace, preserved fresh-preclaim CUDA:0 ordering, one-attempt
cardinality, four explicit authorization/confirmation gates, and permanent
non-reuse of the consumed input-order attempt marker.

The next gate is preservation of the consumed failed attempt before any
execution request may be opened. This review grants no execution request,
authorization, attempt claim, runtime activation, execution, replay, training,
deployment, chain, wallet/funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_lineage_operator_generation2
    as operator,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-adapter-rejection-"
    "fresh-lineage-operator-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "1f6bca6a4dd346f9eda4d36a71157ecb300d2c86"

OPERATOR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_lineage_operator_generation2.py"
)
OPERATOR_GIT_BLOB = "263b1039f9a75d729e4a249af62fe3712755edc8"

OPERATOR_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_lineage_operator_generation2.py"
)
OPERATOR_TEST_GIT_BLOB = "1f5324cbbcbd1a660b24abf7cc77ffcabe8ef5b4"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_failed_attempt_preservation"
)


class Pair06V9InputOrderAdapterRejectionFreshLineageOperatorReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionFreshLineageOperatorReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        operator
        .pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_contract()
    )

    _require(
        out.get(
            "pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_implemented"
        )
        is True,
        "fresh-lineage adapter-rejection operator missing",
    )
    _require(
        out.get(
            "pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_reviewed"
        )
        is False,
        "fresh-lineage operator unexpectedly self-reviewed",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "fresh-lineage operator scope drift",
    )

    for field in (
        "exact_v8_python_required",
        "exact_current_main_required",
        "exact_operator_source_sha256_required",
        "fresh_v8_environment_and_assets_required",
        "reviewed_base_preclaim_gpu_helpers_reused",
        "reviewed_worktree_materializer_reused",
        "preclaim_worktree_materialization_implemented",
        "preclaim_materialization_cleanup_on_hold_implemented",
        "fresh_preclaim_gpu_observation_implemented",
        "fresh_preclaim_gpu_admission_required",
        "fresh_preclaim_gpu_observation_precedes_attempt_marker",
        "zero_foreign_cuda0_compute_processes_required",
        "durable_create_only_attempt_marker_implemented",
        "attempt_marker_precedes_model_load_and_child_spawn",
        "marker_sha256_is_attempt_id",
        "authority_rechecked_after_claim",
        "authority_rechecked_before_each_inference_by_parent",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
        "adapter_rejection_evidence_namespace_distinct_from_consumed_input_order",
        "explicit_execution_authorization_boolean_required",
        "explicit_policy_activation_authorization_boolean_required",
        "explicit_order_coherence_activation_authorization_boolean_required",
        "explicit_repair_activation_authorization_boolean_required",
        "explicit_execution_confirmation_token_required",
        "explicit_policy_confirmation_token_required",
        "explicit_order_coherence_confirmation_token_required",
        "explicit_repair_confirmation_token_required",
        "all_confirmation_tokens_distinct",
        "prior_failed_attempt_preservation_required_before_execution_request",
    ):
        _require(
            out.get(field) is True,
            "fresh-lineage operator invariant drift: " + field,
        )

    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "fresh-lineage attempt cardinality drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "fresh-lineage GPU threshold drift",
    )
    _require(
        out.get("prior_input_order_attempt_marker_sha256")
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d",
        "consumed input-order marker binding drift",
    )
    _require(
        out.get("prior_input_order_attempt_reusable") is False
        and out.get("prior_input_order_authorization_reusable") is False,
        "consumed input-order lineage unexpectedly reusable",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "execution_request_created",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
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
            "fresh-lineage operator authority drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (OPERATOR_PATH, OPERATOR_GIT_BLOB),
        (OPERATOR_TEST_PATH, OPERATOR_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "operator_path": OPERATOR_PATH,
        "operator_git_blob": OPERATOR_GIT_BLOB,
        "operator_test_path": OPERATOR_TEST_PATH,
        "operator_test_git_blob": OPERATOR_TEST_GIT_BLOB,
        "pair06_v9_input_order_adapter_rejection_fresh_lineage_operator_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_adapter_rejection_evidence_namespace_required": True,
        "prior_input_order_attempt_marker_sha256": (
            "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
        ),
        "prior_input_order_attempt_reusable": False,
        "prior_input_order_authorization_reusable": False,
        "quadruple_explicit_authorizations_required": True,
        "quadruple_distinct_confirmation_tokens_required": True,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "repair_activation_authorization_accepted": False,
        "prior_failed_attempt_preservation_required_before_execution_request": True,
        "execution_request_created": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_operator": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve_or_request(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderAdapterRejectionFreshLineageOperatorReviewHold(
        NEXT_GATE
    )
