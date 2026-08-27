from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis._spar_conditional_v2_1 import (
    ACCEPTED_SCHEMA,
    DECISION_SCHEMA,
    PREPARED_SCHEMA,
    RUN_SCHEMA,
    validate_conditional_v21_evidence,
)
from openra_env.analysis._spar_conditional_v2_1_reviewed_identity import (
    PARENT_V2_CANDIDATE_SHA256,
    REVIEWED_V21_IDENTITY,
)
from openra_env.analysis._spar_contract import ContractError

CANDIDATE_SHA = REVIEWED_V21_IDENTITY["candidate_sha256"]


def run_header(*, with_v21: bool = True) -> dict:
    row = {"event": "run_header", "run_id": "fixture"}
    if with_v21:
        row["conditional_engagement_v2_1"] = {
            "schema": RUN_SCHEMA,
            "candidate_only": True,
            **REVIEWED_V21_IDENTITY,
            "parent_v2_candidate_sha256": PARENT_V2_CANDIDATE_SHA256,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
            "automatic_corpus_admission": False,
        }
    return row


def joint_decision(
    round_no: int,
    *,
    mode: str = "BALANCED_SEARCH",
    tool: str = "advance",
    with_v21: bool = True,
) -> dict:
    row = {
        "event": "joint_decision",
        "round": round_no,
        "apollyon": {
            "tool": tool,
            "tool_contract": {"offered_tool_names": [tool]},
        },
    }
    if not with_v21:
        return row
    reasons = ["no_emergency_condition_proven"]
    if mode == "FORCE_CONVERSION":
        reasons = [
            "rebuilt_force_without_contact",
            "repeated_blind_attack_move_without_military_progress",
        ]
    row["conditional_engagement_v2_1"] = {
        "prepared": {
            "schema": PREPARED_SCHEMA,
            "round": round_no,
            "candidate_sha256": CANDIDATE_SHA,
            "current_allowed_tool_names": [tool],
            "decision": {
                "schema": DECISION_SCHEMA,
                "mode": mode,
                "reasons": reasons,
                "evidence": {"round": round_no},
                "instruction": "convert rebuilt force into productive observed contact",
                "candidate_sha256": CANDIDATE_SHA,
                "runtime_seed_branching": False,
            },
            "coaching": (
                "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_1\n"
                f"MODE={mode}\nCURRENT_ALLOWED_TOOL_NAMES\n"
                "do not infer hidden state"
            ),
            "history_committed": False,
        },
        "accepted": {
            "schema": ACCEPTED_SCHEMA,
            "round": round_no,
            "candidate_sha256": CANDIDATE_SHA,
            "mode": mode,
            "reasons": reasons,
            "selected_tool": tool,
            "function_was_offered": True,
            "history_size": min(round_no, 5),
        },
    }
    return row


def write_rows(path: Path, rows: list[dict]) -> str:
    raw = "".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    )
    path.write_text(raw, encoding="utf-8")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def validate(path: Path, rows: list[dict]) -> dict:
    digest = write_rows(path, rows)
    return validate_conditional_v21_evidence(
        path,
        expected_trajectory_sha256=digest,
    )


def test_valid_v21_evidence_binds_every_round_and_counts_force_conversion(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    report = validate(path, [
        run_header(),
        joint_decision(1),
        joint_decision(2, mode="FORCE_CONVERSION", tool="move_units"),
        joint_decision(3, mode="MEASURED_CONTACT", tool="attack_target"),
    ])
    assert report["present"] is True
    assert report["reviewed_identity_verified"] is True
    assert report["rounds_verified"] == 3
    assert report["mode_counts"]["FORCE_CONVERSION"] == 1
    assert report["all_round_receipts_verified"] is True
    assert report["tool_surface_bound"] is True
    assert report["accepted_tool_bound"] is True


def test_baseline_without_v21_remains_valid_optional_absence(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    report = validate(path, [run_header(with_v21=False), joint_decision(1, with_v21=False)])
    assert report == {"present": False, "rounds_verified": 0, "mode_counts": {}}


def test_run_binding_requires_round_evidence(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header(), joint_decision(1, with_v21=False)]
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="missing V2.1 evidence"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)


def test_stray_round_evidence_without_run_binding_is_rejected(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header(with_v21=False), joint_decision(1)]
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="without V2.1 run binding"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)


def test_prepared_tool_surface_must_equal_host_contract(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1)
    row["conditional_engagement_v2_1"]["prepared"]["current_allowed_tool_names"] = ["advance", "move_units"]
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="tool surface does not match"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)


def test_accepted_tool_must_match_trajectory_tool_and_be_offered(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1)
    row["conditional_engagement_v2_1"]["accepted"]["selected_tool"] = "move_units"
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="does not match Apollyon trajectory tool"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)


def test_candidate_mode_and_coaching_identity_drift_fail_closed(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1)
    row["conditional_engagement_v2_1"]["prepared"]["candidate_sha256"] = "9" * 64
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="prepared candidate SHA mismatch"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)

    row = joint_decision(1)
    row["conditional_engagement_v2_1"]["prepared"]["coaching"] = (
        "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_1\nMODE=FORCE_CONVERSION\n"
        "CURRENT_ALLOWED_TOOL_NAMES\ndo not infer hidden state"
    )
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="does not bind the recorded mode"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)


def test_all_five_self_attested_identities_changed_together_still_hold(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    header = run_header()
    binding = header["conditional_engagement_v2_1"]
    binding.update({
        "source_commit": "1" * 40,
        "candidate_sha256": "2" * 64,
        "policy_sha256": "3" * 64,
        "session_sha256": "4" * 64,
        "wrapper_sha256": "5" * 64,
    })
    row = joint_decision(1)
    evidence = row["conditional_engagement_v2_1"]
    evidence["prepared"]["candidate_sha256"] = "2" * 64
    evidence["prepared"]["decision"]["candidate_sha256"] = "2" * 64
    evidence["accepted"]["candidate_sha256"] = "2" * 64
    digest = write_rows(path, [header, row])
    with pytest.raises(ContractError, match="reviewed identity mismatch"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)


def test_parent_v2_candidate_and_second_pass_digest_fail_closed(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    header = run_header()
    header["conditional_engagement_v2_1"]["parent_v2_candidate_sha256"] = "f" * 64
    digest = write_rows(path, [header, joint_decision(1)])
    with pytest.raises(ContractError, match="parent V2 candidate mismatch"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256=digest)

    write_rows(path, [run_header(), joint_decision(1)])
    with pytest.raises(ContractError, match="changed between base and V2.1 validation"):
        validate_conditional_v21_evidence(path, expected_trajectory_sha256="0" * 64)
