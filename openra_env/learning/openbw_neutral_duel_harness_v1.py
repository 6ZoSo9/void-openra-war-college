"""Source-only neutral two-agent OpenBW smoke-duel contract.

This stage binds War College-owned neutral BWAPI bot source and a deterministic
future local 1v1 topology. It does not inspect game assets, create a socket,
launch BWAPILauncher, execute a bot, create a game session, train, or bind the
Apollyon/Abaddon identities.
"""

from __future__ import annotations

from typing import Any, Mapping

SCHEMA = "void.war-college.openbw-neutral-duel-harness.v1"
COMPILE_RECEIPT_SCHEMA = "void.war-college.openbw-neutral-bot-compile-receipt.v1"
RUNTIME_ADMISSION_SCHEMA = "void.war-college.openbw-neutral-duel-runtime-admission.v1"
NEXT_GATE = "OPENBW_NEUTRAL_DUEL_COMPILE_EVIDENCE_REQUIRED"

OPENBW_COMMIT = "4b046d5f65302b10cb0a745f0fecd37ec85b20a8"
BWAPI_COMMIT = "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2"
BWAPI_CSTDINT_PATCH_COMMIT = "04eb2f7f88174808ba46e3a53cc2a82f85da57ad"
BOT_SOURCE_BLOB = "2ee1ee850b7b4ef2fb3292305189375f97015f3a"
BOT_CMAKE_BLOB = "39ca02f5bde4dc42a949846433fd59285b47ffff"

SEED = 2050
BOUNDED_LEAVE_FRAME = 480
GAME_NAME = "VOID_WC_OPENBW_SMOKE_V1"
RACE = "Terran"
GAME_TYPE = "MELEE"
REQUIRED_GAME_DATA = ("Stardat.mpq", "Broodat.mpq", "Patch_rt.mpq")


class OpenBWNeutralDuelHold(ValueError):
    pass


def neutral_duel_contract() -> dict[str, Any]:
    common_env = {
        "OPENBW_ENABLE_UI": "0",
        "OPENBW_LAN_MODE": "LOCAL",
        "OPENBW_LOCAL_PATH": "<private_run_dir>/openbw-duel.sock",
        "BWAPI_CONFIG_AUTO_MENU__AUTO_MENU": "LAN",
        "BWAPI_CONFIG_AUTO_MENU__MAP": "<operator_admitted_shared_map_path>",
        "BWAPI_CONFIG_AUTO_MENU__GAME": GAME_NAME,
        "BWAPI_CONFIG_AUTO_MENU__RACE": RACE,
        "BWAPI_CONFIG_AUTO_MENU__GAME_TYPE": GAME_TYPE,
        "BWAPI_CONFIG_AUTO_MENU__AUTO_RESTART": "OFF",
        "BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_MIN_PLAYERS": "2",
        "BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_MAX_PLAYERS": "2",
        "BWAPI_CONFIG_AUTO_MENU__WAIT_FOR_TIME": "0",
        "BWAPI_CONFIG_CONFIG__SHARED_MEMORY": "OFF",
        "BWAPI_CONFIG_STARCRAFT__SOUND": "OFF",
        "LD_LIBRARY_PATH": "<pinned_bwapi_build>/lib",
    }
    host_env = {
        **common_env,
        "BWAPI_CONFIG_AI__AI": "<war_college_bot_a_so>",
        "BWAPI_CONFIG_STARCRAFT__SEED_OVERRIDE": str(SEED),
    }
    joiner_env = {
        **common_env,
        "BWAPI_CONFIG_AI__AI": "<war_college_bot_b_so>",
    }
    return {
        "schema": SCHEMA,
        "upstream": {
            "openbw_commit": OPENBW_COMMIT,
            "bwapi_commit": BWAPI_COMMIT,
            "bwapi_cstdint_patch_commit": BWAPI_CSTDINT_PATCH_COMMIT,
        },
        "war_college_sources": {
            "bot_source": {
                "path": "integrations/openbw/neutral_smoke_bot.cpp",
                "git_blob_sha1": BOT_SOURCE_BLOB,
            },
            "cmake": {
                "path": "integrations/openbw/CMakeLists.txt",
                "git_blob_sha1": BOT_CMAKE_BLOB,
            },
        },
        "bots": {
            "A": {
                "identity": "void-openbw-neutral-smoke-a-v1",
                "compile_role": 0,
                "behavior": "passive_except_leave_at_fixed_frame",
                "leave_frame": BOUNDED_LEAVE_FRAME,
                "actual_apollyon": False,
                "actual_abaddon": False,
            },
            "B": {
                "identity": "void-openbw-neutral-smoke-b-v1",
                "compile_role": 1,
                "behavior": "passive",
                "leave_frame": None,
                "actual_apollyon": False,
                "actual_abaddon": False,
            },
        },
        "future_runtime_topology": {
            "process_count": 2,
            "players": 2,
            "local_transport": "LOCAL",
            "private_socket_path_required": True,
            "socket_must_not_preexist": True,
            "host_starts_first": True,
            "joiner_starts_only_after_host_socket_observed": True,
            "same_map_bytes_required": True,
            "host_seed_override": SEED,
            "joiner_seed_override": None,
            "host_environment": host_env,
            "joiner_environment": joiner_env,
            "working_directory": "<operator_admitted_game_data_root>",
            "required_game_data": REQUIRED_GAME_DATA,
            "required_game_data_sha256": None,
            "required_map_sha256": None,
        },
        "evidence": {
            "compile_before_runtime": True,
            "bot_shared_objects_must_be_elf": True,
            "gameInit_export_required": True,
            "newAIModule_export_required": True,
            "runtime_rows_training_candidate": False,
            "automatic_corpus_admission": False,
            "automatic_policy_promotion": False,
            "replay_hash_required_after_future_runtime": True,
        },
        "authority": {
            "asset_admission_complete": False,
            "runtime_authorized": False,
            "game_execution_authorized": False,
            "model_execution_authorized": False,
            "training_authorized": False,
            "policy_promotion_authorized": False,
            "apollyon_binding_authorized": False,
            "abaddon_binding_authorized": False,
        },
        "next_gate": NEXT_GATE,
    }


def validate_compile_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    if type(receipt) is not dict:
        raise OpenBWNeutralDuelHold("compile_receipt_object_required")
    if receipt.get("schema") != COMPILE_RECEIPT_SCHEMA:
        raise OpenBWNeutralDuelHold("compile_receipt_schema")
    for field, value in (
        ("openbw_commit", OPENBW_COMMIT),
        ("bwapi_commit", BWAPI_COMMIT),
        ("bot_source_git_blob_sha1", BOT_SOURCE_BLOB),
        ("bot_cmake_git_blob_sha1", BOT_CMAKE_BLOB),
    ):
        if receipt.get(field) != value:
            raise OpenBWNeutralDuelHold("compile_identity_drift:" + field)
    for field in (
        "bwapilauncher_build_passed",
        "bot_a_build_passed",
        "bot_b_build_passed",
        "bot_a_gameInit_export_present",
        "bot_a_newAIModule_export_present",
        "bot_b_gameInit_export_present",
        "bot_b_newAIModule_export_present",
    ):
        if receipt.get(field) is not True:
            raise OpenBWNeutralDuelHold("missing_compile_fact:" + field)
    for field in (
        "launcher_executed",
        "bot_a_loaded",
        "bot_b_loaded",
        "game_assets_read",
        "game_session_created",
        "model_executed",
        "training_performed",
    ):
        if receipt.get(field) is not False:
            raise OpenBWNeutralDuelHold("forbidden_runtime_fact:" + field)
    return {
        "schema": "void.war-college.openbw-neutral-bot-compile-admission.v1",
        "compile_evidence_valid": True,
        "runtime_authorized": False,
        "next_gate": "OPENBW_OPERATOR_GAME_DATA_ADMISSION_REQUIRED",
    }


def validate_future_runtime_admission(claim: Mapping[str, Any]) -> dict[str, Any]:
    """Validate only a future evidence shape. Success still grants no execution."""
    if type(claim) is not dict or claim.get("schema") != RUNTIME_ADMISSION_SCHEMA:
        raise OpenBWNeutralDuelHold("runtime_admission_schema")
    assets = claim.get("game_data_sha256")
    if type(assets) is not dict or set(assets) != set(REQUIRED_GAME_DATA):
        raise OpenBWNeutralDuelHold("game_data_hash_set")
    for value in assets.values():
        if not _is_sha256(value):
            raise OpenBWNeutralDuelHold("game_data_hash_invalid")
    if not _is_sha256(claim.get("map_sha256")):
        raise OpenBWNeutralDuelHold("map_hash_invalid")
    if claim.get("license_or_ownership_reviewed_by_operator") is not True:
        raise OpenBWNeutralDuelHold("operator_asset_rights_review_required")
    return {
        "schema": "void.war-college.openbw-neutral-duel-runtime-evidence-admission.v1",
        "asset_evidence_shape_valid": True,
        "runtime_authorized": False,
        "game_execution_authorized": False,
        "next_gate": "OPENBW_NEUTRAL_DUEL_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED",
    }


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise OpenBWNeutralDuelHold(
        "OPENBW_NEUTRAL_DUEL_SEPARATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
