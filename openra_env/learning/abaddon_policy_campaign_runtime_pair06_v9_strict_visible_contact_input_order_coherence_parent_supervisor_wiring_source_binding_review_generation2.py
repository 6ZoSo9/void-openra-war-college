"""Exact-blob review of the Pair-06 V9 input-order parent-supervisor gate.

This review pins the input-order child CLI entrypoint, parent-supervisor wiring,
and both focused regression suites to exact repository bytes.

The reviewed no-offload V8 parent remains unchanged. The parent execution code
is reused through a call-scoped copied globals namespace whose child-command
binding launches the reviewed order-coherent child entrypoint. Process-global
parent functions remain unchanged.

The durable attempt-claim prerequisite, CUDA:0/no-offload placement checks,
authority checks, decision service, child retirement, and receipt construction
remain intact. No operator entrypoint is wired and no execution lineage or
follow-on authority is created.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_generation2
    as parent_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "parent-supervisor-wiring-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "15f29f910751eab2ba7702851061aaa10eeab151"

CHILD_ENTRY_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "proto_game_child_entrypoint_generation2.py"
)
CHILD_ENTRY_GIT_BLOB = "bd8779f074674d089532afa889c4af86e1402d52"
CHILD_ENTRY_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "proto_game_child_entrypoint_generation2.py"
)
CHILD_ENTRY_TEST_GIT_BLOB = "fe6d35d745f910718b75c0eff88af1e38b844e79"

PARENT_WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "parent_supervisor_wiring_generation2.py"
)
PARENT_WIRING_GIT_BLOB = "607cf5ff20f46769609208a261132434ef966785"
PARENT_WIRING_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "parent_supervisor_wiring_generation2.py"
)
PARENT_WIRING_TEST_GIT_BLOB = "ae4238c7b0c134cd6f2e4ff90afa44e433122e82"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "OPERATOR_ENTRYPOINT_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_wiring"
)


class Pair06V9InputOrderCoherenceParentWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceParentWiringReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    child = child_entry.pair06_v9_input_order_coherence_child_entrypoint_contract()
    parent = parent_wiring.pair06_v9_input_order_coherence_parent_wiring_contract()

    _require(
        child.get(
            "pair06_v9_input_order_coherence_child_entrypoint_implemented"
        )
        is True,
        "V9 input-order child entrypoint missing",
    )
    _require(
        child.get("pair_slot") == 6
        and child.get("arm") == "baseline"
        and child.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 input-order child entrypoint scope drift",
    )
    for field in (
        "existing_execution_confirmation_token_required",
        "historical_v9_policy_activation_token_required",
        "separate_order_coherence_activation_token_required",
        "all_confirmation_tokens_distinct",
        "reviewed_order_coherent_proto_child_wiring_required",
        "typed_tool_membership_exact_match_required",
        "typed_tool_order_canonicalized_to_offered_order",
        "membership_drift_still_fail_closed",
    ):
        _require(
            child.get(field) is True,
            "V9 input-order child entrypoint invariant drift: " + field,
        )
    for field in (
        "consumed_v9_attempt_retry_authorized",
        "socketpair_created_by_entrypoint",
        "child_spawn_performed_by_entrypoint",
        "model_load_performed_by_entrypoint",
        "attempt_claim_created_by_entrypoint",
        "execution_request_created_by_entrypoint",
        "execution_performed_by_contract_inspection",
        "runtime_activation_authorized_by_contract_inspection",
        "automatic_retry",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            child.get(field) is False,
            "V9 input-order child entrypoint boundary drift: " + field,
        )
    _require(
        child.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED"
        ),
        "V9 input-order child entrypoint frontier drift",
    )

    _require(
        parent.get("pair_slot") == 6
        and parent.get("arm") == "baseline"
        and parent.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 input-order parent wiring scope drift",
    )
    for field in (
        "input_order_child_entrypoint_implemented",
        "historical_no_offload_parent_run_code_reused",
        "call_scoped_child_command_binding_implemented",
        "existing_execution_confirmation_token_preserved",
        "historical_v9_policy_activation_token_preserved",
        "separate_order_coherence_activation_token_added",
        "all_confirmation_tokens_distinct",
        "typed_tool_membership_exact_match_required",
        "typed_tool_order_canonicalized_to_offered_order",
        "membership_drift_still_fail_closed",
        "existing_no_offload_model_loader_reused",
        "existing_cuda0_placement_checks_reused",
        "existing_parent_decision_service_loop_reused",
        "existing_child_retirement_reused",
        "existing_parent_receipt_returned_unchanged",
        "durable_attempt_claim_required_by_existing_parent",
    ):
        _require(
            parent.get(field) is True,
            "V9 input-order parent wiring invariant drift: " + field,
        )
    for field in (
        "existing_no_offload_parent_source_modified",
        "process_global_child_command_builder_mutated",
        "process_global_parent_run_function_mutated",
        "new_concurrency_scope_leak_introduced",
        "existing_parent_automatic_retry",
        "consumed_v9_attempt_retry_authorized",
        "attempt_claim_created_by_this_wiring",
        "execution_request_created_by_this_wiring",
        "attempt_created_by_this_wiring",
        "operator_entrypoint_wiring_implemented",
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
            parent.get(field) is False,
            "V9 input-order parent wiring boundary drift: " + field,
        )
    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 input-order parent source-review frontier drift",
    )

    root = Path(__file__).parents[2]
    for path, expected in (
        (CHILD_ENTRY_PATH, CHILD_ENTRY_GIT_BLOB),
        (CHILD_ENTRY_TEST_PATH, CHILD_ENTRY_TEST_GIT_BLOB),
        (PARENT_WIRING_PATH, PARENT_WIRING_GIT_BLOB),
        (PARENT_WIRING_TEST_PATH, PARENT_WIRING_TEST_GIT_BLOB),
    ):
        target = root / path
        _require(target.is_file(), "reviewed source missing: " + path)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + path,
        )

    return {
        "child_entrypoint": deepcopy(child),
        "parent_wiring": deepcopy(parent),
    }


def pair06_v9_input_order_coherence_parent_wiring_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "child_entry_path": CHILD_ENTRY_PATH,
        "child_entry_git_blob": CHILD_ENTRY_GIT_BLOB,
        "child_entry_test_path": CHILD_ENTRY_TEST_PATH,
        "child_entry_test_git_blob": CHILD_ENTRY_TEST_GIT_BLOB,
        "parent_wiring_path": PARENT_WIRING_PATH,
        "parent_wiring_git_blob": PARENT_WIRING_GIT_BLOB,
        "parent_wiring_test_path": PARENT_WIRING_TEST_PATH,
        "parent_wiring_test_git_blob": PARENT_WIRING_TEST_GIT_BLOB,
        "pair06_v9_input_order_coherence_parent_wiring_reviewed": True,
        "input_order_child_entrypoint_reviewed": True,
        "existing_no_offload_parent_source_modified": False,
        "historical_parent_run_code_reused_reviewed": True,
        "call_scoped_child_command_binding_reviewed": True,
        "process_global_child_command_builder_mutated": False,
        "process_global_parent_run_function_mutated": False,
        "new_concurrency_scope_leak_introduced": False,
        "execution_confirmation_token_preserved": True,
        "historical_v9_policy_activation_token_preserved": True,
        "distinct_order_coherence_activation_token_preserved": True,
        "durable_attempt_claim_prerequisite_preserved": True,
        "no_offload_cuda0_parent_path_preserved": True,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "consumed_v9_attempt_retry_authorized": False,
        "operator_entrypoint_wiring_implemented": False,
        "execution_request_created": False,
        "attempt_claim_created": False,
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
        "validated": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_operator_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceParentWiringReviewHold(NEXT_GATE)
