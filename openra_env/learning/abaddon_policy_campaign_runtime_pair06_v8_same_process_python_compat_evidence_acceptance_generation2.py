"""Accept exact Precision evidence for pair-06 V8/proto Python compatibility.

The read-only observer proved both venvs resolve to Python 3.12.3 on
/usr/bin/python3.12, but their site-packages differ. The accepted V8 environment
contains protobuf 7.36.1 and lacks grpc/grpc_tools. The accepted proto/game
environment contains grpc 1.75.1, grpc_tools.protoc, and protobuf 6.33.6.

The exact legacy base runner's generate_proto() invokes:
    sys.executable -m grpc_tools.protoc
Therefore the legacy game path cannot run unchanged inside the accepted V8
environment without changing its accepted package set.

This source records evidence only. It performs no host observation, package
install, model load, inference, game execution, service action, network action,
training, chain mutation, wallet action, or funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-same-process-python-compat-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-same-process-python-compat-evidence-acceptance.v1"
)

OBSERVER_SHA256 = (
    "98cd66991e9e0a61c009a5ca7d5103d52ae4fd777cad1c83319dd906561ce42f"
)
EXECUTION_MAIN_HEAD = "213fcc39d1ef61455da1564032ccbb5930f0112a"
V8_PYTHON = (
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/"
    "venv/bin/python3.12"
)
PROTO_PYTHON = (
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)
RESOLVED_PYTHON = "/usr/bin/python3.12"
BASE_RUNNER_SHA256 = (
    "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615"
)
COMPATIBILITY_VERDICT = (
    "INCOMPATIBLE_V8_ENVIRONMENT_MISSING_LEGACY_GAME_DEPENDENCIES"
)

EXPECTED_EVIDENCE = {
    "observer_sha256": OBSERVER_SHA256,
    "execution_main_head": EXECUTION_MAIN_HEAD,
    "pair_slot": 6,
    "arm": "baseline",
    "held_out": False,
    "filesystem_mutation": False,
    "package_install": False,
    "model_load": False,
    "model_inference": False,
    "game_execution": False,
    "network_request": False,
    "service_action": False,
    "v8_python": V8_PYTHON,
    "v8_python_resolved": RESOLVED_PYTHON,
    "v8_python_version": (3, 12, 3),
    "v8_import_grpc": False,
    "v8_import_grpc_tools_protoc": False,
    "v8_import_google_protobuf": True,
    "v8_protobuf_version": "7.36.1",
    "proto_python": PROTO_PYTHON,
    "proto_python_resolved": RESOLVED_PYTHON,
    "proto_python_version": (3, 12, 3),
    "proto_import_grpc": True,
    "proto_grpc_version": "1.75.1",
    "proto_import_grpc_tools_protoc": True,
    "proto_import_google_protobuf": True,
    "proto_protobuf_version": "6.33.6",
    "resolved_interpreter_identity_equal": True,
    "v8_has_legacy_grpc_proto_dependencies": False,
    "base_runner_sha256": BASE_RUNNER_SHA256,
    "generate_proto_uses_sys_executable": True,
    "generate_proto_invokes_grpc_tools_protoc": True,
    "legacy_main_executable_identity_check_passes": True,
    "same_process_v8_can_import_legacy_game_dependencies": False,
    "compatibility_verdict": COMPATIBILITY_VERDICT,
}

NEXT_GATE = "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_child_runtime_split_design"


class Pair06V8PythonCompatEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PythonCompatEvidenceAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def accept_pair06_v8_python_compat_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _require(isinstance(evidence, Mapping), "pair06 Python compatibility evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair06 Python compatibility evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair06 Python compatibility evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair06 Python compatibility evidence digest drift",
    )
    _require(
        supplied["resolved_interpreter_identity_equal"] is True,
        "pair06 Python executable identity drift",
    )
    _require(
        supplied["v8_has_legacy_grpc_proto_dependencies"] is False,
        "pair06 V8 environment unexpectedly gained legacy game dependencies",
    )
    _require(
        supplied["generate_proto_uses_sys_executable"] is True
        and supplied["generate_proto_invokes_grpc_tools_protoc"] is True,
        "pair06 legacy proto generation behavior drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_same_process_python_compat_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "observer_sha256": OBSERVER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "v8_python": V8_PYTHON,
        "proto_python": PROTO_PYTHON,
        "resolved_python": RESOLVED_PYTHON,
        "same_system_python_binary": True,
        "separate_virtualenv_site_packages": True,
        "v8_has_legacy_grpc_proto_dependencies": False,
        "same_process_legacy_game_path_compatible": False,
        "package_install_into_v8_authorized": False,
        "cross_venv_site_packages_injection_authorized": False,
        "parent_child_runtime_split_required": True,
        "model_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def pair06_v8_python_compat_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_python_compat_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_same_process_python_compat_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "same_system_python_binary": True,
        "separate_virtualenv_site_packages": True,
        "same_process_legacy_game_path_compatible": False,
        "parent_child_runtime_split_required": True,
        "package_install_into_v8_authorized": False,
        "cross_venv_site_packages_injection_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def execute_or_install(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PythonCompatEvidenceAcceptanceHold(NEXT_GATE)
