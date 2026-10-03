"""Exact-blob review of actionable adapter-rejection feedback V2.

Pins the source-only V2 shim and focused tests. The review confirms that V1
remains immutable, only the V1 unavailable sentinel is rewritten, and the V2
sentinel communicates the exact unit_ids wire-format correction needed by the
next bounded decision attempt.

No parser/translator relaxation, coercion, retry-count change, host-validation
change, execution request, or runtime authority is introduced.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_generation2
    as v2,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "review-contract.v1"
)

ACCEPTED_BASE_HEAD = "d8c84b2061039de47d0fe34bc8a91dc067522b56"

V2_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_generation2.py"
)
V2_GIT_BLOB = "02ada3893596a2596ad8f980d7e1a0b5fe8faf92"

V2_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_generation2.py"
)
V2_TEST_GIT_BLOB = "e3d540e8ba2efdb0b258daf20cc62b95383a8ddd"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_PARENT_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_parent_integration"
)


class Pair06V9AdapterRejectionActionableFeedbackV2ReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionActionableFeedbackV2ReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = v2.pair06_v9_adapter_rejection_actionable_feedback_v2_contract()

    _require(
        out.get("pair_slot") == 6 and out.get("arm") == "baseline",
        "actionable feedback V2 scope drift",
    )
    _require(
        out.get("actionable_feedback_v2_implemented") is True
        and out.get("v1_source_modified") is False
        and out.get("v1_success_responses_pass_through_unchanged") is True
        and out.get("only_v1_sentinel_is_rewritten") is True,
        "actionable feedback V2 composition drift",
    )
    _require(
        out.get("v1_sentinel_tool")
        == "__v8_adapter_rejected_unit_ids_invalid__"
        and out.get("v2_sentinel_tool")
        == (
            "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
            "not_json_array_or_bare_integer__"
        ),
        "actionable feedback V2 sentinel drift",
    )
    _require(
        out.get("expected_child_feedback")
        == (
            "function_not_offered:"
            "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
            "not_json_array_or_bare_integer__"
        ),
        "actionable feedback V2 child feedback drift",
    )
    _require(
        out.get("quoted_string_example_single") == '"123"'
        and out.get("quoted_string_example_multiple") == '"123,456"'
        and out.get("invalid_json_array_example") == "[123,456]"
        and out.get("invalid_bare_integer_example") == "123",
        "actionable feedback V2 examples drift",
    )

    for field in (
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "six_attempt_decision_bound_modified",
        "host_validation_modified",
        "world_mutation_before_child_validation",
        "consumed_attempt_retry_authorized",
        "new_execution_request_opened",
        "attempt_claim_created",
        "attempt_created",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "actionable feedback V2 boundary drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (V2_PATH, V2_GIT_BLOB),
        (V2_TEST_PATH, V2_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_adapter_rejection_actionable_feedback_v2_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "v2_path": V2_PATH,
        "v2_git_blob": V2_GIT_BLOB,
        "v2_test_path": V2_TEST_PATH,
        "v2_test_git_blob": V2_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_actionable_feedback_v2_reviewed": True,
        "v1_sentinel_tool": validated["v1_sentinel_tool"],
        "v2_sentinel_tool": validated["v2_sentinel_tool"],
        "expected_child_feedback": validated["expected_child_feedback"],
        "feedback_requires_quoted_unit_ids_string": True,
        "feedback_rejects_json_array_unit_ids": True,
        "feedback_rejects_bare_integer_unit_ids": True,
        "v1_source_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "six_attempt_decision_bound_modified": False,
        "host_validation_modified": False,
        "consumed_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_v2": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionActionableFeedbackV2ReviewHold(NEXT_GATE)
