from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_PROPOSAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_execution_adapter_generation2.py"
)
SOURCE = (
    LOCAL_PROPOSAL_SOURCE
    if LOCAL_PROPOSAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/abaddon_policy_campaign_execution_adapter_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "f5f8f0fca4c3ee8729ab6e7445251fb0f108aea66dc8e695319e9a0692019b51"

FORBIDDEN_IMPORT_ROOTS = {
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "httpx",
    "asyncio",
    "multiprocessing",
    "ctypes",
}
FORBIDDEN_CALL_NAMES = {
    "exec",
    "eval",
    "compile",
    "__import__",
    "os.system",
    "os.popen",
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
}


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")



def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_execution_adapter_contract",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _record(m, *, pair_slot=1, arm="baseline", status="completed"):
    desc = m.execution_descriptor(pair_slot=pair_slot, arm=arm)
    base = {
        "pair_slot": pair_slot,
        "arm": arm,
        "seed": desc["runner_contract"]["cli_values"]["--seed"],
        "held_out": desc["held_out"],
        "opponent_snapshot_id": desc["apollyon_opponent"]["snapshot_id"],
        "warm_start_sha256": "c" * 64,
        "status": status,
    }
    if status == m.STATUS_COMPLETED:
        base.update(
            {
                "outcome": m.OUTCOME_DRAW_OR_UNFINISHED,
                "trajectory_sha256": "a" * 64,
                "summary_sha256": "b" * 64,
            }
        )
    elif status == m.STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE:
        base.update(
            {
                "failed_round": 14,
                "failure_class": m.FAILURE_OPPONENT_MODEL_PROTOCOL,
                "pair_excluded_from_matched_scoring": True,
                "partial_trajectory_sha256": "d" * 64,
                "rounds_completed": 13,
                "terminal_no_retry": True,
            }
        )
    return base


def test_static_source_has_no_execution_surface():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.Call):
            parts = []
            cur = node.func
            while isinstance(cur, ast.Attribute):
                parts.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                parts.append(cur.id)
            dotted = ".".join(reversed(parts)) if parts else ""
            assert dotted not in FORBIDDEN_CALL_NAMES


def test_descriptor_topology_is_exact_and_nonrunnable():
    m = _load()
    rows = m.all_execution_descriptors()
    assert len(rows) == 36
    assert [row["execution_index"] for row in rows] == list(range(1, 37))
    assert sum(row["arm"] == "baseline" for row in rows) == 18
    assert sum(row["arm"] == "candidate" for row in rows) == 18
    for row in rows:
        assert row["eligible"] is False
        assert row["command"]["argv_materialized"] is False
        assert row["command"]["shell_command_materialized"] is False
        assert row["command"]["process_spawn_implemented"] is False
        assert row["workdir"]["path_materialized"] is False
        assert row["workdir"]["created"] is False
        assert row["runtime"]["cross_control_selector_implemented"] is False
        assert row["runtime"]["selection_performed"] is False
        assert row["runtime"]["started"] is False
        assert row["warm_start_pair_binding"]["raw_sha256_equality_required"] is False
        assert row["warm_start_pair_binding"]["normalized_sha256_equality_required"] is True


def test_completed_result_shape_is_exactly_admitted():
    m = _load()
    row = _record(m, status=m.STATUS_COMPLETED)
    checked = m.validate_result_record(row)
    assert checked == row


def test_terminal_result_shape_is_exactly_admitted_and_no_retry():
    m = _load()
    row = _record(
        m,
        status=m.STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE,
    )
    checked = m.validate_result_record(row)
    assert checked == row
    assert checked["terminal_no_retry"] is True
    assert checked["pair_excluded_from_matched_scoring"] is True


def test_terminal_result_cannot_gain_completed_artifacts():
    m = _load()
    row = _record(
        m,
        status=m.STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE,
    )
    row["summary_sha256"] = "e" * 64
    _expect_hold(
        m.ExecutionAdapterHold,
        "completed fields",
        lambda: m.validate_result_record(row),
    )


def test_completed_result_cannot_gain_terminal_fields():
    m = _load()
    row = _record(m, status=m.STATUS_COMPLETED)
    row["terminal_no_retry"] = True
    _expect_hold(
        m.ExecutionAdapterHold,
        "terminal fields",
        lambda: m.validate_result_record(row),
    )


def test_result_identity_is_bound_to_frozen_ledger():
    m = _load()
    row = _record(m, status=m.STATUS_COMPLETED)
    row["seed"] += 1
    _expect_hold(
        m.ExecutionAdapterHold,
        "seed does not match",
        lambda: m.validate_result_record(row),
    )


def test_duplicate_arm_result_is_rejected():
    m = _load()
    row = _record(m, status=m.STATUS_COMPLETED)
    _expect_hold(
        m.ExecutionAdapterHold,
        "duplicate result record",
        lambda: m.validate_result_records([row, dict(row)]),
    )


def test_empty_resume_begins_with_pair1_baseline_only_as_next_cursor():
    m = _load()
    out = m.resume_plan([])
    assert out["observed_result_count"] == 0
    assert out["complete_pair_count"] == 0
    assert out["sealed_excluded_pair_count"] == 0
    assert out["pending_pair_count"] == 18
    assert out["remaining_arm_count"] == 36
    assert out["next_descriptor"]["pair_slot"] == 1
    assert out["next_descriptor"]["arm"] == "baseline"
    assert out["commands_materialized"] is False
    assert out["runtime_selection_performed"] is False
    assert out["runtime_execution_authorized"] is False


def test_resume_after_baseline_moves_to_same_pair_candidate():
    m = _load()
    baseline = _record(m, pair_slot=1, arm="baseline")
    out = m.resume_plan([baseline])
    assert out["remaining_arm_count"] == 35
    assert out["next_descriptor"]["pair_slot"] == 1
    assert out["next_descriptor"]["arm"] == "candidate"


def test_completed_pair_moves_cursor_to_pair2_baseline():
    m = _load()
    baseline = _record(m, pair_slot=1, arm="baseline")
    candidate = _record(m, pair_slot=1, arm="candidate")
    candidate["trajectory_sha256"] = "d" * 64
    candidate["summary_sha256"] = "e" * 64
    candidate["warm_start_sha256"] = "f" * 64
    out = m.resume_plan([candidate, baseline])
    assert out["complete_pair_count"] == 1
    assert out["sealed_excluded_pair_count"] == 0
    assert out["matched_scoring_pair_slots"] == [1]
    assert out["remaining_arm_count"] == 34
    assert out["next_descriptor"]["pair_slot"] == 2
    assert out["next_descriptor"]["arm"] == "baseline"


def test_terminal_no_retry_seals_pair_and_skips_missing_counterpart():
    m = _load()
    terminal = _record(
        m,
        pair_slot=1,
        arm="baseline",
        status=m.STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE,
    )
    out = m.resume_plan([terminal])
    assert out["complete_pair_count"] == 0
    assert out["sealed_excluded_pair_count"] == 1
    assert out["excluded_pair_slots"] == [1]
    assert out["pair_states"][0]["state"] == "SEALED_EXCLUDED_NO_RETRY"
    assert out["remaining_arm_count"] == 34
    assert out["next_descriptor"]["pair_slot"] == 2
    assert out["next_descriptor"]["arm"] == "baseline"
    assert all(
        row["pair_slot"] != 1
        for row in out["all_remaining_descriptors"]
    )


def test_resume_is_input_order_independent():
    m = _load()
    rows = [
        _record(m, pair_slot=1, arm="baseline"),
        _record(m, pair_slot=1, arm="candidate"),
        _record(m, pair_slot=2, arm="baseline"),
    ]
    rows[1]["trajectory_sha256"] = "d" * 64
    rows[1]["summary_sha256"] = "e" * 64
    rows[1]["warm_start_sha256"] = "f" * 64
    rows[2]["trajectory_sha256"] = "1" * 64
    rows[2]["summary_sha256"] = "2" * 64
    rows[2]["warm_start_sha256"] = "3" * 64
    assert m.resume_plan(rows) == m.resume_plan(list(reversed(rows)))


def test_execute_always_holds():
    m = _load()
    _expect_hold(
        m.ExecutionAdapterHold,
        "EXECUTION_IMPLEMENTATION_NOT_PRESENT",
        lambda: m.execute(),
    )
