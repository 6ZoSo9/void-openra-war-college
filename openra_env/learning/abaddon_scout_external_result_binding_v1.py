"""Bind declared scout result identities without accepting them as evidence.

A future caller may use this module to construct one canonical record tying a
fresh scout experiment identity to an attempt marker, trajectory, result payload,
post-run-state evidence digest, and the exact reviewed source inventory.

This module does not read those files and therefore does not verify that any
declared digest corresponds to reality. It cannot authenticate an operator,
authorize execution, admit training data, promote a policy, deploy, mutate VOID,
or move funds. Result acceptance requires a separate external evidence review.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


SCHEMA = "void.abaddon.scout-external-result-binding.v1"
VALIDATION_SCHEMA = "void.abaddon.scout-external-result-binding-validation.v1"
MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"
NEXT_GATE = "SCOUT_EXTERNAL_RESULT_EVIDENCE_REVIEW_REQUIRED"
MAX_BINDING_BYTES = 16384

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
    (
        "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py",
        "1f7ee7057c27946f488afe26501482ea4f4fc53d",
    ),
    (
        "openra_env/learning/abaddon_scout_external_launcher_contract_review_v1.py",
        "3b6281b6a7bcaa9d5b3d9300728103883a810a6c",
    ),
    (
        "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py",
        "043225a7ff6528b9ae7f80994fe17480ad36ed3e",
    ),
    (
        "openra_env/learning/abaddon_scout_external_attempt_guard_review_v1.py",
        "858a218e87b2dc2eee21a9065bd530fcc0523ee2",
    ),
)

FALSE_VERIFICATION_FIELDS = (
    "source_inventory_verified",
    "attempt_marker_verified",
    "trajectory_verified",
    "result_payload_verified",
    "post_run_state_verified",
    "result_evidence_verified",
)

FALSE_AUTHORITY_FIELDS = (
    "operator_authenticated",
    "scout_experiment_authorized",
    "scout_execution_authorized",
    "scout_execution_performed",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutExternalResultBindingHold(ValueError):
    """The declared binding drifted or a verification/authority claim was requested."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutExternalResultBindingHold(code)


def _valid_hex64(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _valid_experiment_id(value: Any) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= 128
        and value.startswith("abaddon-scout-")
        and "pair03" not in value
        and all(character in "abcdefghijklmnopqrstuvwxyz0123456789._-" for character in value)
    )


def _binding_record(
    *,
    experiment_id: str,
    attempt_marker_sha256: str,
    trajectory_sha256: str,
    result_payload_sha256: str,
    post_run_state_sha256: str,
) -> dict[str, Any]:
    _require(_valid_experiment_id(experiment_id), "SCOUT_RESULT_EXPERIMENT_ID_INVALID")
    for label, value in (
        ("attempt_marker", attempt_marker_sha256),
        ("trajectory", trajectory_sha256),
        ("result_payload", result_payload_sha256),
        ("post_run_state", post_run_state_sha256),
    ):
        _require(_valid_hex64(value), f"SCOUT_RESULT_{label.upper()}_DIGEST_INVALID")

    return {
        "schema": SCHEMA,
        "record_kind": "declared_identities_not_verified_evidence",
        "main_head": MAIN_HEAD,
        "experiment_id": experiment_id,
        "source_references": dict(SOURCE_REFERENCES),
        "declared_digests": {
            "attempt_marker_sha256": attempt_marker_sha256,
            "trajectory_sha256": trajectory_sha256,
            "result_payload_sha256": result_payload_sha256,
            "post_run_state_sha256": post_run_state_sha256,
        },
        "verification": {field: False for field in FALSE_VERIFICATION_FIELDS},
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "pair03_attempt_reuse_allowed": False,
        "pair03_attempt_reset_allowed": False,
        "automatic_retry": False,
        "declared_digest_is_self_authenticating": False,
        "callback_return_proves_shutdown": False,
        "historical_cleanup_prints_prove_shutdown": False,
        "next_gate": NEXT_GATE,
    }


def build_scout_result_binding(
    *,
    experiment_id: str,
    attempt_marker_sha256: str,
    trajectory_sha256: str,
    result_payload_sha256: str,
    post_run_state_sha256: str,
) -> bytes:
    record = _binding_record(
        experiment_id=experiment_id,
        attempt_marker_sha256=attempt_marker_sha256,
        trajectory_sha256=trajectory_sha256,
        result_payload_sha256=result_payload_sha256,
        post_run_state_sha256=post_run_state_sha256,
    )
    raw = (
        json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")
    _require(len(raw) <= MAX_BINDING_BYTES, "SCOUT_RESULT_BINDING_BYTE_LIMIT")
    return raw


def validate_scout_result_binding(
    payload: bytes,
    *,
    experiment_id: str,
    attempt_marker_sha256: str,
    trajectory_sha256: str,
    result_payload_sha256: str,
    post_run_state_sha256: str,
) -> dict[str, Any]:
    _require(type(payload) is bytes, "SCOUT_RESULT_BINDING_EXACT_BYTES_REQUIRED")
    expected = build_scout_result_binding(
        experiment_id=experiment_id,
        attempt_marker_sha256=attempt_marker_sha256,
        trajectory_sha256=trajectory_sha256,
        result_payload_sha256=result_payload_sha256,
        post_run_state_sha256=post_run_state_sha256,
    )
    _require(payload == expected, "SCOUT_RESULT_BINDING_BYTES_DRIFT")

    return {
        "schema": VALIDATION_SCHEMA,
        "binding_bytes_valid": True,
        "binding_sha256": hashlib.sha256(payload).hexdigest(),
        "binding_bytes": len(payload),
        "verification": {field: False for field in FALSE_VERIFICATION_FIELDS},
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def accept_result_as_verified(*args: Any, **kwargs: Any) -> None:
    """Declared digests cannot be promoted into verified evidence here."""
    raise ScoutExternalResultBindingHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    """Result binding never creates execution authority."""
    raise ScoutExternalResultBindingHold(NEXT_GATE)
