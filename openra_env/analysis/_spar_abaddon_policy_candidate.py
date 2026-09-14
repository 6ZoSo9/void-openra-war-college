"""Fail-closed validation for Abaddon's reviewed policy-candidate evidence."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from ._spar_abaddon_policy_candidate_reviewed_identity import REVIEWED_IDENTITY
from ._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    SHA256,
    ContractError,
    _bool,
    _int,
    _jsonl,
    _obj,
    _pattern,
    _read,
    _str,
)

TRAJECTORY_KEY = "abaddon_policy_candidate_v1"
RUN_SCHEMA = "void.abaddon.policy-candidate-run-binding.v1"
ROUND_SCHEMA = "void.abaddon.policy-candidate-round-binding.v1"

IDENTITY_KEYS = (
    "wrapper_sha256",
    "legacy_runner_sha256",
    "abaddon_controller_sha256",
    "abaddon_refiner_sha256",
)
CANDIDATE_KEYS = (
    "candidate_file_sha256",
    "candidate_genome_sha256",
)


def _run_binding(header: dict[str, Any]) -> dict[str, Any] | None:
    raw = header.get(TRAJECTORY_KEY)
    if raw is None:
        return None
    raw = _obj(raw, f"run_header.{TRAJECTORY_KEY}")
    if _str(raw.get("schema"), "Abaddon candidate run schema") != RUN_SCHEMA:
        raise ContractError("Abaddon candidate run schema mismatch")

    _bool(raw.get("candidate_only"), "Abaddon candidate_only", True)
    _bool(raw.get("review_required"), "Abaddon review_required", True)
    _bool(raw.get("training_use_approved"), "Abaddon training_use_approved", False)
    _bool(raw.get("apollyon_policy_mutated"), "Abaddon apollyon_policy_mutated", False)
    _bool(raw.get("host_validation_unchanged"), "Abaddon host_validation_unchanged", True)
    _bool(
        raw.get("world_mutated_before_host_validation"),
        "Abaddon world_mutated_before_host_validation",
        False,
    )
    _bool(raw.get("training_performed"), "Abaddon training_performed", False)
    _bool(raw.get("weights_updated"), "Abaddon weights_updated", False)
    _bool(raw.get("automatic_corpus_admission"), "Abaddon automatic_corpus_admission", False)
    _bool(
        raw.get("automatic_abaddon_policy_promotion"),
        "Abaddon automatic_abaddon_policy_promotion",
        False,
    )

    if _str(raw.get("candidate_general"), "candidate_general") != "abaddon":
        raise ContractError("Abaddon candidate_general mismatch")
    if _str(raw.get("opponent_general"), "opponent_general") != "apollyon":
        raise ContractError("Abaddon opponent_general mismatch")
    if _str(raw.get("host_validation_path"), "host_validation_path") != "legacy_base.decision_to_commands":
        raise ContractError("Abaddon host validation path mismatch")

    candidate = {
        key: _pattern(raw.get(key), f"Abaddon {key}", SHA256)
        for key in CANDIDATE_KEYS
    }
    identity = {
        key: _pattern(raw.get(key), f"Abaddon {key}", SHA256)
        for key in IDENTITY_KEYS
    }
    for key, expected in REVIEWED_IDENTITY.items():
        if identity.get(key) != expected:
            raise ContractError(f"Abaddon reviewed producer identity mismatch: {key}")

    return {
        "schema": RUN_SCHEMA,
        "candidate_only": True,
        "review_required": True,
        "training_use_approved": False,
        "candidate_general": "abaddon",
        "opponent_general": "apollyon",
        **candidate,
        **identity,
        "reviewed_wrapper_identity_verified": True,
        "apollyon_policy_mutated": False,
        "host_validation_path": "legacy_base.decision_to_commands",
        "host_validation_unchanged": True,
        "world_mutated_before_host_validation": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_abaddon_policy_promotion": False,
    }


def _round_binding(
    row: dict[str, Any],
    *,
    round_number: int,
    run: dict[str, Any] | None,
) -> bool | None:
    raw = row.get(TRAJECTORY_KEY)
    if run is None:
        if raw is not None:
            raise ContractError("Abaddon candidate round evidence present without run binding")
        return None
    if raw is None:
        raise ContractError(f"round {round_number} missing Abaddon candidate evidence")

    raw = _obj(raw, f"round {round_number} Abaddon candidate evidence")
    if _str(raw.get("schema"), "Abaddon round schema") != ROUND_SCHEMA:
        raise ContractError("Abaddon candidate round schema mismatch")
    if _int(raw.get("round"), "Abaddon candidate round", 1) != round_number:
        raise ContractError("Abaddon candidate round number mismatch")

    for key in (*CANDIDATE_KEYS, *IDENTITY_KEYS):
        value = _pattern(raw.get(key), f"round {round_number} {key}", SHA256)
        if value != run[key]:
            raise ContractError(f"round {round_number} Abaddon candidate binding mismatch: {key}")

    _bool(raw.get("host_validation_unchanged"), "Abaddon round host_validation_unchanged", True)
    _bool(
        raw.get("world_mutated_before_host_validation"),
        "Abaddon round world_mutated_before_host_validation",
        False,
    )

    accepted = _bool(raw.get("legacy_host_accepted"), "Abaddon round legacy_host_accepted")
    abaddon = _obj(row.get("abaddon"), "Abaddon trajectory decision")
    host_accepted = _bool(abaddon.get("accepted"), "Abaddon trajectory accepted")
    if accepted is not host_accepted:
        raise ContractError(f"round {round_number} Abaddon host acceptance binding mismatch")

    expected_reason = str(abaddon.get("host_reason", ""))
    reason = _str(raw.get("legacy_host_reason"), "Abaddon round legacy_host_reason", empty=True)
    if reason != expected_reason:
        raise ContractError(f"round {round_number} Abaddon host reason binding mismatch")
    return accepted


def validate_abaddon_policy_candidate_evidence(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str,
) -> dict[str, Any]:
    if SHA256.fullmatch(expected_trajectory_sha256) is None:
        raise ContractError("expected trajectory SHA-256 malformed for Abaddon candidate validation")

    raw = _read(trajectory_path, "trajectory", MAX_TRAJECTORY_BYTES)
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_trajectory_sha256:
        raise ContractError("trajectory changed between base and Abaddon candidate validation")

    rows = _jsonl(raw)
    if not rows:
        raise ContractError("trajectory is empty during Abaddon candidate validation")

    run = _run_binding(rows[0])
    rounds = 0
    accepted_count = 0
    rejected_count = 0

    for row in rows[1:]:
        event = row.get("event")
        if event != "joint_decision":
            if row.get(TRAJECTORY_KEY) is not None:
                raise ContractError("Abaddon candidate evidence is present on a non-decision row")
            continue

        rounds += 1
        row_round = _int(row.get("round"), "Abaddon trajectory round", 1)
        if row_round != rounds:
            raise ContractError(f"Abaddon candidate expected decision round {rounds}, got {row_round}")
        accepted = _round_binding(row, round_number=rounds, run=run)
        if accepted is True:
            accepted_count += 1
        elif accepted is False:
            rejected_count += 1

    if run is None:
        return {
            "present": False,
            "rounds_verified": 0,
            "host_accept_count": 0,
            "host_rejection_count": 0,
        }
    if rounds == 0:
        raise ContractError("Abaddon candidate run binding has no joint_decision rows")

    return {
        "present": True,
        **run,
        "rounds_verified": rounds,
        "all_round_receipts_verified": True,
        "host_acceptance_bound": True,
        "host_validation_unchanged": True,
        "host_accept_count": accepted_count,
        "host_rejection_count": rejected_count,
    }
