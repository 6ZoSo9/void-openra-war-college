"""Exact-blob source review of the pair-06 V9 operator entrypoint.

Pins the one-shot V9 operator source and focused regression suite. The review
confirms that V9 uses a fresh evidence namespace, preserves the reviewed
preclaim-GPU and no-offload ordering, carries the successful V8 V2 lineage only
as spent/non-reusable history, and remains inert by contract inspection.

No execution request is created here. No authorization, attempt claim, attempt,
runtime activation, execution, replay, training, promotion, deployment, chain,
wallet, transaction, funds, or scheduler authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_operator_entrypoint_generation2
    as operator,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-operator-entrypoint-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "a016b2c0111b431e825a61417e6570654d570d96"
OPERATOR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_operator_entrypoint_generation2.py"
)
OPERATOR_GIT_BLOB = "d2e097bfd5b3afb7cd7e0581c2496777c89d43de"
OPERATOR_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_operator_entrypoint_generation2.py"
)
OPERATOR_TEST_GIT_BLOB = "0e08b2ebb8c3c66fe3676513073e016304c166d2"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_execution_authorization_request"
)


class Pair06V9StrictVisibleContactOperatorReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactOperatorReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = operator.pair06_v9_strict_visible_contact_operator_contract()

    _require(
        out.get(
            "pair06_v9_strict_visible_contact_operator_entrypoint_implemented"
        )
        is True,
        "V9 operator entrypoint missing",
    )
    _require(
        out.get(
            "pair06_v9_strict_visible_contact_operator_entrypoint_reviewed"
        )
        is False,
        "V9 operator unexpectedly self-reviewed",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 operator scope drift",
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
        "explicit_execution_authorization_boolean_required",
        "explicit_policy_activation_authorization_boolean_required",
        "explicit_execution_confirmation_token_required",
        "explicit_policy_confirmation_token_required",
        "execution_and_policy_confirmation_tokens_distinct",
    ):
        _require(
            out.get(field) is True,
            "V9 operator invariant drift: " + field,
        )

    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 GPU free-memory threshold drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V9 operator attempt cardinality drift",
    )
    _require(
        out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False,
        "V8 predecessor lineage unexpectedly reusable",
    )

    for field in (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
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
            "V9 operator authority drift: " + field,
        )

    deps = out.get("dependencies")
    _require(isinstance(deps, dict), "V9 operator dependencies missing")
    prior = deps.get("prior_v8_v2_success_review")
    _require(isinstance(prior, dict), "V8 predecessor review missing")
    _require(
        prior.get("attempt_consumed") is True
        and prior.get("attempt_reusable") is False
        and prior.get("authorization_reusable") is False
        and prior.get("lineage_closed") is True,
        "V8 predecessor success-lineage boundary drift",
    )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_OPERATOR_ENTRYPOINT_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 operator review frontier drift",
    )

    return deepcopy(out)


def pair06_v9_strict_visible_contact_operator_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "operator_path": OPERATOR_PATH,
        "operator_git_blob": OPERATOR_GIT_BLOB,
        "operator_test_path": OPERATOR_TEST_PATH,
        "operator_test_git_blob": OPERATOR_TEST_GIT_BLOB,
        "pair06_v9_strict_visible_contact_operator_entrypoint_reviewed": True,
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
        "fresh_v9_evidence_namespace_required": True,
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "dual_explicit_authorizations_required": True,
        "dual_distinct_confirmation_tokens_required": True,
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
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
    raise Pair06V9StrictVisibleContactOperatorReviewHold(NEXT_GATE)
