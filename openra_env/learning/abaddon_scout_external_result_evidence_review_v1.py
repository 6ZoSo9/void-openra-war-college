"""In-memory structural review for declared scout result evidence.

This module hashes caller-supplied bytes and binds them to the reviewed result
declaration. It performs no filesystem, process, network, model, engine, service,
or wallet action.

A structurally valid package is still not final evidence: the independent
post-run observer source is only declared here, not source-verified. Final result
acceptance therefore remains closed.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from openra_env.learning import abaddon_scout_external_result_binding_v1 as binding


REVIEW_SCHEMA = "void.abaddon.scout-external-result-evidence-structural-review.v1"
POST_RUN_SCHEMA = "void.abaddon.scout-post-run-state-evidence.v1"
NEXT_GATE = "SCOUT_POST_RUN_OBSERVER_IMPLEMENTATION_REVIEW_REQUIRED"

MAX_ATTEMPT_MARKER_BYTES = 4096
MAX_TRAJECTORY_BYTES = 16 * 1024 * 1024
MAX_RESULT_PAYLOAD_BYTES = 1024 * 1024
MAX_POST_RUN_STATE_BYTES = 65536

ATTEMPT_MARKER_SCHEMA = "void.abaddon.scout-external-attempt-consumption.v1"
ATTEMPT_RECORD_KIND = "attempt_consumed_not_execution_evidence"
REQUEST_SHA256 = "67582949d9cbb6815c59ba9c78e6ac40fc303080320b5d707ad2b9e64e9baf55"
LAUNCHER_CONTRACT_GIT_BLOB = "1f7ee7057c27946f488afe26501482ea4f4fc53d"
POST_RUN_OBSERVER_CONTRACT_GIT_BLOB = "fd71ac745c10349047d49f753ecfce1aab712648"

REQUIRED_POST_RUN_OBSERVATIONS = (
    "attempt_marker_present",
    "runtime_service_inactive",
    "engine_container_absent",
    "model_process_absent",
    "source_checkout_clean",
)

FALSE_POST_RUN_CLAIMS = (
    "callback_return_used_as_shutdown_proof",
    "historical_cleanup_print_used_as_shutdown_proof",
    "automatic_retry",
    "pair03_attempt_reused",
    "pair03_attempt_reset",
)

FALSE_AUTHORITY_FIELDS = (
    "post_run_observer_source_verified",
    "result_evidence_verified",
    "operator_authenticated",
    "scout_execution_authorized",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutExternalResultEvidenceReviewHold(ValueError):
    """The package is malformed, mismatched, or still lacks source provenance."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutExternalResultEvidenceReviewHold(code)


def _exact_bytes(value: Any, maximum: int, label: str) -> bytes:
    _require(type(value) is bytes, f"{label}_EXACT_BYTES_REQUIRED")
    _require(0 < len(value) <= maximum, f"{label}_BYTE_LIMIT")
    return value


def _canonical_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        decoded = raw.decode("ascii")
        value = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ScoutExternalResultEvidenceReviewHold(f"{label}_JSON_INVALID") from None
    _require(type(value) is dict, f"{label}_OBJECT_REQUIRED")
    canonical = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")
    _require(raw == canonical, f"{label}_NONCANONICAL")
    return value


def _hex40(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 40
        and all(character in "0123456789abcdef" for character in value)
    )


def _review_attempt_marker(
    raw: bytes,
    *,
    experiment_id: str,
) -> dict[str, Any]:
    record = _canonical_json(raw, "SCOUT_RESULT_ATTEMPT_MARKER")
    _require(
        set(record)
        == {
            "schema",
            "record_kind",
            "experiment_id",
            "request_sha256",
            "launcher_contract_git_blob",
            "single_use_scope",
            "pair03_attempt_reused",
            "pair03_attempt_reset",
            "scout_execution_authorized",
            "scout_execution_performed",
            "reusable_execution_permit",
            "automatic_retry",
            "training_authorized",
            "automatic_policy_promotion",
        },
        "SCOUT_RESULT_ATTEMPT_MARKER_FIELDS",
    )
    _require(record["schema"] == ATTEMPT_MARKER_SCHEMA, "SCOUT_RESULT_ATTEMPT_SCHEMA")
    _require(record["record_kind"] == ATTEMPT_RECORD_KIND, "SCOUT_RESULT_ATTEMPT_KIND")
    _require(record["experiment_id"] == experiment_id, "SCOUT_RESULT_ATTEMPT_EXPERIMENT")
    _require(record["request_sha256"] == REQUEST_SHA256, "SCOUT_RESULT_ATTEMPT_REQUEST")
    _require(
        record["launcher_contract_git_blob"] == LAUNCHER_CONTRACT_GIT_BLOB,
        "SCOUT_RESULT_ATTEMPT_LAUNCHER",
    )
    _require(record["single_use_scope"] is True, "SCOUT_RESULT_ATTEMPT_SINGLE_USE")
    for field in (
        "pair03_attempt_reused",
        "pair03_attempt_reset",
        "scout_execution_authorized",
        "scout_execution_performed",
        "reusable_execution_permit",
        "automatic_retry",
        "training_authorized",
        "automatic_policy_promotion",
    ):
        _require(record[field] is False, f"SCOUT_RESULT_ATTEMPT_FALSE_REQUIRED:{field}")
    return record


def _review_post_run_state(
    raw: bytes,
    *,
    experiment_id: str,
    attempt_marker_sha256: str,
) -> dict[str, Any]:
    record = _canonical_json(raw, "SCOUT_RESULT_POST_RUN")
    _require(
        set(record)
        == {
            "schema",
            "record_kind",
            "experiment_id",
            "attempt_marker_sha256",
            "observer_contract_git_blob",
            "observations",
            "claims",
        },
        "SCOUT_RESULT_POST_RUN_FIELDS",
    )
    _require(record["schema"] == POST_RUN_SCHEMA, "SCOUT_RESULT_POST_RUN_SCHEMA")
    _require(
        record["record_kind"] == "independent_post_run_state_declaration",
        "SCOUT_RESULT_POST_RUN_KIND",
    )
    _require(record["experiment_id"] == experiment_id, "SCOUT_RESULT_POST_RUN_EXPERIMENT")
    _require(
        record["attempt_marker_sha256"] == attempt_marker_sha256,
        "SCOUT_RESULT_POST_RUN_ATTEMPT_DIGEST",
    )
    _require(
        record["observer_contract_git_blob"] == POST_RUN_OBSERVER_CONTRACT_GIT_BLOB,
        "SCOUT_RESULT_POST_RUN_OBSERVER_CONTRACT_IDENTITY",
    )

    observations = record["observations"]
    _require(
        type(observations) is dict
        and set(observations) == set(REQUIRED_POST_RUN_OBSERVATIONS),
        "SCOUT_RESULT_POST_RUN_OBSERVATION_FIELDS",
    )
    for field in REQUIRED_POST_RUN_OBSERVATIONS:
        _require(
            observations[field] is True,
            f"SCOUT_RESULT_POST_RUN_OBSERVATION_REQUIRED:{field}",
        )

    claims = record["claims"]
    _require(
        type(claims) is dict and set(claims) == set(FALSE_POST_RUN_CLAIMS),
        "SCOUT_RESULT_POST_RUN_CLAIM_FIELDS",
    )
    for field in FALSE_POST_RUN_CLAIMS:
        _require(
            claims[field] is False,
            f"SCOUT_RESULT_POST_RUN_FALSE_REQUIRED:{field}",
        )
    return record


def review_scout_result_evidence(
    *,
    binding_payload: bytes,
    experiment_id: str,
    attempt_marker_bytes: bytes,
    trajectory_bytes: bytes,
    result_payload_bytes: bytes,
    post_run_state_bytes: bytes,
) -> dict[str, Any]:
    """Structurally bind supplied bytes; do not accept them as final evidence."""
    marker = _exact_bytes(
        attempt_marker_bytes,
        MAX_ATTEMPT_MARKER_BYTES,
        "SCOUT_RESULT_ATTEMPT_MARKER",
    )
    trajectory = _exact_bytes(
        trajectory_bytes,
        MAX_TRAJECTORY_BYTES,
        "SCOUT_RESULT_TRAJECTORY",
    )
    result_payload = _exact_bytes(
        result_payload_bytes,
        MAX_RESULT_PAYLOAD_BYTES,
        "SCOUT_RESULT_PAYLOAD",
    )
    post_run = _exact_bytes(
        post_run_state_bytes,
        MAX_POST_RUN_STATE_BYTES,
        "SCOUT_RESULT_POST_RUN",
    )

    marker_sha256 = hashlib.sha256(marker).hexdigest()
    trajectory_sha256 = hashlib.sha256(trajectory).hexdigest()
    result_payload_sha256 = hashlib.sha256(result_payload).hexdigest()
    post_run_sha256 = hashlib.sha256(post_run).hexdigest()

    _review_attempt_marker(marker, experiment_id=experiment_id)
    post_run_record = _review_post_run_state(
        post_run,
        experiment_id=experiment_id,
        attempt_marker_sha256=marker_sha256,
    )

    binding_validation = binding.validate_scout_result_binding(
        binding_payload,
        experiment_id=experiment_id,
        attempt_marker_sha256=marker_sha256,
        trajectory_sha256=trajectory_sha256,
        result_payload_sha256=result_payload_sha256,
        post_run_state_sha256=post_run_sha256,
    )

    return {
        "schema": REVIEW_SCHEMA,
        "experiment_id": experiment_id,
        "binding_sha256": binding_validation["binding_sha256"],
        "attempt_marker_sha256": marker_sha256,
        "trajectory_sha256": trajectory_sha256,
        "result_payload_sha256": result_payload_sha256,
        "post_run_state_sha256": post_run_sha256,
        "post_run_observer_contract_git_blob": post_run_record["observer_contract_git_blob"],
        "post_run_observer_contract_verified": True,
        "binding_bytes_verified": True,
        "attempt_marker_structure_verified": True,
        "trajectory_digest_verified": True,
        "result_payload_digest_verified": True,
        "post_run_state_structure_verified": True,
        "post_run_observer_implementation_verified": False,
        "result_evidence_verified": False,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def accept_result_as_verified(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalResultEvidenceReviewHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalResultEvidenceReviewHold(NEXT_GATE)
