"""Explicit one-shot V2R13 pair-09 baseline invocation.

Import performs no host observation, marker consumption, materialization, model
load, game execution, or runtime action.

Operational execution requires BOTH:
* an explicit per-call authorization_accepted=True decision; and
* the exact pair-09 baseline confirmation token.

Those inputs represent a trusted local operator decision, not cryptographic
authentication or a reusable permit. Before the durable attempt marker is
consumed, the invocation revalidates exact current main, source identities,
revocation, cached sudo, the reviewed read-only host preflight, and preserved
pair-03 evidence. After consumption there is no automatic retry or reset path.
"""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from types import SimpleNamespace
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_generation2
    as request,
)

CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR09_BASELINE_ONCE"
)
SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-invocation.v1"
)
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
ISOLATED_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2"
)
ARM_ROOT = ISOLATED_ROOT / "generation2/pair-09/baseline"
CLAIMS_NAME = "pair09-baseline-claims-v1"
RESULT_NAME = "pair-09-baseline-execution-result-v1.json"
REVOCATION_NAME = "REVOKE_V2R13"
PROTO_PYTHON = Path(
    "/home/zoso/.local/share/void-tools/"
    "openra-bridge-proto-v1/venv/bin/python"
)
LEGACY_RUNNER = Path(
    "/home/zoso/Downloads/"
    "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
)
LEGACY_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

PREFIX = "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_"
SELF_PATH = PREFIX + "pair09_baseline_invocation_generation2.py"

PINNED_SOURCES = (
    (
        PREFIX + "pair09_baseline_authorization_request_generation2.py",
        "8d49f5fbc73c574884e1e262eb929395551b6419",
    ),
    (
        PREFIX
        + "pair09_baseline_authorization_request_"
        "source_binding_review_generation2.py",
        "8342290da226a053e56a328885bd80bb5a77587f",
    ),
    (
        PREFIX + "pair09_baseline_attempt_guard_generation2.py",
        "4f3a470247196dde8fd7b7ad4807f1025adfb9b8",
    ),
    (
        PREFIX
        + "pair09_baseline_attempt_guard_"
        "source_binding_review_generation2.py",
        "7770954472ebd9abd7f51020ed352dea9adb6df2",
    ),
    (
        PREFIX + "pair09_baseline_host_preflight_generation2.py",
        "fc40d30be98db04fa783ab0534e8ab8eb869ce2d",
    ),
    (
        PREFIX
        + "pair09_baseline_host_preflight_"
        "source_binding_review_generation2.py",
        "01f95aee884a699b3e46472c3a12bfbfb0c3332d",
    ),
    (
        PREFIX + "pair09_baseline_git_backend_generation2.py",
        "9be2736081b67895faa9ecb5c4d978445a9f4a32",
    ),
    (
        PREFIX
        + "pair09_baseline_git_backend_"
        "source_binding_review_generation2.py",
        "680b24865b43041c5d3719aa0fc13e4ba3f318b8",
    ),
    (
        PREFIX + "first_baseline_invocation_generation2.py",
        "5b790efaf4085deb15eaef538635fd11f5cad9a5",
    ),
    (
        PREFIX + "bounded_executor_generation2.py",
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd",
    ),
    (
        PREFIX + "host_preflight_generation2.py",
        "0ae27981a08b27083b235ae4807705c88da259a1",
    ),
    (
        "tools/"
        "abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_"
        "generation2.py",
        "62d8a906ea41138b5443ba3bf96799b6e430b5be",
    ),
)

MAX_SOURCE_BYTES = 1024 * 1024
MAX_RESULT_BYTES = 1024 * 1024


class V2R13Pair09BaselineInvocationHold(RuntimeError):
    """Stop without automatic retry; consumed attempts are never reset."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise V2R13Pair09BaselineInvocationHold(code)


def _hex(value: Any, size: int) -> bool:
    return (
        type(value) is str
        and len(value) == size
        and all(c in "0123456789abcdef" for c in value)
    )


def _bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=str,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_bytes(value)).hexdigest()


def _components():
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
        as baseline,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
        as executor,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_generation2
        as attempt,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_source_binding_review_generation2
        as attempt_review,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_generation2
        as preflight,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_host_preflight_source_binding_review_generation2
        as preflight_review,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_git_backend_generation2
        as git,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_git_backend_source_binding_review_generation2
        as git_review,
    )
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_source_binding_review_generation2
        as request_review,
    )

    return SimpleNamespace(
        baseline=baseline,
        executor=executor,
        attempt=attempt,
        attempt_review=attempt_review,
        preflight=preflight,
        preflight_review=preflight_review,
        git=git,
        git_review=git_review,
        request_review=request_review,
    )


def _validate_source_chain(parts) -> None:
    request_review = (
        parts.request_review
        .v2r13_pair09_baseline_authorization_request_review_contract()
    )
    attempt_review = (
        parts.attempt_review
        .v2r13_pair09_baseline_attempt_guard_review_contract()
    )
    preflight_review = (
        parts.preflight_review
        .v2r13_pair09_baseline_host_preflight_review_contract()
    )
    git_review = (
        parts.git_review
        .v2r13_pair09_baseline_git_backend_review_contract()
    )

    _require(
        request_review.get(
            "pair09_baseline_authorization_request_reviewed"
        )
        is True,
        "PAIR09_INVOCATION_REQUEST_REVIEW_HOLD",
    )
    _require(
        attempt_review.get("pair09_baseline_attempt_guard_reviewed") is True,
        "PAIR09_INVOCATION_ATTEMPT_REVIEW_HOLD",
    )
    _require(
        preflight_review.get("pair09_baseline_host_preflight_reviewed")
        is True,
        "PAIR09_INVOCATION_PREFLIGHT_REVIEW_HOLD",
    )
    _require(
        git_review.get("pair09_baseline_git_backend_reviewed") is True,
        "PAIR09_INVOCATION_GIT_REVIEW_HOLD",
    )

    for reviewed in (
        request_review,
        attempt_review,
        preflight_review,
    ):
        _require(
            reviewed.get("pair09_baseline_execution_authorized") is False,
            "PAIR09_INVOCATION_PREMATURE_RUNTIME_AUTHORITY",
        )
    _require(
        git_review.get("runtime_execution_authorized") is False,
        "PAIR09_INVOCATION_PREMATURE_RUNTIME_AUTHORITY",
    )


def _check_python() -> None:
    _require(
        sys.dont_write_bytecode is True,
        "PAIR09_INVOCATION_BYTECODE_DISABLED_REQUIRED",
    )
    _require(
        Path(sys.executable) == PROTO_PYTHON
        and Path(sys.prefix) == PROTO_PYTHON.parent.parent
        and sys.prefix != sys.base_prefix,
        "PAIR09_INVOCATION_ISOLATED_PYTHON_REQUIRED",
    )


def _read_file(path: Path, maximum: int, preflight) -> bytes:
    with preflight._open_directory(path.parent) as parent:
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
                "PAIR09_INVOCATION_FILE_SHAPE_HOLD",
            )
            raw = bytearray()
            for _ in range(2048):
                if len(raw) == before.st_size:
                    break
                chunk = os.read(
                    fd,
                    min(65536, before.st_size - len(raw)),
                )
                _require(
                    bool(chunk),
                    "PAIR09_INVOCATION_FILE_SHORT_READ",
                )
                raw.extend(chunk)
            _require(
                len(raw) == before.st_size
                and os.read(fd, 1) == b"",
                "PAIR09_INVOCATION_FILE_READ_BOUND",
            )
            named = os.stat(
                path.name,
                dir_fd=parent,
                follow_symlinks=False,
            )
            _require(
                preflight._identity(before)
                == preflight._identity(os.fstat(fd))
                == preflight._identity(named),
                "PAIR09_INVOCATION_FILE_CHANGED",
            )
            return bytes(raw)
        finally:
            os.close(fd)


def _verify_sources(
    parts,
    expected_self_sha256: str,
) -> dict[str, str]:
    _require(
        Path(__file__) == SOURCE_ROOT / SELF_PATH,
        "PAIR09_INVOCATION_ORIGIN_HOLD",
    )

    expected_modules = (
        (
            request,
            "pair09_baseline_authorization_request_generation2.py",
        ),
        (
            parts.attempt,
            "pair09_baseline_attempt_guard_generation2.py",
        ),
        (
            parts.preflight,
            "pair09_baseline_host_preflight_generation2.py",
        ),
        (
            parts.git,
            "pair09_baseline_git_backend_generation2.py",
        ),
        (
            parts.baseline,
            "first_baseline_invocation_generation2.py",
        ),
        (
            parts.executor,
            "bounded_executor_generation2.py",
        ),
    )
    for module, suffix in expected_modules:
        _require(
            Path(module.__file__) == SOURCE_ROOT / (PREFIX + suffix),
            "PAIR09_INVOCATION_DEPENDENCY_ORIGIN_HOLD",
        )

    own = _read_file(
        SOURCE_ROOT / SELF_PATH,
        MAX_SOURCE_BYTES,
        parts.preflight,
    )
    _require(
        hashlib.sha256(own).hexdigest() == expected_self_sha256,
        "PAIR09_INVOCATION_SOURCE_DRIFT",
    )

    identities = {}
    for relative, expected_blob in PINNED_SOURCES:
        raw = _read_file(
            SOURCE_ROOT / relative,
            MAX_SOURCE_BYTES,
            parts.preflight,
        )
        actual = hashlib.sha1(
            b"blob "
            + str(len(raw)).encode()
            + b"\0"
            + raw
        ).hexdigest()
        _require(
            actual == expected_blob,
            "PAIR09_INVOCATION_DEPENDENCY_SOURCE_DRIFT",
        )
        identities[relative] = actual

    return identities


def _current_main(backend, expected_head: str) -> dict[str, str]:
    def query(*args):
        result = backend.run_git(str(SOURCE_ROOT), *args)
        _require(
            result.returncode == 0,
            "PAIR09_INVOCATION_MAIN_QUERY_HOLD",
        )
        return result.stdout.strip()

    _require(
        query("symbolic-ref", "-q", "HEAD") == "refs/heads/main",
        "PAIR09_INVOCATION_MAIN_BRANCH_HOLD",
    )
    head = query("rev-parse", "HEAD")
    tree = query("rev-parse", "HEAD^{tree}")
    _require(
        head == expected_head and _hex(tree, 40),
        "PAIR09_INVOCATION_MAIN_IDENTITY_HOLD",
    )
    rows = query(
        "status",
        "--porcelain",
        "--untracked-files=all",
    ).splitlines()
    _require(
        all(row.startswith("?? ") for row in rows),
        "PAIR09_INVOCATION_TRACKED_SOURCE_DIRTY",
    )
    return {"head": head, "tree": tree}


def _not_revoked(preflight) -> None:
    with preflight._open_directory(ISOLATED_ROOT) as directory:
        try:
            os.stat(
                REVOCATION_NAME,
                dir_fd=directory,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            return
    raise V2R13Pair09BaselineInvocationHold(
        "PAIR09_INVOCATION_EXECUTION_REVOKED"
    )


def _preserved_pair03(preflight) -> dict[str, Any]:
    return {
        str(relative): preflight._read_preserved_file(
            relative,
            digest,
            maximum,
        )
        for relative, digest, maximum in preflight.PRESERVED_FILES
    }


@contextmanager
def _claims_directory(preflight):
    with preflight._open_directory(ISOLATED_ROOT) as parent:
        try:
            os.mkdir(
                CLAIMS_NAME,
                0o700,
                dir_fd=parent,
            )
        except FileExistsError:
            pass

        fd = os.open(
            CLAIMS_NAME,
            os.O_RDONLY
            | os.O_DIRECTORY
            | os.O_NOFOLLOW
            | os.O_CLOEXEC,
            dir_fd=parent,
        )
        try:
            observed = os.fstat(fd)
            _require(
                observed.st_uid == os.geteuid()
                and stat.S_IMODE(observed.st_mode) == 0o700,
                "PAIR09_INVOCATION_CLAIMS_DIRECTORY_HOLD",
            )
            os.fsync(parent)
            yield fd, (observed.st_dev, observed.st_ino)
        finally:
            os.close(fd)


def _write_result(
    directory_fd: int,
    result: dict[str, Any],
    preflight,
) -> str:
    raw = _bytes(result) + b"\n"
    _require(
        len(raw) <= MAX_RESULT_BYTES,
        "PAIR09_INVOCATION_RESULT_SIZE_HOLD",
    )

    fd = os.open(
        RESULT_NAME,
        os.O_RDWR
        | os.O_CREAT
        | os.O_EXCL
        | os.O_NOFOLLOW
        | os.O_CLOEXEC,
        0o600,
        dir_fd=directory_fd,
    )
    try:
        os.fchmod(fd, 0o600)
        offset = 0
        for _ in range(2048):
            if offset == len(raw):
                break
            count = os.write(fd, raw[offset:])
            _require(
                0 < count <= len(raw) - offset,
                "PAIR09_INVOCATION_RESULT_WRITE_HOLD",
            )
            offset += count
        _require(
            offset == len(raw),
            "PAIR09_INVOCATION_RESULT_WRITE_BOUND",
        )

        before = os.fstat(fd)
        _require(
            stat.S_ISREG(before.st_mode)
            and before.st_nlink == 1
            and before.st_size == len(raw),
            "PAIR09_INVOCATION_RESULT_FILE_HOLD",
        )
        os.fsync(fd)
        os.fsync(directory_fd)
        os.lseek(fd, 0, os.SEEK_SET)

        copied = bytearray()
        for _ in range(2048):
            if len(copied) == len(raw):
                break
            chunk = os.read(
                fd,
                min(65536, len(raw) - len(copied)),
            )
            _require(
                bool(chunk),
                "PAIR09_INVOCATION_RESULT_SHORT_READ",
            )
            copied.extend(chunk)

        _require(
            bytes(copied) == raw
            and os.read(fd, 1) == b"",
            "PAIR09_INVOCATION_RESULT_READBACK_HOLD",
        )
        named = os.stat(
            RESULT_NAME,
            dir_fd=directory_fd,
            follow_symlinks=False,
        )
        _require(
            preflight._identity(before)
            == preflight._identity(os.fstat(fd))
            == preflight._identity(named),
            "PAIR09_INVOCATION_RESULT_CHANGED",
        )
    finally:
        os.close(fd)

    return hashlib.sha256(raw).hexdigest()


def _validate_execution(receipt: Any) -> None:
    _require(
        type(receipt) is dict
        and receipt.get("schema")
        == (
            "void.abaddon.generation2."
            "v2r13-bounded-runtime-execution-receipt.v1"
        ),
        "PAIR09_INVOCATION_EXECUTOR_RECEIPT_HOLD",
    )
    _require(
        type(receipt.get("pair_slot")) is int
        and receipt["pair_slot"] == 9
        and receipt.get("arm") == "baseline"
        and receipt.get("held_out") is False,
        "PAIR09_INVOCATION_EXECUTOR_SCOPE_HOLD",
    )

    for field in (
        "runtime_execution_authorized",
        "runtime_execution_performed",
        "runtime_started",
        "runtime_cleanup_attempted",
        "runtime_cleanup_completed",
        "fresh_runtime_readiness_admitted",
        "revocation_checked_before_materialization",
        "revocation_checked_before_inference",
    ):
        _require(
            receipt.get(field) is True,
            "PAIR09_INVOCATION_EXECUTOR_COMPLETION_HOLD:" + field,
        )

    for field in (
        "automatic_retry",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(
            receipt.get(field) is False,
            "PAIR09_INVOCATION_EXECUTOR_BOUNDARY_HOLD:" + field,
        )

    _require(
        receipt.get("candidate_binding") is None,
        "PAIR09_INVOCATION_BASELINE_CANDIDATE_BINDING_HOLD",
    )
    _require(
        receipt.get("execution_receipt_sha256")
        == _digest(
            {
                key: value
                for key, value in receipt.items()
                if key != "execution_receipt_sha256"
            }
        ),
        "PAIR09_INVOCATION_EXECUTOR_DIGEST_HOLD",
    )

    artifact = receipt.get("run_artifact")
    _require(
        type(artifact) is dict,
        "PAIR09_INVOCATION_ARTIFACT_HOLD",
    )
    run_id = artifact.get("run_id")
    _require(
        type(run_id) is str
        and 0 < len(run_id) <= 128
        and run_id not in {".", ".."}
        and all(
            c
            in (
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "abcdefghijklmnopqrstuvwxyz"
                "0123456789-_."
            )
            for c in run_id
        ),
        "PAIR09_INVOCATION_RUN_ID_HOLD",
    )
    _require(
        artifact.get("run_dir")
        == str(ARM_ROOT / "runs" / run_id),
        "PAIR09_INVOCATION_RUN_PATH_HOLD",
    )
    for name in (
        "warm_start_sha256",
        "trajectory_sha256",
        "summary_sha256",
    ):
        _require(
            _hex(artifact.get(name), 64),
            "PAIR09_INVOCATION_ARTIFACT_DIGEST_HOLD",
        )


def execute_pair09_baseline(
    *,
    expected_main_head: str,
    expected_invocation_source_sha256: str,
    authorization_accepted: bool,
    confirm: str,
) -> dict[str, Any]:
    """Execute exactly one explicitly authorized pair-09 baseline attempt."""

    _require(
        authorization_accepted is True,
        "PAIR09_BASELINE_SPECIFIC_AUTHORIZATION_REQUIRED",
    )
    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "PAIR09_BASELINE_SPECIFIC_CONFIRMATION_REQUIRED",
    )
    _require(
        _hex(expected_main_head, 40)
        and _hex(expected_invocation_source_sha256, 64),
        "PAIR09_INVOCATION_EXPECTED_SOURCE_INVALID",
    )

    _check_python()
    parts = _components()
    _validate_source_chain(parts)
    sources = _verify_sources(
        parts,
        expected_invocation_source_sha256,
    )

    backend = parts.git.Pair09BaselineGitBackend(
        confirm=parts.git.CONFIRM_TOKEN
    )
    main = _current_main(backend, expected_main_head)

    _not_revoked(parts.preflight)
    _require(
        parts.baseline._sudo_cache_ready() is True,
        "CACHED_SUDO_AUTHORITY_REQUIRED",
    )

    observed = parts.preflight.collect_pair09_baseline_host_preflight(
        expected_main_head=expected_main_head,
        confirm=parts.preflight.CONFIRM_TOKEN,
    )
    _require(
        type(observed) is dict
        and observed.get(
            "pair09_baseline_host_conditions_validated"
        )
        is True
        and observed.get("expected_main_head")
        == expected_main_head
        and observed.get("pair03_baseline_preserved") is True
        and observed.get("pair03_candidate_preserved") is True
        and observed.get("pair09_baseline_absent") is True
        and observed.get("pair09_candidate_absent") is True
        and observed.get("held_out_pair15_absent") is True
        and observed.get("legacy_runtime_authority_inherited") is False
        and observed.get("single_use_attempt_consumed") is False
        and observed.get("pair09_baseline_execution_authorized") is False,
        "PAIR09_INVOCATION_PREFLIGHT_ADMISSION_HOLD",
    )
    _require(
        observed.get("observed_host_snapshot_sha256")
        == _digest(observed.get("observed_host_snapshot")),
        "PAIR09_INVOCATION_PREFLIGHT_DIGEST_HOLD",
    )

    preserved = _preserved_pair03(parts.preflight)
    _require(
        preserved == observed.get("pair03_preserved_evidence"),
        "PAIR09_INVOCATION_PRESERVED_EVIDENCE_DRIFT",
    )

    def authority(pair_slot: int, arm: str) -> bool:
        if (
            type(pair_slot) is not int
            or pair_slot != 9
            or type(arm) is not str
            or arm != "baseline"
        ):
            return False
        try:
            _not_revoked(parts.preflight)
            return (
                authorization_accepted is True
                and _current_main(backend, expected_main_head) == main
                and _verify_sources(
                    parts,
                    expected_invocation_source_sha256,
                )
                == sources
                and _preserved_pair03(parts.preflight) == preserved
            )
        except Exception:
            return False

    def readiness(
        context: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        _require(
            isinstance(context, Mapping)
            and type(context.get("pair_slot")) is int
            and context["pair_slot"] == 9
            and context.get("arm") == "baseline"
            and context.get("runtime_selection_key")
            == "apollyon-v2r13-qualified-predecessor",
            "PAIR09_INVOCATION_READINESS_CONTEXT_HOLD",
        )
        _require(
            authority(9, "baseline") is True,
            "PAIR09_INVOCATION_REVOKED_BEFORE_READINESS",
        )
        return parts.baseline._fresh_readiness_provider(context)

    _require(
        authority(9, "baseline") is True,
        "PAIR09_INVOCATION_REVOKED_BEFORE_CONSUMPTION",
    )

    with _claims_directory(parts.preflight) as (directory, identity):
        try:
            os.stat(
                RESULT_NAME,
                dir_fd=directory,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise V2R13Pair09BaselineInvocationHold(
                "PAIR09_INVOCATION_PRIOR_RESULT_PRESENT"
            )

        consumed = parts.attempt.consume_pair09_baseline_attempt(
            directory_fd=directory,
            expected_directory_identity=identity,
            request_bytes=(
                request.build_pair09_baseline_authorization_request()
            ),
            invocation_source_sha256=(
                expected_invocation_source_sha256
            ),
            confirm=parts.attempt.CLAIM_CONFIRMATION,
        )
        _require(
            consumed.get("single_use_slot_consumed") is True
            and consumed.get("directory_identity") == identity
            and consumed.get(
                "pair09_baseline_specific_authorization_accepted"
            )
            is False
            and consumed.get(
                "pair09_baseline_execution_authorized"
            )
            is False,
            "PAIR09_INVOCATION_ATTEMPT_CONSUMPTION_HOLD",
        )

        _require(
            authority(9, "baseline") is True,
            "PAIR09_INVOCATION_REVOKED_AFTER_CONSUMPTION",
        )

        receipt = parts.executor.execute_v2r13_arm(
            pair_slot=9,
            arm="baseline",
            isolated_workdir_root=str(ISOLATED_ROOT),
            source_repository_root=str(SOURCE_ROOT),
            engine_repository_root=str(SOURCE_ROOT / "OpenRA"),
            legacy_runner_path=str(LEGACY_RUNNER),
            candidate_genome_path=None,
            execution_authorized=True,
            authority_check=authority,
            readiness_provider=readiness,
            path_exists=backend.path_exists,
            run_git=backend.run_git,
        )
        _validate_execution(receipt)

        _require(
            _preserved_pair03(parts.preflight) == preserved,
            "PAIR09_INVOCATION_PAIR03_CHANGED_AFTER_EXECUTION",
        )

        result = {
            "schema": SCHEMA,
            "pair_slot": 9,
            "arm": "baseline",
            "held_out": False,
            "expected_main_head": expected_main_head,
            "main_tree": main["tree"],
            "invocation_source_sha256": (
                expected_invocation_source_sha256
            ),
            "source_bindings_sha256": _digest(sources),
            "pair09_baseline_specific_call_confirmed": True,
            "pair09_baseline_specific_authorization_accepted": True,
            "operator_authenticated": False,
            "single_use_attempt": deepcopy(consumed),
            "host_preflight": deepcopy(observed),
            "pair09_baseline_execution_performed": True,
            "pair03_baseline_preserved": True,
            "pair03_candidate_preserved": True,
            "automatic_retry": False,
            "policy_promotion_performed": False,
            "executor_receipt": deepcopy(receipt),
        }
        result_sha = _write_result(
            directory,
            result,
            parts.preflight,
        )

    return {
        **result,
        "result_file": str(
            ISOLATED_ROOT / CLAIMS_NAME / RESULT_NAME
        ),
        "result_file_sha256": result_sha,
    }


def pair09_baseline_invocation_contract() -> dict[str, Any]:
    parts = _components()
    _validate_source_chain(parts)
    return {
        "schema": SCHEMA,
        "pair09_baseline_invocation_implemented": True,
        "pair09_baseline_invocation_reviewed": False,
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "confirm_token": CONFIRM_TOKEN,
        "explicit_authorization_boolean_required": True,
        "explicit_confirmation_token_required": True,
        "operator_authentication_implemented": False,
        "exact_current_main_required": True,
        "exact_invocation_source_sha256_required": True,
        "exact_dependency_git_blobs_required": True,
        "fresh_current_main_host_preflight_required": True,
        "cached_sudo_required": True,
        "revocation_sentinel_absent_required": True,
        "isolated_grpc_python_required": True,
        "pair03_preserved_evidence_revalidation_required": True,
        "single_use_attempt_consumption_required": True,
        "fresh_live_readiness_before_inference_required": True,
        "pair09_baseline_specific_authorization_accepted": False,
        "single_use_attempt_consumed": False,
        "pair09_baseline_execution_authorized": False,
        "pair09_baseline_execution_performed": False,
        "pair09_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "runtime_execution_performed_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "game_execution_performed_by_contract_inspection": False,
        "pinned_sources": dict(PINNED_SOURCES),
        "next_gate": (
            "V2R13_PAIR09_BASELINE_INVOCATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "next_change_class": (
            "source_only_v2r13_pair09_baseline_invocation_"
            "source_binding_review"
        ),
    }
