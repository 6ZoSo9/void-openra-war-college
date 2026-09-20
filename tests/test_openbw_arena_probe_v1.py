import pytest

from openra_env.learning import openbw_arena_probe_v1 as probe


def test_contract_is_pinned_external_build_only():
    value = probe.openbw_arena_probe_contract()
    assert value["schema"] == probe.SCHEMA
    assert value["upstream"]["openbw"]["commit"] == "4b046d5f65302b10cb0a745f0fecd37ec85b20a8"
    assert value["upstream"]["bwapi"]["commit"] == "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2"
    assert value["integration"]["strategy"] == "external_pinned_dependency"
    assert value["integration"]["vendor_openbw_source_into_war_college"] is False
    assert value["integration"]["vendor_bwapi_source_into_war_college"] is False
    assert value["integration"]["openbw_core_license_clarity_required_before_redistribution"] is True
    assert value["integration"]["headless_build"] is True
    assert value["integration"]["openbw_ui_enabled"] is False
    assert value["integration"]["build_only"] is True
    assert value["integration"]["launcher_execution"] is False


def test_contract_does_not_bundle_or_fetch_starcraft_assets():
    value = probe.openbw_arena_probe_contract()
    assert value["runtime"]["required_external_game_data"] == (
        "Stardat.mpq",
        "Broodat.mpq",
        "Patch_rt.mpq",
    )
    assert value["runtime"]["game_assets_bundled"] is False
    assert value["runtime"]["game_assets_downloaded_by_probe"] is False
    assert value["runtime"]["built_in_computer_player_available"] is False


def test_contract_grants_no_runtime_or_training_authority():
    value = probe.openbw_arena_probe_contract()
    assert all(v is False for v in value["authority"].values())
    with pytest.raises(probe.OpenBWArenaProbeHold):
        probe.authorize_or_execute()


def test_build_receipt_accepts_only_build_without_execution():
    receipt = {
        "schema": probe.RECEIPT_SCHEMA,
        "openbw_commit": probe.OPENBW["commit"],
        "bwapi_commit": probe.OPENBW_BWAPI["commit"],
        "headless_configure_passed": True,
        "bwapilauncher_build_passed": True,
        "launcher_exists": True,
        "launcher_executed": False,
        "game_assets_read": False,
        "game_assets_downloaded": False,
        "game_session_created": False,
        "model_executed": False,
        "training_performed": False,
    }
    result = probe.validate_headless_build_receipt(receipt)
    assert result["build_probe_valid"] is True
    assert result["runtime_authorized"] is False


@pytest.mark.parametrize(
    "field",
    (
        "launcher_executed",
        "game_assets_read",
        "game_assets_downloaded",
        "game_session_created",
        "model_executed",
        "training_performed",
    ),
)
def test_build_receipt_rejects_runtime_side_effects(field):
    receipt = {
        "schema": probe.RECEIPT_SCHEMA,
        "openbw_commit": probe.OPENBW["commit"],
        "bwapi_commit": probe.OPENBW_BWAPI["commit"],
        "headless_configure_passed": True,
        "bwapilauncher_build_passed": True,
        "launcher_exists": True,
        "launcher_executed": False,
        "game_assets_read": False,
        "game_assets_downloaded": False,
        "game_session_created": False,
        "model_executed": False,
        "training_performed": False,
    }
    receipt[field] = True
    with pytest.raises(probe.OpenBWArenaProbeHold):
        probe.validate_headless_build_receipt(receipt)


def test_gcc13_compatibility_patch_is_exact_and_transient():
    value = probe.openbw_arena_probe_contract()
    patch = value["integration"]["compatibility_patch"]
    assert patch["upstream_pr"] == "OpenBW/bwapi#16"
    assert patch["upstream_patch_commit"] == "04eb2f7f88174808ba46e3a53cc2a82f85da57ad"
    assert patch["preimage_git_blob_sha1"] == "ccf26f5e77693e5f682ff27f7d3185ad08b6c7b6"
    assert patch["postimage_git_blob_sha1"] == "debb572f6eb23c44ff1096bf8ba3ebea5da3ac7b"
    assert value["integration"]["compatibility_patch_upstream_open"] is True
    assert value["integration"]["compatibility_patch_transient_only"] is True
