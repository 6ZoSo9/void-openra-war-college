"""Reviewed portable frozen-checkout binding for the V2R13 campaign control.

The historical V2R13 campaign runner requires the War College source checkout at
an exact old commit.  This module makes that source requirement portable by
binding the exact legacy runner to a detached frozen source worktree while the
canonical current checkout remains untouched.  It does not create worktrees,
start runtimes, launch games, call a model, train, or mutate weights.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

BINDING_SCHEMA = "void.apollyon.v2r13-portable-checkout-binding.v1"

FROZEN_WAR_COLLEGE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_WAR_COLLEGE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
FROZEN_ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"

LEGACY_WARM_START_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)
BASE_JOINT_RUNNER_SHA256 = (
    "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615"
)
APOLLYON_BOUNDARY_RUNNER_SHA256 = (
    "72fb0e9909dcdddb6c4a7713a5aa55568d2bef43020e6478945ca69247590abc"
)
BROKER_V11_SOAK_V14_SHA256 = (
    "41e5a4a760b9d6e67f11c35f2ed70c29c96c2f94019d511d5e289142828879e3"
)
JOINT_PROTO_SHA256 = (
    "9a48ca90bd525b7fd5502e7426cd8c1bb96b1308c2b18904d4d7af023699eae3"
)
RUNTIME_IMAGE_ID = (
    "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
)
MODEL_ALIAS = "void-apollyon-candidate-v2r13:latest"
MODEL_DIGEST = "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"


class PortableCheckoutBindingError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PortableCheckoutBindingError(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def portable_binding_contract() -> dict[str, Any]:
    """Return the reviewed nonexecuting V2R13 portable-checkout contract."""
    body = {
        "schema": BINDING_SCHEMA,
        "frozen_war_college_commit": FROZEN_WAR_COLLEGE_COMMIT,
        "frozen_war_college_tree": FROZEN_WAR_COLLEGE_TREE,
        "frozen_engine_commit": FROZEN_ENGINE_COMMIT,
        "legacy_warm_start_runner_sha256": LEGACY_WARM_START_RUNNER_SHA256,
        "base_joint_runner_sha256": BASE_JOINT_RUNNER_SHA256,
        "apollyon_boundary_runner_sha256": APOLLYON_BOUNDARY_RUNNER_SHA256,
        "broker_v11_soak_v14_sha256": BROKER_V11_SOAK_V14_SHA256,
        "joint_proto_sha256": JOINT_PROTO_SHA256,
        "runtime_image_id": RUNTIME_IMAGE_ID,
        "model_alias": MODEL_ALIAS,
        "model_digest": MODEL_DIGEST,
        "source_materialization": "detached_git_worktree",
        "source_worktree_must_be_clean": True,
        "source_worktree_detached": True,
        "canonical_checkout_must_remain_unchanged": True,
        "canonical_checkout_mutation_required": False,
        "legacy_source_root_rebound": True,
        "base_source_root_rebound": True,
        "joint_proto_rebound_to_frozen_source": True,
        "engine_root_rebound_to_exact_engine_worktree": True,
        "runtime_image_identity_unchanged": True,
        "host_validation_unchanged": True,
        "input_surface_unchanged": True,
        "current_main_head_independent": True,
        "worktree_cleanup_required": True,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
        "training": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
    }
    return {
        **body,
        "binding_contract_sha256": _sha256(body),
    }


def _validate_expected_legacy_shape(legacy: Any) -> None:
    _require(
        getattr(legacy, "BASE_RUNNER_SHA", None) == BASE_JOINT_RUNNER_SHA256,
        "legacy base runner SHA binding drift",
    )
    _require(
        getattr(legacy, "WAR_COLLEGE_COMMIT", None) == FROZEN_WAR_COLLEGE_COMMIT,
        "legacy War College commit drift",
    )
    _require(
        getattr(legacy, "ENGINE_COMMIT", None) == FROZEN_ENGINE_COMMIT,
        "legacy engine commit drift",
    )
    _require(
        getattr(legacy, "IMAGE_ID", None) == RUNTIME_IMAGE_ID,
        "legacy runtime image drift",
    )
    _require(callable(getattr(legacy, "load_base", None)), "legacy load_base missing")


def _validate_expected_base_shape(base: Any) -> None:
    _require(
        getattr(base, "WAR_COLLEGE_COMMIT", None) == FROZEN_WAR_COLLEGE_COMMIT,
        "base War College commit drift",
    )
    _require(
        getattr(base, "ENGINE_COMMIT", None) == FROZEN_ENGINE_COMMIT,
        "base engine commit drift",
    )
    _require(
        getattr(base, "IMAGE_ID", None) == RUNTIME_IMAGE_ID,
        "base runtime image drift",
    )
    _require(
        getattr(base, "APOLLYON_RUNNER_SHA", None) == APOLLYON_BOUNDARY_RUNNER_SHA256,
        "base Apollyon boundary SHA drift",
    )
    _require(
        getattr(base, "PROTO_SHA", None) == JOINT_PROTO_SHA256,
        "base joint proto SHA drift",
    )
    _require(
        getattr(base, "APOLLYON_MODEL", None) == MODEL_ALIAS,
        "base Apollyon model alias drift",
    )


def reviewed_path_binding(
    *,
    frozen_source_root: Path,
    exact_engine_root: Path,
) -> dict[str, Any]:
    source = Path(frozen_source_root).expanduser().resolve()
    engine = Path(exact_engine_root).expanduser().resolve()
    _require(source != engine, "source and engine roots must be distinct")
    proto = source / "proto" / "rl_bridge.proto"
    return {
        "source_root": source,
        "engine_root": engine,
        "proto_path": proto,
        "frozen_war_college_commit": FROZEN_WAR_COLLEGE_COMMIT,
        "frozen_engine_commit": FROZEN_ENGINE_COMMIT,
    }


class PortableRunnerBinding:
    """Temporarily rebind exact legacy/base module paths to frozen worktrees.

    This changes only in-memory module globals.  It never calls either module's
    main function and therefore grants no execution authority.
    """

    def __init__(
        self,
        legacy: Any,
        *,
        frozen_source_root: Path,
        exact_engine_root: Path,
    ) -> None:
        _validate_expected_legacy_shape(legacy)
        self.legacy = legacy
        self.paths = reviewed_path_binding(
            frozen_source_root=frozen_source_root,
            exact_engine_root=exact_engine_root,
        )
        self._original_load_base = legacy.load_base
        self._legacy_values: dict[str, Any] = {}
        self._installed = False
        self.loaded_base: Any | None = None
        self._base_values: dict[str, Any] = {}

    def install(self) -> None:
        _require(not self._installed, "portable binding already installed")
        for key in ("RL", "OPENRA"):
            _require(hasattr(self.legacy, key), f"legacy {key} missing")
            self._legacy_values[key] = getattr(self.legacy, key)
        self.legacy.RL = self.paths["source_root"]
        self.legacy.OPENRA = self.paths["engine_root"]
        self.legacy.load_base = self._load_bound_base
        self._installed = True

    def _load_bound_base(self):
        _require(self._installed, "portable binding is not installed")
        base = self._original_load_base()
        _validate_expected_base_shape(base)
        for key in ("RL", "OPENRA", "PROTO"):
            _require(hasattr(base, key), f"base {key} missing")
            self._base_values[key] = getattr(base, key)
        base.RL = self.paths["source_root"]
        base.OPENRA = self.paths["engine_root"]
        base.PROTO = self.paths["proto_path"]
        self.loaded_base = base
        return base

    def restore(self) -> None:
        if not self._installed:
            return
        if self.loaded_base is not None:
            for key, value in self._base_values.items():
                setattr(self.loaded_base, key, value)
        for key, value in self._legacy_values.items():
            setattr(self.legacy, key, value)
        self.legacy.load_base = self._original_load_base
        self.loaded_base = None
        self._base_values.clear()
        self._legacy_values.clear()
        self._installed = False

    def __enter__(self):
        self.install()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.restore()
        return False

    def attestation(self) -> dict[str, Any]:
        _require(self._installed, "portable binding is not installed")
        base_bound = self.loaded_base is not None
        if base_bound:
            _require(
                Path(self.loaded_base.RL).resolve() == self.paths["source_root"],
                "base source root binding drift",
            )
            _require(
                Path(self.loaded_base.OPENRA).resolve() == self.paths["engine_root"],
                "base engine root binding drift",
            )
            _require(
                Path(self.loaded_base.PROTO).resolve() == self.paths["proto_path"],
                "base proto binding drift",
            )
        body = {
            "schema": BINDING_SCHEMA,
            "legacy_source_root_bound": (
                Path(self.legacy.RL).resolve() == self.paths["source_root"]
            ),
            "legacy_engine_root_bound": (
                Path(self.legacy.OPENRA).resolve() == self.paths["engine_root"]
            ),
            "base_loaded_and_bound": base_bound,
            "runtime_execution_performed": False,
            "model_execution_performed": False,
            "game_started": False,
        }
        return {
            **body,
            "attestation_sha256": _sha256(body),
        }
