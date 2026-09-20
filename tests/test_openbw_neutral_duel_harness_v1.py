from pathlib import Path

import pytest

from openra_env.learning import openbw_neutral_duel_harness_v1 as harness


ROOT = Path(__file__).resolve().parents[1]
BOT = ROOT / "integrations/openbw/neutral_smoke_bot.cpp"


def test_contract_binds_neutral_non_model_two_process_topology():
    value = harness.neutral_duel_contract()
    assert value["upstream"]["openbw_commit"] == harness.OPENBW_COMMIT
    assert value["upstream"]["bwapi_commit"] == harness.BWAPI_COMMIT
    assert value["war_college_sources"]["bot_source"]["git_blob_sha1"] == harness.BOT_SOURCE_BLOB
    assert value["war_college_sources"]["cmake"]["git_blob_sha1"] == harness.BOT_CMAKE_BLOB
    assert value["bots"]["A"]["actual_apollyon"] is False
    assert value["bots"]["A"]["actual_abaddon"] is False
    assert value["bots"]["B"]["actual_apollyon"] is False
    assert value["bots"]["B"]["actual_abaddon"] is False
    assert value["future_runtime_topology"]["process_count"] == 2
    assert value["future_runtime_topology"]["players"] == 2
    assert value["future_runtime_topology"]["local_transport"] == "LOCAL"
    assert value["future_runtime_topology"]["host_seed_override"] == 2050
    assert value["future_runtime_topology"]["joiner_seed_override"] is None
    assert all(flag is False for flag in value["authority"].values())


def test_bot_source_is_minimal_and_does_not_enable_hidden_or_user_input():
    source = BOT.read_text(encoding="utf-8")
    assert "leaveGame()" in source
    assert "kBoundedLeaveFrame = 480" in source
    assert "setCommandOptimizationLevel(0)" in source
    assert "enableFlag(" not in source
    assert "sendText(" not in source
    assert "std::ifstream" not in source
    assert "std::ofstream" not in source
    assert "system(" not in source
    assert "socket(" not in source
    assert "fork(" not in source


def test_environment_plan_uses_bwapi_exact_env_mapping_and_same_map():
    value = harness.neutral_duel_contract()
    host = value["future_runtime_topology"]["host_environment"]
    joiner = value["future_runtime_topology"]["joiner_environment"]
    for env in (host, joiner):
        assert env["OPENBW_ENABLE_UI"] == "0"
        assert env["OPENBW_LAN_MODE"] == "LOCAL"
        assert env["BWAPI_CONFIG_AUTO_MENU__AUTO_MENU"] == "LAN"
        assert env["BWAPI_CONFIG_AUTO_MENU__MAP"] == "<operator_admitted_shared_map_path>"
        assert env["BWAPI_CONFIG_AUTO_MENU__GAME"] == harness.GAME_NAME
        assert env["BWAPI_CONFIG_AUTO_MENU__AUTO_RESTART"] == "OFF"
        assert env["BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_MIN_PLAYERS"] == "2"
        assert env["BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_MAX_PLAYERS"] == "2"
    assert host["BWAPI_CONFIG_STARCRAFT__SEED_OVERRIDE"] == "2050"
    assert "BWAPI_CONFIG_STARCRAFT__SEED_OVERRIDE" not in joiner


def test_compile_receipt_is_build_only_and_never_authorizes_runtime():
    receipt = {
        "schema": harness.COMPILE_RECEIPT_SCHEMA,
        "openbw_commit": harness.OPENBW_COMMIT,
        "bwapi_commit": harness.BWAPI_COMMIT,
        "bot_source_git_blob_sha1": harness.BOT_SOURCE_BLOB,
        "bot_cmake_git_blob_sha1": harness.BOT_CMAKE_BLOB,
        "bwapilauncher_build_passed": True,
        "bot_a_build_passed": True,
        "bot_b_build_passed": True,
        "bot_a_gameInit_export_present": True,
        "bot_a_newAIModule_export_present": True,
        "bot_b_gameInit_export_present": True,
        "bot_b_newAIModule_export_present": True,
        "launcher_executed": False,
        "bot_a_loaded": False,
        "bot_b_loaded": False,
        "game_assets_read": False,
        "game_session_created": False,
        "model_executed": False,
        "training_performed": False,
    }
    result = harness.validate_compile_receipt(receipt)
    assert result["compile_evidence_valid"] is True
    assert result["runtime_authorized"] is False


def test_asset_evidence_shape_never_becomes_execution_authority():
    hashes = {name: "a" * 64 for name in harness.REQUIRED_GAME_DATA}
    claim = {
        "schema": harness.RUNTIME_ADMISSION_SCHEMA,
        "game_data_sha256": hashes,
        "map_sha256": "b" * 64,
        "license_or_ownership_reviewed_by_operator": True,
    }
    result = harness.validate_future_runtime_admission(claim)
    assert result["asset_evidence_shape_valid"] is True
    assert result["runtime_authorized"] is False
    assert result["game_execution_authorized"] is False
    with pytest.raises(harness.OpenBWNeutralDuelHold):
        harness.authorize_or_execute()
