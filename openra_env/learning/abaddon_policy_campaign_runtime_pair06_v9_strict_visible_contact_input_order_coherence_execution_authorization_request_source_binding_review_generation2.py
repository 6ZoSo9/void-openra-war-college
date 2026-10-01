"""Exact-blob review of the fresh Pair-06 V9 input-order authorization request.

Pins the proposal-only request source and regression suite. The review confirms
matched Pair-06 baseline scope, non-reusable predecessor lineages, fresh CUDA:0
preclaim admission, the fresh order-coherence evidence namespace, and three
fresh authorization lanes.

A matching request digest is not authorization. General source-work
authorization is not execution authorization. This review performs no host I/O
and grants no attempt claim, policy activation, order-coherence activation,
runtime, execution, replay, training, promotion, deployment, chain,
wallet/funds, or scheduler authority.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_execution_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "execution-authorization-request-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "23dabde76ef494e741294bf7c4ed210af5ce45a9"

REQUEST_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_request_generation2.py"
)
REQUEST_GIT_BLOB = "1110cd7fc41f390f579e2207ac2fc9d0bfa4adcf"

REQUEST_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_request_generation2.py"
)
REQUEST_TEST_GIT_BLOB = "e03d008ff79f2428994b4f877a3c0477868be632"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "audit_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "execution_authorization_acceptance"
)


class Pair06V9InputOrderCoherenceRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceRequestReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.pair06_v9_input_order_execution_authorization_request_contract()

    _require(
        out.get(
            "pair06_v9_input_order_execution_authorization_request_implemented"
        )
        is True,
        "V9 input-order execution request missing",
    )
    _require(
        out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-repair-v1",
        "V9 input-order request identity drift",
    )
    _require(
        out.get("pair_slot") == 6
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
        "V9 input-order controlled scope drift",
    )
    _require(
        out.get("reviewed_operator_stack_head")
        == "23dabde76ef494e741294bf7c4ed210af5ce45a9"
        and out.get("canonical_main_must_be_bound_by_later_authorization")
        is True,
        "V9 input-order stack/main binding drift",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V9 input-order attempt cardinality drift",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get("fresh_preclaim_gpu_observation_precedes_attempt_marker")
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "V9 input-order GPU admission policy drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 input-order GPU threshold drift",
    )
    _require(
        out.get("fresh_order_evidence_namespace_required") is True
        and out.get("prior_v8_v2_attempt_reusable") is False
        and out.get("prior_v8_v2_authorization_reusable") is False
        and out.get("historical_v9_attempt_reusable") is False
        and out.get("historical_v9_authorization_reusable") is False,
        "V9 input-order lineage/evidence boundary drift",
    )
    _require(
        out.get("controlled_comparison_causal_claim_made") is False,
        "V9 input-order request unexpectedly makes causal claim",
    )
    _require(
        out.get("fresh_execution_authorization_required") is True
        and out.get("fresh_policy_activation_authorization_required") is True
        and out.get(
            "fresh_order_coherence_activation_authorization_required"
        )
        is True
        and out.get("fresh_user_authorization_text_required") is True,
        "V9 input-order fresh authorization boundary drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False
        and out.get("request_digest_reusable_as_authorization") is False
        and out.get(
            "general_source_work_authorization_is_execution_authorization"
        )
        is False,
        "V9 input-order request authorization semantics drift",
    )

    for field in request.FALSE_AUTHORITY_FIELDS + (
        "host_io_performed_by_contract_inspection",
    ):
        _require(
            out.get(field) is False,
            "V9 input-order request authority drift: " + field,
        )

    proposal = out.get("request")
    _require(isinstance(proposal, dict), "V9 input-order request record missing")
    binding = proposal.get("source_binding")
    _require(isinstance(binding, dict), "V9 input-order source binding missing")
    _require(
        binding.get("reviewed_operator_stack_head")
        == out["reviewed_operator_stack_head"]
        and binding.get(
            "canonical_main_must_be_bound_by_later_authorization"
        )
        is True,
        "V9 input-order proposal stack/main binding drift",
    )

    comparison = proposal.get("controlled_comparison")
    _require(
        isinstance(comparison, dict),
        "V9 input-order controlled comparison missing",
    )
    for field in (
        "same_pair_slot",
        "same_arm",
        "same_doctrine",
        "same_seed",
        "same_round_budget",
        "same_tick_budget",
        "same_starter_infantry",
        "same_runtime_selection",
    ):
        _require(
            comparison.get(field) is True,
            "V9 input-order comparison matching drift: " + field,
        )
    _require(
        comparison.get("causal_claim_made") is False,
        "V9 input-order comparison causal claim drift",
    )

    lineage = proposal.get("lineage")
    _require(isinstance(lineage, dict), "V9 input-order lineage missing")
    _require(
        lineage.get("prior_v8_v2_attempt_consumed") is True
        and lineage.get("prior_v8_v2_attempt_reusable") is False
        and lineage.get("prior_v8_v2_authorization_reusable") is False
        and lineage.get("prior_v8_v2_result_reusable_as_authority") is False
        and lineage.get("prior_v8_v2_closeout_reusable_as_authority") is False
        and lineage.get("prior_v8_v2_lineage_closed") is True
        and lineage.get("historical_v9_attempt_reusable") is False
        and lineage.get("historical_v9_authorization_reusable") is False,
        "V9 input-order predecessor lineage reuse drift",
    )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 input-order request review frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (REQUEST_PATH, REQUEST_GIT_BLOB),
        (REQUEST_TEST_PATH, REQUEST_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_input_order_execution_authorization_request_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "request_path": REQUEST_PATH,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_test_path": REQUEST_TEST_PATH,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_bytes_sha256": validated["request_sha256"],
        "request_byte_length": validated["request_byte_length"],
        "pair06_v9_input_order_execution_authorization_request_reviewed": True,
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "doctrine": "FEINTER",
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "runtime_selection_key": "apollyon-v3-qwen35-4b-lora-v1",
        "reviewed_operator_stack_head": validated[
            "reviewed_operator_stack_head"
        ],
        "canonical_main_must_be_bound_by_later_authorization": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_order_evidence_namespace_required": True,
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "historical_v9_attempt_reusable": False,
        "historical_v9_authorization_reusable": False,
        "controlled_comparison_causal_claim_made": False,
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "fresh_order_coherence_activation_authorization_required": True,
        "fresh_user_authorization_text_required": True,
        "matching_request_digest_grants_authority": False,
        "request_digest_reusable_as_authorization": False,
        "general_source_work_authorization_is_execution_authorization": False,
        "v9_execution_authorization_accepted": False,
        "v9_policy_activation_authorization_accepted": False,
        "v9_order_coherence_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "automatic_retry": False,
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
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceRequestReviewHold(NEXT_GATE)
