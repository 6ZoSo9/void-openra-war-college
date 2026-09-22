"""Source-only review of the V2R13 pair-09 candidate restricted Git backend."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_git_backend_generation2
    as backend,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-git-backend-review-contract.v1"
)

BACKEND_GIT_BLOB = "6cb3b780d9beab0dcaaacae4ccb3ffd24701489d"
BACKEND_SOURCE_SHA256 = (
    "ab76220fbca190e8b9ef25f4b8148187f6454d590ed73d53ecee609cb68fafee"
)
BACKEND_TEST_GIT_BLOB = "c703a89fd12d0b1ebd63a50a4e63e004fd2af6b4"
BACKEND_TEST_SHA256 = (
    "6faf828f1b7405786bfb907146c1eaf0b409ebaad4bf68dddeb5b75807afa00a"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_candidate_invocation"


class V2R13Pair09CandidateGitBackendReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateGitBackendReviewHold(message)


@lru_cache(maxsize=1)
def _validate_backend_cached() -> dict[str, Any]:
    contract = backend.pair09_candidate_git_backend_contract()
    _require(
        contract.get("pair09_candidate_git_backend_implemented") is True,
        "candidate Git backend missing",
    )
    _require(
        contract.get("pair09_candidate_git_backend_reviewed") is False,
        "candidate Git backend self-reviewed",
    )
    _require(contract.get("pair_slot") == 9, "candidate Git pair-slot drift")
    _require(contract.get("arm") == "candidate", "candidate Git arm drift")
    _require(contract.get("held_out") is False, "candidate Git held-out drift")
    _require(contract.get("binding_count") == 2, "candidate Git binding count drift")
    _require(
        contract.get("frozen_source_commit")
        == "973802ef0a614e5afa782ff20e231e18966ae3e5",
        "candidate frozen source drift",
    )
    _require(
        contract.get("frozen_engine_commit")
        == "1607a7a6501d42a47638393ecef8b22831064932",
        "candidate frozen engine drift",
    )
    for field in (
        "fetch_implemented",
        "canonical_checkout_implemented",
        "force_remove_implemented",
        "reset_implemented",
        "clean_implemented",
        "config_implemented",
        "prune_implemented",
        "runtime_execution_authorized",
        "runtime_execution_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(contract.get(field) is False, f"candidate Git boundary drift: {field}")
    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_GIT_BACKEND_SOURCE_BINDING_REVIEW_REQUIRED",
        "candidate Git review frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair09_candidate_git_backend_review_contract() -> dict[str, Any]:
    validated = _validate_backend_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "backend_git_blob": BACKEND_GIT_BLOB,
        "backend_source_sha256": BACKEND_SOURCE_SHA256,
        "backend_test_git_blob": BACKEND_TEST_GIT_BLOB,
        "backend_test_sha256": BACKEND_TEST_SHA256,
        "separate_review_instrument": True,
        "pair09_candidate_git_backend_reviewed": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "binding_count": 2,
        "restricted_git_worktree_backend_reviewed": True,
        "fetch_implemented": False,
        "canonical_checkout_implemented": False,
        "force_remove_implemented": False,
        "reset_implemented": False,
        "clean_implemented": False,
        "config_implemented": False,
        "prune_implemented": False,
        "runtime_execution_authorized": False,
        "runtime_execution_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "validated_backend": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateGitBackendReviewHold(
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
