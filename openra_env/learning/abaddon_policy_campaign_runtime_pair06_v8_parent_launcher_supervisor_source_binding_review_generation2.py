"""Source-only review of the pair-06 V8 parent launcher/supervisor."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_generation2
    as supervisor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2
    as child_entry,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-launcher-supervisor-review-contract.v1"
)

ENTRYPOINT_GIT_BLOB = "79123c0bc8d67d0001a17d4eff0162b8b9b18e0e"
ENTRYPOINT_SOURCE_SHA256 = (
    "abf44c851df2e412cfc9b115a2467d703bbc17d75016403ba235f37f1c2162bf"
)
ENTRYPOINT_TEST_GIT_BLOB = "45cdb661fdb777076c2fb383f9b9ea93c6c98768"
ENTRYPOINT_TEST_SHA256 = (
    "2a593cef0b481bf0444a60f2fd767704ba8aaad05231aa28dc148be7f4322e32"
)
SUPERVISOR_GIT_BLOB = "cec19a6edebc1ac05a0eba08b5cefeb3b528d0d5"
SUPERVISOR_SOURCE_SHA256 = (
    "7fa91033336e1d03f96c540d156d390b096ac2758c30549659ae32c217152814"
)
SUPERVISOR_TEST_GIT_BLOB = "7a0ef5837a2bba7e9e2abd29334f92eec693c78e"
SUPERVISOR_TEST_SHA256 = (
    "2c1a4bef16cb0f5bbeb57254394168eb62d9e5207e7f5983bc7e51b7c3be8758"
)

NEXT_GATE = "PAIR06_V8_BASELINE_ATTEMPT_CLAIM_AND_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_baseline_attempt_claim_and_invocation_implementation"
)


class Pair06V8ParentSupervisorReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ParentSupervisorReviewHold(message)


@lru_cache(maxsize=1)
def _validate_cached() -> dict[str, Any]:
    entry = child_entry.pair06_v8_proto_game_child_entrypoint_contract()
    sup = supervisor.pair06_v8_parent_launcher_supervisor_contract()

    _require(
        entry.get("pair06_v8_proto_game_child_entrypoint_implemented") is True,
        "pair06 proto child entrypoint missing",
    )
    _require(entry.get("pair_slot") == 6, "child entrypoint slot drift")
    _require(entry.get("arm") == "baseline", "child entrypoint arm drift")
    _require(entry.get("inherited_fd_required") is True, "child inherited fd requirement missing")
    _require(entry.get("socketpair_created_by_entrypoint") is False, "child entrypoint creates socketpair")
    _require(entry.get("exact_confirmation_token_required") is True, "child confirmation token missing")
    _require(entry.get("execution_performed_by_contract_inspection") is False, "child entrypoint inspection executes")

    _require(
        sup.get("pair06_v8_parent_launcher_supervisor_implemented") is True,
        "pair06 parent supervisor missing",
    )
    _require(
        sup.get("pair06_v8_parent_launcher_supervisor_reviewed") is False,
        "pair06 parent supervisor unexpectedly self-reviewed",
    )
    _require(sup.get("pair_slot") == 6, "parent supervisor slot drift")
    _require(sup.get("arm") == "baseline", "parent supervisor arm drift")

    for field in (
        "socketpair_creation_implemented",
        "child_spawn_with_inherited_fd_implemented",
        "child_private_process_group_implemented",
        "hello_ready_handshake_implemented",
        "parent_decision_service_loop_implemented",
        "authority_check_before_load_implemented",
        "authority_check_before_each_inference_implemented",
        "natural_exit_verification_implemented",
        "term_then_kill_retirement_implemented",
        "v8_reference_release_in_finally_implemented",
        "attempt_claim_required_but_not_implemented",
        "worktree_materialization_required_but_not_implemented",
        "isolated_runs_root_required_but_not_created",
    ):
        _require(sup.get(field) is True, f"parent supervisor invariant drift: {field}")

    for field in (
        "execution_authorized_by_contract_inspection",
        "subprocess_spawn_performed_by_contract_inspection",
        "model_load_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(sup.get(field) is False, f"parent supervisor authority drift: {field}")
    _require(sup.get("automatic_retry") is False, "parent supervisor automatic retry enabled")

    _require(
        sup.get("next_gate")
        == "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_SOURCE_BINDING_REVIEW_REQUIRED",
        "parent supervisor review frontier drift",
    )
    return {"entrypoint": deepcopy(entry), "supervisor": deepcopy(sup)}


def pair06_v8_parent_launcher_supervisor_review_contract() -> dict[str, Any]:
    validated = _validate_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "entrypoint_git_blob": ENTRYPOINT_GIT_BLOB,
        "entrypoint_source_sha256": ENTRYPOINT_SOURCE_SHA256,
        "entrypoint_test_git_blob": ENTRYPOINT_TEST_GIT_BLOB,
        "entrypoint_test_sha256": ENTRYPOINT_TEST_SHA256,
        "supervisor_git_blob": SUPERVISOR_GIT_BLOB,
        "supervisor_source_sha256": SUPERVISOR_SOURCE_SHA256,
        "supervisor_test_git_blob": SUPERVISOR_TEST_GIT_BLOB,
        "supervisor_test_sha256": SUPERVISOR_TEST_SHA256,
        "pair06_v8_parent_launcher_supervisor_source_binding_present": True,
        "pair06_v8_parent_launcher_supervisor_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "socketpair_creation_implemented": True,
        "child_spawn_with_inherited_fd_implemented": True,
        "child_private_process_group_implemented": True,
        "hello_ready_handshake_implemented": True,
        "parent_decision_service_loop_implemented": True,
        "authority_check_before_load_implemented": True,
        "authority_check_before_each_inference_implemented": True,
        "natural_exit_verification_implemented": True,
        "term_then_kill_retirement_implemented": True,
        "v8_reference_release_in_finally_implemented": True,
        "attempt_claim_required_but_not_implemented": True,
        "worktree_materialization_required_but_not_implemented": True,
        "isolated_runs_root_required_but_not_created": True,
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
        "validated": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_claim(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ParentSupervisorReviewHold(NEXT_GATE)
