"""Source-only review of the failed-retry preservation guard repair."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_generation2
    as preservation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-failed-retry-preservation-guard-repair-review-contract.v1"
)

PRESERVATION_CONTRACT_GIT_BLOB = "b38480ebcb32fb0397f722dad89193e8ec58cb98"
CORRECTED_PRECISION_TOOL_GIT_BLOB = "812d78f28f8d7f0b486b1b2bb7cce3b9da2a2733"
CORRECTED_PRECISION_TOOL_SOURCE_SHA256 = (
    "cf003915c8e9d7cac58c080ac9455f815afc7bea120a4b5056718957ca02913c"
)
CORRECTED_TEST_GIT_BLOB = "1ac81d60ed4bdb7877d8bb34919952b4e83381fb"
CORRECTED_TEST_SHA256 = (
    "ddba7d498fcc061fd477fd4c64052e95c62f8f433191f78b20208ecaec01d071"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_failed_retry_preservation"


class V2R13FailedRetryPreservationGuardRepairReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13FailedRetryPreservationGuardRepairReviewHold(message)


@lru_cache(maxsize=1)
def _validate_contract_cached() -> dict[str, Any]:
    contract = preservation.v2r13_pair03_baseline_failed_retry_preservation_contract()

    _require(
        contract.get("preservation_implemented") is True,
        "preservation implementation state must be true",
    )
    _require(
        contract.get("precision_preservation_tool_present") is True,
        "precision preservation tool missing",
    )
    _require(
        contract.get("precision_preservation_tool_source_binding_present") is False,
        "contract unexpectedly self-binds precision tool",
    )
    _require(contract.get("preservation_invoked") is False, "preservation already invoked")
    _require(
        contract.get("additional_retry_authorized") is False,
        "preservation unexpectedly authorizes retry",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")

    for field in (
        "runtime_start_authorized",
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"preservation boundary drift: {field}")

    return deepcopy(contract)


def v2r13_failed_retry_preservation_guard_repair_review_contract() -> dict[str, Any]:
    validated = _validate_contract_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_contract_git_blob": PRESERVATION_CONTRACT_GIT_BLOB,
        "corrected_precision_tool_git_blob": CORRECTED_PRECISION_TOOL_GIT_BLOB,
        "corrected_precision_tool_source_sha256": (
            CORRECTED_PRECISION_TOOL_SOURCE_SHA256
        ),
        "corrected_test_git_blob": CORRECTED_TEST_GIT_BLOB,
        "corrected_test_sha256": CORRECTED_TEST_SHA256,
        "guard_repair_source_binding_present": True,
        "guard_repair_reviewed": True,
        "expected_preservation_implemented_value": True,
        "contract_implementation_guard_polarity_correct": True,
        "preservation_invoked": False,
        "additional_retry_authorized": False,
        "automatic_retry": False,
        "runtime_execution_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_preservation_contract": validated,
    }


def invoke_preservation(*args: Any, **kwargs: Any) -> None:
    raise V2R13FailedRetryPreservationGuardRepairReviewHold(NEXT_GATE)
