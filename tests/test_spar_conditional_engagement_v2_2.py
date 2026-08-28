from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis._spar_conditional_v2_2 import (
    ACCEPTED_SCHEMA,
    COMPLIANCE_SCHEMA,
    DECISION_SCHEMA,
    PREPARED_SCHEMA,
    RUN_SCHEMA,
    validate_conditional_v22_evidence,
)
from openra_env.analysis._spar_conditional_v2_2_reviewed_identity import (
    PARENT_V21_CANDIDATE_SHA256,
    REVIEWED_V22_IDENTITY,
)
from openra_env.analysis._spar_contract import ContractError

CANDIDATE_SHA = REVIEWED_V22_IDENTITY["candidate_sha256"]


def run_header(*, with_v22: bool = True) -> dict:
    row = {"event": "run_header", "run_id": "fixture"}
    if with_v22:
        row["conditional_engagement_v2_2"] = {
            "schema": RUN_SCHEMA,
            "candidate_only": True,
            **REVIEWED_V22_IDENTITY,
            "parent_v2_1_candidate_sha256": PARENT_V21_CANDIDATE_SHA256,
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
    offered: list[str] | None = None,
    with_v22: bool = True,
) -> dict:
    offered = [tool] if offered is None else offered
    row = {
        "event": "joint_decision",
        "round": round_no,
        "apollyon": {
            "tool": tool,
            "tool_contract": {"offered_tool_names": offered},
        },
    }
    if not with_v22:
        return row
    reasons = ["no_emergency_condition_proven"]
    if mode == "FORCE_CONVERSION":
        reasons = [
            "rebuilt_force_without_contact",
            "repeated_blind_attack_move_without_military_progress",
        ]
    alternatives = [name for name in offered if name != "attack_move"] if mode == "FORCE_CONVERSION" else []
    discouraged = mode == "FORCE_CONVERSION" and bool(alternatives)
    preferred = "move_units" if mode == "FORCE_CONVERSION" and "move_units" in offered else None
    coaching = (
        "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_2\n"
        f"MODE={mode}\n"
        "CURRENT_ALLOWED_TOOL_NAMES=" + ",".join(offered) + "\n"
        "BOUNDARY=Use exactly one function; do not infer hidden state or invent actor IDs.\n"
        "TOOL_SURFACE_UNCHANGED=true"
    )
    if discouraged:
        coaching += "\nFORCE_CONVERSION_ACTION_RULE=Do not choose attack_move this round; choose an offered alternative."
    if preferred:
        coaching += "\nPREFERRED_OFFERED_ALTERNATIVE=move_units"
    row["conditional_engagement_v2_2"] = {
        "prepared": {
            "schema": PREPARED_SCHEMA,
            "round": round_no,
            "candidate_sha256": CANDIDATE_SHA,
            "current_allowed_tool_names": offered,
            "decision": {
                "schema": DECISION_SCHEMA,
                "mode": mode,
                "reasons": reasons,
                "evidence": {"round": round_no},
                "instruction": "reviewed candidate instruction",
                "candidate_sha256": CANDIDATE_SHA,
                "runtime_seed_branching": False,
            },
            "coaching": coaching,
            "action_compliance": {
                "schema": COMPLIANCE_SCHEMA,
                "mode": mode,
                "tool_surface_unchanged": True,
                "attack_move_discouraged": discouraged,
                "preferred_offered_alternative": preferred,
                "non_attack_move_offered_names": alternatives,
            },
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
            "history_size": min(round_no, 6),
        },
    }
    return row


def write_rows(path: Path, rows: list[dict]) -> str:
    raw = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    path.write_text(raw, encoding="utf-8")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def validate(path: Path, rows: list[dict]) -> dict:
    digest = write_rows(path, rows)
    return validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_valid_v22_binds_compliance_and_counts_followed_alternative(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header()]
    rows.extend(joint_decision(round_no) for round_no in (1, 2))
    rows.append(joint_decision(3, mode="FORCE_CONVERSION", tool="move_units", offered=["attack_move", "move_units", "build_unit"]))
    report = validate(path, rows)
    assert report["present"] is True
    assert report["reviewed_identity_verified"] is True
    assert report["rounds_verified"] == 3
    assert report["mode_counts"]["FORCE_CONVERSION"] == 1
    assert report["action_compliance_bound"] is True
    assert report["attack_move_discouraged_rounds"] == 1
    assert report["followed_non_attack_move_rounds"] == 1
    assert report["ignored_attack_move_discouragement_rounds"] == 0
    assert report["preferred_move_units_offered_rounds"] == 1
    assert report["preferred_move_units_selected_rounds"] == 1


def test_advisory_only_attack_move_is_recorded_as_ignored_not_rejected(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    report = validate(path, [
        run_header(),
        joint_decision(1),
        joint_decision(2),
        joint_decision(3, mode="FORCE_CONVERSION", tool="attack_move", offered=["attack_move", "move_units"]),
    ])
    assert report["attack_move_discouraged_rounds"] == 1
    assert report["followed_non_attack_move_rounds"] == 0
    assert report["ignored_attack_move_discouragement_rounds"] == 1


def test_baseline_without_v22_remains_valid_optional_absence(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    report = validate(path, [run_header(with_v22=False), joint_decision(1, with_v22=False)])
    assert report == {"present": False, "rounds_verified": 0, "mode_counts": {}}


def test_run_binding_requires_round_evidence_and_stray_evidence_is_rejected(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [run_header(), joint_decision(1, with_v22=False)]
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="missing V2.2 evidence"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)

    rows = [run_header(with_v22=False), joint_decision(1)]
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="without V2.2 run binding"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_five_identity_forgery_and_parent_drift_fail_closed(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    header = run_header()
    header["conditional_engagement_v2_2"].update({
        "source_commit": "1" * 40,
        "candidate_sha256": "2" * 64,
        "policy_sha256": "3" * 64,
        "session_sha256": "4" * 64,
        "wrapper_sha256": "5" * 64,
    })
    row = joint_decision(1)
    evidence = row["conditional_engagement_v2_2"]
    evidence["prepared"]["candidate_sha256"] = "2" * 64
    evidence["prepared"]["decision"]["candidate_sha256"] = "2" * 64
    evidence["accepted"]["candidate_sha256"] = "2" * 64
    digest = write_rows(path, [header, row])
    with pytest.raises(ContractError, match="reviewed identity mismatch"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)

    header = run_header()
    header["conditional_engagement_v2_2"]["parent_v2_1_candidate_sha256"] = "f" * 64
    digest = write_rows(path, [header, joint_decision(1)])
    with pytest.raises(ContractError, match="parent V2.1 candidate mismatch"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_tool_surface_and_compliance_alternatives_are_exactly_bound(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1, mode="FORCE_CONVERSION", tool="move_units", offered=["attack_move", "move_units"])
    row["conditional_engagement_v2_2"]["prepared"]["current_allowed_tool_names"] = ["attack_move", "move_units", "build_unit"]
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="tool surface does not match"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)

    row = joint_decision(1, mode="FORCE_CONVERSION", tool="move_units", offered=["attack_move", "move_units"])
    row["conditional_engagement_v2_2"]["prepared"]["action_compliance"]["non_attack_move_offered_names"] = ["move_units", "build_unit"]
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="alternatives mismatch"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_discouragement_and_preferred_move_units_must_follow_offered_surface(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1, mode="FORCE_CONVERSION", tool="move_units", offered=["attack_move", "move_units"])
    row["conditional_engagement_v2_2"]["prepared"]["action_compliance"]["attack_move_discouraged"] = False
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="attack_move_discouraged"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)

    row = joint_decision(1, mode="FORCE_CONVERSION", tool="advance", offered=["attack_move", "advance"])
    row["conditional_engagement_v2_2"]["prepared"]["action_compliance"]["preferred_offered_alternative"] = "move_units"
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="preferred alternative is present"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_coaching_action_rule_and_exact_surface_are_mandatory(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1, mode="FORCE_CONVERSION", tool="move_units", offered=["attack_move", "move_units"])
    prepared = row["conditional_engagement_v2_2"]["prepared"]
    prepared["coaching"] = prepared["coaching"].replace("Do not choose attack_move this round", "choose deliberately")
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="action rule is missing"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)

    row = joint_decision(1)
    prepared = row["conditional_engagement_v2_2"]["prepared"]
    prepared["coaching"] = prepared["coaching"].replace("CURRENT_ALLOWED_TOOL_NAMES=advance", "CURRENT_ALLOWED_TOOL_NAMES=move_units")
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="exact offered tool surface"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_accepted_tool_and_history_window_evolution_fail_closed(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    row = joint_decision(1, tool="advance", offered=["advance", "move_units"])
    row["conditional_engagement_v2_2"]["accepted"]["selected_tool"] = "move_units"
    digest = write_rows(path, [run_header(), row])
    with pytest.raises(ContractError, match="does not match Apollyon trajectory tool"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)

    rows = [run_header()] + [joint_decision(i) for i in range(1, 8)]
    rows[-1]["conditional_engagement_v2_2"]["accepted"]["history_size"] = 5
    digest = write_rows(path, rows)
    with pytest.raises(ContractError, match="bounded-history evolution"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256=digest)


def test_second_pass_digest_change_fails_closed(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    write_rows(path, [run_header(), joint_decision(1)])
    with pytest.raises(ContractError, match="changed between base and V2.2 validation"):
        validate_conditional_v22_evidence(path, expected_trajectory_sha256="0" * 64)
