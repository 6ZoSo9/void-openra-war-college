"""Source-only review of the pair-06 non-held-out allocation selection."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair06_nonheldout_allocation_generation2
    as allocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair06-nonheldout-allocation-source-binding-review-contract.v1"
)

ALLOCATION_GIT_BLOB = "ffc2208c7d75609937bfeda44083de1e5b70853e"
ALLOCATION_SOURCE_SHA256 = (
    "257977fde8a2bfdd266736bf69b554e41545aa9944b21c9ecc1499d999382a66"
)
ALLOCATION_TEST_GIT_BLOB = "08fc2f300dbb1f87fae8a08fe521f8a49828c16e"
ALLOCATION_TEST_SHA256 = (
    "fbde05698ea4da12ac314557ba7dea20061eae64fa2ed84510266292d7208cae"
)

NEXT_GATE = "V2R13_PAIR06_BOUNDED_CAPABILITY_EXTENSION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair06_bounded_capability_extension"


class V2R13Pair06NonheldoutAllocationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair06NonheldoutAllocationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_allocation_cached() -> dict[str, Any]:
    contract = allocation.v2r13_pair06_nonheldout_allocation_contract()

    _require(
        contract.get("new_nonheldout_allocation_selected") is True,
        "pair06 allocation missing",
    )
    _require(
        contract.get("selection_rule")
        == "lowest_unused_nonheldout_historical_control_pair_slot",
        "pair06 selection rule drift",
    )
    _require(
        tuple(contract.get("completed_nonheldout_pair_slots", ())) == (3, 9),
        "completed non-held-out pair set drift",
    )
    _require(
        tuple(contract.get("eligible_unused_historical_control_pair_slots", ()))
        == (6, 12),
        "eligible pair06 allocation set drift",
    )
    _require(contract.get("selected_pair_slot") == 6, "selected pair-slot drift")
    _require(contract.get("selected_seed") == 208354846, "selected seed drift")
    _require(contract.get("selected_rounds") == 36, "selected round-limit drift")
    _require(contract.get("selected_held_out") is False, "pair06 became held-out")
    _require(
        contract.get("selected_opponent_role") == "prior_accepted_model_control",
        "pair06 opponent role drift",
    )
    _require(
        contract.get("selected_opponent_snapshot_id")
        == "apollyon-v3-v8-accepted-model-control",
        "pair06 opponent snapshot drift",
    )
    _require(
        contract.get("selected_opponent_snapshot_sha256")
        == "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667",
        "pair06 opponent snapshot SHA drift",
    )
    _require(
        contract.get("matched_baseline_candidate_required") is True,
        "pair06 matched-arm requirement missing",
    )
    _require(
        tuple(contract.get("bounded_executor_current_pair_slots", ()))
        == (3, 9, 15),
        "current bounded executor pair-slot set drift",
    )
    _require(
        tuple(contract.get("bounded_executor_current_held_out_pair_slots", ()))
        == (15,),
        "current bounded executor held-out set drift",
    )
    _require(
        contract.get("bounded_executor_extension_required") is True,
        "pair06 capability extension not required",
    )
    _require(
        contract.get("pair06_runtime_execution_authorized") is False,
        "pair06 execution prematurely authorized",
    )
    _require(
        contract.get("pair06_runtime_execution_performed") is False,
        "pair06 execution already performed",
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

    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 allocation authority drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR06_BOUNDED_CAPABILITY_EXTENSION_REQUIRED",
        "pair06 allocation frontier drift",
    )
    return deepcopy(contract)


def v2r13_pair06_nonheldout_allocation_review_contract() -> dict[str, Any]:
    reviewed = _validate_allocation_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "allocation_git_blob": ALLOCATION_GIT_BLOB,
        "allocation_source_sha256": ALLOCATION_SOURCE_SHA256,
        "allocation_test_git_blob": ALLOCATION_TEST_GIT_BLOB,
        "allocation_test_sha256": ALLOCATION_TEST_SHA256,
        "separate_review_instrument": True,
        "allocation_source_identity_pinned_by_git_blob": True,
        "allocation_source_identity_pinned_by_sha256": True,
        "allocation_test_identity_pinned_by_git_blob": True,
        "allocation_test_identity_pinned_by_sha256": True,
        "pair06_nonheldout_allocation_reviewed": True,
        "selected_pair_slot": 6,
        "selected_seed": 208354846,
        "selected_held_out": False,
        "selected_opponent_role": "prior_accepted_model_control",
        "selected_opponent_snapshot_id": (
            "apollyon-v3-v8-accepted-model-control"
        ),
        "selected_opponent_snapshot_sha256": (
            "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667"
        ),
        "bounded_executor_extension_required": True,
        "pair06_runtime_execution_authorized": False,
        "pair06_runtime_execution_performed": False,
        "pair15_execution_authorized": False,
        "pair15_execution_performed": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_allocation": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_pair06(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair06NonheldoutAllocationReviewHold(
        "V2R13_PAIR06_RUNTIME_EXECUTION_NOT_AUTHORIZED"
    )


def execute_pair15(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair06NonheldoutAllocationReviewHold(
        "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair06NonheldoutAllocationReviewHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
