"""Explicit one-shot pair-03 candidate invocation on the designated Precision.

Import does not collect, reserve, materialize or execute. Only the dedicated
per-call confirmation enters the operational path. It is a trusted local
operator decision, NOT cryptographic authentication or a stored runtime permit.
The existing executor owns preload/readiness/start/cleanup; this module composes
its candidate-specific gates without changing accepted baseline globals.

The OS, Python import environment and cooperative same-UID namespace are trusted.
File identity checks are observations, not atomic executed-code custody or
protection against deletion/rollback of the persistent attempt directory.
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
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2 as request,
)

CONFIRM_TOKEN = "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_CANDIDATE_ONCE"
SCHEMA = "void.abaddon.generation2.v2r13-pair03-candidate-invocation.v1"
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
ISOLATED_ROOT = Path("/home/zoso/dev/void-war-college-execution/v2r13-generation2")
CANDIDATE_ROOT = ISOLATED_ROOT / "generation2/pair-03/candidate"
CLAIMS_NAME = "pair03-candidate-claims-v1"
RESULT_NAME = "pair-03-candidate-execution-result-v1.json"
REVOCATION_NAME = "REVOKE_V2R13"
PROTO_PYTHON = Path("/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python")
LEGACY_RUNNER = Path("/home/zoso/Downloads/void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py")
LEGACY_RUNNER_SHA256 = "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
CANDIDATE_FIXTURE = "fixtures/learning/abaddon-policy-genome-generation-2-candidate-252.json"
PREFIX = "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_"
SELF_PATH = PREFIX + "pair03_candidate_invocation_generation2.py"
PINNED_SOURCES = (
    (PREFIX + "pair03_candidate_authorization_request_generation2.py", "07516a24553b2516b859bebca21818c0bd0bf01e"),
    (PREFIX + "pair03_candidate_attempt_guard_generation2.py", "b47a2befd6d7181aa5a00805ae20e66293625d45"),
    (PREFIX + "pair03_candidate_host_preflight_generation2.py", "32c27cacdcd850022bd3de358f82554112c6fd7b"),
    (PREFIX + "pair03_candidate_git_backend_generation2.py", "fe578c66b14e08c64e9281a808064b8c8d5e739a"),
    (PREFIX + "host_preflight_generation2.py", "0ae27981a08b27083b235ae4807705c88da259a1"),
    ("tools/abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2.py", "62d8a906ea41138b5443ba3bf96799b6e430b5be"),
)
MAX_SOURCE_BYTES = 1024 * 1024
MAX_RESULT_BYTES = 1024 * 1024


class CandidateInvocationHold(RuntimeError):
    """Stop without retrying; an already consumed slot is never reset."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise CandidateInvocationHold(code)


def _hex(value: Any, size: int) -> bool:
    return type(value) is str and len(value) == size and all(c in "0123456789abcdef" for c in value)


def _bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_bytes(value)).hexdigest()


def _components():
    # Lazy loading is deliberate: invalid/absent confirmation cannot reach host
    # collection or import the runtime composition graph.
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2 as baseline,
        abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2 as executor,
        abaddon_policy_campaign_runtime_v2r13_pair03_candidate_attempt_guard_generation2 as attempt,
        abaddon_policy_campaign_runtime_v2r13_pair03_candidate_host_preflight_generation2 as preflight,
        abaddon_policy_campaign_runtime_v2r13_pair03_candidate_git_backend_generation2 as git,
    )
    return SimpleNamespace(baseline=baseline, executor=executor, attempt=attempt, preflight=preflight, git=git)


def _check_python() -> None:
    _require(sys.dont_write_bytecode is True, "CANDIDATE_BYTECODE_DISABLED_REQUIRED")
    # Matching resolved binaries is insufficient: the system interpreter and a
    # venv symlink can resolve to the same executable with different packages.
    _require(Path(sys.executable) == PROTO_PYTHON
             and Path(sys.prefix) == PROTO_PYTHON.parent.parent
             and sys.prefix != sys.base_prefix, "CANDIDATE_ISOLATED_PYTHON_REQUIRED")


def _read_file(path: Path, maximum: int, preflight) -> bytes:
    with preflight._open_directory(path.parent) as parent:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=parent)
        try:
            before = os.fstat(fd)
            _require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                     and 0 < before.st_size <= maximum, "CANDIDATE_FILE_SHAPE_HOLD")
            raw = bytearray()
            for _ in range(1024):
                if len(raw) == before.st_size:
                    break
                chunk = os.read(fd, min(65536, before.st_size - len(raw)))
                _require(bool(chunk), "CANDIDATE_FILE_SHORT_READ")
                raw.extend(chunk)
            _require(len(raw) == before.st_size and os.read(fd, 1) == b"", "CANDIDATE_FILE_READ_BOUND")
            _require(preflight._identity(before) == preflight._identity(os.fstat(fd)) == preflight._identity(
                os.stat(path.name, dir_fd=parent, follow_symlinks=False)), "CANDIDATE_FILE_CHANGED")
            return bytes(raw)
        finally:
            os.close(fd)


def _verify_sources(parts, expected_self_sha256: str) -> dict[str, str]:
    _require(Path(__file__) == SOURCE_ROOT / SELF_PATH, "CANDIDATE_INVOCATION_ORIGIN_HOLD")
    for module, suffix in (
        (request, "pair03_candidate_authorization_request_generation2.py"),
        (parts.attempt, "pair03_candidate_attempt_guard_generation2.py"),
        (parts.preflight, "pair03_candidate_host_preflight_generation2.py"),
        (parts.git, "pair03_candidate_git_backend_generation2.py"),
        (parts.baseline, "first_baseline_invocation_generation2.py"),
        (parts.executor, "bounded_executor_generation2.py"),
    ):
        _require(Path(module.__file__) == SOURCE_ROOT / (PREFIX + suffix), "CANDIDATE_DEPENDENCY_ORIGIN_HOLD")
    own = _read_file(SOURCE_ROOT / SELF_PATH, MAX_SOURCE_BYTES, parts.preflight)
    _require(hashlib.sha256(own).hexdigest() == expected_self_sha256, "CANDIDATE_INVOCATION_SOURCE_DRIFT")
    identities = {}
    for relative, expected_blob in (*request.SOURCE_REFERENCES, *PINNED_SOURCES):
        raw = _read_file(SOURCE_ROOT / relative, MAX_SOURCE_BYTES, parts.preflight)
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        _require(actual == expected_blob, "CANDIDATE_DEPENDENCY_SOURCE_DRIFT")
        identities[relative] = actual
    return identities


def _current_main(backend, expected_head: str) -> dict[str, str]:
    def query(*args):
        result = backend.run_git(str(SOURCE_ROOT), *args)
        _require(result.returncode == 0, "CANDIDATE_MAIN_QUERY_HOLD")
        return result.stdout.strip()
    _require(query("symbolic-ref", "-q", "HEAD") == "refs/heads/main", "CANDIDATE_MAIN_BRANCH_HOLD")
    head, tree = query("rev-parse", "HEAD"), query("rev-parse", "HEAD^{tree}")
    _require(head == expected_head and _hex(tree, 40), "CANDIDATE_MAIN_IDENTITY_HOLD")
    # Match the accepted tracked-clean policy; ordinary untracked caches are not
    # removed or misreported as tracked changes. Git quotes embedded newlines.
    rows = query("status", "--porcelain", "--untracked-files=all").splitlines()
    _require(all(row.startswith("?? ") for row in rows), "CANDIDATE_TRACKED_SOURCE_DIRTY")
    return {"head": head, "tree": tree}


def _not_revoked(preflight) -> None:
    with preflight._open_directory(ISOLATED_ROOT) as directory:
        try:
            os.stat(REVOCATION_NAME, dir_fd=directory, follow_symlinks=False)
        except FileNotFoundError:
            return
    raise CandidateInvocationHold("CANDIDATE_EXECUTION_REVOKED")


def _baseline_files(preflight) -> dict[str, Any]:
    return {name: preflight._read_baseline_file(name, digest, cap)
            for name, digest, cap in preflight.BASELINE_FILES}


@contextmanager
def _claims_directory(preflight):
    # A fixed namespace outside all arm paths; never remove/recreate/reset it.
    with preflight._open_directory(ISOLATED_ROOT) as parent:
        try:
            os.mkdir(CLAIMS_NAME, 0o700, dir_fd=parent)
        except FileExistsError:
            pass
        fd = os.open(CLAIMS_NAME, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)
        try:
            observed = os.fstat(fd)
            _require(observed.st_uid == os.geteuid() and stat.S_IMODE(observed.st_mode) == 0o700,
                     "CANDIDATE_CLAIMS_DIRECTORY_HOLD")
            os.fsync(parent)
            yield fd, (observed.st_dev, observed.st_ino)
        finally:
            os.close(fd)


def _write_result(directory_fd: int, result: dict[str, Any], preflight) -> str:
    raw = _bytes(result) + b"\n"
    _require(len(raw) <= MAX_RESULT_BYTES, "CANDIDATE_RESULT_SIZE_HOLD")
    fd = os.open(RESULT_NAME, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                 0o600, dir_fd=directory_fd)
    try:
        os.fchmod(fd, 0o600)
        offset = 0
        for _ in range(1024):
            if offset == len(raw):
                break
            count = os.write(fd, raw[offset:])
            _require(0 < count <= len(raw) - offset, "CANDIDATE_RESULT_WRITE_HOLD")
            offset += count
        _require(offset == len(raw), "CANDIDATE_RESULT_WRITE_BOUND")
        before = os.fstat(fd)
        _require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size == len(raw),
                 "CANDIDATE_RESULT_FILE_HOLD")
        os.fsync(fd)
        os.fsync(directory_fd)
        os.lseek(fd, 0, os.SEEK_SET)
        copied = bytearray()
        for _ in range(1024):
            if len(copied) == len(raw):
                break
            chunk = os.read(fd, min(65536, len(raw) - len(copied)))
            _require(bool(chunk), "CANDIDATE_RESULT_SHORT_READ")
            copied.extend(chunk)
        _require(bytes(copied) == raw and os.read(fd, 1) == b"", "CANDIDATE_RESULT_READBACK_HOLD")
        _require(preflight._identity(before) == preflight._identity(os.fstat(fd)) == preflight._identity(
            os.stat(RESULT_NAME, dir_fd=directory_fd, follow_symlinks=False)), "CANDIDATE_RESULT_CHANGED")
    finally:
        os.close(fd)  # Failure cannot return success; uncertain files stay put.
    return hashlib.sha256(raw).hexdigest()


def _expected_candidate_binding() -> dict[str, str]:
    pinned = request.candidate_authorization_request_contract()["request"]["candidate_reference"]
    return {"candidate_file_sha256": pinned["fixture_sha256"],
            "candidate_genome_sha256": pinned["semantic_genome_sha256"],
            "wrapper_sha256": pinned["wrapper_sha256"], "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
            "abaddon_controller_sha256": pinned["controller_sha256"], "abaddon_refiner_sha256": pinned["refiner_sha256"]}


def _validate_execution(receipt: Any) -> None:
    _require(type(receipt) is dict and receipt.get("schema") == "void.abaddon.generation2.v2r13-bounded-runtime-execution-receipt.v1",
             "CANDIDATE_EXECUTOR_RECEIPT_HOLD")
    _require(type(receipt.get("pair_slot")) is int and receipt["pair_slot"] == 3
             and receipt.get("arm") == "candidate" and receipt.get("held_out") is False,
             "CANDIDATE_EXECUTOR_SCOPE_HOLD")
    for field in ("runtime_execution_authorized", "runtime_execution_performed", "runtime_started",
                  "runtime_cleanup_attempted", "runtime_cleanup_completed", "fresh_runtime_readiness_admitted",
                  "revocation_checked_before_materialization", "revocation_checked_before_inference"):
        _require(receipt.get(field) is True, "CANDIDATE_EXECUTOR_COMPLETION_HOLD:" + field)
    for field in ("automatic_retry", "training_performed", "weights_updated", "automatic_policy_promotion",
                  "deployment_performed", "void_chain_mutation_performed", "wallet_or_funds_action_performed"):
        _require(receipt.get(field) is False, "CANDIDATE_EXECUTOR_BOUNDARY_HOLD:" + field)
    _require(receipt.get("candidate_binding") == _expected_candidate_binding(), "CANDIDATE_POLICY_BINDING_HOLD")
    _require(receipt.get("execution_receipt_sha256") == _digest({
        key: value for key, value in receipt.items() if key != "execution_receipt_sha256"
    }), "CANDIDATE_EXECUTOR_DIGEST_HOLD")
    artifact = receipt.get("run_artifact")
    _require(type(artifact) is dict, "CANDIDATE_ARTIFACT_HOLD")
    run_id = artifact.get("run_id")
    _require(type(run_id) is str and 0 < len(run_id) <= 128 and run_id not in {".", ".."}
             and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_." for c in run_id),
             "CANDIDATE_RUN_ID_HOLD")
    _require(artifact.get("run_dir") == str(CANDIDATE_ROOT / "runs" / run_id), "CANDIDATE_RUN_PATH_HOLD")
    for name in ("warm_start_sha256", "trajectory_sha256", "summary_sha256"):
        _require(_hex(artifact.get(name), 64), "CANDIDATE_ARTIFACT_DIGEST_HOLD")


def execute_pair03_candidate(*, expected_main_head: str, expected_invocation_source_sha256: str,
                             confirm: str) -> dict[str, Any]:
    """Perform one explicitly confirmed candidate attempt; never retry or promote.

    No external authority flag, evidence packet, callback, path override or
    historical six-arm permit is accepted. Only a trusted operator should call
    this after exact-head source acceptance. Failed calls can leave a consumed
    marker and runtime evidence; automatic re-entry is forbidden by that marker.
    """
    _require(type(confirm) is str and confirm == CONFIRM_TOKEN, "CANDIDATE_SPECIFIC_CONFIRMATION_REQUIRED")
    _require(_hex(expected_main_head, 40) and _hex(expected_invocation_source_sha256, 64), "CANDIDATE_EXPECTED_SOURCE_INVALID")
    _check_python()
    parts = _components()
    sources = _verify_sources(parts, expected_invocation_source_sha256)
    backend = parts.git.CandidateGitBackend(confirm=parts.git.CONFIRM_TOKEN)
    main = _current_main(backend, expected_main_head)
    _not_revoked(parts.preflight)
    _require(parts.baseline._sudo_cache_ready() is True, "CACHED_SUDO_AUTHORITY_REQUIRED")
    observed = parts.preflight.collect_pair03_candidate_host_preflight(
        expected_main_head=expected_main_head, confirm=parts.preflight.CONFIRM_TOKEN)
    _require(type(observed) is dict and observed.get("candidate_host_conditions_validated") is True
             and observed.get("expected_main_head") == expected_main_head
             and observed.get("completed_baseline_preserved") is True
             and observed.get("legacy_runtime_authority_inherited") is False
             and observed.get("candidate_execution_authorized") is False
             and observed.get("single_use_attempt_consumed") is False,
             "CANDIDATE_PREFLIGHT_ADMISSION_HOLD")
    _require(observed.get("observed_host_snapshot_sha256") == _digest(observed.get("observed_host_snapshot")),
             "CANDIDATE_PREFLIGHT_DIGEST_HOLD")
    baseline = _baseline_files(parts.preflight)
    _require(baseline == observed.get("baseline_files"), "CANDIDATE_BASELINE_OBSERVATION_DRIFT")

    def authority(pair_slot: int, arm: str) -> bool:
        if type(pair_slot) is not int or pair_slot != 3 or type(arm) is not str or arm != "candidate":
            return False
        try:
            _not_revoked(parts.preflight)
            return (_current_main(backend, expected_main_head) == main
                    and _verify_sources(parts, expected_invocation_source_sha256) == sources
                    and _baseline_files(parts.preflight) == baseline)
        except Exception:
            return False

    def readiness(context: Mapping[str, Any]) -> Mapping[str, Any]:
        _require(isinstance(context, Mapping) and type(context.get("pair_slot")) is int
                 and context["pair_slot"] == 3 and context.get("arm") == "candidate"
                 and context.get("runtime_selection_key") == "apollyon-v2r13-qualified-predecessor",
                 "CANDIDATE_READINESS_CONTEXT_HOLD")
        _require(authority(3, "candidate") is True, "CANDIDATE_REVOKED_BEFORE_READINESS")
        return parts.baseline._fresh_readiness_provider(context)

    _require(authority(3, "candidate") is True, "CANDIDATE_REVOKED_BEFORE_CONSUMPTION")
    with _claims_directory(parts.preflight) as (directory, identity):
        try:
            os.stat(RESULT_NAME, dir_fd=directory, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            raise CandidateInvocationHold("CANDIDATE_PRIOR_RESULT_PRESENT")
        consumed = parts.attempt.consume_candidate_attempt(
            directory_fd=directory, expected_directory_identity=identity,
            request_bytes=request.build_candidate_authorization_request(),
            invocation_source_sha256=expected_invocation_source_sha256,
            confirm=parts.attempt.CLAIM_CONFIRMATION)
        _require(consumed.get("single_use_slot_consumed") is True
                 and consumed.get("request_sha256") == parts.attempt.REQUEST_SHA256
                 and consumed.get("directory_identity") == identity
                 and consumed.get("candidate_execution_authorized") is False,
                 "CANDIDATE_ATTEMPT_CONSUMPTION_HOLD")
        _require(authority(3, "candidate") is True, "CANDIDATE_REVOKED_AFTER_CONSUMPTION")
        receipt = parts.executor.execute_v2r13_arm(
            pair_slot=3, arm="candidate", isolated_workdir_root=str(ISOLATED_ROOT),
            source_repository_root=str(SOURCE_ROOT), engine_repository_root=str(SOURCE_ROOT / "OpenRA"),
            legacy_runner_path=str(LEGACY_RUNNER), candidate_genome_path=str(SOURCE_ROOT / CANDIDATE_FIXTURE),
            execution_authorized=True, authority_check=authority, readiness_provider=readiness,
            path_exists=backend.path_exists, run_git=backend.run_git)
        _validate_execution(receipt)
        _require(_baseline_files(parts.preflight) == baseline, "CANDIDATE_BASELINE_CHANGED_AFTER_EXECUTION")
        result = {"schema": SCHEMA, "pair_slot": 3, "arm": "candidate", "held_out": False,
                  "expected_main_head": expected_main_head, "main_tree": main["tree"],
                  "invocation_source_sha256": expected_invocation_source_sha256,
                  "source_bindings_sha256": _digest(sources),
                  "candidate_specific_call_confirmed": True, "operator_authenticated": False,
                  "single_use_attempt": deepcopy(consumed), "host_preflight": deepcopy(observed),
                  "candidate_execution_performed": True, "completed_baseline_preserved": True,
                  "automatic_retry": False, "policy_promotion_performed": False,
                  "executor_receipt": deepcopy(receipt)}
        result_sha = _write_result(directory, result, parts.preflight)
    return {**result, "result_file": str(ISOLATED_ROOT / CLAIMS_NAME / RESULT_NAME), "result_file_sha256": result_sha}
