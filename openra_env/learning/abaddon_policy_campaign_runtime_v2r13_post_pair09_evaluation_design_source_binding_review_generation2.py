"""Source-only review of the post-pair-09 non-held-out evaluation design."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_post_pair09_evaluation_design_generation2
    as design,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-post-pair09-evaluation-design-source-binding-review-contract.v1"
)

DESIGN_GIT_BLOB = "36c618c2172993b0ce8bf0b0c4e5af7677e5f81c"
DESIGN_SOURCE_SHA256 = (
    "6255385bd6a65d044fa2a2c4cb7a3370a47dead3c918ed40287a95107969a2e4"
)
DESIGN_TEST_GIT_BLOB = "169fe65510dd9a698b88fc542fd67fba6953c24e"
DESIGN_TEST_SHA256 = (
    "92b29523d46da66dafaf78aa68416f9cb3cb2ebaa36a947b646c1dd443f93869"
)

NEXT_GATE = "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_new_nonheldout_evaluation_allocation"


class V2R13PostPair09EvaluationDesignReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13PostPair09EvaluationDesignReviewHold(message)


@lru_cache(maxsize=1)
def _validate_design_cached() -> dict[str, Any]:
    contract = design.v2r13_post_pair09_evaluation_design_contract()

    _require(
        contract.get("post_pair09_evaluation_design_implemented") is True,
        "post-pair09 design missing",
    )
    _require(
        contract.get("post_pair09_evaluation_design_reviewed") is False,
        "post-pair09 design unexpectedly self-reviewed",
    )
    _require(
        tuple(contract.get("authorized_pair_slots", ())) == (3, 9, 15),
        "authorized pair-slot set drift",
    )
    _require(
        tuple(contract.get("held_out_pair_slots", ())) == (15,),
        "held-out pair-slot set drift",
    )
    _require(
        tuple(contract.get("nonheldout_pair_slots", ())) == (3, 9),
        "non-held-out pair-slot set drift",
    )
    _require(
        tuple(contract.get("completed_nondecisive_nonheldout_pair_slots", ()))
        == (3, 9),
        "completed non-held-out evidence set drift",
    )
    _require(
        contract.get("existing_nonheldout_capacity_exhausted") is True,
        "non-held-out capacity not exhausted",
    )
    _require(
        contract.get("held_out_pair15_preserved") is True,
        "pair15 held-out preservation missing",
    )
    _require(
        contract.get("held_out_contamination_prohibited") is True,
        "held-out contamination prohibition missing",
    )
    _require(
        contract.get("held_out_use_as_tuning_tiebreaker_allowed") is False,
        "pair15 became a tuning tie-breaker",
    )
    _require(
        contract.get("new_nonheldout_evaluation_allocation_required") is True,
        "new non-held-out allocation not required",
    )
    _require(
        contract.get("new_nonheldout_execution_authorized") is False,
        "new non-held-out execution prematurely authorized",
    )
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution prematurely authorized",
    )
    _require(
        contract.get("pair15_execution_performed") is False,
        "pair15 execution already performed",
    )
    _require(
        contract.get("pair03_replay_authorized") is False,
        "pair03 replay authorized",
    )
    _require(
        contract.get("pair09_replay_authorized") is False,
        "pair09 replay authorized",
    )
    _require(contract.get("candidate_promoted") is False, "candidate promoted")
    _require(contract.get("candidate_rejected") is False, "candidate rejected")
    _require(
        contract.get("next_gate")
        == "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED",
        "post-pair09 design frontier drift",
    )

    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"post-pair09 authority drift: {field}")

    return deepcopy(contract)


def v2r13_post_pair09_evaluation_design_review_contract() -> dict[str, Any]:
    reviewed = _validate_design_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "design_git_blob": DESIGN_GIT_BLOB,
        "design_source_sha256": DESIGN_SOURCE_SHA256,
        "design_test_git_blob": DESIGN_TEST_GIT_BLOB,
        "design_test_sha256": DESIGN_TEST_SHA256,
        "separate_review_instrument": True,
        "design_source_identity_pinned_by_git_blob": True,
        "design_source_identity_pinned_by_sha256": True,
        "design_test_identity_pinned_by_git_blob": True,
        "design_test_identity_pinned_by_sha256": True,
        "post_pair09_evaluation_design_reviewed": True,
        "authorized_pair_slots": (3, 9, 15),
        "held_out_pair_slots": (15,),
        "nonheldout_pair_slots": (3, 9),
        "existing_nonheldout_capacity_exhausted": True,
        "held_out_pair15_preserved": True,
        "held_out_contamination_prohibited": True,
        "held_out_use_as_tuning_tiebreaker_allowed": False,
        "new_nonheldout_evaluation_allocation_required": True,
        "new_nonheldout_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair15_execution_performed": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "candidate_promoted": False,
        "candidate_rejected": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_design": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_pair15(*args: Any, **kwargs: Any) -> None:
    raise V2R13PostPair09EvaluationDesignReviewHold(
        "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def replay_existing_pair(*args: Any, **kwargs: Any) -> None:
    raise V2R13PostPair09EvaluationDesignReviewHold(
        "V2R13_EXISTING_PAIR_REPLAY_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13PostPair09EvaluationDesignReviewHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
