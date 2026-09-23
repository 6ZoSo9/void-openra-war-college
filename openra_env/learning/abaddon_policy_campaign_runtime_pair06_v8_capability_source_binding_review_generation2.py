"""Source-only review of the dormant pair-06 accepted-V8 runtime capability."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_generation2
    as capability,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-runtime-capability-source-binding-review-contract.v1"
)

CAPABILITY_GIT_BLOB = "e9f1157aa138ca9d084dab0297fc099d60905885"
CAPABILITY_SOURCE_SHA256 = (
    "39e22020daa3081fb3b5a100896c8f0df104f643d011bc30aaa1763123efdbbc"
)
CAPABILITY_TEST_GIT_BLOB = "7c834237da0759412c846937703ed6fa9b615d9d"
CAPABILITY_TEST_SHA256 = (
    "31474fbcf690b0fd1b6f4bfab12b369e7c4cf0194cfe7055a6a8afef2e96f456"
)

NEXT_GATE = "PAIR06_V8_HOST_PATH_BINDING_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_host_path_binding"


class Pair06V8RuntimeCapabilityReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8RuntimeCapabilityReviewHold(message)


@lru_cache(maxsize=1)
def _validate_capability_cached() -> dict[str, Any]:
    contract = capability.pair06_v8_runtime_capability_contract()

    _require(
        contract.get("pair06_v8_runtime_capability_implemented") is True,
        "pair06 V8 capability missing",
    )
    _require(
        contract.get("pair06_v8_runtime_capability_reviewed") is False,
        "pair06 V8 capability unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 capability slot drift")
    _require(
        tuple(contract.get("arms", ())) == ("baseline", "candidate"),
        "pair06 capability arm set drift",
    )
    _require(contract.get("held_out") is False, "pair06 capability became held-out")
    _require(
        contract.get("runtime_selection_key")
        == "apollyon-v3-v8-accepted-model-control",
        "pair06 V8 runtime selection drift",
    )
    _require(
        contract.get("activation_kind") == "inprocess_accepted_v8_runtime",
        "pair06 V8 activation kind drift",
    )
    _require(
        contract.get("runtime_loader_callable_bound") is True,
        "pair06 V8 loader callable missing",
    )
    _require(
        contract.get("model_dir_path_bound") is False,
        "pair06 V8 model dir prematurely bound",
    )
    _require(
        contract.get("adapter_dir_path_bound") is False,
        "pair06 V8 adapter dir prematurely bound",
    )
    _require(
        contract.get("runtime_load_authorized") is False,
        "pair06 V8 runtime load prematurely authorized",
    )
    _require(
        contract.get("runtime_load_performed") is False,
        "pair06 V8 runtime already loaded",
    )
    _require(
        contract.get("model_weights_loaded") is False,
        "pair06 V8 model weights already loaded",
    )
    _require(
        contract.get("model_inference_performed") is False,
        "pair06 V8 inference already performed",
    )
    _require(
        contract.get("game_execution_performed") is False,
        "pair06 V8 game already executed",
    )
    _require(
        contract.get("game_mutation_performed") is False,
        "pair06 V8 game mutation already performed",
    )
    _require(
        contract.get("runtime_environment_verification_required_before_load") is True,
        "pair06 V8 environment verification requirement missing",
    )
    _require(
        contract.get("runtime_assets_hash_verification_required_before_load") is True,
        "pair06 V8 asset verification requirement missing",
    )
    _require(
        contract.get("offline_only_model_load_required") is True,
        "pair06 V8 offline-only load requirement missing",
    )
    _require(
        contract.get("authority_callback_required") is True,
        "pair06 V8 authority callback requirement missing",
    )
    _require(contract.get("automatic_retry") is False, "pair06 automatic retry enabled")
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution prematurely authorized",
    )
    _require(
        contract.get("pair03_replay_authorized") is False,
        "pair03 replay authorized",
    )
    _require(
        contract.get("pair09_replay_authorized") is False,
        "pair09 replay authorized",
    )

    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 V8 authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_RUNTIME_CAPABILITY_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 V8 capability review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_runtime_capability_review_contract() -> dict[str, Any]:
    reviewed = _validate_capability_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "capability_git_blob": CAPABILITY_GIT_BLOB,
        "capability_source_sha256": CAPABILITY_SOURCE_SHA256,
        "capability_test_git_blob": CAPABILITY_TEST_GIT_BLOB,
        "capability_test_sha256": CAPABILITY_TEST_SHA256,
        "separate_review_instrument": True,
        "capability_source_identity_pinned_by_git_blob": True,
        "capability_source_identity_pinned_by_sha256": True,
        "capability_test_identity_pinned_by_git_blob": True,
        "capability_test_identity_pinned_by_sha256": True,
        "pair06_v8_runtime_capability_reviewed": True,
        "pair_slot": 6,
        "arms": ("baseline", "candidate"),
        "held_out": False,
        "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
        "activation_kind": "inprocess_accepted_v8_runtime",
        "runtime_loader_callable_bound": True,
        "model_dir_path_bound": False,
        "adapter_dir_path_bound": False,
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
        "reviewed_capability": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def load_pair06_v8_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RuntimeCapabilityReviewHold(
        "PAIR06_V8_HOST_PATH_BINDING_REQUIRED"
    )


def execute_pair06_game(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RuntimeCapabilityReviewHold(
        "PAIR06_V8_GAME_EXECUTION_NOT_AUTHORIZED"
    )


def execute_pair15(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8RuntimeCapabilityReviewHold(
        "PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )
