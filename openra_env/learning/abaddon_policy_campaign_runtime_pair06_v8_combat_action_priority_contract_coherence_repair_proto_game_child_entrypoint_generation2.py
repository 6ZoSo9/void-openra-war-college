"""CLI entrypoint for the repaired pair-06 combat-priority proto child.

Import and contract inspection are inert. Operational execution requires the
existing pair-06 child execution confirmation token, the separate
combat-priority policy activation token, and an inherited socket descriptor.

The historical combat-priority entrypoint remains unchanged. This entrypoint
delegates only to the reviewed coherent proto-child wiring.

No retry or execution authority is granted by contract inspection.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import socket
import sys
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_generation2
    as coherent_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_source_binding_review_generation2
    as coherent_child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_game_child_entrypoint_generation2
    as historical_entrypoint,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-priority-contract-coherence-repair-"
    "proto-game-child-entrypoint-contract.v1"
)

CONFIRM_TOKEN = historical_entrypoint.CONFIRM_TOKEN
POLICY_CONFIRM_TOKEN = historical_entrypoint.POLICY_CONFIRM_TOKEN
PROTO_PYTHON = historical_entrypoint.PROTO_PYTHON

CONSUMED_ATTEMPT_MARKER_SHA256 = (
    "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_contract_coherence_"
    "repair_parent_supervisor_wiring"
)


class Pair06V8CombatPriorityCoherentChildEntrypointHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityCoherentChildEntrypointHold(message)


def _review() -> dict[str, Any]:
    out = (
        coherent_child_review
        .pair06_v8_combat_priority_coherent_proto_child_wiring_review_contract()
    )
    _require(
        out.get("pair06_v8_combat_priority_coherent_proto_child_wiring_reviewed")
        is True,
        "coherent combat-priority proto-child wiring not reviewed",
    )
    _require(
        out.get("repaired_decision_hook_bound") is True
        and out.get("production_functions_filtered_to_offered_surface") is True,
        "coherent combat-priority repair binding drift",
    )
    _require(
        out.get("existing_child_execution_authorization_gate_preserved") is True
        and out.get("existing_policy_activation_authorization_gate_preserved")
        is True,
        "coherent child authorization gate drift",
    )
    _require(
        out.get("consumed_attempt_marker_sha256")
        == CONSUMED_ATTEMPT_MARKER_SHA256
        and out.get("consumed_attempt_reusable") is False,
        "consumed attempt lineage drift",
    )
    _require(
        out.get("attempt_retry_authorized") is False
        and out.get("runtime_execution_authorized") is False,
        "coherent child review unexpectedly grants runtime authority",
    )
    _require(
        out.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "coherent child entrypoint frontier drift",
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
        coherent_child.run_pair06_v8_combat_priority_coherent_proto_game_child(
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


def pair06_v8_combat_priority_coherent_child_entrypoint_contract() -> dict[str, Any]:
    reviewed = _review()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_combat_priority_coherent_child_entrypoint_implemented": True,
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
        "coherent_proto_child_wiring_reviewed": True,
        "production_functions_filtered_to_offered_surface": True,
        "consumed_attempt_marker_sha256": CONSUMED_ATTEMPT_MARKER_SHA256,
        "consumed_attempt_reusable": False,
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
