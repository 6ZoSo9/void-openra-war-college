"""Source-only allocation of a fresh non-held-out V2R13 evaluation lane.

The post-pair-09 design preserves held-out pair 15 and requires a new
non-held-out evaluation allocation. The canonical Generation-2 campaign ledger
already contains additional non-held-out matched pairs that have never been
authorized by the V2R13 bounded executor.

Selection rule:
* consider canonical non-held-out historical-control pairs;
* exclude completed pair slots 3 and 9;
* select the lowest remaining canonical pair slot.

That deterministically selects pair 6:
* seed 208354846;
* opponent role prior_accepted_model_control;
* opponent snapshot apollyon-v3-v8-accepted-model-control;
* 36 matched baseline/candidate rounds.

This module selects the allocation only. Pair 6 is not currently in the V2R13
bounded executor's authorized pair-slot set, so execution remains impossible
until a separate source-only capability extension is reviewed.

No runtime, replay, held-out, training, promotion, deployment, VOID-chain,
wallet, or funds authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_plan_generation2 as campaign_plan,
)
from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2
    as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as bounded_executor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_post_pair09_evaluation_design_source_binding_review_generation2
    as post_pair09_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair06-nonheldout-allocation-contract.v1"
)

POST_PAIR09_REVIEW_GIT_BLOB = "0867c939818600af31aafee65c449be6f33c33a1"
CAMPAIGN_PLAN_GIT_BLOB = "86c6feb3072f9d540dbd4f7ee6462addcbac54aa"
PLAN_FIXTURE_GIT_BLOB = "3c884e8c35e4099ea51cc5ed46521149ade9a7b0"
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
BOUNDED_EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"

COMPLETED_NONHELDOUT_PAIR_SLOTS = (3, 9)
HISTORICAL_CONTROL_ROLES = (
    "prior_qualified_predecessor",
    "prior_accepted_model_control",
)
ELIGIBLE_UNUSED_HISTORICAL_CONTROL_PAIR_SLOTS = (6, 12)

SELECTED_PAIR_SLOT = 6
SELECTED_SEED = 208354846
SELECTED_ROUNDS = 36
SELECTED_TICKS_PER_ROUND = 25
SELECTED_STARTER_INFANTRY = 4
SELECTED_STAGING_MAX_TICKS = 800
SELECTED_OPPONENT_ROLE = "prior_accepted_model_control"
SELECTED_OPPONENT_SNAPSHOT_ID = "apollyon-v3-v8-accepted-model-control"
SELECTED_OPPONENT_SNAPSHOT_SHA256 = (
    "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667"
)

NEXT_GATE = "V2R13_PAIR06_BOUNDED_CAPABILITY_EXTENSION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair06_bounded_capability_extension"


class V2R13Pair06NonheldoutAllocationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair06NonheldoutAllocationHold(message)


@lru_cache(maxsize=1)
def _post_pair09_cached() -> dict[str, Any]:
    contract = (
        post_pair09_review
        .v2r13_post_pair09_evaluation_design_review_contract()
    )
    _require(
        contract.get("post_pair09_evaluation_design_reviewed") is True,
        "post-pair09 design not reviewed",
    )
    _require(
        contract.get("existing_nonheldout_capacity_exhausted") is True,
        "post-pair09 legacy non-held-out capacity not exhausted",
    )
    _require(
        contract.get("held_out_pair15_preserved") is True,
        "pair15 preservation missing",
    )
    _require(
        contract.get("held_out_contamination_prohibited") is True,
        "held-out contamination prohibition missing",
    )
    _require(
        contract.get("new_nonheldout_evaluation_allocation_required") is True,
        "new non-held-out allocation not required",
    )
    _require(
        contract.get("new_nonheldout_execution_authorized") is False,
        "new non-held-out execution already authorized",
    )
    _require(
        contract.get("pair15_execution_authorized") is False,
        "pair15 execution already authorized",
    )
    _require(
        contract.get("next_gate")
        == "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED",
        "post-pair09 allocation frontier drift",
    )
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _selected_row_cached() -> dict[str, Any]:
    plan = campaign_plan.precommitted_campaign_plan()
    rows = plan.get("pair_slots")
    _require(
        isinstance(rows, list) and len(rows) == 18,
        "canonical campaign pair ledger drift",
    )

    candidates = [
        row
        for row in rows
        if isinstance(row, dict)
        and row.get("held_out") is False
        and row.get("opponent_role") in HISTORICAL_CONTROL_ROLES
        and row.get("pair_slot") not in COMPLETED_NONHELDOUT_PAIR_SLOTS
    ]
    slots = tuple(sorted(int(row["pair_slot"]) for row in candidates))
    _require(
        slots == ELIGIBLE_UNUSED_HISTORICAL_CONTROL_PAIR_SLOTS,
        "eligible unused historical-control slot set drift",
    )

    selected = min(candidates, key=lambda row: int(row["pair_slot"]))
    _require(
        selected.get("pair_slot") == SELECTED_PAIR_SLOT,
        "deterministic selected pair-slot drift",
    )
    _require(selected.get("held_out") is False, "selected pair unexpectedly held-out")
    _require(selected.get("seed") == SELECTED_SEED, "selected seed drift")
    _require(selected.get("rounds") == SELECTED_ROUNDS, "selected round-limit drift")
    _require(
        selected.get("ticks_per_round") == SELECTED_TICKS_PER_ROUND,
        "selected ticks-per-round drift",
    )
    _require(
        selected.get("starter_infantry") == SELECTED_STARTER_INFANTRY,
        "selected starter-infantry drift",
    )
    _require(
        selected.get("staging_max_ticks") == SELECTED_STAGING_MAX_TICKS,
        "selected staging-max-ticks drift",
    )
    _require(
        selected.get("opponent_role") == SELECTED_OPPONENT_ROLE,
        "selected opponent role drift",
    )
    _require(
        selected.get("opponent_snapshot_id") == SELECTED_OPPONENT_SNAPSHOT_ID,
        "selected opponent snapshot id drift",
    )
    _require(
        selected.get("opponent_snapshot_sha256")
        == SELECTED_OPPONENT_SNAPSHOT_SHA256,
        "selected opponent snapshot SHA drift",
    )
    binding = selected.get("pair_binding")
    _require(isinstance(binding, dict), "selected pair binding missing")
    for field in (
        "same_abaddon_doctrine",
        "same_opponent_snapshot",
        "same_round_limit",
        "same_seed",
        "same_ticks_per_round",
        "same_warm_start_contract_required",
    ):
        _require(binding.get(field) is True, f"selected pair binding drift: {field}")

    return deepcopy(selected)


@lru_cache(maxsize=1)
def _commands_cached() -> dict[str, dict[str, Any]]:
    commands = {
        arm: command_materializer.materialize_command(
            pair_slot=SELECTED_PAIR_SLOT,
            arm=arm,
        )
        for arm in ("baseline", "candidate")
    }
    for arm, command in commands.items():
        _require(
            command.get("pair_slot") == SELECTED_PAIR_SLOT,
            f"{arm} pair-slot drift",
        )
        _require(command.get("arm") == arm, f"{arm} arm drift")
        _require(
            command.get("runtime_execution_authorized") is False,
            f"{arm} command carries runtime authority",
        )
        _require(
            command.get("runtime_started") is False,
            f"{arm} runtime already started",
        )
        _require(
            command.get("command_execution_performed") is False,
            f"{arm} command already executed",
        )
        _require(
            command.get("model_inference_performed") is False,
            f"{arm} inference already performed",
        )
        _require(
            command.get("game_execution_performed") is False,
            f"{arm} game already executed",
        )
        _require(
            command.get("training_performed") is False,
            f"{arm} training already performed",
        )
        _require(
            command.get("weights_updated") is False,
            f"{arm} weights already updated",
        )

    _require(
        tuple(commands["baseline"]["runner_argv"])
        == tuple(commands["candidate"]["runner_argv"]),
        "pair06 matched runner argv drift",
    )
    _require(
        commands["baseline"]["runtime_selection_key"]
        == SELECTED_OPPONENT_SNAPSHOT_ID,
        "pair06 baseline runtime selection drift",
    )
    _require(
        commands["candidate"]["runtime_selection_key"]
        == SELECTED_OPPONENT_SNAPSHOT_ID,
        "pair06 candidate runtime selection drift",
    )
    _require(
        commands["baseline"]["opponent_snapshot_sha256"]
        == SELECTED_OPPONENT_SNAPSHOT_SHA256,
        "pair06 baseline snapshot SHA drift",
    )
    _require(
        commands["candidate"]["opponent_snapshot_sha256"]
        == SELECTED_OPPONENT_SNAPSHOT_SHA256,
        "pair06 candidate snapshot SHA drift",
    )
    return deepcopy(commands)


def v2r13_pair06_nonheldout_allocation_contract() -> dict[str, Any]:
    post_pair09 = _post_pair09_cached()
    selected = _selected_row_cached()
    commands = _commands_cached()

    _require(
        tuple(bounded_executor.AUTHORIZED_PAIR_SLOTS) == (3, 9, 15),
        "current V2R13 authorized pair-slot set drift",
    )
    _require(
        tuple(bounded_executor.HELD_OUT_PAIR_SLOTS) == (15,),
        "current V2R13 held-out pair-slot set drift",
    )
    _require(
        SELECTED_PAIR_SLOT not in bounded_executor.AUTHORIZED_PAIR_SLOTS,
        "pair06 unexpectedly already executable",
    )
    _require(
        SELECTED_PAIR_SLOT not in bounded_executor.HELD_OUT_PAIR_SLOTS,
        "pair06 unexpectedly held-out",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "post_pair09_review_git_blob": POST_PAIR09_REVIEW_GIT_BLOB,
        "campaign_plan_git_blob": CAMPAIGN_PLAN_GIT_BLOB,
        "plan_fixture_git_blob": PLAN_FIXTURE_GIT_BLOB,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "bounded_executor_git_blob": BOUNDED_EXECUTOR_GIT_BLOB,
        "new_nonheldout_allocation_selected": True,
        "selection_rule": (
            "lowest_unused_nonheldout_historical_control_pair_slot"
        ),
        "completed_nonheldout_pair_slots": COMPLETED_NONHELDOUT_PAIR_SLOTS,
        "eligible_unused_historical_control_pair_slots": (
            ELIGIBLE_UNUSED_HISTORICAL_CONTROL_PAIR_SLOTS
        ),
        "selected_pair_slot": SELECTED_PAIR_SLOT,
        "selected_seed": SELECTED_SEED,
        "selected_rounds": SELECTED_ROUNDS,
        "selected_ticks_per_round": SELECTED_TICKS_PER_ROUND,
        "selected_starter_infantry": SELECTED_STARTER_INFANTRY,
        "selected_staging_max_ticks": SELECTED_STAGING_MAX_TICKS,
        "selected_held_out": False,
        "selected_opponent_role": SELECTED_OPPONENT_ROLE,
        "selected_opponent_snapshot_id": SELECTED_OPPONENT_SNAPSHOT_ID,
        "selected_opponent_snapshot_sha256": (
            SELECTED_OPPONENT_SNAPSHOT_SHA256
        ),
        "matched_baseline_candidate_required": True,
        "matched_runner_argv": tuple(commands["baseline"]["runner_argv"]),
        "baseline_command": deepcopy(commands["baseline"]),
        "candidate_command": deepcopy(commands["candidate"]),
        "canonical_pair_row": deepcopy(selected),
        "bounded_executor_current_pair_slots": (3, 9, 15),
        "bounded_executor_current_held_out_pair_slots": (15,),
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
        "post_pair09_design_review": deepcopy(post_pair09),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_pair06(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair06NonheldoutAllocationHold(
        "V2R13_PAIR06_RUNTIME_EXECUTION_NOT_AUTHORIZED"
    )


def execute_pair15(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair06NonheldoutAllocationHold(
        "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair06NonheldoutAllocationHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
