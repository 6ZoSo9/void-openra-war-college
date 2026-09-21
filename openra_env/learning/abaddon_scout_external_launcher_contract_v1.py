"""Non-executing source-bound proposal for a future Abaddon scout experiment.

This module fixes the source inventory, experiment scope, required gates, and
result-binding requirements for a future reviewed launcher. It is deliberately
incapable of starting a runtime, consuming an attempt, authenticating an
operator, loading a model, executing a game, or accepting a result as proof.

A matching proposal digest is never execution authority. The completed pair-03
attempt and its launcher are explicitly non-reusable.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


REQUEST_SCHEMA = "void.abaddon.scout-external-launcher-request.v1"
VALIDATION_SCHEMA = "void.abaddon.scout-external-launcher-request-validation.v1"
RESULT_SCHEMA = "void.abaddon.scout-external-result-requirements.v1"
NEXT_GATE = "SCOUT_EXTERNAL_LAUNCHER_SOURCE_REVIEW_REQUIRED"
MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"
MAX_REQUEST_BYTES = 8192
REQUEST_SHA256 = "67582949d9cbb6815c59ba9c78e6ac40fc303080320b5d707ad2b9e64e9baf55"

SOURCE_REFERENCES = (
    (
        "openra_env/learning/abaddon_scout_runner_binding_v1.py",
        "9e4894b64f0820a53faf8226974d99687066679b",
    ),
    (
        "openra_env/learning/abaddon_scout_host_bridge_v1.py",
        "1fa8ea14c757e46658813dca035037f125e23880",
    ),
    (
        "openra_env/learning/abaddon_scout_missions_v1.py",
        "12ca91f68f595919061dd6d5f927fb46428c9a58",
    ),
    (
        "openra_env/learning/goal_effect_core_v1.py",
        "0bd626f6733a77a4861d71e5dea093d0a899c878",
    ),
    (
        "fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py",
        "132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51",
    ),
    (
        "fixtures/learning/scout-missions-v1/joint_host_v1_2.py",
        "6e751b855da1d9425c4fd2bd5a997ae1c742ae11",
    ),
    (
        "fixtures/learning/scout-missions-v1/abaddon_controller_v1.py",
        "938afb496bfe704c5ff75adbf938473d9c431062",
    ),
    (
        "fixtures/learning/scout-missions-v1/rl_bridge.proto",
        "a20e85cf7d9f3b4c1523b1916569942d7b74e694",
    ),
)

HISTORICAL_SHA256 = {
    "warm_start_runner_v1_4.py": (
        "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
    ),
    "joint_host_v1_2.py": (
        "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615"
    ),
    "abaddon_controller_v1.py": (
        "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
    ),
}

REQUIRED_GATES = (
    "exact_launcher_source_reviewed",
    "exact_source_inventory_verified",
    "fresh_experiment_identity_accepted",
    "fresh_durable_single_use_attempt_guard",
    "consumed_pair03_slot_not_reused",
    "current_operation_authority_rechecked",
    "fresh_runtime_readiness_verified",
    "post_run_runtime_state_independently_verified",
    "result_and_trajectory_bound_to_admitted_source_inventory",
)

FALSE_AUTHORITY_FIELDS = (
    "operator_authenticated",
    "source_inventory_verified",
    "runtime_readiness_verified",
    "fresh_attempt_guard_bound",
    "fresh_attempt_consumed",
    "scout_experiment_authorized",
    "scout_execution_authorized",
    "scout_execution_performed",
    "result_evidence_verified",
    "post_run_state_verified",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutExternalLauncherContractHold(ValueError):
    """The fixed proposal drifted or an unauthorized action was requested."""


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "main_head": MAIN_HEAD,
        "source_references": dict(SOURCE_REFERENCES),
        "historical_sha256": dict(HISTORICAL_SHA256),
        "proposed_scope": {
            "experiment_family": "abaddon-scout-source-bound-v1",
            "maximum_attempts": 1,
            "maximum_automatic_retries": 0,
            "pair03_attempt_reuse_allowed": False,
            "pair03_attempt_reset_allowed": False,
            "held_out": False,
        },
        "required_gates": list(REQUIRED_GATES),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "binding_claims": {
            "matching_request_digest_grants_authority": False,
            "source_contract_grants_runtime_authority": False,
            "historical_pair03_authority_reusable": False,
            "callback_return_proves_shutdown": False,
            "historical_cleanup_prints_prove_shutdown": False,
        },
        "result_requirements": {
            "exact_source_inventory_required": True,
            "trajectory_sha256_required": True,
            "result_sha256_required": True,
            "fresh_attempt_identity_required": True,
            "independent_post_run_state_required": True,
            "automatic_training_admission": False,
            "automatic_policy_promotion": False,
        },
        "next_gate": NEXT_GATE,
    }


def build_scout_launcher_request() -> bytes:
    """Return the one canonical non-authorizing proposal."""
    return (
        json.dumps(
            _request_record(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def validate_scout_launcher_request(payload: bytes) -> dict[str, Any]:
    """Validate exact canonical bytes; successful validation grants no authority."""
    if type(payload) is not bytes:
        raise ScoutExternalLauncherContractHold("request must be exact bytes")
    if not 0 < len(payload) <= MAX_REQUEST_BYTES:
        raise ScoutExternalLauncherContractHold("request byte limit")
    if payload != build_scout_launcher_request():
        raise ScoutExternalLauncherContractHold("request bytes differ from fixed proposal")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != REQUEST_SHA256:
        raise ScoutExternalLauncherContractHold("request digest drift")
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": digest,
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def scout_launcher_contract() -> dict[str, Any]:
    """Return fresh proposal/validation snapshots without granting authority."""
    validation = validate_scout_launcher_request(build_scout_launcher_request())
    validation["request"] = _request_record()
    return validation


def scout_result_requirements() -> dict[str, Any]:
    """Describe what a future result binder must prove; accept no result here."""
    return {
        "schema": RESULT_SCHEMA,
        "source_references": dict(SOURCE_REFERENCES),
        "historical_sha256": dict(HISTORICAL_SHA256),
        "fresh_attempt_identity_required": True,
        "trajectory_sha256_required": True,
        "result_sha256_required": True,
        "independent_post_run_state_required": True,
        "pair03_attempt_reuse_allowed": False,
        "automatic_retry": False,
        "automatic_training_admission": False,
        "automatic_policy_promotion": False,
        "result_evidence_verified": False,
        "post_run_state_verified": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute_scout(*args: Any, **kwargs: Any) -> None:
    """Execution remains impossible in this source-only contract."""
    raise ScoutExternalLauncherContractHold(NEXT_GATE)


def accept_result_as_verified(*args: Any, **kwargs: Any) -> None:
    """No caller-supplied result is accepted by this proposal module."""
    raise ScoutExternalLauncherContractHold(NEXT_GATE)
