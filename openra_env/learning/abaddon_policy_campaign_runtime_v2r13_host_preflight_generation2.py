"""Read-only host-preflight semantics for bounded Generation-2 V2R13 execution.

The validator in this module admits only an exact local Precision host snapshot.
Snapshot collection is separate and may use read-only host backends. Importing
this module performs no filesystem, Git, Docker, systemd, network, model, game,
training, deployment, VOID-chain, wallet, or funds action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_source_binding_review_generation2
    as executor_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-execution-host-preflight-contract.v1"
)
SNAPSHOT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-execution-host-preflight-snapshot.v1"
)
ADMISSION_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-execution-host-preflight-admission.v1"
)

EXECUTOR_REVIEW_GIT_BLOB = "9111f921db54bf58dc8046328f7d05cf319d6ebb"

EXPECTED_HOSTNAME = "zoso-Precision-Tower-7810"
EXPECTED_HOME = "/home/zoso"
EXPECTED_SOURCE_ROOT = "/home/zoso/dev/openra-rl-war-college"
EXPECTED_ENGINE_ROOT = "/home/zoso/dev/openra-rl-war-college/OpenRA"
EXPECTED_DOJO_ROOT = "/home/zoso/dev/void-apollyon-dojo"
EXPECTED_DOWNLOADS_ROOT = "/home/zoso/Downloads"
EXPECTED_PROTO_PYTHON = (
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)

FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
FROZEN_ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"

GENERATION = "ad1926569b12466c"
RUNTIME_IMAGE = f"void-openra-joint-duel:{GENERATION}"
RUNTIME_IMAGE_ID = (
    "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
)

OLLAMA_SERVICE = "ollama.service"
ACTIVATION_PERMIT = "/etc/void/allow-local-ollama-model-runtime"
DORMANT_FUSE = (
    "/etc/systemd/system/ollama.service.d/"
    "zzzz-void-local-model-dormant-fuse-v1.conf"
)
DORMANT_CONDITION = f"ConditionPathExists={ACTIVATION_PERMIT}"

AUTHORIZED_PAIR_SLOTS = (3, 9, 15)
AUTHORIZED_ARMS = ("baseline", "candidate")

TRACKED_BLOBS = {
    "authorization_source": {
        "path": (
            "openra_env/learning/"
            "abaddon_policy_campaign_runtime_v2r13_execution_authorization_acceptance_generation2.py"
        ),
        "blob": "2501d48ae889b9ed17cdf42acef033023f7d3886",
    },
    "executor_source": {
        "path": (
            "openra_env/learning/"
            "abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2.py"
        ),
        "blob": "c7e20c1157e0bcf7f65036631aad47fb82c7aefd",
    },
    "executor_review_source": {
        "path": (
            "openra_env/learning/"
            "abaddon_policy_campaign_runtime_v2r13_bounded_executor_source_binding_review_generation2.py"
        ),
        "blob": EXECUTOR_REVIEW_GIT_BLOB,
    },
    "candidate_wrapper": {
        "path": "tools/abaddon_policy_candidate_duel_wrapper.py",
        "blob": "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776",
    },
    "candidate_fixture": {
        "path": (
            "fixtures/learning/"
            "abaddon-policy-genome-generation-2-candidate-252.json"
        ),
        "blob": "20091bff54edbb567127722fae81e5a5308737d2",
    },
}

EXTERNAL_FILES = {
    "legacy_warm_start_runner": {
        "path": (
            "/home/zoso/Downloads/"
            "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
        ),
        "sha256": "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901",
    },
    "base_joint_runner": {
        "path": (
            "/home/zoso/Downloads/"
            "void-actual-apollyon-vs-abaddon-joint-sparring-batch-v1_2.py"
        ),
        "sha256": "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615",
    },
    "apollyon_boundary_runner": {
        "path": (
            "/home/zoso/Downloads/"
            "void-apollyon-openra-war-college-attested-run-v1_13.py"
        ),
        "sha256": "72fb0e9909dcdddb6c4a7713a5aa55568d2bef43020e6478945ca69247590abc",
    },
    "v2r13_broker_soak": {
        "path": (
            "/home/zoso/Downloads/"
            "void-apollyon-v2r13-seeded-stochastic-adversarial-soak-v14.py"
        ),
        "sha256": "41e5a4a760b9d6e67f11c35f2ed70c29c96c2f94019d511d5e289142828879e3",
    },
    "runtime_authority_report": {
        "path": (
            "/home/zoso/Downloads/"
            "void-openra-joint-duel-effect-authority-smoke-v1_2-20260827T062507.json"
        ),
        "sha256": "1073b98f938c8095b50ce97812e2fd08557e93ca491de2868b1b0a8250a5355f",
    },
    "abaddon_controller": {
        "path": "/home/zoso/dev/void-apollyon-dojo/dojo/abaddon_controller.py",
        "sha256": "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103",
    },
    "abaddon_refiner": {
        "path": "/home/zoso/dev/void-apollyon-dojo/dojo/abaddon_refiner.py",
        "sha256": "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b",
    },
    "joint_training_attestation": {
        "path": (
            "/home/zoso/dev/void-apollyon-dojo/provenance/"
            "joint-duel-training-eligibility-v1.json"
        ),
        "sha256": "1368c737d0f7acae8aabfa539d5e9f51cd87a987bd2d4a03e0cde32d8d0378dd",
    },
    "fastadvance_training_attestation": {
        "path": (
            "/home/zoso/dev/void-apollyon-dojo/provenance/"
            "fastadvance-training-eligibility-v1.json"
        ),
        "sha256": "191db2dcd1d3b501aa5b36824982e474a69e09b420c4cb453ac95ce358ac859f",
    },
    "ollama_hardening_dropin": {
        "path": (
            "/etc/systemd/system/ollama.service.d/"
            "zzzz-void-apollyon-ollama-hardening-v1.conf"
        ),
        "sha256": "d3c81d5cd3f3dfbe0a45af4d7b7fa02a12efbb1ec361fd9ea3b8002aed6de833",
    },
    "ollama_alignment_sandbox_dropin": {
        "path": (
            "/etc/systemd/system/ollama.service.d/"
            "zzzzzz-void-apollyon-alignment-sandbox-v1.conf"
        ),
        "sha256": "b5c6d4cc3e63e682118e67b2330a7011346628cff4e4e3d18b91e2cc061705f2",
    },
    "ollama_local_only_dropin": {
        "path": (
            "/etc/systemd/system/ollama.service.d/"
            "zzzzzzz-void-apollyon-local-only-v1.conf"
        ),
        "sha256": "820df9b519b7c47a2047a5d7db98d7627802e66284915524fed46590aeea1508",
    },
}

NEXT_GATE = "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_host_preflight_source_binding_review"


class V2R13HostPreflightHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13HostPreflightHold(message)


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _validate_review_frontier() -> dict[str, Any]:
    contract = executor_review.v2r13_bounded_executor_source_binding_review_contract()
    _require(
        contract.get("bounded_v2r13_runtime_executor_source_binding_present") is True,
        "bounded executor source binding missing",
    )
    _require(
        contract.get("bounded_v2r13_runtime_executor_reviewed") is True,
        "bounded executor review missing",
    )
    _require(
        contract.get("runtime_execution_authorization_accepted") is True,
        "V2R13 runtime authorization not accepted",
    )
    _require(
        contract.get("runtime_execution_implemented") is True,
        "V2R13 runtime executor not implemented",
    )
    _require(
        contract.get("runtime_execution_performed") is False,
        "runtime execution already performed by source review",
    )
    _require(
        contract.get("host_preflight_completed") is False,
        "source review unexpectedly claims host preflight",
    )
    _require(
        tuple(contract.get("execution_source_blockers", ())) == (),
        "execution source blocker reappeared",
    )
    _require(
        tuple(contract.get("execution_blockers", ()))
        == ("V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_REQUIRED",),
        "host-preflight frontier drift",
    )
    return deepcopy(contract)


def host_preflight_contract() -> dict[str, Any]:
    review = _validate_review_frontier()
    return {
        "schema": CONTRACT_SCHEMA,
        "executor_review_git_blob": EXECUTOR_REVIEW_GIT_BLOB,
        "expected_hostname": EXPECTED_HOSTNAME,
        "expected_home": EXPECTED_HOME,
        "expected_source_root": EXPECTED_SOURCE_ROOT,
        "expected_engine_root": EXPECTED_ENGINE_ROOT,
        "expected_dojo_root": EXPECTED_DOJO_ROOT,
        "expected_downloads_root": EXPECTED_DOWNLOADS_ROOT,
        "expected_proto_python": EXPECTED_PROTO_PYTHON,
        "frozen_source_commit": FROZEN_SOURCE_COMMIT,
        "frozen_source_tree": FROZEN_SOURCE_TREE,
        "frozen_engine_commit": FROZEN_ENGINE_COMMIT,
        "runtime_image": RUNTIME_IMAGE,
        "runtime_image_id": RUNTIME_IMAGE_ID,
        "ollama_service": OLLAMA_SERVICE,
        "tracked_blobs": deepcopy(TRACKED_BLOBS),
        "external_files": deepcopy(EXTERNAL_FILES),
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "host_preflight_validator_implemented": True,
        "real_host_collector_implemented_by_this_source": False,
        "read_only_snapshot_required": True,
        "runtime_execution_authorized": True,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "executor_review": review,
    }


def _validate_exact_file_rows(rows: Mapping[str, Any]) -> None:
    _require(isinstance(rows, Mapping), "external file census missing")
    _require(set(rows) == set(EXTERNAL_FILES), "external file label set drift")
    for label, expected in EXTERNAL_FILES.items():
        row = rows[label]
        _require(isinstance(row, Mapping), f"external file row malformed: {label}")
        _require(row.get("path") == expected["path"], f"external path drift: {label}")
        _require(row.get("exists") is True, f"external file missing: {label}")
        _require(row.get("is_file") is True, f"external path not file: {label}")
        _require(row.get("is_symlink") is False, f"external file symlinked: {label}")
        _require(
            row.get("sha256") == expected["sha256"],
            f"external SHA-256 drift: {label}",
        )


def _validate_tracked_blobs(rows: Mapping[str, Any]) -> None:
    _require(isinstance(rows, Mapping), "tracked blob census missing")
    _require(set(rows) == set(TRACKED_BLOBS), "tracked blob label set drift")
    for label, expected in TRACKED_BLOBS.items():
        row = rows[label]
        _require(isinstance(row, Mapping), f"tracked blob row malformed: {label}")
        _require(row.get("path") == expected["path"], f"tracked path drift: {label}")
        _require(row.get("blob") == expected["blob"], f"tracked blob drift: {label}")


def _validate_arm_paths(rows: Mapping[str, Any], isolated_root: str) -> None:
    _require(isinstance(rows, Mapping), "authorized arm-path census missing")
    expected_keys = {
        f"{pair_slot}:{arm}"
        for pair_slot in AUTHORIZED_PAIR_SLOTS
        for arm in AUTHORIZED_ARMS
    }
    _require(set(rows) == expected_keys, "authorized arm-path key set drift")
    for pair_slot in AUTHORIZED_PAIR_SLOTS:
        for arm in AUTHORIZED_ARMS:
            key = f"{pair_slot}:{arm}"
            row = rows[key]
            _require(isinstance(row, Mapping), f"arm-path row malformed: {key}")
            expected = (
                f"{isolated_root}/generation2/pair-{pair_slot:02d}/{arm}"
            )
            _require(row.get("path") == expected, f"arm-path drift: {key}")
            _require(row.get("exists") is False, f"arm-path already exists: {key}")


def validate_host_preflight_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Admit one exact, read-only Precision host snapshot."""
    _validate_review_frontier()
    _require(isinstance(snapshot, Mapping), "host preflight snapshot must be object")
    _require(snapshot.get("schema") == SNAPSHOT_SCHEMA, "host snapshot schema drift")

    expected_main_head = snapshot.get("expected_main_head")
    _require(
        isinstance(expected_main_head, str) and len(expected_main_head) == 40,
        "expected main head malformed",
    )
    _require(
        all(char in "0123456789abcdef" for char in expected_main_head),
        "expected main head must be lowercase hex",
    )

    _require(snapshot.get("hostname") == EXPECTED_HOSTNAME, "Precision hostname drift")
    _require(snapshot.get("home") == EXPECTED_HOME, "Precision home path drift")

    source = snapshot.get("source_repository")
    _require(isinstance(source, Mapping), "source repository snapshot missing")
    _require(source.get("root") == EXPECTED_SOURCE_ROOT, "source repository root drift")
    _require(source.get("toplevel") == EXPECTED_SOURCE_ROOT, "source toplevel drift")
    _require(source.get("branch") == "main", "source checkout must be on main")
    _require(source.get("head") == expected_main_head, "source main head drift")
    _require(
        source.get("head_tree") == source.get("expected_head_tree"),
        "source main tree drift",
    )
    _require(source.get("tracked_status") == "", "source tracked worktree dirty")
    _require(
        source.get("frozen_source_commit") == FROZEN_SOURCE_COMMIT,
        "frozen source commit unavailable or drifted",
    )
    _require(
        source.get("frozen_source_tree") == FROZEN_SOURCE_TREE,
        "frozen source tree unavailable or drifted",
    )
    _validate_tracked_blobs(source.get("tracked_blobs"))

    engine = snapshot.get("engine_repository")
    _require(isinstance(engine, Mapping), "engine repository snapshot missing")
    _require(engine.get("root") == EXPECTED_ENGINE_ROOT, "engine repository root drift")
    _require(engine.get("toplevel") == EXPECTED_ENGINE_ROOT, "engine toplevel drift")
    _require(engine.get("tracked_status") == "", "engine tracked worktree dirty")
    _require(
        engine.get("frozen_engine_commit") == FROZEN_ENGINE_COMMIT,
        "frozen engine commit unavailable or drifted",
    )

    proto = snapshot.get("proto_python")
    _require(isinstance(proto, Mapping), "proto Python snapshot missing")
    _require(proto.get("path") == EXPECTED_PROTO_PYTHON, "proto Python path drift")
    _require(proto.get("exists") is True, "proto Python missing")
    _require(proto.get("is_file") is True, "proto Python is not file-like")

    isolated = snapshot.get("isolated_workdir")
    _require(isinstance(isolated, Mapping), "isolated workdir snapshot missing")
    isolated_root = isolated.get("root")
    _require(
        isinstance(isolated_root, str) and isolated_root.startswith(EXPECTED_HOME + "/"),
        "isolated workdir root must be under Precision home",
    )
    _require(isolated.get("exists") is True, "isolated workdir root missing")
    _require(isolated.get("is_dir") is True, "isolated workdir root not directory")
    _require(isolated.get("is_symlink") is False, "isolated workdir root symlinked")
    _validate_arm_paths(isolated.get("authorized_arm_paths"), isolated_root)

    _validate_exact_file_rows(snapshot.get("external_files"))

    docker = snapshot.get("docker")
    _require(isinstance(docker, Mapping), "Docker snapshot missing")
    _require(docker.get("context") == "rootless", "rootless Docker context required")
    _require(docker.get("info_contains_rootless") is True, "rootless Docker daemon required")
    _require(docker.get("image") == RUNTIME_IMAGE, "runtime image name drift")
    _require(docker.get("image_id") == RUNTIME_IMAGE_ID, "runtime image identity drift")
    _require(docker.get("generation_label") == GENERATION, "runtime image label drift")
    stale = docker.get("stale_warmstart_containers")
    _require(isinstance(stale, list) and stale == [], "stale warm-start container present")

    ollama = snapshot.get("ollama")
    _require(isinstance(ollama, Mapping), "Ollama snapshot missing")
    _require(ollama.get("service") == OLLAMA_SERVICE, "Ollama service drift")
    _require(ollama.get("active") == "inactive", "Ollama must begin inactive")
    _require(ollama.get("enabled") == "disabled", "Ollama must begin disabled")
    _require(ollama.get("activation_permit_present") is False, "activation permit leaked")
    fuse_present = ollama.get("dormant_fuse_present")
    _require(type(fuse_present) is bool, "dormant fuse presence malformed")
    if fuse_present:
        _require(
            ollama.get("dormant_condition_present") is True,
            "dormant fuse does not bind activation permit",
        )
    else:
        _require(
            ollama.get("dormant_condition_present") is False,
            "dormant condition reported without fuse",
        )

    authority = snapshot.get("authority")
    _require(isinstance(authority, Mapping), "host snapshot authority block missing")
    for field in (
        "git_fetch_performed",
        "git_checkout_performed",
        "filesystem_mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "policy_promotion_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(authority.get(field) is False, f"host preflight crossed boundary: {field}")

    digest = _canonical_sha256(snapshot)
    return {
        "schema": ADMISSION_SCHEMA,
        "snapshot_sha256": digest,
        "expected_main_head": expected_main_head,
        "host_preflight_completed": True,
        "host_preflight_green": True,
        "runtime_execution_authorization_accepted": True,
        "runtime_execution_implemented": True,
        "runtime_execution_authorized": True,
        "runtime_execution_performed": False,
        "fresh_readiness_still_required_before_inference": True,
        "automatic_retry": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_EVIDENCE_ACCEPTANCE_REQUIRED",
        "snapshot": deepcopy(dict(snapshot)),
    }


def collect_host_preflight_snapshot(*args: Any, **kwargs: Any) -> None:
    raise V2R13HostPreflightHold(
        "REAL_HOST_COLLECTION_NOT_IMPLEMENTED_BY_VALIDATOR_SOURCE"
    )


def execute_v2r13_runtime(*args: Any, **kwargs: Any) -> None:
    raise V2R13HostPreflightHold(NEXT_GATE)
