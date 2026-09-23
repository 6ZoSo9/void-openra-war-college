"""Source-only design for pair-06 baseline V8 runtime lifetime handoff.

The completed Precision load proved exact bytes/environment and consumed its
single load attempt, but that Python process exited without exporting a
persistent runtime handle. Therefore that completed load cannot be reused for a
later game process.

The future baseline game must use a new, separately authorized, atomic process
lifecycle:
1. fresh environment and exact-asset verification;
2. create-only game-attempt claim;
3. exact V8 load;
4. start the pair-06 baseline game;
5. permit model inference only inside that game lifecycle;
6. cleanup runtime/game resources;
7. publish one durable game result.

This design grants no load, inference, or game authority and performs no host
action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_evidence_source_binding_review_generation2
    as load_evidence_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair06_nonheldout_allocation_source_binding_review_generation2
    as allocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-lifetime-handoff-design-contract.v1"
)

LOAD_EVIDENCE_REVIEW_GIT_BLOB = "98a4658050b6b953fe34ac2a25d642356ebec9c8"
LOAD_EVIDENCE_REVIEW_SOURCE_SHA256 = (
    "PENDING_REPIN_AFTER_FINAL_EVIDENCE_REVIEW"
)
ALLOCATION_REVIEW_GIT_BLOB = "5dd312086df8d2a6c205badb3feb71560c519990"
ALLOCATION_REVIEW_SOURCE_SHA256 = (
    "695c9ff074a21a7ff6002d30a50852e7a9a746c5735a078f985b80a6a22dfe0a"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
SEED = 208354846
ROUNDS = 36
TICKS_PER_ROUND = 25
STARTER_INFANTRY = 4
STAGING_MAX_TICKS = 800
RUNTIME_SELECTION_KEY = "apollyon-v3-v8-accepted-model-control"

ATOMIC_LIFECYCLE = (
    "fresh_runtime_environment_verification",
    "exact_17_asset_verification",
    "create_only_game_attempt_claim",
    "exact_v8_runtime_load",
    "pair06_baseline_game_start",
    "model_inference_within_authorized_game_only",
    "runtime_and_game_cleanup",
    "durable_game_result_publication",
)

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_runtime_lifetime_handoff_design_review"


class Pair06V8BaselineLifetimeHandoffDesignHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLifetimeHandoffDesignHold(message)


@lru_cache(maxsize=1)
def _dependencies_cached() -> dict[str, Any]:
    load = load_evidence_review.pair06_v8_baseline_load_evidence_review_contract()
    allocation = allocation_review.v2r13_pair06_nonheldout_allocation_review_contract()

    _require(
        load.get("pair06_v8_baseline_load_evidence_reviewed") is True,
        "pair06 baseline load evidence not reviewed",
    )
    _require(load.get("pair_slot") == PAIR_SLOT, "pair06 load slot drift")
    _require(load.get("arm") == ARM, "pair06 load arm drift")
    _require(load.get("held_out") is False, "pair06 load became held-out")
    _require(load.get("attempt_consumed") is True, "pair06 validation load not consumed")
    _require(load.get("maximum_attempts") == 1, "pair06 validation load attempt count drift")
    _require(load.get("runtime_load_performed") is True, "pair06 validation load not performed")
    _require(load.get("model_weights_loaded") is True, "pair06 validation weights not loaded")
    _require(
        load.get("persistent_runtime_handle_exported") is False,
        "pair06 validation load unexpectedly exported persistent runtime",
    )
    _require(
        load.get("runtime_residency_after_launcher_attested") is False,
        "pair06 validation runtime residency unexpectedly attested",
    )
    _require(
        load.get("another_baseline_load_authorized") is False,
        "pair06 second load prematurely authorized",
    )
    _require(
        load.get("model_inference_authorized") is False
        and load.get("game_execution_authorized") is False,
        "pair06 validation load leaked execution authority",
    )
    _require(
        load.get("next_gate")
        == "PAIR06_V8_BASELINE_RUNTIME_LIFETIME_HANDOFF_DESIGN_REQUIRED",
        "pair06 load-evidence lifetime frontier drift",
    )

    _require(
        allocation.get("pair06_nonheldout_allocation_reviewed") is True,
        "pair06 allocation not reviewed",
    )
    _require(allocation.get("selected_pair_slot") == PAIR_SLOT, "pair06 allocation slot drift")
    reviewed = allocation.get("reviewed_allocation")
    _require(isinstance(reviewed, dict), "pair06 reviewed allocation missing")
    _require(reviewed.get("selected_seed") == SEED, "pair06 seed drift")
    _require(reviewed.get("selected_rounds") == ROUNDS, "pair06 rounds drift")
    _require(
        reviewed.get("selected_ticks_per_round") == TICKS_PER_ROUND,
        "pair06 ticks-per-round drift",
    )
    _require(
        reviewed.get("selected_starter_infantry") == STARTER_INFANTRY,
        "pair06 starter infantry drift",
    )
    _require(
        reviewed.get("selected_staging_max_ticks") == STAGING_MAX_TICKS,
        "pair06 staging cap drift",
    )
    _require(
        allocation.get("selected_opponent_snapshot_id") == RUNTIME_SELECTION_KEY,
        "pair06 V8 runtime selection drift",
    )
    _require(
        allocation.get("v2r13_executor_not_applicable_to_pair06") is True,
        "pair06 incorrectly routed through V2R13 executor",
    )

    return {
        "load_evidence_review": deepcopy(load),
        "allocation_review": deepcopy(allocation),
    }


def pair06_v8_baseline_lifetime_handoff_design_contract() -> dict[str, Any]:
    dependencies = _dependencies_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "load_evidence_review_git_blob": LOAD_EVIDENCE_REVIEW_GIT_BLOB,
        "load_evidence_review_source_sha256": LOAD_EVIDENCE_REVIEW_SOURCE_SHA256,
        "allocation_review_git_blob": ALLOCATION_REVIEW_GIT_BLOB,
        "allocation_review_source_sha256": ALLOCATION_REVIEW_SOURCE_SHA256,
        "pair06_v8_baseline_lifetime_handoff_design_implemented": True,
        "pair06_v8_baseline_lifetime_handoff_design_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "seed": SEED,
        "rounds": ROUNDS,
        "ticks_per_round": TICKS_PER_ROUND,
        "starter_infantry": STARTER_INFANTRY,
        "staging_max_ticks": STAGING_MAX_TICKS,
        "runtime_selection_key": RUNTIME_SELECTION_KEY,
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
        "atomic_lifecycle": ATOMIC_LIFECYCLE,
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
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_load(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLifetimeHandoffDesignHold(NEXT_GATE)
