from __future__ import annotations

import pytest

from openra_env.learning import (
    apollyon_xiphos_candidate_training_host_preflight_generation2 as preflight,
)


def _green_git(expected: str) -> dict:
    return {
        "repository_present": True,
        "expected_main_head": expected,
        "branch": "refs/heads/main",
        "main_branch": True,
        "head": expected,
        "tree": "b" * 40,
        "tracked_clean": True,
        "matches_expected_main": True,
    }


def _green_gpu() -> dict:
    return {
        "query_success": True,
        "gpus": [
            {
                "index": 0,
                "name": "GPU",
                "uuid": "GPU-0",
                "memory_total_mib": 16384,
                "memory_free_mib": 16000,
                "driver_version": "1",
            }
        ],
        "compute_processes": [],
        "cuda0_compute_process_count": 0,
        "cuda0_admitted": True,
    }


def _green_disk() -> dict:
    return {
        "query_success": True,
        "probe_path": "/home/zoso",
        "free_bytes": 100 * 1024**3,
        "total_bytes": 200 * 1024**3,
    }


def _green_service() -> dict:
    return {
        "systemctl_present": True,
        "user_manager_query_success": True,
        "user_manager_state": "running",
        "external_service_control_available": True,
    }



def test_readonly_command_env_binds_external_user_bus_without_inheriting_shell(monkeypatch):
    monkeypatch.setattr(preflight.os, "geteuid", lambda: 1000)
    monkeypatch.setenv("VOID_UNTRUSTED_TEST_VALUE", "must-not-leak")

    env = preflight._readonly_command_env()

    assert env["XDG_RUNTIME_DIR"] == "/run/user/1000"
    assert env["DBUS_SESSION_BUS_ADDRESS"] == "unix:path=/run/user/1000/bus"
    assert env["PATH"] == "/usr/local/bin:/usr/bin:/bin"
    assert env["GIT_TERMINAL_PROMPT"] == "0"
    assert "VOID_UNTRUSTED_TEST_VALUE" not in env


def test_readonly_command_env_refuses_root(monkeypatch):
    monkeypatch.setattr(preflight.os, "geteuid", lambda: 0)
    with pytest.raises(
        preflight.ApollyonXiphosCandidateTrainingHostPreflightHold,
        match="UNPRIVILEGED_USER_REQUIRED",
    ):
        preflight._readonly_command_env()

def test_contract_is_read_only_and_grants_no_training_authority():
    out = preflight.apollyon_xiphos_candidate_training_host_preflight_contract()
    assert out["read_only_host_collection_implemented"] is True
    assert out["preferred_candidate_training_host"] == "Xiphos"
    assert out["expected_host_normalized"] == "xiphos"
    assert out["shutdown_control_external_to_trainable_model"] is True
    assert out["automatic_promotion_allowed"] is False

    for field in (
        "network_access_by_collection",
        "git_fetch_by_collection",
        "git_checkout_by_collection",
        "git_reset_by_collection",
        "directory_creation_by_collection",
        "package_install_by_collection",
        "service_mutation_by_collection",
        "process_signal_by_collection",
        "model_load_by_collection",
        "model_inference_by_collection",
        "game_execution_by_collection",
        "training_by_collection",
        "weights_update_by_collection",
        "candidate_training_execution_authorized",
        "selfplay_execution_authorized",
        "deployment_authorized",
        "promotion_authorized",
        "scheduler_mutation_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_collection_requires_exact_readonly_confirmation():
    with pytest.raises(
        preflight.ApollyonXiphosCandidateTrainingHostPreflightHold,
        match="READONLY_CONFIRMATION_REQUIRED",
    ):
        preflight.collect_xiphos_candidate_training_host_preflight(
            expected_main_head="a" * 40,
            confirm="wrong",
        )


def test_green_snapshot_requires_xiphos_source_gpu_runtime_and_external_control(monkeypatch):
    expected = "a" * 40
    monkeypatch.setattr(preflight.socket, "gethostname", lambda: "Xiphos")
    monkeypatch.setattr(preflight.os, "geteuid", lambda: 1000)
    monkeypatch.setattr(preflight, "_git_snapshot", lambda head: _green_git(head))
    monkeypatch.setattr(preflight, "_gpu_snapshot", _green_gpu)
    monkeypatch.setattr(preflight, "_disk_snapshot", _green_disk)
    monkeypatch.setattr(preflight, "_service_control_snapshot", _green_service)
    monkeypatch.setattr(
        preflight,
        "_real_directory",
        lambda path: path == preflight.MODEL_ROOT,
    )
    monkeypatch.setattr(
        preflight,
        "_real_file",
        lambda path: path == preflight.VENV_PYTHON,
    )

    out = preflight.collect_xiphos_candidate_training_host_preflight(
        expected_main_head=expected,
        confirm=preflight.CONFIRM_TOKEN,
    )
    assert out["candidate_training_host_qualified"] is True
    assert out["holds"] == []
    assert out["host_normalized"] == "xiphos"
    assert out["gpu"]["cuda0_admitted"] is True
    assert out["source"]["matches_expected_main"] is True
    assert out["model_root_present"] is True
    assert out["venv_python_present"] is True
    assert out["service_control"]["external_service_control_available"] is True


@pytest.mark.parametrize(
    ("mutation", "expected_hold"),
    (
        ("wrong_host", "host_identity"),
        ("root", "unprivileged_user_required"),
        ("source_missing", "war_college_source_missing"),
        ("source_drift", "war_college_source_identity"),
        ("gpu_busy", "cuda0_idle_admission"),
        ("model_missing", "candidate_model_root_missing"),
        ("venv_missing", "candidate_runtime_venv_missing"),
        ("disk_missing", "disk_query"),
        ("service_missing", "external_service_control"),
    ),
)
def test_each_host_gap_fails_closed(monkeypatch, mutation, expected_hold):
    expected = "a" * 40
    hostname = "Xiphos"
    uid = 1000
    git = _green_git(expected)
    gpu = _green_gpu()
    disk = _green_disk()
    service = _green_service()
    model_present = True
    venv_present = True

    if mutation == "wrong_host":
        hostname = "Precision"
    elif mutation == "root":
        uid = 0
    elif mutation == "source_missing":
        git["repository_present"] = False
    elif mutation == "source_drift":
        git["matches_expected_main"] = False
    elif mutation == "gpu_busy":
        gpu["cuda0_admitted"] = False
        gpu["cuda0_compute_process_count"] = 1
    elif mutation == "model_missing":
        model_present = False
    elif mutation == "venv_missing":
        venv_present = False
    elif mutation == "disk_missing":
        disk["query_success"] = False
    elif mutation == "service_missing":
        service["external_service_control_available"] = False

    monkeypatch.setattr(preflight.socket, "gethostname", lambda: hostname)
    monkeypatch.setattr(preflight.os, "geteuid", lambda: uid)
    monkeypatch.setattr(preflight, "_git_snapshot", lambda head: git)
    monkeypatch.setattr(preflight, "_gpu_snapshot", lambda: gpu)
    monkeypatch.setattr(preflight, "_disk_snapshot", lambda: disk)
    monkeypatch.setattr(preflight, "_service_control_snapshot", lambda: service)
    monkeypatch.setattr(
        preflight,
        "_real_directory",
        lambda path: model_present if path == preflight.MODEL_ROOT else False,
    )
    monkeypatch.setattr(
        preflight,
        "_real_file",
        lambda path: venv_present if path == preflight.VENV_PYTHON else False,
    )

    out = preflight.collect_xiphos_candidate_training_host_preflight(
        expected_main_head=expected,
        confirm=preflight.CONFIRM_TOKEN,
    )
    assert out["candidate_training_host_qualified"] is False
    assert expected_hold in out["holds"]
    assert out["training_performed"] is False
    assert out["weights_updated"] is False
    assert out["service_mutation_performed"] is False


def test_collection_receipt_is_explicitly_nonmutating(monkeypatch):
    expected = "a" * 40
    monkeypatch.setattr(preflight.socket, "gethostname", lambda: "Xiphos")
    monkeypatch.setattr(preflight.os, "geteuid", lambda: 1000)
    monkeypatch.setattr(preflight, "_git_snapshot", lambda head: _green_git(head))
    monkeypatch.setattr(preflight, "_gpu_snapshot", _green_gpu)
    monkeypatch.setattr(preflight, "_disk_snapshot", _green_disk)
    monkeypatch.setattr(preflight, "_service_control_snapshot", _green_service)
    monkeypatch.setattr(preflight, "_real_directory", lambda path: True)
    monkeypatch.setattr(preflight, "_real_file", lambda path: True)

    out = preflight.collect_xiphos_candidate_training_host_preflight(
        expected_main_head=expected,
        confirm=preflight.CONFIRM_TOKEN,
    )

    for field in (
        "network_access_performed",
        "git_fetch_performed",
        "git_checkout_performed",
        "git_reset_performed",
        "directory_creation_performed",
        "package_install_performed",
        "service_mutation_performed",
        "process_signal_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "promotion_performed",
        "scheduler_mutation_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False
