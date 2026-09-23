"""Source-only review of the V2R13 pair-09 candidate policy disposition.

This separate instrument pins the exact pair-09 disposition source and tests,
confirms the mixed pair-09 evidence remains preserved, and advances only to a
post-pair-09 source-only evaluation-design gate.

It does not authorize candidate replay, held-out execution, training, promotion,
deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_policy_disposition_generation2
    as disposition,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-policy-disposition-source-binding-review-contract.v1"
)

DISPOSITION_GIT_BLOB = "ed5a241c847d73da3669e00348b29bbed686b712"
DISPOSITION_SOURCE_SHA256 = (
    "47924e98b89eff71973b55a9f474a348da77f2d8e3797654e53c7727b5f13124"
)
DISPOSITION_TEST_GIT_BLOB = "820157b51efa13673e3f051d419b86f843ea4a97"
DISPOSITION_TEST_SHA256 = (
    "37b1d77f4ef46cd33c6e8db48ad7b9628a6af3bcda5693e1f5f0ef9f610cba68"
)

NEXT_GATE = "V2R13_POST_PAIR09_EVALUATION_DESIGN_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_post_pair09_evaluation_design"


class V2R13Pair09CandidatePolicyDispositionReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidatePolicyDispositionReviewHold(message)


@lru_cache(maxsize=1)
def _validate_disposition_cached() -> dict[str, Any]:
    contract = disposition.v2r13_pair09_candidate_policy_disposition_contract()

    _require(contract.get("pair_slot") == 9, "pair-slot drift")
    _require(contract.get("baseline_arm") == "baseline", "baseline arm drift")
    _require(contract.get("candidate_arm") == "candidate", "candidate arm drift")
    _require(contract.get("policy_disposition_made") is True, "policy disposition missing")
    _require(
        contract.get("policy_disposition")
        == "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION",
        "policy disposition drift",
    )
    _require(
        contract.get("pair09_measurement_conclusive") is False,
        "pair09 unexpectedly conclusive",
    )
    _require(
        contract.get("candidate_preserved_as_evidence") is True,
        "candidate preservation missing",
    )
    _require(contract.get("candidate_promoted") is False, "candidate unexpectedly promoted")
    _require(contract.get("candidate_rejected") is False, "candidate unexpectedly rejected")
    _require(
        contract.get("candidate_replay_permitted") is False,
        "candidate replay unexpectedly permitted",
    )
    _require(
        contract.get("another_candidate_execution_authorized") is False,
        "another candidate execution unexpectedly authorized",
    )
    _require(
        contract.get("additional_bounded_evaluation_required") is True,
        "additional bounded evaluation requirement missing",
    )
    _require(
        contract.get("post_pair09_evaluation_design_required") is True,
        "post-pair09 design requirement missing",
    )
    _require(
        contract.get("held_out_execution_authorized") is False,
        "held-out execution already authorized",
    )
    _require(
        contract.get("held_out_execution_performed") is False,
        "held-out execution already performed",
    )
    _require(
        contract.get("source_binding_reviewed") is False,
        "disposition unexpectedly self-reviewed",
    )
    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED",
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


def v2r13_pair09_candidate_policy_disposition_review_contract() -> dict[str, Any]:
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
        "pair_slot": 9,
        "policy_disposition_reviewed": True,
        "policy_disposition": reviewed["policy_disposition"],
        "candidate_preserved_as_evidence": True,
        "candidate_promoted": False,
        "candidate_rejected": False,
        "candidate_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "additional_bounded_evaluation_required": True,
        "post_pair09_evaluation_design_required": True,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
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


def authorize_held_out_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidatePolicyDispositionReviewHold(
        "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def replay_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidatePolicyDispositionReviewHold(
        "V2R13_PAIR09_CANDIDATE_REPLAY_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidatePolicyDispositionReviewHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
