from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis._spar_abaddon_policy_candidate import (
    ROUND_SCHEMA,
    RUN_SCHEMA,
    TRAJECTORY_KEY,
    validate_abaddon_policy_candidate_evidence,
)
from openra_env.analysis._spar_abaddon_policy_candidate_reviewed_identity import (
    REVIEWED_IDENTITY,
)
from openra_env.analysis._spar_contract import ContractError
from tools import abaddon_policy_candidate_duel_wrapper as wrapper


def write_rows(tmp_path: Path, rows: list[dict]) -> tuple[Path, str]:
    path = tmp_path / "trajectory.jsonl"
    raw = "".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    ).encode()
    path.write_bytes(raw)
    return path, hashlib.sha256(raw).hexdigest()


def run_binding() -> dict:
    return {
        "schema": RUN_SCHEMA,
        "candidate_file_sha256": "1" * 64,
        "candidate_genome_sha256": "2" * 64,
        **REVIEWED_IDENTITY,
        "candidate_only": True,
        "review_required": True,
        "training_use_approved": False,
        "candidate_general": "abaddon",
        "opponent_general": "apollyon",
        "apollyon_policy_mutated": False,
        "host_validation_path": "legacy_base.decision_to_commands",
        "host_validation_unchanged": True,
        "world_mutated_before_host_validation": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_abaddon_policy_promotion": False,
    }


def round_binding(number: int, accepted: bool = True) -> dict:
    return {
        "schema": ROUND_SCHEMA,
        "candidate_file_sha256": "1" * 64,
        "candidate_genome_sha256": "2" * 64,
        **REVIEWED_IDENTITY,
        "round": number,
        "legacy_host_accepted": accepted,
        "legacy_host_reason": "" if accepted else "fixture reject",
        "host_validation_unchanged": True,
        "world_mutated_before_host_validation": False,
    }


def rows(*, candidate: bool = True, accepted: bool = True) -> list[dict]:
    header = {"event": "run_header"}
    if candidate:
        header[TRAJECTORY_KEY] = run_binding()
    decision = {
        "event": "joint_decision",
        "round": 1,
        "abaddon": {
            "accepted": accepted,
            "host_reason": "" if accepted else "fixture reject",
        },
    }
    if candidate:
        decision[TRAJECTORY_KEY] = round_binding(1, accepted)
    return [header, decision, {"event": "joint_result", "round": 1}]


def validate(tmp_path: Path, rows_value: list[dict]) -> dict:
    path, digest = write_rows(tmp_path, rows_value)
    return validate_abaddon_policy_candidate_evidence(
        path,
        expected_trajectory_sha256=digest,
    )


def test_reviewed_identity_binds_exact_wrapper_source():
    assert wrapper.wrapper_source_sha256() == REVIEWED_IDENTITY["wrapper_sha256"]
    assert wrapper.LEGACY_RUNNER_SHA256 == REVIEWED_IDENTITY["legacy_runner_sha256"]
    assert wrapper.ABADDON_CONTROLLER_SHA256 == REVIEWED_IDENTITY["abaddon_controller_sha256"]
    assert wrapper.ABADDON_REFINER_SHA256 == REVIEWED_IDENTITY["abaddon_refiner_sha256"]


def test_absent_candidate_evidence_remains_absent(tmp_path):
    result = validate(tmp_path, rows(candidate=False))
    assert result["present"] is False
    assert result["rounds_verified"] == 0


def test_valid_candidate_evidence_binds_all_rounds(tmp_path):
    result = validate(tmp_path, rows())
    assert result["present"] is True
    assert result["reviewed_wrapper_identity_verified"] is True
    assert result["all_round_receipts_verified"] is True
    assert result["host_acceptance_bound"] is True
    assert result["rounds_verified"] == 1
    assert result["host_accept_count"] == 1
    assert result["host_rejection_count"] == 0


def test_wrapper_identity_drift_is_rejected(tmp_path):
    value = rows()
    value[0][TRAJECTORY_KEY]["wrapper_sha256"] = "f" * 64
    with pytest.raises(ContractError, match="producer identity mismatch"):
        validate(tmp_path, value)


def test_candidate_binding_drift_is_rejected(tmp_path):
    value = rows()
    value[1][TRAJECTORY_KEY]["candidate_genome_sha256"] = "3" * 64
    with pytest.raises(ContractError, match="binding mismatch"):
        validate(tmp_path, value)


def test_host_acceptance_drift_is_rejected(tmp_path):
    value = rows()
    value[1][TRAJECTORY_KEY]["legacy_host_accepted"] = False
    value[1][TRAJECTORY_KEY]["legacy_host_reason"] = ""
    with pytest.raises(ContractError, match="host acceptance binding mismatch"):
        validate(tmp_path, value)


def test_missing_round_evidence_is_rejected(tmp_path):
    value = rows()
    del value[1][TRAJECTORY_KEY]
    with pytest.raises(ContractError, match="missing Abaddon candidate evidence"):
        validate(tmp_path, value)


def test_non_decision_candidate_evidence_is_rejected(tmp_path):
    value = rows()
    value[2][TRAJECTORY_KEY] = copy.deepcopy(round_binding(1))
    with pytest.raises(ContractError, match="non-decision"):
        validate(tmp_path, value)
