"""Source-only identity binding for the deterministic scout-canary opponent.

This review fixes the exact opponent proposal source selected after the canary
seed was derived. It does not import or execute the opponent module, validate a
host command, choose a runtime image, create an attempt marker, or authorize a
game. A future accepted-main review must independently verify the committed blob.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import abaddon_scout_repair_canary_source_design_v1 as source_design

SCHEMA = "void.abaddon.scout-repair-canary-opponent-source-binding-review.v1"
NEXT_GATE = "SCOUT_REPAIR_ACCEPTED_MAIN_AND_ATTEMPT_GUARD_DESIGN_REQUIRED"
OPPONENT_PATH = "openra_env/learning/abaddon_scout_canary_opponent_v1.py"
OPPONENT_GIT_BLOB = "d643e41f0436897ad03dc73086c44bb36c601ed6"
OPPONENT_SHA256 = "d602ba95d9a079e82ffc87cad22c8e6839ee5fdf1ccc910672018249359be66f"


class ScoutRepairOpponentSourceBindingHold(ValueError):
    pass


def scout_repair_opponent_source_binding_review() -> dict[str, Any]:
    prior = source_design.scout_repair_canary_source_design()
    opponent = prior.get("opponent")
    if not isinstance(opponent, dict):
        raise ScoutRepairOpponentSourceBindingHold("opponent_design_missing")
    if opponent.get("deterministic_required") is not True or opponent.get("model_backed") is not False:
        raise ScoutRepairOpponentSourceBindingHold("opponent_design_not_deterministic_non_model")
    if opponent.get("source_identity") is not None or opponent.get("implementation") is not None:
        raise ScoutRepairOpponentSourceBindingHold("opponent_prematurely_bound")
    if prior.get("execution_authorized") is not False or prior.get("execution_performed") is not False:
        raise ScoutRepairOpponentSourceBindingHold("prior_design_carries_authority")
    return {
        **deepcopy(prior),
        "schema": SCHEMA,
        "opponent": {
            "implementation": "deterministic_pressure_opponent_v1",
            "source_identity": {
                "path": OPPONENT_PATH,
                "git_blob": OPPONENT_GIT_BLOB,
                "sha256": OPPONENT_SHA256,
                "committed_on_accepted_main_verified": False,
            },
            "model_backed": False,
            "deterministic_required": True,
            "same_for_both_arms": True,
            "proposal_only": True,
            "unchanged_host_validation_required": True,
            "execution_authority": False,
        },
        "opponent_source_reviewed": True,
        "accepted_main_head_with_repair": None,
        "execution_authorized": False,
        "execution_performed": False,
        "automatic_retry": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairOpponentSourceBindingHold(NEXT_GATE)
