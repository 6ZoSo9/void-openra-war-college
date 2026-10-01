"""CLI entrypoint for the reviewed Pair-06 V9 input-order-coherent proto child.

Import and contract inspection are inert. Operational execution requires three
distinct confirmations:
* the existing exact Pair-06 child execution token;
* the reviewed V9 strict-visible-contact policy activation token;
* a separate input-order-coherence activation token.

The entrypoint consumes only an inherited socket file descriptor. It creates no
socketpair, loads no model, creates no durable attempt claim or execution
request, and grants no authority by contract inspection.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import socket
import sys
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2
    as legacy_entrypoint,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_generation2
    as order_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_source_binding_review_generation2
    as order_child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_game_child_entrypoint_generation2
    as historical_v9_entrypoint,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "proto-child-entrypoint-contract.v1"
)

CONFIRM_TOKEN = legacy_entrypoint.CONFIRM_TOKEN
POLICY_CONFIRM_TOKEN = historical_v9_entrypoint.POLICY_CONFIRM_TOKEN
ORDER_CONFIRM_TOKEN = "VOID_PAIR06_V9_INPUT_ORDER_COHERENCE_ACTIVATE_ONCE"
PROTO_PYTHON = legacy_entrypoint.PROTO_PYTHON

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "parent_supervisor_wiring"
)


class Pair06V9InputOrderCoherenceChildEntrypointHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceChildEntrypointHold(message)


def _review() -> dict[str, Any]:
    reviewed = (
        order_child_review
        .pair06_v9_input_order_coherence_proto_child_wiring_review_contract()
    )

    _require(
        reviewed.get(
            "pair06_v9_input_order_coherence_proto_child_wiring_reviewed"
        )
        is True,
        "V9 input-order proto-child wiring not reviewed",
    )
    _require(
        reviewed.get("historical_v9_proto_child_source_modified") is False
        and reviewed.get("existing_v8_proto_child_source_modified") is False,
        "V9 input-order child historical source drift",
    )
    _require(
        reviewed.get("original_child_execution_authorization_gate_preserved")
        is True
        and reviewed.get("historical_v9_policy_activation_gate_preserved")
        is True
        and reviewed.get("additional_order_coherence_activation_gate_required")
        is True,
        "V9 input-order child authorization-gate drift",
    )
    _require(
        reviewed.get("order_coherent_decision_hook_reviewed") is True
        and reviewed.get("membership_drift_still_fail_closed") is True,
        "V9 input-order child decision boundary drift",
    )
    _require(
        reviewed.get("consumed_v9_attempt_retry_authorized") is False
        and reviewed.get("new_execution_request_opened") is False
        and reviewed.get("attempt_created") is False
        and reviewed.get("runtime_execution_authorized") is False,
        "V9 input-order child unexpectedly grants execution lineage",
    )
    _require(
        reviewed.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "V9 input-order child entrypoint frontier drift",
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
    value.add_argument("--order-confirm", required=True)
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
        "pair06 V9 strict-contact policy activation token required",
    )
    _require(
        args.order_confirm == ORDER_CONFIRM_TOKEN,
        "pair06 V9 input-order coherence activation token required",
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
        order_child.run_pair06_v9_input_order_coherence_proto_game_child(
            sock=sock,
            attempt_id=args.attempt_id,
            runs_root=args.runs_root,
            frozen_source_root=args.frozen_source_root,
            exact_engine_root=args.exact_engine_root,
            policy_activation_authorized=True,
            order_coherence_activation_authorized=True,
            execution_authorized=True,
        )
    finally:
        sock.close()

    return 0


def pair06_v9_input_order_coherence_child_entrypoint_contract() -> dict[str, Any]:
    reviewed = _review()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v9_input_order_coherence_child_entrypoint_implemented": True,
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "proto_python": str(PROTO_PYTHON),
        "inherited_fd_required": True,
        "socketpair_created_by_entrypoint": False,
        "existing_execution_confirmation_token_required": True,
        "historical_v9_policy_activation_token_required": True,
        "separate_order_coherence_activation_token_required": True,
        "all_confirmation_tokens_distinct": (
            len({CONFIRM_TOKEN, POLICY_CONFIRM_TOKEN, ORDER_CONFIRM_TOKEN}) == 3
        ),
        "reviewed_order_coherent_proto_child_wiring_required": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "consumed_v9_attempt_retry_authorized": False,
        "child_spawn_performed_by_entrypoint": False,
        "model_load_performed_by_entrypoint": False,
        "attempt_claim_created_by_entrypoint": False,
        "execution_request_created_by_entrypoint": False,
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
        "scheduler_mutation_authorized": False,
        "reviewed_child_wiring": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


if __name__ == "__main__":
    raise SystemExit(main())
