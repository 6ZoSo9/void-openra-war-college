"""Exact-blob review of the pair-06 V9 child entrypoint and parent wiring.

This review pins the V9 child CLI entrypoint, the scoped no-offload parent
wiring, and both focused regression suites to exact repository bytes.

The reviewed historical no-offload parent remains unchanged. Existing execution
confirmation, the distinct V9 policy-activation confirmation, the durable
attempt-claim prerequisite, CUDA:0/no-offload loading, authority checks,
decision service, retirement, and receipt construction remain intact.

No operator invocation is wired. No execution request, durable attempt claim, or
attempt is created, and no runtime activation or execution authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_parent_supervisor_wiring_generation2
    as parent_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_game_child_entrypoint_generation2
    as child_entry,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-parent-supervisor-wiring-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "d0b2b21caff35cb34b5c8c857a70665e8cd95ad4"

CHILD_ENTRY_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_proto_game_child_entrypoint_generation2.py"
)
CHILD_ENTRY_GIT_BLOB = "69c82b62aafb395ba6494cc33c864a51da59e8c1"
CHILD_ENTRY_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_proto_game_child_entrypoint_generation2.py"
)
CHILD_ENTRY_TEST_GIT_BLOB = "b7c607dec5428dd74bf894c786577da2fefe2180"

PARENT_WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_parent_supervisor_wiring_generation2.py"
)
PARENT_WIRING_GIT_BLOB = "000ef4001694490f00aa01aac94371ccdd447307"
PARENT_WIRING_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_parent_supervisor_wiring_generation2.py"
)
PARENT_WIRING_TEST_GIT_BLOB = "c05a3095ce3e8953a52a49a05745b0cf22272de8"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_OPERATOR_ENTRYPOINT_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_operator_entrypoint_wiring"
)


class Pair06V9StrictVisibleContactParentWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactParentWiringReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    child = child_entry.pair06_v9_strict_visible_contact_child_entrypoint_contract()
    parent = parent_wiring.pair06_v9_strict_visible_contact_parent_wiring_contract()

    _require(
        child.get(
            "pair06_v9_strict_visible_contact_child_entrypoint_implemented"
        )
        is True,
        "V9 child entrypoint missing",
    )
    _require(
        child.get("pair_slot") == 6
        and child.get("arm") == "baseline"
        and child.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 child entrypoint scope drift",
    )
    _require(
        child.get("existing_execution_confirmation_token_required") is True
        and child.get("separate_v9_policy_activation_token_required") is True
        and child.get("execution_and_policy_confirmation_tokens_distinct")
        is True,
        "V9 child confirmation-token boundary drift",
    )
    _require(
        child.get("coherent_v9_tool_contract_path_preserved") is True,
        "V9 child coherence path drift",
    )
    for field in (
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
            "V9 child entrypoint boundary drift: " + field,
        )
    _require(
        child.get("next_gate")
        == "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED",
        "V9 child entrypoint frontier drift",
    )

    _require(
        parent.get("pair_slot") == 6
        and parent.get("arm") == "baseline"
        and parent.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 parent wiring scope drift",
    )
    for field in (
        "v9_child_entrypoint_implemented",
        "child_command_builder_substitution_implemented",
        "child_command_builder_substitution_scoped_to_single_call",
        "child_command_builder_restored_in_finally",
        "existing_execution_confirmation_token_preserved",
        "separate_v9_policy_activation_token_added",
        "existing_no_offload_model_loader_reused",
        "existing_cuda0_placement_checks_reused",
        "existing_parent_decision_service_loop_reused",
        "existing_child_retirement_reused",
        "existing_parent_receipt_returned_unchanged",
        "durable_attempt_claim_required_by_existing_parent",
    ):
        _require(
            parent.get(field) is True,
            "V9 parent wiring invariant drift: " + field,
        )
    _require(
        parent.get("existing_no_offload_parent_source_modified") is False
        and parent.get("existing_parent_automatic_retry") is False,
        "V9 parent historical/no-retry boundary drift",
    )
    for field in (
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
            "V9 parent wiring boundary drift: " + field,
        )
    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 parent wiring review frontier drift",
    )

    return {
        "child_entrypoint": deepcopy(child),
        "parent_wiring": deepcopy(parent),
    }


def pair06_v9_strict_visible_contact_parent_wiring_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "child_entry_path": CHILD_ENTRY_PATH,
        "child_entry_git_blob": CHILD_ENTRY_GIT_BLOB,
        "child_entry_test_path": CHILD_ENTRY_TEST_PATH,
        "child_entry_test_git_blob": CHILD_ENTRY_TEST_GIT_BLOB,
        "parent_wiring_path": PARENT_WIRING_PATH,
        "parent_wiring_git_blob": PARENT_WIRING_GIT_BLOB,
        "parent_wiring_test_path": PARENT_WIRING_TEST_PATH,
        "parent_wiring_test_git_blob": PARENT_WIRING_TEST_GIT_BLOB,
        "pair06_v9_strict_visible_contact_parent_wiring_reviewed": True,
        "v9_child_entrypoint_reviewed": True,
        "existing_no_offload_parent_source_modified": False,
        "execution_confirmation_token_preserved": True,
        "distinct_v9_policy_activation_token_preserved": True,
        "durable_attempt_claim_prerequisite_preserved": True,
        "no_offload_cuda0_parent_path_preserved": True,
        "scoped_child_command_substitution_reviewed": True,
        "child_command_restored_in_finally_reviewed": True,
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
    raise Pair06V9StrictVisibleContactParentWiringReviewHold(NEXT_GATE)
