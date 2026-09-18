"""Source-only review of the V2R13 pair-03 baseline readiness-bridge repair.

Pins the repaired first-baseline invocation and regression tests.  This review
does not authorize a retry.  The first runtime attempt created the pair-03
baseline arm root and failed during fresh-readiness admission before controller
inference, so failed-attempt forensics must be completed first.
"""

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
    "v2r13-first-baseline-worktree-readiness-repair-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-first-baseline-worktree-readiness-repair-review.v1"
)

REPAIRED_INVOCATION_GIT_BLOB = "c5785b53ed0261981f25db116ceb1a43042a7580"
REPAIRED_INVOCATION_SOURCE_SHA256 = (
    "b840ae629eb2599aa61c6bad2661ca1f3d2dd4d66204579c980666325311816c"
)
REPAIRED_TEST_GIT_BLOB = "52f7d70e8ecb8b99efb85c5dc1aa17b52e258961"
REPAIRED_TEST_SHA256 = (
    "8b1e97e732030ac2bb6cb0cbabff8b07926b1a0cdc1a77d76ba931352f054ed9"
)
PRECISION_CLI_GIT_BLOB = "f543834f86ff52be41498123b423cc1ab9e75f49"

NEXT_GATE = "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_FORENSICS_REQUIRED"
NEXT_CHANGE_CLASS = "precision_read_only_v2r13_pair03_baseline_failed_attempt_forensics"


class V2R13FirstBaselineReadinessRepairReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13FirstBaselineReadinessRepairReviewHold(message)


@lru_cache(maxsize=1)
def _validate_repaired_invocation_cached() -> dict[str, Any]:
    contract = invocation.first_baseline_invocation_contract()

    _require(contract.get("pair_slot") == 3, "repair pair-slot drift")
    _require(contract.get("arm") == "baseline", "repair arm drift")
    _require(contract.get("held_out") is False, "repair baseline became held-out")

    for field in (
        "execution_requires_current_main_preflight",
        "execution_requires_cached_sudo_authority",
        "execution_requires_revocation_sentinel_absent",
        "execution_requires_isolated_grpc_python",
        "restricted_git_worktree_backend_implemented",
        "fresh_canonical_live_readiness_before_inference_implemented",
        "fresh_worktree_observation_from_materialization_path_record_implemented",
        "fresh_worktree_observation_uses_explicit_host_lstat_backend",
        "fresh_worktree_observation_uses_reviewed_git_backend",
        "fresh_worktree_observation_uses_reviewed_path_resolver",
        "fresh_readiness_uses_reviewed_ollama_http_backend",
        "fresh_readiness_uses_reviewed_rootless_docker_backend",
    ):
        _require(contract.get(field) is True, f"repair contract missing: {field}")

    _require(
        contract.get("materialization_receipt_direct_worktree_admission") is False,
        "repair still admits materialization receipt directly",
    )
    _require(
        contract.get("candidate_arm_implemented_by_this_source") is False,
        "repair expanded into candidate execution",
    )
    _require(
        contract.get("held_out_arm_implemented_by_this_source") is False,
        "repair expanded into held-out execution",
    )
    _require(contract.get("automatic_retry") is False, "repair enabled automatic retry")
    _require(
        contract.get("runtime_execution_authorized") is True,
        "underlying accepted runtime authority disappeared",
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
        _require(contract.get(field) is False, f"repair boundary drift: {field}")

    return deepcopy(contract)


def v2r13_first_baseline_worktree_readiness_repair_review() -> dict[str, Any]:
    validated = _validate_repaired_invocation_cached()
    return {
        "schema": REVIEW_SCHEMA,
        "repaired_invocation_git_blob": REPAIRED_INVOCATION_GIT_BLOB,
        "repaired_invocation_source_sha256": REPAIRED_INVOCATION_SOURCE_SHA256,
        "repaired_test_git_blob": REPAIRED_TEST_GIT_BLOB,
        "repaired_test_sha256": REPAIRED_TEST_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "separate_review_instrument": True,
        "materialization_receipt_direct_worktree_admission": False,
        "materialization_path_record_observed_before_live_readiness": True,
        "canonical_worktree_observation_validated_before_live_readiness": True,
        "explicit_host_lstat_backend_reviewed": True,
        "reviewed_git_observer_backend_reviewed": True,
        "reviewed_path_resolver_reviewed": True,
        "runtime_retry_authorized_by_this_review": False,
        "automatic_retry": False,
        "candidate_arm_authorized_by_this_review": False,
        "held_out_arm_authorized_by_this_review": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "failed_attempt_forensics_required": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_repaired_invocation_contract": deepcopy(validated),
    }


def v2r13_first_baseline_worktree_readiness_repair_review_contract() -> dict[str, Any]:
    review = v2r13_first_baseline_worktree_readiness_repair_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "repaired_invocation_git_blob": REPAIRED_INVOCATION_GIT_BLOB,
        "repaired_invocation_source_sha256": REPAIRED_INVOCATION_SOURCE_SHA256,
        "repaired_test_git_blob": REPAIRED_TEST_GIT_BLOB,
        "repaired_test_sha256": REPAIRED_TEST_SHA256,
        "precision_cli_git_blob": PRECISION_CLI_GIT_BLOB,
        "repair_source_binding_present": True,
        "repair_reviewed": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "failed_attempt_forensics_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": review,
    }


def retry_pair03_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13FirstBaselineReadinessRepairReviewHold(NEXT_GATE)
