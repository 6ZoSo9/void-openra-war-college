from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_host_preflight_generation2
    as preflight,
)

HEAD = "a" * 40
HOLD = preflight.V2R13Pair09CandidateHostPreflightHold


def fake_snapshot():
    rows = {}
    for key, exists in preflight.EXPECTED_ARM_LAYOUT.items():
        pair_text, arm = key.split(":")
        rows[key] = {
            "path": str(
                preflight.ISOLATED_ROOT
                / "generation2"
                / f"pair-{int(pair_text):02d}"
                / arm
            ),
            "exists": exists,
        }
    return {
        "expected_main_head": HEAD,
        "isolated_workdir": {
            "root": str(preflight.ISOLATED_ROOT),
            "authorized_arm_paths": rows,
        },
    }


def install_fake_host(monkeypatch):
    snapshot = fake_snapshot()
    monkeypatch.setattr(
        preflight,
        "_collect_host_snapshot",
        lambda expected_main_head: deepcopy(snapshot),
    )
    monkeypatch.setattr(
        preflight,
        "_arm_census",
        lambda: deepcopy(preflight.EXPECTED_ARM_LAYOUT),
    )

    def read(relative, digest, maximum):
        return {
            "path": str(preflight.ISOLATED_ROOT / relative),
            "sha256": digest,
            "bytes": min(maximum, 100),
        }

    monkeypatch.setattr(preflight, "_read_preserved_file", read)

    class Legacy:
        @staticmethod
        def validate_host_preflight_snapshot(projected):
            return {
                "host_preflight_green": True,
                "snapshot_sha256": preflight._digest(projected),
            }

    monkeypatch.setattr(preflight, "_legacy_validator", lambda: Legacy())
    return snapshot


def test_contract_is_source_only_and_non_authorizing():
    out = preflight.pair09_candidate_host_preflight_contract()
    assert out["pair09_candidate_host_preflight_implemented"] is True
    assert out["pair09_candidate_host_preflight_reviewed"] is False
    assert out["read_only_host_collection"] is True
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["pair03_baseline_preservation_required"] is True
    assert out["pair03_candidate_preservation_required"] is True
    assert out["pair09_baseline_preservation_required"] is True
    assert out["pair09_candidate_absence_required"] is True
    assert out["held_out_pair15_absence_required"] is True
    assert out["single_use_attempt_consumed"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["runtime_started"] is False


def test_collect_accepts_exact_current_layout_and_preserves_evidence(monkeypatch):
    snapshot = install_fake_host(monkeypatch)
    out = preflight.collect_pair09_candidate_host_preflight(
        expected_main_head=HEAD,
        confirm=preflight.CONFIRM_TOKEN,
    )
    assert out["pair09_candidate_host_conditions_validated"] is True
    assert out["expected_main_head"] == HEAD
    assert out["observed_host_snapshot"] == snapshot
    assert out["observed_host_snapshot_sha256"] == preflight._digest(snapshot)
    assert out["observed_arm_layout"] == preflight.EXPECTED_ARM_LAYOUT
    assert len(out["preserved_evidence"]) == len(preflight.PRESERVED_FILES)
    assert out["pair03_baseline_preserved"] is True
    assert out["pair03_candidate_preserved"] is True
    assert out["pair09_baseline_preserved"] is True
    assert out["pair09_candidate_absent"] is True
    assert out["held_out_pair15_absent"] is True
    assert out["legacy_structural_projection_is_host_observation"] is False
    assert out["legacy_runtime_authority_inherited"] is False
    assert out["single_use_attempt_consumed"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["pair09_candidate_execution_performed"] is False


def test_projection_hides_only_completed_arms(monkeypatch):
    snapshot = install_fake_host(monkeypatch)
    seen = {}

    class Legacy:
        @staticmethod
        def validate_host_preflight_snapshot(projected):
            seen["projection"] = deepcopy(projected)
            return {
                "host_preflight_green": True,
                "snapshot_sha256": preflight._digest(projected),
            }

    monkeypatch.setattr(preflight, "_legacy_validator", lambda: Legacy())
    preflight.collect_pair09_candidate_host_preflight(
        expected_main_head=HEAD,
        confirm=preflight.CONFIRM_TOKEN,
    )
    projected = seen["projection"]
    rows = projected["isolated_workdir"]["authorized_arm_paths"]
    assert all(row["exists"] is False for row in rows.values())
    assert snapshot["isolated_workdir"]["authorized_arm_paths"]["3:baseline"]["exists"] is True
    assert snapshot["isolated_workdir"]["authorized_arm_paths"]["3:candidate"]["exists"] is True
    assert snapshot["isolated_workdir"]["authorized_arm_paths"]["9:baseline"]["exists"] is True


@pytest.mark.parametrize(
    "confirm",
    ["", True, "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR09_CANDIDATE_ONCE"],
)
def test_bad_confirmation_stops_before_host_collection(monkeypatch, confirm):
    def forbidden(*args, **kwargs):
        raise AssertionError("host collection reached")

    monkeypatch.setattr(preflight, "_collect_host_snapshot", forbidden)
    with pytest.raises(HOLD, match="CONFIRMATION_REQUIRED"):
        preflight.collect_pair09_candidate_host_preflight(
            expected_main_head=HEAD,
            confirm=confirm,
        )


def test_candidate_present_is_rejected(monkeypatch):
    snapshot = fake_snapshot()
    snapshot["isolated_workdir"]["authorized_arm_paths"]["9:candidate"]["exists"] = True
    monkeypatch.setattr(
        preflight,
        "_collect_host_snapshot",
        lambda expected_main_head: snapshot,
    )
    with pytest.raises(HOLD, match="ARM_LAYOUT_HOLD"):
        preflight.collect_pair09_candidate_host_preflight(
            expected_main_head=HEAD,
            confirm=preflight.CONFIRM_TOKEN,
        )


def test_layout_change_during_collection_is_rejected(monkeypatch):
    install_fake_host(monkeypatch)
    calls = 0

    def census():
        nonlocal calls
        calls += 1
        result = deepcopy(preflight.EXPECTED_ARM_LAYOUT)
        if calls > 1:
            result["9:candidate"] = True
        return result

    monkeypatch.setattr(preflight, "_arm_census", census)
    with pytest.raises(HOLD, match="LAYOUT_CHANGED"):
        preflight.collect_pair09_candidate_host_preflight(
            expected_main_head=HEAD,
            confirm=preflight.CONFIRM_TOKEN,
        )


def test_preserved_evidence_digest_failure_is_terminal(monkeypatch):
    install_fake_host(monkeypatch)

    def fail(*args):
        raise HOLD("PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_DIGEST_MISMATCH")

    monkeypatch.setattr(preflight, "_read_preserved_file", fail)
    with pytest.raises(HOLD, match="EVIDENCE_DIGEST_MISMATCH"):
        preflight.collect_pair09_candidate_host_preflight(
            expected_main_head=HEAD,
            confirm=preflight.CONFIRM_TOKEN,
        )


def test_collect_never_grants_runtime_or_followon_authority(monkeypatch):
    install_fake_host(monkeypatch)
    out = preflight.collect_pair09_candidate_host_preflight(
        expected_main_head=HEAD,
        confirm=preflight.CONFIRM_TOKEN,
    )
    for field in (
        "single_use_attempt_consumed",
        "pair09_candidate_execution_authorized",
        "pair09_candidate_execution_performed",
        "runtime_started",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
