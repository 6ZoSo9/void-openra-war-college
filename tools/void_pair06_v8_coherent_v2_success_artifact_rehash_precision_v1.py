#!/usr/bin/env python3
"""Read-only Precision rehash for the closed pair-06 V8 V2 coherent success.

This observer reads exactly six already-existing durable artifacts, verifies
their recorded SHA-256 identities, checks selected cross-file semantics, and
prints one public-safe canonical JSON manifest to stdout.

It does not create, modify, rename, delete, reset, retry, execute, train,
promote, deploy, start/stop a service, access a wallet, or touch the VOID chain.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-coherent-v2-success-artifact-rehash-manifest.v1"
)
CONFIRM_TOKEN = "VOID_PAIR06_V8_COHERENT_V2_SUCCESS_ARTIFACT_REHASH_READ_ONLY"
SOURCE_BASIS_MAIN = "d25c45a4790cad764205adeea2e8e480c1bbb9bf"
AUTHORIZED_MAIN_HEAD = "d8b16f1c23a74803ac4ace94045fed147c3c69fe"
RUN_ID = "warmstart-apollyon-vs-abaddon-20260927T183337Z-feinter-s208354846"

ARM_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/baseline"
)
CLAIMS_ROOT = ARM_ROOT / "claims-v1"
RUN_DIR = ARM_ROOT / "runs-combat-priority-coherent-v2-v1" / RUN_ID

ARTIFACTS = {
    "attempt_marker": {
        "path": CLAIMS_ROOT
        / "pair06-v8-combat-priority-coherent-v2-baseline-game-attempt-v1.json",
        "sha256": "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207",
    },
    "result": {
        "path": CLAIMS_ROOT
        / "pair06-v8-combat-priority-coherent-v2-baseline-game-result-v1.json",
        "sha256": "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4",
    },
    "closeout": {
        "path": CLAIMS_ROOT
        / "pair06-v8-combat-priority-coherent-v2-baseline-game-closeout-v1.json",
        "sha256": "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1",
    },
    "trajectory": {
        "path": RUN_DIR / "trajectory.jsonl",
        "sha256": "afc57351991c90dc21e4d2316ddd23fce8b01b9132a3435a9252de7227001ddc",
    },
    "summary": {
        "path": RUN_DIR / "summary.json",
        "sha256": "a5d72287487849164e727836eee82dd5821ddb46f5803b995b1d67cc289075ab",
    },
    "warm_start": {
        "path": RUN_DIR / "warm-start.jsonl",
        "sha256": "f36f2717d34e028d02d1b7076d7de1cff65dce1ffed59710110f2adbf4ad700d",
    },
}

MAX_ARTIFACT_BYTES = 16 * 1024 * 1024
IDENTITY_FIELDS = (
    "st_dev",
    "st_ino",
    "st_size",
    "st_mtime_ns",
    "st_ctime_ns",
    "st_mode",
    "st_nlink",
)


class ArtifactRehashHold(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ArtifactRehashHold(code)


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return tuple(int(getattr(value, field)) for field in IDENTITY_FIELDS)


def _read_exact_regular_file(
    path: Path,
    *,
    expected_sha256: str,
    maximum_bytes: int = MAX_ARTIFACT_BYTES,
) -> tuple[bytes, dict[str, Any]]:
    """Read one stable regular file generation through one no-follow fd."""
    _require(path.is_absolute(), "ARTIFACT_PATH_NOT_ABSOLUTE")
    resolved = path.resolve(strict=True)
    _require(resolved == path, "ARTIFACT_PATH_RESOLUTION_DRIFT")
    _require(
        type(maximum_bytes) is int and 0 < maximum_bytes <= MAX_ARTIFACT_BYTES,
        "ARTIFACT_BYTE_BOUND_INVALID",
    )

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise ArtifactRehashHold(
            f"ARTIFACT_OPEN_FAILED:{path.name}:{type(exc).__name__}"
        ) from None

    chunks: list[bytes] = []
    try:
        before = os.fstat(fd)
        _require(stat.S_ISREG(before.st_mode), "ARTIFACT_NOT_REGULAR")
        _require(before.st_nlink == 1, "ARTIFACT_LINK_COUNT_DRIFT")
        _require(before.st_size >= 0, "ARTIFACT_NEGATIVE_SIZE")
        _require(before.st_size <= maximum_bytes, "ARTIFACT_EXCEEDS_BYTE_BOUND")

        digest = hashlib.sha256()
        total = 0
        while True:
            remaining = maximum_bytes + 1 - total
            _require(remaining > 0, "ARTIFACT_EXCEEDS_BYTE_BOUND")
            chunk = os.read(fd, min(1024 * 1024, remaining))
            _require(isinstance(chunk, bytes), "ARTIFACT_READ_TYPE")
            if not chunk:
                break
            total += len(chunk)
            _require(total <= maximum_bytes, "ARTIFACT_EXCEEDS_BYTE_BOUND")
            digest.update(chunk)
            chunks.append(chunk)

        after = os.fstat(fd)
        _require(_identity(before) == _identity(after), "ARTIFACT_GENERATION_CHANGED")
        _require(total == before.st_size, "ARTIFACT_SIZE_CHANGED")
        actual = digest.hexdigest()
        _require(actual == expected_sha256, f"ARTIFACT_SHA256_DRIFT:{path.name}")
        return b"".join(chunks), {
            "sha256": actual,
            "byte_count": total,
            "regular_file": True,
            "single_link": True,
            "generation_stable": True,
            "symlink_followed": False,
        }
    finally:
        os.close(fd)


def _json_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ArtifactRehashHold(f"{label}_JSON_INVALID") from None
    _require(type(value) is dict, f"{label}_JSON_OBJECT_REQUIRED")
    return value


def _validate_marker(marker: dict[str, Any]) -> None:
    _require(
        marker.get("schema")
        == (
            "void.abaddon.generation2."
            "pair06-v8-combat-priority-coherent-v2-baseline-game-attempt.v1"
        ),
        "MARKER_SCHEMA_DRIFT",
    )
    _require(
        marker.get("record_kind") == "attempt_consumed_not_execution_evidence",
        "MARKER_RECORD_KIND_DRIFT",
    )
    _require(
        marker.get("pair_slot") == 6
        and marker.get("arm") == "baseline"
        and marker.get("held_out") is False,
        "MARKER_SCOPE_DRIFT",
    )
    _require(
        marker.get("expected_main_head") == AUTHORIZED_MAIN_HEAD,
        "MARKER_MAIN_DRIFT",
    )
    _require(
        marker.get("maximum_attempts") == 1
        and marker.get("automatic_retry") is False,
        "MARKER_SINGLE_USE_DRIFT",
    )
    for field in (
        "prior_consumed_attempt_reusable",
        "prior_failed_run_reusable_as_authority",
        "prior_authorization_reusable",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(marker.get(field) is False, "MARKER_BOUNDARY_DRIFT:" + field)


def _validate_result(result: dict[str, Any]) -> None:
    _require(
        result.get("schema")
        == (
            "void.abaddon.generation2."
            "pair06-v8-combat-priority-coherent-v2-baseline-game-result-no-offload.v1"
        ),
        "RESULT_SCHEMA_DRIFT",
    )
    _require(
        result.get("pair_slot") == 6
        and result.get("arm") == "baseline"
        and result.get("held_out") is False,
        "RESULT_SCOPE_DRIFT",
    )
    _require(
        result.get("attempt_marker_sha256") == ARTIFACTS["attempt_marker"]["sha256"],
        "RESULT_ATTEMPT_BINDING_DRIFT",
    )
    for field in (
        "automatic_retry",
        "candidate_execution_performed",
        "pair15_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(result.get(field) is False, "RESULT_BOUNDARY_DRIFT:" + field)

    supervisor = result.get("supervisor_receipt")
    _require(type(supervisor) is dict, "RESULT_SUPERVISOR_RECEIPT_REQUIRED")
    _require(
        supervisor.get("attempt_id") == ARTIFACTS["attempt_marker"]["sha256"]
        and supervisor.get("attempt_claimed") is True,
        "RESULT_SUPERVISOR_ATTEMPT_DRIFT",
    )
    _require(
        supervisor.get("child_retirement_terminal") == "natural_exit",
        "RESULT_CHILD_RETIREMENT_DRIFT",
    )
    _require(
        supervisor.get("game_execution_performed") is True
        and supervisor.get("model_inference_performed") is True
        and supervisor.get("model_inference_count") == 36,
        "RESULT_EXECUTION_FACT_DRIFT",
    )

    game = supervisor.get("game_result")
    _require(type(game) is dict, "RESULT_GAME_RESULT_REQUIRED")
    _require(game.get("run_id") == RUN_ID, "RESULT_GAME_RUN_ID_DRIFT")
    _require(
        game.get("trajectory_sha256") == ARTIFACTS["trajectory"]["sha256"]
        and game.get("summary_sha256") == ARTIFACTS["summary"]["sha256"]
        and game.get("warm_start_sha256") == ARTIFACTS["warm_start"]["sha256"],
        "RESULT_GAME_ARTIFACT_BINDING_DRIFT",
    )
    _require(game.get("game_cleanup_completed") is True, "RESULT_GAME_CLEANUP_DRIFT")
    _require(game.get("legacy_ollama_started") is False, "RESULT_LEGACY_OLLAMA_DRIFT")


def _validate_closeout(closeout: dict[str, Any]) -> None:
    _require(
        closeout.get("schema")
        == (
            "void.abaddon.generation2."
            "pair06-v8-combat-priority-coherent-v2-baseline-game-closeout-no-offload.v1"
        ),
        "CLOSEOUT_SCHEMA_DRIFT",
    )
    _require(
        closeout.get("attempt_marker_sha256") == ARTIFACTS["attempt_marker"]["sha256"]
        and closeout.get("result_file_sha256") == ARTIFACTS["result"]["sha256"],
        "CLOSEOUT_BINDING_DRIFT",
    )
    _require(
        closeout.get("worktree_cleanup_completed") is True
        and closeout.get("runs_preserved") is True
        and closeout.get("automatic_retry") is False,
        "CLOSEOUT_STATE_DRIFT",
    )
    cleanup = closeout.get("worktree_cleanup")
    _require(type(cleanup) is dict, "CLOSEOUT_WORKTREE_CLEANUP_REQUIRED")
    _require(
        cleanup.get("source_worktree_removed") is True
        and cleanup.get("engine_worktree_removed") is True
        and cleanup.get("removed_worktree_count") == 2,
        "CLOSEOUT_WORKTREE_CLEANUP_DRIFT",
    )
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(closeout.get(field) is False, "CLOSEOUT_BOUNDARY_DRIFT:" + field)


def _validate_summary(summary: dict[str, Any]) -> None:
    _require(
        summary.get("schema") == "void.apollyon-abaddon.warm-start-combat-spar-summary.v1",
        "SUMMARY_SCHEMA_DRIFT",
    )
    _require(
        summary.get("run_id") == RUN_ID
        and summary.get("rounds_completed") == 36
        and summary.get("final_tick") == 3551
        and summary.get("outcome") == "DRAW_OR_UNFINISHED",
        "SUMMARY_RUN_IDENTITY_DRIFT",
    )
    _require(
        summary.get("trajectory_sha256") == ARTIFACTS["trajectory"]["sha256"]
        and summary.get("warm_start_sha256") == ARTIFACTS["warm_start"]["sha256"],
        "SUMMARY_ARTIFACT_BINDING_DRIFT",
    )
    _require(
        summary.get("automatic_corpus_admission") is False
        and summary.get("automatic_apollyon_weight_mutation") is False
        and summary.get("automatic_abaddon_policy_promotion") is False,
        "SUMMARY_AUTOMATION_BOUNDARY_DRIFT",
    )


def collect_success_artifact_rehash_manifest(*, confirm: str) -> dict[str, Any]:
    _require(confirm == CONFIRM_TOKEN, "READ_ONLY_REHASH_CONFIRMATION_REQUIRED")

    raw: dict[str, bytes] = {}
    receipts: dict[str, dict[str, Any]] = {}
    for label, spec in ARTIFACTS.items():
        artifact_raw, receipt = _read_exact_regular_file(
            spec["path"],
            expected_sha256=spec["sha256"],
        )
        raw[label] = artifact_raw
        receipts[label] = receipt

    _validate_marker(_json_object(raw["attempt_marker"], "MARKER"))
    _validate_result(_json_object(raw["result"], "RESULT"))
    _validate_closeout(_json_object(raw["closeout"], "CLOSEOUT"))
    _validate_summary(_json_object(raw["summary"], "SUMMARY"))

    return {
        "schema": SCHEMA,
        "source_basis_main": SOURCE_BASIS_MAIN,
        "authorized_execution_main": AUTHORIZED_MAIN_HEAD,
        "run_id": RUN_ID,
        "pair_slot": 6,
        "arm": "baseline",
        "artifact_count": len(receipts),
        "artifacts": receipts,
        "artifact_bytes_verified": True,
        "artifact_cross_file_semantics_verified": True,
        "repo_side_local_artifact_rehash_performed": True,
        "execution_lineage_closed": True,
        "attempt_reusable": False,
        "authorization_reusable": False,
        "automatic_retry": False,
        "new_execution_request_opened": False,
        "host_observation_performed": True,
        "host_mutation_performed": False,
        "game_execution_performed_by_observer": False,
        "model_inference_performed_by_observer": False,
        "training_performed_by_observer": False,
        "deployment_performed_by_observer": False,
        "void_chain_mutation_performed_by_observer": False,
        "wallet_or_funds_action_performed_by_observer": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args()
    manifest = collect_success_artifact_rehash_manifest(confirm=args.confirm)
    print(
        json.dumps(
            manifest,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
