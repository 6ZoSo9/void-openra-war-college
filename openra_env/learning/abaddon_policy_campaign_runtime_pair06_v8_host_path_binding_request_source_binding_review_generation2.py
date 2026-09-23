"""Source-only review of the pair-06 V8 host-path binding request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-host-path-binding-request-source-binding-review-contract.v1"
)

REQUEST_GIT_BLOB = "ea2b399f7c3fe26caca43524c0c5b79a638e92fa"
REQUEST_SOURCE_SHA256 = (
    "923bac4c770648d9d75c319cfd849845bf7f7159b0a533b3e9083ff46885769a"
)
REQUEST_TEST_GIT_BLOB = "22fd9fc5cb714e24a0d85b3f1df87a2b7ed685e4"
REQUEST_TEST_SHA256 = (
    "5a00f73719e22139e70c4912d8185c18cfe695f045fb438f879ea7583895db26"
)

NEXT_GATE = "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_precision_host_path_observation"


class Pair06V8HostPathBindingRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8HostPathBindingRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validate_request_cached() -> dict[str, Any]:
    contract = request.pair06_v8_host_path_binding_request_contract()

    _require(contract.get("pair_slot") == 6, "pair06 path request slot drift")
    _require(
        contract.get("host_path_binding_request_implemented") is True,
        "pair06 path request missing",
    )
    _require(
        contract.get("host_path_binding_request_reviewed") is False,
        "pair06 path request unexpectedly self-reviewed",
    )
    _require(
        contract.get("precision_host_observation_required") is True,
        "Precision observation requirement missing",
    )
    _require(
        contract.get("host_observation_performed") is False,
        "host observation already performed",
    )
    _require(
        contract.get("filesystem_scan_performed_by_contract") is False,
        "contract unexpectedly scans filesystem",
    )
    _require(
        contract.get("model_dir_path_bound") is False
        and contract.get("adapter_dir_path_bound") is False,
        "V8 host paths already bound",
    )
    _require(
        contract.get("model_dir_candidate_count") == 0
        and contract.get("adapter_dir_candidate_count") == 0,
        "host path candidates unexpectedly present",
    )
    _require(
        contract.get("required_model_asset_count") == 12,
        "model asset count drift",
    )
    _require(
        contract.get("required_adapter_asset_count") == 5,
        "adapter asset count drift",
    )
    _require(
        contract.get("required_asset_count") == 17,
        "asset manifest cardinality drift",
    )
    manifest = contract.get("required_asset_manifest")
    _require(
        isinstance(manifest, tuple) and len(manifest) == 17,
        "asset manifest shape drift",
    )
    _require(
        contract.get("exact_hash_match_required_for_every_asset") is True,
        "exact-hash requirement missing",
    )
    _require(
        contract.get("model_and_adapter_directories_must_be_distinct") is True,
        "model/adapter distinct-directory requirement missing",
    )
    _require(
        contract.get("symlinked_required_files_allowed") is False,
        "symlinked required files unexpectedly allowed",
    )

    for field in (
        "runtime_load_authorized",
        "runtime_load_performed",
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"path request authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED",
        "path request frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_host_path_binding_request_review_contract() -> dict[str, Any]:
    reviewed = _validate_request_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "separate_review_instrument": True,
        "request_source_identity_pinned_by_git_blob": True,
        "request_source_identity_pinned_by_sha256": True,
        "request_test_identity_pinned_by_git_blob": True,
        "request_test_identity_pinned_by_sha256": True,
        "pair06_v8_host_path_binding_request_reviewed": True,
        "pair_slot": 6,
        "precision_host_observation_required": True,
        "host_observation_performed": False,
        "model_dir_path_bound": False,
        "adapter_dir_path_bound": False,
        "required_asset_count": 17,
        "required_asset_manifest": deepcopy(reviewed["required_asset_manifest"]),
        "exact_hash_match_required_for_every_asset": True,
        "model_and_adapter_directories_must_be_distinct": True,
        "symlinked_required_files_allowed": False,
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
        "reviewed_request": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_precision_host(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingRequestReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8HostPathBindingRequestReviewHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
