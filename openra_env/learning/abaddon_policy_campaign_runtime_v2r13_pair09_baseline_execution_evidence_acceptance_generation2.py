"""Accept exact durable evidence for the completed V2R13 pair-09 baseline.

This source binds the single authorized pair-09 baseline execution that completed
on Precision. It records the durable attempt/result identities, exact run
artifacts, executor/readiness receipts, and non-escalation boundaries.

Importing or inspecting this module performs no host action and grants no
candidate, held-out, training, promotion, deployment, VOID-chain, wallet, or
funds authority.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_invocation_source_binding_review_generation2
    as invocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-execution-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-execution-evidence-acceptance.v1"
)

LAUNCHER_SHA256 = (
    "1ef774f2de9323eb7ef01762574d1fc8ec1df8b557bf9b6e083028ca2388a945"
)
EXECUTION_MAIN_HEAD = "361b5e8a4033515d6bdd3a7f50456c778df5aa5f"
EXECUTION_MAIN_TREE = "f692fa0be5190e9e1401320c5a1a831127da0ac5"
INVOCATION_SOURCE_SHA256 = (
    "815d824bfa7aabc2659ff1fd2e4407c81dff7d5101103ac6868e6c1dfa5b768b"
)
SOURCE_BINDINGS_SHA256 = (
    "9d116f4b9f8c17ada27d49affb56e20a9e6312d3e54b06f3a4fb34b950b8fd52"
)

ATTEMPT_MARKER_SHA256 = (
    "57f862fe39a8939f3d47d4184fe264e0b9cd3988143f4cdc3adb9973a0e2e41c"
)
RESULT_FILE_SHA256 = (
    "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
)
REQUEST_SHA256 = (
    "5879d5fedbc6b16f62a777090ce947516625b003348cd9d9ac7c9520570ce4c1"
)

RUN_ID = "warmstart-apollyon-vs-abaddon-20260922T211556Z-feinter-s1496195137"
RUN_DIR = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-09/baseline/runs/" + RUN_ID
)
SEED = 1496195137
OUTCOME = "DRAW_OR_UNFINISHED"
ROUNDS_COMPLETED = 36
FINAL_TICK = 3551
WARM_START_HANDOFF_TICK = 2651
WARM_START_SHA256 = (
    "d40816f63f86b5103b9d181ecc31e6b694005c1f3032a1b3fc614a209f2d7790"
)
TRAJECTORY_SHA256 = (
    "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
)
SUMMARY_SHA256 = (
    "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
)

EXECUTOR_RECEIPT_SHA256 = (
    "0a868ad891b11a2a5910555939725a01292018aad3156428c9bb5599fd10a3cc"
)
AUTHORIZATION_ATTESTATION_SHA256 = (
    "34ad7143e876b91056f730de37ab470b6fd8a5f99d84aadefb178cabf87a2031"
)
PLAN_SHA256 = (
    "6b1ddf22b9716a4c694003d4d126e97bbe028a1335c2ad2b5ddbadd3053cc02f"
)
FRESH_READINESS_ADMISSION_SHA256 = (
    "9ad68457eac9bdb2688e73496935da2067185be22c4b8ab7ac071b1b2871bfb7"
)
FRESH_READINESS_EVIDENCE_SHA256 = (
    "1facd8327ec0b35c3e4ee2d6d5442bdb15936692a1ac9fe1dc064077dcc68572"
)
HOST_PREFLIGHT_SNAPSHOT_SHA256 = (
    "9963a9665a21cc963c361cef5939704b59cd257bf8c6e58927e710eb67177578"
)

EXPECTED_EVIDENCE = {
    "launcher_sha256": LAUNCHER_SHA256,
    "execution_main_head": EXECUTION_MAIN_HEAD,
    "execution_main_tree": EXECUTION_MAIN_TREE,
    "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
    "source_bindings_sha256": SOURCE_BINDINGS_SHA256,
    "pair_slot": 9,
    "arm": "baseline",
    "held_out": False,
    "maximum_attempts": 1,
    "automatic_retry": False,
    "attempt_consumed": True,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "request_sha256": REQUEST_SHA256,
    "result_present": True,
    "result_file_sha256": RESULT_FILE_SHA256,
    "run_id": RUN_ID,
    "run_dir": RUN_DIR,
    "seed": SEED,
    "outcome": OUTCOME,
    "rounds_completed": ROUNDS_COMPLETED,
    "final_tick": FINAL_TICK,
    "warm_start_handoff_tick": WARM_START_HANDOFF_TICK,
    "warm_start_contact_achieved": False,
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
    "runtime_execution_authorized": True,
    "runtime_execution_performed": True,
    "runtime_started": True,
    "runtime_cleanup_attempted": True,
    "runtime_cleanup_completed": True,
    "fresh_runtime_readiness_admitted": True,
    "revocation_checked_before_materialization": True,
    "revocation_checked_before_inference": True,
    "executor_receipt_sha256": EXECUTOR_RECEIPT_SHA256,
    "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
    "plan_sha256": PLAN_SHA256,
    "fresh_readiness_admission_sha256": FRESH_READINESS_ADMISSION_SHA256,
    "fresh_readiness_evidence_sha256": FRESH_READINESS_EVIDENCE_SHA256,
    "host_preflight_snapshot_sha256": HOST_PREFLIGHT_SNAPSHOT_SHA256,
    "pair03_baseline_preserved": True,
    "pair03_candidate_preserved": True,
    "candidate_execution_performed": False,
    "held_out_execution_performed": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
    "ollama_active_after": "inactive",
    "ollama_enabled_after": "disabled",
    "activation_permit_present_after": False,
}

NEXT_GATE = (
    "V2R13_PAIR09_BASELINE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair09_baseline_execution_evidence_review"
)


class V2R13Pair09BaselineExecutionEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineExecutionEvidenceAcceptanceHold(message)


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
        .v2r13_pair09_baseline_invocation_review_contract()
    )
    _require(
        reviewed.get("pair09_baseline_invocation_source_binding_present") is True,
        "pair09 invocation source binding missing",
    )
    _require(
        reviewed.get("pair09_baseline_invocation_reviewed") is True,
        "pair09 invocation source not reviewed",
    )
    _require(reviewed.get("precision_cli_reviewed") is True, "pair09 CLI not reviewed")
    _require(reviewed.get("pair_slot") == 9, "pair09 reviewed slot drift")
    _require(reviewed.get("arm") == "baseline", "pair09 reviewed arm drift")
    _require(reviewed.get("held_out") is False, "pair09 reviewed held-out drift")
    _require(reviewed.get("single_use_attempt") is True, "pair09 one-shot drift")
    _require(reviewed.get("automatic_retry") is False, "pair09 automatic retry enabled")
    _require(
        reviewed.get("pair09_baseline_execution_performed") is False,
        "source review unexpectedly records runtime execution",
    )
    _require(
        reviewed.get("next_gate")
        == "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
        "pair09 pre-execution frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair09_baseline_execution_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "pair09 baseline evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair09 baseline evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair09 baseline evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair09 baseline evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair09_baseline_execution_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "execution_main_tree": EXECUTION_MAIN_TREE,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "attempt_consumed": True,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "result_file_sha256": RESULT_FILE_SHA256,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "run_id": RUN_ID,
        "seed": SEED,
        "outcome": OUTCOME,
        "rounds_completed": ROUNDS_COMPLETED,
        "final_tick": FINAL_TICK,
        "warm_start_sha256": WARM_START_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "pair03_baseline_preserved": True,
        "pair03_candidate_preserved": True,
        "automatic_retry": False,
        "another_baseline_execution_authorized": False,
        "candidate_execution_authorized": False,
        "candidate_execution_performed": False,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
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


def v2r13_pair09_baseline_execution_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair09_baseline_execution_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair09_baseline_execution_evidence_accepted": True,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_consumed": True,
        "maximum_attempts": 1,
        "another_baseline_execution_authorized": False,
        "candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "automatic_retry": False,
        "baseline_result_review_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineExecutionEvidenceAcceptanceHold(NEXT_GATE)
