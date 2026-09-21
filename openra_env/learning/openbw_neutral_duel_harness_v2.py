"""Source-only contract for the qualified OpenBW S1 neutral dual harness v2.

This contract adopts the exact War College-owned bot/CMake bytes exercised by the
merged-builder dual LOCAL_FD qualification. Importing it performs no filesystem,
network, CASC, OpenBW, bot, model, or game action.
"""

from __future__ import annotations

from typing import Any, Mapping

SCHEMA = "void.war-college.openbw-neutral-duel-harness.v2"
QUALIFICATION_SCHEMA = "void.war-college.openbw-s1-merged-builder-runtime-qualification.v1"
QUALIFICATION_RECEIPT = (
    "config/war-college/openbw-s1-merged-builder-runtime-qualification-v1.json"
)

QUALIFIED_BUILDER_COMMIT = "6ffee13a6b8b26ed70cbb55aed3df5e9d7d20c73"
SOURCE_BUILDER_BLOB = "7f815991a4537c03a18d1f740b44d4999addd706"
OPENBW_COMMIT = "4b046d5f65302b10cb0a745f0fecd37ec85b20a8"
BWAPI_COMMIT = "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2"
CASCLIB_COMMIT = "2a280f5a231966dc5d1b534978dd9f9f04a374cd"

BOT_SOURCE_PATH = "integrations/openbw/neutral_smoke_bot.cpp"
BOT_SOURCE_BLOB = "3bc58999d2506ee8d5e130b834e4288ea55e909e"
BOT_CMAKE_PATH = "integrations/openbw/CMakeLists.txt"
BOT_CMAKE_BLOB = "39ca02f5bde4dc42a949846433fd59285b47ffff"
DUAL_RUNTIME_VERIFIER_SHA256 = (
    "65f3dfa73c5addfe5e5acce1ad48ee49a9cba0da65b79cc635b317c68d420d48"
)

MAP_PATH = "bwapi/TestAIModule/maps/TestModule/MapTest.scx"
MAP_GIT_BLOB_SHA1 = "ca1ef64453f5c024771c9883eee75a86c1b9b66a"
MAP_SIZE_BYTES = 47310
BOUNDED_LEAVE_FRAME = 480
NAMED_PEER_DEPARTURE_MIN_FRAME = 360

NEXT_GATE = "OPENBW_NEUTRAL_AGENT_IDENTITY_BINDING_REVIEW_REQUIRED"


class OpenBWNeutralDuelV2Hold(ValueError):
    pass


def neutral_duel_contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "qualification": {
            "receipt_path": QUALIFICATION_RECEIPT,
            "qualified_builder_commit": QUALIFIED_BUILDER_COMMIT,
            "source_builder_blob": SOURCE_BUILDER_BLOB,
            "dual_runtime_verifier_sha256": DUAL_RUNTIME_VERIFIER_SHA256,
            "runtime_already_qualified": True,
        },
        "upstream": {
            "openbw_commit": OPENBW_COMMIT,
            "bwapi_commit": BWAPI_COMMIT,
            "casclib_commit": CASCLIB_COMMIT,
        },
        "war_college_sources": {
            "bot_source": {
                "path": BOT_SOURCE_PATH,
                "git_blob_sha1": BOT_SOURCE_BLOB,
            },
            "cmake": {
                "path": BOT_CMAKE_PATH,
                "git_blob_sha1": BOT_CMAKE_BLOB,
            },
        },
        "bots": {
            "A": {
                "identity": "void-openbw-neutral-smoke-a-v2",
                "compile_role": 0,
                "behavior": "passive_except_bounded_leave",
                "leave_frame": BOUNDED_LEAVE_FRAME,
                "actual_apollyon": False,
                "actual_abaddon": False,
            },
            "B": {
                "identity": "void-openbw-neutral-smoke-b-v2",
                "compile_role": 1,
                "behavior": "passive_then_leave_after_named_VOID-A_departure",
                "named_peer_departure_min_frame": NAMED_PEER_DEPARTURE_MIN_FRAME,
                "actual_apollyon": False,
                "actual_abaddon": False,
            },
        },
        "qualified_runtime_topology": {
            "process_count": 2,
            "players": 2,
            "lan_mode": "LOCAL_FD",
            "transport": "preconnected_socketpair",
            "socket_family": "AF_UNIX",
            "same_map_bytes_required": True,
            "map_path": MAP_PATH,
            "map_git_blob_sha1": MAP_GIT_BLOB_SHA1,
            "map_size_bytes": MAP_SIZE_BYTES,
            "casc_allow_download": False,
            "cache_growth_bytes": 0,
            "complete_map_information": False,
            "user_input": False,
            "bwapi_multiplayer_reporting_known_incomplete": True,
        },
        "fixture_adaptation": {
            "required_for_pinned_map": True,
            "reason": "pinned MapTest.scx has one open-human and one computer slot",
            "test_only": True,
            "production_builder_contains_lobby_promotion": False,
            "promotion": "exactly_one_computer_slot_to_open_human",
        },
        "authority": {
            "future_game_execution_authorized": False,
            "model_execution_authorized": False,
            "training_authorized": False,
            "policy_promotion_authorized": False,
            "apollyon_binding_authorized": False,
            "abaddon_binding_authorized": False,
            "deployment_authorized": False,
            "wallet_or_funds_action_authorized": False,
        },
        "next_gate": NEXT_GATE,
    }


def validate_qualification_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    if type(receipt) is not dict:
        raise OpenBWNeutralDuelV2Hold("qualification_receipt_object_required")
    if receipt.get("schema") != QUALIFICATION_SCHEMA:
        raise OpenBWNeutralDuelV2Hold("qualification_receipt_schema")
    if receipt.get("merged_main_commit") != QUALIFIED_BUILDER_COMMIT:
        raise OpenBWNeutralDuelV2Hold("qualified_builder_commit_drift")
    if receipt.get("source_builder_blob") != SOURCE_BUILDER_BLOB:
        raise OpenBWNeutralDuelV2Hold("source_builder_blob_drift")

    upstream = receipt.get("upstream")
    if upstream != {
        "openbw": OPENBW_COMMIT,
        "bwapi": BWAPI_COMMIT,
        "casclib": CASCLIB_COMMIT,
    }:
        raise OpenBWNeutralDuelV2Hold("upstream_identity_drift")

    dual = receipt.get("dual_runtime")
    if type(dual) is not dict:
        raise OpenBWNeutralDuelV2Hold("dual_runtime_receipt_required")
    required_true = (
        "two_open_human_lobby_slots_proven",
        "two_instance_local_sync_proven",
        "named_peer_departure_sync_proven",
        "bounded_peer_followup_exit_proven",
        "bounded_dual_game_lifecycle_proven",
        "merged_builder_dual_runtime_proven",
    )
    for field in required_true:
        if dual.get(field) is not True:
            raise OpenBWNeutralDuelV2Hold("missing_qualification_fact:" + field)
    if dual.get("runtime_returncodes") != [0, 0]:
        raise OpenBWNeutralDuelV2Hold("dual_runtime_returncodes")
    if dual.get("cache_growth_bytes") != 0:
        raise OpenBWNeutralDuelV2Hold("cache_growth_nonzero")
    if dual.get("casc_allow_download") is not False:
        raise OpenBWNeutralDuelV2Hold("casc_download_not_disabled")
    if dual.get("production_builder_contains_lobby_promotion") is not False:
        raise OpenBWNeutralDuelV2Hold("production_builder_lobby_promotion")
    if dual.get("transient_test_only_lobby_slot_promotion") is not True:
        raise OpenBWNeutralDuelV2Hold("test_lobby_adaptation_missing")
    if dual.get("terminal") != (
        "OPENBW_S1_MERGED_BUILDER_DUAL_LOCAL_RUNTIME_PRECISION_V2_GREEN"
    ):
        raise OpenBWNeutralDuelV2Hold("dual_runtime_terminal")

    return {
        "schema": "void.war-college.openbw-neutral-duel-v2-admission.v1",
        "qualified_runtime_evidence_valid": True,
        "future_game_execution_authorized": False,
        "model_execution_authorized": False,
        "training_authorized": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise OpenBWNeutralDuelV2Hold(NEXT_GATE)
