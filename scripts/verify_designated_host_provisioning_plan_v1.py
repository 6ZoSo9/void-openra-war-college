#!/usr/bin/env python3
"""Verify the source-only designated-host provisioning plan."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = ROOT / "config/war-college/designated-host-provisioning-plan-v1.json"
BINDING_PATH = ROOT / "config/war-college/designated-host-execution-binding-v1.json"
MARKER = "VOID_WAR_COLLEGE_DESIGNATED_HOST_PROVISIONING_PLAN_V1"
EXPECTED_PARENT = "b30df61bf75660f6f1dcb7240cf37a2a4788959a"
GIT = "/usr/bin/git"


class ProvisioningPlanError(ValueError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_blob(path: str, ref: str = "HEAD") -> str:
    cp = subprocess.run(
        [GIT, "-C", str(ROOT), "rev-parse", f"{ref}:{path}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
        },
    )
    if cp.returncode != 0:
        raise ProvisioningPlanError(f"Git blob query failed for {ref}:{path}")
    return cp.stdout.strip()


def verify_plan(plan: Any, binding: Any) -> dict[str, Any]:
    holds: list[str] = []
    if type(plan) is not dict:
        return {"contract": "HOLD", "holds": ["HOLD_PROVISIONING_PLAN_NOT_OBJECT"]}
    if type(binding) is not dict:
        return {"contract": "HOLD", "holds": ["HOLD_EXECUTION_BINDING_NOT_OBJECT"]}

    if plan.get("marker") != MARKER or plan.get("version") != 1:
        holds.append("HOLD_PROVISIONING_PLAN_MARKER_VERSION")
    if (
        plan.get("semantic_parent_pr") != 34
        or plan.get("semantic_parent_head") != EXPECTED_PARENT
    ):
        holds.append("HOLD_PROVISIONING_PLAN_PARENT_MISMATCH")
    if plan.get("operator_uid") != 1000 or plan.get("operator_gid") != 1000:
        holds.append("HOLD_PROVISIONING_OPERATOR_IDENTITY_MISMATCH")

    binding_path = plan.get("execution_binding_path")
    if binding_path != "config/war-college/designated-host-execution-binding-v1.json":
        holds.append("HOLD_PROVISIONING_EXECUTION_BINDING_PATH")
    elif plan.get("execution_binding_git_blob") != _git_blob(binding_path):
        holds.append("HOLD_PROVISIONING_EXECUTION_BINDING_BLOB")

    expected_authority = {
        "daemon_reload_authorized": False,
        "materialization_authorized": False,
        "plan_only": True,
        "private_key_access": False,
        "runtime_execution_authorized": False,
        "service_start_authorized": False,
    }
    if plan.get("authority") != expected_authority:
        holds.append("HOLD_PROVISIONING_AUTHORITY_DRIFT")

    runtime = plan.get("runtime_worktree")
    if type(runtime) is not dict:
        holds.append("HOLD_PROVISIONING_RUNTIME_PLAN_INVALID")
    else:
        if runtime.get("repository") != "/home/zoso/dev/openra-rl-war-college":
            holds.append("HOLD_PROVISIONING_RUNTIME_REPOSITORY")
        if runtime.get("target_path") != binding.get("working_directory"):
            holds.append("HOLD_PROVISIONING_RUNTIME_TARGET")
        if runtime.get("source_commit") != binding.get("runtime_source_commit"):
            holds.append("HOLD_PROVISIONING_RUNTIME_COMMIT")
        if runtime.get("required_artifact_git_blobs") != binding.get(
            "runtime_artifact_git_blobs"
        ):
            holds.append("HOLD_PROVISIONING_RUNTIME_BLOBS")
        if runtime.get("creation") != "git_worktree_add_detach":
            holds.append("HOLD_PROVISIONING_RUNTIME_CREATION")
        if (
            runtime.get("collision_policy")
            != "accept_exact_clean_generation_else_hold"
        ):
            holds.append("HOLD_PROVISIONING_RUNTIME_COLLISION_POLICY")
        if runtime.get("require_clean") is not True:
            holds.append("HOLD_PROVISIONING_RUNTIME_CLEAN_REQUIREMENT")

        source_commit = runtime.get("source_commit")
        if type(source_commit) is str:
            for rel, expected in sorted(
                binding.get("runtime_artifact_git_blobs", {}).items()
            ):
                if _git_blob(rel, source_commit) != expected:
                    holds.append("HOLD_PROVISIONING_HISTORICAL_RUNTIME_BLOB")
                    break

    expected_artifacts = {
        "systemd_user_unit": (
            binding.get("source_unit_path"),
            "aeb467f581e71e21fd48bef970f72c2950d39419",
            binding.get("unit_sha256"),
            binding.get("installed_unit_path"),
            binding.get("unit_required_mode"),
        ),
        "environment": (
            binding.get("source_environment_path"),
            "3aa76da32e4349fd169fb66246d85eca48c38d98",
            binding.get("environment_sha256"),
            binding.get("installed_environment_path"),
            binding.get("environment_required_mode"),
        ),
        "wrapper": (
            binding.get("source_wrapper_path"),
            "816ffeb46c553c754a152a26d348d64433120162",
            binding.get("wrapper_sha256"),
            binding.get("installed_wrapper_path"),
            binding.get("wrapper_required_mode"),
        ),
    }
    artifacts = plan.get("artifacts")
    if type(artifacts) is not list or len(artifacts) != 3:
        holds.append("HOLD_PROVISIONING_ARTIFACT_SET")
    else:
        by_kind = {a.get("kind"): a for a in artifacts if type(a) is dict}
        if set(by_kind) != set(expected_artifacts):
            holds.append("HOLD_PROVISIONING_ARTIFACT_KINDS")
        else:
            for kind, expected in expected_artifacts.items():
                source_path, source_blob, source_sha, target, mode = expected
                item = by_kind[kind]
                if (
                    item.get("source_path") != source_path
                    or item.get("source_git_blob") != source_blob
                    or item.get("source_sha256") != source_sha
                    or item.get("target_path") != target
                    or item.get("required_mode") != mode
                    or item.get("required_uid") != 1000
                    or item.get("required_gid") != 1000
                    or item.get("symlink_allowed") is not False
                    or item.get("collision_policy") != "accept_exact_else_hold"
                ):
                    holds.append(
                        f"HOLD_PROVISIONING_ARTIFACT_{kind.upper()}_DRIFT"
                    )
                    continue
                if _git_blob(source_path) != source_blob:
                    holds.append(
                        f"HOLD_PROVISIONING_ARTIFACT_{kind.upper()}_BLOB"
                    )
                if _sha256(ROOT / source_path) != source_sha:
                    holds.append(
                        f"HOLD_PROVISIONING_ARTIFACT_{kind.upper()}_SHA256"
                    )

    if plan.get("materialization") != {
        "atomic_same_directory_replace": True,
        "follow_symlinks": False,
        "overwrite_nonmatching_existing": False,
        "preserve_exact_source_bytes": True,
    }:
        holds.append("HOLD_PROVISIONING_MATERIALIZATION_POLICY")

    if plan.get("daemon_reload") != {
        "authorized": False,
        "command": ["/usr/bin/systemctl", "--user", "daemon-reload"],
        "required_after_unit_materialization": True,
        "service_start_after_reload": False,
    }:
        holds.append("HOLD_PROVISIONING_DAEMON_RELOAD_POLICY")

    post = plan.get("post_provision_preflight")
    expected_post = {
        "collector_git_blob": "aadcc32fbba9a11d9f4d53f2410a7321c46c0131",
        "collector_path": (
            "scripts/discover_designated_host_execution_binding_runtime_v1.py"
        ),
        "command": [
            "/usr/bin/python3",
            "scripts/discover_designated_host_execution_binding_runtime_v1.py",
        ],
        "required_dropin_paths": [],
        "required_mutation_performed": False,
        "required_need_daemon_reload": False,
        "required_service_started": False,
        "required_systemd_fragment_path": binding.get("installed_unit_path"),
        "required_systemd_load_state": "loaded",
        "required_verification_contract": "GREEN",
    }
    if post != expected_post:
        holds.append("HOLD_PROVISIONING_POST_PREFLIGHT_POLICY")
    elif _git_blob(post["collector_path"]) != post["collector_git_blob"]:
        holds.append("HOLD_PROVISIONING_POST_PREFLIGHT_COLLECTOR_BLOB")

    green = not holds
    return {
        "contract": "GREEN" if green else "HOLD",
        "holds": sorted(set(holds)),
        "plan_only": True,
        "materialization_authorized": False,
        "daemon_reload_authorized": False,
        "service_start_authorized": False,
        "runtime_execution_authorized": False,
        "private_key_access": False,
    }


def main() -> int:
    try:
        plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
        result = verify_plan(plan, binding)
    except (OSError, json.JSONDecodeError, ProvisioningPlanError) as error:
        result = {
            "contract": "HOLD",
            "holds": [
                f"HOLD_PROVISIONING_PLAN_FAILURE:{type(error).__name__}"
            ],
            "plan_only": True,
            "materialization_authorized": False,
            "daemon_reload_authorized": False,
            "service_start_authorized": False,
            "runtime_execution_authorized": False,
            "private_key_access": False,
        }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["contract"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
