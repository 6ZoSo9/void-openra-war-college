"""Dormant read-only rootless-Docker image-identity backend for V2R13.

This source implements a concrete *candidate* host mechanism for the final
Generation-2 V2R13 runtime-image identity channel.

Reviewed discovery established that Precision's rootless Docker daemon stores
the exact frozen OpenRA joint-duel sandbox image while no container is currently
running or retained from that image. Therefore this backend proves local
immutable image-store identity; it deliberately does not require an active
container.

The backend is limited to three exact read-only Docker operations:

1. ``docker context inspect rootless``
2. ``docker --context rootless info --format {{json .}}``
3. ``docker --context rootless image inspect <exact frozen image ID>``

The context must resolve to the reviewed rootless Unix socket and Docker info
must report rootless security. The inspected image ID must equal the exact
frozen identity.

No container list/start/stop/restart/exec/create/remove operation exists here.
No image pull/build/tag/remove/prune operation exists here. No Ollama endpoint,
model load/inference, game execution, service action, training, deployment,
VOID-chain mutation, or funds action exists here.

This candidate does NOT self-admit its source. A separately reviewed source
SHA-256 must be supplied by the caller and later bound by a distinct admission
instrument. Until that binding exists, the Generation-2 V2R13 primitive frontier
remains 13 supported / 3 unresolved.
"""

from __future__ import annotations

import json
import subprocess
from typing import Any, Mapping, Protocol, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_runtime_image_readonly_observer_generation2
    as runtime_image_interface,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-rootless-docker-image-backend-contract.v1"
)

DOCKER = "/usr/bin/docker"
CONTEXT_NAME = "rootless"
EXPECTED_CONTEXT_HOST = "unix:///run/user/1000/docker.sock"
EXPECTED_DOCKER_ROOT_DIR = "/home/zoso/.local/share/docker"
EXPECTED_IMAGE_TAG = "void-openra-joint-duel:ad1926569b12466c"
EXPECTED_IMAGE_REPO_DIGEST = (
    "void-openra-joint-duel@"
    "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
)
EXPECTED_GENERATION_LABEL = "ad1926569b12466c"
EXPECTED_PURPOSE_LABEL = "joint-duel-sandbox"
EXPECTED_WORKING_DIR = "/opt/openra"
EXPECTED_ENTRYPOINT_PREFIX = (
    "dotnet",
    "/opt/openra/bin/OpenRA.dll",
)

COMMAND_TIMEOUT_SECONDS = 5.0
MAX_STDOUT_BYTES = 4 * 1024 * 1024
MAX_STDERR_BYTES = 64 * 1024

CONTEXT_COMMAND = (
    DOCKER,
    "context",
    "inspect",
    CONTEXT_NAME,
)
INFO_COMMAND = (
    DOCKER,
    "--context",
    CONTEXT_NAME,
    "info",
    "--format",
    "{{json .}}",
)
IMAGE_INSPECT_COMMAND = (
    DOCKER,
    "--context",
    CONTEXT_NAME,
    "image",
    "inspect",
    activation_contract.V2R13_RUNTIME_IMAGE_ID,
)

ALLOWED_COMMANDS = frozenset(
    (
        CONTEXT_COMMAND,
        INFO_COMMAND,
        IMAGE_INSPECT_COMMAND,
    )
)

FORBIDDEN_DOCKER_TOKENS = frozenset(
    (
        "run",
        "start",
        "stop",
        "restart",
        "exec",
        "create",
        "rm",
        "remove",
        "kill",
        "pause",
        "unpause",
        "pull",
        "push",
        "build",
        "tag",
        "rmi",
        "prune",
        "commit",
        "save",
        "load",
        "import",
        "export",
    )
)


class RuntimeV2R13RootlessDockerImageBackendHold(ValueError):
    pass


class CommandRunner(Protocol):
    def __call__(self, args: Sequence[str]) -> Mapping[str, Any]:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13RootlessDockerImageBackendHold(message)


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _validate_exact_command(args: Sequence[str]) -> tuple[str, ...]:
    _require(
        isinstance(args, (tuple, list)),
        "rootless-Docker command must be sequence",
    )
    command = tuple(args)
    _require(
        command in ALLOWED_COMMANDS,
        "V2R13_ROOTLESS_DOCKER_COMMAND_NOT_REVIEWED",
    )
    lowered = {part.lower() for part in command[1:]}
    _require(
        lowered.isdisjoint(FORBIDDEN_DOCKER_TOKENS),
        "V2R13_ROOTLESS_DOCKER_MUTATING_TOKEN_FORBIDDEN",
    )
    return command


def host_readonly_command_runner(args: Sequence[str]) -> dict[str, Any]:
    """Run exactly one reviewed Docker metadata command.

    This function is never invoked automatically.
    """
    command = _validate_exact_command(args)

    try:
        completed = subprocess.run(
            list(command),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
            env={
                "HOME": "/home/zoso",
                "LANG": "C",
                "LC_ALL": "C",
                "PATH": "/usr/bin:/bin",
            },
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeV2R13RootlessDockerImageBackendHold(
            "V2R13_ROOTLESS_DOCKER_COMMAND_TIMEOUT"
        ) from error

    stdout = completed.stdout.encode("utf-8", errors="replace")
    stderr = completed.stderr.encode("utf-8", errors="replace")

    _require(
        len(stdout) <= MAX_STDOUT_BYTES,
        "V2R13_ROOTLESS_DOCKER_STDOUT_EXCEEDS_BOUND",
    )
    _require(
        len(stderr) <= MAX_STDERR_BYTES,
        "V2R13_ROOTLESS_DOCKER_STDERR_EXCEEDS_BOUND",
    )

    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def _command_result(
    run_command: CommandRunner,
    command: tuple[str, ...],
    *,
    label: str,
) -> str:
    _require(callable(run_command), f"{label}: command runner required")
    result = run_command(command)
    _require(isinstance(result, Mapping), f"{label}: command result malformed")
    _require(
        set(result) == {"returncode", "stdout", "stderr"},
        f"{label}: command result field-set drift",
    )
    _require(type(result["returncode"]) is int, f"{label}: returncode malformed")
    _require(type(result["stdout"]) is str, f"{label}: stdout malformed")
    _require(type(result["stderr"]) is str, f"{label}: stderr malformed")
    _require(result["returncode"] == 0, f"{label}: command failed")
    _require(
        len(result["stdout"].encode("utf-8")) <= MAX_STDOUT_BYTES,
        f"{label}: stdout exceeds reviewed bound",
    )
    _require(
        len(result["stderr"].encode("utf-8")) <= MAX_STDERR_BYTES,
        f"{label}: stderr exceeds reviewed bound",
    )
    return result["stdout"]


def _json_object(raw: str, *, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeV2R13RootlessDockerImageBackendHold(
            f"{label}: invalid JSON"
        ) from error
    _require(isinstance(value, Mapping), f"{label}: expected JSON object")
    return value


def _json_singleton_object(raw: str, *, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeV2R13RootlessDockerImageBackendHold(
            f"{label}: invalid JSON"
        ) from error
    _require(
        isinstance(value, list) and len(value) == 1,
        f"{label}: expected one JSON object",
    )
    row = value[0]
    _require(isinstance(row, Mapping), f"{label}: image row malformed")
    return row


def _validate_context(raw: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeV2R13RootlessDockerImageBackendHold(
            "V2R13_ROOTLESS_DOCKER_CONTEXT_INVALID_JSON"
        ) from error

    _require(
        isinstance(value, list) and len(value) == 1,
        "V2R13 rootless Docker context count drift",
    )
    row = value[0]
    _require(
        isinstance(row, Mapping),
        "V2R13 rootless Docker context row malformed",
    )
    _require(
        row.get("Name") == CONTEXT_NAME,
        "V2R13 rootless Docker context name drift",
    )
    endpoints = row.get("Endpoints")
    _require(
        isinstance(endpoints, Mapping),
        "V2R13 rootless Docker context endpoints missing",
    )
    docker_endpoint = endpoints.get("docker")
    _require(
        isinstance(docker_endpoint, Mapping),
        "V2R13 rootless Docker endpoint missing",
    )
    _require(
        docker_endpoint.get("Host") == EXPECTED_CONTEXT_HOST,
        "V2R13 rootless Docker context host drift",
    )
    _require(
        docker_endpoint.get("SkipTLSVerify") is False,
        "V2R13 rootless Docker context TLS setting drift",
    )
    return row


def _validate_info(raw: str) -> Mapping[str, Any]:
    row = _json_object(raw, label="V2R13_ROOTLESS_DOCKER_INFO")
    security = row.get("SecurityOptions")
    _require(
        isinstance(security, list),
        "V2R13 rootless Docker security options missing",
    )
    _require(
        "name=rootless" in security,
        "V2R13 Docker daemon is not rootless",
    )
    _require(
        row.get("DockerRootDir") == EXPECTED_DOCKER_ROOT_DIR,
        "V2R13 rootless Docker data-root drift",
    )
    _require(
        row.get("OSType") == "linux",
        "V2R13 rootless Docker OS type drift",
    )
    return row


def _validate_image(raw: str) -> Mapping[str, Any]:
    row = _json_singleton_object(
        raw,
        label="V2R13_ROOTLESS_DOCKER_IMAGE_INSPECT",
    )

    expected_id = activation_contract.V2R13_RUNTIME_IMAGE_ID
    _require(
        row.get("Id") == expected_id,
        "V2R13 rootless Docker image ID drift",
    )

    repo_tags = row.get("RepoTags")
    _require(
        isinstance(repo_tags, list),
        "V2R13 rootless Docker RepoTags malformed",
    )
    _require(
        EXPECTED_IMAGE_TAG in repo_tags,
        "V2R13 rootless Docker reviewed tag missing",
    )

    repo_digests = row.get("RepoDigests")
    _require(
        isinstance(repo_digests, list),
        "V2R13 rootless Docker RepoDigests malformed",
    )
    _require(
        EXPECTED_IMAGE_REPO_DIGEST in repo_digests,
        "V2R13 rootless Docker reviewed repo digest missing",
    )

    config = row.get("Config")
    _require(
        isinstance(config, Mapping),
        "V2R13 rootless Docker image config missing",
    )
    labels = config.get("Labels")
    _require(
        isinstance(labels, Mapping),
        "V2R13 rootless Docker image labels missing",
    )
    _require(
        labels.get("void.openra.generation") == EXPECTED_GENERATION_LABEL,
        "V2R13 rootless Docker generation label drift",
    )
    _require(
        labels.get("void.openra.purpose") == EXPECTED_PURPOSE_LABEL,
        "V2R13 rootless Docker purpose label drift",
    )
    _require(
        config.get("WorkingDir") == EXPECTED_WORKING_DIR,
        "V2R13 rootless Docker working directory drift",
    )

    entrypoint = config.get("Entrypoint")
    _require(
        isinstance(entrypoint, list)
        and tuple(entrypoint[:2]) == EXPECTED_ENTRYPOINT_PREFIX,
        "V2R13 rootless Docker OpenRA entrypoint drift",
    )

    return row


def collect_rootless_docker_runtime_image_receipt(
    *,
    observation_authorized: bool,
    reviewed_source_sha256: str,
    run_command: CommandRunner,
) -> dict[str, Any]:
    """Collect exact local rootless-Docker image identity without execution."""
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_ROOTLESS_DOCKER_OBSERVATION_NOT_AUTHORIZED",
    )
    _require(
        _is_sha256(reviewed_source_sha256),
        "V2R13 rootless Docker reviewed source SHA malformed",
    )
    _require(callable(run_command), "V2R13 rootless Docker command runner required")

    context_raw = _command_result(
        run_command,
        CONTEXT_COMMAND,
        label="V2R13_ROOTLESS_DOCKER_CONTEXT",
    )
    context = _validate_context(context_raw)

    info_raw = _command_result(
        run_command,
        INFO_COMMAND,
        label="V2R13_ROOTLESS_DOCKER_INFO",
    )
    info = _validate_info(info_raw)

    image_raw = _command_result(
        run_command,
        IMAGE_INSPECT_COMMAND,
        label="V2R13_ROOTLESS_DOCKER_IMAGE_INSPECT",
    )
    image = _validate_image(image_raw)

    return {
        "schema": runtime_image_interface.BACKEND_RECEIPT_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "primitive_name": "runtime_image_identity_verified",
        "source_sha256": reviewed_source_sha256,
        "backend_kind": "rootless_docker_local_image_store_v1",
        "observation_mode": "read_only",
        "runtime_image_id": image["Id"],
        "runtime_image_identity_observation_performed": True,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "_candidate_metadata": {
            "context_name": context["Name"],
            "context_host": context["Endpoints"]["docker"]["Host"],
            "docker_root_dir": info["DockerRootDir"],
            "rootless_security": True,
            "reviewed_image_tag_present": True,
            "reviewed_repo_digest_present": True,
            "generation_label": image["Config"]["Labels"]["void.openra.generation"],
            "purpose_label": image["Config"]["Labels"]["void.openra.purpose"],
            "working_dir": image["Config"]["WorkingDir"],
            "openra_entrypoint_prefix": list(image["Config"]["Entrypoint"][:2]),
        },
    }


def strip_candidate_metadata(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Return exactly the interface-defined backend receipt field set."""
    _require(isinstance(receipt, Mapping), "rootless Docker receipt must be object")
    expected = set(runtime_image_interface.BACKEND_RECEIPT_FIELDS)
    _require(
        set(receipt) == expected | {"_candidate_metadata"},
        "rootless Docker candidate receipt field-set drift",
    )
    return {key: receipt[key] for key in runtime_image_interface.BACKEND_RECEIPT_FIELDS}


def v2r13_rootless_docker_image_backend_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "runtime_image_interface_git_blob": (
            "8bc118684fb085361fa98dd80b6a1ee37edeb523"
        ),
        "activation_contract_git_blob": (
            "a3acb42280c334daa24a3b830105a04666fd603b"
        ),
        "expected_runtime_image_id": activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "backend_kind": "rootless_docker_local_image_store_v1",
        "reviewed_context_name": CONTEXT_NAME,
        "reviewed_context_host": EXPECTED_CONTEXT_HOST,
        "reviewed_docker_root_dir": EXPECTED_DOCKER_ROOT_DIR,
        "reviewed_image_tag": EXPECTED_IMAGE_TAG,
        "reviewed_image_repo_digest": EXPECTED_IMAGE_REPO_DIGEST,
        "reviewed_generation_label": EXPECTED_GENERATION_LABEL,
        "reviewed_purpose_label": EXPECTED_PURPOSE_LABEL,
        "reviewed_working_dir": EXPECTED_WORKING_DIR,
        "reviewed_entrypoint_prefix": EXPECTED_ENTRYPOINT_PREFIX,
        "allowed_command_count": len(ALLOWED_COMMANDS),
        "context_inspect_only": True,
        "docker_info_only": True,
        "image_inspect_only": True,
        "container_list_implemented": False,
        "container_start_stop_exec_implemented": False,
        "image_pull_build_remove_implemented": False,
        "network_probe_implemented": False,
        "ollama_http_request_implemented": False,
        "chat_completions_request_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "host_command_runner_present": True,
        "automatic_host_backend_selection": False,
        "observation_requires_explicit_authority": True,
        "reviewed_source_binding_required": True,
        "canonical_backend_source_binding_present": False,
        "candidate_backend_implemented": True,
        "runtime_image_identity_provider_primitive_implemented": False,
        "candidate_backend_does_not_admit_collector_identity": True,
        "candidate_backend_does_not_advance_primitive_frontier": True,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }
