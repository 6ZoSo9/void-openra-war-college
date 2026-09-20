from pathlib import Path

import pytest

from openra_env.learning import openbw_casc_loader_probe_v1 as probe


ROOT = Path(__file__).resolve().parents[1]
TRANSFORMER = ROOT / "scripts/apply_openbw_casc_loader_compat_v1.py"
BRIDGE = ROOT / "integrations/openbw/casc_bridge/void_openbw_casc_bridge.cpp"


def test_contract_pins_all_upstream_identities():
    c = probe.casc_loader_probe_contract()
    assert c["upstream"]["openbw"]["commit"] == "4b046d5f65302b10cb0a745f0fecd37ec85b20a8"
    assert c["upstream"]["openbw"]["data_loading_blob"] == "c8d5a0fd65a1672116189e9c95a7706e81f6671c"
    assert c["upstream"]["bwapi"]["commit"] == "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2"
    assert c["upstream"]["casclib"]["commit"] == "2a280f5a231966dc5d1b534978dd9f9f04a374cd"
    assert c["upstream"]["casclib"]["license"] == "MIT"
    assert c["upstream"]["casclib"]["license_blob"] == "3b17df3d9bc1d17b55b61024baec95bfb1f264ea"
    bridge = c["upstream"]["war_college_casc_bridge"]
    assert bridge["header_blob"] == "112a6190449127f6c305273a764786085ea179d1"
    assert bridge["source_blob"] == "81b954aca0b0a5d7ab6975294d567da7f855be78"
    assert bridge["cmake_blob"] == "b95aa50b7f0703cc38657a4be77fb693eb869739"


def test_transformer_is_exact_source_bound_and_openbw_never_includes_casclib():
    source = TRANSFORMER.read_text(encoding="utf-8")
    assert "OPENBW_DATA_LOADING_PREIMAGE" in source
    assert "BWAPI_OPENBWDATA_CMAKE_PREIMAGE" in source
    assert "void_openbw_casc_bridge.h" in source
    assert "CascLib.h" not in source
    assert "chkforge_source_used" in source
    assert "casclib_header_included_by_openbw" in source


def test_bridge_owns_the_casclib_api_boundary():
    source = BRIDGE.read_text(encoding="utf-8")
    for symbol in (
        "CascOpenStorage",
        "CascOpenFile",
        "CascGetFileSize64",
        "CascReadFile",
        "CascCloseFile",
        "CascCloseStorage",
    ):
        assert symbol in source


def test_contract_grants_no_install_or_runtime_authority():
    c = probe.casc_loader_probe_contract()
    assert all(value is False for value in c["authority"].values())
    assert c["build"]["bwapilauncher_execution"] is False
    assert c["build"]["game_data_opened"] is False
    assert c["transformation"]["war_college_vendors_modified_openbw"] is False
    assert c["transformation"]["chkforge_source_copied"] is False
    assert c["transformation"]["casclib_header_included_by_openbw"] is False
    assert c["transformation"]["war_college_c_abi_shim"] is True
    with pytest.raises(probe.OpenBWCascProbeHold):
        probe.authorize_or_execute()


def test_official_installer_observation_is_nonexecution():
    obs = probe.casc_loader_probe_contract()["official_installer_observation"]
    assert obs["effective_artifact"] == "Battle.net-Setup.exe"
    assert obs["sha256"] == "de5d32d4ea5eed5a9e120027fb68b370976dbfecc8f2a8f91305977f0b87fcaf"
    assert obs["bytes"] == 4896464
    assert obs["executed"] is False
