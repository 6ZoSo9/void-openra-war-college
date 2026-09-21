from pathlib import Path

import pytest

from openra_env.learning import openbw_online_casc_metadata_probe_v1 as probe


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "integrations/openbw/online_casc_metadata_probe.cpp"


def test_contract_pins_source_and_casclib_identity():
    c = probe.online_casc_metadata_contract()
    assert c["upstream"]["casclib"]["commit"] == "2a280f5a231966dc5d1b534978dd9f9f04a374cd"
    assert c["upstream"]["casclib"]["license"] == "MIT"
    assert c["upstream"]["casclib"]["string_parameter_separator"] == "*"
    assert c["probe"]["source_blob"] == "fe1e3b76e107e7d3df44ed22d2e670080e178ea9"
    assert c["probe"]["cmake_blob"] == "c605e10d3a49e385b57ab491af11eee02ca8a25e"
    assert c["probe"]["product"] == "s1"
    assert c["probe"]["region"] == "us"
    assert c["probe"]["locale"] == "enUS"
    assert c["probe"]["open_transport"] == "CASC_OPEN_STORAGE_ARGS"
    assert c["probe"]["string_parameter_parser_used"] is False


def test_probe_uses_structured_online_open_and_is_metadata_only():
    source = SOURCE.read_text(encoding="utf-8")
    assert "CASC_OPEN_STORAGE_ARGS" in source
    assert "CascOpenStorageEx(nullptr, &open_args, true, &storage)" in source
    assert "CascOpenOnlineStorage(" not in source
    assert 'cache + ":s1:us"' not in source
    assert 'cache + "*s1*us"' not in source
    assert 'open_args.szCodeName = "s1"' in source
    assert 'open_args.szRegion = "us"' in source
    assert "open_args.dwFlags = CASC_FEATURE_ALLOW_DOWNLOAD" in source
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
    assert c["behavior"]["structured_open_args"] is True
    assert c["behavior"]["internal_metadata_download_flag"] is True
    assert c["behavior"]["string_parameter_parser_used"] is False
    assert c["behavior"]["open_game_file_payload"] is False
    assert c["behavior"]["read_game_file_payload"] is False
    assert c["behavior"]["battle_net_required"] is False
    assert all(v is False for v in c["authority"].values())
    with pytest.raises(probe.OpenBWOnlineCascMetadataHold):
        probe.authorize_or_execute()
