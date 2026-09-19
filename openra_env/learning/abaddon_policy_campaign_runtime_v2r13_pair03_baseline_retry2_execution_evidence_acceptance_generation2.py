"""Accept exact Precision evidence for V2R13 pair-03 baseline retry index 2.

This gate binds the successful one-shot retry-2 runtime receipt and its run
artifact. It records the observed DRAW_OR_UNFINISHED result without promoting
it, authorizing a candidate arm, authorizing another retry, training, changing
weights, deploying, mutating VOID, or touching wallets/funds.

Importing or inspecting this module performs no host action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_invocation_source_binding_review_generation2
    as invocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry2-execution-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-retry2-execution-evidence-acceptance.v1"
)

LAUNCHER_SHA256 = (
    "e48dff60a089ed3cfa75729ecaec60cb52d41037663eb46cb1a8929540ac833c"
)
EXECUTION_MAIN_HEAD = "3432cc19f7612f7e3819eefe2c207d302cd4b580"
EXECUTION_MAIN_TREE = "1e07d46a3fbd03c963def4389064ea12577f5648"

RUN_ID = "warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685"
RUN_DIR = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/baseline/runs/"
    + RUN_ID
)
OUTCOME = "DRAW_OR_UNFINISHED"
ROUNDS_COMPLETED = 36
FINAL_TICK = 3551
WARM_START_HANDOFF_TICK = 2651
WARM_START_SHA256 = (
    "2f5de8450cae1e96d4db20c1f1ec0aa8ee0cccda2d77a1c794a162dcb5763958"
)
TRAJECTORY_SHA256 = (
    "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
)
SUMMARY_SHA256 = (
    "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
)

ADDITIONAL_RETRY_INVOCATION_RECEIPT_SHA256 = (
    "9075720e81a55afe02d285d541c559e5cd9b03a32251d36d39c4ef4362052e74"
)
UNDERLYING_INVOCATION_RECEIPT_SHA256 = (
    "2f242dbd6ff5840074b74b554cf330c59755a29cfd17d35feda182a6424e3694"
)
UNDERLYING_EXECUTOR_RECEIPT_SHA256 = (
    "352677479e3a2864ee5a792bc2557b77bcfeccb0f497920f9784a8b82cd75e4d"
)
EXECUTION_RECEIPT_FILE_SHA256 = (
    "0bf4fd6f780eaddec758c785f16b456cd4707a67ad01fd7a0d8af7bafb06da86"
)
FRESH_HOST_PREFLIGHT_SNAPSHOT_SHA256 = (
    "da32564f2459d67d6fcc254fbc53810a02aa57a1c177f758ebb3efc7cf9b24b0"
)
FRESH_READINESS_ADMISSION_SHA256 = (
    "19ced538fe6cb2c3660bf39189bce6ae6dc554ea0e1f7418d9b7c81368d5b79d"
)
FRESH_READINESS_EVIDENCE_SHA256 = (
    "fde2176e0989dc55682ee8a322c633135fe3bbcb1cf234061c153f80b156d3ce"
)

FIRST_ARCHIVED_WARM_START_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
FIRST_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
)
RETRY1_ARCHIVED_WARM_START_SHA256 = (
    "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
)
RETRY1_PRESERVATION_RECEIPT_SHA256 = (
    "833fb5bde1bbb96d6e2ceedff615fd86bf3b2522d21687d900355cbe705a0f15"
)
RETRY1_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "007127f4834e3b2c772316f2f65a3b355c308a7a451eca996ad00c21f3f7cd28"
)

EXPECTED_EVIDENCE = {
    "launcher_sha256": LAUNCHER_SHA256,
    "execution_main_head": EXECUTION_MAIN_HEAD,
    "execution_main_tree": EXECUTION_MAIN_TREE,
    "pair_slot": 3,
    "arm": "baseline",
    "held_out": False,
    "retry_index": 2,
    "max_additional_retry_executions": 1,
    "total_retry_executions_authorized": 2,
    "additional_retry_authorization_consumed": True,
    "additional_retry_execution_performed": True,
    "remaining_additional_retry_executions": 0,
    "automatic_retry": False,
    "recursive_retry": False,
    "run_id": RUN_ID,
    "run_dir": RUN_DIR,
    "outcome": OUTCOME,
    "rounds_completed": ROUNDS_COMPLETED,
    "final_tick": FINAL_TICK,
    "warm_start_handoff_tick": WARM_START_HANDOFF_TICK,
    "warm_start_sha256": WARM_START_SHA256,
    "trajectory_sha256": TRAJECTORY_SHA256,
    "summary_sha256": SUMMARY_SHA256,
    "actual_apollyon_vs_actual_abaddon": True,
    "controller_rows_joint_same_tick": True,
    "warm_start_rows_excluded_from_agent_training": True,
    "candidate_only": True,
    "automatic_corpus_admission": False,
    "automatic_apollyon_weight_mutation": False,
    "automatic_abaddon_policy_promotion": False,
    "fresh_runtime_readiness_admitted": True,
    "fresh_host_preflight_snapshot_sha256": FRESH_HOST_PREFLIGHT_SNAPSHOT_SHA256,
    "fresh_readiness_admission_sha256": FRESH_READINESS_ADMISSION_SHA256,
    "fresh_readiness_evidence_sha256": FRESH_READINESS_EVIDENCE_SHA256,
    "runtime_execution_performed": True,
    "runtime_cleanup_completed": True,
    "candidate_arm_executed": False,
    "held_out_arm_executed": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
    "additional_retry_invocation_receipt_sha256": (
        ADDITIONAL_RETRY_INVOCATION_RECEIPT_SHA256
    ),
    "underlying_invocation_receipt_sha256": UNDERLYING_INVOCATION_RECEIPT_SHA256,
    "underlying_executor_receipt_sha256": UNDERLYING_EXECUTOR_RECEIPT_SHA256,
    "execution_receipt_file_sha256": EXECUTION_RECEIPT_FILE_SHA256,
    "first_archived_warm_start_sha256": FIRST_ARCHIVED_WARM_START_SHA256,
    "first_preservation_receipt_file_sha256": (
        FIRST_PRESERVATION_RECEIPT_FILE_SHA256
    ),
    "retry1_archived_warm_start_sha256": RETRY1_ARCHIVED_WARM_START_SHA256,
    "retry1_preservation_receipt_sha256": RETRY1_PRESERVATION_RECEIPT_SHA256,
    "retry1_preservation_receipt_file_sha256": (
        RETRY1_PRESERVATION_RECEIPT_FILE_SHA256
    ),
    "ollama_active_after": "inactive",
    "ollama_enabled_after": "disabled",
    "activation_permit_present_after": False,
}

NEXT_GATE = (
    "V2R13_PAIR03_BASELINE_RETRY2_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair03_baseline_retry2_execution_evidence_review"
)


class V2R13Pair03BaselineRetry2ExecutionEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineRetry2ExecutionEvidenceAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def _validate_dependency() -> dict[str, Any]:
    reviewed = (
        invocation_review
        .v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    )
    _require(
        reviewed.get("invocation_source_binding_present") is True,
        "retry-2 invocation source binding missing",
    )
    _require(reviewed.get("invocation_reviewed") is True, "retry-2 invocation not reviewed")
    _require(reviewed.get("pair_slot") == 3, "reviewed pair-slot drift")
    _require(reviewed.get("arm") == "baseline", "reviewed arm drift")
    _require(reviewed.get("retry_index") == 2, "reviewed retry index drift")
    _require(
        reviewed.get("single_additional_retry_invocation_reviewed") is True,
        "single retry-2 invocation review missing",
    )
    _require(reviewed.get("automatic_retry") is False, "automatic retry enabled")
    _require(reviewed.get("recursive_retry") is False, "recursive retry enabled")
    _require(
        reviewed.get("runtime_execution_performed") is False,
        "review source unexpectedly records runtime execution",
    )
    _require(
        reviewed.get("next_gate")
        == "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED",
        "retry-2 invocation frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair03_baseline_retry2_execution_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "retry-2 evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "retry-2 evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"retry-2 evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "retry-2 evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "retry2_execution_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "pair_slot": 3,
        "arm": "baseline",
        "held_out": False,
        "retry_index": 2,
        "additional_retry_authorization_consumed": True,
        "additional_retry_execution_performed": True,
        "remaining_additional_retry_executions": 0,
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "run_id": RUN_ID,
        "outcome": OUTCOME,
        "rounds_completed": ROUNDS_COMPLETED,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "automatic_retry": False,
        "recursive_retry": False,
        "another_retry_authorized": False,
        "candidate_arm_authorized": False,
        "candidate_arm_executed": False,
        "held_out_arm_authorized": False,
        "held_out_arm_executed": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "automatic_policy_promotion": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "baseline_result_review_required": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "dependency_review": dependency,
    }


def v2r13_pair03_baseline_retry2_execution_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair03_baseline_retry2_execution_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "retry2_execution_evidence_accepted": True,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "additional_retry_authorization_consumed": True,
        "remaining_additional_retry_executions": 0,
        "another_retry_authorized": False,
        "candidate_arm_authorized": False,
        "held_out_arm_authorized": False,
        "automatic_retry": False,
        "recursive_retry": False,
        "baseline_result_review_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def authorize_candidate_or_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineRetry2ExecutionEvidenceAcceptanceHold(NEXT_GATE)
