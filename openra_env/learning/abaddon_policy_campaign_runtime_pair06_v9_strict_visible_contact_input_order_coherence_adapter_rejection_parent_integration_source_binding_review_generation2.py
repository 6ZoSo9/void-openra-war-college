"""Exact-blob review of the Pair-06 V9 adapter-rejection parent integration.

Pins the source-only integration and focused tests. The review confirms that the
historical parent code object is reused with a copied globals namespace where
only the reviewed input-order child-command factory and reviewed exact-error
adapter-rejection response shim are substituted.

No process-global parent function is mutated. Building or inspecting the
integration performs no host I/O, model load, inference, child spawn, game
execution, attempt claim, replay, training, deployment, chain, wallet/funds, or
scheduler action. The consumed input-order attempt remains non-retryable.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-parent-integration-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "2ebbdd39e8d0993dc82da09f0e3775939d5993a6"

INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "adapter_rejection_parent_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "8413a2c773f7e5df22f4874157d5e1d6f151a18c"

INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "adapter_rejection_parent_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "df6c92a88e634565520acb6921ca1b7773a1f5ee"

ADAPTER_RESPONSE_GIT_BLOB = "5d6ec9e9f1cb575972f0ccd41e2e9c5ac99da101"
ADAPTER_RESPONSE_REVIEW_GIT_BLOB = "a8eaa4725074a16a607425319fda5af5130f0737"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_OPERATOR_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_operator_integration"
)


class Pair06V9InputOrderAdapterRejectionParentIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderAdapterRejectionParentIntegrationReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_parent_integration_contract()
    )

    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "adapter-rejection parent integration scope drift",
    )

    for field in (
        "adapter_rejection_parent_integration_implemented",
        "historical_parent_run_code_reused",
        "call_scoped_child_command_binding_reused",
        "call_scoped_decision_response_binding_implemented",
        "input_order_child_command_used",
        "reviewed_adapter_rejection_response_used",
    ):
        _require(
            out.get(field) is True,
            "adapter-rejection parent integration invariant drift: " + field,
        )

    for field in (
        "historical_parent_source_modified",
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
            "adapter-rejection parent integration boundary drift: " + field,
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


def pair06_v9_input_order_adapter_rejection_parent_integration_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "adapter_response_git_blob": ADAPTER_RESPONSE_GIT_BLOB,
        "adapter_response_review_git_blob": ADAPTER_RESPONSE_REVIEW_GIT_BLOB,
        "pair06_v9_input_order_adapter_rejection_parent_integration_reviewed": True,
        "policy_id": validated["policy_id"],
        "historical_parent_run_code_reused": True,
        "call_scoped_child_command_binding_reused": True,
        "call_scoped_decision_response_binding_implemented": True,
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
    raise Pair06V9InputOrderAdapterRejectionParentIntegrationReviewHold(
        NEXT_GATE
    )
