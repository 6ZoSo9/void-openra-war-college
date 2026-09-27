"""CLI entrypoint for the reviewed pair-06 combat-priority V2 proto child.

This entrypoint preserves the existing pair-06 child execution confirmation
token and the separate combat-priority policy-activation token. It delegates
only to the reviewed V2 legality-coherent proto-child wiring.

Import and contract inspection are inert. No retry or execution authority is
granted by inspection.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import socket
import sys
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_child_wiring_generation2
    as v2_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_child_wiring_source_binding_review_generation2
    as v2_child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_game_child_entrypoint_generation2
    as v1_entrypoint,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-v2-"
    "proto-game-child-entrypoint-contract.v1"
)

CONFIRM_TOKEN = v1_entrypoint.CONFIRM_TOKEN
POLICY_CONFIRM_TOKEN = v1_entrypoint.POLICY_CONFIRM_TOKEN
PROTO_PYTHON = v1_entrypoint.PROTO_PYTHON

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
)
FAILED_RUN_ID = (
    "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_v2_parent_supervisor_wiring"
)


class Pair06V8CombatPriorityCoherentV2ChildEntrypointHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentV2ChildEntrypointHold(message)


def _review() -> dict[str, Any]:
    out = (
        v2_child_review
        .pair06_v8_combat_priority_coherent_v2_proto_child_wiring_review_contract()
    )
    _require(
        out.get(
            "pair06_v8_combat_priority_coherent_v2_proto_child_wiring_reviewed"
        )
        is True,
        "V2 combat-priority proto-child wiring not reviewed",
    )
    for field in (
        "v2_repaired_decision_hook_bound",
        "production_functions_filtered_to_offered_surface_by_v1",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "translator_legal_building_mapping_coherent",
        "translator_legal_unit_mapping_coherent",
        "existing_child_execution_authorization_gate_preserved",
        "existing_policy_activation_authorization_gate_preserved",
    ):
        _require(out.get(field) is True, "V2 child review invariant drift: " + field)

    _require(
        out.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_attempt_reusable") is False,
        "consumed V2 precursor attempt lineage drift",
    )
    _require(
        out.get("failed_run_id") == FAILED_RUN_ID
        and out.get("failed_run_reusable_as_authority") is False
        and out.get("prior_authorization_reusable") is False,
        "consumed V2 precursor run/authorization drift",
    )
    _require(
        out.get("attempt_retry_authorized") is False
        and out.get("runtime_execution_authorized") is False
        and out.get("automatic_retry") is False,
        "V2 child review unexpectedly grants runtime authority",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "V2 child entrypoint frontier drift",
    )
    return out


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(add_help=False)
    value.add_argument("--fd", type=int, required=True)
    value.add_argument("--attempt-id", required=True)
    value.add_argument("--runs-root", required=True)
    value.add_argument("--frozen-source-root", required=True)
    value.add_argument("--exact-engine-root", required=True)
    value.add_argument("--confirm", required=True)
    value.add_argument("--policy-confirm", required=True)
    return value


def main(argv: list[str] | None = None) -> int:
    _review()
    args = parser().parse_args(argv)

    _require(
        args.confirm == CONFIRM_TOKEN,
        "pair06 child execution confirmation token required",
    )
    _require(
        args.policy_confirm == POLICY_CONFIRM_TOKEN,
        "pair06 combat-priority policy activation token required",
    )
    _require(args.fd >= 3, "pair06 child inherited fd invalid")
    _require(
        Path(sys.executable) == PROTO_PYTHON,
        "pair06 child exact proto Python required",
    )
    _require(
        isinstance(args.attempt_id, str)
        and len(args.attempt_id) == 64
        and all(ch in "0123456789abcdef" for ch in args.attempt_id),
        "pair06 child attempt_id invalid",
    )

    sock = socket.socket(fileno=args.fd)
    sock.settimeout(360.0)
    try:
        v2_child.run_pair06_v8_combat_priority_coherent_v2_proto_game_child(
            sock=sock,
            attempt_id=args.attempt_id,
            runs_root=args.runs_root,
            frozen_source_root=args.frozen_source_root,
            exact_engine_root=args.exact_engine_root,
            policy_activation_authorized=True,
            execution_authorized=True,
        )
    finally:
        sock.close()
    return 0


def pair06_v8_combat_priority_coherent_v2_child_entrypoint_contract() -> dict[str, Any]:
    reviewed = _review()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_combat_priority_coherent_v2_child_entrypoint_implemented": True,
        "pair_slot": 6,
        "arm": "baseline",
        "proto_python": str(PROTO_PYTHON),
        "inherited_fd_required": True,
        "socketpair_created_by_entrypoint": False,
        "existing_execution_confirmation_token_required": True,
        "existing_policy_activation_confirmation_token_required": True,
        "execution_and_policy_confirmation_tokens_distinct": (
            CONFIRM_TOKEN != POLICY_CONFIRM_TOKEN
        ),
        "v2_proto_child_wiring_reviewed": True,
        "production_functions_filtered_to_offered_surface_by_v1": True,
        "legal_buildings_reconstructed_from_remaining_production": True,
        "legal_units_reconstructed_from_remaining_production": True,
        "translator_legal_building_mapping_coherent": True,
        "translator_legal_unit_mapping_coherent": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
        "failed_run_id": FAILED_RUN_ID,
        "failed_run_reusable_as_authority": False,
        "prior_authorization_reusable": False,
        "attempt_retry_authorized": False,
        "child_spawn_performed_by_entrypoint": False,
        "model_load_performed_by_entrypoint": False,
        "execution_performed_by_contract_inspection": False,
        "runtime_activation_authorized_by_contract_inspection": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_child_wiring": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


if __name__ == "__main__":
    raise SystemExit(main())
