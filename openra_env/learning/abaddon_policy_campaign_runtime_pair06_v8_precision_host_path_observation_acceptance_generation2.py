"""Source-only acceptance of exact Precision pair-06 V8 host-path evidence.

The evidence was produced by a bounded read-only observer pinned to canonical
main. It discovered exactly one accepted base-model directory and one accepted
adapter directory under the known V8 work root, then re-ran the accepted V8
17-file asset verifier without loading model weights or executing inference.

Importing or inspecting this source performs no filesystem scan, model load,
inference, game execution, training, promotion, deployment, VOID-chain
mutation, or wallet/funds action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-host-path-observation-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-host-path-observation-acceptance.v1"
)

REQUEST_REVIEW_GIT_BLOB = "ac37557e7231c684d82a0a369bb4c3dabaa7c7d2"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "32284d5301e9591af85b8f972bb076cecb625f549f6cc9aac8b1f2680ee91240"
)

OBSERVER_SHA256 = (
    "033f3ded80191902d74687c5f12a5f03e9f12d956a7c293ee706999acdf59c18"
)
CANONICAL_MAIN_HEAD = "4f83631e70fdc96c27c8bb9b6e976c161be57606"
WORK_ROOT = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
MODEL_DIR = WORK_ROOT + "/model"
ADAPTER_DIR = WORK_ROOT + "/adapter-v8"

EXPECTED_EVIDENCE = {
    "observer_sha256": OBSERVER_SHA256,
    "canonical_main_head": CANONICAL_MAIN_HEAD,
    "pair_slot": 6,
    "arm_scope": ("baseline", "candidate"),
    "held_out": False,
    "work_root": WORK_ROOT,
    "search_scope": "bounded_known_v8_work_root",
    "filesystem_scan_read_only": True,
    "host_asset_mutation": False,
    "model_dir_candidate_count": 1,
    "adapter_dir_candidate_count": 1,
    "model_dir": MODEL_DIR,
    "adapter_dir": ADAPTER_DIR,
    "accepted_v8_asset_verifier_green": True,
    "verified_asset_count": 17,
    "runtime_execution_performed": False,
    "model_execution_performed": False,
    "model_load": False,
    "model_weights_loaded": False,
    "model_inference": False,
    "game_execution": False,
    "training": False,
    "weights_updated": False,
    "policy_promotion": False,
    "deployment": False,
    "void_chain_mutation": False,
    "wallet_or_funds_action": False,
    "pair15_execution": False,
    "observation_result_ready_for_source_acceptance": True,
}

NEXT_GATE = "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_precision_host_path_observation_source_binding_review"
)


class Pair06V8PrecisionHostPathObservationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PrecisionHostPathObservationAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def _validate_request_review() -> dict[str, Any]:
    reviewed = request_review.pair06_v8_host_path_binding_request_review_contract()
    _require(
        reviewed.get("pair06_v8_host_path_binding_request_reviewed") is True,
        "pair06 V8 host-path request not reviewed",
    )
    _require(reviewed.get("pair_slot") == 6, "pair06 host-path request slot drift")
    _require(
        reviewed.get("precision_host_observation_required") is True,
        "Precision host observation no longer required",
    )
    _require(
        reviewed.get("host_observation_performed") is False,
        "source request unexpectedly records host observation",
    )
    _require(
        reviewed.get("model_dir_path_bound") is False
        and reviewed.get("adapter_dir_path_bound") is False,
        "source request unexpectedly binds host paths",
    )
    _require(
        reviewed.get("required_asset_count") == 17,
        "pair06 V8 required asset count drift",
    )
    _require(
        reviewed.get("exact_hash_match_required_for_every_asset") is True,
        "pair06 V8 exact-hash requirement missing",
    )
    _require(
        reviewed.get("runtime_load_authorized") is False
        and reviewed.get("runtime_load_performed") is False,
        "pair06 V8 runtime load unexpectedly authorized/performed",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_PRECISION_HOST_PATH_OBSERVATION_REQUIRED",
        "pair06 V8 host-observation frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair06_v8_precision_host_path_observation(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    reviewed = _validate_request_review()
    _require(isinstance(evidence, Mapping), "pair06 V8 observation evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair06 V8 observation evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair06 V8 observation evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair06 V8 observation evidence digest drift",
    )
    _require(MODEL_DIR != ADAPTER_DIR, "model/adapter observation paths not distinct")
    _require(MODEL_DIR.startswith(WORK_ROOT + "/"), "model dir escaped bounded work root")
    _require(ADAPTER_DIR.startswith(WORK_ROOT + "/"), "adapter dir escaped bounded work root")

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_precision_host_path_observation_accepted": True,
        "accepted_evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "canonical_main_head": CANONICAL_MAIN_HEAD,
        "pair_slot": 6,
        "held_out": False,
        "work_root": WORK_ROOT,
        "model_dir": MODEL_DIR,
        "adapter_dir": ADAPTER_DIR,
        "model_dir_candidate_count": 1,
        "adapter_dir_candidate_count": 1,
        "verified_asset_count": 17,
        "all_required_assets_exact_hash_verified": True,
        "host_observation_completed": True,
        "host_observation_green": True,
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
        "reviewed_request": reviewed,
        "accepted_evidence": deepcopy(supplied),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def pair06_v8_precision_host_path_observation_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_precision_host_path_observation(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "pair06_v8_precision_host_path_observation_accepted": True,
        "accepted_evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "model_dir": MODEL_DIR,
        "adapter_dir": ADAPTER_DIR,
        "verified_asset_count": 17,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_observation": accepted,
    }


def bind_host_paths(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionHostPathObservationAcceptanceHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionHostPathObservationAcceptanceHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
