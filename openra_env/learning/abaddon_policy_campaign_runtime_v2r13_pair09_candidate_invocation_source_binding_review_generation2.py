"""Source-only review of the one-shot V2R13 pair-09 candidate invocation."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_invocation_generation2
    as invocation,
)
from tools import (
    abaddon_policy_campaign_runtime_v2r13_precision_pair09_candidate_generation2
    as precision_cli,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-invocation-source-binding-review-contract.v1"
)

INVOCATION_GIT_BLOB = "1c8a845a76569dd656cb11ad09593c24713a8ce2"
INVOCATION_SOURCE_SHA256 = (
    "4858f3fe148829d050604746cd64fa426963370a71029f95d7cc40bb71b5ba7c"
)
INVOCATION_TEST_GIT_BLOB = "7717bf608b6c995ef9acc3f107bac6752c0ce43a"
INVOCATION_TEST_SHA256 = (
    "9dac5c7e10e8feee66a2e1d6315cb5e7482c8892d579672173282edd094ef79b"
)
PRECISION_CLI_GIT_BLOB = "6be5d1e346afeb699a6c8fe251c5b2c397315f6e"
PRECISION_CLI_SOURCE_SHA256 = (
    "221ff13d4872024dc2288a7d51f039133a66f8767336e2c9f6b83ca1f9801ff8"
)
PRECISION_CLI_TEST_GIT_BLOB = "c74ba630cda19363abf2b627f371dfdc80b390da"
PRECISION_CLI_TEST_SHA256 = (
    "4db3385e61f57a4b316bb4f87ea08cb99d8093b8a4dc553962f6c3382c89981e"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "trusted_operator_v2r13_pair09_candidate_execution_authorization"
)


class V2R13Pair09CandidateInvocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateInvocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_invocation_cached() -> dict[str, Any]:
    contract = invocation.pair09_candidate_invocation_contract()

    _require(
        contract.get("pair09_candidate_invocation_implemented") is True,
        "pair09 candidate invocation missing",
    )
    _require(
        contract.get("pair09_candidate_invocation_reviewed") is False,
        "pair09 candidate invocation self-reviewed",
    )
    _require(contract.get("pair_slot") == 9, "candidate invocation slot drift")
    _require(contract.get("arm") == "candidate", "candidate invocation arm drift")
    _require(contract.get("held_out") is False, "candidate invocation held-out drift")

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
        "pair09_baseline_revalidation_required",
        "candidate_policy_binding_required",
        "single_use_attempt_consumption_required",
        "fresh_live_readiness_before_inference_required",
    ):
        _require(
            contract.get(field) is True,
            f"candidate invocation gate missing: {field}",
        )

    _require(
        contract.get("operator_authentication_implemented") is False,
        "candidate invocation unexpectedly claims operator authentication",
    )

    for field in (
        "pair09_candidate_specific_authorization_accepted",
        "single_use_attempt_consumed",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "pair09_baseline_rerun_authorized",
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
        _require(
            contract.get(field) is False,
            f"candidate invocation boundary drift: {field}",
        )

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "candidate invocation review frontier drift",
    )

    _require(
        precision_cli.INVOCATION_SOURCE_SHA256
        == INVOCATION_SOURCE_SHA256,
        "candidate Precision CLI invocation SHA drift",
    )
    _require(
        precision_cli.AUTHORIZATION_TOKEN
        == "VOID_ABADDON_GENERATION2_V2R13_AUTHORIZE_PAIR09_CANDIDATE_ONCE",
        "candidate Precision CLI authorization token drift",
    )
    _require(
        precision_cli.invocation.CONFIRM_TOKEN
        == "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR09_CANDIDATE_ONCE",
        "candidate Precision CLI confirmation token drift",
    )

    return deepcopy(contract)


def v2r13_pair09_candidate_invocation_review_contract() -> dict[str, Any]:
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
        "pair09_candidate_invocation_source_binding_present": True,
        "pair09_candidate_invocation_reviewed": True,
        "precision_cli_reviewed": True,
        "precision_cli_requires_expected_main_head": True,
        "precision_cli_requires_explicit_authorization": True,
        "precision_cli_requires_explicit_confirmation": True,
        "precision_cli_pins_reviewed_invocation_source_sha256": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "single_use_attempt": True,
        "automatic_retry": False,
        "operator_authenticated": False,
        "pair09_candidate_specific_authorization_accepted": False,
        "single_use_attempt_consumed": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_candidate_execution_performed": False,
        "pair09_baseline_rerun_authorized": False,
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


def authorize_or_execute_pair09_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateInvocationReviewHold(NEXT_GATE)
