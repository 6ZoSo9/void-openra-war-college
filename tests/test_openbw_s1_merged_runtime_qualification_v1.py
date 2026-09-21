from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "config/war-college/openbw-s1-merged-builder-runtime-qualification-v1.json"
BUILDER = ROOT / "openra_env/learning/openbw_s1_source_patch_v1.py"


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def test_runtime_qualification_receipt_payload_digest_is_stable():
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))
    expected = row.pop("evidence_payload_sha256")
    raw = json.dumps(
        row,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    assert hashlib.sha256(raw).hexdigest() == expected


def test_runtime_qualification_binds_merged_builder_and_upstream_pins():
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert row["merged_main_commit"] == "6ffee13a6b8b26ed70cbb55aed3df5e9d7d20c73"
    assert _git_blob_sha1(BUILDER.read_bytes()) == row["source_builder_blob"]
    assert row["upstream"] == {
        "openbw": "4b046d5f65302b10cb0a745f0fecd37ec85b20a8",
        "bwapi": "48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2",
        "casclib": "2a280f5a231966dc5d1b534978dd9f9f04a374cd",
    }


def test_single_runtime_green_and_bounded():
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))["single_runtime"]
    assert row["runtime_returncode"] == 0
    assert row["frames_observed"] == [120, 240, 360]
    assert row["leave_requested_frame"] == 480
    assert row["end_frame"] == 481
    assert row["cache_growth_bytes"] == 0
    assert row["peak_observed_cache_growth_bytes"] == 0
    assert row["casc_allow_download"] is False
    assert row["complete_map_information"] is False
    assert row["user_input"] is False
    assert row["model_execution"] is False
    assert row["training"] is False
    assert row["terminal"].endswith("_GREEN")


def test_dual_runtime_green_synced_and_bounded():
    row = json.loads(RECEIPT.read_text(encoding="utf-8"))["dual_runtime"]
    assert row["runtime_returncodes"] == [0, 0]
    assert row["instance_a_leave_requested_frame"] == 480
    assert row["instance_a_end_frame"] == 481
    assert row["instance_b_named_peer_departure_frame"] == 483
    assert row["instance_b_leave_requested_frame"] == 483
    assert row["instance_b_end_frame"] == 484
    assert row["cache_growth_bytes"] == 0
    assert row["peak_observed_cache_growth_bytes"] == 0
    assert row["two_open_human_lobby_slots_proven"] is True
    assert row["two_instance_local_sync_proven"] is True
    assert row["named_peer_departure_sync_proven"] is True
    assert row["bounded_peer_followup_exit_proven"] is True
    assert row["bounded_dual_game_lifecycle_proven"] is True
    assert row["merged_builder_dual_runtime_proven"] is True
    assert row["production_builder_contains_lobby_promotion"] is False
    assert row["transient_test_only_lobby_slot_promotion"] is True
    assert row["terminal"].endswith("_GREEN")


def test_runtime_qualification_does_not_promote_test_lobby_patch():
    source = BUILDER.read_text(encoding="utf-8")
    assert "VOID_OPENBW_DUAL_PROMOTE_ONE_COMPUTER_SLOT" not in source
    assert "controller_computer" not in source
    assert "controller_open" not in source
    boundaries = json.loads(RECEIPT.read_text(encoding="utf-8"))["boundaries"]
    assert boundaries == {
        "production_builder_modified_by_runtime_qualification": False,
        "war_college_checkout_mutated": False,
        "network_payload_download_allowed": False,
        "battle_net_execution": False,
        "starcraft_binary_execution": False,
        "policy_promotion": False,
        "deployment": False,
        "wallet_or_funds_action": False,
    }
