"""Exact-blob review of the Pair-06 V9 input-order authorization acceptance.

Pins the audit-only acceptance source and focused regression suite. The review
confirms that the fresh user authorization is bound by digest/length to the
exact reviewed request and to canonical main at authorization time.

The record itself performs no GPU observation, attempt claim, strict-contact
policy activation, order-coherence activation, model load, inference, game
execution, replay, training, promotion, deployment, VOID-chain mutation,
wallet/funds action, or scheduler mutation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_execution_authorization_acceptance_generation2
    as acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "execution-authorization-acceptance-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "b30533b6f3855845e24eeabc1729e8113358cdbb"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_GIT_BLOB = "f3d978c18f8793f6a91fdb0ec507d2a17ed5852f"

ACCEPTANCE_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_TEST_GIT_BLOB = "807a766540fa2a4dd6966ab3b17fdbeca49d7447"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "authorized_execution_launcher"
)


class Pair06V9InputOrderCoherenceAuthorizationAcceptanceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceAuthorizationAcceptanceReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = acceptance.pair06_v9_input_order_execution_authorization_acceptance_contract()

    _require(
        out.get("authorization_record_kind") == "explicit_user_authorization"
        and out.get("authorization_accepted") is True
        and out.get("execution_authorization_accepted") is True
        and out.get("policy_activation_authorization_accepted") is True
        and out.get("order_coherence_activation_authorization_accepted")
        is True,
        "V9 input-order authorization acceptance missing",
    )
    _require(
        out.get("authorized_main_head")
        == "b30533b6f3855845e24eeabc1729e8113358cdbb"
        and out.get("authorized_main_tree")
        == "d78ade6ea0a8a53634417eea424ebb0a3b1e03a5"
        and out.get("canonical_main_bound_at_authorization_time") is True,
        "V9 input-order authorized main binding drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "ad1edd0797e2ec6d95d0a4346a09d1a6d02e7f47ba32029cd6d80ec48c532af3"
        and out.get("authorization_text_bytes") == 13,
        "V9 input-order authorization text binding drift",
    )
    _require(
        out.get("request_review_git_blob")
        == "19afaae0a30ddebb22e37ba7b5004d370fb97517"
        and out.get("request_source_git_blob")
        == "1110cd7fc41f390f579e2207ac2fc9d0bfa4adcf"
        and out.get("request_test_git_blob")
        == "e03d008ff79f2428994b4f877a3c0477868be632"
        and out.get("request_review_test_git_blob")
        == "4788c6068b35bc2a71020d58ea03c424c431de85",
        "V9 input-order reviewed request source binding drift",
    )
    _require(
        out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-repair-v1"
        and out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("held_out") is False
        and out.get("doctrine") == "FEINTER"
        and out.get("seed") == 208354846
        and out.get("rounds") == 36
        and out.get("ticks_per_round") == 25
        and out.get("starter_infantry") == 4
        and out.get("staging_max_ticks") == 800
        and out.get("runtime_selection_key")
        == "apollyon-v3-qwen35-4b-lora-v1",
        "V9 input-order accepted scope drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("automatic_retry") is False,
        "V9 input-order accepted attempt cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True
        and out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 input-order accepted GPU policy drift",
    )
    for field in (
        "gpu_admission_failure_must_not_create_attempt_marker",
        "gpu_admission_failure_must_not_activate_policy",
        "gpu_admission_failure_must_not_activate_order_coherence",
        "gpu_admission_failure_must_not_load_model",
        "gpu_admission_failure_must_not_execute_inference",
        "gpu_admission_failure_must_not_execute_game",
        "fresh_order_evidence_namespace_required",
        "receipt_bound_preclaim_gpu_execution_authorized",
        "v9_policy_activation_authorized",
        "v9_order_coherence_activation_authorized",
        "attempt_marker_creation_authorized_after_fresh_gpu_admission",
        "policy_activation_authorized_after_fresh_gpu_admission",
        "order_coherence_activation_authorized_after_fresh_gpu_admission",
        "runtime_load_authorized_after_fresh_gpu_admission",
        "model_inference_authorized_after_fresh_gpu_admission",
        "game_execution_authorized_after_fresh_gpu_admission",
    ):
        _require(
            out.get(field) is True,
            "V9 input-order acceptance invariant drift: " + field,
        )
    _require(
        out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False
        and out.get("historical_v9_attempt_reusable") is False
        and out.get("historical_v9_authorization_reusable") is False
        and out.get("controlled_comparison_causal_claim_made") is False,
        "V9 input-order predecessor/comparison boundary drift",
    )
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "attempt_marker_created_by_this_record",
        "gpu_observation_performed_by_this_record",
        "policy_activation_performed_by_this_record",
        "order_coherence_activation_performed_by_this_record",
        "runtime_load_performed_by_this_record",
        "model_inference_performed_by_this_record",
        "game_execution_performed_by_this_record",
    ):
        _require(
            out.get(field) is False,
            "V9 input-order acceptance effect boundary drift: " + field,
        )
    _require(
        out.get("execution_authorization_reusable_after_attempt_claim") is False
        and out.get(
            "policy_activation_authorization_reusable_after_attempt_claim"
        )
        is False
        and out.get(
            "order_coherence_activation_authorization_reusable_after_attempt_claim"
        )
        is False,
        "V9 input-order authorization reuse boundary drift",
    )
    _require(
        out.get("next_gate") == NEXT_GATE,
        "V9 input-order acceptance next gate drift",
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


def pair06_v9_input_order_execution_authorization_acceptance_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "acceptance_path": ACCEPTANCE_PATH,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_test_path": ACCEPTANCE_TEST_PATH,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "pair06_v9_input_order_execution_authorization_acceptance_reviewed": True,
        "authorization_text_sha256": validated["authorization_text_sha256"],
        "authorization_text_bytes": validated["authorization_text_bytes"],
        "authorized_request_sha256": validated["authorized_request_sha256"],
        "authorized_request_bytes": validated["authorized_request_bytes"],
        "authorized_main_head": validated["authorized_main_head"],
        "authorized_main_tree": validated["authorized_main_tree"],
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_order_evidence_namespace_required": True,
        "receipt_bound_preclaim_gpu_execution_authorized": True,
        "v9_policy_activation_authorized": True,
        "v9_order_coherence_activation_authorized": True,
        "execution_authorization_reusable_after_attempt_claim": False,
        "policy_activation_authorization_reusable_after_attempt_claim": False,
        "order_coherence_activation_authorization_reusable_after_attempt_claim": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_acceptance": validated,
        "source_frontier_closed": True,
        "execution_blockers": (
            "reviewed_authorized_execution_launcher",
            "explicit_launcher_confirmation",
            "exact_current_main_and_canonical_blobs",
            "fresh_preclaim_gpu_admission",
            "fresh_create_only_order_coherence_attempt_marker",
        ),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceAuthorizationAcceptanceReviewHold(
        NEXT_GATE
    )
