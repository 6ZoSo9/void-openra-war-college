#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from openra_env.learning.general_brain_generation import manifest_sha256
from openra_env.learning.general_brain_training import (
    GeneralBrainTrainingError,
    adapter_sha256,
    build_corpus_snapshot,
    corpus_snapshot_sha256,
    evaluate_promotion,
    make_challenger_from_training,
    make_training_receipt,
    train_tactical_preference_adapter,
    training_receipt_sha256,
)


class CliError(ValueError):
    pass


def stable_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False) + "\n"


def load_object(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise CliError(f"{path} must contain a JSON object")
    return value


def write_exact(path: Path, value: Mapping[str, Any]) -> str:
    encoded = stable_json(value)
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if current != encoded:
            raise CliError(f"refusing to replace different existing artifact: {path}")
        return "unchanged"
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()
    return "created"


def snapshot_command(args: argparse.Namespace) -> int:
    trajectories = [(Path(value), None) for value in args.trajectory]
    snapshot = build_corpus_snapshot(args.general, trajectories)
    status = write_exact(Path(args.output), snapshot)
    print("GENERAL_BRAIN_CORPUS_SNAPSHOT_GREEN")
    print(f"general_id={snapshot['general_id']}")
    print(f"record_count={snapshot['record_count']}")
    print(f"preference_record_count={snapshot['preference_record_count']}")
    print(f"positive_imitation_record_count={snapshot['positive_imitation_record_count']}")
    print(f"corpus_snapshot_sha256={corpus_snapshot_sha256(snapshot)}")
    print(f"output_status={status}")
    print("authority_envelope_trainable=false")
    print("automatic_corpus_admission=false")
    print("automatic_weight_mutation=false")
    print("automatic_promotion=false")
    return 0


def train_command(args: argparse.Namespace) -> int:
    parent = load_object(Path(args.parent_manifest))
    corpus = load_object(Path(args.corpus))
    adapter = train_tactical_preference_adapter(parent, corpus)
    receipt = make_training_receipt(parent, corpus, adapter)
    challenger = make_challenger_from_training(parent, corpus, adapter, receipt)

    statuses = {
        "adapter": write_exact(Path(args.adapter_output), adapter),
        "receipt": write_exact(Path(args.receipt_output), receipt),
        "challenger": write_exact(Path(args.challenger_output), challenger),
    }
    print("GENERAL_BRAIN_ADAPTER_TRAINING_GREEN")
    print(f"general_id={challenger['general_id']}")
    print(f"parent_generation={int(challenger['generation']) - 1}")
    print(f"challenger_generation={challenger['generation']}")
    print(f"parent_manifest_sha256={manifest_sha256(parent)}")
    print(f"corpus_snapshot_sha256={corpus_snapshot_sha256(corpus)}")
    print(f"training_receipt_sha256={training_receipt_sha256(receipt)}")
    print(f"adapter_artifact_sha256={adapter_sha256(adapter)}")
    print("artifact_status=" + json.dumps(statuses, sort_keys=True, separators=(",", ":")))
    print("adapter_scope=tactical_competence_only")
    print("authority_envelope_trainable=false")
    print("automatic_weight_mutation=false")
    print("automatic_promotion=false")
    print("promotion_state=CHALLENGER_REVIEW_REQUIRED")
    return 0


def promotion_command(args: argparse.Namespace) -> int:
    incumbent = load_object(Path(args.incumbent))
    challenger = load_object(Path(args.challenger))
    evaluation = load_object(Path(args.evaluation))
    decision = evaluate_promotion(incumbent, challenger, evaluation)
    status = write_exact(Path(args.output), decision)
    print("GENERAL_BRAIN_PROMOTION_REVIEW_COMPLETE")
    print(f"eligible_for_promotion={str(decision['eligible_for_promotion']).lower()}")
    print("reasons=" + json.dumps(decision["reasons"], separators=(",", ":")))
    print(f"output_status={status}")
    print("automatic_promotion=false")
    print("review_required=true")
    return 0


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Reviewed General Brain corpus, adapter training, and promotion contracts")
    sub = value.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot", help="Build reviewed tactical corpus from exact trajectories")
    snapshot.add_argument("--general", choices=("apollyon", "abaddon"), required=True)
    snapshot.add_argument("--trajectory", action="append", required=True)
    snapshot.add_argument("--output", required=True)
    snapshot.set_defaults(func=snapshot_command)

    train = sub.add_parser("train", help="Train deterministic tactical preference adapter")
    train.add_argument("--parent-manifest", required=True)
    train.add_argument("--corpus", required=True)
    train.add_argument("--adapter-output", required=True)
    train.add_argument("--receipt-output", required=True)
    train.add_argument("--challenger-output", required=True)
    train.set_defaults(func=train_command)

    promote = sub.add_parser("promotion-check", help="Evaluate challenger against frozen promotion wall")
    promote.add_argument("--incumbent", required=True)
    promote.add_argument("--challenger", required=True)
    promote.add_argument("--evaluation", required=True)
    promote.add_argument("--output", required=True)
    promote.set_defaults(func=promotion_command)
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (
        CliError,
        GeneralBrainTrainingError,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        print(f"GENERAL_BRAIN_TRAINING_HOLD: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
