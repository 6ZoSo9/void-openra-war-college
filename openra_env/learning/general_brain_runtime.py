from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .general_brain_generation import (
    NONTRAINABLE_AUTHORITY_ENVELOPE,
    manifest_sha256,
    validate_brain_manifest,
)
from .general_brain_training import adapter_sha256, validate_adapter

BRAIN_RUN_SCHEMA = "void.general-brain-runtime-binding.v1"
BRAIN_ROUND_SCHEMA = "void.general-brain-runtime-round.v1"


class GeneralBrainRuntimeError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GeneralBrainRuntimeError(message)


def _sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _read_json(path: Path, label: str) -> Mapping[str, Any]:
    path = path.expanduser().resolve()
    _require(path.is_file(), f"{label} missing: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GeneralBrainRuntimeError(f"cannot read {label}: {error}") from error
    _require(isinstance(value, Mapping), f"{label} must contain an object")
    return value


def file_sha256(path: Path) -> str:
    path = path.expanduser().resolve()
    _require(path.is_file(), f"file missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_challenger_binding(
    *,
    adapter_path: Path,
    challenger_manifest_path: Path,
    expected_adapter_sha256: str,
    expected_challenger_file_sha256: str,
) -> dict[str, Any]:
    expected_adapter = _sha(expected_adapter_sha256, "expected adapter SHA-256")
    expected_manifest_file = _sha(
        expected_challenger_file_sha256,
        "expected challenger file SHA-256",
    )
    actual_adapter_file = file_sha256(adapter_path)
    actual_manifest_file = file_sha256(challenger_manifest_path)
    _require(actual_adapter_file == expected_adapter, "adapter file SHA-256 drift")
    _require(
        actual_manifest_file == expected_manifest_file,
        "challenger manifest file SHA-256 drift",
    )

    adapter = dict(_read_json(adapter_path, "adapter"))
    manifest = dict(_read_json(challenger_manifest_path, "challenger manifest"))
    validate_adapter(adapter)
    validate_brain_manifest(manifest)

    _require(adapter.get("general_id") == "apollyon", "challenger adapter must belong to Apollyon")
    _require(manifest.get("general_id") == "apollyon", "challenger manifest must belong to Apollyon")
    _require(manifest.get("generation") == 1, "challenger generation must be 1")
    competence = manifest.get("competence_adapter")
    _require(isinstance(competence, Mapping), "challenger competence_adapter missing")
    _require(competence.get("state") == "challenger", "Generation 1 must remain challenger-only")

    semantic_adapter = adapter_sha256(adapter)
    semantic_manifest = manifest_sha256(manifest)
    _require(semantic_adapter == expected_adapter, "adapter semantic SHA-256 drift")
    _require(
        competence.get("artifact_sha256") == semantic_adapter,
        "challenger manifest is not bound to adapter artifact",
    )
    _require(
        manifest.get("authority_envelope") == NONTRAINABLE_AUTHORITY_ENVELOPE,
        "challenger authority envelope drift",
    )

    return {
        "schema": BRAIN_RUN_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "challenger_only": True,
        "adapter_sha256": semantic_adapter,
        "adapter_file_sha256": actual_adapter_file,
        "challenger_manifest_sha256": semantic_manifest,
        "challenger_manifest_file_sha256": actual_manifest_file,
        "adapter": copy.deepcopy(adapter),
        "manifest": copy.deepcopy(manifest),
        "authority_envelope_trainable": False,
        "sovereign_directives_trainable": False,
        "tool_authorization_trainable": False,
        "automatic_weight_install": False,
        "automatic_promotion": False,
        "review_required": True,
    }


def tactical_overlay(
    binding: Mapping[str, Any],
    *,
    mode: str,
    offered_tool_names: Sequence[str],
) -> dict[str, Any]:
    _require(binding.get("schema") == BRAIN_RUN_SCHEMA, "General Brain run binding schema drift")
    _require(isinstance(mode, str) and mode, "mode must be nonempty text")
    names = tuple(offered_tool_names)
    _require(bool(names), "offered tool surface must not be empty")
    _require(all(isinstance(name, str) and name for name in names), "offered tools malformed")
    _require(len(names) == len(set(names)), "offered tools contain duplicates")

    adapter = binding.get("adapter")
    _require(isinstance(adapter, Mapping), "adapter binding missing")
    raw_weights = adapter.get("weights")
    _require(isinstance(raw_weights, Mapping), "adapter weights missing")
    raw_mode = raw_weights.get(mode, {})
    _require(isinstance(raw_mode, Mapping), "mode weights malformed")

    offered_weights: dict[str, float] = {}
    for tool, raw_score in raw_mode.items():
        _require(isinstance(tool, str) and tool, "adapter tool weight name malformed")
        _require(type(raw_score) in (int, float), "adapter tool weight must be numeric")
        if tool in names:
            offered_weights[tool] = float(raw_score)

    preferred_tool: str | None = None
    preferred_score: float | None = None
    if offered_weights:
        preferred_tool, preferred_score = sorted(
            offered_weights.items(),
            key=lambda item: (-item[1], item[0]),
        )[0]
        if preferred_score <= 0:
            preferred_tool = None
            preferred_score = None

    preferred_arguments: dict[str, Any] = {}
    if mode == "FORCE_CONVERSION" and preferred_tool == "move_units":
        preferred_arguments = {"unit_ids": "all_combat"}

    lines = [
        "GENERAL_BRAIN_COMPETENCE_ADAPTER_V1",
        "GENERAL_ID=apollyon",
        "GENERAL_BRAIN_GENERATION=1",
        f"TACTICAL_MODE={mode}",
        "TACTICAL_WEIGHT_SCOPE=tactical_competence_only",
        "OFFERED_TOOL_NAMES=" + ",".join(names),
        "OFFERED_TACTICAL_WEIGHTS=" + ",".join(
            f"{tool}:{offered_weights[tool]:g}" for tool in sorted(offered_weights)
        ),
        "AUTHORITY_ENVELOPE_TRAINABLE=false",
        "TOOL_AUTHORIZATION_TRAINABLE=false",
        "BOUNDARY=This adapter is tactical preference guidance only. Use only a currently offered host-authorized tool.",
    ]
    if preferred_tool is not None:
        lines.append(f"LEARNED_PREFERRED_TOOL={preferred_tool}")
        lines.append(f"LEARNED_PREFERENCE_WEIGHT={preferred_score:g}")
    if preferred_arguments:
        lines.append('LEARNED_PREFERRED_ARGUMENTS=unit_ids="all_combat"')
    coaching = "\n".join(lines)

    return {
        "schema": BRAIN_ROUND_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "mode": mode,
        "adapter_sha256": binding["adapter_sha256"],
        "challenger_manifest_sha256": binding["challenger_manifest_sha256"],
        "offered_tool_names": list(names),
        "offered_weights": dict(sorted(offered_weights.items())),
        "preferred_tool": preferred_tool,
        "preferred_score": preferred_score,
        "preferred_arguments": preferred_arguments,
        "preference_applied": preferred_tool is not None,
        "tool_surface_unchanged": True,
        "authority_envelope_trainable": False,
        "tool_authorization_trainable": False,
        "automatic_weight_install": False,
        "automatic_promotion": False,
        "coaching": coaching,
    }


__all__ = [
    "BRAIN_ROUND_SCHEMA",
    "BRAIN_RUN_SCHEMA",
    "GeneralBrainRuntimeError",
    "file_sha256",
    "load_challenger_binding",
    "tactical_overlay",
]
