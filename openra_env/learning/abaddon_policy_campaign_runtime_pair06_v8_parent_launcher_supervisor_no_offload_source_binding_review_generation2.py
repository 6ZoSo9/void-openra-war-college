"""Source-only review of no-offload pair-06 V8 parent supervisor generation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as supervisor,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-launcher-supervisor-no-offload-review-contract.v1"
)

SUPERVISOR_GIT_BLOB = "231758aeced0a57949dc39165df0f994e8473ebc"
SUPERVISOR_SOURCE_SHA256 = (
    "1333cac233d6e9235a2d64c36b8398bb4773150cf2fe5025f28fed5457fe7d7f"
)
SUPERVISOR_TEST_GIT_BLOB = "db1261a4dcd3df33e5d2e53a07084ff0346100c3"
SUPERVISOR_TEST_SHA256 = (
    "a1f3fdc2a4f718015a8c330a2404f5a8cd344bad53d0e331af9bc9c69d8a3f6c"
)

NEXT_GATE = "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_attempt_invocation_no_offload"


class Pair06V8ParentSupervisorNoOffloadReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ParentSupervisorNoOffloadReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = supervisor.pair06_v8_parent_launcher_supervisor_no_offload_contract()
    _require(
        out.get("pair06_v8_parent_launcher_supervisor_implemented") is True,
        "no-offload pair06 parent supervisor missing",
    )
    _require(
        out.get("pair06_v8_parent_launcher_supervisor_reviewed") is False,
        "no-offload pair06 parent supervisor unexpectedly self-reviewed",
    )
    _require(out.get("pair_slot") == 6, "no-offload pair06 parent slot drift")
    _require(out.get("arm") == "baseline", "no-offload pair06 parent arm drift")

    for field in (
        "socketpair_creation_implemented",
        "child_spawn_with_inherited_fd_implemented",
        "child_private_process_group_implemented",
        "hello_ready_handshake_implemented",
        "parent_decision_service_loop_implemented",
        "authority_check_before_load_implemented",
        "authority_check_before_each_inference_implemented",
        "inference_safe_no_offload_loader_reviewed",
        "inference_safe_loader_bound_before_generate_adapter",
        "cpu_disk_meta_parameter_offload_forbidden",
        "all_parameters_cuda0_required_before_child_spawn",
        "inference_safe_placement_receipt_implemented",
        "offload_safe_generate_adapter_reviewed",
        "offload_safe_generate_bound_after_load_before_child_spawn",
        "natural_exit_verification_implemented",
        "term_then_kill_retirement_implemented",
        "v8_reference_release_in_finally_implemented",
        "attempt_claim_required_but_not_implemented",
        "worktree_materialization_required_but_not_implemented",
        "isolated_runs_root_required_but_not_created",
    ):
        _require(out.get(field) is True, f"no-offload parent invariant drift: {field}")

    _require(
        out.get("hard_coded_cuda_input_transfer_used_by_pair06_parent") is False,
        "no-offload parent hard-coded CUDA input drift",
    )
    for field in (
        "execution_authorized_by_contract_inspection",
        "subprocess_spawn_performed_by_contract_inspection",
        "model_load_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
        "automatic_retry",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(out.get(field) is False, f"no-offload parent boundary drift: {field}")

    _require(
        out.get("next_gate")
        == "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
        "no-offload parent review frontier drift",
    )
    return deepcopy(out)


def pair06_v8_parent_launcher_supervisor_no_offload_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "supervisor_git_blob": SUPERVISOR_GIT_BLOB,
        "supervisor_source_sha256": SUPERVISOR_SOURCE_SHA256,
        "supervisor_test_git_blob": SUPERVISOR_TEST_GIT_BLOB,
        "supervisor_test_sha256": SUPERVISOR_TEST_SHA256,
        "pair06_v8_parent_launcher_supervisor_no_offload_source_binding_present": True,
        "pair06_v8_parent_launcher_supervisor_no_offload_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "inference_safe_no_offload_loader_reviewed": True,
        "cpu_disk_meta_parameter_offload_forbidden": True,
        "all_parameters_cuda0_required_before_child_spawn": True,
        "inference_safe_placement_receipt_implemented": True,
        "attempt_claim_required_but_not_implemented": True,
        "execution_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_supervisor": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_claim(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ParentSupervisorNoOffloadReviewHold(NEXT_GATE)
