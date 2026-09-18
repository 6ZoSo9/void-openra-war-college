#!/usr/bin/env python3
"""Read-only Precision collector for Generation-2 V2R13 host preflight."""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as preflight,
)

MARK = "VOID_ABADDON_GENERATION2_V2R13_PRECISION_HOST_PREFLIGHT_V1"


class CollectorHold(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CollectorHold(message)


def run(
    argv: list[str],
    *,
    cwd: Path | None = None,
    allowed: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        argv,
        cwd=str(cwd) if cwd is not None else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode not in allowed:
        raise CollectorHold(
            f"command failed rc={cp.returncode}: {argv!r}: "
            f"{cp.stderr.strip() or cp.stdout.strip()}"
        )
    return cp


def out(argv: list[str], *, cwd: Path | None = None) -> str:
    return run(argv, cwd=cwd).stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_row(path: str) -> dict[str, Any]:
    p = Path(path)
    exists = p.exists()
    is_file = p.is_file()
    is_symlink = p.is_symlink()
    digest = None
    if exists and is_file and not is_symlink:
        digest = sha256_file(p)
    return {
        "path": path,
        "exists": exists,
        "is_file": is_file,
        "is_symlink": is_symlink,
        "sha256": digest,
    }


def path_row(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "exists": path.exists(),
        "is_dir": path.is_dir(),
        "is_symlink": path.is_symlink(),
    }


def tracked_blob_rows(source_root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for label, expected in preflight.TRACKED_BLOBS.items():
        result[label] = {
            "path": expected["path"],
            "blob": out(
                ["git", "rev-parse", f"HEAD:{expected['path']}"],
                cwd=source_root,
            ),
        }
    return result


def collect(args: argparse.Namespace) -> dict[str, Any]:
    source_root = Path(args.source_repository_root).expanduser().resolve()
    engine_root = Path(args.engine_repository_root).expanduser().resolve()
    isolated_root = Path(args.isolated_workdir_root).expanduser().resolve()

    require(str(source_root) == preflight.EXPECTED_SOURCE_ROOT, "source root drift")
    require(str(engine_root) == preflight.EXPECTED_ENGINE_ROOT, "engine root drift")
    require(
        str(isolated_root).startswith(preflight.EXPECTED_HOME + "/"),
        "isolated root must remain under Precision home",
    )

    expected_head = args.expected_main_head
    require(
        len(expected_head) == 40
        and all(char in "0123456789abcdef" for char in expected_head),
        "expected main head malformed",
    )

    source_toplevel = out(["git", "rev-parse", "--show-toplevel"], cwd=source_root)
    source_branch = out(["git", "branch", "--show-current"], cwd=source_root)
    source_head = out(["git", "rev-parse", "HEAD"], cwd=source_root)
    source_tree = out(["git", "rev-parse", "HEAD^{tree}"], cwd=source_root)
    expected_head_tree = out(
        ["git", "rev-parse", f"{expected_head}^{{tree}}"],
        cwd=source_root,
    )
    source_frozen_commit = out(
        ["git", "rev-parse", "--verify", f"{preflight.FROZEN_SOURCE_COMMIT}^{{commit}}"],
        cwd=source_root,
    )
    source_frozen_tree = out(
        ["git", "rev-parse", f"{preflight.FROZEN_SOURCE_COMMIT}^{{tree}}"],
        cwd=source_root,
    )
    source_tracked_status = out(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=source_root,
    )
    source_untracked_status = out(
        ["git", "status", "--porcelain", "--untracked-files=normal"],
        cwd=source_root,
    )
    source_origin = out(["git", "remote", "get-url", "origin"], cwd=source_root)

    engine_toplevel = out(["git", "rev-parse", "--show-toplevel"], cwd=engine_root)
    engine_head = out(["git", "rev-parse", "HEAD"], cwd=engine_root)
    engine_tree = out(["git", "rev-parse", "HEAD^{tree}"], cwd=engine_root)
    engine_frozen_commit = out(
        ["git", "rev-parse", "--verify", f"{preflight.FROZEN_ENGINE_COMMIT}^{{commit}}"],
        cwd=engine_root,
    )
    engine_frozen_tree = out(
        ["git", "rev-parse", f"{preflight.FROZEN_ENGINE_COMMIT}^{{tree}}"],
        cwd=engine_root,
    )
    engine_tracked_status = out(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=engine_root,
    )

    proto = Path(preflight.EXPECTED_PROTO_PYTHON)
    isolated = path_row(isolated_root)
    isolated["root"] = str(isolated_root)
    arm_paths: dict[str, Any] = {}
    for pair_slot in preflight.AUTHORIZED_PAIR_SLOTS:
        for arm in preflight.AUTHORIZED_ARMS:
            key = f"{pair_slot}:{arm}"
            arm_path = isolated_root / "generation2" / f"pair-{pair_slot:02d}" / arm
            arm_paths[key] = {
                "path": str(arm_path),
                "exists": arm_path.exists(),
            }
    isolated["authorized_arm_paths"] = arm_paths

    external_files = {
        label: file_row(expected["path"])
        for label, expected in preflight.EXTERNAL_FILES.items()
    }

    docker_context = out(["docker", "context", "show"])
    docker_info = out(["docker", "info"])
    image_id = out(
        ["docker", "image", "inspect", "-f", "{{.Id}}", preflight.RUNTIME_IMAGE]
    )
    generation_label = out(
        [
            "docker",
            "image",
            "inspect",
            "-f",
            '{{ index .Config.Labels "void.openra.generation" }}',
            preflight.RUNTIME_IMAGE,
        ]
    )
    container_names = out(["docker", "ps", "-a", "--format", "{{.Names}}"])
    stale = [
        name
        for name in container_names.splitlines()
        if name.startswith("void-warmstart-spar-")
    ]

    active = run(
        ["systemctl", "is-active", preflight.OLLAMA_SERVICE],
        allowed=(0, 1, 2, 3, 4),
    ).stdout.strip()
    enabled = run(
        ["systemctl", "is-enabled", preflight.OLLAMA_SERVICE],
        allowed=(0, 1, 2, 3, 4),
    ).stdout.strip()
    permit = Path(preflight.ACTIVATION_PERMIT)
    fuse = Path(preflight.DORMANT_FUSE)
    fuse_present = fuse.is_file()
    condition_present = False
    if fuse_present:
        condition_present = (
            preflight.DORMANT_CONDITION
            in fuse.read_text(encoding="utf-8", errors="replace").splitlines()
        )

    return {
        "schema": preflight.SNAPSHOT_SCHEMA,
        "expected_main_head": expected_head,
        "hostname": socket.gethostname(),
        "home": str(Path.home().resolve()),
        "source_repository": {
            "root": str(source_root),
            "toplevel": source_toplevel,
            "branch": source_branch,
            "head": source_head,
            "head_tree": source_tree,
            "expected_head_tree": expected_head_tree,
            "origin_url": source_origin,
            "tracked_status": source_tracked_status,
            "untracked_status": source_untracked_status,
            "frozen_source_commit": source_frozen_commit,
            "frozen_source_tree": source_frozen_tree,
            "tracked_blobs": tracked_blob_rows(source_root),
        },
        "engine_repository": {
            "root": str(engine_root),
            "toplevel": engine_toplevel,
            "head": engine_head,
            "head_tree": engine_tree,
            "tracked_status": engine_tracked_status,
            "frozen_engine_commit": engine_frozen_commit,
            "frozen_engine_tree": engine_frozen_tree,
        },
        "proto_python": {
            "path": str(proto),
            "exists": proto.exists(),
            "is_file": proto.is_file(),
            "is_symlink": proto.is_symlink(),
        },
        "isolated_workdir": isolated,
        "external_files": external_files,
        "docker": {
            "context": docker_context,
            "info_contains_rootless": "rootless" in docker_info.lower(),
            "image": preflight.RUNTIME_IMAGE,
            "image_id": image_id,
            "generation_label": generation_label,
            "stale_warmstart_containers": stale,
        },
        "ollama": {
            "service": preflight.OLLAMA_SERVICE,
            "active": active,
            "enabled": enabled,
            "activation_permit_present": permit.exists(),
            "dormant_fuse_present": fuse_present,
            "dormant_condition_present": condition_present,
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-main-head", required=True)
    parser.add_argument(
        "--source-repository-root",
        default=preflight.EXPECTED_SOURCE_ROOT,
    )
    parser.add_argument(
        "--engine-repository-root",
        default=preflight.EXPECTED_ENGINE_ROOT,
    )
    parser.add_argument("--isolated-workdir-root", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print(MARK)
    print("mutation_mode=read_only")
    print("git_fetch_performed=false")
    print("git_checkout_performed=false")
    print("runtime_start=false")
    print("model_inference=false")
    print("game_execution=false")
    print("training=false")
    print("deployment=false")
    print("void_chain_mutation=false")
    print("wallet_or_funds_action=false")
    try:
        snapshot = collect(args)
        admission = preflight.validate_host_preflight_snapshot(snapshot)
    except Exception as error:
        print(f"{MARK}_HOLD", file=sys.stderr)
        print(f"blocker={type(error).__name__}:{error}", file=sys.stderr)
        return 2

    print(f"expected_main_head={snapshot['expected_main_head']}")
    print(f"source_head={snapshot['source_repository']['head']}")
    print(f"source_branch={snapshot['source_repository']['branch']}")
    print(f"source_origin={snapshot['source_repository']['origin_url']}")
    print(f"source_untracked_status={snapshot['source_repository']['untracked_status']!r}")
    print(f"engine_head={snapshot['engine_repository']['head']}")
    print(f"docker_context={snapshot['docker']['context']}")
    print(f"ollama_active={snapshot['ollama']['active']}")
    print(f"ollama_enabled={snapshot['ollama']['enabled']}")
    print(f"snapshot_sha256={admission['snapshot_sha256']}")
    print("host_preflight_green=true")
    print("runtime_execution_performed=false")
    print("next_gate=V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_EVIDENCE_ACCEPTANCE_REQUIRED")
    print("snapshot_json=" + json.dumps(snapshot, sort_keys=True, separators=(",", ":")))
    print("admission_json=" + json.dumps(admission, sort_keys=True, separators=(",", ":")))
    print(f"{MARK}_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
