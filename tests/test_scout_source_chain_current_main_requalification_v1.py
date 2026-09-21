from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "config/war-college/scout-source-chain-current-main-requalification-v1.json"


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def _receipt() -> dict:
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_requalification_lineage_and_base_are_exact():
    row = _receipt()
    assert row["schema"] == "void.war-college.scout-source-chain-current-main-requalification.v1"
    assert row["base_main_commit"] == "3703eaddc7e95f917de72747cc3e6248c78fb295"
    assert row["historical_bound_main_commit"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert row["historical_main_binding_preserved"] is True
    assert row["current_main_dependencies_match_historical_binding"] is True
    assert row["payload_bytes_recomposed_without_rewrite"] is True
    assert row["source_pr_lineage"] == [
        {"pr_number": 191, "head_sha": "1e9fd02bb8120628e7daf4208fd3ee51f7dd140e", "file_count": 23},
        {"pr_number": 192, "head_sha": "3213b6cbe3fec94f90c0ccb13d10eab8482e2245", "file_count": 16},
        {"pr_number": 193, "head_sha": "2fe34494a35bf5dcfc1aedda3d8096e1b10b9b12", "file_count": 4},
        {"pr_number": 194, "head_sha": "13a4c64783c0380b6f969ce6d10fddd0e18df1e8", "file_count": 4},
    ]


def test_all_consolidated_payload_blobs_match_source_pr_bytes():
    row = _receipt()
    assert len(row["payload_blobs"]) == 47
    for relative, expected_blob in row["payload_blobs"].items():
        path = ROOT / relative
        assert path.is_file(), relative
        assert _git_blob_sha1(path.read_bytes()) == expected_blob, relative


def test_historical_bound_dependencies_are_unchanged_on_requalified_main():
    row = _receipt()
    assert len(row["dependency_blobs"]) == 8
    for relative, expected_blob in row["dependency_blobs"].items():
        path = ROOT / relative
        assert path.is_file(), relative
        assert _git_blob_sha1(path.read_bytes()) == expected_blob, relative


def test_requalification_does_not_rewrite_historical_main_binding():
    launcher = (
        ROOT
        / "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py"
    ).read_text(encoding="utf-8")
    review = (
        ROOT
        / "openra_env/learning/abaddon_scout_external_launcher_contract_review_v1.py"
    ).read_text(encoding="utf-8")
    historical = _receipt()["historical_bound_main_commit"]
    assert f'MAIN_HEAD = "{historical}"' in launcher
    assert f'BOUND_MAIN_HEAD = "{historical}"' in review


def test_requalification_grants_no_runtime_or_experiment_authority():
    boundaries = _receipt()["boundaries"]
    assert boundaries == {
        "game_execution": False,
        "model_execution": False,
        "runtime_activation": False,
        "attempt_consumption": False,
        "training": False,
        "policy_promotion": False,
        "deployment": False,
        "void_chain_mutation": False,
        "wallet_or_funds_action": False,
    }


def test_canary_chain_still_leaves_future_accepted_main_unresolved():
    source = (
        ROOT
        / "openra_env/learning/abaddon_scout_repair_canary_source_design_v1.py"
    ).read_text(encoding="utf-8")
    opponent_review = (
        ROOT
        / "openra_env/learning/abaddon_scout_canary_opponent_source_binding_review_v1.py"
    ).read_text(encoding="utf-8")
    assert '"accepted_main_head_with_repair": None' in source
    assert '"accepted_main_head_with_repair": None' in opponent_review
