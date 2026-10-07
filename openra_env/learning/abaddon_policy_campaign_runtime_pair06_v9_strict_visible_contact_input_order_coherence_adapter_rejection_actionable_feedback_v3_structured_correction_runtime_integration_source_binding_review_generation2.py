"""Exact-blob review of Pair-06 V9 actionable-feedback V3 runtime integration."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from types import FunctionType
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "structured-correction-runtime-integration-review.v1"
)

ACCEPTED_BASE_HEAD = "b98d2a5bf3df81479d6d2965cd9b99d4144df853"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_structured_correction_runtime_"
    "integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "71a065ff3a38d5c298bbf16559b942af22d564ff"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_structured_correction_runtime_"
    "integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "2471ffc45178ad21f716f18c78eac3999bb98fae"

V2_PARENT_INTEGRATION_GIT_BLOB = "22eb8708b600d15e6f3aa0e02e5697a7cf01a820"
V2_PARENT_REVIEW_GIT_BLOB = "c3a39dbb0a22d9350894a8f78b824af0b4e07a01"
V3_CORRECTION_GIT_BLOB = "9456c729db82284fa9a41e5bc728c254e0768caa"
V3_CORRECTION_REVIEW_GIT_BLOB = "437a0a35223b8b418fb3482407c8dc00d160f8e9"
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_OPERATOR_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v3_operator_integration"
)


class Pair06V9ActionableFeedbackV3RuntimeIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3RuntimeIntegrationReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = integration.pair06_v9_actionable_feedback_v3_runtime_integration_contract()

    _require(
        out.get("actionable_feedback_v3_runtime_integration_implemented") is True,
        "V3 runtime integration missing",
    )
    _require(
        out.get("v2_parent_integration_git_blob")
        == V2_PARENT_INTEGRATION_GIT_BLOB
        and out.get("v2_parent_review_git_blob") == V2_PARENT_REVIEW_GIT_BLOB
        and out.get("v3_correction_git_blob") == V3_CORRECTION_GIT_BLOB
        and out.get("v3_correction_review_git_blob")
        == V3_CORRECTION_REVIEW_GIT_BLOB
        and out.get("v8_runtime_git_blob") == V8_RUNTIME_GIT_BLOB,
        "V3 runtime integration dependency identity drift",
    )

    for field in (
        "reviewed_v2_parent_integration_reused",
        "historical_parent_run_code_reused",
        "call_scoped_child_command_binding_preserved",
        "call_scoped_decision_response_binding_upgraded_to_v3",
        "exact_v2_feedback_trigger_only",
        "nonmatching_feedback_delegates_to_v2_unchanged",
        "structured_feedback_injected_into_user_prompt",
        "corrective_retry_transfer_prompt_preserved",
        "v2_adapter_rejection_fail_closed_shim_reused",
    ):
        _require(
            out.get(field) is True,
            "V3 runtime integration invariant drift: " + field,
        )

    _require(
        out.get("corrective_retry_legacy_prompt_fallback_used") is False,
        "V3 runtime integration unexpectedly uses legacy corrective prompt",
    )

    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "process_global_parent_run_function_mutated",
        "process_global_child_command_builder_mutated",
        "process_global_decision_response_mutated",
        "process_global_runtime_method_mutated",
        "builder_executes_parent",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
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
        _require(out.get(field) is False, "V3 runtime boundary drift: " + field)

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate")
        == (
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_"
            "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V3 runtime implementation frontier drift",
    )

    scoped = integration.build_pair06_v9_actionable_feedback_v3_parent_run()
    _require(isinstance(scoped, FunctionType), "V3 parent builder did not return FunctionType")
    _require(
        scoped.__globals__.get("_decision_response")
        is integration.decision_response_with_v3_structured_correction,
        "V3 scoped decision-response binding drift",
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


def pair06_v9_actionable_feedback_v3_runtime_integration_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v3_runtime_integration_reviewed": True,
        "policy_id": out["policy_id"],
        "intervention_id": out["intervention_id"],
        "reviewed_v2_parent_integration_reused": True,
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_preserved": True,
        "call_scoped_decision_response_binding_upgraded_to_v3": True,
        "exact_v2_feedback_trigger_only": True,
        "nonmatching_feedback_delegates_to_v2_unchanged": True,
        "structured_feedback_injected_into_user_prompt": True,
        "corrective_retry_transfer_prompt_preserved": True,
        "corrective_retry_legacy_prompt_fallback_used": False,
        "v2_adapter_rejection_fail_closed_shim_reused": True,
        "frozen_v8_tool_schema_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "six_attempt_bound_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "process_global_parent_run_function_mutated": False,
        "process_global_decision_response_mutated": False,
        "process_global_runtime_method_mutated": False,
        "consumed_v2_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
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


def integrate_operator_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV3RuntimeIntegrationReviewHold(NEXT_GATE)
