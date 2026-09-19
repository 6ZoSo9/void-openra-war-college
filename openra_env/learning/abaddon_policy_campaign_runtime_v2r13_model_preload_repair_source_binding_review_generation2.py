"""Source-only review of the V2R13 model-preload-before-readiness repair."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-model-preload-repair-source-binding-review-contract.v1"
)

REPAIRED_INVOCATION_GIT_BLOB = "5b790efaf4085deb15eaef538635fd11f5cad9a5"
REPAIRED_INVOCATION_SOURCE_SHA256 = (
    "3d87705a42156b0603cfa945e455200f0999291b7d70ee57bf65334d8f8c4a40"
)
REPAIRED_TEST_GIT_BLOB = "0584426fe3dc10d79c6d535503f453529826dd1b"
REPAIRED_TEST_SHA256 = (
    "4ac3a8dff592c04e315e46e506318559595e7831887dada663705dd870ff8f6c"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_RETRY_REBIND_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_retry_rebind"


class V2R13ModelPreloadRepairReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13ModelPreloadRepairReviewHold(message)


@lru_cache(maxsize=1)
def _validate_repair_cached() -> dict[str, Any]:
    contract = invocation.first_baseline_invocation_contract()

    _require(contract.get("pair_slot") == 3, "repair pair-slot drift")
    _require(contract.get("arm") == "baseline", "repair arm drift")
    _require(contract.get("held_out") is False, "repair baseline became held-out")

    for field in (
        "fresh_canonical_live_readiness_before_inference_implemented",
        "exact_v2r13_model_preload_before_readiness_implemented",
        "model_preload_uses_empty_generate_prompt",
        "model_preload_requires_empty_response_text",
        "model_preload_token_evaluation_forbidden",
        "fresh_worktree_observation_from_materialization_path_record_implemented",
        "fresh_readiness_uses_reviewed_ollama_http_backend",
        "fresh_readiness_uses_reviewed_rootless_docker_backend",
    ):
        _require(contract.get(field) is True, f"preload repair contract missing: {field}")

    _require(
        contract.get("model_preload_inference_performed") is False,
        "preload repair crosses model-inference boundary",
    )
    _require(contract.get("automatic_retry") is False, "automatic retry enabled")
    _require(
        contract.get("candidate_arm_implemented_by_this_source") is False,
        "candidate execution leaked into preload repair",
    )
    _require(
        contract.get("held_out_arm_implemented_by_this_source") is False,
        "held-out execution leaked into preload repair",
    )

    for field in (
        "runtime_execution_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"preload repair boundary drift: {field}")

    return deepcopy(contract)


def v2r13_model_preload_repair_source_binding_review_contract() -> dict[str, Any]:
    validated = _validate_repair_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "repaired_invocation_git_blob": REPAIRED_INVOCATION_GIT_BLOB,
        "repaired_invocation_source_sha256": REPAIRED_INVOCATION_SOURCE_SHA256,
        "repaired_test_git_blob": REPAIRED_TEST_GIT_BLOB,
        "repaired_test_sha256": REPAIRED_TEST_SHA256,
        "repair_source_binding_present": True,
        "repair_reviewed": True,
        "exact_v2r13_model_preload_reviewed": True,
        "empty_generate_prompt_reviewed": True,
        "empty_response_required": True,
        "token_evaluation_forbidden": True,
        "model_load_before_readiness_reviewed": True,
        "model_inference_during_preload": False,
        "runtime_execution_invoked": False,
        "runtime_execution_performed": False,
        "automatic_retry": False,
        "candidate_arm_authorized": False,
        "held_out_arm_authorized": False,
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
        "validated_repair_contract": validated,
    }


def execute_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13ModelPreloadRepairReviewHold(NEXT_GATE)
