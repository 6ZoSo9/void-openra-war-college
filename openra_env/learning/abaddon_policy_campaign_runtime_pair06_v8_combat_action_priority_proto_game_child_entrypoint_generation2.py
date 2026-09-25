"""CLI entrypoint for the reviewed pair-06 combat-priority proto child.

Import and contract inspection are inert. Operational execution requires:
* the existing exact pair-06 child execution confirmation token;
* a second exact combat-priority policy activation token;
* an inherited socket file descriptor.

This entrypoint creates no socketpair, loads no model, and grants no authority
by contract inspection.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import socket
import sys
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_generation2
    as child_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_source_binding_review_generation2
    as child_wiring_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2
    as legacy_entrypoint,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-proto-child-entrypoint-contract.v1"
)

CONFIRM_TOKEN = legacy_entrypoint.CONFIRM_TOKEN
POLICY_CONFIRM_TOKEN = "VOID_PAIR06_V8_COMBAT_PRIORITY_POLICY_ACTIVATE_ONCE"
PROTO_PYTHON = legacy_entrypoint.PROTO_PYTHON

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_parent_supervisor_wiring"
)


class Pair06V8CombatPriorityChildEntrypointHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityChildEntrypointHold(message)


def _review() -> dict[str, Any]:
    reviewed = (
        child_wiring_review
        .pair06_v8_combat_action_priority_proto_child_wiring_review_contract()
    )
    _require(
        reviewed.get(
            "pair06_v8_combat_action_priority_proto_child_wiring_reviewed"
        )
        is True,
        "pair06 combat-priority proto-child wiring not reviewed",
    )
    _require(
        reviewed.get("existing_proto_child_source_modified") is False,
        "pair06 reviewed proto-child source unexpectedly modified",
    )
    _require(
        reviewed.get("additional_policy_activation_gate_required") is True,
        "pair06 policy activation gate missing",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_REQUIRED",
        "pair06 combat-priority child entrypoint frontier drift",
    )
    return reviewed


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
        child_wiring.run_pair06_v8_combat_priority_proto_game_child(
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


def pair06_v8_combat_priority_proto_child_entrypoint_contract() -> dict[str, Any]:
    reviewed = _review()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_combat_priority_proto_child_entrypoint_implemented": True,
        "pair_slot": 6,
        "arm": "baseline",
        "proto_python": str(PROTO_PYTHON),
        "inherited_fd_required": True,
        "socketpair_created_by_entrypoint": False,
        "existing_execution_confirmation_token_required": True,
        "separate_policy_activation_token_required": True,
        "policy_activation_token_distinct_from_execution_token": (
            POLICY_CONFIRM_TOKEN != CONFIRM_TOKEN
        ),
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
