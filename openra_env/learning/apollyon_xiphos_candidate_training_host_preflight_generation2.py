"""Read-only Xiphos qualification for Apollyon candidate training.

This module implements a trusted-operator observation gate for the preferred
candidate-training host named by the reviewed controlled-autonomy policy.

Import and contract inspection perform no host I/O.  Explicit collection is
read-only: it does not fetch or checkout Git, create paths, install packages,
start/stop services, load a model, run inference, execute a War College game,
train, mutate weights, deploy, change a scheduler, access the network, touch
VOID chain state, or access wallets/funds.

The preflight does not grant training authority.  It only establishes whether
Xiphos has the expected source/runtime assets, an idle CUDA:0 admission window,
and external user-service control needed for a later bounded training plan.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import subprocess
from typing import Any

from openra_env.learning import (
    apollyon_controlled_autonomous_learning_policy_source_binding_review_generation2
    as policy_review,
)


SCHEMA = "void.apollyon.generation2.xiphos-candidate-training-host-preflight.v1"
CONTRACT_SCHEMA = (
    "void.apollyon.generation2.xiphos-candidate-training-host-preflight-contract.v1"
)

POLICY_REVIEW_GIT_BLOB = "4a4b9123e6cad52fcf2bb8b1f70dde0bba36ce20"

EXPECTED_HOST_NORMALIZED = "xiphos"
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
MODEL_ROOT = Path("/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1")
VENV_PYTHON = MODEL_ROOT / "venv/bin/python3.12"
MINIMUM_CUDA0_FREE_FRACTION_NUMERATOR = 9
MINIMUM_CUDA0_FREE_FRACTION_DENOMINATOR = 10
CONFIRM_TOKEN = "VOID_APOLLYON_XIPHOS_CANDIDATE_TRAINING_HOST_PREFLIGHT_READONLY"

MAX_COMMAND_OUTPUT_BYTES = 1024 * 1024
COMMAND_TIMEOUT_SECONDS = 15

NEXT_GATE = (
    "APOLLYON_XIPHOS_CANDIDATE_TRAINING_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_apollyon_xiphos_candidate_training_host_preflight_review"
)


class ApollyonXiphosCandidateTrainingHostPreflightHold(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ApollyonXiphosCandidateTrainingHostPreflightHold(code)


@lru_cache(maxsize=1)
def _policy() -> dict[str, Any]:
    reviewed = (
        policy_review
        .apollyon_controlled_autonomous_learning_policy_review_contract()
    )
    _require(
        reviewed.get("apollyon_controlled_autonomous_learning_policy_reviewed")
        is True,
        "XIPHOS_PREFLIGHT_CONTROLLED_AUTONOMY_POLICY_NOT_REVIEWED",
    )
    _require(
        reviewed.get("preferred_candidate_training_host") == "Xiphos"
        and reviewed.get("candidate_training_allowed_after_external_host_preflight")
        is True,
        "XIPHOS_PREFLIGHT_HOST_POLICY_DRIFT",
    )
    _require(
        reviewed.get("authority_envelope_trainable") is False
        and reviewed.get("shutdown_control_external_to_trainable_model") is True
        and reviewed.get("incumbent_weight_mutation_allowed") is False
        and reviewed.get("automatic_promotion_allowed") is False,
        "XIPHOS_PREFLIGHT_CONTROL_POLICY_DRIFT",
    )
    _require(
        reviewed.get("candidate_training_execution_authorized_now") is False
        and reviewed.get("selfplay_execution_authorized_now") is False
        and reviewed.get("deployment_authorized") is False
        and reviewed.get("promotion_authorized") is False,
        "XIPHOS_PREFLIGHT_PREMATURE_TRAINING_AUTHORITY",
    )
    return deepcopy(reviewed)


def _real_directory(path: Path) -> bool:
    try:
        observed = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISDIR(observed.st_mode) and not stat.S_ISLNK(observed.st_mode)


def _real_file(path: Path) -> bool:
    try:
        observed = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISREG(observed.st_mode) and not stat.S_ISLNK(observed.st_mode)


def _run_readonly(argv: list[str]) -> subprocess.CompletedProcess[str]:
    _require(
        isinstance(argv, list)
        and bool(argv)
        and all(isinstance(value, str) and bool(value) for value in argv),
        "XIPHOS_PREFLIGHT_COMMAND_INVALID",
    )
    proc = subprocess.run(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        timeout=COMMAND_TIMEOUT_SECONDS,
        env={
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )
    _require(
        len(proc.stdout.encode("utf-8")) + len(proc.stderr.encode("utf-8"))
        <= MAX_COMMAND_OUTPUT_BYTES,
        "XIPHOS_PREFLIGHT_COMMAND_OUTPUT_BOUND",
    )
    return proc


def _git_snapshot(expected_main_head: str) -> dict[str, Any]:
    if not _real_directory(SOURCE_ROOT) or not _real_directory(SOURCE_ROOT / ".git"):
        return {
            "repository_present": False,
            "expected_main_head": expected_main_head,
            "main_branch": False,
            "head": None,
            "tree": None,
            "tracked_clean": False,
            "matches_expected_main": False,
        }

    def git(*args: str) -> str:
        proc = _run_readonly(["/usr/bin/git", "-C", str(SOURCE_ROOT), *args])
        _require(proc.returncode == 0, "XIPHOS_PREFLIGHT_GIT_QUERY_FAILED")
        return proc.stdout.strip()

    root = git("rev-parse", "--show-toplevel")
    _require(root == str(SOURCE_ROOT), "XIPHOS_PREFLIGHT_REPOSITORY_ROOT_DRIFT")
    branch = git("symbolic-ref", "-q", "HEAD")
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    status = git("status", "--porcelain", "--untracked-files=all").splitlines()
    tracked = [row for row in status if not row.startswith("?? ")]

    return {
        "repository_present": True,
        "expected_main_head": expected_main_head,
        "branch": branch,
        "main_branch": branch == "refs/heads/main",
        "head": head,
        "tree": tree,
        "tracked_clean": len(tracked) == 0,
        "matches_expected_main": head == expected_main_head,
    }


def _gpu_snapshot() -> dict[str, Any]:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return {
            "query_success": False,
            "reason": "nvidia_smi_missing",
            "gpus": [],
            "compute_processes": [],
            "cuda0_admitted": False,
        }

    gpu = _run_readonly(
        [
            nvidia_smi,
            "--query-gpu=index,name,uuid,memory.total,memory.free,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    if gpu.returncode != 0:
        return {
            "query_success": False,
            "reason": "gpu_query_failed",
            "gpus": [],
            "compute_processes": [],
            "cuda0_admitted": False,
        }

    gpus = []
    for line in gpu.stdout.splitlines():
        if not line.strip():
            continue
        fields = [field.strip() for field in line.split(",")]
        _require(len(fields) == 6, "XIPHOS_PREFLIGHT_GPU_ROW_SHAPE")
        index, name, uuid, total, free, driver = fields
        _require(index.isdigit(), "XIPHOS_PREFLIGHT_GPU_INDEX_INVALID")
        _require(total.isdigit() and free.isdigit(), "XIPHOS_PREFLIGHT_GPU_MEMORY_INVALID")
        gpus.append(
            {
                "index": int(index),
                "name": name,
                "uuid": uuid,
                "memory_total_mib": int(total),
                "memory_free_mib": int(free),
                "driver_version": driver,
            }
        )

    proc = _run_readonly(
        [
            nvidia_smi,
            "--query-compute-apps=gpu_uuid,pid,process_name,used_memory",
            "--format=csv,noheader,nounits",
        ]
    )
    compute = []
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            if not line.strip():
                continue
            fields = [field.strip() for field in line.split(",")]
            _require(len(fields) == 4, "XIPHOS_PREFLIGHT_GPU_PROCESS_ROW_SHAPE")
            gpu_uuid, pid, name, used = fields
            _require(pid.isdigit() and used.isdigit(), "XIPHOS_PREFLIGHT_GPU_PROCESS_INVALID")
            compute.append(
                {
                    "gpu_uuid": gpu_uuid,
                    "pid": int(pid),
                    "process_name": name,
                    "used_memory_mib": int(used),
                }
            )

    cuda0 = next((row for row in gpus if row["index"] == 0), None)
    cuda0_processes = (
        []
        if cuda0 is None
        else [row for row in compute if row["gpu_uuid"] == cuda0["uuid"]]
    )
    admitted = False
    if cuda0 is not None and cuda0["memory_total_mib"] > 0:
        admitted = (
            not cuda0_processes
            and cuda0["memory_free_mib"]
            * MINIMUM_CUDA0_FREE_FRACTION_DENOMINATOR
            >= cuda0["memory_total_mib"]
            * MINIMUM_CUDA0_FREE_FRACTION_NUMERATOR
        )

    return {
        "query_success": True,
        "gpus": gpus,
        "compute_processes": compute,
        "cuda0_compute_process_count": len(cuda0_processes),
        "cuda0_admitted": admitted,
    }


def _disk_snapshot() -> dict[str, Any]:
    probe = Path("/home/zoso")
    if not _real_directory(probe):
        return {"query_success": False}
    stats = os.statvfs(probe)
    return {
        "query_success": True,
        "probe_path": str(probe),
        "free_bytes": stats.f_bavail * stats.f_frsize,
        "total_bytes": stats.f_blocks * stats.f_frsize,
    }


def _service_control_snapshot() -> dict[str, Any]:
    systemctl = shutil.which("systemctl")
    if not systemctl:
        return {
            "systemctl_present": False,
            "user_manager_query_success": False,
            "external_service_control_available": False,
        }
    proc = _run_readonly([systemctl, "--user", "is-system-running"])
    state = proc.stdout.strip()
    available = proc.returncode in (0, 1) and state in (
        "running",
        "degraded",
        "starting",
        "maintenance",
    )
    return {
        "systemctl_present": True,
        "user_manager_query_success": proc.returncode in (0, 1),
        "user_manager_state": state,
        "external_service_control_available": available,
    }


def apollyon_xiphos_candidate_training_host_preflight_contract() -> dict[str, Any]:
    reviewed = _policy()
    return {
        "schema": CONTRACT_SCHEMA,
        "policy_review_git_blob": POLICY_REVIEW_GIT_BLOB,
        "policy_reviewed": True,
        "preferred_candidate_training_host": "Xiphos",
        "expected_host_normalized": EXPECTED_HOST_NORMALIZED,
        "source_root": str(SOURCE_ROOT),
        "model_root": str(MODEL_ROOT),
        "venv_python": str(VENV_PYTHON),
        "minimum_cuda0_free_fraction_numerator": (
            MINIMUM_CUDA0_FREE_FRACTION_NUMERATOR
        ),
        "minimum_cuda0_free_fraction_denominator": (
            MINIMUM_CUDA0_FREE_FRACTION_DENOMINATOR
        ),
        "read_only_host_collection_implemented": True,
        "network_access_by_collection": False,
        "git_fetch_by_collection": False,
        "git_checkout_by_collection": False,
        "git_reset_by_collection": False,
        "directory_creation_by_collection": False,
        "package_install_by_collection": False,
        "service_mutation_by_collection": False,
        "process_signal_by_collection": False,
        "model_load_by_collection": False,
        "model_inference_by_collection": False,
        "game_execution_by_collection": False,
        "training_by_collection": False,
        "weights_update_by_collection": False,
        "candidate_training_execution_authorized": False,
        "selfplay_execution_authorized": False,
        "deployment_authorized": False,
        "promotion_authorized": False,
        "scheduler_mutation_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "shutdown_control_external_to_trainable_model": reviewed[
            "shutdown_control_external_to_trainable_model"
        ],
        "automatic_promotion_allowed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def collect_xiphos_candidate_training_host_preflight(
    *,
    expected_main_head: str,
    confirm: str,
) -> dict[str, Any]:
    """Collect one read-only Xiphos host snapshot."""
    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "XIPHOS_PREFLIGHT_READONLY_CONFIRMATION_REQUIRED",
    )
    _require(
        isinstance(expected_main_head, str)
        and len(expected_main_head) == 40
        and all(ch in "0123456789abcdef" for ch in expected_main_head),
        "XIPHOS_PREFLIGHT_EXPECTED_MAIN_INVALID",
    )

    contract = apollyon_xiphos_candidate_training_host_preflight_contract()
    _require(
        contract.get("candidate_training_execution_authorized") is False,
        "XIPHOS_PREFLIGHT_PREMATURE_TRAINING_AUTHORITY",
    )

    hostname = socket.gethostname()
    normalized = hostname.strip().lower()
    uid = os.geteuid()
    git = _git_snapshot(expected_main_head)
    gpu = _gpu_snapshot()
    disk = _disk_snapshot()
    service = _service_control_snapshot()

    model_root_present = _real_directory(MODEL_ROOT)
    venv_python_present = _real_file(VENV_PYTHON)

    holds = []
    if normalized != EXPECTED_HOST_NORMALIZED:
        holds.append("host_identity")
    if uid == 0:
        holds.append("unprivileged_user_required")
    if not git["repository_present"]:
        holds.append("war_college_source_missing")
    elif not (
        git.get("main_branch")
        and git.get("tracked_clean")
        and git.get("matches_expected_main")
    ):
        holds.append("war_college_source_identity")
    if not gpu.get("query_success"):
        holds.append("gpu_query")
    elif not gpu.get("cuda0_admitted"):
        holds.append("cuda0_idle_admission")
    if not model_root_present:
        holds.append("candidate_model_root_missing")
    if not venv_python_present:
        holds.append("candidate_runtime_venv_missing")
    if not disk.get("query_success"):
        holds.append("disk_query")
    if not service.get("external_service_control_available"):
        holds.append("external_service_control")

    qualified = not holds
    return {
        "schema": SCHEMA,
        "read_only": True,
        "host": hostname,
        "host_normalized": normalized,
        "uid": uid,
        "expected_main_head": expected_main_head,
        "source": deepcopy(git),
        "gpu": deepcopy(gpu),
        "disk": deepcopy(disk),
        "service_control": deepcopy(service),
        "model_root_present": model_root_present,
        "venv_python_present": venv_python_present,
        "candidate_training_host_qualified": qualified,
        "holds": holds,
        "network_access_performed": False,
        "git_fetch_performed": False,
        "git_checkout_performed": False,
        "git_reset_performed": False,
        "directory_creation_performed": False,
        "package_install_performed": False,
        "service_mutation_performed": False,
        "process_signal_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "promotion_performed": False,
        "scheduler_mutation_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--expected-main", required=True)
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args(argv)
    out = collect_xiphos_candidate_training_host_preflight(
        expected_main_head=args.expected_main,
        confirm=args.confirm,
    )
    print(
        json.dumps(
            out,
            sort_keys=True,
            indent=2,
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return 0 if out["candidate_training_host_qualified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
