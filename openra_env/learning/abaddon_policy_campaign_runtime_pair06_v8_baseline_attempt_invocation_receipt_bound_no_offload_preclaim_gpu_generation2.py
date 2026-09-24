"""One-shot pair-06 baseline V8 game attempt invocation.

This source closes the final implementation gap before a separate explicit
execution authorization can be accepted.

Operational order when later authorized:
1. verify exact V8 parent environment, canonical main, source identity,
   revocation state, V8 environment/assets, and empty target roots;
2. materialize the exact reviewed frozen legacy source/engine worktrees;
3. perform a fresh reviewed read-only CUDA:0 observation and require the
   pre-claim GPU admission contract to pass;
4. create the durable single-use attempt marker;
5. invoke the reviewed V8 parent supervisor with marker SHA-256 as attempt id;
6. create a durable execution-result file immediately after successful game
   completion;
7. clean only the worktrees owned by this invocation;
8. create a durable cleanup-closeout file.

The attempt marker is never deleted or reset. Any failure after its creation
consumes the attempt. Automatic retry is forbidden. Post-claim failure leaves
available worktrees/run artifacts in place except where the reviewed cleanup
has already succeeded.

Import and contract inspection perform no host I/O or execution.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Mapping

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_git_backend_generation2
    as git_backend,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as supervisor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as supervisor_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_second_failed_attempt_preservation_result_source_binding_review_generation2
    as preservation_result_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_path_inputs_generation2 as path_inputs,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2
    as materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_source_binding_review_generation2
    as materializer_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_admission_generation2
    as gpu_admission,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_readonly_observer_generation2
    as gpu_observer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_readonly_observer_source_binding_review_generation2
    as gpu_observer_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_preclaim_gpu_observation_source_binding_review_generation2
    as precision_gpu_observation_review,
)

SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-game-attempt-invocation-receipt-bound-no-offload-preclaim-gpu.v1"
)
CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-game-attempt-invocation-receipt-bound-no-offload-preclaim-gpu-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False

SOURCE_ROOT = Path(git_backend.SOURCE_ROOT)
ENGINE_REPOSITORY_ROOT = SOURCE_ROOT / "OpenRA"
ARM_ROOT = Path(git_backend.ARM_ROOT)
FROZEN_SOURCE_ROOT = Path(git_backend.FROZEN_SOURCE_ROOT)
EXACT_ENGINE_ROOT = Path(git_backend.EXACT_ENGINE_ROOT)
CLAIMS_ROOT = ARM_ROOT / "claims-v1"
RUNS_ROOT = ARM_ROOT / "runs-v1"

MARKER_NAME = "pair06-v8-baseline-game-attempt-v1.json"
RESULT_NAME = "pair06-v8-baseline-game-result-v1.json"
CLOSEOUT_NAME = "pair06-v8-baseline-game-closeout-v1.json"
REVOCATION_NAME = "REVOKE_PAIR06_V8_BASELINE_GAME"

SELF_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2.py"
)
V8_PYTHON = Path(
    "/home/zoso/Downloads/"
    "void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
)
CONFIRM_TOKEN = "VOID_PAIR06_V8_BASELINE_RECEIPT_BOUND_NO_OFFLOAD_GAME_EXECUTE_ONCE"

SUPERVISOR_REVIEW_GIT_BLOB = "6a65984b81e563def012c6da1405ad47747bb465"
SUPERVISOR_REVIEW_SOURCE_SHA256 = (
    "68422a2beef30774a43120be69e88bac6a6a3d2dd3871a7c4de1c08e1fd5cb49"
)
PRESERVATION_RESULT_REVIEW_GIT_BLOB = "16fe141898537776be87654d32f4e7b67c34e880"
PRESERVATION_RESULT_REVIEW_SOURCE_SHA256 = (
    "f22a25a097e739ca1f661f207d69b4c98d69f26227fa5a43d8c84010de91f66a"
)
MATERIALIZER_REVIEW_GIT_BLOB = "3dcc325c431ec451a737b6e228c365ce1acb4f98"
MATERIALIZER_REVIEW_SOURCE_SHA256 = (
    "b894b0b109fb943f444cfb3467249b7ed991fc8673967e271456c80d4df503fe"
)
MATERIALIZER_GIT_BLOB = "8c6fb13480e03f094f63fdb753ec19a0ce223c80"
MATERIALIZER_SOURCE_SHA256 = (
    "e1c189775b9b09d043f9e49d143d9f4ecab253ba5ea293fdf69820d0d2d86ff3"
)

NEXT_GATE = (
    "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_RECEIPT_BOUND_NO_OFFLOAD_"
    "PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_baseline_attempt_invocation_receipt_bound_"
    "no_offload_preclaim_gpu_review"
)


class Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold(message)


def _hex(value: Any, size: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == size
        and all(ch in "0123456789abcdef" for ch in value)
    )


def _stable_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _dependency_contracts() -> dict[str, Any]:
    sup = supervisor_review.pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    preservation = (
        preservation_result_review
        .pair06_v8_second_preservation_result_review_contract()
    )
    mat = materializer_review.v2r13_frozen_worktree_materializer_source_binding_review_contract()
    backend = git_backend.pair06_v8_baseline_git_backend_contract()
    gpu_observer_bound = (
        gpu_observer_review
        .pair06_v8_preclaim_gpu_readonly_observer_review_contract()
    )
    historical_gpu = (
        precision_gpu_observation_review
        .pair06_v8_precision_preclaim_gpu_observation_review_contract()
    )

    _require(
        sup.get("pair06_v8_parent_launcher_supervisor_no_offload_reviewed") is True,
        "PAIR06_V8_INVOCATION_SUPERVISOR_NOT_REVIEWED",
    )
    _require(
        sup.get("pair_slot") == PAIR_SLOT
        and sup.get("arm") == ARM
        and sup.get("execution_authorized") is False,
        "PAIR06_V8_INVOCATION_SUPERVISOR_SCOPE_DRIFT",
    )
    _require(
        sup.get("next_gate")
        == "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_REQUIRED",
        "PAIR06_V8_INVOCATION_SUPERVISOR_FRONTIER_DRIFT",
    )

    _require(
        preservation.get("pair06_v8_second_preservation_result_reviewed") is True,
        "PAIR06_V8_INVOCATION_SECOND_PRESERVATION_NOT_REVIEWED",
    )
    _require(
        preservation.get("second_failed_attempt_archived") is True
        and preservation.get("second_failed_attempt_deleted") is False
        and preservation.get("prior_failed_attempt_archive_unchanged") is True,
        "PAIR06_V8_INVOCATION_ARCHIVE_LINEAGE_DRIFT",
    )
    _require(
        preservation.get(
            "fresh_baseline_arm_root_may_be_created_by_later_authorized_attempt"
        )
        is True,
        "PAIR06_V8_INVOCATION_FRESH_ROOT_NOT_AVAILABLE",
    )
    _require(
        preservation.get("runtime_retry_authorized") is False
        and preservation.get("automatic_retry") is False,
        "PAIR06_V8_INVOCATION_PRESERVATION_RETRY_DRIFT",
    )
    _require(
        preservation.get("next_gate")
        == "PAIR06_V8_NO_OFFLOAD_BASELINE_ATTEMPT_INVOCATION_REQUIRED",
        "PAIR06_V8_INVOCATION_PRESERVATION_FRONTIER_DRIFT",
    )

    _require(
        mat.get("frozen_worktree_materializer_reviewed") is True,
        "PAIR06_V8_INVOCATION_MATERIALIZER_NOT_REVIEWED",
    )
    _require(
        mat.get("materialization_requires_explicit_authority") is True
        and mat.get("cleanup_requires_explicit_authority") is True,
        "PAIR06_V8_INVOCATION_MATERIALIZER_AUTHORITY_DRIFT",
    )
    _require(
        mat.get("runtime_execution_authorized") is False,
        "PAIR06_V8_INVOCATION_MATERIALIZER_RUNTIME_AUTHORITY_DRIFT",
    )

    _require(
        backend.get("pair_slot") == PAIR_SLOT
        and backend.get("arm") == ARM
        and backend.get("runtime_execution_authorized") is False,
        "PAIR06_V8_INVOCATION_GIT_BACKEND_SCOPE_DRIFT",
    )
    _require(
        backend.get("fetch_implemented") is False
        and backend.get("force_remove_implemented") is False,
        "PAIR06_V8_INVOCATION_GIT_BACKEND_CAPABILITY_DRIFT",
    )

    _require(
        gpu_observer_bound.get(
            "pair06_v8_preclaim_gpu_readonly_observer_reviewed"
        )
        is True,
        "PAIR06_V8_INVOCATION_GPU_OBSERVER_NOT_REVIEWED",
    )
    _require(
        gpu_observer_bound.get("pair_slot") == PAIR_SLOT
        and gpu_observer_bound.get("gpu_index") == 0
        and gpu_observer_bound.get("observation_requires_explicit_authority")
        is True,
        "PAIR06_V8_INVOCATION_GPU_OBSERVER_SCOPE_DRIFT",
    )
    _require(
        gpu_observer_bound.get("process_signal_implemented") is False
        and gpu_observer_bound.get("process_termination_implemented") is False
        and gpu_observer_bound.get("attempt_marker_creation_implemented") is False
        and gpu_observer_bound.get("runtime_load_implemented") is False,
        "PAIR06_V8_INVOCATION_GPU_OBSERVER_BOUNDARY_DRIFT",
    )

    _require(
        historical_gpu.get(
            "pair06_v8_precision_preclaim_gpu_observation_reviewed"
        )
        is True,
        "PAIR06_V8_INVOCATION_GPU_HISTORY_NOT_REVIEWED",
    )
    _require(
        historical_gpu.get("historical_observation_only") is True
        and historical_gpu.get("observation_reusable_for_future_claim") is False
        and historical_gpu.get(
            "fresh_reobservation_required_before_attempt_marker"
        )
        is True,
        "PAIR06_V8_INVOCATION_GPU_FRESHNESS_POLICY_DRIFT",
    )
    _require(
        historical_gpu.get("retry_authorized") is False
        and historical_gpu.get("attempt_marker_creation_authorized") is False
        and historical_gpu.get("runtime_load_authorized") is False
        and historical_gpu.get("game_execution_authorized") is False,
        "PAIR06_V8_INVOCATION_GPU_HISTORY_AUTHORITY_DRIFT",
    )
    _require(
        historical_gpu.get("next_gate")
        == "PAIR06_V8_PRECLAIM_GPU_INVOCATION_INTEGRATION_SOURCE_REQUIRED",
        "PAIR06_V8_INVOCATION_GPU_HISTORY_FRONTIER_DRIFT",
    )

    return {
        "supervisor_review": deepcopy(sup),
        "second_preservation_result_review": deepcopy(preservation),
        "materializer_review": deepcopy(mat),
        "git_backend": deepcopy(backend),
        "preclaim_gpu_observer_review": deepcopy(gpu_observer_bound),
        "historical_precision_gpu_observation_review": deepcopy(historical_gpu),
    }


def _check_python() -> None:
    _require(
        sys.dont_write_bytecode is True,
        "PAIR06_V8_INVOCATION_BYTECODE_DISABLED_REQUIRED",
    )
    _require(
        Path(sys.executable) == V8_PYTHON
        and Path(sys.prefix).resolve() == V8_PYTHON.parent.parent.resolve()
        and (sys.version_info.major, sys.version_info.minor) == (3, 12),
        "PAIR06_V8_INVOCATION_EXACT_V8_PYTHON_REQUIRED",
    )


def _verify_self(expected_source_sha256: str) -> str:
    source = SOURCE_ROOT / SELF_PATH
    _require(
        Path(__file__) == source,
        "PAIR06_V8_INVOCATION_ORIGIN_HOLD",
    )
    raw = source.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    _require(
        actual == expected_source_sha256,
        "PAIR06_V8_INVOCATION_SOURCE_DRIFT",
    )
    return actual


def _git(*args: str) -> str:
    proc = subprocess.run(
        ["/usr/bin/git", "-C", str(SOURCE_ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
        env={
            "PATH": "/usr/bin:/bin",
            "LC_ALL": "C",
            "LANG": "C",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_TERMINAL_PROMPT": "0",
        },
    )
    _require(
        proc.returncode == 0,
        "PAIR06_V8_INVOCATION_GIT_QUERY_HOLD",
    )
    return proc.stdout.strip()


def _current_main(expected_main_head: str) -> dict[str, str]:
    _require(
        _git("symbolic-ref", "-q", "HEAD") == "refs/heads/main",
        "PAIR06_V8_INVOCATION_MAIN_BRANCH_HOLD",
    )
    head = _git("rev-parse", "HEAD")
    tree = _git("rev-parse", "HEAD^{tree}")
    _require(
        head == expected_main_head and _hex(tree, 40),
        "PAIR06_V8_INVOCATION_MAIN_IDENTITY_HOLD",
    )
    rows = _git(
        "status",
        "--porcelain",
        "--untracked-files=all",
    ).splitlines()
    _require(
        all(row.startswith("?? ") for row in rows),
        "PAIR06_V8_INVOCATION_TRACKED_SOURCE_DIRTY",
    )
    return {"head": head, "tree": tree}


def _not_revoked() -> None:
    if (CLAIMS_ROOT / REVOCATION_NAME).exists():
        raise Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold(
            "PAIR06_V8_INVOCATION_REVOKED"
        )


def _ensure_private_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    observed = path.lstat()
    _require(
        stat.S_ISDIR(observed.st_mode)
        and not stat.S_ISLNK(observed.st_mode)
        and observed.st_uid == os.geteuid(),
        "PAIR06_V8_INVOCATION_PRIVATE_DIRECTORY_HOLD",
    )
    os.chmod(path, 0o700)
    observed = path.lstat()
    _require(
        stat.S_IMODE(observed.st_mode) == 0o700,
        "PAIR06_V8_INVOCATION_PRIVATE_DIRECTORY_MODE_HOLD",
    )
    return path


def _require_empty_directory(path: Path) -> None:
    _ensure_private_dir(path)
    _require(
        not any(path.iterdir()),
        "PAIR06_V8_INVOCATION_DIRECTORY_NOT_EMPTY",
    )


def _write_create_only(path: Path, value: Mapping[str, Any]) -> str:
    raw = _stable_bytes(value)
    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | os.O_NOFOLLOW
        | os.O_CLOEXEC
    )
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold(
            "PAIR06_V8_INVOCATION_CREATE_ONLY_COLLISION"
        ) from exc

    try:
        os.fchmod(fd, 0o600)
        offset = 0
        while offset < len(raw):
            written = os.write(fd, raw[offset:])
            _require(
                type(written) is int and written > 0,
                "PAIR06_V8_INVOCATION_WRITE_HOLD",
            )
            offset += written
        os.fsync(fd)
        observed = os.fstat(fd)
        _require(
            stat.S_ISREG(observed.st_mode)
            and observed.st_nlink == 1
            and observed.st_uid == os.geteuid()
            and stat.S_IMODE(observed.st_mode) == 0o600
            and observed.st_size == len(raw),
            "PAIR06_V8_INVOCATION_FILE_SHAPE_HOLD",
        )
    finally:
        os.close(fd)

    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path: Path) -> str:
    observed = path.lstat()
    _require(
        stat.S_ISREG(observed.st_mode)
        and not stat.S_ISLNK(observed.st_mode)
        and observed.st_uid == os.geteuid(),
        "PAIR06_V8_INVOCATION_EVIDENCE_FILE_HOLD",
    )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fresh_preflight() -> dict[str, Any]:
    environment = v8_runtime.verify_v8_runtime_environment()
    assets = v8_runtime.verify_v8_runtime_assets(
        model_dir=(
            "/home/zoso/Downloads/"
            "void-apollyon-v3-qwen35-4b-lora-v1/model"
        ),
        adapter_dir=(
            "/home/zoso/Downloads/"
            "void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
        ),
    )
    _require(
        assets.get("verified_file_count") == 17,
        "PAIR06_V8_INVOCATION_ASSET_COUNT_HOLD",
    )
    _require(
        assets.get("runtime_execution_performed") is False
        and assets.get("model_execution_performed") is False,
        "PAIR06_V8_INVOCATION_PREFLIGHT_EXECUTION_HOLD",
    )
    return {
        "runtime_environment": deepcopy(environment),
        "runtime_assets": {
            **deepcopy(assets),
            "model_dir": str(assets["model_dir"]),
            "adapter_dir": str(assets["adapter_dir"]),
        },
    }


def _prepare_directories() -> None:
    _ensure_private_dir(ARM_ROOT)
    _ensure_private_dir(CLAIMS_ROOT)
    _require_empty_directory(RUNS_ROOT)


def _materialize(backend: git_backend.Pair06V8BaselineGitBackend):
    path_record = path_inputs.build_path_input_record(
        path_inputs.V2R13,
        frozen_source_root=str(FROZEN_SOURCE_ROOT),
        exact_engine_root=str(EXACT_ENGINE_ROOT),
    )
    return materializer.materialize_v2r13_frozen_worktrees(
        path_record,
        source_repository_root=str(SOURCE_ROOT),
        engine_repository_root=str(ENGINE_REPOSITORY_ROOT),
        materialization_authorized=True,
        path_exists=backend.path_exists,
        run_git=backend.run_git,
    )


def _validate_supervisor_receipt(
    receipt: Any,
    *,
    attempt_id: str,
) -> dict[str, Any]:
    _require(
        isinstance(receipt, Mapping),
        "PAIR06_V8_INVOCATION_SUPERVISOR_RECEIPT_HOLD",
    )
    value = dict(receipt)
    _require(
        value.get("schema")
        == (
            "void.abaddon.generation2."
            "pair06-v8-parent-launcher-supervisor-no-offload-receipt.v1"
        ),
        "PAIR06_V8_INVOCATION_SUPERVISOR_SCHEMA_HOLD",
    )
    _require(
        value.get("pair_slot") == PAIR_SLOT
        and value.get("arm") == ARM
        and value.get("attempt_id") == attempt_id
        and value.get("attempt_claimed") is True,
        "PAIR06_V8_INVOCATION_SUPERVISOR_SCOPE_HOLD",
    )
    placement = value.get("inference_safe_placement")
    _require(
        isinstance(placement, Mapping)
        and placement.get("all_parameters_cuda0") is True
        and placement.get("input_embedding_cuda0") is True
        and placement.get("cpu_parameter_count") == 0
        and placement.get("meta_parameter_count") == 0
        and placement.get("disk_offload_present") is False,
        "PAIR06_V8_INVOCATION_INFERENCE_SAFE_PLACEMENT_HOLD",
    )
    for field in (
        "runtime_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    ):
        _require(
            value.get(field) is True,
            "PAIR06_V8_INVOCATION_SUPERVISOR_COMPLETION_HOLD:" + field,
        )
    _require(
        type(value.get("model_inference_count")) is int
        and value["model_inference_count"] > 0,
        "PAIR06_V8_INVOCATION_INFERENCE_COUNT_HOLD",
    )
    _require(
        value.get("child_retirement_terminal") == "natural_exit",
        "PAIR06_V8_INVOCATION_CHILD_TERMINAL_HOLD",
    )
    _require(
        value.get("legacy_ollama_started") is False,
        "PAIR06_V8_INVOCATION_LEGACY_OLLAMA_HOLD",
    )
    for field in (
        "automatic_retry",
        "candidate_execution_performed",
        "held_out_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(
            value.get(field) is False,
            "PAIR06_V8_INVOCATION_BOUNDARY_HOLD:" + field,
        )
    game_result = value.get("game_result")
    _require(
        isinstance(game_result, Mapping)
        and game_result.get("pair_slot") == PAIR_SLOT
        and game_result.get("arm") == ARM
        and game_result.get("held_out") is False
        and game_result.get("seed") == 208354846
        and game_result.get("doctrine") == "FEINTER"
        and game_result.get("rounds_limit") == 36
        and game_result.get("ticks_per_round") == 25,
        "PAIR06_V8_INVOCATION_GAME_RESULT_SCOPE_HOLD",
    )
    for field in (
        "warm_start_sha256",
        "trajectory_sha256",
        "summary_sha256",
    ):
        _require(
            _hex(game_result.get(field), 64),
            "PAIR06_V8_INVOCATION_GAME_ARTIFACT_DIGEST_HOLD",
        )
    return deepcopy(value)


def _fresh_preclaim_gpu_observation() -> dict[str, Any]:
    evidence = gpu_observer.observe_pair06_v8_preclaim_gpu_readonly(
        observation_authorized=True,
        command_runner=gpu_observer.host_nvidia_smi_readonly_runner,
    )
    admitted = gpu_admission.evaluate_pair06_v8_preclaim_gpu_observation(
        evidence
    )
    _require(
        admitted.get("preclaim_gpu_admitted") is True,
        "PAIR06_V8_INVOCATION_GPU_ADMISSION_NOT_GREEN",
    )
    _require(
        admitted.get("execution_authorized") is False,
        "PAIR06_V8_INVOCATION_GPU_ADMISSION_AUTHORITY_DRIFT",
    )
    return {
        "observation": deepcopy(evidence),
        "admission": deepcopy(admitted),
    }


def execute_pair06_v8_baseline_game_receipt_bound_no_offload(
    *,
    expected_main_head: str,
    expected_invocation_source_sha256: str,
    authorization_accepted: bool,
    confirm: str,
) -> dict[str, Any]:
    """Execute exactly one pair-06 V8 baseline game attempt when later authorized."""

    _require(
        _hex(expected_main_head, 40),
        "PAIR06_V8_INVOCATION_EXPECTED_MAIN_REQUIRED",
    )
    _require(
        _hex(expected_invocation_source_sha256, 64),
        "PAIR06_V8_INVOCATION_EXPECTED_SOURCE_REQUIRED",
    )
    _require(
        authorization_accepted is True,
        "PAIR06_V8_BASELINE_GAME_SPECIFIC_AUTHORIZATION_REQUIRED",
    )
    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "PAIR06_V8_BASELINE_GAME_SPECIFIC_CONFIRMATION_REQUIRED",
    )

    _dependency_contracts()
    _check_python()
    source_sha = _verify_self(expected_invocation_source_sha256)
    main = _current_main(expected_main_head)
    _prepare_directories()
    _not_revoked()
    preflight = _fresh_preflight()

    marker_path = CLAIMS_ROOT / MARKER_NAME
    result_path = CLAIMS_ROOT / RESULT_NAME
    closeout_path = CLAIMS_ROOT / CLOSEOUT_NAME

    for path, code in (
        (marker_path, "PAIR06_V8_INVOCATION_PRIOR_ATTEMPT_PRESENT"),
        (result_path, "PAIR06_V8_INVOCATION_PRIOR_RESULT_PRESENT"),
        (closeout_path, "PAIR06_V8_INVOCATION_PRIOR_CLOSEOUT_PRESENT"),
    ):
        _require(not path.exists(), code)

    backend = git_backend.Pair06V8BaselineGitBackend(
        confirm=git_backend.CONFIRM_TOKEN
    )
    materialization = None
    try:
        materialization = _materialize(backend)

        # Everything in this block is pre-claim preparation. If any later
        # pre-claim recheck fails, remove only the worktrees owned by this
        # backend instance so the still-unconsumed attempt remains retryable.
        _current_main(expected_main_head)
        _verify_self(expected_invocation_source_sha256)
        _not_revoked()
        _fresh_preflight()

        # This is the final pre-claim host check. A hold here triggers the
        # existing worktree cleanup path and leaves the attempt marker absent.
        # No other host observation or runtime action occurs between this
        # admission and create-only marker construction.
        gpu_preclaim = _fresh_preclaim_gpu_observation()
    except BaseException:
        if materialization is not None:
            try:
                materializer.cleanup_v2r13_frozen_worktrees(
                    materialization,
                    cleanup_authorized=True,
                    path_exists=backend.path_exists,
                    run_git=backend.run_git,
                )
            except BaseException as cleanup_error:
                raise Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold(
                    "PAIR06_V8_INVOCATION_PRECLAIM_CLEANUP_FAILED"
                ) from cleanup_error
        raise

    marker_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-baseline-game-attempt.v1"
        ),
        "record_kind": "attempt_consumed_not_execution_evidence",
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "expected_main_head": expected_main_head,
        "main_tree": main["tree"],
        "invocation_source_sha256": source_sha,
        "materialization_sha256": _digest(materialization),
        "preclaim_gpu_observation_sha256": _digest(
            gpu_preclaim["observation"]
        ),
        "preclaim_gpu_free_memory_bytes": (
            gpu_preclaim["observation"]["free_memory_bytes"]
        ),
        "preclaim_gpu_total_memory_bytes": (
            gpu_preclaim["observation"]["total_memory_bytes"]
        ),
        "preclaim_gpu_compute_process_count": len(
            gpu_preclaim["observation"]["compute_processes"]
        ),
        "fresh_preclaim_gpu_admitted": True,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "pair06_baseline_specific_authorization_accepted": True,
        "runtime_load_authorized": True,
        "model_inference_authorized": True,
        "game_execution_authorized": True,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
    marker_sha256 = _write_create_only(marker_path, marker_payload)
    attempt_id = marker_sha256

    def authority_check(pair_slot: int, arm: str) -> bool:
        if pair_slot != PAIR_SLOT or arm != ARM:
            return False
        try:
            if (CLAIMS_ROOT / REVOCATION_NAME).exists():
                return False
            if _current_main(expected_main_head) != main:
                return False
            if _verify_self(expected_invocation_source_sha256) != source_sha:
                return False
            if _file_sha256(marker_path) != marker_sha256:
                return False
            return True
        except Exception:
            return False

    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V8_INVOCATION_REVOKED_AFTER_CLAIM",
    )

    receipt = supervisor.execute_pair06_v8_parent_supervisor_no_offload(
        attempt_id=attempt_id,
        attempt_claimed=True,
        runs_root=str(RUNS_ROOT),
        frozen_source_root=str(FROZEN_SOURCE_ROOT),
        exact_engine_root=str(EXACT_ENGINE_ROOT),
        execution_authorized=True,
        authority_check=authority_check,
    )
    receipt = _validate_supervisor_receipt(
        receipt,
        attempt_id=attempt_id,
    )

    result_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-baseline-game-result-no-offload.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "main_head": expected_main_head,
        "main_tree": main["tree"],
        "invocation_source_sha256": source_sha,
        "attempt_marker_sha256": marker_sha256,
        "attempt_id": attempt_id,
        "materialization": deepcopy(materialization),
        "preflight": deepcopy(preflight),
        "fresh_preclaim_gpu": deepcopy(gpu_preclaim),
        "supervisor_receipt": deepcopy(receipt),
        "pair06_baseline_execution_performed": True,
        "automatic_retry": False,
        "candidate_execution_performed": False,
        "pair15_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
    }
    result_sha256 = _write_create_only(result_path, result_payload)

    cleanup = materializer.cleanup_v2r13_frozen_worktrees(
        materialization,
        cleanup_authorized=True,
        path_exists=backend.path_exists,
        run_git=backend.run_git,
    )
    _require(
        cleanup.get("source_worktree_removed") is True
        and cleanup.get("engine_worktree_removed") is True
        and cleanup.get("removed_worktree_count") == 2,
        "PAIR06_V8_INVOCATION_WORKTREE_CLEANUP_HOLD",
    )

    closeout_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-baseline-game-closeout-no-offload.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "attempt_id": attempt_id,
        "attempt_marker_sha256": marker_sha256,
        "result_file_sha256": result_sha256,
        "worktree_cleanup": deepcopy(cleanup),
        "worktree_cleanup_completed": True,
        "runs_preserved": True,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
    closeout_sha256 = _write_create_only(
        closeout_path,
        closeout_payload,
    )

    return {
        **deepcopy(result_payload),
        "result_file": str(result_path),
        "result_file_sha256": result_sha256,
        "closeout_file": str(closeout_path),
        "closeout_file_sha256": closeout_sha256,
        "attempt_marker_file": str(marker_path),
        "attempt_marker_sha256": marker_sha256,
    }


def pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_contract() -> dict[str, Any]:
    dependencies = _dependency_contracts()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_implemented": True,
        "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_reviewed": False,
        "no_offload_parent_generation_required": True,
        "second_preservation_result_review_required": True,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "confirm_token": CONFIRM_TOKEN,
        "exact_v8_python_required": True,
        "exact_current_main_required": True,
        "exact_invocation_source_sha256_required": True,
        "fresh_v8_environment_and_assets_required": True,
        "reviewed_worktree_materializer_reused": True,
        "pair06_specific_git_backend_required": True,
        "preclaim_worktree_materialization_implemented": True,
        "preclaim_materialization_cleanup_on_hold_implemented": True,
        "preclaim_empty_runs_root_required": True,
        "reviewed_preclaim_gpu_observer_required": True,
        "historical_gpu_observation_nonreusable": True,
        "fresh_preclaim_gpu_observation_implemented": True,
        "fresh_preclaim_gpu_admission_required": True,
        "fresh_preclaim_gpu_observation_occurs_after_materialization": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "gpu_admission_hold_cleans_materialization_before_claim": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "durable_create_only_attempt_marker_implemented": True,
        "marker_deletion_api_implemented": False,
        "reset_api_implemented": False,
        "resume_api_implemented": False,
        "attempt_marker_precedes_model_load_and_child_spawn": True,
        "marker_sha256_is_attempt_id": True,
        "authority_rechecked_after_claim": True,
        "authority_rechecked_before_each_inference_by_supervisor": True,
        "no_offload_parent_receipt_schema_required": True,
        "inference_safe_placement_receipt_required": True,
        "durable_execution_result_before_cleanup_implemented": True,
        "success_only_worktree_cleanup_implemented": True,
        "durable_cleanup_closeout_implemented": True,
        "runs_preserved_after_success": True,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "explicit_authorization_boolean_required": True,
        "explicit_confirmation_token_required": True,
        "pair06_baseline_specific_authorization_accepted": False,
        "attempt_consumed": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8BaselineAttemptInvocationReceiptBoundNoOffloadHold(NEXT_GATE)
