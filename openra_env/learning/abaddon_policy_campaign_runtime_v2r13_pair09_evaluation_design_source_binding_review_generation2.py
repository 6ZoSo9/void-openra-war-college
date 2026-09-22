"""Source-only review of the bounded V2R13 pair-09 evaluation design.

This separate review pins the exact pair-09 design source and tests and confirms
that pair 09 is non-held-out, matched baseline/candidate, baseline-first, and
still non-executing. It advances only to source-only baseline preparation.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_evaluation_design_generation2
    as design,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-evaluation-design-source-binding-review-contract.v1"
)

DESIGN_GIT_BLOB = "3e110288a6f0e4f14fbe9e591e8d1840cb786975"
DESIGN_SOURCE_SHA256 = (
    "5690f1993fa7e2ea6cff28451c57bcbc725c57ae81450cc499839efea26f29bf"
)
DESIGN_TEST_GIT_BLOB = "272be1e4c070a721b56c287b7d3ecf7cc8a77511"
DESIGN_TEST_SHA256 = (
    "2dfbcc54f70aa6490843d3c42dda2efb2df5a4ef5e7ce20dc99c70e721280aa5"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_EXECUTION_PREPARATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_baseline_execution_preparation"


class V2R13Pair09EvaluationDesignReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09EvaluationDesignReviewHold(message)


@lru_cache(maxsize=1)
def _validate_design_cached() -> dict[str, Any]:
    contract = design.v2r13_pair09_evaluation_design_contract()

    _require(contract.get("pair09_evaluation_design_implemented") is True, "pair09 design missing")
    _require(contract.get("pair09_evaluation_design_reviewed") is False, "pair09 design self-reviewed")
    _require(contract.get("pair_slot") == 9, "pair09 slot drift")
    _require(tuple(contract.get("arms", ())) == ("baseline", "candidate"), "pair09 arm set drift")
    _require(contract.get("held_out") is False, "pair09 unexpectedly held-out")
    _require(contract.get("baseline_first") is True, "pair09 baseline-first requirement missing")
    _require(
        contract.get("baseline_must_complete_before_candidate") is True,
        "pair09 baseline completion ordering missing",
    )
    _require(
        contract.get("matched_pair_runner_argv_required") is True,
        "pair09 matched runner argv requirement missing",
    )
    _require(
        tuple(contract["baseline_command"]["runner_argv"])
        == tuple(contract["candidate_command"]["runner_argv"]),
        "pair09 runner argv mismatch",
    )
    _require(
        contract.get("candidate_policy_preserved_from_pair03") is True,
        "pair03 candidate preservation lost",
    )
    _require(contract.get("candidate_policy_promoted") is False, "candidate unexpectedly promoted")
    _require(contract.get("candidate_policy_rejected") is False, "candidate unexpectedly rejected")
    _require(
        contract.get("legacy_six_arm_authorization_sufficient_for_pair09") is False,
        "legacy broad authority became sufficient",
    )
    _require(
        contract.get("historical_bounded_executor_capability_reusable") is True,
        "bounded executor capability unexpectedly unavailable",
    )
    _require(contract.get("pair09_baseline_execution_authorized") is False, "pair09 baseline already authorized")
    _require(contract.get("pair09_candidate_execution_authorized") is False, "pair09 candidate already authorized")
    _require(contract.get("pair09_execution_performed") is False, "pair09 already executed")
    _require(contract.get("candidate_replay_permitted") is False, "pair03 candidate replay permitted")
    _require(contract.get("held_out_execution_authorized") is False, "held-out execution authorized")

    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair09 design authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_EVALUATION_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair09 design review frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair09_evaluation_design_review_contract() -> dict[str, Any]:
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
        "pair09_evaluation_design_reviewed": True,
        "pair_slot": 9,
        "arms": ("baseline", "candidate"),
        "held_out": False,
        "baseline_first": True,
        "baseline_must_complete_before_candidate": True,
        "matched_pair_runner_argv": tuple(reviewed["matched_pair_runner_argv"]),
        "candidate_policy_preserved_from_pair03": True,
        "candidate_policy_promoted": False,
        "candidate_policy_rejected": False,
        "pair09_baseline_execution_preparation_required": True,
        "pair09_baseline_execution_authorized": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_execution_performed": False,
        "candidate_replay_permitted": False,
        "held_out_execution_authorized": False,
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


def execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09EvaluationDesignReviewHold(
        "V2R13_PAIR09_BASELINE_EXECUTION_NOT_AUTHORIZED"
    )


def execute_pair09_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09EvaluationDesignReviewHold(
        "V2R13_PAIR09_CANDIDATE_EXECUTION_NOT_AUTHORIZED"
    )


def execute_held_out_pair(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09EvaluationDesignReviewHold(
        "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )
