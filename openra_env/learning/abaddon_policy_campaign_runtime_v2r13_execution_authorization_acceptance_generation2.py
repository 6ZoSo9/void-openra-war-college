"""Source-only V2R13 runtime-execution authorization acceptance."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_isolated_workdir_allocator_source_binding_review_generation2
    as allocator_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_current_main_preload_live_readiness_evidence_acceptance_generation2
    as readiness_acceptance,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-execution-authorization-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-execution-authorization-acceptance.v1"
)

READINESS_ACCEPTANCE_GIT_BLOB = "5986293833ebf710aee8cbdae0a18edadf21e4b6"
READINESS_ACCEPTANCE_SOURCE_SHA256 = (
    "a91350385ede0e3e6575cbf81fbacf88bc336bd0ea3d37b86035d46d442b0778"
)
ALLOCATOR_REVIEW_GIT_BLOB = "a1fb192ce13030f814da74d12bc930968e77d765"
ALLOCATOR_REVIEW_SOURCE_SHA256 = (
    "3985b0fbc74a25e29d44ae09d9c52c051ebb9044058d1bdd93ba6c9d1cca5761"
)
ACCEPTED_READINESS_EVIDENCE_SHA256 = (
    "ee5c9c555323fc0a0b6550953700ec033ad2f4bb9d8b8763c5f59bfdb9bf91d2"
)

AUTHORIZATION_SCOPE = "v2r13_lane_only"
AUTHORIZED_PAIR_SLOTS = (3, 9, 15)
AUTHORIZED_ARMS = ("baseline", "candidate")
AUTHORIZED_EXECUTION_ARM_COUNT = 6

AUTHORIZATION_ATTESTATION = {
    "authorization_basis": "explicit_operator_authorization_in_control_session",
    "authorization_date": "2026-09-18",
    "authorization_granted": True,
    "authorization_scope": AUTHORIZATION_SCOPE,
    "authorized_arms": AUTHORIZED_ARMS,
    "authorized_execution_arm_count": AUTHORIZED_EXECUTION_ARM_COUNT,
    "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
    "authorized_runtime_selection_key": V2R13,
    "cryptographic_operator_signature_present": False,
    "repository_attestation_is_cryptographic_proof": False,
    "revocation_check_required_before_each_execution": True,
    "runtime_readiness_revalidation_required_before_each_execution": True,
    "training_authorized": False,
    "weights_update_authorized": False,
    "automatic_policy_promotion_authorized": False,
    "deployment_authorized": False,
    "void_chain_mutation_authorized": False,
    "wallet_or_funds_action_authorized": False,
}

NEXT_GATE = "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "v2r13_bounded_runtime_execution_implementation"


class V2R13RuntimeExecutionAuthorizationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13RuntimeExecutionAuthorizationHold(message)


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


AUTHORIZATION_ATTESTATION_SHA256 = (
    "34ad7143e876b91056f730de37ab470b6fd8a5f99d84aadefb178cabf87a2031"
)
_require(
    _digest(AUTHORIZATION_ATTESTATION) == AUTHORIZATION_ATTESTATION_SHA256,
    "embedded authorization attestation digest drift",
)


def _validate_dependencies() -> dict[str, Any]:
    readiness = (
        readiness_acceptance
        .current_main_v2r13_live_readiness_evidence_acceptance_contract()
    )
    review = allocator_review.isolated_workdir_allocator_source_binding_review()

    _require(
        readiness.get("current_main_preload_live_readiness_evidence_accepted") is True,
        "V2R13 current-main readiness acceptance missing",
    )
    _require(
        readiness.get("accepted_evidence_sha256")
        == ACCEPTED_READINESS_EVIDENCE_SHA256,
        "V2R13 accepted readiness evidence identity drift",
    )
    _require(
        readiness.get("runtime_readiness_admitted") is True,
        "V2R13 runtime readiness is not admitted",
    )
    _require(
        readiness.get("runtime_execution_authorization_scope") == AUTHORIZATION_SCOPE,
        "V2R13 readiness authorization scope drift",
    )
    _require(
        readiness.get("other_runtime_lanes_readiness_implied") is False,
        "V2R13 readiness unexpectedly implies other runtime lanes",
    )
    _require(
        readiness.get("next_gate") == "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "V2R13 readiness next-gate drift",
    )
    _require(
        readiness.get("runtime_execution_authorized") is False,
        "V2R13 readiness source unexpectedly self-authorizes execution",
    )
    _require(
        readiness.get("runtime_execution_performed") is False,
        "V2R13 readiness source unexpectedly executes runtime",
    )

    _require(review.get("source_frontier_closed") is True, "execution source frontier reopened")
    _require(
        tuple(review.get("execution_materialization_source_blockers", ())) == (),
        "execution source blockers reappeared",
    )
    _require(
        tuple(review.get("execution_materialization_blockers", ()))
        == ("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",),
        "execution blocker frontier drift",
    )
    _require(
        review.get("runtime_execution_authorized") is False,
        "allocator review unexpectedly self-authorizes execution",
    )

    dependencies = review.get("dependencies")
    _require(isinstance(dependencies, Mapping), "allocator review dependencies missing")
    allocations = dependencies.get("allocations")
    _require(isinstance(allocations, list), "allocator review allocation ledger missing")

    v2r13_allocations = [
        deepcopy(row)
        for row in allocations
        if isinstance(row, Mapping) and row.get("runtime_selection_key") == V2R13
    ]
    _require(
        len(v2r13_allocations) == AUTHORIZED_EXECUTION_ARM_COUNT,
        "V2R13 allocation cardinality drift",
    )

    by_pair: dict[int, set[str]] = {}
    for row in v2r13_allocations:
        pair_slot = row.get("pair_slot")
        arm = row.get("arm")
        _require(pair_slot in AUTHORIZED_PAIR_SLOTS, "unexpected V2R13 pair slot")
        _require(arm in AUTHORIZED_ARMS, "unexpected V2R13 arm")
        by_pair.setdefault(int(pair_slot), set()).add(str(arm))
        _require(
            tuple(row.get("remaining_blockers", ()))
            == ("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",),
            "V2R13 allocation blocker drift",
        )
        _require(
            tuple(row.get("remaining_source_blockers", ())) == (),
            "V2R13 allocation source blocker drift",
        )
        _require(
            row.get("runtime_execution_authorized") is False,
            "pre-authorization allocation unexpectedly executable",
        )
        _require(
            row.get("runtime_started") is False,
            "pre-authorization allocation unexpectedly starts runtime",
        )
        _require(
            row.get("command_execution_performed") is False,
            "pre-authorization allocation unexpectedly executes command",
        )

    _require(
        set(by_pair) == set(AUTHORIZED_PAIR_SLOTS),
        "V2R13 pair-slot set drift",
    )
    for pair_slot, arms in by_pair.items():
        _require(
            arms == set(AUTHORIZED_ARMS),
            f"V2R13 matched-pair arm drift: {pair_slot}",
        )

    return {
        "readiness_acceptance": deepcopy(readiness),
        "allocator_review": deepcopy(review),
        "v2r13_allocations": v2r13_allocations,
    }


def _validate_authorization(value: Mapping[str, Any]) -> dict[str, Any]:
    _require(isinstance(value, Mapping), "authorization must be object")
    supplied = dict(value)
    _require(
        set(supplied) == set(AUTHORIZATION_ATTESTATION),
        "authorization field-set drift",
    )
    for field, expected in AUTHORIZATION_ATTESTATION.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"authorization drift: {field}",
        )
    _require(
        _digest(supplied) == AUTHORIZATION_ATTESTATION_SHA256,
        "authorization attestation digest drift",
    )
    return deepcopy(supplied)


def _authorized_allocation(row: Mapping[str, Any]) -> dict[str, Any]:
    copied = deepcopy(dict(row))
    copied["runtime_execution_authorized"] = True
    copied["authorization_scope"] = AUTHORIZATION_SCOPE
    copied["authorization_attestation_sha256"] = AUTHORIZATION_ATTESTATION_SHA256
    copied["remaining_blockers"] = (NEXT_GATE,)
    copied["runtime_started"] = False
    copied["command_execution_performed"] = False
    copied["model_inference_performed"] = False
    copied["game_execution_performed"] = False
    copied["training_performed"] = False
    copied["weights_updated"] = False
    copied["deployment_performed"] = False
    copied["void_chain_mutation_performed"] = False
    copied["wallet_or_funds_action_performed"] = False
    return copied


def accept_v2r13_runtime_execution_authorization(
    authorization: Mapping[str, Any],
) -> dict[str, Any]:
    """Accept exact external authorization without performing execution."""
    dependencies = _validate_dependencies()
    accepted = _validate_authorization(authorization)
    authorized_allocations = [
        _authorized_allocation(row) for row in dependencies["v2r13_allocations"]
    ]

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "authorization_accepted": True,
        "authorization": accepted,
        "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "authorized_runtime_selection_key": V2R13,
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "authorized_execution_arm_count": len(authorized_allocations),
        "runtime_execution_authorized": True,
        "other_runtime_lanes_authorized": False,
        "fresh_runtime_readiness_required_before_each_execution": True,
        "revocation_check_required_before_each_execution": True,
        "runtime_execution_implemented": False,
        "runtime_execution_performed": False,
        "runtime_started": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "authorized_allocations": authorized_allocations,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def v2r13_runtime_execution_authorization_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    accepted = accept_v2r13_runtime_execution_authorization(
        AUTHORIZATION_ATTESTATION
    )
    return {
        "schema": CONTRACT_SCHEMA,
        "readiness_acceptance_git_blob": READINESS_ACCEPTANCE_GIT_BLOB,
        "readiness_acceptance_source_sha256": READINESS_ACCEPTANCE_SOURCE_SHA256,
        "allocator_review_git_blob": ALLOCATOR_REVIEW_GIT_BLOB,
        "allocator_review_source_sha256": ALLOCATOR_REVIEW_SOURCE_SHA256,
        "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
        "authorization_repository_attestation": True,
        "authorization_cryptographic_proof": False,
        "authorization_accepted": True,
        "authorization_scope": AUTHORIZATION_SCOPE,
        "authorized_runtime_selection_key": V2R13,
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "authorized_execution_arm_count": AUTHORIZED_EXECUTION_ARM_COUNT,
        "runtime_execution_authorized": True,
        "other_runtime_lanes_authorized": False,
        "fresh_runtime_readiness_required_before_each_execution": True,
        "revocation_check_required_before_each_execution": True,
        "runtime_execution_implemented": False,
        "runtime_execution_performed": False,
        "runtime_started": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "source_frontier_closed_before_authorization": True,
        "authorized_allocations": deepcopy(accepted["authorized_allocations"]),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def execute_authorized_v2r13_runtime(*args: Any, **kwargs: Any) -> None:
    raise V2R13RuntimeExecutionAuthorizationHold(NEXT_GATE)


def authorize_other_runtime_lane(*args: Any, **kwargs: Any) -> None:
    raise V2R13RuntimeExecutionAuthorizationHold(
        "AUTHORIZATION_SCOPE_V2R13_ONLY"
    )
