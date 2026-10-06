from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_second_exhaustion_authorized_preservation_launcher_generation2
    as launcher,
)


def test_contract_is_inert_and_binds_authorized_preservation():
    out = (
        launcher
        .pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_contract()
    )

    assert out["authorized_preservation_launcher_implemented"] is True
    assert out["attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["authorization_text_sha256"] == (
        "3bc5742250626e26bea6885ca237d43371a11146f417bcaf395e3118a1127fb3"
    )
    assert out["authorization_text_bytes"] == 682
    assert out["exact_current_main_required"] is True
    assert out["exact_launcher_source_sha256_required"] is True
    assert out["explicit_launcher_confirmation_token_required"] is True
    assert out["reviewed_preservation_authorization_required"] is True
    assert out["reviewed_preservation_implementation_required"] is True
    assert out["preservation_delegation_exactly_once"] is True
    assert out["non_force_worktree_removal_required"] is True
    assert out["engine_before_source_removal_required"] is True
    assert out["atomic_archive_rename_required"] is True
    assert out["create_only_preservation_receipt_required"] is True
    assert out["first_v2_archive_mutation_authorized"] is False


def test_wrong_confirmation_fails_before_dependencies_or_host_work(monkeypatch):
    called = {"acceptance": 0, "self": 0, "main": 0, "preserve": 0}

    monkeypatch.setattr(
        launcher,
        "_acceptance",
        lambda: called.__setitem__("acceptance", called["acceptance"] + 1),
    )
    monkeypatch.setattr(
        launcher,
        "_verify_self",
        lambda value: called.__setitem__("self", called["self"] + 1),
    )
    monkeypatch.setattr(
        launcher.base_invocation,
        "_current_main",
        lambda value: called.__setitem__("main", called["main"] + 1),
    )
    monkeypatch.setattr(
        launcher.preservation,
        "preserve_pair06_v9_actionable_feedback_v2_second_exhaustion",
        lambda **kwargs: called.__setitem__("preserve", called["preserve"] + 1),
    )

    with pytest.raises(
        launcher.Pair06V9V2SecondExhaustionAuthorizedPreservationLauncherHold,
        match="AUTHORIZED_PRESERVATION_CONFIRMATION_REQUIRED",
    ):
        launcher.execute_authorized_preservation_once(
            expected_main_head="a" * 40,
            expected_launcher_source_sha256="b" * 64,
            launcher_confirm="wrong",
        )

    assert called == {"acceptance": 0, "self": 0, "main": 0, "preserve": 0}


def test_successful_launcher_delegates_preservation_exactly_once(monkeypatch):
    calls = []

    monkeypatch.setattr(
        launcher,
        "_acceptance",
        lambda: {"acceptance_review": {"ok": True}},
    )
    monkeypatch.setattr(
        launcher,
        "_verify_self",
        lambda value: "c" * 64,
    )
    monkeypatch.setattr(
        launcher.base_invocation,
        "_current_main",
        lambda value: {"head": value, "tree": "d" * 40},
    )

    def preserve(**kwargs):
        calls.append(kwargs)
        return {
            "attempt_marker_sha256": launcher.ATTEMPT_MARKER_SHA256,
            "attempt_consumed": True,
            "source_worktree_removed_non_force": True,
            "engine_worktree_removed_non_force": True,
            "archive_atomic_rename_performed": True,
            "attempt_marker_inode_preserved": True,
            "warm_start_inode_preserved": True,
            "trajectory_inode_preserved": True,
            "automatic_retry": False,
            "runtime_retry_authorized": False,
            "new_execution_request_opened": False,
            "game_execution_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
            "scheduler_mutation_performed": False,
            "preservation_receipt": "/tmp/preservation.json",
            "preservation_receipt_sha256": "e" * 64,
        }

    monkeypatch.setattr(
        launcher.preservation,
        "preserve_pair06_v9_actionable_feedback_v2_second_exhaustion",
        preserve,
    )

    out = launcher.execute_authorized_preservation_once(
        expected_main_head="a" * 40,
        expected_launcher_source_sha256="b" * 64,
        launcher_confirm=launcher.LAUNCHER_CONFIRM_TOKEN,
    )

    assert calls == [
        {
            "preservation_authorized": True,
            "confirm": launcher.preservation.CONFIRM_TOKEN,
        }
    ]
    assert out["launcher_source_sha256"] == "c" * 64
    assert out["launcher_main"]["head"] == "a" * 40
    assert out["single_authorized_preservation_consumed"] is True
    assert out["authorization_reusable_after_preservation"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_retry_authorized",
        "automatic_retry",
        "execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "preservation_performed_by_contract_inspection",
        "host_io_performed_by_contract_inspection",
        "authorization_reusable_after_preservation",
    ),
)
def test_contract_grants_no_runtime_or_follow_on_authority(field):
    out = (
        launcher
        .pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_contract()
    )
    assert out[field] is False


def test_contract_advances_only_to_exact_blob_review():
    out = (
        launcher
        .pair06_v9_v2_second_exhaustion_authorized_preservation_launcher_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_SECOND_EXHAUSTION_"
        "AUTHORIZED_PRESERVATION_LAUNCHER_SOURCE_BINDING_REVIEW_REQUIRED"
    )
