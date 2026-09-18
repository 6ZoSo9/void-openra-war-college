"""Source-only review of the first bounded Generation-2 V2R13 invocation.

This review pins the exact pair-03 baseline invocation implementation, Precision
CLI, and tests. It performs no host I/O and does not execute runtime. It advances
only to the explicit first-baseline invocation gate.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-first-baseline-invocation-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-first-baseline-invocation-source-binding-review.v1"
)

INVOCATION_GIT_BLOB = "3f4580948aca13a1748703fa0a38a01463a10352"
INVOCATION_SOURCE_SHA256 = (
    "9b1fdab1d371113e68a01f07ae221b60e7a8975aec51639e0fb7d28dadfe893b"
)
PRECISION_CLI_GIT_BLOB = "f543834f86ff52be41498123b423cc1ab9e75f49"
PRECISION_CLI_SOURCE_SHA256 = (
    "255838f63a26dd7c85d29a37ae4df28385698a6f579a0ce27b8c899f5c9857a3"
)
INVOCATION_TEST_GIT_BLOB = "8d0c351a7f851f07f464155d0c539f3b255c3809"
INVOCATION_TEST_SHA256 = (
    "ec941066059d485196a99d61fcb2731c4dc2948c5bbb5b36108f929403326373"
)

PAIR_SLOT = 3
ARM = "baseline"
CONFIRM_TOKEN = "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"

NEXT_GATE = "V2R13_FIRST_BASELINE_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_invocation"


class V2R13FirstBaselineInvocationSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13FirstBaselineInvocationSourceBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_invocation_cached() -> dict[str, Any]:
    contract = invocation.first_baseline_invocation_contract()

    _require(contract.get("pair_slot") == PAIR_SLOT, "pair-slot scope drift")
    _require(contract.get("arm") == ARM, "arm scope drift")
    _require(contract.get("held_out") is False, "baseline unexpectedly held-out")
    _require(
        contract.get("confirm_token") == CONFIRM_TOKEN,
        "confirmation token drift",
    )

    for field in (
        "execution_requires_current_main_preflight",
        "execution_requires_cached_sudo_authority",
        "execution_requires_revocation_sentinel_absent",
        "execution_requires_isolated_grpc_python",
        "restricted_git_worktree_backend_implemented",
        "fresh_canonical_live_readiness_before_inference_implemented",
        "fresh_readiness_uses_reviewed_ollama_http_backend",
        "fresh_readiness_uses_reviewed_rootless_docker_backend",
    ):
        _require(contract.get(field) is True, f"required execution gate missing: {field}")

    _require(
        contract.get("candidate_arm_implemented_by_this_source") is False,
        "candidate execution leaked into first-baseline source",
    )
    _require(
        contract.get("held_out_arm_implemented_by_this_source") is False,
        "held-out execution leaked into first-baseline source",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("runtime_execution_authorized") is True,
        "runtime authority missing",
    )

    for field in (
        "runtime_execution_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"source boundary drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_FIRST_BASELINE_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pre-review gate drift",
    )

    accepted = contract.get("accepted_preflight_evidence_contract")
    _require(isinstance(accepted, dict), "accepted preflight contract missing")
    _require(
        accepted.get("host_preflight_evidence_accepted") is True,
        "host-preflight evidence not accepted",
    )
    _require(
        accepted.get("runtime_execution_authorized") is True,
        "accepted preflight lost runtime authority",
    )
    _require(
        accepted.get("runtime_execution_performed") is False,
        "accepted preflight unexpectedly records runtime execution",
    )

    return deepcopy(contract)


def _validate_invocation() -> dict[str, Any]:
    return deepcopy(_validate_invocation_cached())


def v2r13_first_baseline_invocation_source_binding_review() -> dict[str, Any]:
    validated = _validate_invocation()
    return {
        "schema": REVIEW_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "invocation_source_identity_pinned_by_git_blob": True,
        "invocation_source_identity_pinned_by_sha256": True,
        "precision_cli_identity_pinned_by_git_blob": True,
        "precision_cli_identity_pinned_by_sha256": True,
        "invocation_test_identity_pinned_by_git_blob": True,
        "invocation_test_identity_pinned_by_sha256": True,
        "separate_review_instrument": True,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": False,
        "candidate_arm_reviewed_for_execution": False,
        "held_out_arm_reviewed_for_execution": False,
        "current_main_preflight_required": True,
        "cached_sudo_required": True,
        "revocation_sentinel_required_absent": True,
        "restricted_git_backend_reviewed": True,
        "fresh_readiness_before_inference_reviewed": True,
        "automatic_retry": False,
        "runtime_execution_authorized": True,
        "runtime_execution_invoked": False,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_invocation_contract": validated,
    }


def v2r13_first_baseline_invocation_source_binding_review_contract() -> dict[str, Any]:
    review = v2r13_first_baseline_invocation_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "first_baseline_invocation_source_binding_present": True,
        "first_baseline_invocation_reviewed": True,
        "runtime_execution_authorized": True,
        "runtime_execution_invoked": False,
        "runtime_execution_performed": False,
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": review,
    }


def invoke_first_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13FirstBaselineInvocationSourceBindingReviewHold(NEXT_GATE)
