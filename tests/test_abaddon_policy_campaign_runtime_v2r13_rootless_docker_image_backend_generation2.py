from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "25e8f41dcea700860ec1b97726b321a99c2622e00ddba12433246c7b121b11f6"
REVIEWED_SOURCE_SHA = "c" * 64


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_rootless_docker_image_backend",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _context_payload(m):
    return [
        {
            "Name": m.CONTEXT_NAME,
            "Endpoints": {
                "docker": {
                    "Host": m.EXPECTED_CONTEXT_HOST,
                    "SkipTLSVerify": False,
                }
            },
        }
    ]


def _info_payload(m):
    return {
        "Name": "zoso-Precision-Tower-7810",
        "OSType": "linux",
        "DockerRootDir": m.EXPECTED_DOCKER_ROOT_DIR,
        "SecurityOptions": [
            "name=seccomp,profile=builtin",
            "name=rootless",
            "name=cgroupns",
        ],
        "Containers": 0,
        "ContainersRunning": 0,
        "ContainersStopped": 0,
        "Images": 7,
    }


def _image_payload(m):
    return [
        {
            "Id": m.activation_contract.V2R13_RUNTIME_IMAGE_ID,
            "RepoTags": [m.EXPECTED_IMAGE_TAG],
            "RepoDigests": [m.EXPECTED_IMAGE_REPO_DIGEST],
            "Config": {
                "Labels": {
                    "void.openra.generation": m.EXPECTED_GENERATION_LABEL,
                    "void.openra.purpose": m.EXPECTED_PURPOSE_LABEL,
                },
                "WorkingDir": m.EXPECTED_WORKING_DIR,
                "Entrypoint": [
                    "dotnet",
                    "/opt/openra/bin/OpenRA.dll",
                    "Engine.EngineDir=/opt/openra",
                    "Game.Mod=ra",
                    "Game.Platform=Null",
                    "Launch.MultiSession=9999",
                ],
            },
        }
    ]


class FakeRunner:
    def __init__(self, m, *, context=None, info=None, image=None, rc_by_command=None):
        self.m = m
        self.calls = []
        self.context = _context_payload(m) if context is None else context
        self.info = _info_payload(m) if info is None else info
        self.image = _image_payload(m) if image is None else image
        self.rc_by_command = rc_by_command or {}

    def __call__(self, args):
        command = tuple(args)
        self.calls.append(command)
        rc = self.rc_by_command.get(command, 0)
        if command == self.m.CONTEXT_COMMAND:
            value = self.context
        elif command == self.m.INFO_COMMAND:
            value = self.info
        elif command == self.m.IMAGE_INSPECT_COMMAND:
            value = self.image
        else:
            raise AssertionError(f"unexpected command: {command!r}")
        return {
            "returncode": rc,
            "stdout": json.dumps(value, sort_keys=True),
            "stderr": "" if rc == 0 else "synthetic failure",
        }


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _collect(m, runner=None, **kwargs):
    if runner is None:
        runner = FakeRunner(m)
    return m.collect_rootless_docker_runtime_image_receipt(
        observation_authorized=True,
        reviewed_source_sha256=REVIEWED_SOURCE_SHA,
        run_command=runner,
        **kwargs,
    )


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_contract_binds_exact_canonical_interfaces():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_contract()
    assert out["runtime_image_interface_git_blob"] == (
        "8bc118684fb085361fa98dd80b6a1ee37edeb523"
    )
    assert out["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert out["expected_runtime_image_id"] == (
        "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
    )


def test_contract_binds_reviewed_rootless_docker_discovery():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_contract()
    assert out["reviewed_context_name"] == "rootless"
    assert out["reviewed_context_host"] == "unix:///run/user/1000/docker.sock"
    assert out["reviewed_docker_root_dir"] == "/home/zoso/.local/share/docker"
    assert out["reviewed_image_tag"] == "void-openra-joint-duel:ad1926569b12466c"
    assert out["reviewed_generation_label"] == "ad1926569b12466c"
    assert out["reviewed_purpose_label"] == "joint-duel-sandbox"


def test_contract_has_exact_three_readonly_commands():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_contract()
    assert out["allowed_command_count"] == 3
    assert out["context_inspect_only"] is True
    assert out["docker_info_only"] is True
    assert out["image_inspect_only"] is True
    assert m.ALLOWED_COMMANDS == frozenset(
        (m.CONTEXT_COMMAND, m.INFO_COMMAND, m.IMAGE_INSPECT_COMMAND)
    )


def test_contract_has_no_container_or_image_mutation_mechanics():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_contract()
    for field in (
        "container_list_implemented",
        "container_start_stop_exec_implemented",
        "image_pull_build_remove_implemented",
        "network_probe_implemented",
        "ollama_http_request_implemented",
        "chat_completions_request_implemented",
        "model_load_implemented",
        "model_inference_implemented",
        "game_execution_implemented",
    ):
        assert out[field] is False


def test_contract_requires_authority_source_binding_and_no_auto_backend():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_contract()
    assert out["host_command_runner_present"] is True
    assert out["automatic_host_backend_selection"] is False
    assert out["observation_requires_explicit_authority"] is True
    assert out["reviewed_source_binding_required"] is True
    assert out["canonical_backend_source_binding_present"] is False


def test_contract_preserves_13_3_frontier():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_contract()
    assert out["candidate_backend_implemented"] is True
    assert out["runtime_image_identity_provider_primitive_implemented"] is False
    assert out["candidate_backend_does_not_admit_collector_identity"] is True
    assert out["candidate_backend_does_not_advance_primitive_frontier"] is True
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3


def test_observation_requires_authority_before_runner_call():
    m = _load()
    runner = FakeRunner(m)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "OBSERVATION_NOT_AUTHORIZED",
        lambda: m.collect_rootless_docker_runtime_image_receipt(
            observation_authorized=False,
            reviewed_source_sha256=REVIEWED_SOURCE_SHA,
            run_command=runner,
        ),
    )
    assert runner.calls == []


def test_malformed_source_sha_rejected_before_runner_call():
    m = _load()
    runner = FakeRunner(m)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "source SHA malformed",
        lambda: m.collect_rootless_docker_runtime_image_receipt(
            observation_authorized=True,
            reviewed_source_sha256="not-a-sha",
            run_command=runner,
        ),
    )
    assert runner.calls == []


def test_noncallable_runner_is_rejected():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "command runner required",
        lambda: m.collect_rootless_docker_runtime_image_receipt(
            observation_authorized=True,
            reviewed_source_sha256=REVIEWED_SOURCE_SHA,
            run_command=None,
        ),
    )


def test_valid_fake_collection_uses_exact_command_order():
    m = _load()
    runner = FakeRunner(m)
    _collect(m, runner)
    assert runner.calls == [
        m.CONTEXT_COMMAND,
        m.INFO_COMMAND,
        m.IMAGE_INSPECT_COMMAND,
    ]


def test_valid_fake_collection_returns_exact_image_identity():
    m = _load()
    receipt = _collect(m)
    assert receipt["runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID
    assert receipt["runtime_image_identity_observation_performed"] is True
    assert receipt["backend_kind"] == "rootless_docker_local_image_store_v1"
    assert receipt["observation_mode"] == "read_only"


def test_valid_fake_collection_reports_no_actions():
    m = _load()
    receipt = _collect(m)
    for field in (
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    ):
        assert receipt[field] is False


def test_valid_fake_collection_carries_reviewed_candidate_metadata():
    m = _load()
    receipt = _collect(m)
    meta = receipt["_candidate_metadata"]
    assert meta["context_name"] == "rootless"
    assert meta["context_host"] == "unix:///run/user/1000/docker.sock"
    assert meta["docker_root_dir"] == "/home/zoso/.local/share/docker"
    assert meta["rootless_security"] is True
    assert meta["reviewed_image_tag_present"] is True
    assert meta["reviewed_repo_digest_present"] is True
    assert meta["generation_label"] == "ad1926569b12466c"
    assert meta["purpose_label"] == "joint-duel-sandbox"
    assert meta["working_dir"] == "/opt/openra"
    assert meta["openra_entrypoint_prefix"] == ["dotnet", "/opt/openra/bin/OpenRA.dll"]


def test_strip_candidate_metadata_matches_interface_field_set():
    m = _load()
    receipt = _collect(m)
    stripped = m.strip_candidate_metadata(receipt)
    assert set(stripped) == set(m.runtime_image_interface.BACKEND_RECEIPT_FIELDS)
    assert "_candidate_metadata" not in stripped


def test_canonical_interface_accepts_stripped_fake_receipt_but_does_not_verify():
    m = _load()
    receipt = m.strip_candidate_metadata(_collect(m))
    out = m.runtime_image_interface.validate_runtime_image_backend_receipt(
        receipt,
        expected_source_sha256=REVIEWED_SOURCE_SHA,
    )
    assert out["backend_receipt_valid"] is True
    assert out["runtime_image_identity_observed"] is True
    assert out["runtime_image_identity_matches_expected"] is True
    assert out["runtime_image_identity_verified"] is False
    assert out["collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False


def test_context_name_drift_rejected():
    m = _load()
    context = _context_payload(m)
    context[0]["Name"] = "default"
    runner = FakeRunner(m, context=context)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "context name drift",
        lambda: _collect(m, runner),
    )


def test_context_host_drift_rejected():
    m = _load()
    context = _context_payload(m)
    context[0]["Endpoints"]["docker"]["Host"] = "unix:///var/run/docker.sock"
    runner = FakeRunner(m, context=context)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "context host drift",
        lambda: _collect(m, runner),
    )


def test_context_tls_drift_rejected():
    m = _load()
    context = _context_payload(m)
    context[0]["Endpoints"]["docker"]["SkipTLSVerify"] = True
    runner = FakeRunner(m, context=context)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "TLS setting drift",
        lambda: _collect(m, runner),
    )


def test_nonrootless_daemon_rejected():
    m = _load()
    info = _info_payload(m)
    info["SecurityOptions"] = ["name=seccomp,profile=builtin"]
    runner = FakeRunner(m, info=info)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "daemon is not rootless",
        lambda: _collect(m, runner),
    )


def test_docker_data_root_drift_rejected():
    m = _load()
    info = _info_payload(m)
    info["DockerRootDir"] = "/var/lib/docker"
    runner = FakeRunner(m, info=info)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "data-root drift",
        lambda: _collect(m, runner),
    )


def test_image_id_drift_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["Id"] = "sha256:" + "0" * 64
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "image ID drift",
        lambda: _collect(m, runner),
    )


def test_reviewed_tag_missing_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["RepoTags"] = []
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "reviewed tag missing",
        lambda: _collect(m, runner),
    )


def test_reviewed_repo_digest_missing_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["RepoDigests"] = []
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "reviewed repo digest missing",
        lambda: _collect(m, runner),
    )


def test_generation_label_drift_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["Config"]["Labels"]["void.openra.generation"] = "other"
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "generation label drift",
        lambda: _collect(m, runner),
    )


def test_purpose_label_drift_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["Config"]["Labels"]["void.openra.purpose"] = "other"
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "purpose label drift",
        lambda: _collect(m, runner),
    )


def test_working_dir_drift_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["Config"]["WorkingDir"] = "/tmp"
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "working directory drift",
        lambda: _collect(m, runner),
    )


def test_openra_entrypoint_drift_rejected():
    m = _load()
    image = _image_payload(m)
    image[0]["Config"]["Entrypoint"][1] = "/wrong/OpenRA.dll"
    runner = FakeRunner(m, image=image)
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "OpenRA entrypoint drift",
        lambda: _collect(m, runner),
    )


def test_command_failure_rejected():
    m = _load()
    runner = FakeRunner(m, rc_by_command={m.INFO_COMMAND: 1})
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendHold,
        "INFO: command failed",
        lambda: _collect(m, runner),
    )


def test_unreviewed_command_rejected_before_subprocess():
    m = _load()
    original = m.subprocess.run

    def trap(*args, **kwargs):
        raise AssertionError("subprocess must not be reached")

    m.subprocess.run = trap
    try:
        _expect_hold(
            m.RuntimeV2R13RootlessDockerImageBackendHold,
            "COMMAND_NOT_REVIEWED",
            lambda: m.host_readonly_command_runner(
                (m.DOCKER, "ps")
            ),
        )
    finally:
        m.subprocess.run = original


def test_mutating_command_rejected_before_subprocess():
    m = _load()
    original = m.subprocess.run

    def trap(*args, **kwargs):
        raise AssertionError("subprocess must not be reached")

    m.subprocess.run = trap
    try:
        _expect_hold(
            m.RuntimeV2R13RootlessDockerImageBackendHold,
            "COMMAND_NOT_REVIEWED",
            lambda: m.host_readonly_command_runner(
                (m.DOCKER, "run", "alpine")
            ),
        )
    finally:
        m.subprocess.run = original


def test_static_source_has_no_automatic_host_runner_invocation():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    calls = [_dotted(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    assert calls.count("subprocess.run") == 1
    assert "host_readonly_command_runner" not in calls
    assert "collect_rootless_docker_runtime_image_receipt" not in calls


def test_static_source_has_no_forbidden_docker_mutation_commands():
    m = _load()
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    string_values = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, str)
    ]
    allowed_command_strings = {
        part
        for command in m.ALLOWED_COMMANDS
        for part in command
    }
    for token in m.FORBIDDEN_DOCKER_TOKENS:
        if token in string_values:
            assert token not in allowed_command_strings
