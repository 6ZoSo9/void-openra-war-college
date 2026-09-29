"""Bind scout post-run state evidence to the exact observed source context.

The existing v1 post-run observer intentionally emits a small stable evidence
record. Its source-cleanliness observation is stronger than the serialized
record: the concrete backend checks a caller-admitted War College commit and the
frozen OpenRA commit, but v1 evidence does not carry those identities.

This module closes that provenance gap without changing the historical v1
schema. It composes the reviewed backend and v1 observer, then emits a second
canonical binding record that commits the exact backend inputs and the SHA-256
of the v1 evidence bytes.

Nothing runs on import. The contract helper is pure. The composite collector can
perform only whatever read-only probes the already-reviewed backend callbacks
perform; it adds no process, service, Docker, model, game, training, deployment,
VOID-chain, wallet, signing, transaction, or funds authority.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from openra_env.learning import abaddon_scout_post_run_backend_v1 as backend
from openra_env.learning import abaddon_scout_post_run_observer_v1 as observer


BINDING_SCHEMA = "void.abaddon.scout-post-run-provenance-binding.v1"
CONTRACT_SCHEMA = "void.abaddon.scout-post-run-provenance-bundle-contract.v1"
RECORD_KIND = "post_run_state_context_binding_not_final_acceptance"
MAX_BINDING_BYTES = 65536

BACKEND_PATH = "openra_env/learning/abaddon_scout_post_run_backend_v1.py"
BACKEND_GIT_BLOB = "f52dc74027f6243faa4d5a6cbe5da81a22bbf78e"
BACKEND_REVIEW_PATH = (
    "openra_env/learning/abaddon_scout_post_run_backend_source_binding_review_v1.py"
)
BACKEND_REVIEW_GIT_BLOB = "06b8ce51d6101e0d1ec0d39c6b6a057d91ae8974"
OBSERVER_PATH = "openra_env/learning/abaddon_scout_post_run_observer_v1.py"
OBSERVER_GIT_BLOB = "11dfa40a861e6772258178bbc32840c670e47f9f"
OBSERVER_CONTRACT_PATH = (
    "openra_env/learning/abaddon_scout_post_run_observer_contract_v1.py"
)
OBSERVER_CONTRACT_GIT_BLOB = observer.OBSERVER_CONTRACT_GIT_BLOB

NEXT_GATE = "SCOUT_POST_RUN_PROVENANCE_BINDING_SOURCE_REVIEW_REQUIRED"

FALSE_AUTHORITY_FIELDS = (
    "result_evidence_verified",
    "operator_authenticated",
    "scout_execution_authorized",
    "scout_execution_performed",
    "automatic_retry",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutPostRunProvenanceBundleHold(ValueError):
    """The supplied state evidence or provenance context is inconsistent."""


@dataclass(frozen=True)
class ScoutPostRunProvenanceBundle:
    state_evidence: bytes
    provenance_binding: bytes


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutPostRunProvenanceBundleHold(code)


def _is_hex(value: Any, length: int) -> bool:
    return (
        type(value) is str
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def _valid_experiment_id(value: Any) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= 128
        and value.startswith("abaddon-scout-")
        and "pair03" not in value
        and all(
            character in "abcdefghijklmnopqrstuvwxyz0123456789._-"
            for character in value
        )
    )


def _valid_container_name(value: Any) -> bool:
    if type(value) is not str or not value.startswith(backend.CONTAINER_PREFIX):
        return False
    suffix = value[len(backend.CONTAINER_PREFIX):]
    return bool(suffix) and suffix.isdigit() and int(suffix) > 0


def _validate_inputs(
    inputs: backend.ScoutPostRunBackendInputs,
) -> backend.ScoutPostRunBackendInputs:
    _require(
        isinstance(inputs, backend.ScoutPostRunBackendInputs),
        "SCOUT_PROVENANCE_INPUTS_REQUIRED",
    )
    _require(
        _valid_experiment_id(inputs.experiment_id),
        "SCOUT_PROVENANCE_EXPERIMENT_ID_INVALID",
    )
    _require(
        _is_hex(inputs.attempt_marker_sha256, 64),
        "SCOUT_PROVENANCE_ATTEMPT_SHA256_INVALID",
    )
    _require(
        _is_hex(inputs.accepted_war_college_commit, 40),
        "SCOUT_PROVENANCE_WAR_COLLEGE_COMMIT_INVALID",
    )
    _require(
        _valid_container_name(inputs.engine_container_name),
        "SCOUT_PROVENANCE_CONTAINER_NAME_INVALID",
    )
    _require(
        type(inputs.attempt_directory_identity) is tuple
        and len(inputs.attempt_directory_identity) == 2
        and all(
            type(value) is int and value >= 0
            for value in inputs.attempt_directory_identity
        ),
        "SCOUT_PROVENANCE_DIRECTORY_IDENTITY_INVALID",
    )
    marker_path = Path(inputs.attempt_marker_path)
    _require(marker_path.is_absolute(), "SCOUT_PROVENANCE_MARKER_PATH_NOT_ABSOLUTE")
    _require(
        marker_path.name == backend.attempt_guard.MARKER_NAME,
        "SCOUT_PROVENANCE_MARKER_NAME_DRIFT",
    )
    return inputs


def _canonical_json_record(raw: bytes) -> dict[str, Any]:
    _require(type(raw) is bytes, "SCOUT_PROVENANCE_STATE_BYTES_REQUIRED")
    _require(
        0 < len(raw) <= observer.MAX_EVIDENCE_BYTES,
        "SCOUT_PROVENANCE_STATE_BYTE_LIMIT",
    )
    try:
        decoded = raw.decode("ascii")
        record = json.loads(decoded)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ScoutPostRunProvenanceBundleHold(
            "SCOUT_PROVENANCE_STATE_JSON_INVALID"
        ) from None
    _require(type(record) is dict, "SCOUT_PROVENANCE_STATE_OBJECT_REQUIRED")
    canonical = (
        json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    _require(raw == canonical, "SCOUT_PROVENANCE_STATE_NONCANONICAL")
    return record


def _review_state_evidence(
    raw: bytes,
    *,
    inputs: backend.ScoutPostRunBackendInputs,
) -> dict[str, Any]:
    record = _canonical_json_record(raw)
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
        "SCOUT_PROVENANCE_STATE_FIELDS_DRIFT",
    )
    _require(
        record["schema"] == observer.EVIDENCE_SCHEMA,
        "SCOUT_PROVENANCE_STATE_SCHEMA_DRIFT",
    )
    _require(
        record["record_kind"] == "independent_post_run_state_declaration",
        "SCOUT_PROVENANCE_STATE_KIND_DRIFT",
    )
    _require(
        record["experiment_id"] == inputs.experiment_id,
        "SCOUT_PROVENANCE_STATE_EXPERIMENT_DRIFT",
    )
    _require(
        record["attempt_marker_sha256"] == inputs.attempt_marker_sha256,
        "SCOUT_PROVENANCE_STATE_ATTEMPT_DRIFT",
    )
    _require(
        record["observer_contract_git_blob"] == OBSERVER_CONTRACT_GIT_BLOB,
        "SCOUT_PROVENANCE_OBSERVER_CONTRACT_DRIFT",
    )

    observations = record["observations"]
    _require(
        type(observations) is dict
        and set(observations) == set(observer.REQUIRED_OBSERVATIONS),
        "SCOUT_PROVENANCE_OBSERVATION_FIELDS_DRIFT",
    )
    for field in observer.REQUIRED_OBSERVATIONS:
        _require(
            observations[field] is True,
            "SCOUT_PROVENANCE_OBSERVATION_REQUIRED:" + field,
        )

    claims = record["claims"]
    _require(
        type(claims) is dict and set(claims) == set(observer.FALSE_CLAIMS),
        "SCOUT_PROVENANCE_CLAIM_FIELDS_DRIFT",
    )
    for field in observer.FALSE_CLAIMS:
        _require(
            claims[field] is False,
            "SCOUT_PROVENANCE_FALSE_CLAIM_REQUIRED:" + field,
        )
    return record


def _digest_json(value: Any) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def build_scout_post_run_provenance_binding(
    *,
    inputs: backend.ScoutPostRunBackendInputs,
    state_evidence: bytes,
) -> bytes:
    """Bind canonical v1 evidence bytes to the exact backend observation inputs."""
    validated = _validate_inputs(inputs)
    state_record = _review_state_evidence(state_evidence, inputs=validated)

    marker_path_sha256 = hashlib.sha256(
        validated.attempt_marker_path.encode("utf-8")
    ).hexdigest()
    directory_identity_sha256 = _digest_json(
        {
            "st_dev": validated.attempt_directory_identity[0],
            "st_ino": validated.attempt_directory_identity[1],
        }
    )

    record = {
        "schema": BINDING_SCHEMA,
        "record_kind": RECORD_KIND,
        "experiment_id": validated.experiment_id,
        "attempt_marker_sha256": validated.attempt_marker_sha256,
        "attempt_marker_path_sha256": marker_path_sha256,
        "attempt_directory_identity_sha256": directory_identity_sha256,
        "engine_container_name": validated.engine_container_name,
        "accepted_war_college_commit": validated.accepted_war_college_commit,
        "expected_engine_commit": backend.EXPECTED_ENGINE_COMMIT,
        "post_run_state_sha256": hashlib.sha256(state_evidence).hexdigest(),
        "observer_contract_git_blob": state_record["observer_contract_git_blob"],
        "source_references": {
            BACKEND_PATH: BACKEND_GIT_BLOB,
            BACKEND_REVIEW_PATH: BACKEND_REVIEW_GIT_BLOB,
            OBSERVER_PATH: OBSERVER_GIT_BLOB,
            OBSERVER_CONTRACT_PATH: OBSERVER_CONTRACT_GIT_BLOB,
        },
        "binding_claims": {
            "accepted_war_college_commit_serialized": True,
            "expected_engine_commit_serialized": True,
            "engine_container_name_serialized": True,
            "attempt_marker_path_committed_without_raw_path": True,
            "attempt_directory_identity_committed_without_raw_identity": True,
            "post_run_state_bytes_sha256_bound": True,
            "historical_v1_state_schema_rewritten": False,
            "matching_binding_grants_final_result_acceptance": False,
        },
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }
    raw = (
        json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    _require(
        0 < len(raw) <= MAX_BINDING_BYTES,
        "SCOUT_PROVENANCE_BINDING_BYTE_LIMIT",
    )
    return raw


def collect_scout_post_run_provenance_bundle(
    inputs: backend.ScoutPostRunBackendInputs,
    *,
    observation_authorized: bool,
    read_authority_check: Callable[[], bool],
    run_command: backend.CommandRunner,
    file_backend: backend.FileBackend,
    lstat_path: backend.PathLstat,
    resolve_path: backend.PathResolver,
) -> ScoutPostRunProvenanceBundle:
    """Collect v1 state evidence once and bind the same exact observation inputs."""
    validated = _validate_inputs(inputs)
    state = backend.collect_bound_scout_post_run_evidence(
        validated,
        observation_authorized=observation_authorized,
        read_authority_check=read_authority_check,
        run_command=run_command,
        file_backend=file_backend,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
    )
    binding = build_scout_post_run_provenance_binding(
        inputs=validated,
        state_evidence=state,
    )
    return ScoutPostRunProvenanceBundle(
        state_evidence=state,
        provenance_binding=binding,
    )


def scout_post_run_provenance_bundle_contract() -> dict[str, Any]:
    """Describe the source-only provenance repair without touching the host."""
    return {
        "schema": CONTRACT_SCHEMA,
        "historical_state_schema": observer.EVIDENCE_SCHEMA,
        "binding_schema": BINDING_SCHEMA,
        "source_references": {
            BACKEND_PATH: BACKEND_GIT_BLOB,
            BACKEND_REVIEW_PATH: BACKEND_REVIEW_GIT_BLOB,
            OBSERVER_PATH: OBSERVER_GIT_BLOB,
            OBSERVER_CONTRACT_PATH: OBSERVER_CONTRACT_GIT_BLOB,
        },
        "accepted_war_college_commit_serialized": True,
        "expected_engine_commit_serialized": True,
        "engine_container_name_serialized": True,
        "attempt_marker_path_raw_publication": False,
        "attempt_directory_identity_raw_publication": False,
        "post_run_state_digest_bound": True,
        "backend_collection_and_binding_share_same_inputs": True,
        "automatic_host_backend_selection": False,
        "contract_call_performs_host_observation": False,
        "historical_v1_schema_rewritten": False,
        "final_result_acceptance": False,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunProvenanceBundleHold(
        "SCOUT_PROVENANCE_EXECUTION_AUTHORITY_UNAVAILABLE"
    )
