"""Compile-only contract for current Blizzard CASC data support in OpenBW.

This contract permits only a transient exact-source transformation and build
probe. It does not install Battle.net, open any game data, launch OpenBW, load
bots, create a session, or authorize training/runtime.
"""

from __future__ import annotations

from typing import Any

SCHEMA = "void.war-college.openbw-casc-loader-probe.v1"
NEXT_GATE = "OPENBW_CURRENT_BLIZZARD_DATA_INSTALLATION_REQUIRED"

OPENBW = {
    "repository": "OpenBW/openbw",
    "commit": "4b046d5f65302b10cb0a745f0fecd37ec85b20a8",
    "data_loading_blob": "c8d5a0fd65a1672116189e9c95a7706e81f6671c",
    "root_license_file_present": False,
}

BWAPI = {
    "repository": "OpenBW/bwapi",
    "commit": "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2",
    "openbwdata_cmake_blob": "4339d2300fefce5005ed57f49522d0ad66038019",
    "cstdint_patch_commit": "04eb2f7f88174808ba46e3a53cc2a82f85da57ad",
}

CASCLIB = {
    "repository": "ladislav-zezula/CascLib",
    "commit": "2a280f5a231966dc5d1b534978dd9f9f04a374cd",
    "license": "MIT",
    "license_blob": "3b17df3d9bc1d17b55b61024baec95bfb1f264ea",
    "header_blob": "39e9d3bdf360940e165f7793c95acac5fe00a8ca",
}

OFFICIAL_INSTALLER = {
    "requested_product": "STARCRAFT",
    "effective_artifact": "Battle.net-Setup.exe",
    "effective_version_path": "installer/win/1.0.66/Battle.net-Setup.exe",
    "sha256": "de5d32d4ea5eed5a9e120027fb68b370976dbfecc8f2a8f91305977f0b87fcaf",
    "bytes": 4896464,
    "executed": False,
}


class OpenBWCascProbeHold(ValueError):
    pass


def casc_loader_probe_contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "purpose": "compile-only current Blizzard CASC compatibility feasibility",
        "upstream": {
            "openbw": dict(OPENBW),
            "bwapi": dict(BWAPI),
            "casclib": dict(CASCLIB),
        },
        "official_installer_observation": dict(OFFICIAL_INSTALLER),
        "transformation": {
            "openbw_checkout_only": True,
            "exact_preimage_required": True,
            "war_college_vendors_modified_openbw": False,
            "chkforge_source_copied": False,
            "casclib_api_reimplemented": False,
            "casclib_linked_as_external_mit_dependency": True,
            "loader_behavior": "CascOpenStorage+CascOpenFile+CascReadFile",
        },
        "build": {
            "casclib_shared_library": True,
            "openbw_ui_enabled": False,
            "bwapilauncher_target": True,
            "bwapilauncher_execution": False,
            "game_data_opened": False,
        },
        "authority": {
            "battle_net_install_authorized": False,
            "game_install_authorized": False,
            "game_data_read_authorized": False,
            "game_execution_authorized": False,
            "bot_load_authorized": False,
            "model_execution_authorized": False,
            "training_authorized": False,
            "policy_promotion_authorized": False,
        },
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise OpenBWCascProbeHold(NEXT_GATE)
