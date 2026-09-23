from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2
    as entry,
)


def test_entrypoint_contract_is_inert_and_requires_inherited_fd():
    out = entry.pair06_v8_proto_game_child_entrypoint_contract()
    assert out["pair06_v8_proto_game_child_entrypoint_implemented"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["inherited_fd_required"] is True
    assert out["socketpair_created_by_entrypoint"] is False
    assert out["exact_confirmation_token_required"] is True
    assert out["execution_performed_by_contract_inspection"] is False
    assert out["child_spawn_performed_by_entrypoint"] is False
    assert out["model_load_performed_by_entrypoint"] is False


def test_parser_requires_all_operational_inputs():
    args = entry.parser().parse_args([
        "--fd", "7",
        "--attempt-id", "a" * 64,
        "--runs-root", "/tmp/runs",
        "--frozen-source-root", "/tmp/source",
        "--exact-engine-root", "/tmp/engine",
        "--confirm", entry.CONFIRM_TOKEN,
    ])
    assert args.fd == 7
    assert args.attempt_id == "a" * 64


def test_entrypoint_frontier_is_parent_supervisor():
    out = entry.pair06_v8_proto_game_child_entrypoint_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED"
    )
