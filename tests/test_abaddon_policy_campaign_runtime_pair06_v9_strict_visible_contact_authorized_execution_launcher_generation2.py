from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_authorized_execution_launcher_generation2
    as launcher,
)


def test_contract_binds_exact_authorization_and_runtime_sources():
    out = launcher.pair06_v9_authorized_execution_launcher_contract()

    assert out["pair06_v9_authorized_execution_launcher_implemented"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["policy_id"] == (
        "pair06-v9-strict-visible-contact-envelope-v1"
    )
    assert out["acceptance_git_blob"] == (
        "0b72636735120e8ebf7df101b05c46d41c4ba2f0"
    )
    assert out["acceptance_review_git_blob"] == (
        "1bdba57d92a382d9ed0dd7b5d4134b284af8837c"
    )
    assert out["request_review_git_blob"] == (
        "8565d587e57335a2a30940effa40713ae6a7315a"
    )
    assert out["operator_git_blob"] == (
        "d2e097bfd5b3afb7cd7e0581c2496777c89d43de"
    )
    assert out["operator_review_git_blob"] == (
        "7c797d9e3c045d92e64b0f9ff0910563c4662cd3"
    )


def test_contract_preserves_single_attempt_and_gpu_gate():
    out = launcher.pair06_v9_authorized_execution_launcher_contract()

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_v9_evidence_namespace_required"] is True
    assert out["authorization_reusable_after_attempt_claim"] is False


def test_contract_inspection_is_inert():
    out = launcher.pair06_v9_authorized_execution_launcher_contract()

    assert out["contract_inspection_performs_host_io"] is False
    assert out["contract_inspection_creates_attempt_marker"] is False
    assert out["contract_inspection_loads_model"] is False
    assert out["contract_inspection_runs_inference"] is False
    assert out["contract_inspection_executes_game"] is False


def test_wrong_launcher_confirmation_holds_before_runtime_identity(monkeypatch):
    touched = {"identity": False}

    def forbidden_identity():
        touched["identity"] = True
        raise AssertionError("runtime identity must not be queried")

    monkeypatch.setattr(launcher, "_runtime_identity", forbidden_identity)

    with pytest.raises(
        launcher.Pair06V9AuthorizedExecutionLauncherHold,
        match="LAUNCH_CONFIRMATION_REQUIRED",
    ):
        launcher.execute_authorized_pair06_v9_once(
            launcher_confirm="wrong",
        )

    assert touched["identity"] is False


def test_authorized_launcher_delegates_exactly_once_to_reviewed_operator(
    monkeypatch,
):
    calls = []

    monkeypatch.setattr(
        launcher,
        "_runtime_identity",
        lambda: {
            "main_head": "a" * 40,
            "operator_source_sha256": "b" * 64,
        },
    )

    def fake_execute(**kwargs):
        calls.append(kwargs)
        return {
            "pair_slot": 6,
            "arm": "baseline",
            "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
            "automatic_retry": False,
            "attempt_marker_sha256": "c" * 64,
            "result_file_sha256": "d" * 64,
            "closeout_file_sha256": "e" * 64,
        }

    monkeypatch.setattr(
        launcher.operator,
        "execute_pair06_v9_strict_visible_contact_baseline_game",
        fake_execute,
    )

    result = launcher.execute_authorized_pair06_v9_once(
        launcher_confirm=launcher.LAUNCH_CONFIRM_TOKEN,
    )

    assert len(calls) == 1
    assert calls[0]["expected_main_head"] == "a" * 40
    assert calls[0]["expected_operator_source_sha256"] == "b" * 64
    assert calls[0]["execution_authorization_accepted"] is True
    assert calls[0]["policy_activation_authorization_accepted"] is True
    assert calls[0]["execution_confirm"] == launcher.operator.EXECUTION_CONFIRM_TOKEN
    assert calls[0]["policy_confirm"] == launcher.operator.POLICY_CONFIRM_TOKEN
    assert result["single_authorized_attempt_consumed"] is True
    assert result["attempt_marker_sha256"] == "c" * 64


@pytest.mark.parametrize(
    "field",
    (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_launcher_grants_no_extra_authority(field):
    out = launcher.pair06_v9_authorized_execution_launcher_contract()
    assert out[field] is False


def test_launcher_advances_only_to_host_execution():
    out = launcher.pair06_v9_authorized_execution_launcher_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "explicit_launcher_confirmation",
        "exact_current_main_and_canonical_blobs",
        "fresh_preclaim_gpu_admission",
        "fresh_create_only_v9_attempt_marker",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_HOST_EXECUTION_REQUIRED"
    )
