"""Bounded pair-06 baseline V8 game-coupled runtime core.

This source implements the same-process composition required by the reviewed
runtime-lifetime design. It performs no action on import or contract
inspection.

Operational execution requires all of the following:
* explicit execution_authorized=True;
* a callable authority check that remains true before load and before every
  model inference;
* a separately reviewed game-runner adapter supplied by the caller;
* exact pair-06 baseline parameters;
* fresh V8 environment and exact-asset verification performed by the existing
  reviewed load capability.

The core loads V8 and runs the game in the same process. It does not provide
the OpenRA game-runner adapter, durable attempt claim, or operator invocation;
those remain later reviewed gates. Candidate, held-out, training, promotion,
deployment, VOID-chain, wallet, and funds authority remain closed.
"""

from __future__ import annotations

from copy import deepcopy
import gc
import hashlib
import json
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_lifetime_handoff_design_source_binding_review_generation2
    as lifetime_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_generation2
    as capability,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_source_binding_review_generation2
    as host_path_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-game-coupled-runtime-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-game-coupled-runtime-receipt.v1"
)

LIFETIME_REVIEW_GIT_BLOB = "90293b7e6c1138757cf34fcca7e1e4d50cb314dc"
LIFETIME_REVIEW_SOURCE_SHA256 = (
    "b9dd866cba7f92056e1533e1723b9a1ab5a21b7642a6e3e0fd3c5223f5a90d54"
)
HOST_PATH_REVIEW_GIT_BLOB = "c162a8013894ebcb6f310432c96e7daf2c9de3d0"
HOST_PATH_REVIEW_SOURCE_SHA256 = (
    "49c4f44f6f164595fb9c50290b81aa56b62261b4924e859dfd7383a6e84ad07a"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
SEED = 208354846
ROUNDS = 36
TICKS_PER_ROUND = 25
STARTER_INFANTRY = 4
STAGING_MAX_TICKS = 800
RUNTIME_SELECTION_KEY = "apollyon-v3-v8-accepted-model-control"

NEXT_GATE = "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_game_coupled_runtime_review"


class Pair06V8BaselineGameCoupledRuntimeHold(RuntimeError):
    pass


class AuthorityCheck(Protocol):
    def __call__(self, pair_slot: int, arm: str) -> bool:
        ...


class GameRunner(Protocol):
    def __call__(
        self,
        *,
        pair_slot: int,
        arm: str,
        seed: int,
        rounds: int,
        ticks_per_round: int,
        starter_infantry: int,
        staging_max_ticks: int,
        runtime_selection_key: str,
        apollyon_decider: Any,
        authority_check: AuthorityCheck,
    ) -> Mapping[str, Any]:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineGameCoupledRuntimeHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
        default=str,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _dependencies() -> dict[str, Any]:
    lifetime = lifetime_review.pair06_v8_baseline_lifetime_handoff_design_review_contract()
    paths = host_path_review.pair06_v8_host_path_binding_review_contract()

    _require(
        lifetime.get("pair06_v8_baseline_lifetime_handoff_design_reviewed") is True,
        "pair06 lifetime design not reviewed",
    )
    _require(lifetime.get("pair_slot") == PAIR_SLOT, "pair06 lifetime slot drift")
    _require(lifetime.get("arm") == ARM, "pair06 lifetime arm drift")
    _require(lifetime.get("held_out") is False, "pair06 lifetime held-out drift")
    _require(lifetime.get("seed") == SEED, "pair06 lifetime seed drift")
    _require(lifetime.get("rounds") == ROUNDS, "pair06 lifetime rounds drift")
    _require(
        lifetime.get("game_coupled_runtime_lifecycle_required") is True
        and lifetime.get("same_process_load_and_game_required") is True,
        "pair06 same-process lifetime requirement missing",
    )
    _require(
        lifetime.get("new_game_coupled_load_authorization_required") is True
        and lifetime.get("new_game_execution_authorization_required") is True,
        "pair06 new game authority requirement missing",
    )
    _require(
        lifetime.get("game_coupled_load_authorized") is False
        and lifetime.get("game_execution_authorized") is False,
        "pair06 lifetime design prematurely authorizes execution",
    )
    _require(
        lifetime.get("next_gate")
        == "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_IMPLEMENTATION_REQUIRED",
        "pair06 lifetime implementation frontier drift",
    )

    _require(
        paths.get("pair06_v8_host_path_binding_reviewed") is True,
        "pair06 host-path binding not reviewed",
    )
    _require(paths.get("pair_slot") == PAIR_SLOT, "pair06 host-path slot drift")
    _require(
        paths.get("model_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model",
        "pair06 model-dir drift",
    )
    _require(
        paths.get("adapter_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8",
        "pair06 adapter-dir drift",
    )
    _require(paths.get("verified_asset_count") == 17, "pair06 asset-count drift")

    return {
        "lifetime_review": deepcopy(lifetime),
        "host_path_review": deepcopy(paths),
    }


def pair06_v8_baseline_game_coupled_runtime_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "lifetime_review_git_blob": LIFETIME_REVIEW_GIT_BLOB,
        "lifetime_review_source_sha256": LIFETIME_REVIEW_SOURCE_SHA256,
        "host_path_review_git_blob": HOST_PATH_REVIEW_GIT_BLOB,
        "host_path_review_source_sha256": HOST_PATH_REVIEW_SOURCE_SHA256,
        "pair06_v8_baseline_game_coupled_runtime_implemented": True,
        "pair06_v8_baseline_game_coupled_runtime_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "seed": SEED,
        "rounds": ROUNDS,
        "ticks_per_round": TICKS_PER_ROUND,
        "starter_infantry": STARTER_INFANTRY,
        "staging_max_ticks": STAGING_MAX_TICKS,
        "runtime_selection_key": RUNTIME_SELECTION_KEY,
        "same_process_load_and_game_implemented": True,
        "authority_check_before_load_implemented": True,
        "authority_check_before_each_inference_implemented": True,
        "fresh_environment_verification_delegated_to_reviewed_loader": True,
        "exact_asset_verification_delegated_to_reviewed_loader": True,
        "model_reference_release_in_finally_implemented": True,
        "game_runner_adapter_required": True,
        "game_runner_adapter_implemented_by_this_source": False,
        "durable_game_attempt_claim_implemented_by_this_source": False,
        "operator_invocation_implemented_by_this_source": False,
        "game_coupled_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "runtime_execution_performed_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "game_execution_performed_by_contract_inspection": False,
        "candidate_runtime_load_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_pair06_baseline_game_coupled_runtime(
    *,
    execution_authorized: bool,
    authority_check: AuthorityCheck,
    game_runner: GameRunner,
) -> dict[str, Any]:
    """Execute one injected pair-06 baseline game lifecycle when later authorized."""
    dependencies = _dependencies()
    _require(
        type(execution_authorized) is bool and execution_authorized is True,
        "PAIR06_V8_BASELINE_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    _require(callable(authority_check), "pair06 authority_check required")
    _require(callable(game_runner), "pair06 reviewed game_runner adapter required")
    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V8_BASELINE_GAME_AUTHORITY_REVOKED_BEFORE_LOAD",
    )

    paths = dependencies["host_path_review"]
    runtime = capability.load_pair06_v8_runtime(
        pair_slot=PAIR_SLOT,
        arm=ARM,
        model_dir=paths["model_dir"],
        adapter_dir=paths["adapter_dir"],
        runtime_load_authorized=True,
        authority_check=authority_check,
    )

    inference_count = 0
    game_receipt: Mapping[str, Any] | None = None
    model_reference_release_attempted = False
    model_reference_release_completed = False

    def apollyon_decider(
        *,
        state: Mapping[str, Any],
        typed_tools: Any,
        tool_contract: Mapping[str, Any],
        doctrine: str,
        round_no: int,
        feedback: str = "",
    ) -> dict[str, Any]:
        nonlocal inference_count
        _require(
            authority_check(PAIR_SLOT, ARM) is True,
            "PAIR06_V8_BASELINE_GAME_AUTHORITY_REVOKED_BEFORE_INFERENCE",
        )
        _require(runtime is not None, "pair06 V8 runtime released before inference")
        result = runtime.decide_campaign_turn(
            state=state,
            typed_tools=typed_tools,
            tool_contract=tool_contract,
            doctrine=doctrine,
            round_no=round_no,
            feedback=feedback,
        )
        _require(isinstance(result, Mapping), "pair06 V8 decision result must be object")
        inference_count += 1
        return deepcopy(dict(result))

    try:
        game_receipt = game_runner(
            pair_slot=PAIR_SLOT,
            arm=ARM,
            seed=SEED,
            rounds=ROUNDS,
            ticks_per_round=TICKS_PER_ROUND,
            starter_infantry=STARTER_INFANTRY,
            staging_max_ticks=STAGING_MAX_TICKS,
            runtime_selection_key=RUNTIME_SELECTION_KEY,
            apollyon_decider=apollyon_decider,
            authority_check=authority_check,
        )
    finally:
        model_reference_release_attempted = True
        runtime = None
        gc.collect()
        model_reference_release_completed = True

    _require(isinstance(game_receipt, Mapping), "pair06 game-runner receipt must be object")
    supplied = dict(game_receipt)

    for field, expected in (
        ("pair_slot", PAIR_SLOT),
        ("arm", ARM),
        ("held_out", HELD_OUT),
        ("seed", SEED),
        ("rounds_limit", ROUNDS),
        ("ticks_per_round", TICKS_PER_ROUND),
        ("starter_infantry", STARTER_INFANTRY),
        ("staging_max_ticks", STAGING_MAX_TICKS),
        ("runtime_selection_key", RUNTIME_SELECTION_KEY),
    ):
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair06 game-runner receipt drift: {field}",
        )

    for field in (
        "game_started",
        "model_inference_performed",
        "game_execution_performed",
        "game_cleanup_attempted",
        "game_cleanup_completed",
    ):
        _require(
            supplied.get(field) is True,
            f"pair06 game-runner completion missing: {field}",
        )

    _require(inference_count > 0, "pair06 V8 game completed without model inference")
    _require(
        supplied.get("model_inference_count") == inference_count,
        "pair06 inference-count receipt drift",
    )

    for field in (
        "automatic_retry",
        "candidate_runtime_load_performed",
        "candidate_execution_performed",
        "held_out_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(
            supplied.get(field) is False,
            f"pair06 game-runner boundary drift: {field}",
        )

    _require(
        model_reference_release_attempted is True
        and model_reference_release_completed is True,
        "pair06 V8 model reference release incomplete",
    )

    body = {
        "schema": RECEIPT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "seed": SEED,
        "rounds_limit": ROUNDS,
        "ticks_per_round": TICKS_PER_ROUND,
        "starter_infantry": STARTER_INFANTRY,
        "staging_max_ticks": STAGING_MAX_TICKS,
        "runtime_selection_key": RUNTIME_SELECTION_KEY,
        "runtime_load_authorized": True,
        "runtime_load_performed": True,
        "model_inference_authorized": True,
        "model_inference_performed": True,
        "model_inference_count": inference_count,
        "game_execution_authorized": True,
        "game_started": True,
        "game_execution_performed": True,
        "game_cleanup_attempted": True,
        "game_cleanup_completed": True,
        "model_reference_release_attempted": True,
        "model_reference_release_completed": True,
        "automatic_retry": False,
        "candidate_runtime_load_performed": False,
        "candidate_execution_performed": False,
        "held_out_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "game_runner_receipt": deepcopy(supplied),
    }
    return {**body, "execution_receipt_sha256": _digest(body)}
