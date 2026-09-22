"""Source-only review of the V2R13 pair-09 candidate host preflight."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_host_preflight_generation2
    as preflight,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-host-preflight-review-contract.v1"
)

PREFLIGHT_GIT_BLOB = "1cc236ac9706fef4731d3335d5ba53cd181c38c3"
PREFLIGHT_SOURCE_SHA256 = (
    "17a38abe77b3c06fb178ad641ba59bf3b319485df6aa3c17202ddc39006462e8"
)
PREFLIGHT_TEST_GIT_BLOB = "fba24796ecc7ddec730625eadb8bd61dc29c4d85"
PREFLIGHT_TEST_SHA256 = (
    "19f301b07489e949888976363a3168497942b41cfa4c2a110a82db3b061fea5d"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_GIT_BACKEND_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_git_backend"


class V2R13Pair09CandidateHostPreflightReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateHostPreflightReviewHold(message)


@lru_cache(maxsize=1)
def _validate_preflight_cached() -> dict[str, Any]:
    contract = preflight.pair09_candidate_host_preflight_contract()
    _require(
        contract.get("pair09_candidate_host_preflight_implemented") is True,
        "candidate preflight missing",
    )
    _require(
        contract.get("pair09_candidate_host_preflight_reviewed") is False,
        "candidate preflight self-reviewed",
    )
    _require(
        contract.get("read_only_host_collection") is True,
        "candidate preflight not read-only",
    )
    _require(contract.get("pair_slot") == 9, "candidate preflight pair-slot drift")
    _require(contract.get("arm") == "candidate", "candidate preflight arm drift")
    _require(contract.get("held_out") is False, "candidate preflight held-out drift")
    for field in (
        "pair03_baseline_preservation_required",
        "pair03_candidate_preservation_required",
        "pair09_baseline_preservation_required",
        "pair09_candidate_absence_required",
        "held_out_pair15_absence_required",
    ):
        _require(contract.get(field) is True, f"candidate preflight requirement missing: {field}")
    for field in (
        "single_use_attempt_consumed",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "legacy_runtime_authority_inherited",
        "runtime_started",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(contract.get(field) is False, f"candidate preflight boundary drift: {field}")
    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED",
        "candidate preflight review frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair09_candidate_host_preflight_review_contract() -> dict[str, Any]:
    validated = _validate_preflight_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "preflight_git_blob": PREFLIGHT_GIT_BLOB,
        "preflight_source_sha256": PREFLIGHT_SOURCE_SHA256,
        "preflight_test_git_blob": PREFLIGHT_TEST_GIT_BLOB,
        "preflight_test_sha256": PREFLIGHT_TEST_SHA256,
        "separate_review_instrument": True,
        "pair09_candidate_host_preflight_reviewed": True,
        "read_only_host_collection_reviewed": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "pair03_baseline_preservation_reviewed": True,
        "pair03_candidate_preservation_reviewed": True,
        "pair09_baseline_preservation_reviewed": True,
        "pair09_candidate_absence_reviewed": True,
        "held_out_pair15_absence_reviewed": True,
        "preserved_evidence_count": len(preflight.PRESERVED_FILES),
        "legacy_runtime_authority_inherited": False,
        "single_use_attempt_consumed": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_candidate_execution_performed": False,
        "runtime_started": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "validated_preflight": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateHostPreflightReviewHold(
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
