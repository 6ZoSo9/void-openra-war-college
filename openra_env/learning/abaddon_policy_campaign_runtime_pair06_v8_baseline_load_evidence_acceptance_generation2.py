"""Accept exact durable evidence for the completed pair-06 baseline V8 load.

This module binds the single authorized pair-06 baseline model-load attempt
completed on Precision. It records the exact launcher, canonical Git state,
invocation identity, authorization attestation, durable attempt marker, result
receipt, fresh runtime-environment verification, and exact 17-file asset
verification.

Import or contract inspection performs no host action. This acceptance grants
no second load, candidate load, inference, game execution, held-out execution,
training, promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_invocation_source_binding_review_generation2
    as invocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-load-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-load-evidence-acceptance.v1"
)

INVOCATION_REVIEW_GIT_BLOB = "9accb92a9af284922aeeee120f31178a02c99fe4"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "757e7ef4a53da7377355bd70953ac6f7011d9058abc9bb74ac25428fa5012b4e"
)

LAUNCHER_SHA256 = (
    "1d2b787f0ca5dd89701e4f9862088d8b458dce872034a870e36f73a5ef177246"
)
EXECUTION_MAIN_HEAD = "cdafee828fe3066651089e43cef88e4668d680ee"
EXECUTION_MAIN_TREE = "796e6ab771bbae3b9f82a74108ce8038713322a7"
INVOCATION_SOURCE_SHA256 = (
    "864e830cf2d62d3776321b75665f07b58f0b548d6a3dc114b0b9cd84eb9a2ea4"
)
AUTHORIZATION_ATTESTATION_SHA256 = (
    "1a498a1e596c03985f3c9f861df1d2182a7698acac9bd12cffe520f09a9502cc"
)
ATTEMPT_MARKER_SHA256 = (
    "59018bdfbd3058b2bd54b79797de19f60e47bfb5da20cab2779cbb974ec92b7d"
)
RESULT_FILE_SHA256 = (
    "aa5e05327460961df4239532b6c78599fc9340bb975e29f12691b64effd5f774"
)

EXPECTED_EVIDENCE = {
    "launcher_sha256": LAUNCHER_SHA256,
    "execution_main_head": EXECUTION_MAIN_HEAD,
    "execution_main_tree": EXECUTION_MAIN_TREE,
    "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
    "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
    "pair_slot": 6,
    "arm": "baseline",
    "held_out": False,
    "maximum_attempts": 1,
    "automatic_retry": False,
    "attempt_consumed": True,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "result_present": True,
    "result_file_sha256": RESULT_FILE_SHA256,
    "runtime_environment_verified": True,
    "runtime_assets_verified": True,
    "verified_asset_count": 17,
    "preclaim_runtime_execution_performed": False,
    "preclaim_model_execution_performed": False,
    "runtime_load_authorized": True,
    "runtime_load_performed": True,
    "model_weights_loaded": True,
    "candidate_runtime_load_authorized": False,
    "model_inference_authorized": False,
    "model_inference_performed": False,
    "game_execution_authorized": False,
    "game_execution_performed": False,
    "pair15_execution_authorized": False,
    "training_authorized": False,
    "training_performed": False,
    "deployment_authorized": False,
    "deployment_performed": False,
    "void_chain_mutation_authorized": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_authorized": False,
    "wallet_or_funds_action_performed": False,
}

NEXT_GATE = "PAIR06_V8_BASELINE_LOAD_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_load_evidence_review"


class Pair06V8BaselineLoadEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadEvidenceAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def _validate_dependency() -> dict[str, Any]:
    reviewed = invocation_review.pair06_v8_baseline_load_invocation_review_contract()

    _require(
        reviewed.get("pair06_v8_baseline_load_invocation_reviewed") is True,
        "pair06 baseline load invocation not reviewed",
    )
    _require(reviewed.get("pair_slot") == 6, "pair06 reviewed slot drift")
    _require(reviewed.get("arm") == "baseline", "pair06 reviewed arm drift")
    _require(reviewed.get("held_out") is False, "pair06 reviewed held-out drift")
    _require(
        reviewed.get("runtime_load_authorized_by_reviewed_dependency") is True,
        "pair06 reviewed load authority missing",
    )
    _require(
        reviewed.get("single_use_attempt_consumption_required") is True,
        "pair06 reviewed single-use boundary missing",
    )
    _require(
        reviewed.get("single_use_attempt_consumed") is False,
        "pair06 source review unexpectedly consumed attempt",
    )
    _require(reviewed.get("automatic_retry") is False, "pair06 automatic retry enabled")
    _require(
        reviewed.get("runtime_load_performed") is False
        and reviewed.get("model_weights_loaded") is False,
        "pair06 source review unexpectedly performed load",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_BASELINE_RUNTIME_LOAD_PRECISION_EXECUTION_REQUIRED",
        "pair06 pre-execution frontier drift",
    )

    for field in (
        "candidate_runtime_load_authorized",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
        "game_execution_performed",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(reviewed.get(field) is False, f"pair06 source-review scope drift: {field}")

    return deepcopy(reviewed)


def accept_pair06_v8_baseline_load_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "pair06 load evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair06 load evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair06 load evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair06 load evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_baseline_load_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "execution_main_tree": EXECUTION_MAIN_TREE,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
        "attempt_consumed": True,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "result_file_sha256": RESULT_FILE_SHA256,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "maximum_attempts": 1,
        "runtime_environment_verified": True,
        "runtime_assets_verified": True,
        "verified_asset_count": 17,
        "runtime_load_authorized": True,
        "runtime_load_performed": True,
        "model_weights_loaded": True,
        "persistent_runtime_handle_exported": False,
        "runtime_residency_after_launcher_attested": False,
        "another_baseline_load_authorized": False,
        "candidate_runtime_load_authorized": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "pair15_execution_performed": False,
        "automatic_retry": False,
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
        "runtime_lifetime_handoff_design_required": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "dependency_review": dependency,
    }


def pair06_v8_baseline_load_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_baseline_load_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
        "invocation_review_source_sha256": INVOCATION_REVIEW_SOURCE_SHA256,
        "pair06_v8_baseline_load_evidence_accepted": True,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_consumed": True,
        "maximum_attempts": 1,
        "runtime_load_performed": True,
        "model_weights_loaded": True,
        "persistent_runtime_handle_exported": False,
        "runtime_residency_after_launcher_attested": False,
        "another_baseline_load_authorized": False,
        "candidate_runtime_load_authorized": False,
        "game_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "runtime_lifetime_handoff_design_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineLoadEvidenceAcceptanceHold(NEXT_GATE)
