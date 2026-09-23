"""Source-only review of accepted pair-06 V8 Precision host-path evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_host_path_observation_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-host-path-observation-source-binding-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "df31976eba984e5e2ee35250043a836059c835ef"
ACCEPTANCE_SOURCE_SHA256 = (
    "e852c56a7f3cbe97998fb4363eaacf57463895babf11b62f4332c010d986f872"
)
ACCEPTANCE_TEST_GIT_BLOB = "5f9a74bc8a26fa0d1fed5fe3119e275d85cfaa2c"
ACCEPTANCE_TEST_SHA256 = (
    "1587df7abb5a63544c39a87f067246587f6bec671bac7098ad3bbac7731b4180"
)

NEXT_GATE = "PAIR06_V8_HOST_PATH_BINDING_SOURCE_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_host_path_binding"


class Pair06V8PrecisionHostPathObservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PrecisionHostPathObservationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = (
        acceptance
        .pair06_v8_precision_host_path_observation_acceptance_contract()
    )
    _require(
        contract.get("pair06_v8_precision_host_path_observation_accepted") is True,
        "pair06 V8 Precision observation acceptance missing",
    )
    _require(
        contract.get("observer_sha256")
        == "033f3ded80191902d74687c5f12a5f03e9f12d956a7c293ee706999acdf59c18",
        "pair06 V8 observer SHA drift",
    )
    _require(
        contract.get("model_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model",
        "pair06 V8 model dir drift",
    )
    _require(
        contract.get("adapter_dir")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8",
        "pair06 V8 adapter dir drift",
    )
    _require(
        contract.get("verified_asset_count") == 17,
        "pair06 V8 verified asset count drift",
    )
    _require(
        contract.get("runtime_load_authorized") is False
        and contract.get("runtime_load_performed") is False,
        "pair06 V8 runtime load unexpectedly authorized/performed",
    )
    _require(
        contract.get("model_inference_performed") is False
        and contract.get("game_execution_performed") is False,
        "pair06 V8 observation unexpectedly executed model/game",
    )
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 V8 observation review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_precision_host_path_observation_review_contract() -> dict[str, Any]:
    reviewed = _validate_acceptance_cached()
    accepted = reviewed["accepted_observation"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "separate_review_instrument": True,
        "observation_source_identity_pinned_by_git_blob": True,
        "observation_source_identity_pinned_by_sha256": True,
        "observation_test_identity_pinned_by_git_blob": True,
        "observation_test_identity_pinned_by_sha256": True,
        "pair06_v8_precision_host_path_observation_reviewed": True,
        "pair_slot": 6,
        "held_out": False,
        "model_dir": accepted["model_dir"],
        "adapter_dir": accepted["adapter_dir"],
        "model_dir_candidate_count": 1,
        "adapter_dir_candidate_count": 1,
        "verified_asset_count": 17,
        "all_required_assets_exact_hash_verified": True,
        "host_asset_mutation": False,
        "model_dir_path_binding_eligible": True,
        "adapter_dir_path_binding_eligible": True,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_acceptance": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def bind_host_paths(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionHostPathObservationReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionHostPathObservationReviewHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
