from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as preflight,
)

REPO = Path(__file__).resolve().parents[1]
VALIDATOR = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2.py"
)
COLLECTOR = (
    REPO
    / "tools/"
    "abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2.py"
)
EXPECTED_HEAD = "a" * 40
EXPECTED_TREE = "b" * 40
ENGINE_HEAD = "c" * 40
ENGINE_TREE = "d" * 40
ENGINE_FROZEN_TREE = "e" * 40
ISOLATED_ROOT = "/home/zoso/void-war-college-execution/v2r13-generation2"


def _external_files():
    return {
        label: {
            "path": expected["path"],
            "exists": True,
            "is_file": True,
            "is_symlink": False,
            "sha256": expected["sha256"],
        }
        for label, expected in preflight.EXTERNAL_FILES.items()
    }


def _tracked_blobs():
    return {
        label: {
            "path": expected["path"],
            "blob": expected["blob"],
        }
        for label, expected in preflight.TRACKED_BLOBS.items()
    }


def _arm_paths():
    return {
        f"{pair_slot}:{arm}": {
            "path": (
                f"{ISOLATED_ROOT}/generation2/"
                f"pair-{pair_slot:02d}/{arm}"
            ),
            "exists": False,
        }
        for pair_slot in preflight.AUTHORIZED_PAIR_SLOTS
        for arm in preflight.AUTHORIZED_ARMS
    }


def valid_snapshot():
    return {
        "schema": preflight.SNAPSHOT_SCHEMA,
        "expected_main_head": EXPECTED_HEAD,
        "hostname": preflight.EXPECTED_HOSTNAME,
        "home": preflight.EXPECTED_HOME,
        "source_repository": {
            "root": preflight.EXPECTED_SOURCE_ROOT,
            "toplevel": preflight.EXPECTED_SOURCE_ROOT,
            "branch": "main",
            "head": EXPECTED_HEAD,
            "head_tree": EXPECTED_TREE,
            "expected_head_tree": EXPECTED_TREE,
            "origin_url": "https://github.com/yxc20089/OpenRA-RL.git",
            "tracked_status": "",
            "untracked_status": "?? unsloth_compiled_cache/",
            "frozen_source_commit": preflight.FROZEN_SOURCE_COMMIT,
            "frozen_source_tree": preflight.FROZEN_SOURCE_TREE,
            "tracked_blobs": _tracked_blobs(),
        },
        "engine_repository": {
            "root": preflight.EXPECTED_ENGINE_ROOT,
            "toplevel": preflight.EXPECTED_ENGINE_ROOT,
            "head": ENGINE_HEAD,
            "head_tree": ENGINE_TREE,
            "tracked_status": "",
            "frozen_engine_commit": preflight.FROZEN_ENGINE_COMMIT,
            "frozen_engine_tree": ENGINE_FROZEN_TREE,
        },
        "proto_python": {
            "path": preflight.EXPECTED_PROTO_PYTHON,
            "exists": True,
            "is_file": True,
            "is_symlink": True,
        },
        "isolated_workdir": {
            "path": ISOLATED_ROOT,
            "root": ISOLATED_ROOT,
            "exists": True,
            "is_dir": True,
            "is_symlink": False,
            "authorized_arm_paths": _arm_paths(),
        },
        "external_files": _external_files(),
        "docker": {
            "context": "rootless",
            "info_contains_rootless": True,
            "image": preflight.RUNTIME_IMAGE,
            "image_id": preflight.RUNTIME_IMAGE_ID,
            "generation_label": preflight.GENERATION,
            "stale_warmstart_containers": [],
        },
        "ollama": {
            "service": preflight.OLLAMA_SERVICE,
            "active": "inactive",
            "enabled": "disabled",
            "activation_permit_present": False,
            "dormant_fuse_present": True,
            "dormant_condition_present": True,
        },
        "authority": {
            "git_fetch_performed": False,
            "git_checkout_performed": False,
            "filesystem_mutation_performed": False,
            "service_action_performed": False,
            "runtime_start_performed": False,
            "model_load_performed": False,
            "model_inference_performed": False,
            "game_execution_performed": False,
            "training_performed": False,
            "weights_updated": False,
            "policy_promotion_performed": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
        },
    }


def test_contract_advances_from_executor_review_to_preflight_source_review():
    out = preflight.host_preflight_contract()
    assert out["host_preflight_validator_implemented"] is True
    assert out["real_host_collector_implemented_by_this_source"] is False
    assert out["read_only_snapshot_required"] is True
    assert out["runtime_execution_authorized"] is True
    assert out["runtime_execution_performed"] is False
    assert out["next_gate"] == (
        "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_exact_valid_snapshot_is_admitted():
    out = preflight.validate_host_preflight_snapshot(valid_snapshot())
    assert out["host_preflight_completed"] is True
    assert out["host_preflight_green"] is True
    assert out["runtime_execution_authorized"] is True
    assert out["runtime_execution_performed"] is False
    assert out["fresh_readiness_still_required_before_inference"] is True
    assert len(out["snapshot_sha256"]) == 64
    assert out["next_gate"] == (
        "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_EVIDENCE_ACCEPTANCE_REQUIRED"
    )


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("hostname",), "other-host", "Precision hostname drift"),
        (
            ("source_repository", "branch"),
            "feature",
            "source checkout must be on main",
        ),
        (
            ("source_repository", "head"),
            "f" * 40,
            "source main head drift",
        ),
        (
            ("source_repository", "tracked_status"),
            " M openra_env/x.py",
            "source tracked worktree dirty",
        ),
        (
            ("engine_repository", "tracked_status"),
            " M OpenRA.Game/x.cs",
            "engine tracked worktree dirty",
        ),
        (
            ("docker", "context"),
            "default",
            "rootless Docker context required",
        ),
        (
            ("ollama", "active"),
            "active",
            "Ollama must begin inactive",
        ),
        (
            ("ollama", "activation_permit_present"),
            True,
            "activation permit leaked",
        ),
    ],
)
def test_core_preflight_drift_is_rejected(path, value, message):
    snapshot = valid_snapshot()
    target = snapshot
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(preflight.V2R13HostPreflightHold, match=message):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_external_dependency_hash_drift_is_rejected():
    snapshot = valid_snapshot()
    snapshot["external_files"]["legacy_warm_start_runner"]["sha256"] = "0" * 64
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="external SHA-256 drift",
    ):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_tracked_executor_blob_drift_is_rejected():
    snapshot = valid_snapshot()
    snapshot["source_repository"]["tracked_blobs"]["executor_source"]["blob"] = (
        "0" * 40
    )
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="tracked blob drift",
    ):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_existing_authorized_arm_path_is_rejected():
    snapshot = valid_snapshot()
    snapshot["isolated_workdir"]["authorized_arm_paths"]["15:candidate"][
        "exists"
    ] = True
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="arm-path already exists",
    ):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_stale_warmstart_container_is_rejected():
    snapshot = valid_snapshot()
    snapshot["docker"]["stale_warmstart_containers"] = [
        "void-warmstart-spar-1234"
    ]
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="stale warm-start container present",
    ):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_dormant_fuse_must_bind_activation_permit_when_present():
    snapshot = valid_snapshot()
    snapshot["ollama"]["dormant_condition_present"] = False
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="dormant fuse does not bind activation permit",
    ):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_absent_dormant_fuse_is_allowed_only_with_no_condition_claim():
    snapshot = valid_snapshot()
    snapshot["ollama"]["dormant_fuse_present"] = False
    snapshot["ollama"]["dormant_condition_present"] = False
    out = preflight.validate_host_preflight_snapshot(snapshot)
    assert out["host_preflight_green"] is True


def test_mutation_claim_is_rejected():
    snapshot = valid_snapshot()
    snapshot["authority"]["git_fetch_performed"] = True
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="host preflight crossed boundary",
    ):
        preflight.validate_host_preflight_snapshot(snapshot)


def test_untracked_cache_does_not_dirty_tracked_source_boundary():
    snapshot = valid_snapshot()
    snapshot["source_repository"]["untracked_status"] = (
        "?? unsloth_compiled_cache/\n?? local-evidence/"
    )
    out = preflight.validate_host_preflight_snapshot(snapshot)
    assert out["host_preflight_green"] is True


def test_validator_source_has_no_host_io_imports():
    tree = ast.parse(VALIDATOR.read_text(encoding="utf-8"), filename=str(VALIDATOR))
    forbidden = {
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "httpx",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_precision_collector_contains_no_mutating_host_commands():
    text = COLLECTOR.read_text(encoding="utf-8")
    forbidden_fragments = (
        '"fetch"',
        '"checkout"',
        '"pull"',
        '"reset"',
        '"clean"',
        '"worktree", "add"',
        '"worktree", "remove"',
        '"systemctl", "start"',
        '"systemctl", "stop"',
        '"systemctl", "restart"',
        '"systemctl", "daemon-reload"',
        '"docker", "run"',
        '"docker", "rm"',
        ".mkdir(",
        ".write_text(",
        ".write_bytes(",
        ".unlink(",
    )
    for fragment in forbidden_fragments:
        assert fragment not in text


def test_execution_entrypoint_remains_held_until_source_review():
    with pytest.raises(
        preflight.V2R13HostPreflightHold,
        match="V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        preflight.execute_v2r13_runtime()
