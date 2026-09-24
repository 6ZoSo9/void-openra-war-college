from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_readonly_observer_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_observer_source_and_test():
    out = review.pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    assert out["observer_git_blob"] == (
        "8cc439b59e31ca99e078c5bb96648826ac21edaf"
    )
    assert out["observer_source_sha256"] == (
        "e4006f0ba8959430dc0f8d83374c6743813a1956f7b31b69a9d361ee01e719e4"
    )
    assert out["observer_test_git_blob"] == (
        "af6e5e8def82a5484e83eecb68a5cba99b0e69b5"
    )
    assert out["observer_test_sha256"] == (
        "d54eac1e08b856c2ef734ab29e29d9d9252499ac22b1e22812848c840c33564b"
    )


def test_review_pins_corrected_admission_review_identity():
    out = review.pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    assert out["admission_review_git_blob"] == (
        "00876b15ce0317d548b14e98dd5c3a480f11c84f"
    )
    assert out["admission_review_source_sha256"] == (
        "3991a1bcb2ffe855495cb983c3a4540f947d2079d60c7bf8fd1283b8a6ca06ba"
    )


def test_review_preserves_exact_readonly_observer_surface():
    out = review.pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    assert out["pair06_v8_preclaim_gpu_readonly_observer_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["gpu_index"] == 0
    assert out["nvidia_smi_path"] == "/usr/bin/nvidia-smi"
    assert out["device_query"] == review.observer.DEVICE_QUERY
    assert out["process_query"] == review.observer.PROCESS_QUERY
    assert out["observation_requires_explicit_authority"] is True
    assert out["automatic_command_runner_selection"] is False


def test_review_remains_nonmutating_and_nonauthorizing():
    out = review.pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    for field in (
        "observer_grants_gpu_admission",
        "process_signal_implemented",
        "process_termination_implemented",
        "attempt_marker_creation_implemented",
        "runtime_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
        "retry_authorized",
        "execution_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_precision_observation():
    out = review.pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_PRECLAIM_GPU_PRECISION_OBSERVATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PRECLAIM_GPU_PRECISION_OBSERVATION_REQUIRED"
    )


def test_runtime_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PreclaimGpuReadonlyObserverReviewHold,
        match="PAIR06_V8_PRECLAIM_GPU_PRECISION_OBSERVATION_REQUIRED",
    ):
        review.observe_or_execute()
