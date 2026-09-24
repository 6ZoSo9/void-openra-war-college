"""V8 parent launcher/supervisor for the pair-06 proto game child.

Import and contract inspection are inert. The operational entrypoint requires:
* explicit execution_authorized=True;
* an already-created durable attempt claim;
* the exact accepted V8 Python environment;
* prepared frozen source/engine worktrees and an empty isolated runs root;
* a callable authority check that stays true before load and every inference.

The parent owns V8 load/inference, a private inherited socketpair, child spawn,
decision servicing, child process-group retirement, and V8 reference release.
The child owns gRPC/proto/OpenRA and never loads a model.

This source does not create the durable attempt claim or materialize worktrees.
"""

from __future__ import annotations

from copy import deepcopy
import gc
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_host_path_binding_source_binding_review_generation2
    as host_path_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_inference_safe_loader_generation2
    as inference_safe_loader,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_inference_safe_loader_source_binding_review_generation2
    as inference_safe_loader_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_offload_safe_generate_adapter_generation2
    as offload_adapter,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_offload_safe_generate_adapter_source_binding_review_generation2
    as offload_adapter_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_ipc_bridge_generation2
    as ipc,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_source_binding_review_generation2
    as child_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2
    as child_entry,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-launcher-supervisor-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-parent-launcher-supervisor-receipt.v1"
)

CHILD_REVIEW_GIT_BLOB = "bd2d7d97a9ed9c04be3bddae5f64977265686fa5"
CHILD_REVIEW_SOURCE_SHA256 = (
    "8a6d62ca43f3475fab51481e75670a0a5e79ddc7cbc3865ad4ad34db50d8536c"
)
OFFLOAD_ADAPTER_REVIEW_GIT_BLOB = "74dce709c20b147ca5fd42213ac7014c82a672f1"
OFFLOAD_ADAPTER_REVIEW_SOURCE_SHA256 = (
    "bbb39b01e162a92aef5f8f0d09c3d4adee964cdb1c923d78bc61e92aaf40dc83"
)
INFERENCE_SAFE_LOADER_REVIEW_GIT_BLOB = "d9f910e6290187431ecb7003da1da6b127708084"
INFERENCE_SAFE_LOADER_REVIEW_SOURCE_SHA256 = (
    "99f362a33696eaf6aede3da72d21f1df91e89e3ea3b6f71c93e2119b706c9eac"
)

PAIR_SLOT = 6
ARM = "baseline"
V8_PYTHON = Path(
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/"
    "venv/bin/python3.12"
)
PROTO_PYTHON = Path(
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
CHILD_MODULE = (
    "openra_env.learning."
    "abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_entrypoint_generation2"
)
SOCKET_TIMEOUT_S = 360.0
NATURAL_EXIT_GRACE_S = 15.0
SIGNAL_GRACE_S = 5.0

NEXT_GATE = "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_launcher_supervisor_review"


class Pair06V8ParentSupervisorHold(RuntimeError):
    pass


class AuthorityCheck(Protocol):
    def __call__(self, pair_slot: int, arm: str) -> bool:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ParentSupervisorHold(message)


def _dependencies() -> dict[str, Any]:
    child_contract = child_review.pair06_v8_proto_game_child_review_contract()
    _require(
        child_contract.get("pair06_v8_proto_game_child_reviewed") is True,
        "pair06 proto game child not reviewed",
    )
    _require(child_contract.get("pair_slot") == PAIR_SLOT, "pair06 child slot drift")
    _require(child_contract.get("arm") == ARM, "pair06 child arm drift")
    _require(
        child_contract.get("next_gate")
        == "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_IMPLEMENTATION_REQUIRED",
        "pair06 parent-supervisor frontier drift",
    )

    paths = host_path_review.pair06_v8_host_path_binding_review_contract()
    _require(paths.get("pair_slot") == PAIR_SLOT, "pair06 host path slot drift")
    _require(paths.get("verified_asset_count") == 17, "pair06 asset count drift")

    offload = offload_adapter_review.pair06_v8_offload_safe_generate_adapter_review_contract()
    _require(
        offload.get("pair06_v8_offload_safe_generate_adapter_reviewed") is True,
        "pair06 offload-safe generate adapter not reviewed",
    )
    _require(offload.get("pair_slot") == PAIR_SLOT, "pair06 offload adapter slot drift")
    _require(offload.get("arm") == ARM, "pair06 offload adapter arm drift")
    _require(
        offload.get("input_device_from_embedding_weight") is True
        and offload.get("hard_coded_cuda_input_transfer_used") is False,
        "pair06 offload adapter device-placement drift",
    )
    _require(
        offload.get("next_gate")
        == "PAIR06_V8_PARENT_SUPERVISOR_OFFLOAD_ADAPTER_BINDING_REQUIRED",
        "pair06 offload adapter frontier drift",
    )

    safe_loader = inference_safe_loader_review.pair06_v8_inference_safe_loader_review_contract()
    _require(
        safe_loader.get("pair06_v8_inference_safe_loader_reviewed") is True,
        "pair06 inference-safe loader not reviewed",
    )
    _require(safe_loader.get("pair_slot") == PAIR_SLOT, "pair06 inference-safe loader slot drift")
    _require(safe_loader.get("arm") == ARM, "pair06 inference-safe loader arm drift")
    _require(
        safe_loader.get("device_map") == {"": 0}
        and safe_loader.get("offload_embedding") is False,
        "pair06 inference-safe loader placement policy drift",
    )
    _require(
        safe_loader.get("cpu_parameter_offload_allowed") is False
        and safe_loader.get("disk_parameter_offload_allowed") is False
        and safe_loader.get("meta_parameter_allowed_after_load") is False,
        "pair06 inference-safe loader offload boundary drift",
    )
    _require(
        safe_loader.get("next_gate")
        == "PAIR06_V8_PARENT_SUPERVISOR_INFERENCE_SAFE_LOADER_BINDING_REQUIRED",
        "pair06 inference-safe loader frontier drift",
    )
    return {
        "child_review": deepcopy(child_contract),
        "host_path_review": deepcopy(paths),
        "offload_adapter_review": deepcopy(offload),
        "inference_safe_loader_review": deepcopy(safe_loader),
    }


def _require_parent_environment() -> None:
    _require(
        Path(sys.executable) == V8_PYTHON,
        "pair06 parent must use exact accepted V8 venv executable",
    )
    _require(
        Path(sys.prefix).resolve() == V8_PYTHON.parent.parent.resolve(),
        "pair06 parent sys.prefix must be accepted V8 venv",
    )


def _hex64(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def _group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _retire_child(process: Any, pgid: int) -> str:
    _require(type(pgid) is int and pgid > 1, "child pgid invalid")
    _require(process.pid == pgid, "child must lead private process group")

    try:
        rc = process.wait(timeout=NATURAL_EXIT_GRACE_S)
    except subprocess.TimeoutExpired:
        rc = None

    if rc is not None and not _group_exists(pgid):
        return "natural_exit"

    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=SIGNAL_GRACE_S)
    except subprocess.TimeoutExpired:
        pass
    if not _group_exists(pgid):
        return "sigterm_retired"

    try:
        os.killpg(pgid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=SIGNAL_GRACE_S)
    except subprocess.TimeoutExpired as exc:
        raise Pair06V8ParentSupervisorHold(
            "pair06 child did not exit after SIGKILL"
        ) from exc
    _require(not _group_exists(pgid), "pair06 child process group still exists after SIGKILL")
    return "sigkill_retired"


def _child_command(
    *,
    child_fd: int,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
) -> list[str]:
    return [
        str(PROTO_PYTHON),
        "-B",
        "-m",
        CHILD_MODULE,
        "--fd", str(child_fd),
        "--attempt-id", attempt_id,
        "--runs-root", runs_root,
        "--frozen-source-root", frozen_source_root,
        "--exact-engine-root", exact_engine_root,
        "--confirm", child_entry.CONFIRM_TOKEN,
    ]


def _decision_response(
    runtime: Any,
    request: Mapping[str, Any],
    *,
    seq: int,
    authority_check: AuthorityCheck,
) -> dict[str, Any]:
    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V8_PARENT_AUTHORITY_REVOKED_BEFORE_INFERENCE",
    )
    result = runtime.decide_campaign_turn(
        state=request["state"],
        typed_tools=request["typed_tools"],
        tool_contract=request["tool_contract"],
        doctrine=request["doctrine"],
        round_no=request["round_no"],
        feedback=request["feedback"],
    )
    _require(isinstance(result, Mapping), "V8 decision result must be object")
    _require(result.get("host_mutation_performed") is False, "V8 parent mutated host")
    action = result.get("campaign_action")
    _require(isinstance(action, Mapping), "V8 campaign_action missing")
    return {
        "type": "DECIDE_RESPONSE",
        "seq": seq,
        "protocol_version": 1,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "attempt_id": request["attempt_id"],
        "round_no": request["round_no"],
        "attempt_no": request["attempt_no"],
        "campaign_action": deepcopy(dict(action)),
        "host_mutation_performed": False,
    }


def execute_pair06_v8_parent_supervisor(
    *,
    attempt_id: str,
    attempt_claimed: bool,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    execution_authorized: bool,
    authority_check: AuthorityCheck,
) -> dict[str, Any]:
    """Execute one coupled pair-06 parent/child attempt when later authorized."""
    dependencies = _dependencies()
    _require_parent_environment()
    _require(execution_authorized is True, "PAIR06_V8_GAME_EXECUTION_AUTHORIZATION_REQUIRED")
    _require(attempt_claimed is True, "PAIR06_V8_DURABLE_ATTEMPT_CLAIM_REQUIRED")
    _require(_hex64(attempt_id), "pair06 attempt_id invalid")
    _require(callable(authority_check), "pair06 authority_check required")
    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V8_PARENT_AUTHORITY_REVOKED_BEFORE_LOAD",
    )

    for value, label in (
        (runs_root, "runs_root"),
        (frozen_source_root, "frozen_source_root"),
        (exact_engine_root, "exact_engine_root"),
    ):
        _require(isinstance(value, str) and value.startswith("/"), f"{label} must be absolute")

    paths = dependencies["host_path_review"]
    runtime = None
    parent_sock = None
    child_sock = None
    process = None
    pgid = None
    parent_send_seq = 1
    child_recv_seq = 1
    inference_count = 0
    game_result = None
    retirement_terminal = None

    try:
        runtime = inference_safe_loader.load_pair06_v8_inference_safe_runtime(
            model_dir=paths["model_dir"],
            adapter_dir=paths["adapter_dir"],
            runtime_load_authorized=True,
            authority_check=authority_check,
        )
        runtime = offload_adapter.bind_pair06_v8_offload_safe_generate(runtime)
        placement = getattr(
            runtime,
            "_void_pair06_inference_safe_placement",
            None,
        )
        _require(
            isinstance(placement, Mapping)
            and placement.get("all_parameters_cuda0") is True
            and placement.get("input_embedding_cuda0") is True
            and placement.get("cpu_parameter_count") == 0
            and placement.get("meta_parameter_count") == 0
            and placement.get("disk_offload_present") is False,
            "PAIR06_V8_INFERENCE_SAFE_PLACEMENT_RECEIPT_HOLD",
        )
        parent_sock, child_sock = socket.socketpair()
        parent_sock.settimeout(SOCKET_TIMEOUT_S)
        child_sock.settimeout(SOCKET_TIMEOUT_S)
        child_fd = child_sock.fileno()

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONNOUSERSITE"] = "1"
        command = _child_command(
            child_fd=child_fd,
            attempt_id=attempt_id,
            runs_root=runs_root,
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
        )
        process = subprocess.Popen(
            command,
            cwd=str(SOURCE_ROOT),
            env=env,
            pass_fds=(child_fd,),
            close_fds=True,
            start_new_session=True,
        )
        pgid = process.pid
        child_sock.close()
        child_sock = None

        ipc.send_message(
            parent_sock,
            {
                "type": "HELLO",
                "seq": parent_send_seq,
                "protocol_version": 1,
                "pair_slot": PAIR_SLOT,
                "arm": ARM,
                "attempt_id": attempt_id,
            },
            direction="parent_to_child",
            expected_seq=parent_send_seq,
            expected_attempt_id=attempt_id,
        )
        parent_send_seq += 1

        ready = ipc.recv_message(
            parent_sock,
            direction="child_to_parent",
            expected_seq=child_recv_seq,
            expected_attempt_id=attempt_id,
        )
        child_recv_seq += 1
        _require(ready["type"] == "READY", "pair06 parent expected READY")
        _require(ready["child_pid"] == process.pid, "pair06 READY child PID drift")
        _require(ready["child_pgid"] == process.pid, "pair06 READY child PGID drift")

        while game_result is None:
            message = ipc.recv_message(
                parent_sock,
                direction="child_to_parent",
                expected_seq=child_recv_seq,
                expected_attempt_id=attempt_id,
            )
            child_recv_seq += 1

            if message["type"] == "DECIDE_REQUEST":
                response = _decision_response(
                    runtime,
                    message,
                    seq=parent_send_seq,
                    authority_check=authority_check,
                )
                inference_count += 1
                ipc.send_message(
                    parent_sock,
                    response,
                    direction="parent_to_child",
                    expected_seq=parent_send_seq,
                    expected_attempt_id=attempt_id,
                )
                parent_send_seq += 1
                continue

            if message["type"] == "GAME_RESULT":
                _require(isinstance(message["result"], dict), "pair06 child result missing")
                game_result = deepcopy(message["result"])
                break

            if message["type"] == "ERROR":
                raise Pair06V8ParentSupervisorHold(
                    f"pair06 child error {message['error_type']}: {message['error_message']}"
                )

            raise Pair06V8ParentSupervisorHold(
                f"unexpected child message: {message['type']}"
            )

        _require(inference_count > 0, "pair06 game completed without V8 inference")
        rc = process.wait(timeout=NATURAL_EXIT_GRACE_S)
        _require(rc == 0, f"pair06 child natural exit nonzero: {rc}")
        _require(not _group_exists(pgid), "pair06 child process group remains after zero exit")
        retirement_terminal = "natural_exit"

        return {
            "schema": RECEIPT_SCHEMA,
            "pair_slot": PAIR_SLOT,
            "arm": ARM,
            "attempt_id": attempt_id,
            "attempt_claimed": True,
            "v8_parent_python": str(V8_PYTHON),
            "proto_child_python": str(PROTO_PYTHON),
            "runtime_load_performed": True,
            "inference_safe_placement": deepcopy(dict(placement)),
            "model_inference_performed": True,
            "model_inference_count": inference_count,
            "game_execution_performed": True,
            "child_pid": process.pid,
            "child_pgid": pgid,
            "child_retirement_terminal": retirement_terminal,
            "legacy_ollama_started": False,
            "automatic_retry": False,
            "candidate_execution_performed": False,
            "held_out_execution_performed": False,
            "training_performed": False,
            "weights_updated": False,
            "automatic_policy_promotion": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
            "game_result": deepcopy(game_result),
        }
    except BaseException:
        if parent_sock is not None and process is not None and process.poll() is None:
            try:
                ipc.send_message(
                    parent_sock,
                    {
                        "type": "ABORT",
                        "seq": parent_send_seq,
                        "protocol_version": 1,
                        "pair_slot": PAIR_SLOT,
                        "arm": ARM,
                        "attempt_id": attempt_id,
                        "reason": "parent_supervisor_abort",
                    },
                    direction="parent_to_child",
                    expected_seq=parent_send_seq,
                    expected_attempt_id=attempt_id,
                )
            except BaseException:
                pass
        raise
    finally:
        if child_sock is not None:
            child_sock.close()
        if parent_sock is not None:
            parent_sock.close()
        if process is not None and pgid is not None and retirement_terminal is None:
            _retire_child(process, pgid)
        runtime = None
        gc.collect()


def pair06_v8_parent_launcher_supervisor_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "child_review_git_blob": CHILD_REVIEW_GIT_BLOB,
        "child_review_source_sha256": CHILD_REVIEW_SOURCE_SHA256,
        "offload_adapter_review_git_blob": OFFLOAD_ADAPTER_REVIEW_GIT_BLOB,
        "offload_adapter_review_source_sha256": OFFLOAD_ADAPTER_REVIEW_SOURCE_SHA256,
        "inference_safe_loader_review_git_blob": INFERENCE_SAFE_LOADER_REVIEW_GIT_BLOB,
        "inference_safe_loader_review_source_sha256": INFERENCE_SAFE_LOADER_REVIEW_SOURCE_SHA256,
        "pair06_v8_parent_launcher_supervisor_implemented": True,
        "pair06_v8_parent_launcher_supervisor_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "v8_parent_python": str(V8_PYTHON),
        "proto_child_python": str(PROTO_PYTHON),
        "socketpair_creation_implemented": True,
        "child_spawn_with_inherited_fd_implemented": True,
        "child_private_process_group_implemented": True,
        "hello_ready_handshake_implemented": True,
        "parent_decision_service_loop_implemented": True,
        "authority_check_before_load_implemented": True,
        "authority_check_before_each_inference_implemented": True,
        "inference_safe_no_offload_loader_reviewed": True,
        "inference_safe_loader_bound_before_generate_adapter": True,
        "cpu_disk_meta_parameter_offload_forbidden": True,
        "all_parameters_cuda0_required_before_child_spawn": True,
        "inference_safe_placement_receipt_implemented": True,
        "offload_safe_generate_adapter_reviewed": True,
        "offload_safe_generate_bound_after_load_before_child_spawn": True,
        "hard_coded_cuda_input_transfer_used_by_pair06_parent": False,
        "natural_exit_verification_implemented": True,
        "term_then_kill_retirement_implemented": True,
        "v8_reference_release_in_finally_implemented": True,
        "attempt_claim_required_but_not_implemented": True,
        "worktree_materialization_required_but_not_implemented": True,
        "isolated_runs_root_required_but_not_created": True,
        "execution_authorized_by_contract_inspection": False,
        "subprocess_spawn_performed_by_contract_inspection": False,
        "model_load_performed_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "game_execution_performed_by_contract_inspection": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_claim(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ParentSupervisorHold(NEXT_GATE)
