"""Read-only candidate preflight that preserves the completed pair-03 baseline.

The historical validator requires all six arm paths to be absent. Reuse its
unchanged host predicates through an explicitly labeled structural projection,
AFTER observing the completed baseline and its exact evidence bytes. The real
snapshot is retained unchanged; projected absence is never a host observation
and the historical validator's broad runtime authority is never propagated.

No import-time I/O, CLI, attempt consumption, runtime start or authorization.
Collection is an explicit trusted-operator read-only action, not remote
attestation, an atomic host snapshot or executed-source custody.
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
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2 as request,
)

SCHEMA = "void.abaddon.generation2.v2r13-pair03-candidate-host-preflight.v1"
CONFIRM_TOKEN = "VOID_ABADDON_GENERATION2_V2R13_OBSERVE_PAIR03_CANDIDATE_PREFLIGHT"
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
ISOLATED_ROOT = Path("/home/zoso/dev/void-war-college-execution/v2r13-generation2")
BASELINE_RUN_ID = "warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685"
BASELINE_RUN_REL = Path("generation2/pair-03/baseline/runs") / BASELINE_RUN_ID
BASELINE_FILES = (
    ("trajectory.jsonl", "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9", 64 * 1024 * 1024),
    ("summary.json", "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6", 1024 * 1024),
)
CHUNK_BYTES = 1024 * 1024
SOURCE_PREFIX = "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_"
DEPENDENCY_GIT_BLOBS = (
    (SOURCE_PREFIX + "host_preflight_generation2.py", "0ae27981a08b27083b235ae4807705c88da259a1"),
    ("tools/abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2.py",
     "62d8a906ea41138b5443ba3bf96799b6e430b5be"),
    (SOURCE_PREFIX + "pair03_baseline_retry2_execution_evidence_acceptance_generation2.py",
     "037730c77bc67cbd722becc30fc898b50cba842b"),
    (SOURCE_PREFIX + "pair03_candidate_authorization_request_generation2.py",
     "07516a24553b2516b859bebca21818c0bd0bf01e"),
)


class CandidateHostPreflightHold(RuntimeError):
    """Read-only preflight did not establish the required conditions."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise CandidateHostPreflightHold(code)


def _digest(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def _legacy_validator():
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as legacy,
    )
    return legacy


def _collect_host_snapshot(expected_main_head: str) -> dict[str, Any]:
    from tools import abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2 as collector
    return collector.collect(SimpleNamespace(
        expected_main_head=expected_main_head,
        source_repository_root=str(SOURCE_ROOT),
        engine_repository_root=str(SOURCE_ROOT / "OpenRA"),
        isolated_workdir_root=str(ISOLATED_ROOT),
    ))


@contextmanager
def _open_directory(path: Path):
    """Retain a no-follow descriptor chain; never mkdir or resolve symlinks."""
    _require(path.is_absolute() and ".." not in path.parts, "PREFLIGHT_DIRECTORY_PATH_INVALID")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
    with ExitStack() as stack:
        fd = os.open("/", flags)
        stack.callback(os.close, fd)
        for part in path.parts[1:]:
            fd = os.open(part, flags, dir_fd=fd)
            stack.callback(os.close, fd)
        yield fd


def _arm_census() -> dict[str, bool]:
    result = {}
    for pair in (3, 9, 15):
        for arm in ("baseline", "candidate"):
            path = ISOLATED_ROOT / "generation2" / f"pair-{pair:02d}" / arm
            try:
                with _open_directory(path.parent) as parent:
                    entry = os.stat(path.name, dir_fd=parent, follow_symlinks=False)
            except FileNotFoundError:
                exists = False
            else:
                # A dangling symlink is not absence; existing non-directories HOLD.
                _require(stat.S_ISDIR(entry.st_mode), "PREFLIGHT_ARM_NOT_DIRECTORY")
                exists = True
            _require(exists is (pair == 3 and arm == "baseline"), "PREFLIGHT_ARM_LAYOUT_HOLD")
            result[f"{pair}:{arm}"] = exists
    return result


def _identity(value: os.stat_result) -> tuple[int, ...]:
    # Reading may update atime; never treat it as content mutation.
    return (value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_uid, value.st_size, value.st_mtime_ns, value.st_ctime_ns)


def _read_baseline_file(name: str, expected_sha256: str, maximum: int) -> dict[str, Any]:
    path = ISOLATED_ROOT / BASELINE_RUN_REL / name
    with _open_directory(path.parent) as parent:
        with ExitStack() as stack:
            fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
            stack.callback(os.close, fd)
            before = os.fstat(fd)
            _require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                     "PREFLIGHT_BASELINE_NOT_REGULAR_SINGLE_LINK")
            _require(0 < before.st_size <= maximum, "PREFLIGHT_BASELINE_SIZE_HOLD")
            digest = hashlib.sha256()
            remaining = before.st_size
            # Bound both bytes and read calls, including short-read schedules.
            for _ in range(maximum // CHUNK_BYTES + 1024):
                if remaining == 0:
                    break
                chunk = os.read(fd, min(CHUNK_BYTES, remaining))
                _require(bool(chunk), "PREFLIGHT_BASELINE_SHORT_READ")
                digest.update(chunk)
                remaining -= len(chunk)
            _require(remaining == 0 and os.read(fd, 1) == b"", "PREFLIGHT_BASELINE_READ_BOUND")
            _require(_identity(before) == _identity(os.fstat(fd)) == _identity(
                os.stat(path.name, dir_fd=parent, follow_symlinks=False)), "PREFLIGHT_BASELINE_CHANGED")
            _require(digest.hexdigest() == expected_sha256, "PREFLIGHT_BASELINE_DIGEST_MISMATCH")
            result = {"path": str(path), "sha256": digest.hexdigest(), "bytes": before.st_size}
        return result


def _check_snapshot_layout(snapshot: dict[str, Any], expected_main_head: str) -> None:
    _require(type(snapshot) is dict and snapshot.get("expected_main_head") == expected_main_head,
             "PREFLIGHT_EXPECTED_MAIN_MISMATCH")
    isolated = snapshot.get("isolated_workdir")
    _require(type(isolated) is dict and isolated.get("root") == str(ISOLATED_ROOT), "PREFLIGHT_ROOT_MISMATCH")
    rows = isolated.get("authorized_arm_paths")
    keys = {f"{pair}:{arm}" for pair in (3, 9, 15) for arm in ("baseline", "candidate")}
    _require(type(rows) is dict and set(rows) == keys, "PREFLIGHT_ARM_SET_MISMATCH")
    for key in sorted(keys):
        pair, arm = key.split(":")
        row = rows[key]
        expected_path = ISOLATED_ROOT / "generation2" / f"pair-{int(pair):02d}" / arm
        _require(type(row) is dict and set(row) == {"path", "exists"}, "PREFLIGHT_ARM_ROW_MALFORMED")
        _require(row["path"] == str(expected_path), "PREFLIGHT_ARM_PATH_MISMATCH")
        _require(row["exists"] is (key == "3:baseline"), "PREFLIGHT_ARM_LAYOUT_HOLD")


def collect_pair03_candidate_host_preflight(*, expected_main_head: str, confirm: str) -> dict[str, Any]:
    """Observe the fixed host and preserved baseline. This cannot launch a game.

    No caller-supplied snapshot, file path, digest override or preflight bypass
    is accepted. Trusted-operator collection is sequential, not atomic. The
    candidate invocation still needs its own operation-bound authorization,
    single-use guard, fresh live readiness and revocation checks.
    """
    _require(type(confirm) is str and confirm == CONFIRM_TOKEN, "PREFLIGHT_READONLY_CONFIRMATION_REQUIRED")
    _require(type(expected_main_head) is str and len(expected_main_head) == 40
             and all(c in "0123456789abcdef" for c in expected_main_head), "PREFLIGHT_MAIN_INVALID")
    _require(os.name == "posix" and all(hasattr(os, name) for name in
             ("O_DIRECTORY", "O_NOFOLLOW", "O_CLOEXEC", "O_NONBLOCK")), "PREFLIGHT_PLATFORM_UNSUPPORTED")
    baseline_reference = request.candidate_authorization_request_contract()["request"]["baseline_reference"]
    _require(baseline_reference["trajectory_sha256"] == BASELINE_FILES[0][1]
             and baseline_reference["summary_sha256"] == BASELINE_FILES[1][1], "PREFLIGHT_BASELINE_PIN_DRIFT")
    try:
        snapshot = _collect_host_snapshot(expected_main_head)
        _check_snapshot_layout(snapshot, expected_main_head)
        _arm_census()
        baseline = {name: _read_baseline_file(name, digest, cap) for name, digest, cap in BASELINE_FILES}
        projection = deepcopy(snapshot)
        projection["isolated_workdir"]["authorized_arm_paths"]["3:baseline"]["exists"] = False
        legacy = _legacy_validator()
        checked = legacy.validate_host_preflight_snapshot(projection)
        _require(checked.get("host_preflight_green") is True
                 and checked.get("snapshot_sha256") == _digest(projection), "PREFLIGHT_SHARED_CHECKS_HOLD")
        _arm_census()
        return {
            "schema": SCHEMA, "pair_slot": 3, "arm": "candidate", "expected_main_head": expected_main_head,
            "candidate_host_conditions_validated": True,
            "observed_host_snapshot": deepcopy(snapshot), "observed_host_snapshot_sha256": _digest(snapshot),
            "baseline_files": baseline, "completed_baseline_preserved": True,
            "legacy_structural_projection_sha256": _digest(projection),
            "legacy_structural_projection_is_host_observation": False,
            "legacy_runtime_authority_inherited": False,
            "candidate_execution_authorized": False, "candidate_execution_performed": False,
            "single_use_attempt_consumed": False, "runtime_started": False,
            "model_load_performed": False, "game_execution_performed": False,
            "independent_host_attestation": False, "atomic_host_snapshot": False,
            "next_gate": "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
        }
    except CandidateHostPreflightHold:
        raise
    except OSError:
        raise CandidateHostPreflightHold("PREFLIGHT_FILESYSTEM_OBSERVATION_HOLD") from None
