"""Read-only host preflight for V2R13 pair-09 candidate.

The accepted host layout now contains completed pair-03 baseline/candidate and
completed pair-09 baseline evidence. Pair-09 candidate and pair-15 arms must
remain absent.

The historical all-arms-absent validator is reused only through an explicitly
labeled structural projection after the real current host snapshot and all
preserved evidence bytes are observed. No runtime authority is inherited.

Import and contract inspection perform no host I/O. Collection is an explicit
trusted-operator read-only action and never consumes the candidate attempt.
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
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_attempt_guard_source_binding_review_generation2
    as guard_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_authorization_request_generation2
    as request,
)

SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-host-preflight.v1"
)
CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-host-preflight-contract.v1"
)
CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_OBSERVE_PAIR09_CANDIDATE_PREFLIGHT"
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
        Path("pair03-candidate-claims-v1/pair-03-candidate-attempt-v1.json"),
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
    (
        Path("pair09-baseline-claims-v1/pair-09-baseline-attempt-v1.json"),
        "57f862fe39a8939f3d47d4184fe264e0b9cd3988143f4cdc3adb9973a0e2e41c",
        4096,
    ),
    (
        Path(
            "pair09-baseline-claims-v1/"
            "pair-09-baseline-execution-result-v1.json"
        ),
        "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2",
        1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-09/baseline/runs/"
            "warmstart-apollyon-vs-abaddon-20260922T211556Z-feinter-s1496195137/"
            "warm-start.jsonl"
        ),
        "d40816f63f86b5103b9d181ecc31e6b694005c1f3032a1b3fc614a209f2d7790",
        64 * 1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-09/baseline/runs/"
            "warmstart-apollyon-vs-abaddon-20260922T211556Z-feinter-s1496195137/"
            "trajectory.jsonl"
        ),
        "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700",
        64 * 1024 * 1024,
    ),
    (
        Path(
            "generation2/pair-09/baseline/runs/"
            "warmstart-apollyon-vs-abaddon-20260922T211556Z-feinter-s1496195137/"
            "summary.json"
        ),
        "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189",
        1024 * 1024,
    ),
)

EXPECTED_ARM_LAYOUT = {
    "3:baseline": True,
    "3:candidate": True,
    "9:baseline": True,
    "9:candidate": False,
    "15:baseline": False,
    "15:candidate": False,
}

NEXT_GATE = (
    "V2R13_PAIR09_CANDIDATE_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair09_candidate_host_preflight_source_binding_review"
)


class V2R13Pair09CandidateHostPreflightHold(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateHostPreflightHold(code)


def _digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


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
        "PAIR09_CANDIDATE_PREFLIGHT_DIRECTORY_PATH_INVALID",
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


def _arm_census() -> dict[str, bool]:
    result: dict[str, bool] = {}
    for key, expected in EXPECTED_ARM_LAYOUT.items():
        pair_text, arm = key.split(":")
        path = (
            ISOLATED_ROOT
            / "generation2"
            / f"pair-{int(pair_text):02d}"
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
                "PAIR09_CANDIDATE_PREFLIGHT_ARM_NOT_DIRECTORY",
            )
            exists = True
        _require(
            exists is expected,
            "PAIR09_CANDIDATE_PREFLIGHT_ARM_LAYOUT_HOLD",
        )
        result[key] = exists
    return result


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
                and before.st_nlink == 1,
                "PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_NOT_REGULAR_SINGLE_LINK",
            )
            _require(
                0 < before.st_size <= maximum,
                "PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_SIZE_HOLD",
            )
            digest = hashlib.sha256()
            remaining = before.st_size
            max_calls = maximum // CHUNK_BYTES + 1024
            for _ in range(max_calls):
                if remaining == 0:
                    break
                chunk = os.read(
                    fd,
                    min(CHUNK_BYTES, remaining),
                )
                _require(
                    bool(chunk),
                    "PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_SHORT_READ",
                )
                digest.update(chunk)
                remaining -= len(chunk)
            _require(
                remaining == 0 and os.read(fd, 1) == b"",
                "PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_READ_BOUND",
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
                "PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_CHANGED",
            )
            _require(
                digest.hexdigest() == expected_sha256,
                "PAIR09_CANDIDATE_PREFLIGHT_EVIDENCE_DIGEST_MISMATCH",
            )
            return {
                "path": str(path),
                "sha256": digest.hexdigest(),
                "bytes": before.st_size,
            }
        finally:
            os.close(fd)


def _check_snapshot_layout(
    snapshot: dict[str, Any],
    expected_main_head: str,
) -> None:
    _require(
        type(snapshot) is dict
        and snapshot.get("expected_main_head") == expected_main_head,
        "PAIR09_CANDIDATE_PREFLIGHT_EXPECTED_MAIN_MISMATCH",
    )
    isolated = snapshot.get("isolated_workdir")
    _require(
        type(isolated) is dict
        and isolated.get("root") == str(ISOLATED_ROOT),
        "PAIR09_CANDIDATE_PREFLIGHT_ROOT_MISMATCH",
    )
    rows = isolated.get("authorized_arm_paths")
    _require(
        type(rows) is dict
        and set(rows) == set(EXPECTED_ARM_LAYOUT),
        "PAIR09_CANDIDATE_PREFLIGHT_ARM_SET_MISMATCH",
    )
    for key, expected_exists in EXPECTED_ARM_LAYOUT.items():
        pair_text, arm = key.split(":")
        row = rows[key]
        expected_path = (
            ISOLATED_ROOT
            / "generation2"
            / f"pair-{int(pair_text):02d}"
            / arm
        )
        _require(
            type(row) is dict
            and set(row) == {"path", "exists"},
            "PAIR09_CANDIDATE_PREFLIGHT_ARM_ROW_MALFORMED",
        )
        _require(
            row["path"] == str(expected_path),
            "PAIR09_CANDIDATE_PREFLIGHT_ARM_PATH_MISMATCH",
        )
        _require(
            row["exists"] is expected_exists,
            "PAIR09_CANDIDATE_PREFLIGHT_ARM_LAYOUT_HOLD",
        )


def pair09_candidate_host_preflight_contract() -> dict[str, Any]:
    guard = guard_review.v2r13_pair09_candidate_attempt_guard_review_contract()
    _require(
        guard.get("pair09_candidate_attempt_guard_reviewed") is True,
        "PAIR09_CANDIDATE_PREFLIGHT_GUARD_NOT_REVIEWED",
    )
    _require(
        guard.get("pair_slot") == 9
        and guard.get("arm") == "candidate"
        and guard.get("held_out") is False,
        "PAIR09_CANDIDATE_PREFLIGHT_GUARD_SCOPE_DRIFT",
    )
    _require(
        guard.get("single_use_attempt_consumption_reviewed") is True,
        "PAIR09_CANDIDATE_PREFLIGHT_GUARD_SINGLE_USE_DRIFT",
    )
    _require(
        guard.get("pair09_candidate_execution_authorized") is False,
        "PAIR09_CANDIDATE_PREFLIGHT_PREMATURE_AUTHORITY",
    )
    return {
        "schema": CONTRACT_SCHEMA,
        "pair09_candidate_host_preflight_implemented": True,
        "pair09_candidate_host_preflight_reviewed": False,
        "read_only_host_collection": True,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "pair03_baseline_preservation_required": True,
        "pair03_candidate_preservation_required": True,
        "pair09_baseline_preservation_required": True,
        "pair09_candidate_absence_required": True,
        "held_out_pair15_absence_required": True,
        "single_use_attempt_consumed": False,
        "pair09_candidate_execution_authorized": False,
        "pair09_candidate_execution_performed": False,
        "legacy_runtime_authority_inherited": False,
        "runtime_started": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "reviewed_guard": deepcopy(guard),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def collect_pair09_candidate_host_preflight(
    *,
    expected_main_head: str,
    confirm: str,
) -> dict[str, Any]:
    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "PAIR09_CANDIDATE_PREFLIGHT_READONLY_CONFIRMATION_REQUIRED",
    )
    _require(
        type(expected_main_head) is str
        and len(expected_main_head) == 40
        and all(c in "0123456789abcdef" for c in expected_main_head),
        "PAIR09_CANDIDATE_PREFLIGHT_MAIN_INVALID",
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
        "PAIR09_CANDIDATE_PREFLIGHT_PLATFORM_UNSUPPORTED",
    )
    contract = pair09_candidate_host_preflight_contract()
    _require(
        contract.get("pair09_candidate_execution_authorized") is False,
        "PAIR09_CANDIDATE_PREFLIGHT_PREMATURE_AUTHORITY",
    )

    request_record = request.pair09_candidate_authorization_request_contract()[
        "request"
    ]
    baseline = request_record["baseline_reference"]
    _require(
        baseline["trajectory_sha256"]
        == "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
        and baseline["summary_sha256"]
        == "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
        and baseline["result_file_sha256"]
        == "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2",
        "PAIR09_CANDIDATE_PREFLIGHT_BASELINE_PIN_DRIFT",
    )

    try:
        snapshot = _collect_host_snapshot(expected_main_head)
        _check_snapshot_layout(snapshot, expected_main_head)
        real_layout = _arm_census()
        preserved = {
            str(relative): _read_preserved_file(
                relative,
                digest,
                maximum,
            )
            for relative, digest, maximum in PRESERVED_FILES
        }

        projection = deepcopy(snapshot)
        for key, present in EXPECTED_ARM_LAYOUT.items():
            if present:
                projection["isolated_workdir"]["authorized_arm_paths"][key][
                    "exists"
                ] = False

        legacy = _legacy_validator()
        checked = legacy.validate_host_preflight_snapshot(projection)
        _require(
            checked.get("host_preflight_green") is True
            and checked.get("snapshot_sha256") == _digest(projection),
            "PAIR09_CANDIDATE_PREFLIGHT_SHARED_CHECKS_HOLD",
        )
        _require(
            _arm_census() == real_layout,
            "PAIR09_CANDIDATE_PREFLIGHT_LAYOUT_CHANGED",
        )

        return {
            "schema": SCHEMA,
            "pair_slot": 9,
            "arm": "candidate",
            "held_out": False,
            "expected_main_head": expected_main_head,
            "pair09_candidate_host_conditions_validated": True,
            "observed_host_snapshot": deepcopy(snapshot),
            "observed_host_snapshot_sha256": _digest(snapshot),
            "observed_arm_layout": deepcopy(real_layout),
            "preserved_evidence": preserved,
            "pair03_baseline_preserved": True,
            "pair03_candidate_preserved": True,
            "pair09_baseline_preserved": True,
            "pair09_candidate_absent": True,
            "held_out_pair15_absent": True,
            "legacy_structural_projection_sha256": _digest(projection),
            "legacy_structural_projection_is_host_observation": False,
            "legacy_runtime_authority_inherited": False,
            "single_use_attempt_consumed": False,
            "pair09_candidate_execution_authorized": False,
            "pair09_candidate_execution_performed": False,
            "runtime_started": False,
            "model_load_performed": False,
            "model_inference_performed": False,
            "game_execution_performed": False,
            "training_performed": False,
            "weights_updated": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
            "independent_host_attestation": False,
            "atomic_host_snapshot": False,
            "next_gate": (
                "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
            ),
        }
    except V2R13Pair09CandidateHostPreflightHold:
        raise
    except OSError:
        raise V2R13Pair09CandidateHostPreflightHold(
            "PAIR09_CANDIDATE_PREFLIGHT_FILESYSTEM_OBSERVATION_HOLD"
        ) from None
