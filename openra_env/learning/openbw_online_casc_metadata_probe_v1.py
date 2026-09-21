"""Source contract for Blizzard s1 online-CASC metadata probing.

The executable is allowed to open Blizzard's online StarCraft metadata root only
when an operator explicitly runs it. It must not open/read any game file payload,
launch Battle.net/StarCraft/OpenBW, or train/bind an agent.
"""

from __future__ import annotations

from typing import Any

SCHEMA = "void.war-college.openbw-online-casc-metadata-probe.v1"
NEXT_GATE = "OPENBW_S1_ONLINE_CASC_METADATA_OPERATOR_PROBE_REQUIRED"

CASCLIB = {
    "repository": "ladislav-zezula/CascLib",
    "commit": "2a280f5a231966dc5d1b534978dd9f9f04a374cd",
    "license": "MIT",
    "license_blob": "3b17df3d9bc1d17b55b61024baec95bfb1f264ea",
    "header_blob": "39e9d3bdf360940e165f7793c95acac5fe00a8ca",
    "open_storage_blob": "80458a45ee6bc193472002c5e7196fdabd684ea6",
    "string_parameter_separator": "*",
}

PROBE = {
    "source_path": "integrations/openbw/online_casc_metadata_probe.cpp",
    "source_blob": "4b3a9f90ac85e25c9a391386eb668bad22b058c8",
    "cmake_path": "integrations/openbw/online_casc_metadata_probe.CMakeLists.txt",
    "cmake_blob": "c605e10d3a49e385b57ab491af11eee02ca8a25e",
    "product": "s1",
    "region": "us",
    "locale": "enUS",
    "open_transport": "CASC_OPEN_STORAGE_ARGS",
    "string_parameter_parser_used": False,
}

CRITICAL_SUFFIXES = (
    "arr/units.dat",
    "arr/weapons.dat",
    "arr/flingy.dat",
    "arr/sprites.dat",
    "arr/images.dat",
    "arr/orders.dat",
    "arr/techdata.dat",
    "arr/upgrades.dat",
    "arr/sfxdata.dat",
    "arr/sfxdata.tbl",
    "tileset/badlands.cv5",
    "tileset/badlands.vf4",
    "tileset/badlands.vx4",
    "tileset/badlands.vr4",
    "tileset/badlands.wpe",
)


class OpenBWOnlineCascMetadataHold(ValueError):
    pass


def online_casc_metadata_contract() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "upstream": {"casclib": dict(CASCLIB)},
        "probe": dict(PROBE),
        "critical_suffixes": CRITICAL_SUFFIXES,
        "behavior": {
            "online_storage_open": True,
            "structured_open_args": True,
            "string_parameter_parser_used": False,
            "enumerate_root_metadata": True,
            "normalize_name_case_and_separators": True,
            "enumeration_cap": 1_000_000,
            "open_game_file_payload": False,
            "read_game_file_payload": False,
            "write_game_file_payload": False,
            "battle_net_required": False,
            "battle_net_login_required": False,
            "battle_net_execution": False,
            "starcraft_execution": False,
            "openbw_execution": False,
        },
        "authority": {
            "operator_network_probe_authorized": False,
            "game_payload_download_authorized": False,
            "battle_net_execution_authorized": False,
            "starcraft_execution_authorized": False,
            "openbw_execution_authorized": False,
            "bot_load_authorized": False,
            "model_execution_authorized": False,
            "training_authorized": False,
        },
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise OpenBWOnlineCascMetadataHold(NEXT_GATE)
