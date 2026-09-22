"""Source-only review of the pair-03 candidate policy disposition.

This separate instrument pins the exact disposition source and tests, confirms
the non-decisive pair-03 evidence remains preserved, and advances only to a
source-only pair-09 evaluation-design gate.

It does not authorize pair-09 execution, held-out execution, replay, training,
promotion, deployment, VOID mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_policy_disposition_generation2
    as disposition,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-policy-disposition-source-binding-review-contract.v1"
)

DISPOSITION_GIT_BLOB = "de74c9107d29e8f415330b75e4b4cd2c1c288146"
DISPOSITION_SOURCE_SHA256 = (
    "1dbe6ed33d1f2946267173612e2f06355b83c8e338da612f8abce99fe5194f0a"
)
DISPOSITION_TEST_GIT_BLOB = "351c2a2f17db052bf51a46d3acb58a2551398bf2"
DISPOSITION_TEST_SHA256 = (
    "802f06ffa9bc9a95c00a676308a3c216ecaab1b583d5bd82c7b0dd0b683fd922"
)

NEXT_GATE = "V2R13_PAIR09_EVALUATION_DESIGN_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_evaluation_design"


class V2R13Pair03CandidatePolicyDispositionReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidatePolicyDispositionReviewHold(message)


@lru_cache(maxsize=1)
def _validate_disposition_cached() -> dict[str, Any]:
    contract = disposition.v2r13_pair03_candidate_policy_disposition_contract()

    _require(contract.get("pair_slot") == 3, "pair-slot drift")
    _require(contract.get("baseline_arm") == "baseline", "baseline arm drift")
    _require(contract.get("candidate_arm") == "candidate", "candidate arm drift")
    _require(contract.get("policy_disposition_made") is True, "policy disposition missing")
    _require(
        contract.get("policy_disposition")
        == "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION",
        "policy disposition drift",
    )
    _require(contract.get("pair03_measurement_conclusive") is False, "pair03 unexpectedly conclusive")
    _require(contract.get("candidate_preserved_as_evidence") is True, "candidate preservation missing")
    _require(contract.get("candidate_promoted") is False, "candidate unexpectedly promoted")
    _require(contract.get("candidate_rejected") is False, "candidate unexpectedly rejected")
    _require(contract.get("candidate_replay_permitted") is False, "candidate replay unexpectedly permitted")
    _require(
        contract.get("additional_bounded_evaluation_required") is True,
        "additional bounded evaluation requirement missing",
    )
    _require(
        contract.get("pair09_evaluation_design_required") is True,
        "pair09 design requirement missing",
    )
    _require(contract.get("pair09_execution_authorized") is False, "pair09 execution already authorized")
    _require(contract.get("held_out_execution_authorized") is False, "held-out execution already authorized")
    _require(contract.get("source_binding_reviewed") is False, "disposition unexpectedly self-reviewed")
    _require(
        contract.get("next_gate")
        == "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pre-review disposition frontier drift",
    )

    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        _require(contract.get(field) is False, f"disposition authority drift: {field}")

    return deepcopy(contract)


def v2r13_pair03_candidate_policy_disposition_review_contract() -> dict[str, Any]:
    reviewed = _validate_disposition_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "disposition_git_blob": DISPOSITION_GIT_BLOB,
        "disposition_source_sha256": DISPOSITION_SOURCE_SHA256,
        "disposition_test_git_blob": DISPOSITION_TEST_GIT_BLOB,
        "disposition_test_sha256": DISPOSITION_TEST_SHA256,
        "separate_review_instrument": True,
        "disposition_source_identity_pinned_by_git_blob": True,
        "disposition_source_identity_pinned_by_sha256": True,
        "disposition_test_identity_pinned_by_git_blob": True,
        "disposition_test_identity_pinned_by_sha256": True,
        "pair_slot": 3,
        "policy_disposition_reviewed": True,
        "policy_disposition": reviewed["policy_disposition"],
        "candidate_preserved_as_evidence": True,
        "candidate_promoted": False,
        "candidate_rejected": False,
        "candidate_replay_permitted": False,
        "additional_bounded_evaluation_required": True,
        "pair09_evaluation_design_required": True,
        "pair09_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "automatic_policy_promotion": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "reviewed_disposition": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_pair09_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidatePolicyDispositionReviewHold(
        "V2R13_PAIR09_EXECUTION_NOT_AUTHORIZED"
    )


def authorize_held_out_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidatePolicyDispositionReviewHold(
        "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidatePolicyDispositionReviewHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
