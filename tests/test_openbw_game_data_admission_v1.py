import hashlib
import os
from pathlib import Path

import pytest

from scripts import openbw_game_data_admission_v1 as admission
from openra_env.learning import openbw_neutral_duel_harness_v1 as harness


def _fixture(root: Path) -> None:
    (root / "Stardat.mpq").write_bytes(b"stardat")
    (root / "Broodat.mpq").write_bytes(b"broodat")
    (root / "Patch_rt.mpq").write_bytes(b"patch")
    maps = root / "maps"
    maps.mkdir()
    (maps / "smoke.scx").write_bytes(b"map-bytes")


def test_admission_hashes_only_explicit_assets_and_grants_no_authority(tmp_path):
    _fixture(tmp_path)
    receipt = admission.admit_game_data(
        game_root=tmp_path,
        map_relative="maps/smoke.scx",
        confirm=admission.CONFIRMATION,
    )
    assert receipt["schema"] == harness.RUNTIME_ADMISSION_SCHEMA
    assert receipt["game_data_sha256"]["Stardat.mpq"] == hashlib.sha256(b"stardat").hexdigest()
    assert receipt["game_data_sha256"]["Broodat.mpq"] == hashlib.sha256(b"broodat").hexdigest()
    assert receipt["game_data_sha256"]["Patch_rt.mpq"] == hashlib.sha256(b"patch").hexdigest()
    assert receipt["map_sha256"] == hashlib.sha256(b"map-bytes").hexdigest()
    assert receipt["files_copied"] is False
    assert receipt["files_modified"] is False
    assert receipt["game_launched"] is False
    assert receipt["runtime_authorized"] is False
    assert receipt["game_execution_authorized"] is False


def test_confirmation_is_explicit(tmp_path):
    _fixture(tmp_path)
    with pytest.raises(admission.OpenBWGameDataAdmissionHold):
        admission.admit_game_data(
            game_root=tmp_path,
            map_relative="maps/smoke.scx",
            confirm="",
        )


@pytest.mark.parametrize("value", ("/absolute.scx", "../escape.scx", "maps/../escape.scx"))
def test_map_path_must_stay_beneath_explicit_root(tmp_path, value):
    _fixture(tmp_path)
    with pytest.raises(admission.OpenBWGameDataAdmissionHold):
        admission.admit_game_data(
            game_root=tmp_path,
            map_relative=value,
            confirm=admission.CONFIRMATION,
        )


def test_final_file_symlink_is_rejected(tmp_path):
    _fixture(tmp_path)
    target = tmp_path / "real.mpq"
    target.write_bytes(b"replacement")
    (tmp_path / "Stardat.mpq").unlink()
    (tmp_path / "Stardat.mpq").symlink_to(target)
    with pytest.raises(admission.OpenBWGameDataAdmissionHold):
        admission.admit_game_data(
            game_root=tmp_path,
            map_relative="maps/smoke.scx",
            confirm=admission.CONFIRMATION,
        )


def test_parent_directory_symlink_is_rejected(tmp_path):
    _fixture(tmp_path)
    real_maps = tmp_path / "real-maps"
    real_maps.mkdir()
    (real_maps / "smoke.scx").write_bytes(b"other-map")
    (tmp_path / "maps" / "smoke.scx").unlink()
    (tmp_path / "maps").rmdir()
    (tmp_path / "maps").symlink_to(real_maps, target_is_directory=True)
    with pytest.raises(admission.OpenBWGameDataAdmissionHold):
        admission.admit_game_data(
            game_root=tmp_path,
            map_relative="maps/smoke.scx",
            confirm=admission.CONFIRMATION,
        )


def test_source_does_not_scan_copy_or_launch():
    source = Path(admission.__file__).read_text(encoding="utf-8")
    for forbidden in (
        "os.walk",
        ".rglob(",
        ".glob(",
        "shutil.copy",
        "subprocess",
        "BWAPILauncher",
        "socket.",
    ):
        assert forbidden not in source
