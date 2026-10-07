"""Exact-blob review of Pair-06 V9 actionable-feedback V3 operator integration."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from types import FunctionType
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_operator_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "operator-integration-review.v1"
)

ACCEPTED_BASE_HEAD = "003bd408bd45611842ac41ab58fd24ca63282391"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_operator_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "9d0f3c41b5a56b877391072bd98921b6d156bb7a"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_operator_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "2b6c7078add67ded3e60e790273ae206f1b13150"

V2_OPERATOR_INTEGRATION_GIT_BLOB = (
    "8a8b1114682940462934dfbfcf25e0dbd3a784a3"
)
V2_OPERATOR_REVIEW_GIT_BLOB = (
    "03d8f1fcfb50a97f2d4970da2b75ae051cef98d6"
)
V3_PARENT_INTEGRATION_GIT_BLOB = (
    "71a065ff3a38d5c298bbf16559b942af22d564ff"
)
V3_PARENT_REVIEW_GIT_BLOB = (
    "b82c6465656e0b06509034b90af8b79c659ae92b"
)

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_FRESH_LINEAGE_OPERATOR_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v3_fresh_lineage_operator"
)


class Pair06V9ActionableFeedbackV3OperatorIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3OperatorIntegrationReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = integration.pair06_v9_actionable_feedback_v3_operator_integration_contract()

    _require(
        out.get("actionable_feedback_v3_operator_integration_implemented") is True,
        "V3 operator integration missing",
    )
    _require(
        out.get("v2_operator_integration_git_blob")
        == V2_OPERATOR_INTEGRATION_GIT_BLOB
        and out.get("v2_operator_review_git_blob") == V2_OPERATOR_REVIEW_GIT_BLOB
        and out.get("v3_parent_integration_git_blob")
        == V3_PARENT_INTEGRATION_GIT_BLOB
        and out.get("v3_parent_review_git_blob") == V3_PARENT_REVIEW_GIT_BLOB,
        "V3 operator dependency identity drift",
    )

    for field in (
        "reviewed_v2_operator_integration_reused",
        "historical_operator_code_object_reused",
        "call_scoped_dependency_binding_upgraded_to_v3",
        "call_scoped_parent_binding_upgraded_to_v3",
        "reviewed_actionable_feedback_v3_parent_used",
        "historical_preclaim_gpu_ordering_preserved",
        "historical_one_attempt_cardinality_preserved",
        "historical_automatic_retry_remains_false",
        "historical_execution_policy_order_authorizations_preserved",
        "structured_feedback_injected_into_user_prompt",
        "corrective_retry_transfer_prompt_preserved",
        "v2_adapter_rejection_fail_closed_shim_reused",
        "fresh_attempt_namespace_required_before_execution_request",
        "fresh_actionable_feedback_v3_activation_authorization_required",
        "fresh_operator_source_required_before_execution_request",
    ):
        _require(
            out.get(field) is True,
            "V3 operator integration invariant drift: " + field,
        )

    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "v2_operator_integration_source_modified",
        "v3_parent_integration_source_modified",
        "process_global_operator_execute_mutated",
        "process_global_operator_dependencies_mutated",
        "process_global_operator_parent_binding_mutated",
        "builder_executes_operator",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "consumed_v2_namespace_reusable",
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
        "actionable_feedback_v3_activation_authorization_accepted",
        "attempt_claim_created",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(out.get(field) is False, "V3 operator boundary drift: " + field)

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate")
        == (
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_OPERATOR_INTEGRATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V3 operator implementation frontier drift",
    )

    scoped = integration.build_pair06_v9_actionable_feedback_v3_operator()
    _require(isinstance(scoped, FunctionType), "V3 operator builder did not return FunctionType")
    _require(
        scoped.__globals__.get("_dependency_contracts")
        is integration._scoped_dependency_contracts,
        "V3 scoped dependency binding drift",
    )
    parent = scoped.__globals__.get("order_parent")
    _require(
        getattr(
            parent,
            "execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload",
            None,
        )
        is integration._execute_v3_parent,
        "V3 scoped parent binding drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (INTEGRATION_PATH, INTEGRATION_GIT_BLOB),
        (INTEGRATION_TEST_PATH, INTEGRATION_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v3_operator_integration_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v3_operator_integration_reviewed": True,
        "policy_id": out["policy_id"],
        "intervention_id": out["intervention_id"],
        "reviewed_v2_operator_integration_reused": True,
        "historical_operator_code_object_reused": True,
        "call_scoped_dependency_binding_upgraded_to_v3": True,
        "call_scoped_parent_binding_upgraded_to_v3": True,
        "reviewed_actionable_feedback_v3_parent_used": True,
        "historical_preclaim_gpu_ordering_preserved": True,
        "historical_one_attempt_cardinality_preserved": True,
        "historical_automatic_retry_remains_false": True,
        "structured_feedback_injected_into_user_prompt": True,
        "corrective_retry_transfer_prompt_preserved": True,
        "v2_adapter_rejection_fail_closed_shim_reused": True,
        "fresh_attempt_namespace_required_before_execution_request": True,
        "fresh_actionable_feedback_v3_activation_authorization_required": True,
        "fresh_operator_source_required_before_execution_request": True,
        "consumed_v2_namespace_reusable": False,
        "consumed_v2_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "actionable_feedback_v3_activation_authorization_accepted": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_integration": out,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def build_fresh_operator_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV3OperatorIntegrationReviewHold(NEXT_GATE)
