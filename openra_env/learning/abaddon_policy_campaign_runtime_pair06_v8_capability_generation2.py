"""Dormant pair-06 capability for the accepted in-process Apollyon V8 runtime.

Pair 6 is a canonical non-held-out Generation-2 pair whose opponent is the
accepted V8 model-control runtime, not the legacy V2R13/Ollama runtime.

This source composes the reviewed pair-06 allocation with the accepted V8
runtime loader and exact activation contract. Import and contract inspection do
not bind host model paths, load weights, run inference, start OpenRA, mutate a
game, train, promote, deploy, touch VOID-chain state, or touch wallets/funds.

The load entrypoint is dormant and requires BOTH:
* an explicit per-call runtime_load_authorized=True; and
* an authority callback that returns True for pair 6 and the requested arm.

Host model/adapter paths remain unresolved until a later reviewed binding gate.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Protocol

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as runtime_activation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair06_nonheldout_allocation_source_binding_review_generation2
    as allocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-runtime-capability-contract.v1"
)

ALLOCATION_REVIEW_GIT_BLOB = "5dd312086df8d2a6c205badb3feb71560c519990"
ALLOCATION_REVIEW_SOURCE_SHA256 = (
    "695c9ff074a21a7ff6002d30a50852e7a9a746c5735a078f985b80a6a22dfe0a"
)
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"
V8_RUNTIME_SOURCE_SHA256 = (
    "faf4b64ea4755fabdbdfc778f3df534a87f056a638763aa1560c7965c482b5af"
)
RUNTIME_ACTIVATION_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
RUNTIME_ACTIVATION_SOURCE_SHA256 = (
    "dc4c90175dee00f23ab28bc362cec41245a069345c0154d519215e3cb8150a3c"
)

PAIR_SLOT = 6
ARMS = ("baseline", "candidate")
HELD_OUT = False
RUNTIME_SELECTION_KEY = "apollyon-v3-v8-accepted-model-control"
RUNTIME_ACTIVATION_KIND = "inprocess_accepted_v8_runtime"

MODEL_DIR_TOKEN = "<PAIR06_V8_MODEL_DIR>"
ADAPTER_DIR_TOKEN = "<PAIR06_V8_ADAPTER_DIR>"

NEXT_GATE = "PAIR06_V8_RUNTIME_CAPABILITY_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_runtime_capability_source_binding_review"


class Pair06V8RuntimeCapabilityHold(RuntimeError):
    pass


class AuthorityCheck(Protocol):
    def __call__(self, pair_slot: int, arm: str) -> bool:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8RuntimeCapabilityHold(message)


@lru_cache(maxsize=1)
def _allocation_cached() -> dict[str, Any]:
    contract = (
        allocation_review
        .v2r13_pair06_nonheldout_allocation_review_contract()
    )
    _require(
        contract.get("pair06_nonheldout_allocation_reviewed") is True,
        "pair06 allocation not reviewed",
    )
    _require(contract.get("selected_pair_slot") == PAIR_SLOT, "pair06 slot drift")
    _require(contract.get("selected_seed") == 208354846, "pair06 seed drift")
    _require(contract.get("selected_held_out") is False, "pair06 became held-out")
    _require(
        contract.get("selected_opponent_snapshot_id") == RUNTIME_SELECTION_KEY,
        "pair06 runtime selection drift",
    )
    _require(
        contract.get("v2r13_executor_not_applicable_to_pair06") is True,
        "pair06 incorrectly routed through V2R13 executor",
    )
    _require(
        contract.get("pair06_v8_runtime_capability_required") is True,
        "pair06 V8 capability not required",
    )
    _require(
        contract.get("pair06_v8_activation_kind") == RUNTIME_ACTIVATION_KIND,
        "pair06 V8 activation-kind drift",
    )
    _require(
        contract.get("pair06_runtime_execution_authorized") is False,
        "pair06 runtime already authorized",
    )
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution unexpectedly authorized",
    )
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_RUNTIME_CAPABILITY_IMPLEMENTATION_REQUIRED",
        "pair06 V8 capability frontier drift",
    )
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _runtime_contract_cached() -> dict[str, Any]:
    contract = v8_runtime.v8_tool_runtime_contract()
    _require(
        contract.get("tool_runtime_contract_sha256")
        == runtime_activation.V8_TOOL_RUNTIME_CONTRACT_SHA256,
        "accepted V8 runtime contract identity drift",
    )
    _require(
        contract.get("base_model_resolved_revision")
        == runtime_activation.V8_BASE_MODEL_REVISION,
        "accepted V8 base-model revision drift",
    )
    _require(
        contract.get("runtime_environment_live_pip_freeze_match_required") is True,
        "accepted V8 live environment verification requirement missing",
    )
    _require(
        contract.get("local_runtime_loader_implemented") is True,
        "accepted V8 loader missing",
    )
    _require(
        contract.get("runtime_assets_hash_verified_before_load") is True,
        "accepted V8 pre-load asset verification missing",
    )
    _require(
        contract.get("offline_only_model_load") is True,
        "accepted V8 offline-only load boundary missing",
    )
    for field in (
        "runtime_execution_performed",
        "model_execution_performed",
        "game_started",
        "game_mutation_performed",
        "training",
        "weights_updated",
        "automatic_corpus_admission",
        "automatic_policy_promotion",
    ):
        _require(contract.get(field) is False, f"accepted V8 runtime scope drift: {field}")
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _activation_plans_cached() -> dict[str, dict[str, Any]]:
    expected_reasons = (
        "V8_MODEL_DIR_BINDING_NOT_REVIEWED",
        "V8_ADAPTER_DIR_BINDING_NOT_REVIEWED",
        "V8_LOAD_CALL_BINDING_NOT_REVIEWED",
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    result: dict[str, dict[str, Any]] = {}
    for arm in ARMS:
        plan = runtime_activation.arm_runtime_activation_plan(
            pair_slot=PAIR_SLOT,
            arm=arm,
        )
        _require(plan.get("pair_slot") == PAIR_SLOT, f"{arm} activation slot drift")
        _require(plan.get("arm") == arm, f"{arm} activation arm drift")
        _require(plan.get("held_out") is False, f"{arm} activation became held-out")
        _require(
            plan.get("opponent_snapshot_id") == RUNTIME_SELECTION_KEY,
            f"{arm} activation runtime selection drift",
        )
        activation = plan.get("activation")
        _require(isinstance(activation, dict), f"{arm} activation missing")
        _require(
            activation.get("activation_kind") == RUNTIME_ACTIVATION_KIND,
            f"{arm} activation is not accepted V8",
        )
        _require(
            activation.get("tool_runtime_source_sha256")
            == runtime_activation.V8_TOOL_RUNTIME_SOURCE_SHA256,
            f"{arm} V8 tool-runtime identity drift",
        )
        _require(
            activation.get("runtime_specific_activation_binding_reviewed") is False,
            f"{arm} activation binding prematurely reviewed",
        )
        _require(
            activation.get("runtime_specific_identity_probe_reviewed") is False,
            f"{arm} identity probe prematurely reviewed",
        )
        _require(
            activation.get("model_dir_path_bound") is False
            and activation.get("adapter_dir_path_bound") is False,
            f"{arm} host paths prematurely bound",
        )
        _require(
            activation.get("load_call_materialized") is False
            and activation.get("model_weights_loaded") is False,
            f"{arm} V8 runtime prematurely loaded",
        )
        _require(
            tuple(plan.get("reasons", ())) == expected_reasons,
            f"{arm} activation blocker frontier drift",
        )
        authority = plan.get("authority")
        _require(isinstance(authority, dict), f"{arm} authority missing")
        _require(
            authority.get("runtime_execution_authorized") is False,
            f"{arm} runtime prematurely authorized",
        )
        result[arm] = deepcopy(plan)
    return result


def pair06_v8_runtime_capability_contract() -> dict[str, Any]:
    allocation = _allocation_cached()
    runtime = _runtime_contract_cached()
    plans = _activation_plans_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "allocation_review_git_blob": ALLOCATION_REVIEW_GIT_BLOB,
        "allocation_review_source_sha256": ALLOCATION_REVIEW_SOURCE_SHA256,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "v8_runtime_source_sha256": V8_RUNTIME_SOURCE_SHA256,
        "runtime_activation_git_blob": RUNTIME_ACTIVATION_GIT_BLOB,
        "runtime_activation_source_sha256": RUNTIME_ACTIVATION_SOURCE_SHA256,
        "pair06_v8_runtime_capability_implemented": True,
        "pair06_v8_runtime_capability_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arms": ARMS,
        "held_out": HELD_OUT,
        "runtime_selection_key": RUNTIME_SELECTION_KEY,
        "activation_kind": RUNTIME_ACTIVATION_KIND,
        "model_dir_token": MODEL_DIR_TOKEN,
        "adapter_dir_token": ADAPTER_DIR_TOKEN,
        "model_dir_path_bound": False,
        "adapter_dir_path_bound": False,
        "runtime_loader_callable_bound": True,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "game_mutation_performed": False,
        "runtime_environment_verification_required_before_load": True,
        "runtime_assets_hash_verification_required_before_load": True,
        "offline_only_model_load_required": True,
        "authority_callback_required": True,
        "automatic_retry": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "activation_plans": deepcopy(plans),
        "accepted_v8_runtime_contract": deepcopy(runtime),
        "reviewed_pair06_allocation": deepcopy(allocation),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def load_pair06_v8_runtime(
    *,
    pair_slot: int,
    arm: str,
    model_dir: str,
    adapter_dir: str,
    runtime_load_authorized: bool,
    authority_check: AuthorityCheck,
):
    """Dormant exact V8 load path. No game or inference is performed here."""
    _allocation_cached()
    _runtime_contract_cached()
    _activation_plans_cached()

    _require(type(pair_slot) is int and pair_slot == PAIR_SLOT, "pair06 load slot drift")
    _require(type(arm) is str and arm in ARMS, "pair06 load arm drift")
    _require(runtime_load_authorized is True, "PAIR06_V8_RUNTIME_LOAD_AUTHORIZATION_REQUIRED")
    _require(callable(authority_check), "pair06 V8 authority callback required")
    _require(
        authority_check(pair_slot, arm) is True,
        "PAIR06_V8_RUNTIME_LOAD_AUTHORITY_REVOKED",
    )
    _require(type(model_dir) is str and bool(model_dir), "pair06 V8 model dir required")
    _require(type(adapter_dir) is str and bool(adapter_dir), "pair06 V8 adapter dir required")
    _require(model_dir != adapter_dir, "pair06 V8 model/adapter dirs must differ")

    return v8_runtime.FrozenV8LocalToolRuntime.load(
        model_dir=Path(model_dir),
        adapter_dir=Path(adapter_dir),
    )


def execute_pair06_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RuntimeCapabilityHold(
        "PAIR06_V8_GAME_EXECUTION_NOT_IMPLEMENTED"
    )


def execute_pair15(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RuntimeCapabilityHold(
        "PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RuntimeCapabilityHold(
        "CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
