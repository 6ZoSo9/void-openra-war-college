from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import openbw_neutral_duel_harness_v2 as harness

ROOT = Path(__file__).resolve().parents[1]
BOT = ROOT / harness.BOT_SOURCE_PATH
CMAKE = ROOT / harness.BOT_CMAKE_PATH
RECEIPT = ROOT / harness.QUALIFICATION_RECEIPT
BUILDER = ROOT / "openra_env/learning/openbw_s1_source_patch_v1.py"


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def test_adopted_bot_and_cmake_match_qualified_runtime_identities():
    assert _git_blob_sha1(BOT.read_bytes()) == harness.BOT_SOURCE_BLOB
    assert _git_blob_sha1(CMAKE.read_bytes()) == harness.BOT_CMAKE_BLOB
    assert harness.BOT_SOURCE_BLOB == "3bc58999d2506ee8d5e130b834e4288ea55e909e"
    assert harness.BOT_CMAKE_BLOB == "39ca02f5bde4dc42a949846433fd59285b47ffff"


def test_contract_uses_proven_local_fd_socketpair_topology():
    value = harness.neutral_duel_contract()
    topology = value["qualified_runtime_topology"]
    assert topology["process_count"] == 2
    assert topology["players"] == 2
    assert topology["lan_mode"] == "LOCAL_FD"
    assert topology["transport"] == "preconnected_socketpair"
    assert topology["socket_family"] == "AF_UNIX"
    assert topology["casc_allow_download"] is False
    assert topology["cache_growth_bytes"] == 0
    assert topology["complete_map_information"] is False
    assert topology["user_input"] is False
    assert topology["bwapi_multiplayer_reporting_known_incomplete"] is True


def test_bot_source_matches_bounded_dual_lifecycle():
    source = BOT.read_text(encoding="utf-8")
    assert "kBoundedLeaveFrame = 480" in source
    assert "kNamedPeerDepartureMinFrame = 360" in source
    assert 'return "VOID-A";' in source
    assert "named_peer_departure_observed_" in source
    assert "bounded_peer_followup_leave_requested=true" in source
    assert "BWAPI::Broodwar->leaveGame();" in source
    assert "enableFlag(" not in source
    assert "sendText(" not in source
    assert "issueCommand" not in source
    assert "std::ifstream" not in source
    assert "std::ofstream" not in source
    assert "socket(" not in source
    assert "fork(" not in source


def test_qualification_receipt_admits_evidence_not_future_execution():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    result = harness.validate_qualification_receipt(receipt)
    assert result["qualified_runtime_evidence_valid"] is True
    assert result["future_game_execution_authorized"] is False
    assert result["model_execution_authorized"] is False
    assert result["training_authorized"] is False
    assert result["next_gate"] == harness.NEXT_GATE


def test_qualification_receipt_matches_runtime_and_builder_boundaries():
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))
    dual = row["dual_runtime"]
    assert row["merged_main_commit"] == harness.QUALIFIED_BUILDER_COMMIT
    assert row["source_builder_blob"] == harness.SOURCE_BUILDER_BLOB
    assert _git_blob_sha1(BUILDER.read_bytes()) == harness.SOURCE_BUILDER_BLOB
    assert dual["runtime_returncodes"] == [0, 0]
    assert dual["cache_growth_bytes"] == 0
    assert dual["peak_observed_cache_growth_bytes"] == 0
    assert dual["two_instance_local_sync_proven"] is True
    assert dual["named_peer_departure_sync_proven"] is True
    assert dual["bounded_peer_followup_exit_proven"] is True
    assert dual["bounded_dual_game_lifecycle_proven"] is True
    assert dual["merged_builder_dual_runtime_proven"] is True


def test_fixture_slot_promotion_stays_out_of_production_builder():
    value = harness.neutral_duel_contract()
    fixture = value["fixture_adaptation"]
    assert fixture["required_for_pinned_map"] is True
    assert fixture["test_only"] is True
    assert fixture["production_builder_contains_lobby_promotion"] is False
    source = BUILDER.read_text(encoding="utf-8")
    assert "VOID_OPENBW_DUAL_PROMOTE_ONE_COMPUTER_SLOT" not in source
    assert "controller_computer" not in source
    assert "controller_open" not in source


def test_neutral_roles_are_not_general_identity_bindings():
    value = harness.neutral_duel_contract()
    for role in ("A", "B"):
        assert value["bots"][role]["actual_apollyon"] is False
        assert value["bots"][role]["actual_abaddon"] is False
    assert all(flag is False for flag in value["authority"].values())
    with pytest.raises(harness.OpenBWNeutralDuelV2Hold):
        harness.authorize_or_execute()


def test_receipt_drift_fails_closed():
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    receipt["dual_runtime"]["cache_growth_bytes"] = 1
    with pytest.raises(harness.OpenBWNeutralDuelV2Hold, match="cache_growth_nonzero"):
        harness.validate_qualification_receipt(receipt)
