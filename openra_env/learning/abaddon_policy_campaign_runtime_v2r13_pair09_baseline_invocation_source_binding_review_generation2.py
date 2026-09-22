"""Source-only review of the one-shot V2R13 pair-09 baseline invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_invocation_generation2
    as invocation,
)
from tools import (
    abaddon_policy_campaign_runtime_v2r13_precision_pair09_baseline_generation2
    as precision_cli,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-invocation-source-binding-review-contract.v1"
)

INVOCATION_GIT_BLOB = "312215c5b82296f15200544a61cc500d908ff9cf"
INVOCATION_SOURCE_SHA256 = (
    "815d824bfa7aabc2659ff1fd2e4407c81dff7d5101103ac6868e6c1dfa5b768b"
)
INVOCATION_TEST_GIT_BLOB = "eea23bdc6a453689d3f77de160761aaf453a5639"
INVOCATION_TEST_SHA256 = (
    "c347ceb4584cd6bfbfe1f517d772097cb3b70f226bf680670c04e2f26147b4cc"
)
PRECISION_CLI_GIT_BLOB = "c9e26cffd595e5dde8b4e166ee25abcf43496345"
PRECISION_CLI_SOURCE_SHA256 = (
    "0b24777dcbe290375323bb852754fe873fc65e4d32004ddad0f986e00df8607f"
)
PRECISION_CLI_TEST_GIT_BLOB = "8a31d97fc828d5322840ba61446c8a03415acdbc"
PRECISION_CLI_TEST_SHA256 = (
    "9173453692f017682813c8195454b6abd6dc99356821e7ceef37e641c6126e33"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_v2r13_pair09_baseline_execution_authorization"


class V2R13Pair09BaselineInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_invocation_cached() -> dict[str, Any]:
    contract = invocation.pair09_baseline_invocation_contract()

    _require(
        contract.get("pair09_baseline_invocation_implemented") is True,
        "pair09 baseline invocation missing",
    )
    _require(
        contract.get("pair09_baseline_invocation_reviewed") is False,
        "pair09 invocation unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 9, "pair09 invocation slot drift")
    _require(contract.get("arm") == "baseline", "pair09 invocation arm drift")
    _require(contract.get("held_out") is False, "pair09 invocation held-out drift")

    for field in (
        "explicit_authorization_boolean_required",
        "explicit_confirmation_token_required",
        "exact_current_main_required",
        "exact_invocation_source_sha256_required",
        "exact_dependency_git_blobs_required",
        "fresh_current_main_host_preflight_required",
        "cached_sudo_required",
        "revocation_sentinel_absent_required",
        "isolated_grpc_python_required",
        "pair03_preserved_evidence_revalidation_required",
        "single_use_attempt_consumption_required",
        "fresh_live_readiness_before_inference_required",
    ):
        _require(contract.get(field) is True, f"invocation gate missing: {field}")

    _require(
        contract.get("operator_authentication_implemented") is False,
        "invocation unexpectedly claims operator authentication",
    )

    for field in (
        "pair09_baseline_specific_authorization_accepted",
        "single_use_attempt_consumed",
        "pair09_baseline_execution_authorized",
        "pair09_baseline_execution_performed",
        "pair09_candidate_execution_authorized",
        "held_out_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "runtime_execution_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
    ):
        _require(contract.get(field) is False, f"invocation boundary drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_BASELINE_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "invocation source-review frontier drift",
    )

    _require(
        precision_cli.INVOCATION_SOURCE_SHA256 == INVOCATION_SOURCE_SHA256,
        "Precision CLI invocation SHA drift",
    )
    _require(
        precision_cli.AUTHORIZATION_TOKEN
        == "VOID_ABADDON_GENERATION2_V2R13_AUTHORIZE_PAIR09_BASELINE_ONCE",
        "Precision CLI authorization token drift",
    )
    _require(
        precision_cli.invocation.CONFIRM_TOKEN
        == "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR09_BASELINE_ONCE",
        "Precision CLI confirmation token drift",
    )

    return deepcopy(contract)


def v2r13_pair09_baseline_invocation_review_contract() -> dict[str, Any]:
    validated = _validate_invocation_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "precision_cli_source_sha256": PRECISION_CLI_SOURCE_SHA256,
        "precision_cli_test_git_blob": PRECISION_CLI_TEST_GIT_BLOB,
        "precision_cli_test_sha256": PRECISION_CLI_TEST_SHA256,
        "separate_review_instrument": True,
        "pair09_baseline_invocation_source_binding_present": True,
        "pair09_baseline_invocation_reviewed": True,
        "precision_cli_reviewed": True,
        "precision_cli_requires_expected_main_head": True,
        "precision_cli_requires_explicit_authorization": True,
        "precision_cli_requires_explicit_confirmation": True,
        "precision_cli_pins_reviewed_invocation_source_sha256": True,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "single_use_attempt": True,
        "automatic_retry": False,
        "operator_authenticated": False,
        "pair09_baseline_specific_authorization_accepted": False,
        "single_use_attempt_consumed": False,
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
        "runtime_execution_invoked_by_review": False,
        "model_inference_invoked_by_review": False,
        "game_execution_invoked_by_review": False,
        "validated_invocation": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineInvocationReviewHold(NEXT_GATE)
