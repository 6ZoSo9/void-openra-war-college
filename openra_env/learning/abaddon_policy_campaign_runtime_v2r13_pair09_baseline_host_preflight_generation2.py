"""Read-only host preflight for V2R13 pair-09 baseline.

This preflight understands that pair-03 baseline and candidate already completed
and must remain preserved. It requires pair-09 baseline/candidate and pair-15
baseline/candidate arm roots to remain absent.

The historical all-arms-absent validator is reused only through a labeled
structural projection after the real current host snapshot and preserved
pair-03 evidence are observed. No runtime authority is inherited.

Import has no host effects. Collection is an explicit read-only operator action.
"""

from __future__ import annotations

from contextlib import ExitStack, contextmanager
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
from types import SimpleNamespace
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_source_binding_review_generation2
    as guard_review,
)

SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-host-preflight.v1"
)
CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_OBSERVE_PAIR09_BASELINE_PREFLIGHT"
)
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
ISOLATED_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2"
)
CHUNK_BYTES = 1024 * 1024

PRESERVED_FILES = (
    (
        Path(
            "generation2/pair-03/baseline/runs/"
            "warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685/"
            "trajectory.jsonl"
        ),
        "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9",
        64 * 1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-03/baseline/runs/"
            "warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685/"
            "summary.json"
        ),
        "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6",
        1024 * 1024,
    ),
    (
        Path(
            "pair03-candidate-claims-v1/"
            "pair-03-candidate-attempt-v1.json"
        ),
        "0ab9062efa497457a6e7d42a149e302b3809887f54c7b1e1112b86b5ec2d7f79",
        4096,
    ),
    (
        Path(
            "pair03-candidate-claims-v1/"
            "pair-03-candidate-execution-result-v1.json"
        ),
        "9be2b3a74205cd6102f5839171638431ef25cb4f57db1028033ef2498f740829",
        1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-03/candidate/runs/"
            "warmstart-apollyon-vs-abaddon-20260920T154029Z-feinter-s1990061685/"
            "warm-start.jsonl"
        ),
        "334846e59a956c1f8e059979f56c1775b39e1d51ef42c172e09fc7ab022a8a3a",
        64 * 1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-03/candidate/runs/"
            "warmstart-apollyon-vs-abaddon-20260920T154029Z-feinter-s1990061685/"
            "trajectory.jsonl"
        ),
        "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65",
        64 * 1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-03/candidate/runs/"
            "warmstart-apollyon-vs-abaddon-20260920T154029Z-feinter-s1990061685/"
            "summary.json"
        ),
        "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0",
        1024 * 1024,
    ),
)

SOURCE_REFERENCES = (
    (
        "openra_env/learning/"
        "abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_"
        "source_binding_review_generation2.py",
        "7770954472ebd9abd7f51020ed352dea9adb6df2",
    ),
    (
        "openra_env/learning/"
        "abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2.py",
        "0ae27981a08b27083b235ae4807705c88da259a1",
    ),
    (
        "tools/"
        "abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_"
        "generation2.py",
        "62d8a906ea41138b5443ba3bf96799b6e430b5be",
    ),
)


class V2R13Pair09BaselineHostPreflightHold(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineHostPreflightHold(code)


def _digest(value: Any) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _legacy_validator():
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2
        as legacy,
    )
    return legacy


def _collect_host_snapshot(expected_main_head: str) -> dict[str, Any]:
    from tools import (
        abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2
        as collector,
    )
    return collector.collect(
        SimpleNamespace(
            expected_main_head=expected_main_head,
            source_repository_root=str(SOURCE_ROOT),
            engine_repository_root=str(SOURCE_ROOT / "OpenRA"),
            isolated_workdir_root=str(ISOLATED_ROOT),
        )
    )


@contextmanager
def _open_directory(path: Path):
    _require(
        path.is_absolute() and ".." not in path.parts,
        "PAIR09_PREFLIGHT_DIRECTORY_PATH_INVALID",
    )
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    with ExitStack() as stack:
        fd = os.open("/", flags)
        stack.callback(os.close, fd)
        for part in path.parts[1:]:
            fd = os.open(part, flags, dir_fd=fd)
            stack.callback(os.close, fd)
        yield fd


def _identity(value: os.stat_result) -> tuple[int, ...]:
    return (
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_nlink,
        value.st_uid,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    )


def _read_preserved_file(
    relative: Path,
    expected_sha256: str,
    maximum: int,
) -> dict[str, Any]:
    path = ISOLATED_ROOT / relative
    with _open_directory(path.parent) as parent:
        fd = os.open(
            path.name,
            os.O_RDONLY
            | os.O_NOFOLLOW
            | os.O_NONBLOCK
            | os.O_CLOEXEC,
            dir_fd=parent,
        )
        try:
            before = os.fstat(fd)
            _require(
                stat.S_ISREG(before.st_mode)
                and before.st_nlink == 1
                and 0 < before.st_size <= maximum,
                "PAIR09_PREFLIGHT_PRESERVED_FILE_SHAPE_HOLD",
            )
            digest = hashlib.sha256()
            remaining = before.st_size
            for _ in range(maximum // CHUNK_BYTES + 1024):
                if remaining == 0:
                    break
                chunk = os.read(fd, min(CHUNK_BYTES, remaining))
                _require(
                    bool(chunk),
                    "PAIR09_PREFLIGHT_PRESERVED_FILE_SHORT_READ",
                )
                digest.update(chunk)
                remaining -= len(chunk)
            _require(
                remaining == 0 and os.read(fd, 1) == b"",
                "PAIR09_PREFLIGHT_PRESERVED_FILE_READ_BOUND",
            )
            named = os.stat(
                path.name,
                dir_fd=parent,
                follow_symlinks=False,
            )
            _require(
                _identity(before)
                == _identity(os.fstat(fd))
                == _identity(named),
                "PAIR09_PREFLIGHT_PRESERVED_FILE_CHANGED",
            )
            _require(
                digest.hexdigest() == expected_sha256,
                "PAIR09_PREFLIGHT_PRESERVED_FILE_DIGEST_MISMATCH",
            )
            return {
                "path": str(path),
                "sha256": digest.hexdigest(),
                "bytes": before.st_size,
            }
        finally:
            os.close(fd)


def _arm_layout() -> dict[str, bool]:
    expected = {
        "3:baseline": True,
        "3:candidate": True,
        "9:baseline": False,
        "9:candidate": False,
        "15:baseline": False,
        "15:candidate": False,
    }
    result = {}
    for key, expected_exists in expected.items():
        pair, arm = key.split(":")
        path = (
            ISOLATED_ROOT
            / "generation2"
            / f"pair-{int(pair):02d}"
            / arm
        )
        try:
            with _open_directory(path.parent) as parent:
                entry = os.stat(
                    path.name,
                    dir_fd=parent,
                    follow_symlinks=False,
                )
        except FileNotFoundError:
            exists = False
        else:
            _require(
                stat.S_ISDIR(entry.st_mode),
                "PAIR09_PREFLIGHT_ARM_NOT_DIRECTORY",
            )
            exists = True

        _require(
            exists is expected_exists,
            "PAIR09_PREFLIGHT_ARM_LAYOUT_HOLD",
        )
        result[key] = exists
    return result


def _check_snapshot_layout(
    snapshot: dict[str, Any],
    expected_main_head: str,
) -> None:
    _require(
        type(snapshot) is dict
        and snapshot.get("expected_main_head") == expected_main_head,
        "PAIR09_PREFLIGHT_EXPECTED_MAIN_MISMATCH",
    )
    isolated = snapshot.get("isolated_workdir")
    _require(
        type(isolated) is dict
        and isolated.get("root") == str(ISOLATED_ROOT),
        "PAIR09_PREFLIGHT_ROOT_MISMATCH",
    )
    rows = isolated.get("authorized_arm_paths")
    expected = _arm_layout()
    _require(
        type(rows) is dict and set(rows) == set(expected),
        "PAIR09_PREFLIGHT_ARM_SET_MISMATCH",
    )
    for key, expected_exists in expected.items():
        pair, arm = key.split(":")
        row = rows[key]
        path = (
            ISOLATED_ROOT
            / "generation2"
            / f"pair-{int(pair):02d}"
            / arm
        )
        _require(
            type(row) is dict
            and set(row) == {"path", "exists"}
            and row["path"] == str(path)
            and row["exists"] is expected_exists,
            "PAIR09_PREFLIGHT_SNAPSHOT_LAYOUT_HOLD",
        )


def collect_pair09_baseline_host_preflight(
    *,
    expected_main_head: str,
    confirm: str,
) -> dict[str, Any]:
    """Observe the fixed host and preserved pair-03 evidence; execute nothing."""

    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "PAIR09_PREFLIGHT_READONLY_CONFIRMATION_REQUIRED",
    )
    _require(
        type(expected_main_head) is str
        and len(expected_main_head) == 40
        and all(c in "0123456789abcdef" for c in expected_main_head),
        "PAIR09_PREFLIGHT_MAIN_INVALID",
    )
    _require(
        os.name == "posix"
        and all(
            hasattr(os, name)
            for name in (
                "O_DIRECTORY",
                "O_NOFOLLOW",
                "O_CLOEXEC",
                "O_NONBLOCK",
            )
        ),
        "PAIR09_PREFLIGHT_PLATFORM_UNSUPPORTED",
    )

    guard = (
        guard_review
        .v2r13_pair09_baseline_attempt_guard_review_contract()
    )
    _require(
        guard.get("pair09_baseline_attempt_guard_reviewed") is True
        and guard.get("single_use_attempt_consumption_reviewed") is True
        and guard.get("pair09_baseline_execution_authorized") is False,
        "PAIR09_PREFLIGHT_GUARD_REVIEW_HOLD",
    )

    snapshot = _collect_host_snapshot(expected_main_head)
    _check_snapshot_layout(snapshot, expected_main_head)

    before_layout = _arm_layout()
    evidence = {
        str(relative): _read_preserved_file(
            relative,
            digest,
            maximum,
        )
        for relative, digest, maximum in PRESERVED_FILES
    }

    projection = deepcopy(snapshot)
    for key in ("3:baseline", "3:candidate"):
        projection["isolated_workdir"]["authorized_arm_paths"][key][
            "exists"
        ] = False

    legacy = _legacy_validator()
    checked = legacy.validate_host_preflight_snapshot(projection)
    _require(
        checked.get("host_preflight_green") is True
        and checked.get("snapshot_sha256") == _digest(projection),
        "PAIR09_PREFLIGHT_SHARED_CHECKS_HOLD",
    )

    after_layout = _arm_layout()
    _require(
        before_layout == after_layout,
        "PAIR09_PREFLIGHT_ARM_LAYOUT_CHANGED",
    )

    return {
        "schema": SCHEMA,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "expected_main_head": expected_main_head,
        "pair09_baseline_host_conditions_validated": True,
        "observed_host_snapshot": deepcopy(snapshot),
        "observed_host_snapshot_sha256": _digest(snapshot),
        "observed_arm_layout": deepcopy(after_layout),
        "pair03_preserved_evidence": evidence,
        "pair03_baseline_preserved": True,
        "pair03_candidate_preserved": True,
        "pair09_baseline_absent": True,
        "pair09_candidate_absent": True,
        "held_out_pair15_absent": True,
        "legacy_structural_projection_sha256": _digest(projection),
        "legacy_structural_projection_is_host_observation": False,
        "legacy_runtime_authority_inherited": False,
        "single_use_attempt_consumed": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "runtime_started": False,
    }


def pair09_baseline_host_preflight_contract() -> dict[str, Any]:
    guard = (
        guard_review
        .v2r13_pair09_baseline_attempt_guard_review_contract()
    )
    return {
        "schema": SCHEMA,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "read_only_host_collection_implemented": True,
        "pair03_baseline_preservation_required": True,
        "pair03_candidate_preservation_required": True,
        "pair09_baseline_absence_required": True,
        "pair09_candidate_absence_required": True,
        "held_out_pair15_absence_required": True,
        "legacy_structural_projection_is_host_observation": False,
        "legacy_runtime_authority_inherited": False,
        "single_use_attempt_consumed": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "runtime_started": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "guard_review": guard,
        "source_references": dict(SOURCE_REFERENCES),
        "next_gate": (
            "V2R13_PAIR09_BASELINE_HOST_PREFLIGHT_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "next_change_class": (
            "source_only_v2r13_pair09_baseline_host_preflight_"
            "source_binding_review"
        ),
    }
