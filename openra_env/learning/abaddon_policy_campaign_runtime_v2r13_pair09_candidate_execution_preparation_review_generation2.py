"""Source-only preparation review for V2R13 pair-09 candidate execution.

This review binds the completed pair-09 baseline result to the canonical
pair-09 candidate command. It proves the two arms share pair slot, seed, round
limit, runner argv and reviewed runtime identity while pinning the exact
candidate wrapper/genome identities.

It grants no candidate execution authority and performs no host, runtime, model,
game, training, deployment, VOID-chain, wallet, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2
    as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as bounded_executor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_result_review_generation2
    as baseline_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-execution-preparation-review-contract.v1"
)

BASELINE_RESULT_REVIEW_GIT_BLOB = "e0f663b144aa2036d7dba2a8d001f8f061f2f892"
BASELINE_RESULT_REVIEW_SOURCE_SHA256 = (
    "acda9a94d229e73381aa45e6898f55b7eb066b67bb1bc29685276518026b9431"
)
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
BOUNDED_EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"

CANDIDATE_WRAPPER_GIT_BLOB = "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
CANDIDATE_WRAPPER_SHA256 = (
    "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
)
CANDIDATE_FIXTURE_GIT_BLOB = "20091bff54edbb567127722fae81e5a5308737d2"
CANDIDATE_FIXTURE_SHA256 = (
    "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
)
CANDIDATE_GENOME_SHA256 = (
    "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
)

BASELINE_TRAJECTORY_SHA256 = (
    "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
)
BASELINE_SUMMARY_SHA256 = (
    "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
)
BASELINE_RESULT_FILE_SHA256 = (
    "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
)

PAIR_SLOT = 9
SEED = 1496195137
ROUND_LIMIT = 36
RUNTIME_SELECTION_KEY = "apollyon-v2r13-qualified-predecessor"

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_authorization_request"


class V2R13Pair09CandidateExecutionPreparationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateExecutionPreparationReviewHold(message)


@lru_cache(maxsize=1)
def _baseline_cached() -> dict[str, Any]:
    contract = baseline_review.v2r13_pair09_baseline_result_review_contract()
    _require(contract.get("baseline_result_reviewed") is True, "baseline result review missing")
    _require(contract.get("pair_slot") == PAIR_SLOT, "baseline pair-slot drift")
    _require(contract.get("arm") == "baseline", "baseline arm drift")
    _require(contract.get("held_out") is False, "baseline held-out drift")
    _require(contract.get("baseline_measurement_complete") is True, "baseline incomplete")
    _require(
        contract.get("baseline_measurement_reproducibly_bound") is True,
        "baseline not reproducibly bound",
    )
    _require(
        contract.get("baseline_valid_for_pairwise_comparison") is True,
        "baseline not admitted for pairwise comparison",
    )
    _require(contract.get("baseline_seed") == SEED, "baseline seed drift")
    _require(contract.get("baseline_rounds_completed") == ROUND_LIMIT, "baseline round-limit drift")
    _require(
        contract.get("baseline_trajectory_sha256") == BASELINE_TRAJECTORY_SHA256,
        "baseline trajectory drift",
    )
    _require(
        contract.get("baseline_summary_sha256") == BASELINE_SUMMARY_SHA256,
        "baseline summary drift",
    )
    _require(
        contract.get("baseline_result_file_sha256") == BASELINE_RESULT_FILE_SHA256,
        "baseline result-file drift",
    )
    _require(contract.get("baseline_attempt_exhausted") is True, "baseline attempt not exhausted")
    _require(
        contract.get("another_baseline_execution_authorized") is False,
        "another baseline unexpectedly authorized",
    )
    _require(
        contract.get("candidate_execution_authorized") is False,
        "candidate prematurely authorized",
    )
    _require(
        contract.get("candidate_execution_performed") is False,
        "candidate prematurely executed",
    )
    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
        "baseline candidate frontier drift",
    )
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _commands_cached() -> dict[str, dict[str, Any]]:
    baseline = command_materializer.materialize_command(
        pair_slot=PAIR_SLOT,
        arm="baseline",
    )
    candidate = command_materializer.materialize_command(
        pair_slot=PAIR_SLOT,
        arm="candidate",
    )

    for arm, command in (("baseline", baseline), ("candidate", candidate)):
        _require(command.get("pair_slot") == PAIR_SLOT, f"{arm} pair-slot drift")
        _require(command.get("arm") == arm, f"{arm} arm drift")
        _require(command.get("runtime_execution_authorized") is False, f"{arm} carries authority")
        _require(command.get("runtime_started") is False, f"{arm} runtime started")
        _require(command.get("process_spawn_implemented") is False, f"{arm} process spawn implemented")
        _require(command.get("command_execution_performed") is False, f"{arm} command executed")
        _require(command.get("model_load_performed") is False, f"{arm} model loaded")
        _require(command.get("model_inference_performed") is False, f"{arm} inference performed")
        _require(command.get("game_execution_performed") is False, f"{arm} game executed")
        _require(command.get("training_performed") is False, f"{arm} training performed")
        _require(command.get("weights_updated") is False, f"{arm} weights updated")

    _require(
        tuple(baseline["runner_argv"]) == tuple(candidate["runner_argv"]),
        "matched pair runner argv drift",
    )
    runner_argv = tuple(candidate["runner_argv"])
    _require("--seed" in runner_argv, "candidate seed flag missing")
    _require(
        runner_argv[runner_argv.index("--seed") + 1] == str(SEED),
        "candidate seed drift",
    )
    _require("--rounds" in runner_argv, "candidate rounds flag missing")
    _require(
        runner_argv[runner_argv.index("--rounds") + 1] == str(ROUND_LIMIT),
        "candidate round-limit drift",
    )
    _require(
        baseline.get("runtime_selection_key")
        == candidate.get("runtime_selection_key")
        == RUNTIME_SELECTION_KEY,
        "matched pair runtime selection drift",
    )
    _require(
        baseline.get("opponent_snapshot_sha256")
        == candidate.get("opponent_snapshot_sha256"),
        "matched pair opponent snapshot drift",
    )
    _require(
        baseline.get("runtime_realization_sha256")
        == candidate.get("runtime_realization_sha256"),
        "matched pair runtime realization drift",
    )

    bindings = candidate.get("path_bindings")
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

    return {"baseline": deepcopy(baseline), "candidate": deepcopy(candidate)}


def v2r13_pair09_candidate_execution_preparation_review_contract() -> dict[str, Any]:
    baseline = _baseline_cached()
    commands = _commands_cached()

    _require(
        bounded_executor.CANDIDATE_WRAPPER_GIT_BLOB == CANDIDATE_WRAPPER_GIT_BLOB,
        "bounded executor wrapper blob drift",
    )
    _require(
        bounded_executor.CANDIDATE_FIXTURE_GIT_BLOB == CANDIDATE_FIXTURE_GIT_BLOB,
        "bounded executor fixture blob drift",
    )
    _require(
        bounded_executor.CANDIDATE_WRAPPER_SHA256 == CANDIDATE_WRAPPER_SHA256,
        "bounded executor wrapper SHA drift",
    )
    _require(
        bounded_executor.CANDIDATE_FIXTURE_SHA256 == CANDIDATE_FIXTURE_SHA256,
        "bounded executor fixture SHA drift",
    )
    _require(
        bounded_executor.CANDIDATE_GENOME_SHA256 == CANDIDATE_GENOME_SHA256,
        "bounded executor genome SHA drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "baseline_result_review_git_blob": BASELINE_RESULT_REVIEW_GIT_BLOB,
        "baseline_result_review_source_sha256": BASELINE_RESULT_REVIEW_SOURCE_SHA256,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "bounded_executor_git_blob": BOUNDED_EXECUTOR_GIT_BLOB,
        "candidate_wrapper_git_blob": CANDIDATE_WRAPPER_GIT_BLOB,
        "candidate_wrapper_sha256": CANDIDATE_WRAPPER_SHA256,
        "candidate_fixture_git_blob": CANDIDATE_FIXTURE_GIT_BLOB,
        "candidate_fixture_sha256": CANDIDATE_FIXTURE_SHA256,
        "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
        "candidate_execution_preparation_reviewed": True,
        "pair_slot": PAIR_SLOT,
        "candidate_arm": "candidate",
        "held_out": False,
        "baseline_evidence_bound_before_candidate_authorization": True,
        "baseline_attempt_exhausted": True,
        "baseline_valid_for_pairwise_comparison": True,
        "baseline_trajectory_sha256": BASELINE_TRAJECTORY_SHA256,
        "baseline_summary_sha256": BASELINE_SUMMARY_SHA256,
        "baseline_result_file_sha256": BASELINE_RESULT_FILE_SHA256,
        "matched_pair_seed": SEED,
        "matched_pair_round_limit": ROUND_LIMIT,
        "matched_pair_runner_argv": tuple(commands["candidate"]["runner_argv"]),
        "matched_pair_runtime_selection_key": RUNTIME_SELECTION_KEY,
        "matched_pair_opponent_snapshot_sha256": commands["candidate"]["opponent_snapshot_sha256"],
        "matched_pair_runtime_realization_sha256": commands["candidate"]["runtime_realization_sha256"],
        "candidate_command_source_only": True,
        "candidate_command": deepcopy(commands["candidate"]),
        "baseline_command": deepcopy(commands["baseline"]),
        "legacy_six_arm_authorization_sufficient": False,
        "candidate_execution_authorized": False,
        "candidate_execution_performed": False,
        "another_baseline_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "baseline_result": deepcopy(baseline),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateExecutionPreparationReviewHold(NEXT_GATE)
