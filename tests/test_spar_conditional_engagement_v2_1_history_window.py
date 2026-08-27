from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from openra_env.analysis._spar_conditional_v2_1 import (
    ACCEPTED_SCHEMA,
    DECISION_SCHEMA,
    PREPARED_SCHEMA,
    REVIEWED_V21_HISTORY_WINDOW_ROUNDS,
    RUN_SCHEMA,
    validate_conditional_v21_evidence,
)
from openra_env.analysis._spar_conditional_v2_1_reviewed_identity import (
    PARENT_V2_CANDIDATE_SHA256,
    REVIEWED_V21_IDENTITY,
)
from openra_env.analysis._spar_contract import ContractError
from openra_env.coaching.conditional_engagement_v2_1 import (
    candidate_sha256,
    validate_candidate,
)

CANDIDATE_SHA = REVIEWED_V21_IDENTITY["candidate_sha256"]


def _run_header() -> dict:
    return {
        "event": "run_header",
        "run_id": "history-window-fixture",
        "conditional_engagement_v2_1": {
            "schema": RUN_SCHEMA,
            "candidate_only": True,
            **REVIEWED_V21_IDENTITY,
            "parent_v2_candidate_sha256": PARENT_V2_CANDIDATE_SHA256,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
            "automatic_corpus_admission": False,
        },
    }


def _joint_decision(round_no: int, *, history_size: int) -> dict:
    tool = "attack_move"
    mode = "BALANCED_SEARCH"
    reasons = ["no_emergency_condition_proven"]
    return {
        "event": "joint_decision",
        "round": round_no,
        "apollyon": {
            "tool": tool,
            "tool_contract": {"offered_tool_names": [tool]},
        },
        "conditional_engagement_v2_1": {
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
                    "instruction": "bounded history test",
                    "candidate_sha256": CANDIDATE_SHA,
                    "runtime_seed_branching": False,
                },
                "coaching": (
                    "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_1\n"
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
                "history_size": history_size,
            },
        },
    }


def _write(path: Path, rows: list[dict]) -> str:
    raw = "".join(
        json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    )
    path.write_text(raw, encoding="utf-8")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _validate(path: Path, rows: list[dict]) -> dict:
    digest = _write(path, rows)
    return validate_conditional_v21_evidence(
        path,
        expected_trajectory_sha256=digest,
    )


def test_reviewed_candidate_and_verifier_agree_on_six_round_window():
    fixture = Path("fixtures/training/conditional_engagement_candidate_v2_1.json")
    candidate = json.loads(fixture.read_text(encoding="utf-8"))
    validate_candidate(candidate)
    assert candidate_sha256(candidate) == CANDIDATE_SHA
    assert candidate["thresholds"]["history_window_rounds"] == 6
    assert REVIEWED_V21_HISTORY_WINDOW_ROUNDS == 6


def test_history_receipts_grow_to_six_then_remain_bounded(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [_run_header()]
    rows.extend(
        _joint_decision(
            round_no,
            history_size=min(round_no, REVIEWED_V21_HISTORY_WINDOW_ROUNDS),
        )
        for round_no in range(1, 8)
    )
    report = _validate(path, rows)
    assert report["present"] is True
    assert report["rounds_verified"] == 7
    assert report["all_round_receipts_verified"] is True


def test_round_six_cannot_claim_legacy_five_round_history(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [_run_header()]
    rows.extend(
        _joint_decision(round_no, history_size=min(round_no, 6))
        for round_no in range(1, 6)
    )
    rows.append(_joint_decision(6, history_size=5))
    with pytest.raises(
        ContractError,
        match="history_size does not match reviewed bounded-history evolution",
    ):
        _validate(path, rows)


def test_history_receipt_cannot_exceed_reviewed_window(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [_run_header()]
    rows.extend(
        _joint_decision(round_no, history_size=min(round_no, 6))
        for round_no in range(1, 7)
    )
    rows.append(_joint_decision(7, history_size=7))
    with pytest.raises(ContractError, match="history_size must be <= 6"):
        _validate(path, rows)


def test_history_receipt_cannot_shrink_after_window_is_full(tmp_path):
    path = tmp_path / "trajectory.jsonl"
    rows = [_run_header()]
    rows.extend(
        _joint_decision(round_no, history_size=min(round_no, 6))
        for round_no in range(1, 7)
    )
    rows.append(_joint_decision(7, history_size=5))
    with pytest.raises(
        ContractError,
        match="history_size does not match reviewed bounded-history evolution",
    ):
        _validate(path, rows)
