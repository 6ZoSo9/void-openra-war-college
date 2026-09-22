"""Source-only review of the V2R13 pair-09 baseline Git backend."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_git_backend_generation2
    as backend,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_source_binding_review_generation2
    as preflight_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-git-backend-source-binding-review-contract.v1"
)

BACKEND_GIT_BLOB = "9be2736081b67895faa9ecb5c4d978445a9f4a32"
BACKEND_SOURCE_SHA256 = (
    "32eb8b36a0f6e13ae710b63a0d40601595a52b9134766a2b414fdf7f12334647"
)
BACKEND_TEST_GIT_BLOB = "38acffa3b1a766dfcd611a7702526aed0c5e6eb6"
BACKEND_TEST_SHA256 = (
    "adc4d4c64f50ba98ca7d45bbce094e035465c1cefd5de96c1eb43cb279a67c55"
)
PREFLIGHT_REVIEW_GIT_BLOB = "01f95aee884a699b3e46472c3a12bfbfb0c3332d"
PREFLIGHT_REVIEW_SOURCE_SHA256 = (
    "8410d052bf15b2036323e12eb7b011c3a1e110fcd2f28df1d724cde3a25f53b2"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_INVOCATION_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_baseline_invocation_implementation"


class V2R13Pair09BaselineGitBackendReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineGitBackendReviewHold(message)


@lru_cache(maxsize=1)
def _validate_backend_cached() -> dict[str, Any]:
    contract = backend.pair09_baseline_git_backend_contract()
    preflight = (
        preflight_review
        .v2r13_pair09_baseline_host_preflight_review_contract()
    )

    _require(
        preflight.get("pair09_baseline_host_preflight_reviewed") is True,
        "pair09 host preflight review missing",
    )
    _require(contract.get("pair_slot") == 9, "backend pair-slot drift")
    _require(contract.get("arm") == "baseline", "backend arm drift")
    _require(contract.get("held_out") is False, "backend held-out drift")
    _require(
        contract.get("fixed_source_root")
        == "/home/zoso/dev/openra-rl-war-college",
        "backend source root drift",
    )
    _require(
        contract.get("fixed_arm_root")
        == (
            "/home/zoso/dev/void-war-college-execution/"
            "v2r13-generation2/generation2/pair-09/baseline"
        ),
        "backend arm root drift",
    )
    _require(
        contract.get("frozen_source_commit")
        == "973802ef0a614e5afa782ff20e231e18966ae3e5",
        "backend frozen source drift",
    )
    _require(
        contract.get("frozen_engine_commit")
        == "1607a7a6501d42a47638393ecef8b22831064932",
        "backend frozen engine drift",
    )
    _require(contract.get("fetch_implemented") is False, "backend fetch enabled")
    _require(
        contract.get("canonical_checkout_implemented") is False,
        "backend canonical checkout enabled",
    )
    _require(
        contract.get("force_remove_implemented") is False,
        "backend force remove enabled",
    )
    _require(
        contract.get("runtime_execution_authorized") is False,
        "backend carries runtime authority",
    )
    _require(
        contract.get("runtime_execution_performed") is False,
        "backend performed runtime execution",
    )
    _require(contract.get("automatic_retry") is False, "backend retry enabled")

    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"backend authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_BASELINE_GIT_BACKEND_SOURCE_BINDING_REVIEW_REQUIRED",
        "backend source-review frontier drift",
    )
    return {
        "backend": deepcopy(contract),
        "preflight_review": deepcopy(preflight),
    }


def v2r13_pair09_baseline_git_backend_review_contract() -> dict[str, Any]:
    validated = _validate_backend_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "backend_git_blob": BACKEND_GIT_BLOB,
        "backend_source_sha256": BACKEND_SOURCE_SHA256,
        "backend_test_git_blob": BACKEND_TEST_GIT_BLOB,
        "backend_test_sha256": BACKEND_TEST_SHA256,
        "preflight_review_git_blob": PREFLIGHT_REVIEW_GIT_BLOB,
        "preflight_review_source_sha256": PREFLIGHT_REVIEW_SOURCE_SHA256,
        "separate_review_instrument": True,
        "pair09_baseline_git_backend_reviewed": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "fixed_source_root": validated["backend"]["fixed_source_root"],
        "fixed_arm_root": validated["backend"]["fixed_arm_root"],
        "frozen_source_commit": validated["backend"]["frozen_source_commit"],
        "frozen_engine_commit": validated["backend"]["frozen_engine_commit"],
        "fetch_implemented": False,
        "canonical_checkout_implemented": False,
        "force_remove_implemented": False,
        "runtime_execution_authorized": False,
        "runtime_execution_performed": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_backend": deepcopy(validated["backend"]),
        "validated_preflight_review": deepcopy(validated["preflight_review"]),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineGitBackendReviewHold(
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
