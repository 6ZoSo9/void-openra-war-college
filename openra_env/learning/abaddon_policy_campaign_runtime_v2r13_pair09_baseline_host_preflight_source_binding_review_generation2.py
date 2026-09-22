"""Source-only review of the V2R13 pair-09 baseline host preflight."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_generation2
    as preflight,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-host-preflight-source-binding-review-contract.v1"
)

PREFLIGHT_GIT_BLOB = "fc40d30be98db04fa783ab0534e8ab8eb869ce2d"
PREFLIGHT_SOURCE_SHA256 = (
    "a8d0a9ff633a88bde75bd166e8d750756344b2e52f769667246a6c8817675244"
)
PREFLIGHT_TEST_GIT_BLOB = "fc505322b7f05c3150442e9192189eadde6db1a3"
PREFLIGHT_TEST_SHA256 = (
    "e06f3d21f574d83a41191cf8b282059ea57aadc189ebbefcbbbf0f24d43dc7be"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_baseline_invocation_implementation"


class V2R13Pair09BaselineHostPreflightReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineHostPreflightReviewHold(message)


@lru_cache(maxsize=1)
def _validate_preflight_cached() -> dict[str, Any]:
    contract = preflight.pair09_baseline_host_preflight_contract()

    _require(contract.get("pair_slot") == 9, "preflight pair-slot drift")
    _require(contract.get("arm") == "baseline", "preflight arm drift")
    _require(contract.get("held_out") is False, "preflight held-out drift")
    _require(
        contract.get("read_only_host_collection_implemented") is True,
        "read-only host collection missing",
    )
    _require(
        contract.get("pair03_baseline_preservation_required") is True,
        "pair03 baseline preservation requirement missing",
    )
    _require(
        contract.get("pair03_candidate_preservation_required") is True,
        "pair03 candidate preservation requirement missing",
    )
    _require(
        contract.get("pair09_baseline_absence_required") is True,
        "pair09 baseline absence requirement missing",
    )
    _require(
        contract.get("pair09_candidate_absence_required") is True,
        "pair09 candidate absence requirement missing",
    )
    _require(
        contract.get("held_out_pair15_absence_required") is True,
        "pair15 absence requirement missing",
    )
    _require(
        contract.get("legacy_structural_projection_is_host_observation") is False,
        "legacy projection mislabeled as host observation",
    )
    _require(
        contract.get("legacy_runtime_authority_inherited") is False,
        "legacy runtime authority inherited",
    )
    _require(
        contract.get("single_use_attempt_consumed") is False,
        "preflight consumed attempt",
    )
    _require(
        contract.get("pair09_baseline_execution_authorized") is False,
        "preflight authorized pair09 baseline",
    )
    _require(
        contract.get("pair09_baseline_execution_performed") is False,
        "preflight executed pair09 baseline",
    )
    _require(contract.get("runtime_started") is False, "preflight started runtime")

    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"preflight authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_BASELINE_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED",
        "preflight source-review frontier drift",
    )

    return deepcopy(contract)


def v2r13_pair09_baseline_host_preflight_review_contract() -> dict[str, Any]:
    validated = _validate_preflight_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "preflight_git_blob": PREFLIGHT_GIT_BLOB,
        "preflight_source_sha256": PREFLIGHT_SOURCE_SHA256,
        "preflight_test_git_blob": PREFLIGHT_TEST_GIT_BLOB,
        "preflight_test_sha256": PREFLIGHT_TEST_SHA256,
        "separate_review_instrument": True,
        "pair09_baseline_host_preflight_reviewed": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "read_only_host_collection_reviewed": True,
        "pair03_baseline_preservation_reviewed": True,
        "pair03_candidate_preservation_reviewed": True,
        "pair09_baseline_absence_reviewed": True,
        "pair09_candidate_absence_reviewed": True,
        "held_out_pair15_absence_reviewed": True,
        "legacy_structural_projection_is_host_observation": False,
        "legacy_runtime_authority_inherited": False,
        "single_use_attempt_consumed": False,
        "pair09_baseline_specific_authorization_accepted": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "pair09_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_preflight": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineHostPreflightReviewHold(
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
