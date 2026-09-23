"""CLI entrypoint for the reviewed pair-06 proto/gRPC game child.

Import and contract inspection are inert. Operational execution requires the
exact confirmation token and an inherited socket file descriptor. This module
creates no socketpair and grants no authority by itself.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import socket
import sys
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_source_binding_review_generation2
    as child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as child,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-proto-game-child-entrypoint-contract.v1"
)
CONFIRM_TOKEN = "VOID_PAIR06_V8_PROTO_GAME_CHILD_EXECUTE_ONCE"
PROTO_PYTHON = Path(
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)

NEXT_GATE = "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_launcher_supervisor_implementation"


class Pair06V8ProtoChildEntrypointHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ProtoChildEntrypointHold(message)


def _review() -> dict[str, Any]:
    reviewed = child_review.pair06_v8_proto_game_child_review_contract()
    _require(
        reviewed.get("pair06_v8_proto_game_child_reviewed") is True,
        "pair06 proto game child not reviewed",
    )
    _require(reviewed.get("pair_slot") == 6, "pair06 child slot drift")
    _require(reviewed.get("arm") == "baseline", "pair06 child arm drift")
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED",
        "pair06 child entrypoint frontier drift",
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
    return value


def main(argv: list[str] | None = None) -> int:
    _review()
    args = parser().parse_args(argv)
    _require(args.confirm == CONFIRM_TOKEN, "pair06 child confirmation token required")
    _require(args.fd >= 3, "pair06 child inherited fd invalid")
    _require(Path(sys.executable) == PROTO_PYTHON, "pair06 child exact proto Python required")
    _require(
        isinstance(args.attempt_id, str)
        and len(args.attempt_id) == 64
        and all(ch in "0123456789abcdef" for ch in args.attempt_id),
        "pair06 child attempt_id invalid",
    )

    sock = socket.socket(fileno=args.fd)
    sock.settimeout(360.0)
    try:
        child.run_pair06_v8_proto_game_child(
            sock=sock,
            attempt_id=args.attempt_id,
            runs_root=args.runs_root,
            frozen_source_root=args.frozen_source_root,
            exact_engine_root=args.exact_engine_root,
            execution_authorized=True,
        )
    finally:
        sock.close()
    return 0


def pair06_v8_proto_game_child_entrypoint_contract() -> dict[str, Any]:
    reviewed = _review()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_proto_game_child_entrypoint_implemented": True,
        "pair_slot": 6,
        "arm": "baseline",
        "proto_python": str(PROTO_PYTHON),
        "inherited_fd_required": True,
        "socketpair_created_by_entrypoint": False,
        "exact_confirmation_token_required": True,
        "execution_performed_by_contract_inspection": False,
        "child_spawn_performed_by_entrypoint": False,
        "model_load_performed_by_entrypoint": False,
        "reviewed_child": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


if __name__ == "__main__":
    raise SystemExit(main())
