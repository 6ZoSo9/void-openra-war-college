"""Source-only review of accepted pair-06 baseline V8 load evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-load-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "0ea17348c2cfcc4ad9f200bc556c0a81305ea736"
ACCEPTANCE_SOURCE_SHA256 = (
    "e91d62488132d120f7e068c5dfc0a81ece80e908180819de861ead486555b090"
)
ACCEPTANCE_TEST_GIT_BLOB = "cbe4735c1097f32fd33989ce97e92ae704ee84e4"
ACCEPTANCE_TEST_SHA256 = (
    "eaf5f28f93c11a46f3414af276a4b51cdb4aab19a46aace7e86db9a83b911c35"
)

NEXT_GATE = "PAIR06_V8_BASELINE_GAME_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_game_execution_authorization_request"


class Pair06V8BaselineLoadEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = acceptance.pair06_v8_baseline_load_evidence_acceptance_contract()

    _require(
        contract.get("pair06_v8_baseline_load_evidence_accepted") is True,
        "pair06 baseline load evidence acceptance missing",
    )
    _require(
        contract.get("launcher_sha256")
        == "1d2b787f0ca5dd89701e4f9862088d8b458dce872034a870e36f73a5ef177246",
        "pair06 launcher SHA drift",
    )
    _require(
        contract.get("execution_main_head")
        == "cdafee828fe3066651089e43cef88e4668d680ee",
        "pair06 execution-main drift",
    )
    _require(contract.get("attempt_consumed") is True, "pair06 attempt not consumed")
    _require(contract.get("maximum_attempts") == 1, "pair06 attempt count drift")
    _require(
        contract.get("runtime_load_performed") is True
        and contract.get("model_weights_loaded") is True,
        "pair06 completed load evidence missing",
    )
    _require(
        contract.get("another_baseline_load_authorized") is False,
        "another pair06 baseline load unexpectedly authorized",
    )
    _require(
        contract.get("candidate_runtime_load_authorized") is False,
        "pair06 candidate load unexpectedly authorized",
    )
    _require(
        contract.get("game_execution_authorized") is False,
        "pair06 game execution prematurely authorized",
    )
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution prematurely authorized",
    )
    _require(contract.get("automatic_retry") is False, "pair06 automatic retry enabled")
    _require(
        contract.get("baseline_game_execution_authorization_request_required") is True,
        "pair06 game authorization-request frontier missing",
    )

    accepted = contract.get("accepted_evidence")
    _require(isinstance(accepted, dict), "accepted pair06 evidence missing")
    _require(accepted.get("pair_slot") == 6, "accepted pair06 slot drift")
    _require(accepted.get("arm") == "baseline", "accepted pair06 arm drift")
    _require(accepted.get("held_out") is False, "accepted pair06 held-out drift")
    _require(
        accepted.get("runtime_environment_verified") is True,
        "pair06 environment verification missing",
    )
    _require(
        accepted.get("runtime_assets_verified") is True
        and accepted.get("verified_asset_count") == 17,
        "pair06 exact asset verification missing",
    )
    _require(
        accepted.get("runtime_load_authorized") is True
        and accepted.get("runtime_load_performed") is True
        and accepted.get("model_weights_loaded") is True,
        "pair06 accepted load completion missing",
    )
    _require(
        accepted.get("model_inference_authorized") is False
        and accepted.get("model_inference_performed") is False,
        "pair06 inference boundary drift",
    )
    _require(
        accepted.get("game_execution_authorized") is False
        and accepted.get("game_execution_performed") is False,
        "pair06 game boundary drift",
    )
    _require(
        accepted.get("pair15_execution_authorized") is False
        and accepted.get("pair15_execution_performed") is False,
        "pair15 held-out boundary drift",
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
        _require(accepted.get(field) is False, f"pair06 evidence scope expanded: {field}")

    return deepcopy(contract)


def pair06_v8_baseline_load_evidence_review_contract() -> dict[str, Any]:
    validated = _validate_acceptance_cached()
    accepted = validated["accepted_evidence"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_source_git_blob": ACCEPTANCE_SOURCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "pair06_v8_baseline_load_evidence_source_binding_present": True,
        "pair06_v8_baseline_load_evidence_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "attempt_consumed": True,
        "maximum_attempts": 1,
        "launcher_sha256": accepted["launcher_sha256"],
        "execution_main_head": accepted["execution_main_head"],
        "execution_main_tree": accepted["execution_main_tree"],
        "invocation_source_sha256": accepted["invocation_source_sha256"],
        "attempt_marker_sha256": accepted["attempt_marker_sha256"],
        "result_file_sha256": accepted["result_file_sha256"],
        "runtime_environment_verified": True,
        "runtime_assets_verified": True,
        "verified_asset_count": 17,
        "runtime_load_performed": True,
        "model_weights_loaded": True,
        "another_baseline_load_authorized": False,
        "candidate_runtime_load_authorized": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "pair15_execution_performed": False,
        "automatic_retry": False,
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
        "baseline_game_execution_authorization_request_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_acceptance": deepcopy(validated),
    }


def authorize_game_execution(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadEvidenceReviewHold(NEXT_GATE)
