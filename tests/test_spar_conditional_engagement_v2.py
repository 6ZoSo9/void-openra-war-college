from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis._spar_conditional_v2 import (
    ACCEPTED_SCHEMA,
    DECISION_SCHEMA,
    PREPARED_SCHEMA,
    RUN_SCHEMA,
    validate_conditional_v2_evidence,
)
from openra_env.analysis._spar_contract import ContractError

CANDIDATE_SHA = "2" * 64


def run_header(*, with_v2: bool = True) -> dict:
    row = {"event": "run_header", "run_id": "fixture"}
    if with_v2:
        row["conditional_engagement_v2"] = {
            "schema": RUN_SCHEMA,
            "candidate_only": True,
            "source_commit": "1" * 40,
            "candidate_sha256": CANDIDATE_SHA,
            "policy_sha256": "3" * 64,
            "session_sha256": "4" * 64,
            "wrapper_sha256": "5" * 64,
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
    with_v2: bool = True,
) -> dict:
    row = {
        "event": "joint_decision",
        "round": round_no,
        "apollyon": {
            "tool": tool,
            "tool_contract": {"offered_tool_names": [tool]},
        },
    }
    if not with_v2:
        return row
    reasons = ["no_emergency_condition_proven"]
    row["conditional_engagement_v2"] = {
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
                "instruction": "preserve options while searching for measured contact",
                "candidate_sha256": CANDIDATE_SHA,
                "runtime_seed_branching": False,
            },
            "coaching": (
                "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2\n"
                f"MODE={mode}\n"
                "CURRENT_ALLOWED_TOOL_NAMES\n"
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
    return validate_conditional_v2_evidence(
        path,
        expected_trajectory_sha256=digest,
    )


def test_valid_v2_evidence_binds_every_round_and_counts_modes(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    report = validate(
        path,
        [
            run_header(),
            joint_decision(1, mode="BALANCED_SEARCH"),
            joint_decision(2, mode="CONTACT_RESPONSE", tool="attack_target"),
            joint_decision(3, mode="ATTRITION_BRAKE", tool="advance"),
        ],
    )
    assert report["present"] is True
    assert report["source_commit"] == "1" * 40
    assert report["candidate_sha256"] == CANDIDATE_SHA
    assert report["rounds_verified"] == 3
    assert report["all_round_receipts_verified"] is True
    assert report["tool_surface_bound"] is True
    assert report["accepted_tool_bound"] is True
    assert report["mode_counts"] == {
        "ATTRITION_BRAKE": 1,
        "BALANCED_SEARCH": 1,
        "CONTACT_RESPONSE": 1,
    }


def test_baseline_without_v2_evidence_remains_valid_optional_absence(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    report = validate(
        path,
        [run_header(with_v2=False), joint_decision(1, with_v2=False)],
    )
    assert report == {
        "present": False,
        "rounds_verified": 0,
        "mode_counts": {},
    }


def test_run_binding_requires_round_evidence(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header(), joint_decision(1, with_v2=False)]
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="missing V2 evidence"):
        validate_conditional_v2_evidence(path, expected_trajectory_sha256=digest)


def test_stray_round_evidence_without_run_binding_is_rejected(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header(with_v2=False), joint_decision(1)]
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="without V2 run binding"):
        validate_conditional_v2_evidence(path, expected_trajectory_sha256=digest)


def test_prepared_tool_surface_must_equal_host_contract(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1)
    row["conditional_engagement_v2"]["prepared"]["current_allowed_tool_names"] = [
        "advance",
        "attack_move",
    ]
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="tool surface does not match"):
        validate_conditional_v2_evidence(path, expected_trajectory_sha256=digest)


def test_accepted_tool_must_match_trajectory_tool_and_be_offered(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1)
    row["conditional_engagement_v2"]["accepted"]["selected_tool"] = "attack_move"
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="does not match Apollyon trajectory tool"):
        validate_conditional_v2_evidence(path, expected_trajectory_sha256=digest)


def test_candidate_mode_and_coaching_identity_drift_fail_closed(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"

    row = joint_decision(1)
    row["conditional_engagement_v2"]["prepared"]["candidate_sha256"] = "9" * 64
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="prepared candidate SHA mismatch"):
        validate_conditional_v2_evidence(path, expected_trajectory_sha256=digest)

    row = joint_decision(1)
    row["conditional_engagement_v2"]["prepared"]["coaching"] = (
        "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2\n"
        "MODE=CONTACT_RESPONSE\nCURRENT_ALLOWED_TOOL_NAMES\n"
        "do not infer hidden state"
    )
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="does not bind the recorded mode"):
        validate_conditional_v2_evidence(path, expected_trajectory_sha256=digest)


def test_second_pass_digest_must_match_base_analyzer_generation(tmp_path) -> None:
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header(), joint_decision(1)]
    write_rows(path, rows)
    with pytest.raises(ContractError, match="changed between base and V2 validation"):
        validate_conditional_v2_evidence(
            path,
            expected_trajectory_sha256="0" * 64,
        )
