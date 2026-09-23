"""Source-only review of the pair-06 baseline V8 game-coupled runtime core."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_game_coupled_runtime_generation2
    as runtime_core,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-game-coupled-runtime-review-contract.v1"
)

RUNTIME_CORE_GIT_BLOB = "032966cc0e41a1841eee4637b4c9d798de16a562"
RUNTIME_CORE_SOURCE_SHA256 = (
    "2aa75242b04dbf533ab6fa100524209844cd9f7c029f6b3a736867c4d6a842d6"
)
RUNTIME_CORE_TEST_GIT_BLOB = "2337b3848d4bb294d409e5132159b4248ab3ccc0"
RUNTIME_CORE_TEST_SHA256 = (
    "9179039fcc75cbc5125ce413271465b16cdab3c09cb35f1aa9724d1190e5f85a"
)

NEXT_GATE = "PAIR06_V8_BASELINE_GAME_RUNNER_ADAPTER_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_game_runner_adapter_implementation"


class Pair06V8BaselineGameCoupledRuntimeReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineGameCoupledRuntimeReviewHold(message)


@lru_cache(maxsize=1)
def _validate_runtime_core_cached() -> dict[str, Any]:
    contract = runtime_core.pair06_v8_baseline_game_coupled_runtime_contract()

    _require(
        contract.get("pair06_v8_baseline_game_coupled_runtime_implemented") is True,
        "pair06 game-coupled runtime missing",
    )
    _require(
        contract.get("pair06_v8_baseline_game_coupled_runtime_reviewed") is False,
        "pair06 game-coupled runtime unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 runtime slot drift")
    _require(contract.get("arm") == "baseline", "pair06 runtime arm drift")
    _require(contract.get("held_out") is False, "pair06 runtime became held-out")
    _require(contract.get("seed") == 208354846, "pair06 runtime seed drift")
    _require(contract.get("rounds") == 36, "pair06 runtime rounds drift")
    _require(contract.get("ticks_per_round") == 25, "pair06 runtime ticks drift")
    _require(contract.get("starter_infantry") == 4, "pair06 starter infantry drift")
    _require(contract.get("staging_max_ticks") == 800, "pair06 staging cap drift")
    _require(
        contract.get("runtime_selection_key")
        == "apollyon-v3-v8-accepted-model-control",
        "pair06 runtime selection drift",
    )

    for field in (
        "same_process_load_and_game_implemented",
        "authority_check_before_load_implemented",
        "authority_check_before_each_inference_implemented",
        "fresh_environment_verification_delegated_to_reviewed_loader",
        "exact_asset_verification_delegated_to_reviewed_loader",
        "model_reference_release_in_finally_implemented",
        "game_runner_adapter_required",
    ):
        _require(contract.get(field) is True, f"pair06 runtime implementation drift: {field}")

    _require(
        contract.get("game_runner_adapter_implemented_by_this_source") is False,
        "pair06 source unexpectedly implements game-runner adapter",
    )
    _require(
        contract.get("durable_game_attempt_claim_implemented_by_this_source") is False,
        "pair06 source unexpectedly implements durable game claim",
    )
    _require(
        contract.get("operator_invocation_implemented_by_this_source") is False,
        "pair06 source unexpectedly implements operator invocation",
    )

    for field in (
        "game_coupled_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "runtime_execution_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
        "candidate_runtime_load_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 runtime authority drift: {field}")

    _require(contract.get("automatic_retry") is False, "pair06 automatic retry enabled")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 runtime review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_baseline_game_coupled_runtime_review_contract() -> dict[str, Any]:
    validated = _validate_runtime_core_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "runtime_core_git_blob": RUNTIME_CORE_GIT_BLOB,
        "runtime_core_source_sha256": RUNTIME_CORE_SOURCE_SHA256,
        "runtime_core_test_git_blob": RUNTIME_CORE_TEST_GIT_BLOB,
        "runtime_core_test_sha256": RUNTIME_CORE_TEST_SHA256,
        "pair06_v8_baseline_game_coupled_runtime_source_binding_present": True,
        "pair06_v8_baseline_game_coupled_runtime_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "starter_infantry": 4,
        "staging_max_ticks": 800,
        "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
        "same_process_load_and_game_implemented": True,
        "authority_check_before_load_implemented": True,
        "authority_check_before_each_inference_implemented": True,
        "fresh_environment_verification_delegated_to_reviewed_loader": True,
        "exact_asset_verification_delegated_to_reviewed_loader": True,
        "model_reference_release_in_finally_implemented": True,
        "game_runner_adapter_required": True,
        "game_runner_adapter_implemented": False,
        "durable_game_attempt_claim_implemented": False,
        "operator_invocation_implemented": False,
        "game_coupled_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "candidate_runtime_load_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_runtime_core": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineGameCoupledRuntimeReviewHold(NEXT_GATE)
