from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_generation2
    as preflight,
)


EXPECTED_LAYOUT = {
    "3:baseline": True,
    "3:candidate": True,
    "9:baseline": False,
    "9:candidate": False,
    "15:baseline": False,
    "15:candidate": False,
}


def _snapshot(head: str):
    rows = {}
    for key, exists in EXPECTED_LAYOUT.items():
        pair, arm = key.split(":")
        rows[key] = {
            "path": (
                f"{preflight.ISOLATED_ROOT}/generation2/"
                f"pair-{int(pair):02d}/{arm}"
            ),
            "exists": exists,
        }
    return {
        "expected_main_head": head,
        "isolated_workdir": {
            "root": str(preflight.ISOLATED_ROOT),
            "authorized_arm_paths": rows,
        },
    }


class _Legacy:
    @staticmethod
    def validate_host_preflight_snapshot(snapshot):
        expected = deepcopy(snapshot)
        for key in expected["isolated_workdir"]["authorized_arm_paths"]:
            assert (
                expected["isolated_workdir"]["authorized_arm_paths"][key]["exists"]
                is False
            )
        return {
            "host_preflight_green": True,
            "snapshot_sha256": preflight._digest(snapshot),
        }


def test_contract_requires_preserved_pair03_and_absent_pair09_pair15():
    out = preflight.pair09_baseline_host_preflight_contract()
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["read_only_host_collection_implemented"] is True
    assert out["pair03_baseline_preservation_required"] is True
    assert out["pair03_candidate_preservation_required"] is True
    assert out["pair09_baseline_absence_required"] is True
    assert out["pair09_candidate_absence_required"] is True
    assert out["held_out_pair15_absence_required"] is True


def test_contract_inherits_no_runtime_authority():
    out = preflight.pair09_baseline_host_preflight_contract()
    assert out["legacy_structural_projection_is_host_observation"] is False
    assert out["legacy_runtime_authority_inherited"] is False
    assert out["single_use_attempt_consumed"] is False
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["pair09_baseline_execution_performed"] is False
    assert out["runtime_started"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_source_references_are_exact():
    out = preflight.pair09_baseline_host_preflight_contract()
    assert out["source_references"] == {
        "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_source_binding_review_generation2.py":
            "7770954472ebd9abd7f51020ed352dea9adb6df2",
        "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2.py":
            "0ae27981a08b27083b235ae4807705c88da259a1",
        "tools/abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2.py":
            "62d8a906ea41138b5443ba3bf96799b6e430b5be",
    }


def test_synthetic_collection_preserves_real_snapshot_and_projects_only_for_legacy(
    monkeypatch,
):
    head = "a" * 40
    real = _snapshot(head)

    monkeypatch.setattr(
        preflight,
        "_collect_host_snapshot",
        lambda expected_main_head: deepcopy(real),
    )
    monkeypatch.setattr(
        preflight,
        "_arm_layout",
        lambda: deepcopy(EXPECTED_LAYOUT),
    )
    monkeypatch.setattr(
        preflight,
        "_legacy_validator",
        lambda: _Legacy,
    )
    monkeypatch.setattr(
        preflight,
        "_read_preserved_file",
        lambda relative, digest, maximum: {
            "path": str(preflight.ISOLATED_ROOT / relative),
            "sha256": digest,
            "bytes": min(maximum, 123),
        },
    )

    out = preflight.collect_pair09_baseline_host_preflight(
        expected_main_head=head,
        confirm=preflight.CONFIRM_TOKEN,
    )

    assert out["pair09_baseline_host_conditions_validated"] is True
    assert out["observed_host_snapshot"] == real
    assert out["observed_host_snapshot_sha256"] == preflight._digest(real)
    assert out["observed_arm_layout"] == EXPECTED_LAYOUT
    assert out["pair03_baseline_preserved"] is True
    assert out["pair03_candidate_preserved"] is True
    assert out["pair09_baseline_absent"] is True
    assert out["pair09_candidate_absent"] is True
    assert out["held_out_pair15_absent"] is True
    assert out["legacy_structural_projection_is_host_observation"] is False
    assert out["legacy_runtime_authority_inherited"] is False
    assert out["single_use_attempt_consumed"] is False
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["runtime_started"] is False
    assert len(out["pair03_preserved_evidence"]) == len(
        preflight.PRESERVED_FILES
    )


def test_snapshot_layout_drift_is_rejected(monkeypatch):
    head = "a" * 40
    bad = _snapshot(head)
    bad["isolated_workdir"]["authorized_arm_paths"]["9:baseline"][
        "exists"
    ] = True

    monkeypatch.setattr(
        preflight,
        "_collect_host_snapshot",
        lambda expected_main_head: deepcopy(bad),
    )
    monkeypatch.setattr(
        preflight,
        "_arm_layout",
        lambda: deepcopy(EXPECTED_LAYOUT),
    )

    with pytest.raises(
        preflight.V2R13Pair09BaselineHostPreflightHold,
        match="PAIR09_PREFLIGHT_SNAPSHOT_LAYOUT_HOLD",
    ):
        preflight.collect_pair09_baseline_host_preflight(
            expected_main_head=head,
            confirm=preflight.CONFIRM_TOKEN,
        )


def test_wrong_confirmation_rejected_before_collection(monkeypatch):
    called = False

    def collect(_):
        nonlocal called
        called = True
        return {}

    monkeypatch.setattr(preflight, "_collect_host_snapshot", collect)
    with pytest.raises(
        preflight.V2R13Pair09BaselineHostPreflightHold,
        match="PAIR09_PREFLIGHT_READONLY_CONFIRMATION_REQUIRED",
    ):
        preflight.collect_pair09_baseline_host_preflight(
            expected_main_head="a" * 40,
            confirm="wrong",
        )
    assert called is False


def test_preflight_advances_only_to_separate_source_review():
    out = preflight.pair09_baseline_host_preflight_contract()
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_HOST_PREFLIGHT_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )
