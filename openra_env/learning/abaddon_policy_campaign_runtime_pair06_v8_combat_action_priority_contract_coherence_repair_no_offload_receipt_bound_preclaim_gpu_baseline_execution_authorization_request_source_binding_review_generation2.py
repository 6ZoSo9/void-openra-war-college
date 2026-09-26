"""Source-only review of the fresh coherent pair-06 execution request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_no_offload_receipt_bound_preclaim_gpu_baseline_execution_authorization_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "execution-authorization-request-review-contract.v1"
)

REQUEST_MAIN_HEAD = "a481eba482d9077a457a1a2c9fc3dca744c49885"
REQUEST_GIT_BLOB = "77e18883acc4c9035591100657012c97f44a92b8"
REQUEST_SOURCE_SHA256 = (
    "054c85fe9d078afb410d210d29f52362ef60a58f613a7256e2793b5e261b1951"
)
REQUEST_TEST_GIT_BLOB = "a1539d2f3ada3037a18275d797858936b2c36d17"
REQUEST_TEST_SHA256 = (
    "42352e775ea97933b3f8e3662c5d53ce1a771e47e1b35ac80d0f4898f00bb699"
)
REQUEST_BYTES_SHA256 = (
    "ef8813f7077efc2b2a3e0ebac1858e4f48e90a986582e2a4bd3a2c1d7d05a90f"
)
REQUEST_BYTE_LENGTH = 4998

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "explicit_fresh_pair06_v8_combat_action_priority_contract_coherence_repair_"
    "execution_and_policy_activation_authorization"
)


class Pair06V8CombatPriorityCoherentRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        request
        .pair06_v8_combat_priority_coherent_execution_authorization_request_contract()
    )
    proposal = out.get("request")

    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_execution_authorization_request_implemented"
        )
        is True,
        "coherent request missing",
    )
    _require(
        isinstance(proposal, dict)
        and proposal.get("record_kind") == "proposal_only_not_authorization",
        "coherent request not proposal-only",
    )
    _require(
        out.get("request_sha256") == REQUEST_BYTES_SHA256,
        "coherent request digest drift",
    )
    _require(
        out.get("request_byte_length") == REQUEST_BYTE_LENGTH,
        "coherent request byte-length drift",
    )
    _require(
        out.get("matching_request_digest_grants_authority") is False,
        "coherent request digest unexpectedly grants authority",
    )

    source = proposal.get("source_binding")
    _require(isinstance(source, dict), "coherent source binding missing")
    _require(
        source.get("invocation_review_main_head")
        == "c941b437d63d82174af2849013d33e8d7ae29a86"
        and source.get("invocation_review_git_blob")
        == "92ac3f8b09aa22be4ed2acf72834da7bc9db08b4"
        and source.get("invocation_review_source_sha256")
        == "05bdcf091a19c0acdc2b40d19617d1c6e15b5788bed8a4e074554795a9d27100"
        and source.get("invocation_source_sha256")
        == "03c05882f2b324ec0166829832dfda3ec88d18274bc7311bed865af9aaf1c095",
        "coherent invocation binding drift",
    )

    lineage = proposal.get("lineage")
    _require(isinstance(lineage, dict), "coherent lineage missing")
    _require(
        lineage.get("prior_failed_request_sha256")
        == "7b02139285193fc69cabe55125b2e643239a0aadee023d2d0f9849411c887ede"
        and lineage.get("prior_failed_request_reusable") is False,
        "prior failed request lineage drift",
    )
    _require(
        lineage.get("prior_failed_authorization_text_sha256")
        == "c17eee0c77cb32d5e8da8b189678fce557bbada9c53a0d4e92d9be7625dd82be"
        and lineage.get("prior_failed_authorization_reusable") is False,
        "prior failed authorization lineage drift",
    )
    _require(
        lineage.get("prior_failed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and lineage.get("prior_failed_attempt_reusable") is False,
        "prior failed attempt lineage drift",
    )
    _require(
        lineage.get("prior_failed_run_id") == FAILED_RUN_ID
        and lineage.get("prior_failed_run_reusable_as_authority") is False
        and lineage.get("prior_failed_result_present") is False
        and lineage.get("prior_failed_closeout_present") is False,
        "prior failed run lineage drift",
    )

    scope = proposal.get("proposed_scope")
    _require(isinstance(scope, dict), "coherent proposed scope missing")
    _require(
        scope.get("pair_slot") == 6
        and scope.get("arm") == "baseline"
        and scope.get("held_out") is False
        and scope.get("doctrine") == "FEINTER"
        and scope.get("seed") == 208354846
        and scope.get("rounds") == 36
        and scope.get("ticks_per_round") == 25
        and scope.get("maximum_attempts") == 1
        and scope.get("maximum_automatic_retries") == 0,
        "coherent proposed scope drift",
    )

    for field in (
        "coherent_execution_authorization_accepted",
        "coherent_policy_activation_authorization_accepted",
        "coherent_execution_authorized",
        "coherent_policy_activation_authorized",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
    ):
        _require(out.get(field) is False, "coherent request authority drift: " + field)

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "NO_OFFLOAD_RECEIPT_BOUND_PRECLAIM_GPU_BASELINE_"
            "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "coherent request review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_combat_priority_coherent_request_review_contract() -> dict[str, Any]:
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
        "pair06_v8_combat_priority_coherent_request_reviewed": True,
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
        "fresh_execution_authorization_required": True,
        "fresh_policy_activation_authorization_required": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "matching_request_digest_grants_authority": False,
        "coherent_execution_authorization_accepted": False,
        "coherent_policy_activation_authorization_accepted": False,
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
    raise Pair06V8CombatPriorityCoherentRequestReviewHold(NEXT_GATE)
