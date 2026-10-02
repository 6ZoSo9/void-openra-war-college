"""Exact-blob review of fresh adapter-rejection execution authorization.

Pins the audit-only acceptance source and focused tests. The review confirms
the exact user authorization text digest/length, canonical main snapshot at
authorization time, exact reviewed request identity, and explicit acceptance
of all four fresh authorization gates.

The acceptance record itself performs no GPU observation, attempt claim,
model load, inference, game execution, training, deployment, chain,
wallet/funds, or scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-fresh-execution-"
    "authorization-acceptance-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "e61d66b64eccc4f52a6a951e68a3df7cdf75ce0b"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_GIT_BLOB = "75c6557a534123e5ac332682356a76dd7c7c58c6"

ACCEPTANCE_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_TEST_GIT_BLOB = "2f0852e84b493adc3988c84ca10b983df5efc3be"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_authorized_execution_launcher"
)


class Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        acceptance
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_contract()
    )

    _require(
        out.get("authorization_record_kind") == "explicit_user_authorization"
        and out.get("authorization_accepted") is True
        and out.get("execution_authorization_accepted") is True
        and out.get("policy_activation_authorization_accepted") is True
        and out.get("order_coherence_activation_authorization_accepted") is True
        and out.get("repair_activation_authorization_accepted") is True,
        "fresh execution authorization acceptance missing",
    )
    _require(
        out.get("authorization_text_sha256")
        == "2364e9c7c7e9e11d9dcdacbe68722b202eb0d5790b5d54cac6b92a995fcb94e8"
        and out.get("authorization_text_bytes") == 286,
        "fresh execution authorization text binding drift",
    )
    _require(
        out.get("authorized_main_head")
        == "e61d66b64eccc4f52a6a951e68a3df7cdf75ce0b"
        and out.get("authorized_main_tree")
        == "27f5520c3a4018a66d6cf180f80d35ef655647fe"
        and out.get("canonical_main_bound_at_authorization_time") is True,
        "fresh execution authorization main binding drift",
    )
    _require(
        out.get("fresh_adapter_rejection_evidence_namespace_required") is True
        and out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("automatic_retry") is False,
        "fresh execution authorization cardinality/namespace drift",
    )

    for field in (
        "attempt_marker_creation_authorized_after_fresh_gpu_admission",
        "policy_activation_authorized_after_fresh_gpu_admission",
        "order_coherence_activation_authorized_after_fresh_gpu_admission",
        "repair_activation_authorized_after_fresh_gpu_admission",
        "runtime_load_authorized_after_fresh_gpu_admission",
        "model_inference_authorized_after_fresh_gpu_admission",
        "game_execution_authorized_after_fresh_gpu_admission",
        "gpu_admission_failure_must_not_create_attempt_marker",
        "gpu_admission_failure_must_not_activate_policy",
        "gpu_admission_failure_must_not_activate_order_coherence",
        "gpu_admission_failure_must_not_activate_repair",
        "gpu_admission_failure_must_not_load_model",
        "gpu_admission_failure_must_not_execute_inference",
        "gpu_admission_failure_must_not_execute_game",
    ):
        _require(
            out.get(field) is True,
            "fresh execution authorization GPU gate drift: " + field,
        )

    for field in (
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "order_coherence_activation_performed_by_this_record",
        "repair_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "execution_authorization_reusable_after_attempt_claim",
        "policy_activation_authorization_reusable_after_attempt_claim",
        "order_coherence_activation_authorization_reusable_after_attempt_claim",
        "repair_activation_authorization_reusable_after_attempt_claim",
    ):
        _require(
            out.get(field) is False,
            "fresh execution authorization effect/reuse drift: " + field,
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


def pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "acceptance_path": ACCEPTANCE_PATH,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_test_path": ACCEPTANCE_TEST_PATH,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_reviewed": True,
        "authorization_text_sha256": validated["authorization_text_sha256"],
        "authorization_text_bytes": validated["authorization_text_bytes"],
        "authorized_request_sha256": validated["authorized_request_sha256"],
        "authorized_request_bytes": validated["authorized_request_bytes"],
        "authorized_main_head": validated["authorized_main_head"],
        "authorized_main_tree": validated["authorized_main_tree"],
        "pair_slot": validated["pair_slot"],
        "arm": validated["arm"],
        "held_out": validated["held_out"],
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "prior_attempt_marker_sha256": (
            validated["prior_attempt_marker_sha256"]
        ),
        "preservation_receipt_sha256": (
            validated["preservation_receipt_sha256"]
        ),
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_adapter_rejection_evidence_namespace_required": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "automatic_retry": False,
        "attempt_marker_created_by_this_record": False,
        "runtime_load_performed_by_this_record": False,
        "model_inference_performed_by_this_record": False,
        "game_execution_performed_by_this_record": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
        "order_coherence_activation_authorization_reusable_after_attempt_claim": False,
        "repair_activation_authorization_reusable_after_attempt_claim": False,
        "validated_acceptance": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionFreshExecutionAuthorizationAcceptanceReviewHold(
        NEXT_GATE
    )
