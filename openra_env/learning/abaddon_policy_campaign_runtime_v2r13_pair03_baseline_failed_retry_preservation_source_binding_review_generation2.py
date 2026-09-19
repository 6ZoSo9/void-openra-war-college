"""Source-only review of the failed pair-03 baseline retry preservation tool."""

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
    "v2r13-pair03-baseline-failed-retry-preservation-review-contract.v1"
)

PRESERVATION_CONTRACT_GIT_BLOB = "b38480ebcb32fb0397f722dad89193e8ec58cb98"
PRESERVATION_CONTRACT_SOURCE_SHA256 = (
    "0d8aa7948afbb5e85d9b61d7d1911f82c4c498f29b1fbf3136d1fb4e138e0569"
)
PRECISION_TOOL_GIT_BLOB = "344d3e0cc811f0dc9c3b5450c4b0b69d9a4c0c38"
PRECISION_TOOL_SOURCE_SHA256 = (
    "4a4c7ffdf247604e504b59c8d0d35e9c7152eed64fd8ed809dee39d77eed0a50"
)
PRESERVATION_TEST_GIT_BLOB = "4b58cd554ac81ff46471d53382c731579a9830bc"
PRESERVATION_TEST_SHA256 = (
    "1b8c1537d4fbacbdd75c68a371c71f1e0a51ceca15f36726a2fbc67c9e8750cc"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_pair03_baseline_failed_retry_preservation"


class V2R13Pair03BaselineFailedRetryPreservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineFailedRetryPreservationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_preservation_cached() -> dict[str, Any]:
    contract = preservation.v2r13_pair03_baseline_failed_retry_preservation_contract()

    _require(
        contract.get("failed_retry_forensics_sha256")
        == "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d",
        "failed-retry forensic identity drift",
    )
    _require(
        contract.get("failed_retry_warm_start_sha256")
        == "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798",
        "failed-retry warm-start identity drift",
    )
    _require(contract.get("failed_retry_warm_start_bytes") == 223319, "retry warm-start byte drift")
    _require(
        contract.get("original_warm_start_sha256")
        == "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28",
        "original archive warm-start drift",
    )
    _require(
        contract.get("original_preservation_receipt_file_sha256")
        == "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7",
        "original preservation receipt drift",
    )

    for field in (
        "exact_failed_retry_tree_required",
        "same_filesystem_atomic_rename_required",
        "archived_retry_tree_must_remain_unchanged",
        "original_first_attempt_archive_must_remain_unchanged",
        "preservation_implemented",
        "precision_preservation_tool_present",
    ):
        _require(contract.get(field) is True, f"preservation requirement missing: {field}")

    for field in (
        "failed_retry_deletion_authorized",
        "additional_retry_authorized",
        "automatic_retry",
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
        "precision_preservation_tool_source_binding_present",
        "preservation_invoked",
    ):
        _require(contract.get(field) is False, f"preservation boundary drift: {field}")

    _require(
        contract.get("next_gate")
        == "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pre-review preservation gate drift",
    )
    return deepcopy(contract)


def v2r13_pair03_baseline_failed_retry_preservation_review_contract() -> dict[str, Any]:
    validated = _validate_preservation_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "preservation_contract_git_blob": PRESERVATION_CONTRACT_GIT_BLOB,
        "preservation_contract_source_sha256": PRESERVATION_CONTRACT_SOURCE_SHA256,
        "precision_tool_git_blob": PRECISION_TOOL_GIT_BLOB,
        "precision_tool_source_sha256": PRECISION_TOOL_SOURCE_SHA256,
        "preservation_test_git_blob": PRESERVATION_TEST_GIT_BLOB,
        "preservation_test_sha256": PRESERVATION_TEST_SHA256,
        "preservation_source_binding_present": True,
        "preservation_reviewed": True,
        "precision_tool_reviewed": True,
        "same_filesystem_atomic_rename_reviewed": True,
        "no_delete_api_reviewed": True,
        "original_first_attempt_archive_preservation_reviewed": True,
        "preservation_invoked": False,
        "failed_retry_deletion_authorized": False,
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
    raise V2R13Pair03BaselineFailedRetryPreservationReviewHold(NEXT_GATE)
