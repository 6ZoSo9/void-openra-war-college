"""Source-only review of the pair-06 baseline V8 runtime lifetime design."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_lifetime_handoff_design_generation2
    as design,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-lifetime-handoff-design-review-contract.v1"
)

DESIGN_GIT_BLOB = "479206e01dea661cce45922a776b258c142a82c1"
DESIGN_SOURCE_SHA256 = (
    "4df1bbcbd243ba9ddbcf21cf730aa315b006f82a8b62b183f319eaa02f1dc459"
)
DESIGN_TEST_GIT_BLOB = "b8a3cef2834efa5d89850505be4f509588c10ede"
DESIGN_TEST_SHA256 = (
    "922f468f2fa6e3ec88beefdb848ed1640763e28a9a746a1dba9ee93f5bd1e00c"
)

NEXT_GATE = "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_game_coupled_runtime_implementation"


class Pair06V8BaselineLifetimeHandoffDesignReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLifetimeHandoffDesignReviewHold(message)


@lru_cache(maxsize=1)
def _validate_design_cached() -> dict[str, Any]:
    contract = design.pair06_v8_baseline_lifetime_handoff_design_contract()

    _require(
        contract.get("pair06_v8_baseline_lifetime_handoff_design_implemented") is True,
        "pair06 lifetime design missing",
    )
    _require(
        contract.get("pair06_v8_baseline_lifetime_handoff_design_reviewed") is False,
        "pair06 lifetime design unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 lifetime slot drift")
    _require(contract.get("arm") == "baseline", "pair06 lifetime arm drift")
    _require(contract.get("held_out") is False, "pair06 lifetime became held-out")
    _require(contract.get("seed") == 208354846, "pair06 lifetime seed drift")
    _require(contract.get("rounds") == 36, "pair06 lifetime rounds drift")
    _require(contract.get("ticks_per_round") == 25, "pair06 lifetime ticks drift")
    _require(contract.get("starter_infantry") == 4, "pair06 starter infantry drift")
    _require(contract.get("staging_max_ticks") == 800, "pair06 staging cap drift")
    _require(
        contract.get("runtime_selection_key")
        == "apollyon-v3-v8-accepted-model-control",
        "pair06 lifetime runtime selection drift",
    )

    _require(contract.get("validation_load_completed") is True, "validation load missing")
    _require(
        contract.get("validation_load_attempt_consumed") is True,
        "validation load attempt not consumed",
    )
    _require(
        contract.get("validation_load_reusable_for_game") is False,
        "validation load incorrectly reusable",
    )
    _require(
        contract.get("cross_process_runtime_reuse_permitted") is False,
        "cross-process runtime reuse incorrectly permitted",
    )
    _require(
        contract.get("persistent_runtime_handle_exported") is False,
        "persistent runtime handle unexpectedly exported",
    )
    _require(
        contract.get("runtime_residency_after_launcher_attested") is False,
        "post-launcher runtime residency unexpectedly attested",
    )

    for field in (
        "game_coupled_runtime_lifecycle_required",
        "same_process_load_and_game_required",
        "fresh_environment_verification_required",
        "exact_17_asset_verification_required",
        "create_only_game_attempt_claim_required",
        "new_game_coupled_load_authorization_required",
        "new_game_execution_authorization_required",
        "single_authorization_must_cover_load_and_game",
    ):
        _require(contract.get(field) is True, f"pair06 lifetime design drift: {field}")

    _require(
        tuple(contract.get("atomic_lifecycle", ())) == design.ATOMIC_LIFECYCLE,
        "pair06 atomic lifecycle drift",
    )

    for field in (
        "another_validation_load_authorized",
        "game_coupled_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "runtime_execution_performed",
        "model_inference_performed",
        "game_execution_performed",
        "candidate_runtime_load_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 lifetime authority drift: {field}")

    _require(contract.get("automatic_retry") is False, "pair06 automatic retry enabled")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 lifetime review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_baseline_lifetime_handoff_design_review_contract() -> dict[str, Any]:
    validated = _validate_design_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "design_git_blob": DESIGN_GIT_BLOB,
        "design_source_sha256": DESIGN_SOURCE_SHA256,
        "design_test_git_blob": DESIGN_TEST_GIT_BLOB,
        "design_test_sha256": DESIGN_TEST_SHA256,
        "pair06_v8_baseline_lifetime_handoff_design_source_binding_present": True,
        "pair06_v8_baseline_lifetime_handoff_design_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "seed": 208354846,
        "rounds": 36,
        "ticks_per_round": 25,
        "validation_load_completed": True,
        "validation_load_attempt_consumed": True,
        "validation_load_reusable_for_game": False,
        "cross_process_runtime_reuse_permitted": False,
        "persistent_runtime_handle_exported": False,
        "runtime_residency_after_launcher_attested": False,
        "game_coupled_runtime_lifecycle_required": True,
        "same_process_load_and_game_required": True,
        "fresh_environment_verification_required": True,
        "exact_17_asset_verification_required": True,
        "create_only_game_attempt_claim_required": True,
        "new_game_coupled_load_authorization_required": True,
        "new_game_execution_authorization_required": True,
        "single_authorization_must_cover_load_and_game": True,
        "atomic_lifecycle": design.ATOMIC_LIFECYCLE,
        "another_validation_load_authorized": False,
        "game_coupled_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "candidate_runtime_load_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_design": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLifetimeHandoffDesignReviewHold(NEXT_GATE)
