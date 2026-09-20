"""Source-only preparation review for V2R13 pair-03 candidate execution.

This instrument prepares the next candidate lane without granting or consuming
candidate authority. It binds the completed baseline result, the exact candidate
policy identities, the source-only candidate command materialization, and the
repaired baseline preload/readiness requirements that a future candidate
invocation must inherit.

The historical broad V2R13 executor capability is treated only as reusable
implementation capability. It is not accepted here as sufficient pair-03
candidate execution authority.

Importing or inspecting this module performs no host, model, game, training,
deployment, VOID-chain, wallet, transaction, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2 as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as bounded_executor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as repaired_baseline_invocation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_result_review_generation2
    as baseline_result_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-execution-preparation-review-contract.v1"
)

BASELINE_RESULT_REVIEW_GIT_BLOB = "877c9dd0969b1b2220f5d886da7521aa756a9742"
BOUNDED_EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
FIRST_BASELINE_INVOCATION_GIT_BLOB = "5b790efaf4085deb15eaef538635fd11f5cad9a5"
CANDIDATE_WRAPPER_GIT_BLOB = "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
CANDIDATE_FIXTURE_GIT_BLOB = "20091bff54edbb567127722fae81e5a5308737d2"

CANDIDATE_WRAPPER_SHA256 = (
    "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
)
CANDIDATE_FIXTURE_SHA256 = (
    "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
)
CANDIDATE_GENOME_SHA256 = (
    "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
)
ABADDON_CONTROLLER_SHA256 = (
    "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
)
ABADDON_REFINER_SHA256 = (
    "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
)

BASELINE_TRAJECTORY_SHA256 = (
    "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
)
BASELINE_SUMMARY_SHA256 = (
    "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
)

NEXT_GATE = "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_candidate_execution_authorization"


class V2R13Pair03CandidateExecutionPreparationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidateExecutionPreparationReviewHold(message)


@lru_cache(maxsize=1)
def _baseline_result_cached() -> dict[str, Any]:
    contract = baseline_result_review.v2r13_pair03_baseline_result_review_contract()
    _require(contract.get("baseline_result_reviewed") is True, "baseline result review missing")
    _require(contract.get("pair_slot") == 3, "baseline pair-slot drift")
    _require(contract.get("arm") == "baseline", "baseline arm drift")
    _require(contract.get("baseline_measurement_complete") is True, "baseline incomplete")
    _require(
        contract.get("baseline_measurement_reproducibly_bound") is True,
        "baseline evidence not reproducibly bound",
    )
    _require(
        contract.get("baseline_valid_for_pairwise_comparison") is True,
        "baseline not admitted for pairwise comparison",
    )
    _require(
        contract.get("baseline_trajectory_sha256") == BASELINE_TRAJECTORY_SHA256,
        "baseline trajectory identity drift",
    )
    _require(
        contract.get("baseline_summary_sha256") == BASELINE_SUMMARY_SHA256,
        "baseline summary identity drift",
    )
    _require(contract.get("retry_authority_exhausted") is True, "retry authority not exhausted")
    _require(contract.get("another_retry_authorized") is False, "another retry already authorized")
    _require(
        contract.get("candidate_execution_authorized") is False,
        "candidate execution prematurely authorized",
    )
    _require(
        contract.get("candidate_execution_performed") is False,
        "candidate execution prematurely performed",
    )
    _require(contract.get("next_gate") == NEXT_GATE, "candidate authorization frontier drift")
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _repaired_baseline_capabilities_cached() -> dict[str, Any]:
    contract = repaired_baseline_invocation.first_baseline_invocation_contract()
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
        _require(contract.get(field) is True, f"repaired baseline capability missing: {field}")

    _require(
        contract.get("materialization_receipt_direct_worktree_admission") is False,
        "direct materialization receipt admission reappeared",
    )
    _require(
        contract.get("model_preload_inference_performed") is False,
        "preload crossed inference boundary",
    )
    _require(
        contract.get("candidate_arm_implemented_by_this_source") is False,
        "baseline wrapper unexpectedly implements candidate",
    )
    _require(contract.get("automatic_retry") is False, "baseline wrapper enables automatic retry")
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _candidate_command_cached() -> dict[str, Any]:
    command = command_materializer.materialize_command(pair_slot=3, arm="candidate")
    _require(command.get("pair_slot") == 3, "candidate command pair-slot drift")
    _require(command.get("arm") == "candidate", "candidate command arm drift")
    _require(command.get("runtime_execution_authorized") is False, "candidate command carries authority")
    _require(command.get("runtime_started") is False, "candidate command starts runtime")
    _require(command.get("process_spawn_implemented") is False, "candidate command implements process spawn")
    _require(command.get("command_execution_performed") is False, "candidate command executed")
    _require(command.get("model_load_performed") is False, "candidate command loaded model")
    _require(command.get("model_inference_performed") is False, "candidate command ran inference")
    _require(command.get("game_execution_performed") is False, "candidate command ran game")
    _require(command.get("training_performed") is False, "candidate command trained")
    _require(command.get("weights_updated") is False, "candidate command updated weights")

    bindings = command.get("path_bindings")
    _require(isinstance(bindings, dict), "candidate path bindings missing")
    wrapper = bindings.get("candidate_wrapper")
    fixture = bindings.get("candidate_genome")
    _require(isinstance(wrapper, dict), "candidate wrapper binding missing")
    _require(isinstance(fixture, dict), "candidate fixture binding missing")
    _require(wrapper.get("git_blob") == CANDIDATE_WRAPPER_GIT_BLOB, "candidate wrapper blob drift")
    _require(wrapper.get("sha256") == CANDIDATE_WRAPPER_SHA256, "candidate wrapper SHA drift")
    _require(fixture.get("git_blob") == CANDIDATE_FIXTURE_GIT_BLOB, "candidate fixture blob drift")
    _require(fixture.get("sha256") == CANDIDATE_FIXTURE_SHA256, "candidate fixture SHA drift")
    _require(
        fixture.get("semantic_genome_sha256") == CANDIDATE_GENOME_SHA256,
        "candidate semantic genome drift",
    )
    return deepcopy(command)


def v2r13_pair03_candidate_execution_preparation_review_contract() -> dict[str, Any]:
    baseline = _baseline_result_cached()
    repaired = _repaired_baseline_capabilities_cached()
    candidate_command = _candidate_command_cached()

    _require(
        bounded_executor.CANDIDATE_WRAPPER_GIT_BLOB == CANDIDATE_WRAPPER_GIT_BLOB,
        "bounded executor candidate wrapper blob drift",
    )
    _require(
        bounded_executor.CANDIDATE_FIXTURE_GIT_BLOB == CANDIDATE_FIXTURE_GIT_BLOB,
        "bounded executor candidate fixture blob drift",
    )
    _require(
        bounded_executor.CANDIDATE_WRAPPER_SHA256 == CANDIDATE_WRAPPER_SHA256,
        "bounded executor candidate wrapper SHA drift",
    )
    _require(
        bounded_executor.CANDIDATE_FIXTURE_SHA256 == CANDIDATE_FIXTURE_SHA256,
        "bounded executor candidate fixture SHA drift",
    )
    _require(
        bounded_executor.CANDIDATE_GENOME_SHA256 == CANDIDATE_GENOME_SHA256,
        "bounded executor candidate genome SHA drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "baseline_result_review_git_blob": BASELINE_RESULT_REVIEW_GIT_BLOB,
        "bounded_executor_git_blob": BOUNDED_EXECUTOR_GIT_BLOB,
        "first_baseline_invocation_git_blob": FIRST_BASELINE_INVOCATION_GIT_BLOB,
        "candidate_wrapper_git_blob": CANDIDATE_WRAPPER_GIT_BLOB,
        "candidate_wrapper_sha256": CANDIDATE_WRAPPER_SHA256,
        "candidate_fixture_git_blob": CANDIDATE_FIXTURE_GIT_BLOB,
        "candidate_fixture_sha256": CANDIDATE_FIXTURE_SHA256,
        "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
        "abaddon_controller_sha256": ABADDON_CONTROLLER_SHA256,
        "abaddon_refiner_sha256": ABADDON_REFINER_SHA256,
        "baseline_trajectory_sha256": BASELINE_TRAJECTORY_SHA256,
        "baseline_summary_sha256": BASELINE_SUMMARY_SHA256,
        "candidate_execution_preparation_reviewed": True,
        "pair_slot": 3,
        "candidate_arm": "candidate",
        "baseline_evidence_bound_before_candidate_authorization": True,
        "candidate_policy_identities_bound_before_authorization": True,
        "candidate_command_materialization_source_only": True,
        "bounded_executor_candidate_capability_reusable": True,
        "legacy_v2r13_authorization_sufficient_for_pair03_candidate": False,
        "candidate_specific_authorization_accepted": False,
        "candidate_execution_authorized": False,
        "candidate_execution_performed": False,
        "candidate_invocation_implemented": False,
        "candidate_invocation_reviewed": False,
        "repaired_readiness_path_must_be_inherited": True,
        "fresh_current_main_preflight_required": True,
        "cached_sudo_required": True,
        "revocation_sentinel_absent_required": True,
        "isolated_grpc_python_required": True,
        "exact_model_preload_before_readiness_required": True,
        "preload_must_not_perform_inference": True,
        "canonical_worktree_observation_required": True,
        "fresh_canonical_live_readiness_required": True,
        "baseline_trajectory_binding_required_for_candidate_receipt": True,
        "baseline_summary_binding_required_for_candidate_receipt": True,
        "automatic_retry": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "baseline_result": deepcopy(baseline),
        "repaired_baseline_capabilities": deepcopy(repaired),
        "candidate_command": deepcopy(candidate_command),
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidateExecutionPreparationReviewHold(NEXT_GATE)
