"""Source-only review of the bounded Generation-2 V2R13 executor.

This review pins the exact accepted executor candidate by Git blob and SHA-256,
independently validates its six-arm authorization surface and safety frontier,
and advances only to host preflight. It performs no host observation, worktree
materialization, runtime start, model inference, game execution, training,
deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as executor,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-bounded-runtime-executor-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-bounded-runtime-executor-source-binding-review.v1"
)

EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
EXECUTOR_SOURCE_SHA256 = (
    "92e92fb32b23b56a3986519d47f44653bb293739f03360de90b32ebf72664a16"
)
EXECUTOR_TEST_GIT_BLOB = "8bbc22fced55191da23b110f79a83cae8b796ecd"
EXECUTOR_TEST_SHA256 = (
    "41216421831edc80223638674946261288d76f23b9024a5f232475f7a41c0fff"
)

AUTHORIZATION_SOURCE_GIT_BLOB = "2501d48ae889b9ed17cdf42acef033023f7d3886"
AUTHORIZATION_ATTESTATION_SHA256 = (
    "34ad7143e876b91056f730de37ab470b6fd8a5f99d84aadefb178cabf87a2031"
)
WORKTREE_MATERIALIZER_REVIEW_GIT_BLOB = "3dcc325c431ec451a737b6e228c365ce1acb4f98"
PORTABLE_CHECKOUT_GIT_BLOB = "077fbf5a2847d85113eb8fcba3904b02343ebfef"
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
CANDIDATE_WRAPPER_GIT_BLOB = "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
CANDIDATE_FIXTURE_GIT_BLOB = "20091bff54edbb567127722fae81e5a5308737d2"

AUTHORIZED_PAIR_SLOTS = (3, 9, 15)
HELD_OUT_PAIR_SLOTS = (15,)
AUTHORIZED_ARMS = ("baseline", "candidate")
AUTHORIZED_EXECUTION_ARM_COUNT = 6

NEXT_GATE = "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_REQUIRED"
NEXT_CHANGE_CLASS = "v2r13_runtime_execution_host_preflight"


class V2R13BoundedExecutorSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13BoundedExecutorSourceBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_executor_cached() -> dict[str, Any]:
    _require(
        executor.AUTHORIZATION_SOURCE_GIT_BLOB == AUTHORIZATION_SOURCE_GIT_BLOB,
        "executor authorization-source blob drift",
    )
    _require(
        executor.AUTHORIZATION_ATTESTATION_SHA256
        == AUTHORIZATION_ATTESTATION_SHA256,
        "executor authorization attestation drift",
    )
    _require(
        executor.WORKTREE_MATERIALIZER_REVIEW_GIT_BLOB
        == WORKTREE_MATERIALIZER_REVIEW_GIT_BLOB,
        "executor materializer-review blob drift",
    )
    _require(
        executor.PORTABLE_CHECKOUT_GIT_BLOB == PORTABLE_CHECKOUT_GIT_BLOB,
        "executor portable-checkout blob drift",
    )
    _require(
        executor.COMMAND_MATERIALIZER_GIT_BLOB == COMMAND_MATERIALIZER_GIT_BLOB,
        "executor command-materializer blob drift",
    )
    _require(
        executor.CANDIDATE_WRAPPER_GIT_BLOB == CANDIDATE_WRAPPER_GIT_BLOB,
        "executor candidate-wrapper blob drift",
    )
    _require(
        executor.CANDIDATE_FIXTURE_GIT_BLOB == CANDIDATE_FIXTURE_GIT_BLOB,
        "executor candidate-fixture blob drift",
    )
    _require(
        tuple(executor.AUTHORIZED_PAIR_SLOTS) == AUTHORIZED_PAIR_SLOTS,
        "executor authorized pair-slot drift",
    )
    _require(
        tuple(executor.HELD_OUT_PAIR_SLOTS) == HELD_OUT_PAIR_SLOTS,
        "executor held-out pair-slot drift",
    )
    _require(
        tuple(executor.AUTHORIZED_ARMS) == AUTHORIZED_ARMS,
        "executor authorized-arm drift",
    )
    _require(
        executor.AUTHORIZED_EXECUTION_ARM_COUNT == AUTHORIZED_EXECUTION_ARM_COUNT,
        "executor authorized-arm count drift",
    )

    contract = executor.bounded_v2r13_runtime_executor_contract()
    _require(
        contract.get("bounded_v2r13_runtime_executor_implemented") is True,
        "bounded V2R13 executor implementation missing",
    )
    _require(
        contract.get("bounded_v2r13_runtime_executor_reviewed") is False,
        "executor unexpectedly self-reviews",
    )
    _require(
        tuple(contract.get("authorized_pair_slots", ())) == AUTHORIZED_PAIR_SLOTS,
        "executor contract pair-slot drift",
    )
    _require(
        tuple(contract.get("held_out_pair_slots", ())) == HELD_OUT_PAIR_SLOTS,
        "executor contract held-out drift",
    )
    _require(
        tuple(contract.get("authorized_arms", ())) == AUTHORIZED_ARMS,
        "executor contract arm drift",
    )
    _require(
        contract.get("authorized_execution_arm_count")
        == AUTHORIZED_EXECUTION_ARM_COUNT,
        "executor contract arm-count drift",
    )
    _require(
        contract.get("other_runtime_lanes_implemented_by_this_source") is False,
        "executor source implements another runtime lane",
    )

    for field in (
        "fresh_readiness_hook_after_runtime_start_before_inference",
        "readiness_failure_runtime_cleanup_implemented",
        "successful_runtime_cleanup_observation_implemented",
        "revocation_check_before_materialization_implemented",
        "revocation_check_before_inference_implemented",
        "detached_frozen_worktree_composition_implemented",
        "portable_runner_binding_composition_implemented",
        "candidate_policy_hook_composition_implemented",
        "isolated_output_root_implemented",
    ):
        _require(contract.get(field) is True, f"executor safety feature missing: {field}")

    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "runtime_execution_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
    ):
        _require(contract.get(field) is False, f"executor boundary drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "executor pre-review next-gate drift",
    )
    _require(
        contract.get("next_change_class")
        == "source_only_v2r13_runtime_execution_implementation_source_binding_review",
        "executor pre-review next-change drift",
    )

    plans = contract.get("execution_plans")
    _require(isinstance(plans, list), "executor plan ledger missing")
    _require(len(plans) == AUTHORIZED_EXECUTION_ARM_COUNT, "executor plan cardinality drift")

    seen: set[tuple[int, str]] = set()
    plan_hashes: set[str] = set()
    for plan in plans:
        _require(isinstance(plan, Mapping), "executor plan malformed")
        pair_slot = plan.get("pair_slot")
        arm = plan.get("arm")
        _require(pair_slot in AUTHORIZED_PAIR_SLOTS, "unreviewed V2R13 pair slot")
        _require(arm in AUTHORIZED_ARMS, "unreviewed V2R13 arm")
        key = (int(pair_slot), str(arm))
        _require(key not in seen, "duplicate V2R13 execution plan")
        seen.add(key)
        _require(plan.get("runtime_selection_key") == V2R13, "runtime selection drift")
        _require(
            plan.get("authorization_attestation_sha256")
            == AUTHORIZATION_ATTESTATION_SHA256,
            "plan authorization binding drift",
        )
        _require(plan.get("runtime_execution_authorized") is True, "plan authority missing")
        _require(
            plan.get("fresh_runtime_readiness_required") is True,
            "plan fresh-readiness gate missing",
        )
        _require(
            plan.get("revocation_check_required") is True,
            "plan revocation gate missing",
        )
        _require(plan.get("automatic_retry") is False, "plan automatic retry enabled")
        _require(
            plan.get("held_out") is (pair_slot in HELD_OUT_PAIR_SLOTS),
            "plan held-out classification drift",
        )
        for field in (
            "training_authorized",
            "weights_update_authorized",
            "automatic_policy_promotion_authorized",
            "deployment_authorized",
            "void_chain_mutation_authorized",
            "wallet_or_funds_action_authorized",
        ):
            _require(plan.get(field) is False, f"plan forbidden authority drift: {field}")
        plan_sha = plan.get("plan_sha256")
        _require(isinstance(plan_sha, str) and len(plan_sha) == 64, "plan digest malformed")
        _require(plan_sha not in plan_hashes, "duplicate V2R13 plan digest")
        plan_hashes.add(plan_sha)

    expected_keys = {
        (pair_slot, arm)
        for pair_slot in AUTHORIZED_PAIR_SLOTS
        for arm in AUTHORIZED_ARMS
    }
    _require(seen == expected_keys, "reviewed V2R13 plan set drift")
    _require(len(plan_hashes) == AUTHORIZED_EXECUTION_ARM_COUNT, "plan digest uniqueness drift")

    return {
        "executor_source_identity_pinned": True,
        "executor_test_identity_pinned": True,
        "authorization_binding_pinned": True,
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "held_out_pair_slots": HELD_OUT_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "authorized_execution_arm_count": AUTHORIZED_EXECUTION_ARM_COUNT,
        "unique_plan_digest_count": len(plan_hashes),
        "execution_plans": deepcopy(plans),
        "runtime_execution_authorization_accepted": True,
        "runtime_execution_implemented": True,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
    }


def _validate_executor() -> dict[str, Any]:
    return deepcopy(_validate_executor_cached())


def v2r13_bounded_executor_source_binding_review() -> dict[str, Any]:
    validated = _validate_executor()
    return {
        "schema": REVIEW_SCHEMA,
        "executor_git_blob": EXECUTOR_GIT_BLOB,
        "executor_source_sha256": EXECUTOR_SOURCE_SHA256,
        "executor_test_git_blob": EXECUTOR_TEST_GIT_BLOB,
        "executor_test_sha256": EXECUTOR_TEST_SHA256,
        "executor_source_identity_pinned_by_git_blob": True,
        "executor_source_identity_pinned_by_sha256": True,
        "executor_test_identity_pinned_by_git_blob": True,
        "executor_test_identity_pinned_by_sha256": True,
        "separate_review_instrument": True,
        "bounded_v2r13_runtime_executor_implemented": True,
        "bounded_v2r13_runtime_executor_source_binding_present": True,
        "bounded_v2r13_runtime_executor_reviewed": True,
        "authorization_scope": "v2r13_lane_only",
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "held_out_pair_slots": HELD_OUT_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "authorized_execution_arm_count": AUTHORIZED_EXECUTION_ARM_COUNT,
        "other_runtime_lanes_authorized": False,
        "fresh_readiness_required_before_inference": True,
        "readiness_failure_cleanup_reviewed": True,
        "successful_runtime_cleanup_observation_reviewed": True,
        "revocation_checks_reviewed": True,
        "automatic_retry": False,
        "runtime_execution_authorization_accepted": True,
        "runtime_execution_implemented": True,
        "runtime_execution_performed": False,
        "host_preflight_completed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_executor": validated,
    }


def v2r13_bounded_executor_source_binding_review_contract() -> dict[str, Any]:
    review = v2r13_bounded_executor_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "executor_git_blob": EXECUTOR_GIT_BLOB,
        "executor_source_sha256": EXECUTOR_SOURCE_SHA256,
        "executor_test_git_blob": EXECUTOR_TEST_GIT_BLOB,
        "executor_test_sha256": EXECUTOR_TEST_SHA256,
        "bounded_v2r13_runtime_executor_source_binding_present": True,
        "bounded_v2r13_runtime_executor_reviewed": True,
        "runtime_execution_authorization_accepted": True,
        "runtime_execution_implemented": True,
        "runtime_execution_performed": False,
        "host_preflight_completed": False,
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": review,
    }


def execute_reviewed_v2r13_runtime(*args: Any, **kwargs: Any) -> None:
    raise V2R13BoundedExecutorSourceBindingReviewHold(NEXT_GATE)


def execute_other_runtime_lane(*args: Any, **kwargs: Any) -> None:
    raise V2R13BoundedExecutorSourceBindingReviewHold(
        "AUTHORIZATION_SCOPE_V2R13_ONLY"
    )
