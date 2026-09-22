"""Source-only design for the next bounded V2R13 pair-09 evaluation.

Pair 03 was inconclusive and its candidate was preserved. This design selects
the already-canonical pair-09 baseline/candidate command materialization and
requires baseline-first matched evaluation semantics without authorizing either
arm to execute.

Historical six-arm V2R13 implementation authority is treated only as reusable
capability. It is not sufficient current policy authority for pair-09 execution.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2
    as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as bounded_executor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_policy_disposition_source_binding_review_generation2
    as disposition_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-evaluation-design-contract.v1"
)

DISPOSITION_REVIEW_GIT_BLOB = "ff606911ce35499b0fd6d25eb10591fc80b0c338"
DISPOSITION_REVIEW_SOURCE_SHA256 = (
    "ab7fbc0be7b6f4a960d2a7f75f1ceeb6e111c6737a546e672098c74bb8c33fb9"
)
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
BOUNDED_EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"

PAIR_SLOT = 9
ARMS = ("baseline", "candidate")
HELD_OUT = False

NEXT_GATE = "V2R13_PAIR09_EVALUATION_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair09_evaluation_design_source_binding_review"


class V2R13Pair09EvaluationDesignHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09EvaluationDesignHold(message)


@lru_cache(maxsize=1)
def _disposition_cached() -> dict[str, Any]:
    contract = disposition_review.v2r13_pair03_candidate_policy_disposition_review_contract()
    _require(contract.get("policy_disposition_reviewed") is True, "pair03 disposition not reviewed")
    _require(
        contract.get("policy_disposition")
        == "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION",
        "pair03 disposition drift",
    )
    _require(contract.get("candidate_preserved_as_evidence") is True, "pair03 candidate not preserved")
    _require(contract.get("candidate_promoted") is False, "pair03 candidate unexpectedly promoted")
    _require(contract.get("candidate_rejected") is False, "pair03 candidate unexpectedly rejected")
    _require(contract.get("pair09_evaluation_design_required") is True, "pair09 design not required")
    _require(contract.get("pair09_execution_authorized") is False, "pair09 execution already authorized")
    _require(contract.get("held_out_execution_authorized") is False, "held-out execution already authorized")
    _require(
        contract.get("next_gate") == "V2R13_PAIR09_EVALUATION_DESIGN_REQUIRED",
        "pair09 design frontier drift",
    )
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _commands_cached() -> dict[str, dict[str, Any]]:
    rows = {
        arm: command_materializer.materialize_command(pair_slot=PAIR_SLOT, arm=arm)
        for arm in ARMS
    }
    for arm, command in rows.items():
        _require(command.get("pair_slot") == PAIR_SLOT, f"{arm} pair-slot drift")
        _require(command.get("arm") == arm, f"{arm} arm drift")
        _require(
            command.get("workdir_token") == f"generation2/pair-{PAIR_SLOT:02d}/{arm}",
            f"{arm} workdir token drift",
        )
        _require(
            command.get("runtime_selection_key") == "apollyon-v2r13-qualified-predecessor",
            f"{arm} runtime selection drift",
        )
        _require(command.get("argv_materialized") is True, f"{arm} argv not materialized")
        _require(command.get("path_bindings_resolved") is False, f"{arm} paths unexpectedly resolved")
        _require(command.get("process_spawn_implemented") is False, f"{arm} process spawn implemented")
        _require(command.get("command_execution_performed") is False, f"{arm} command executed")
        _require(command.get("workdir_materialized") is False, f"{arm} workdir materialized")
        _require(command.get("workdir_created") is False, f"{arm} workdir created")
        _require(command.get("runtime_execution_authorized") is False, f"{arm} command carries runtime authority")
        _require(command.get("runtime_started") is False, f"{arm} runtime started")
        _require(command.get("model_inference_performed") is False, f"{arm} inference performed")
        _require(command.get("game_execution_performed") is False, f"{arm} game executed")
        _require(command.get("training_performed") is False, f"{arm} training performed")
        _require(command.get("weights_updated") is False, f"{arm} weights updated")

    _require(
        tuple(rows["baseline"]["runner_argv"]) == tuple(rows["candidate"]["runner_argv"]),
        "pair09 matched arms do not share runner argv",
    )
    return deepcopy(rows)


def v2r13_pair09_evaluation_design_contract() -> dict[str, Any]:
    disposition = _disposition_cached()
    commands = _commands_cached()

    _require(PAIR_SLOT in bounded_executor.AUTHORIZED_PAIR_SLOTS, "pair09 absent from bounded implementation")
    _require(PAIR_SLOT not in bounded_executor.HELD_OUT_PAIR_SLOTS, "pair09 unexpectedly held-out")

    return {
        "schema": CONTRACT_SCHEMA,
        "disposition_review_git_blob": DISPOSITION_REVIEW_GIT_BLOB,
        "disposition_review_source_sha256": DISPOSITION_REVIEW_SOURCE_SHA256,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "bounded_executor_git_blob": BOUNDED_EXECUTOR_GIT_BLOB,
        "pair09_evaluation_design_implemented": True,
        "pair09_evaluation_design_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arms": ARMS,
        "held_out": HELD_OUT,
        "baseline_first": True,
        "baseline_must_complete_before_candidate": True,
        "matched_pair_runner_argv_required": True,
        "matched_pair_runner_argv": tuple(commands["baseline"]["runner_argv"]),
        "candidate_policy_preserved_from_pair03": True,
        "candidate_policy_promoted": False,
        "candidate_policy_rejected": False,
        "legacy_six_arm_authorization_sufficient_for_pair09": False,
        "historical_bounded_executor_capability_reusable": True,
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
        "baseline_command": deepcopy(commands["baseline"]),
        "candidate_command": deepcopy(commands["candidate"]),
        "pair03_disposition_review": deepcopy(disposition),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09EvaluationDesignHold(
        "V2R13_PAIR09_BASELINE_EXECUTION_NOT_AUTHORIZED"
    )


def execute_pair09_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09EvaluationDesignHold(
        "V2R13_PAIR09_CANDIDATE_EXECUTION_NOT_AUTHORIZED"
    )


def execute_held_out_pair(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09EvaluationDesignHold(
        "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )
