"""Exact-blob review of the Pair-06 actionable-feedback V4 unit_ids repair.

This review pins the pure V4 canonicalization source and focused tests.  It
confirms that only unambiguous positive integer actor ids already present in
current own_units may be rewritten to the frozen V8 string wire format.  The
frozen V8 parser/translator and downstream host validator remain unchanged.

No runtime activation, attempt, inference, game execution, replay, training,
deployment, chain, funds, or scheduler authority is granted here.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_unit_ids_canonicalization_generation2
    as repair,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v4-"
    "unit-ids-canonicalization-review.v1"
)

ACCEPTED_BASE_HEAD = "e983220f85e35c024bcc0da8dec418bcd8342e03"

REPAIR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v4_unit_ids_canonicalization_generation2.py"
)
REPAIR_GIT_BLOB = "05a0e5be44d5f871c194f4a70826436e4bb2aed2"

REPAIR_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v4_unit_ids_canonicalization_generation2.py"
)
REPAIR_TEST_GIT_BLOB = "0f4584dc6e9cc2b4385961aff9fc58b22741a6b9"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V4_RUNTIME_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v4_unit_ids_"
    "canonicalization_runtime_integration"
)


class Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = repair.pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_contract()

    _require(
        out.get("v4_unit_ids_canonicalization_implemented") is True
        and out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V4 canonicalization identity drift",
    )
    _require(
        out.get("consumed_v3_main_head") == ACCEPTED_BASE_HEAD
        and out.get("observed_v3_failed_round") == 6
        and out.get("observed_v3_max_attempts") == 6
        and out.get("observed_v3_terminal_feedback")
        == repair.OBSERVED_V3_TERMINAL_FEEDBACK,
        "V4 consumed V3 failure identity drift",
    )

    for field in (
        "canonicalizable_bare_positive_integer",
        "canonicalizable_nonempty_distinct_positive_integer_list",
        "all_candidate_ids_must_be_currently_owned",
        "existing_string_passes_through_unchanged",
        "non_move_units_passes_through_unchanged",
        "foreign_ids_fail_closed",
        "empty_list_fails_closed",
        "duplicate_ids_fail_closed",
        "boolean_ids_fail_closed",
        "float_ids_fail_closed",
        "nested_ids_fail_closed",
        "canonical_output_revalidated_by_frozen_v8_translator",
    ):
        _require(out.get(field) is True, "V4 repair invariant drift: " + field)

    for field in (
        "frozen_v8_runtime_source_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "host_validator_bypassed",
        "world_mutation_performed",
        "consumed_v3_attempt_retry_authorized",
        "new_execution_request_opened",
        "attempt_claim_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(out.get(field) is False, "V4 authority/boundary drift: " + field)

    _require(
        out.get("v3_correction_review_git_blob")
        == repair.V3_CORRECTION_REVIEW_GIT_BLOB
        and out.get("v3_runtime_review_git_blob")
        == repair.V3_RUNTIME_REVIEW_GIT_BLOB
        and out.get("v3_launcher_review_git_blob")
        == repair.V3_LAUNCHER_REVIEW_GIT_BLOB
        and out.get("v8_runtime_git_blob") == repair.V8_RUNTIME_GIT_BLOB,
        "V4 dependency blob drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (REPAIR_PATH, REPAIR_GIT_BLOB),
        (REPAIR_TEST_PATH, REPAIR_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "repair_path": REPAIR_PATH,
        "repair_git_blob": REPAIR_GIT_BLOB,
        "repair_test_path": REPAIR_TEST_PATH,
        "repair_test_git_blob": REPAIR_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v4_unit_ids_canonicalization_reviewed": True,
        "consumed_v3_main_head": validated["consumed_v3_main_head"],
        "observed_v3_terminal_feedback": validated["observed_v3_terminal_feedback"],
        "observed_v3_failed_round": validated["observed_v3_failed_round"],
        "observed_v3_max_attempts": validated["observed_v3_max_attempts"],
        "canonicalizable_bare_positive_integer": True,
        "canonicalizable_nonempty_distinct_positive_integer_list": True,
        "all_candidate_ids_must_be_currently_owned": True,
        "foreign_ids_fail_closed": True,
        "duplicate_ids_fail_closed": True,
        "canonical_output_revalidated_by_frozen_v8_translator": True,
        "host_validator_modified": False,
        "host_validator_bypassed": False,
        "consumed_v3_attempt_retry_authorized": False,
        "new_execution_request_opened": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "replay_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_repair": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV4UnitIdsCanonicalizationReviewHold(NEXT_GATE)
