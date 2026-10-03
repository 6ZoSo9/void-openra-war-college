"""Exact-source review for the Pair-06 V9 adapter-feedback proto-child lineage.

Pins the new adapter-feedback proto-child wiring and its focused regression
suite, plus the merged feedback overlay and unchanged historical reviewed
input-order child boundary.

No parent wiring, operator wiring, execution request, attempt, model/game run,
retry, training, promotion, deployment, chain, wallet/funds, or scheduler
authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_feedback_proto_child_wiring_generation2
    as wiring,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-adapter-rejection-feedback-"
    "proto-child-wiring-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "bb48c4817c0d18cec311f92c7f2d098f9f9a9f4d"

WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "proto_child_wiring_generation2.py"
)
WIRING_GIT_BLOB = "64af11733bb384959cc7cc5f11d18dab2d9e2c1c"

WIRING_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "proto_child_wiring_generation2.py"
)
WIRING_TEST_GIT_BLOB = "27e7f692117a8d4dde9e0a8cc2271218a26fa22a"

FEEDBACK_OVERLAY_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "overlay_generation2.py"
)
FEEDBACK_OVERLAY_GIT_BLOB = "f720d70d2f7068eeeb05324d3a89aaf6b86daa84"

HISTORICAL_WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_proto_child_wiring_generation2.py"
)
HISTORICAL_WIRING_GIT_BLOB = "1b87cb5596c219e6118f4b69845dbecaa29a3ace"

HISTORICAL_WIRING_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_proto_child_wiring_"
    "source_binding_review_generation2.py"
)
HISTORICAL_WIRING_REVIEW_GIT_BLOB = (
    "7e96e32361b64f71ccf5c2cfd3c10a33c15429a1"
)

NEXT_GATE = (
    "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_adapter_rejection_feedback_"
    "parent_supervisor_wiring"
)


class Pair06V9AdapterFeedbackProtoChildWiringReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterFeedbackProtoChildWiringReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = wiring.pair06_v9_adapter_feedback_proto_child_wiring_contract()

    _require(
        out.get("adapter_feedback_proto_child_wiring_implemented") is True,
        "adapter-feedback proto-child wiring missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "adapter-feedback proto-child scope drift",
    )

    for field in (
        "historical_input_order_child_hook_subclass_reused",
        "feedback_decision_hook_bound",
        "exact_sentinel_retry_feedback_preserved",
        "historical_scoped_v8_child_builder_code_reused",
        "historical_input_order_child_run_code_reused",
        "call_scoped_feedback_hook_binding_implemented",
        "original_child_execution_authorization_gate_preserved",
        "historical_v9_policy_activation_gate_preserved",
        "input_order_coherence_activation_gate_preserved",
    ):
        _require(
            out.get(field) is True,
            "adapter-feedback proto-child invariant drift: " + field,
        )

    _require(
        out.get("sentinel_retry_feedback") == "unit_ids invalid",
        "adapter-feedback retry reason drift",
    )

    for field in (
        "historical_input_order_proto_child_source_modified",
        "historical_input_order_proto_child_review_modified",
        "feedback_overlay_source_modified",
        "process_global_child_hook_factory_mutated",
        "process_global_child_run_function_mutated",
        "new_concurrency_scope_leak_introduced",
        "consumed_v9_attempt_retry_authorized",
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
            "adapter-feedback proto-child authority/global drift: " + field,
        )

    _require(
        out.get("feedback_overlay_git_blob") == FEEDBACK_OVERLAY_GIT_BLOB
        and out.get("historical_wiring_git_blob")
        == HISTORICAL_WIRING_GIT_BLOB
        and out.get("historical_wiring_review_git_blob")
        == HISTORICAL_WIRING_REVIEW_GIT_BLOB,
        "adapter-feedback dependency identity drift",
    )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
            "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "adapter-feedback proto-child source frontier drift",
    )

    root = Path(__file__).parents[2]
    for path, blob in (
        (WIRING_PATH, WIRING_GIT_BLOB),
        (WIRING_TEST_PATH, WIRING_TEST_GIT_BLOB),
        (FEEDBACK_OVERLAY_PATH, FEEDBACK_OVERLAY_GIT_BLOB),
        (HISTORICAL_WIRING_PATH, HISTORICAL_WIRING_GIT_BLOB),
        (HISTORICAL_WIRING_REVIEW_PATH, HISTORICAL_WIRING_REVIEW_GIT_BLOB),
    ):
        target = root / path
        _require(target.is_file(), "reviewed source missing: " + path)
        _require(
            _git_blob_sha1(target.read_bytes()) == blob,
            "reviewed source blob drift: " + path,
        )

    return deepcopy(out)


def pair06_v9_adapter_feedback_proto_child_wiring_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "wiring_path": WIRING_PATH,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_test_path": WIRING_TEST_PATH,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "feedback_overlay_path": FEEDBACK_OVERLAY_PATH,
        "feedback_overlay_git_blob": FEEDBACK_OVERLAY_GIT_BLOB,
        "historical_wiring_path": HISTORICAL_WIRING_PATH,
        "historical_wiring_git_blob": HISTORICAL_WIRING_GIT_BLOB,
        "historical_wiring_review_path": HISTORICAL_WIRING_REVIEW_PATH,
        "historical_wiring_review_git_blob": HISTORICAL_WIRING_REVIEW_GIT_BLOB,
        "pair06_v9_adapter_feedback_proto_child_wiring_reviewed": True,
        "feedback_decision_hook_reviewed": True,
        "historical_input_order_child_run_code_reused_reviewed": True,
        "call_scoped_feedback_hook_binding_reviewed": True,
        "process_global_child_hook_factory_mutated": False,
        "process_global_child_run_function_mutated": False,
        "consumed_v9_attempt_retry_authorized": False,
        "parent_supervisor_wiring_implemented": False,
        "operator_wiring_implemented": False,
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
    raise Pair06V9AdapterFeedbackProtoChildWiringReviewHold(NEXT_GATE)
