from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "tools/abaddon_policy_campaign_orchestrator_generation2.py"
EXPECTED_SOURCE_SHA256 = (
    "a9ce01b55a0cab07ceb3c07047f17f537a9d288c8c209f89528360c996d7240b"
)

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

FORBIDDEN_IMPORT_ROOTS = {
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
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

EXPECTED_TERMINAL_POLICY = {
    "host_validation_weakening": False,
    "infrastructure_or_harness_failure": "STOP_CAMPAIGN",
    "matched_pair_scoring_excludes_terminal_pair_slots": True,
    "opponent_protocol_failure": "SEAL_NO_RETRY_CONTINUE",
    "synthetic_advance_fallback": False,
}


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_nonexecuting_orchestrator",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_static_no_execution_surface():
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


def test_preflight_stays_fail_closed():
    m = _load()
    result = m.preflight()
    assert result["pair_slot_count"] == 18
    assert result["execution_count"] == 36
    assert result["runtime_binding_count"] == 4
    assert result["execution_implementation_present"] is False
    assert result["commands_materialized"] is False
    assert result["subprocess_invocation_materialized"] is False
    assert result["runtime_selection_performed"] is False
    assert result["runtime_started"] is False
    assert result["campaign_execution_authorized"] is False
    assert result["runtime_execution_authorized"] is False
    assert result["game_execution"] is False
    assert result["model_execution"] is False
    assert result["training"] is False
    assert result["weights_updated"] is False
    assert result["automatic_corpus_admission"] is False
    assert result["automatic_policy_promotion"] is False
    assert result["deployment"] is False


def test_ledger_is_exact_18_pairs_36_arms():
    m = _load()
    rows = m.arm_ledger()
    assert len(rows) == 36
    assert sum(row["arm"] == "baseline" for row in rows) == 18
    assert sum(row["arm"] == "candidate" for row in rows) == 18
    assert sorted(
        {row["pair_slot"] for row in rows if row["held_out"]}
    ) == [13, 14, 15, 16, 17, 18]

    for i in range(0, 36, 2):
        baseline = rows[i]
        candidate = rows[i + 1]
        assert baseline["pair_slot"] == candidate["pair_slot"]
        assert (
            baseline["runner_contract"]["cli_values"]
            == candidate["runner_contract"]["cli_values"]
        )
        assert (
            baseline["apollyon_opponent"]["snapshot_id"]
            == candidate["apollyon_opponent"]["snapshot_id"]
        )
        assert baseline["abaddon_policy"]["wrapper_required"] is False
        assert candidate["abaddon_policy"]["wrapper_required"] is True
        assert (
            candidate["abaddon_policy"]["candidate_genome_sha256"]
            == m.CANDIDATE_GENOME_SHA256
        )
        assert baseline["authority"]["runtime_execution_authorized"] is False
        assert candidate["authority"]["runtime_execution_authorized"] is False


def test_runtime_usage_matches_frozen_topology():
    m = _load()
    counts = {}
    for row in m.arm_ledger():
        sid = row["apollyon_opponent"]["snapshot_id"]
        counts[sid] = counts.get(sid, 0) + 1
    assert counts == {
        "apollyon-v13-v14-promoted": 12,
        "apollyon-v13-v10-promoted": 12,
        "apollyon-v2r13-qualified-predecessor": 6,
        "apollyon-v3-v8-accepted-model-control": 6,
    }


def test_terminal_policy_exact():
    m = _load()
    assert m.TERMINAL_POLICY == EXPECTED_TERMINAL_POLICY


def test_execution_request_is_not_eligible():
    m = _load()
    request = m.execution_request(pair_slot=1, arm="candidate")
    assert request["eligible"] is False
    assert request["command_materialized"] is False
    assert request["subprocess_invocation_materialized"] is False
    assert request["runtime_selection_performed"] is False
    assert request["runtime_started"] is False
    assert request["campaign_execution_authorized"] is False
    assert request["runtime_execution_authorized"] is False
    assert request["reasons"] == [
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "EXECUTION_IMPLEMENTATION_NOT_PRESENT",
    ]


def test_execute_campaign_always_holds():
    m = _load()
    try:
        m.execute_campaign()
    except m.OrchestratorHold as exc:
        assert "EXECUTION_IMPLEMENTATION_NOT_PRESENT" in str(exc)
    else:
        raise AssertionError("execute_campaign unexpectedly returned")
