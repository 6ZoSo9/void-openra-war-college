"""Exact-blob review of the Pair-06 V9 actionable-feedback V2 parent integration.

Pins the source-only parent integration and its focused tests. The review
confirms that the already-reviewed V1 parent integration is reused unchanged,
its historical parent code and child-command binding are preserved, and only
the call-scoped decision-response binding is upgraded to the reviewed actionable
feedback V2 shim.

No process-global function is mutated. Building or inspecting the integration
performs no host I/O, model load, inference, child spawn, game execution,
attempt claim, retry, replay, training, deployment, chain, wallet/funds, or
scheduler action. The consumed input-order attempt remains non-retryable.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_parent_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-actionable-feedback-v2-parent-integration-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "81ce5f72a32358266a3432987274e8fe7f977806"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_parent_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "22eb8708b600d15e6f3aa0e02e5697a7cf01a820"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_parent_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "a1e9f70ed3de79730af72b46a54038542db2e0ca"

V1_PARENT_INTEGRATION_GIT_BLOB = "381f30278f58ebfd66348807f56251bd16a9ce92"
V1_PARENT_REVIEW_GIT_BLOB = "81c65183dea163a9cec9bade063d3045045522e0"
V2_FEEDBACK_GIT_BLOB = "02ada3893596a2596ad8f980d7e1a0b5fe8faf92"
V2_FEEDBACK_REVIEW_GIT_BLOB = "e1931048b9e8e589b0749d68e11376569da33612"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_OPERATOR_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_operator_integration"
)


class Pair06V9ActionableFeedbackV2ParentIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2ParentIntegrationReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = integration.pair06_v9_actionable_feedback_v2_parent_integration_contract()

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "actionable feedback V2 parent integration scope drift",
    )

    for field in (
        "actionable_feedback_v2_parent_integration_implemented",
        "reviewed_v1_parent_integration_reused",
        "historical_parent_run_code_reused",
        "call_scoped_child_command_binding_reused",
        "call_scoped_decision_response_binding_upgraded_to_v2",
        "reviewed_actionable_feedback_v2_used",
        "feedback_requires_quoted_unit_ids_string",
        "feedback_rejects_json_array_unit_ids",
        "feedback_rejects_bare_integer_unit_ids",
    ):
        _require(
            out.get(field) is True,
            "actionable feedback V2 parent integration invariant drift: " + field,
        )

    for field in (
        "v1_parent_integration_source_modified",
        "v1_feedback_source_modified",
        "v2_feedback_source_modified",
        "process_global_parent_run_function_mutated",
        "process_global_child_command_builder_mutated",
        "process_global_decision_response_mutated",
        "builder_executes_parent",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "consumed_input_order_attempt_retry_authorized",
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
        _require(
            out.get(field) is False,
            "actionable feedback V2 parent integration boundary drift: " + field,
        )

    _require(
        out.get("v1_parent_integration_git_blob")
        == V1_PARENT_INTEGRATION_GIT_BLOB
        and out.get("v1_parent_review_git_blob") == V1_PARENT_REVIEW_GIT_BLOB,
        "reviewed V1 parent lineage drift",
    )
    _require(
        out.get("v2_feedback_git_blob") == V2_FEEDBACK_GIT_BLOB
        and out.get("v2_feedback_review_git_blob") == V2_FEEDBACK_REVIEW_GIT_BLOB,
        "reviewed actionable feedback V2 lineage drift",
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


def pair06_v9_actionable_feedback_v2_parent_integration_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "v1_parent_integration_git_blob": V1_PARENT_INTEGRATION_GIT_BLOB,
        "v1_parent_review_git_blob": V1_PARENT_REVIEW_GIT_BLOB,
        "v2_feedback_git_blob": V2_FEEDBACK_GIT_BLOB,
        "v2_feedback_review_git_blob": V2_FEEDBACK_REVIEW_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_parent_integration_reviewed": True,
        "policy_id": validated["policy_id"],
        "reviewed_v1_parent_integration_reused": True,
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_reused": True,
        "call_scoped_decision_response_binding_upgraded_to_v2": True,
        "reviewed_actionable_feedback_v2_used": True,
        "process_global_parent_run_function_mutated": False,
        "process_global_child_command_builder_mutated": False,
        "process_global_decision_response_mutated": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "consumed_input_order_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "attempt_created": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
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


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2ParentIntegrationReviewHold(NEXT_GATE)
