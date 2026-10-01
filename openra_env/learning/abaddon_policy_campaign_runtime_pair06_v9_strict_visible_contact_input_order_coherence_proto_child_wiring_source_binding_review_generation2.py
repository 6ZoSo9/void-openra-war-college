"""Exact-blob review of V9 input-order-coherence proto-child wiring.

Pins the source-only child wiring and focused regression suite. The review
confirms that the advanced decision hook is bound through a call-scoped copy of
the exact V8 child run function globals, while the process-global V8 child hook
factory and run function remain unchanged.

The historical V9 policy-activation gate, original child execution gate, and
new input-order-coherence activation gate remain explicit. The consumed V9
attempt remains non-retryable. No parent-supervisor or operator wiring, runtime
activation, execution, replay, training, promotion, deployment, chain,
wallet/funds, or scheduler authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_generation2
    as wiring,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "proto-child-wiring-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "8326cb623d384bcdda37ee8b3c69b942ebfbbcf0"

WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "proto_child_wiring_generation2.py"
)
WIRING_GIT_BLOB = "1b87cb5596c219e6118f4b69845dbecaa29a3ace"

WIRING_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "proto_child_wiring_generation2.py"
)
WIRING_TEST_GIT_BLOB = "37140f7626a0520249cf9704d7d508a60992d6bc"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "parent_supervisor_wiring"
)


class Pair06V9InputOrderCoherenceProtoChildWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceProtoChildWiringReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = wiring.pair06_v9_input_order_coherence_proto_child_wiring_contract()

    _require(
        out.get("input_order_coherence_proto_child_wiring_implemented") is True,
        "V9 input-order proto-child wiring missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 input-order proto-child scope drift",
    )

    for field in (
        "historical_v9_proto_child_hook_subclass_reused",
        "order_coherent_decision_hook_bound",
        "historical_v8_child_run_code_reused",
        "call_scoped_child_hook_factory_binding_implemented",
        "original_child_execution_authorization_gate_preserved",
        "historical_v9_policy_activation_gate_preserved",
        "additional_order_coherence_activation_gate_required",
        "reviewed_order_coherent_decision_hook_used",
        "typed_tool_membership_exact_match_required",
        "typed_tool_order_canonicalized_to_offered_order",
        "membership_drift_still_fail_closed",
        "existing_ipc_decider_reused",
        "existing_legacy_runner_reused",
        "existing_portable_worktree_binding_reused",
    ):
        _require(
            out.get(field) is True,
            "V9 input-order proto-child invariant drift: " + field,
        )

    for field in (
        "historical_v9_proto_child_source_modified",
        "existing_v8_proto_child_source_modified",
        "process_global_child_hook_factory_mutated",
        "process_global_child_run_function_mutated",
        "new_concurrency_scope_leak_introduced",
        "consumed_v9_attempt_retry_authorized",
        "parent_supervisor_repair_wiring_implemented",
        "operator_repair_wiring_implemented",
        "new_execution_request_opened",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "V9 input-order proto-child authority/global drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 input-order proto-child review frontier drift",
    )

    root = Path(__file__).parents[2]
    wiring_path = root / WIRING_PATH
    test_path = root / WIRING_TEST_PATH
    _require(wiring_path.is_file(), "V9 input-order proto-child source missing")
    _require(test_path.is_file(), "V9 input-order proto-child test missing")
    _require(
        _git_blob_sha1(wiring_path.read_bytes()) == WIRING_GIT_BLOB,
        "V9 input-order proto-child source blob drift",
    )
    _require(
        _git_blob_sha1(test_path.read_bytes()) == WIRING_TEST_GIT_BLOB,
        "V9 input-order proto-child test blob drift",
    )

    return deepcopy(out)


def pair06_v9_input_order_coherence_proto_child_wiring_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "wiring_path": WIRING_PATH,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_test_path": WIRING_TEST_PATH,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "pair06_v9_input_order_coherence_proto_child_wiring_reviewed": True,
        "policy_id": validated["policy_id"],
        "historical_v9_proto_child_source_modified": False,
        "existing_v8_proto_child_source_modified": False,
        "historical_v8_child_run_code_reused_reviewed": True,
        "call_scoped_child_hook_factory_binding_reviewed": True,
        "process_global_child_hook_factory_mutated": False,
        "process_global_child_run_function_mutated": False,
        "new_concurrency_scope_leak_introduced": False,
        "original_child_execution_authorization_gate_preserved": True,
        "historical_v9_policy_activation_gate_preserved": True,
        "additional_order_coherence_activation_gate_required": True,
        "order_coherent_decision_hook_reviewed": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "consumed_v9_attempt_retry_authorized": False,
        "parent_supervisor_repair_wiring_implemented": False,
        "operator_repair_wiring_implemented": False,
        "new_execution_request_opened": False,
        "attempt_created": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_wiring": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceProtoChildWiringReviewHold(NEXT_GATE)
