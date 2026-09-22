"""Source-only preparation review for V2R13 pair-09 baseline execution.

This review composes the reviewed pair-09 design with the hardened host,
readiness, preload, worktree, and revocation capabilities proven by the
historical pair-03 baseline wrapper. Those capabilities are reusable; pair-03
runtime authority is not.

No host observation or execution occurs here. Pair-09 baseline remains closed
until a separate explicit authorization gate is satisfied.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as baseline_capabilities,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_evaluation_design_source_binding_review_generation2
    as design_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-execution-preparation-review-contract.v1"
)

DESIGN_REVIEW_GIT_BLOB = "08a1a20a16dcceb2feb183d402edaff96f0cadfa"
DESIGN_REVIEW_SOURCE_SHA256 = (
    "015f6ba4f845e17f88f71f0c76d1ed3debea1c5102786cdcf5c66731b4fda449"
)
FIRST_BASELINE_INVOCATION_GIT_BLOB = "5b790efaf4085deb15eaef538635fd11f5cad9a5"

PAIR_SLOT = 9
ARM = "baseline"
HELD_OUT = False

NEXT_GATE = "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_v2r13_pair09_baseline_execution_authorization"


class V2R13Pair09BaselineExecutionPreparationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineExecutionPreparationReviewHold(message)


@lru_cache(maxsize=1)
def _design_cached() -> dict[str, Any]:
    contract = design_review.v2r13_pair09_evaluation_design_review_contract()
    _require(contract.get("pair09_evaluation_design_reviewed") is True, "pair09 design not reviewed")
    _require(contract.get("pair_slot") == PAIR_SLOT, "pair09 slot drift")
    _require(tuple(contract.get("arms", ())) == ("baseline", "candidate"), "pair09 arms drift")
    _require(contract.get("held_out") is HELD_OUT, "pair09 held-out drift")
    _require(contract.get("baseline_first") is True, "pair09 baseline-first requirement missing")
    _require(
        contract.get("baseline_must_complete_before_candidate") is True,
        "pair09 baseline ordering missing",
    )
    _require(
        contract.get("pair09_baseline_execution_preparation_required") is True,
        "pair09 baseline preparation not required",
    )
    _require(
        contract.get("pair09_baseline_execution_authorized") is False,
        "pair09 baseline already authorized",
    )
    _require(
        contract.get("pair09_candidate_execution_authorized") is False,
        "pair09 candidate already authorized",
    )
    _require(contract.get("pair09_execution_performed") is False, "pair09 already executed")
    _require(contract.get("held_out_execution_authorized") is False, "held-out execution authorized")
    _require(
        contract.get("next_gate") == "V2R13_PAIR09_BASELINE_EXECUTION_PREPARATION_REQUIRED",
        "pair09 preparation frontier drift",
    )
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _hardened_capabilities_cached() -> dict[str, Any]:
    contract = baseline_capabilities.first_baseline_invocation_contract()

    _require(contract.get("pair_slot") == 3, "historical capability source pair drift")
    _require(contract.get("arm") == "baseline", "historical capability source arm drift")

    for field in (
        "execution_requires_current_main_preflight",
        "execution_requires_cached_sudo_authority",
        "execution_requires_revocation_sentinel_absent",
        "execution_requires_isolated_grpc_python",
        "restricted_git_worktree_backend_implemented",
        "fresh_canonical_live_readiness_before_inference_implemented",
        "exact_v2r13_model_preload_before_readiness_implemented",
        "model_preload_uses_empty_generate_prompt",
        "model_preload_requires_empty_response_text",
        "model_preload_token_evaluation_forbidden",
        "fresh_worktree_observation_from_materialization_path_record_implemented",
        "fresh_worktree_observation_uses_explicit_host_lstat_backend",
        "fresh_worktree_observation_uses_reviewed_git_backend",
        "fresh_worktree_observation_uses_reviewed_path_resolver",
        "fresh_readiness_uses_reviewed_ollama_http_backend",
        "fresh_readiness_uses_reviewed_rootless_docker_backend",
    ):
        _require(contract.get(field) is True, f"hardened capability missing: {field}")

    _require(
        contract.get("materialization_receipt_direct_worktree_admission") is False,
        "direct materialization receipt admission reappeared",
    )
    _require(
        contract.get("model_preload_inference_performed") is False,
        "preload unexpectedly performs inference",
    )
    _require(contract.get("automatic_retry") is False, "historical wrapper automatic retry enabled")
    _require(
        contract.get("runtime_execution_performed_by_contract_inspection") is False,
        "historical capability inspection executed runtime",
    )
    _require(
        contract.get("candidate_arm_implemented_by_this_source") is False,
        "historical baseline source unexpectedly implements candidate",
    )
    _require(
        contract.get("held_out_arm_implemented_by_this_source") is False,
        "historical baseline source unexpectedly implements held-out",
    )

    return deepcopy(contract)


def v2r13_pair09_baseline_execution_preparation_review_contract() -> dict[str, Any]:
    design = _design_cached()
    hardened = _hardened_capabilities_cached()
    baseline_command = deepcopy(design["reviewed_design"]["baseline_command"])

    _require(baseline_command.get("pair_slot") == PAIR_SLOT, "pair09 baseline command slot drift")
    _require(baseline_command.get("arm") == ARM, "pair09 baseline command arm drift")
    _require(
        baseline_command.get("workdir_token") == "generation2/pair-09/baseline",
        "pair09 baseline workdir drift",
    )
    _require(
        baseline_command.get("runtime_execution_authorized") is False,
        "pair09 baseline command carries runtime authority",
    )
    _require(
        baseline_command.get("command_execution_performed") is False,
        "pair09 baseline command already executed",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "design_review_git_blob": DESIGN_REVIEW_GIT_BLOB,
        "design_review_source_sha256": DESIGN_REVIEW_SOURCE_SHA256,
        "first_baseline_invocation_git_blob": FIRST_BASELINE_INVOCATION_GIT_BLOB,
        "pair09_baseline_execution_preparation_reviewed": True,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "baseline_first": True,
        "candidate_execution_must_wait_for_baseline_result_review": True,
        "historical_pair03_runtime_authority_sufficient_for_pair09": False,
        "hardened_host_readiness_capabilities_reusable": True,
        "fresh_current_main_preflight_required": True,
        "cached_sudo_required": True,
        "revocation_sentinel_absent_required": True,
        "isolated_grpc_python_required": True,
        "restricted_git_backend_required": True,
        "exact_model_preload_before_readiness_required": True,
        "preload_must_not_perform_inference": True,
        "canonical_worktree_observation_required": True,
        "fresh_canonical_live_readiness_required": True,
        "pair09_baseline_command_source_only": True,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_candidate_execution_performed": False,
        "candidate_replay_permitted": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "baseline_command": baseline_command,
        "reviewed_design": deepcopy(design),
        "reused_hardened_capabilities": deepcopy(hardened),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineExecutionPreparationReviewHold(NEXT_GATE)
