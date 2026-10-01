"""Exact-blob review of the Pair-06 V9 input-order-coherence operator.

Pins the one-shot operator source and focused regression suite. The review
confirms a fresh evidence namespace, preserved preclaim-GPU/no-offload ordering,
three explicit authorization/confirmation gates, non-reuse of the consumed
historical V9 lane, and inert contract inspection.

No execution request is created here. No authorization, attempt claim, attempt,
runtime activation, execution, replay, training, promotion, deployment, chain,
wallet/funds, or scheduler authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_operator_entrypoint_generation2
    as operator,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "operator-entrypoint-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "51a6ba125db8d3c7c5209aa4b37062389ea8b979"

OPERATOR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_generation2.py"
)
OPERATOR_GIT_BLOB = "2a1e9d04b0a877ad4afb4f99f831b7824c5fb59a"

OPERATOR_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_generation2.py"
)
OPERATOR_TEST_GIT_BLOB = "eb46654b9f96895c7ef553c5fe13d59e21f5b3cb"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "execution_authorization_request"
)


class Pair06V9InputOrderCoherenceOperatorReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceOperatorReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = operator.pair06_v9_input_order_coherence_operator_contract()

    _require(
        out.get(
            "pair06_v9_input_order_coherence_operator_entrypoint_implemented"
        )
        is True,
        "V9 input-order operator entrypoint missing",
    )
    _require(
        out.get(
            "pair06_v9_input_order_coherence_operator_entrypoint_reviewed"
        )
        is False,
        "V9 input-order operator unexpectedly self-reviewed",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 input-order operator scope drift",
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
        "no_offload_parent_receipt_schema_required",
        "inference_safe_placement_receipt_required",
        "durable_execution_result_before_cleanup_implemented",
        "success_only_worktree_cleanup_implemented",
        "durable_cleanup_closeout_implemented",
        "runs_preserved_after_success",
        "v9_evidence_namespace_distinct_from_v8",
        "order_evidence_namespace_distinct_from_historical_v9",
        "explicit_execution_authorization_boolean_required",
        "explicit_policy_activation_authorization_boolean_required",
        "explicit_order_coherence_activation_authorization_boolean_required",
        "explicit_execution_confirmation_token_required",
        "explicit_policy_confirmation_token_required",
        "explicit_order_coherence_confirmation_token_required",
        "all_confirmation_tokens_distinct",
    ):
        _require(
            out.get(field) is True,
            "V9 input-order operator invariant drift: " + field,
        )

    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 input-order GPU threshold drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V9 input-order attempt cardinality drift",
    )
    _require(
        out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False
        and out.get("historical_v9_attempt_reusable") is False
        and out.get("historical_v9_authorization_reusable") is False,
        "predecessor execution lineage unexpectedly reusable",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
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
            "V9 input-order operator authority drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "OPERATOR_ENTRYPOINT_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 input-order operator review frontier drift",
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


def pair06_v9_input_order_coherence_operator_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "operator_path": OPERATOR_PATH,
        "operator_git_blob": OPERATOR_GIT_BLOB,
        "operator_test_path": OPERATOR_TEST_PATH,
        "operator_test_git_blob": OPERATOR_TEST_GIT_BLOB,
        "pair06_v9_input_order_coherence_operator_entrypoint_reviewed": True,
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
        "fresh_order_evidence_namespace_required": True,
        "historical_v9_attempt_reusable": False,
        "historical_v9_authorization_reusable": False,
        "triple_explicit_authorizations_required": True,
        "triple_distinct_confirmation_tokens_required": True,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "execution_request_created": False,
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


def request_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceOperatorReviewHold(NEXT_GATE)
