#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from openra_env.learning.general_brain_generation import stable_json
from openra_env.learning.general_brain_policy_adapter import (
    build_policy_snapshot,
    policy_adapter_sha256,
    policy_snapshot_sha256,
    policy_training_receipt_sha256,
    train_policy_adapter_revision_two,
)


def _read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def _file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _create_json(path: Path, value: dict) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = stable_json(value) + "\n"
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _trajectory_pairs(args: argparse.Namespace) -> list[tuple[Path, str]]:
    paths = list(args.trajectory or [])
    digests = list(args.trajectory_sha256 or [])
    if not paths or len(paths) != len(digests):
        raise ValueError("--trajectory and --trajectory-sha256 must be repeated equally")
    return [(Path(path), digest) for path, digest in zip(paths, digests)]


def snapshot_command(args: argparse.Namespace) -> int:
    snapshot = build_policy_snapshot(_trajectory_pairs(args))
    output = Path(args.output)
    _create_json(output, snapshot)
    print("GENERAL_BRAIN_POLICY_SNAPSHOT_GREEN")
    print(f"record_count={snapshot['record_count']}")
    print(f"policy_snapshot_sha256={policy_snapshot_sha256(snapshot)}")
    print(f"output_file_sha256={_file_sha(output)}")
    print("validity_only_examples_admitted=false")
    print("authority_envelope_trainable=false")
    print("automatic_weight_mutation=false")
    print("automatic_promotion=false")
    return 0


def train_command(args: argparse.Namespace) -> int:
    parent_path = Path(args.parent_challenger_manifest)
    snapshot_path = Path(args.snapshot)
    rejected_path = Path(args.rejected_parent_pair)
    expected_rejected_sha = args.rejected_parent_pair_sha256
    actual_rejected_sha = _file_sha(rejected_path)
    if actual_rejected_sha != expected_rejected_sha:
        raise ValueError(
            "rejected parent pair SHA-256 mismatch: "
            f"expected={expected_rejected_sha} actual={actual_rejected_sha}"
        )

    parent = _read_json(parent_path)
    snapshot = _read_json(snapshot_path)
    rejected = _read_json(rejected_path)
    adapter, receipt, revised = train_policy_adapter_revision_two(
        parent,
        snapshot,
        rejected_parent_pair=rejected,
        rejected_parent_pair_sha256=actual_rejected_sha,
    )
    adapter_path = Path(args.adapter_output)
    receipt_path = Path(args.receipt_output)
    challenger_path = Path(args.challenger_output)
    _create_json(adapter_path, adapter)
    _create_json(receipt_path, receipt)
    _create_json(challenger_path, revised)

    print("GENERAL_BRAIN_POLICY_REVISION_TWO_TRAINING_GREEN")
    print("general_id=apollyon")
    print("generation=1")
    print("candidate_revision=2")
    print("parent_revision_status=REJECTED")
    print(f"utility_positive_record_count={adapter['utility_positive_record_count']}")
    policy = adapter["policies"]["FORCE_CONVERSION"]
    print(f"learned_target_x_millis={policy['target_x_millis']}")
    print(f"learned_target_y_millis={policy['target_y_millis']}")
    print(f"policy_adapter_sha256={policy_adapter_sha256(adapter)}")
    print(f"policy_training_receipt_sha256={policy_training_receipt_sha256(receipt)}")
    print(f"adapter_file_sha256={_file_sha(adapter_path)}")
    print(f"receipt_file_sha256={_file_sha(receipt_path)}")
    print(f"challenger_file_sha256={_file_sha(challenger_path)}")
    print("flat_tool_weight_retained=false")
    print("live_weight_install=false")
    print("automatic_promotion=false")
    print("review_required=true")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--trajectory", action="append", required=True)
    snapshot.add_argument("--trajectory-sha256", action="append", required=True)
    snapshot.add_argument("--output", required=True)
    snapshot.set_defaults(handler=snapshot_command)

    train = sub.add_parser("train")
    train.add_argument("--parent-challenger-manifest", required=True)
    train.add_argument("--snapshot", required=True)
    train.add_argument("--rejected-parent-pair", required=True)
    train.add_argument("--rejected-parent-pair-sha256", required=True)
    train.add_argument("--adapter-output", required=True)
    train.add_argument("--receipt-output", required=True)
    train.add_argument("--challenger-output", required=True)
    train.set_defaults(handler=train_command)

    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (OSError, ValueError) as error:
        print(f"GENERAL_BRAIN_POLICY_TRAINING_HOLD: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
