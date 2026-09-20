"""Source-only contract for evaluating OpenBW as a second War College arena.

This module pins public upstream source identities and defines a build-only probe.
It does not clone, build, launch, network, read game assets, or authorize a match.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

SCHEMA = "void.war-college.openbw-arena-probe.v1"
RECEIPT_SCHEMA = "void.war-college.openbw-headless-build-receipt.v1"
NEXT_GATE = "OPENBW_HEADLESS_BUILD_PROBE_HOSTED_CI_REQUIRED"

OPENBW = {
    "repository": "OpenBW/openbw",
    "branch": "master",
    "commit": "4b046d5f65302b10cb0a745f0fecd37ec85b20a8",
    "license_file_at_repo_root": None,
    "github_detected_license": None,
}

OPENBW_BWAPI = {
    "repository": "OpenBW/bwapi",
    "branch": "develop-openbw",
    "commit": "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2",
    "license_file": "LICENSE",
    "license_file_git_blob_sha1": "65c5ca88a67c30becee01c5a8816d964b03862f9",
    "license_text": "GNU Lesser General Public License version 3",
}

REQUIRED_EXTERNAL_GAME_DATA = ("Stardat.mpq", "Broodat.mpq", "Patch_rt.mpq")

BWAPI_COMPAT = {
    "reason": "GCC 13 requires an explicit <cstdint> include for uint32_t in BWAPI/Game.h",
    "upstream_pr": "OpenBW/bwapi#16",
    "upstream_patch_commit": "04eb2f7f88174808ba46e3a53cc2a82f85da57ad",
    "target": "bwapi/include/BWAPI/Game.h",
    "preimage_git_blob_sha1": "ccf26f5e77693e5f682ff27f7d3185ad08b6c7b6",
    "postimage_git_blob_sha1": "debb572f6eb23c44ff1096bf8ba3ebea5da3ac7b",
    "semantic_change": "add_missing_cstdint_include",
}


class OpenBWArenaProbeHold(ValueError):
    pass


def openbw_arena_probe_contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "purpose": "compile-only feasibility probe for a second War College RTS arena",
        "upstream": {
            "openbw": deepcopy(OPENBW),
            "bwapi": deepcopy(OPENBW_BWAPI),
        },
        "integration": {
            "strategy": "external_pinned_dependency",
            "vendor_openbw_source_into_war_college": False,
            "vendor_bwapi_source_into_war_college": False,
            "openbw_core_license_clarity_required_before_redistribution": True,
            "headless_build": True,
            "openbw_ui_enabled": False,
            "build_target": "BWAPILauncher",
            "build_only": True,
            "launcher_execution": False,
            "compatibility_patch": deepcopy(BWAPI_COMPAT),
            "compatibility_patch_upstream_open": True,
            "compatibility_patch_transient_only": True,
        },
        "runtime": {
            "required_external_game_data": REQUIRED_EXTERNAL_GAME_DATA,
            "game_assets_bundled": False,
            "game_assets_downloaded_by_probe": False,
            "built_in_computer_player_available": False,
            "initial_arena_topology": "future_two_process_1v1_with_owned_agents",
            "actual_apollyon_claim": False,
            "actual_abaddon_claim": False,
        },
        "authority": {
            "game_execution_authorized": False,
            "model_execution_authorized": False,
            "training_authorized": False,
            "policy_promotion_authorized": False,
            "network_service_authorized": False,
            "asset_acquisition_authorized": False,
        },
        "next_gate": NEXT_GATE,
    }


def validate_headless_build_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    if type(receipt) is not dict:
        raise OpenBWArenaProbeHold("receipt_object_required")
    if receipt.get("schema") != RECEIPT_SCHEMA:
        raise OpenBWArenaProbeHold("receipt_schema")
    if receipt.get("openbw_commit") != OPENBW["commit"]:
        raise OpenBWArenaProbeHold("openbw_commit_drift")
    if receipt.get("bwapi_commit") != OPENBW_BWAPI["commit"]:
        raise OpenBWArenaProbeHold("bwapi_commit_drift")
    for field in (
        "headless_configure_passed",
        "bwapilauncher_build_passed",
        "launcher_exists",
    ):
        if receipt.get(field) is not True:
            raise OpenBWArenaProbeHold("missing_build_fact:" + field)
    for field in (
        "launcher_executed",
        "game_assets_read",
        "game_assets_downloaded",
        "game_session_created",
        "model_executed",
        "training_performed",
    ):
        if receipt.get(field) is not False:
            raise OpenBWArenaProbeHold("forbidden_runtime_fact:" + field)
    return {
        "schema": "void.war-college.openbw-headless-build-admission.v1",
        "build_probe_valid": True,
        "runtime_authorized": False,
        "next_gate": "OPENBW_RUNTIME_ASSET_AND_TWO_AGENT_HARNESS_DESIGN_REQUIRED",
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise OpenBWArenaProbeHold(NEXT_GATE)
