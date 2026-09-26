"""Source-only review of the combat-priority pair-06 execution request.

Pins the exact merged proposal source/tests and the exact canonical request
bytes. Matching request bytes or digest grant no authority.

This review performs no host I/O, GPU observation, attempt claim, model load,
inference, game execution, replay, training, deployment, chain mutation, or
wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-no-offload-receipt-bound-preclaim-gpu-"
    "baseline-execution-authorization-request-review-contract.v1"
)

REQUEST_MAIN_HEAD = "4ad1831d4df9154601220b00ba394060756723fb"
REQUEST_GIT_BLOB = "bcd8467870c97729a36565167f184f825d082e83"
REQUEST_SOURCE_SHA256 = (
    "e2325e74db689962ada7b97e7cba02e95988524568f9c726e3f2e157475a3a03"
)
REQUEST_TEST_GIT_BLOB = "62cc0a0b5238696e36690a699d19c833eb003f6c"
REQUEST_TEST_SHA256 = (
    "fd470854d39afbdfdecfd154a8553e8262faa238c86fe2e87c65b503e4b58950"
)

REQUEST_BYTES_SHA256 = (
    "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
)
REQUEST_BYTE_LENGTH = 5098

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
    "BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "explicit_pair06_v8_combat_action_priority_no_offload_"
    "receipt_bound_preclaim_gpu_baseline_execution_authorization"
)


class Pair06V8CombatPriorityRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = request.pair06_v8_combat_priority_execution_authorization_request_contract()
    proposal = out.get("request")

    _require(
        out.get(
            "pair06_v8_combat_priority_execution_authorization_request_implemented"
        )
        is True,
        "combat-priority request missing",
    )
    _require(
        isinstance(proposal, dict)
        and proposal.get("record_kind") == "proposal_only_not_authorization",
        "combat-priority request not proposal-only",
    )
    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "combat-priority request digest drift",
    )
    _require(
        out.get("request_byte_length") == REQUEST_BYTE_LENGTH,
        "combat-priority request byte-length drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly grants authority",
    )

    binding = proposal.get("source_binding")
    _require(isinstance(binding, dict), "combat-priority source binding missing")
    _require(
        binding.get("invocation_review_main_head")
        == "3bdc27aca30e0926626410bbedc7d445f4a3dd77"
        and binding.get("invocation_review_git_blob")
        == "222db31907543f2b776d811f309488e8dc95706a"
        and binding.get("invocation_review_source_sha256")
        == "297b53a9f934722c0f1f355e52776c40bd9923e0cd5fbb30cca9c427f2a5f7f2"
        and binding.get("invocation_source_sha256")
        == "db383a1a833599d2b444dc4a07d6d1c08ef75e6e5c5dc6fd50cbe173ce5e39dd",
        "combat-priority invocation source binding drift",
    )

    lineage = proposal.get("lineage")
    _require(isinstance(lineage, dict), "combat-priority lineage missing")
    _require(
        lineage.get("prior_spent_gpu_gated_request_sha256")
        == "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
        and lineage.get("prior_spent_gpu_gated_request_reusable") is False,
        "prior request lineage drift",
    )
    _require(
        lineage.get("prior_spent_authorization_text_sha256")
        == "3cdbfa07fcc1fa14ab0ce01a7e5456b1bf16583ceda5baee16a0191e8a3cf011"
        and lineage.get("prior_spent_authorization_reusable") is False,
        "prior authorization lineage drift",
    )
    _require(
        lineage.get("prior_spent_attempt_marker_sha256")
        == "ae0b092a26b1b36f9a6d93f0060df380351d358df227587a9194a3d084b1e9f9"
        and lineage.get("prior_spent_attempt_reusable") is False
        and lineage.get("prior_successful_attempt_consumed") is True,
        "prior successful attempt lineage drift",
    )
    _require(
        lineage.get("prior_result_file_sha256")
        == "f1a3a1ffec2957b984212e5c11067a477934a1c484020dcb2e6398764a117440"
        and lineage.get("prior_result_reusable_as_authority") is False,
        "prior result lineage drift",
    )
    _require(
        lineage.get("prior_closeout_file_sha256")
        == "f0227597d44ecfc5ae07fdc473a2ca9bda71085fba9970279dedf31d5ac24920"
        and lineage.get("prior_closeout_reusable_as_authority") is False,
        "prior closeout lineage drift",
    )

    gpu = proposal.get("gpu_admission_policy")
    _require(isinstance(gpu, dict), "combat-priority GPU policy missing")
    _require(
        gpu.get("gpu_index") == 0
        and gpu.get("fresh_observation_required") is True
        and gpu.get("fresh_observation_precedes_attempt_marker") is True
        and gpu.get("zero_foreign_compute_processes_required") is True
        and gpu.get("minimum_free_memory_fraction")
        == {"numerator": 9, "denominator": 10},
        "combat-priority GPU admission drift",
    )

    activation = proposal.get("policy_activation")
    _require(isinstance(activation, dict), "combat-priority activation policy missing")
    _require(
        activation.get("policy_id")
        == "pair06-v8-combat-action-priority-envelope-v1"
        and activation.get("policy_activation_requested") is True
        and activation.get("separate_policy_activation_authorization_required")
        is True
        and activation.get("separate_policy_confirmation_required") is True
        and activation.get("request_digest_grants_policy_activation") is False,
        "combat-priority policy activation boundary drift",
    )

    scope = proposal.get("proposed_scope")
    _require(isinstance(scope, dict), "combat-priority request scope missing")
    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("doctrine") == "FEINTER"
        and scope.get("seed") == 208354846
        and scope.get("rounds") == 36
        and scope.get("ticks_per_round") == 25
        and scope.get("maximum_attempts") == 1
        and scope.get("maximum_automatic_retries") == 0
        and scope.get("candidate_arm_included") is False
        and scope.get("held_out_pair15_included") is False
        and scope.get("pair03_replay_included") is False
        and scope.get("pair09_replay_included") is False,
        "combat-priority request scope drift",
    )

    for field in (
        "combat_priority_execution_authorization_accepted",
        "combat_priority_policy_activation_authorization_accepted",
        "combat_priority_execution_authorized",
        "combat_priority_policy_activation_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(out.get(field) is False, "combat-priority request authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_"
            "BASELINE_EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "combat-priority request review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_execution_authorization_request_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_main_head": REQUEST_MAIN_HEAD,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "request_bytes_sha256": REQUEST_BYTES_SHA256,
        "request_byte_length": REQUEST_BYTE_LENGTH,
        "pair06_v8_combat_priority_execution_authorization_request_reviewed": True,
        "request_sha256": validated["request_sha256"],
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "separate_execution_authorization_required": True,
        "separate_policy_activation_authorization_required": True,
        "matching_request_digest_grants_authority": False,
        "combat_priority_execution_authorization_accepted": False,
        "combat_priority_policy_activation_authorization_accepted": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_request": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityRequestReviewHold(NEXT_GATE)
