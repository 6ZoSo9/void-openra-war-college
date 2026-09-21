from __future__ import annotations

import pytest

from openra_env.learning import openbw_s1_source_patch_v1 as patch


def _data_loading_fixture() -> str:
    return (
        "prefix\n"
        + patch.DATA_LOADING_INCLUDE_OLD
        + "\nmiddle\n"
        + patch.DATA_LOADING_LOADER_OLD
        + "\nsuffix\n"
    )


def _ui_fixture() -> str:
    return "prefix\n" + patch.UI_VX4_STRUCT_OLD + "\n" + patch.UI_VX4_PARSE_OLD + "\nsuffix\n"


def _cmake_fixture() -> str:
    return "prefix\n" + patch.CMAKE_LINK_OLD + "suffix\n"


def test_upstream_pins_match_accepted_sources():
    assert patch.OPENBW_COMMIT == "4b046d5f65302b10cb0a745f0fecd37ec85b20a8"
    assert patch.BWAPI_COMMIT == "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2"
    assert patch.CASCLIB_COMMIT == "2a280f5a231966dc5d1b534978dd9f9f04a374cd"
    patch.validate_upstream_blobs(dict(patch.PINNED_UPSTREAM_BLOBS))


def test_upstream_blob_drift_fails_closed():
    observed = dict(patch.PINNED_UPSTREAM_BLOBS)
    observed["openbw/ui/ui.h"] = "0" * 40
    with pytest.raises(patch.SourcePatchHold, match="upstream blob drift"):
        patch.validate_upstream_blobs(observed)


def test_bridge_exposes_last_error_and_exact_file_not_found_discriminator():
    assert "uint32_t void_openbw_casc_last_error(void);" in patch.BRIDGE_HEADER_SOURCE
    assert "void_openbw_casc_error_is_file_not_found" in patch.BRIDGE_HEADER_SOURCE
    assert "GetCascError()" in patch.BRIDGE_CPP_SOURCE
    assert "ERROR_FILE_NOT_FOUND" in patch.BRIDGE_CPP_SOURCE


def test_bridge_download_capability_is_explicit_not_implicit():
    assert "int allow_download" in patch.BRIDGE_HEADER_SOURCE
    assert "allow_download ? CASC_FEATURE_ALLOW_DOWNLOAD : 0" in patch.BRIDGE_CPP_SOURCE


def test_data_loader_tries_modern_then_falls_back_only_on_file_not_found():
    result = patch.patch_openbw_data_loading(_data_loading_fixture())
    modern = result.index('a_string modern_name = filename + "ex";')
    classic = result.index("void_openbw_casc_file classic_file = nullptr;")
    discriminator = result.index("void_openbw_casc_error_is_file_not_found")
    assert modern < discriminator < classic
    assert "modern open failed" in result
    assert "classic open failed" in result
    assert 'filename += "ex"' not in result


def test_data_loader_canonicalizes_classic_u16_words_to_u32_bytes():
    result = patch.patch_openbw_data_loading(_data_loading_fixture())
    assert "classic.size() % 32" in result
    assert "dst.resize(classic.size() * 2);" in result
    assert "uint16_t value" in result
    assert "dst[out + 2] = 0;" in result
    assert "dst[out + 3] = 0;" in result


def test_data_loader_validates_modern_canonical_record_length():
    result = patch.patch_openbw_data_loading(_data_loading_fixture())
    assert "dst.size() % 64" in result
    assert "invalid VX4EX length" in result


def test_data_loader_adds_cstdlib_for_getenv():
    result = patch.patch_openbw_data_loading(_data_loading_fixture())
    assert "#include <cstdlib>" in result
    assert 'std::getenv("VOID_OPENBW_CASC_ALLOW_DOWNLOAD")' in result


def test_generated_loader_uses_real_tabs_not_literal_backslash_t():
    result = patch.patch_openbw_data_loading(_data_loading_fixture())
    assert "\\t" not in patch.DATA_LOADING_LOADER_NEW
    assert "\\t" not in result
    assert "\tvoid_openbw_casc_storage storage = nullptr;" in result


def test_ui_parser_uses_canonical_u32_records():
    result = patch.patch_openbw_ui(_ui_fixture())
    assert "std::array<uint32_t, 16> images" in result
    assert "vx4_data.size() % 64" in result
    assert "img.vx4.resize(vx4_data.size() / 64)" in result
    assert "vx4_r.get<uint32_t>()" in result
    assert "get<uint16_t>()" not in result


def test_cmake_patch_requires_explicit_bridge_roots():
    result = patch.patch_bwapi_openbwdata_cmake(_cmake_fixture())
    assert "VOID_CASC_BRIDGE_SOURCE_ROOT is required" in result
    assert "VOID_CASC_BRIDGE_BUILD_ROOT is required" in result
    assert "libvoid_openbw_casc_bridge.so" in result


def test_each_patch_anchor_must_exist_exactly_once():
    with pytest.raises(patch.SourcePatchHold, match="observed 0"):
        patch.patch_openbw_ui("no anchors")
    duplicate = _cmake_fixture() + patch.CMAKE_LINK_OLD
    with pytest.raises(patch.SourcePatchHold, match="observed 2"):
        patch.patch_bwapi_openbwdata_cmake(duplicate)


def test_bundle_is_deterministic_and_reports_all_source_identities():
    one = patch.build_source_patch_bundle(
        data_loading=_data_loading_fixture(),
        ui_header=_ui_fixture(),
        openbwdata_cmake=_cmake_fixture(),
    )
    two = patch.build_source_patch_bundle(
        data_loading=_data_loading_fixture(),
        ui_header=_ui_fixture(),
        openbwdata_cmake=_cmake_fixture(),
    )
    assert one == two
    identities = one.identities()
    assert len(identities) == 6
    assert all(len(value) == 40 for value in identities.values())


def test_production_builder_contains_no_dual_lobby_slot_promotion():
    joined = "\n".join(
        (
            patch.DATA_LOADING_LOADER_NEW,
            patch.BRIDGE_CPP_SOURCE,
            patch.BRIDGE_HEADER_SOURCE,
            patch.BRIDGE_CMAKE_SOURCE,
        )
    )
    assert "VOID_OPENBW_DUAL_PROMOTE_ONE_COMPUTER_SLOT" not in joined
    assert "controller_computer" not in joined
    assert "controller_open" not in joined
