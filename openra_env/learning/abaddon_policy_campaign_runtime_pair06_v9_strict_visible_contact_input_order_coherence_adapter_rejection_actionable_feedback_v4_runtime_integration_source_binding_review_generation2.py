"""Exact-blob review of Pair-06 actionable-feedback V4 runtime integration.

Pins the V4 corrective runtime wrapper and focused tests.  It confirms that the
reviewed V3 structured corrective turn remains in use, exact
V8CampaignRuntimeError("unit_ids invalid") is the only repair trigger, repaired
ids must satisfy the reviewed owned-id canonicalizer, and the unchanged frozen
V8 translator revalidates canonical output before downstream host validation.

No execution, retry, training, promotion, deployment, chain, funds, or
scheduler authority is granted here.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_runtime_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v4-"
    "runtime-integration-review.v1"
)
ACCEPTED_BASE_HEAD = "666c85409184cf9d23c03a56c3210f3a43099570"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v4_runtime_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "1042819cfa7fd3e76f262c5d65132e887377df9e"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v4_runtime_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "b4b5f11318f0674033005a6521e55dde514d0af5"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V4_OPERATOR_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v4_operator_integration"
)


class Pair06V9ActionableFeedbackV4RuntimeIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV4RuntimeIntegrationReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = integration.pair06_v9_actionable_feedback_v4_runtime_integration_contract()

    _require(
        out.get("actionable_feedback_v4_runtime_integration_implemented") is True
        and out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V4 runtime integration identity drift",
    )

    for field in (
        "reviewed_v3_parent_integration_reused",
        "historical_parent_run_code_reused",
        "call_scoped_child_command_binding_preserved",
        "call_scoped_decision_response_binding_upgraded_to_v4",
        "exact_terminal_feedback_trigger_only",
        "nonmatching_feedback_delegates_to_v3_unchanged",
        "reviewed_v3_structured_turn_reused",
        "corrective_retry_transfer_prompt_preserved",
        "original_output_first_checked_by_frozen_v8_translator",
        "v4_repair_only_after_exact_unit_ids_invalid",
        "current_owned_ids_required_for_repair",
        "canonical_output_revalidated_by_frozen_v8_translator",
        "other_v8_translation_errors_propagate",
        "unsafe_or_ambiguous_unit_ids_fail_closed",
        "v2_adapter_rejection_fail_closed_shim_reused",
    ):
        _require(out.get(field) is True, "V4 runtime invariant drift: " + field)

    for field in (
        "frozen_v8_runtime_source_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "host_validator_bypassed",
        "six_attempt_bound_modified",
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
        "consumed_v3_attempt_retry_authorized",
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
        _require(out.get(field) is False, "V4 runtime boundary drift: " + field)

    _require(
        out.get("v3_runtime_integration_git_blob")
        == integration.V3_RUNTIME_INTEGRATION_GIT_BLOB
        and out.get("v3_runtime_review_git_blob")
        == integration.V3_RUNTIME_REVIEW_GIT_BLOB
        and out.get("v4_repair_git_blob") == integration.V4_REPAIR_GIT_BLOB
        and out.get("v4_repair_review_git_blob")
        == integration.V4_REPAIR_REVIEW_GIT_BLOB,
        "V4 runtime dependency blob drift",
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


def pair06_v9_actionable_feedback_v4_runtime_integration_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v4_runtime_integration_reviewed": True,
        "pair_slot": validated["pair_slot"],
        "arm": validated["arm"],
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "v3_runtime_integration_git_blob": validated[
            "v3_runtime_integration_git_blob"
        ],
        "v3_runtime_review_git_blob": validated["v3_runtime_review_git_blob"],
        "v4_repair_git_blob": validated["v4_repair_git_blob"],
        "v4_repair_review_git_blob": validated["v4_repair_review_git_blob"],
        "exact_terminal_feedback_trigger_only": True,
        "v4_repair_only_after_exact_unit_ids_invalid": True,
        "current_owned_ids_required_for_repair": True,
        "canonical_output_revalidated_by_frozen_v8_translator": True,
        "other_v8_translation_errors_propagate": True,
        "unsafe_or_ambiguous_unit_ids_fail_closed": True,
        "host_validator_modified": False,
        "host_validator_bypassed": False,
        "consumed_v3_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_integration": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_operator_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV4RuntimeIntegrationReviewHold(NEXT_GATE)
