"""Exact-blob review of Pair-06 V9 actionable-feedback V3 structured correction."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_generation2
    as correction,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "structured-correction-review.v1"
)

ACCEPTED_BASE_HEAD = "05833a17a869e8837423a8193ad641e286a33ab1"

SOURCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_structured_correction_generation2.py"
)
SOURCE_GIT_BLOB = "9456c729db82284fa9a41e5bc728c254e0768caa"

TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_structured_correction_generation2.py"
)
TEST_GIT_BLOB = "f9d77bb49201800d756eba035db3347b1b00e17d"

NEXT_GATE = (
    "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_actionable_feedback_v3_structured_correction_"
    "runtime_integration"
)


class Pair06V9ActionableFeedbackV3StructuredCorrectionReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3StructuredCorrectionReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = correction.pair06_v9_actionable_feedback_v3_structured_correction_contract()
    retry = out["example_retry_context"]
    payload = retry["structured_payload"]

    _require(
        out.get("structured_correction_v3_implemented") is True
        and out.get("exact_v2_trigger_only") is True,
        "V3 structured correction implementation missing",
    )
    _require(
        out.get("v2_feedback_review_git_blob")
        == "e1931048b9e8e589b0749d68e11376569da33612"
        and out.get("second_exhaustion_closeout_review_git_blob")
        == "4dadc961e02cd13893bd842bc6ee727c443b55a2"
        and out.get("v8_runtime_git_blob")
        == "fd0e72767ba199e88af9e9eb2455c03ace027a14",
        "V3 dependency source identity drift",
    )
    _require(
        out.get("exact_v2_trigger") == correction.V2_TRIGGER
        and retry.get("input_feedback") == correction.V2_TRIGGER,
        "V3 exact trigger identity drift",
    )
    _require(
        payload.get("tool") == "move_units"
        and payload.get("argument") == "unit_ids"
        and payload.get("required_json_type") == "string"
        and payload.get("ids_source") == "CURRENT STATE own_units id values",
        "V3 structured correction target drift",
    )
    _require(
        payload.get("valid_single_argument_json") == '{"unit_ids":"135"}'
        and payload.get("valid_multiple_argument_json")
        == '{"unit_ids":"135,137"}'
        and payload.get("invalid_json_array_argument_json")
        == '{"unit_ids":[135,137]}'
        and payload.get("invalid_bare_integer_argument_json")
        == '{"unit_ids":135}',
        "V3 structured correction example drift",
    )
    _require(
        retry.get("system_prompt_family") == "transfer"
        and retry.get("preserve_transfer_system_prompt") is True
        and retry.get("legacy_system_prompt_selected") is False
        and out.get("preserve_transfer_system_prompt_required") is True
        and out.get("legacy_prompt_fallback_for_v3_correction_forbidden") is True,
        "V3 corrective prompt-mode drift",
    )
    _require(
        out.get("reviewed_transfer_acceptance_correct") == 28
        and out.get("reviewed_legacy_acceptance_correct") == 24,
        "V3 reviewed prompt acceptance evidence drift",
    )

    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
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
        "contract_inspection_performs_host_io",
    ):
        _require(out.get(field) is False, "V3 boundary drift: " + field)

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate") == NEXT_GATE,
        "V3 source frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (SOURCE_PATH, SOURCE_GIT_BLOB),
        (TEST_PATH, TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v3_structured_correction_review_contract() -> dict[str, Any]:
    out = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "source_path": SOURCE_PATH,
        "source_git_blob": SOURCE_GIT_BLOB,
        "test_path": TEST_PATH,
        "test_git_blob": TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v3_structured_correction_reviewed": True,
        "exact_v2_trigger": out["exact_v2_trigger"],
        "move_units_unit_ids_required_json_type": "string",
        "structured_feedback_sha256": out["example_retry_context"][
            "structured_feedback_sha256"
        ],
        "preserve_transfer_system_prompt_required": True,
        "legacy_prompt_fallback_for_v3_correction_forbidden": True,
        "frozen_v8_tool_schema_modified": False,
        "frozen_v8_parser_modified": False,
        "frozen_v8_translator_modified": False,
        "host_validator_modified": False,
        "six_attempt_bound_modified": False,
        "malformed_unit_ids_coerced": False,
        "malformed_unit_ids_accepted": False,
        "runtime_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "validated_correction": out,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def integrate_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV3StructuredCorrectionReviewHold(NEXT_GATE)
