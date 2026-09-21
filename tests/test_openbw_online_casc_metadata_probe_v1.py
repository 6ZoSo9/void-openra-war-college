from pathlib import Path

import pytest

from openra_env.learning import openbw_online_casc_metadata_probe_v1 as probe


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "integrations/openbw/online_casc_metadata_probe.cpp"


def test_contract_pins_source_and_casclib_identity():
    c = probe.online_casc_metadata_contract()
    assert c["upstream"]["casclib"]["commit"] == "2a280f5a231966dc5d1b534978dd9f9f04a374cd"
    assert c["upstream"]["casclib"]["license"] == "MIT"
    assert c["probe"]["source_blob"] == "ec60962594eaad1a4808f5c7d52c3d792a6ad12c"
    assert c["probe"]["cmake_blob"] == "c605e10d3a49e385b57ab491af11eee02ca8a25e"
    assert c["probe"]["product"] == "s1"
    assert c["probe"]["region"] == "us"
    assert c["probe"]["locale"] == "enUS"


def test_probe_is_metadata_only():
    source = SOURCE.read_text(encoding="utf-8")
    assert "CascOpenOnlineStorage" in source
    assert "CascFindFirstFile" in source
    assert "CascFindNextFile" in source
    assert "CascOpenFile(" not in source
    assert "CascReadFile(" not in source
    assert "system(" not in source
    assert "popen(" not in source
    assert "Battle.net" not in source
    assert "StarCraft.exe" not in source


def test_expected_classic_suffixes_are_bound():
    c = probe.online_casc_metadata_contract()
    suffixes = set(c["critical_suffixes"])
    for value in (
        "arr/units.dat",
        "arr/weapons.dat",
        "arr/techdata.dat",
        "tileset/badlands.cv5",
        "tileset/badlands.vr4",
    ):
        assert value in suffixes


def test_no_runtime_or_payload_authority():
    c = probe.online_casc_metadata_contract()
    assert c["behavior"]["open_game_file_payload"] is False
    assert c["behavior"]["read_game_file_payload"] is False
    assert c["behavior"]["battle_net_required"] is False
    assert all(v is False for v in c["authority"].values())
    with pytest.raises(probe.OpenBWOnlineCascMetadataHold):
        probe.authorize_or_execute()
