"""Source-only V9 strict-visible-contact proposal for pair-06.

The reviewed V8 combat-priority envelope retains train_unit_* functions during
VISIBLE_CONTACT alongside engagement and tactical-control functions. The exact
successful V8 V2-coherent run completed all 36 rounds and ended
DRAW_OR_UNFINISHED.

That result does not prove reinforcement selection caused the draw. This module
therefore records only a bounded hypothesis: during current visible contact,
remove reinforcement-production choices from the model-facing tool surface so
the decision must stay inside engagement and tactical-control actions. Zero-
combat recovery remains unchanged and NORMAL mode remains identity-preserving.

This module is pure. It does not call a model, host validator, game runtime,
service, process, network, training pipeline, deployment path, VOID chain,
wallet, signer, transaction, or funds backend.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any, Iterable

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_policy_source_binding_review_generation2
    as v8_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_source_binding_review_generation2
    as success_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-policy-proposal-contract.v1"
)

V8_POLICY_REVIEW_GIT_BLOB = "6b53ca134325e57d89066894636eb7d574bd3af3"
V8_SUCCESS_REVIEW_GIT_BLOB = "149b04e687d16d797603701089846804a384b7ae"

POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
BASELINE_POLICY_ID = "pair06-v8-combat-action-priority-envelope-v1"

RECOVERY_PREFIX = "train_unit_"
ENGAGEMENT_TOOLS = frozenset({
    "attack_target",
    "move_units",
    "attack_move",
})
TACTICAL_CONTROL_TOOLS = frozenset({
    "set_stance",
    "stop_units",
    "guard_target",
})

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_PROPOSAL_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_policy_proposal_review"
)


class Pair06V9StrictVisibleContactProposalHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactProposalHold(message)


@lru_cache(maxsize=1)
def _validated_basis() -> dict[str, Any]:
    v8 = v8_review.pair06_v8_combat_action_priority_policy_review_contract()
    success = (
        success_review
        .pair06_v8_combat_priority_coherent_v2_success_review_contract()
    )

    _require(
        v8.get("pair06_v8_combat_action_priority_policy_reviewed") is True,
        "V8 combat-priority policy review missing",
    )
    _require(
        v8.get("policy_id") == BASELINE_POLICY_ID,
        "V8 policy id drift",
    )
    _require(
        v8.get("implementation_layer")
        == "pure_pre_inference_tool_surface_transform",
        "V8 intervention layer drift",
    )

    _require(
        success.get(
            "pair06_v8_combat_priority_coherent_v2_success_reviewed"
        )
        is True,
        "V8 successful-run review missing",
    )
    _require(
        success.get("pair_slot") == 6
        and success.get("arm") == "baseline"
        and success.get("rounds_completed") == 36,
        "V8 successful-run identity drift",
    )
    _require(
        success.get("outcome") == "DRAW_OR_UNFINISHED",
        "V8 successful-run outcome drift",
    )
    _require(
        success.get("attempt_consumed") is True
        and success.get("attempt_reusable") is False
        and success.get("authorization_reusable") is False,
        "V8 spent-lineage boundary drift",
    )
    _require(
        success.get("new_execution_request_opened") is False
        and success.get("retry_authorized") is False
        and success.get("training_authorized") is False
        and success.get("promotion_authorized") is False,
        "V8 closeout unexpectedly grants follow-on authority",
    )

    return {
        "v8_policy_review": deepcopy(v8),
        "v8_success_review": deepcopy(success),
    }


def _names(values: Iterable[str]) -> tuple[str, ...]:
    names = tuple(values)
    _require(
        all(isinstance(name, str) and bool(name) for name in names),
        "tool name invalid",
    )
    _require(
        len(names) == len(set(names)),
        "duplicate offered tool name",
    )
    return names


def proposed_v9_strict_visible_contact_envelope(
    *,
    combat_count: int,
    visible_enemy_count: int,
    offered_tool_names: Iterable[str],
) -> dict[str, Any]:
    """Return the proposed V9 tool surface without executing anything."""
    _validated_basis()
    _require(
        type(combat_count) is int and combat_count >= 0,
        "combat_count invalid",
    )
    _require(
        type(visible_enemy_count) is int and visible_enemy_count >= 0,
        "visible_enemy_count invalid",
    )

    offered = _names(offered_tool_names)
    offered_set = set(offered)
    recovery = tuple(
        name for name in offered if name.startswith(RECOVERY_PREFIX)
    )
    engagement = tuple(
        name for name in offered if name in ENGAGEMENT_TOOLS
    )
    tactical_controls = tuple(
        name for name in offered if name in TACTICAL_CONTROL_TOOLS
    )

    if combat_count == 0 and recovery:
        mode = "RECOVERY"
        proposed = recovery
        rationale = (
            "zero combat capacity retains V8 recovery-only production surface"
        )
    elif combat_count > 0 and visible_enemy_count > 0 and engagement:
        mode = "STRICT_VISIBLE_CONTACT"
        proposed = tuple(
            name for name in offered
            if name in ENGAGEMENT_TOOLS or name in TACTICAL_CONTROL_TOOLS
        )
        rationale = (
            "visible contact narrows choices to engagement and tactical control"
        )
    else:
        mode = "NORMAL"
        proposed = offered
        rationale = "strict visible-contact trigger absent"

    _require(bool(proposed), "proposed V9 surface unexpectedly empty")
    _require(set(proposed) <= offered_set, "V9 proposal invented tool name")

    proposed_set = set(proposed)
    return {
        "policy_id": POLICY_ID,
        "baseline_policy_id": BASELINE_POLICY_ID,
        "mode": mode,
        "rationale": rationale,
        "original_offered_tool_names": offered,
        "proposed_offered_tool_names": proposed,
        "recovery_tools": recovery,
        "engagement_tools": engagement,
        "tactical_control_tools": tactical_controls,
        "reinforcement_tools_suppressed": tuple(
            name
            for name in offered
            if name.startswith(RECOVERY_PREFIX) and name not in proposed_set
        ),
        "advance_suppressed": (
            "advance" in offered_set and "advance" not in proposed_set
        ),
        "structure_tools_suppressed": tuple(
            name
            for name in offered
            if name.startswith("build_structure_") and name not in proposed_set
        ),
        "host_validation_changed": False,
        "world_state_changed": False,
        "model_called": False,
        "model_weights_changed": False,
    }


def pair06_v9_strict_visible_contact_policy_proposal_contract() -> dict[str, Any]:
    basis = _validated_basis()
    return {
        "schema": CONTRACT_SCHEMA,
        "policy_id": POLICY_ID,
        "baseline_policy_id": BASELINE_POLICY_ID,
        "v8_policy_review_git_blob": V8_POLICY_REVIEW_GIT_BLOB,
        "v8_success_review_git_blob": V8_SUCCESS_REVIEW_GIT_BLOB,
        "pair_slot": 6,
        "arm": "baseline",
        "evidence_basis": {
            "v8_policy_retains_reinforcement_tools_in_visible_contact": True,
            "v8_v2_coherent_run_completed": True,
            "v8_v2_coherent_rounds_completed": 36,
            "v8_v2_coherent_outcome": "DRAW_OR_UNFINISHED",
            "action_level_causal_attribution_available": False,
        },
        "hypothesis": (
            "removing train_unit choices during active visible contact may "
            "reduce model choice competition and increase tactical-action rate"
        ),
        "causal_claim_made": False,
        "recovery_mode_changed": False,
        "normal_mode_changed": False,
        "visible_contact_mode_changed": True,
        "strict_visible_contact_surface": (
            "current_engagement_plus_tactical_control_functions_only"
        ),
        "reinforcement_tools_allowed_during_strict_visible_contact": False,
        "host_validation_must_remain_unchanged": True,
        "six_attempt_fail_closed_retry_must_remain_unchanged": True,
        "frozen_world_state_across_rejected_attempts_must_remain_unchanged": True,
        "typed_production_legality_must_remain_unchanged": True,
        "implementation_present": False,
        "runtime_integration_present": False,
        "new_execution_request_opened": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_basis": basis,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def implement_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactProposalHold(NEXT_GATE)
