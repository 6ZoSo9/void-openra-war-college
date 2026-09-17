"""Source-only cross-control runtime selector for Abaddon Generation-2.

This module closes only the deterministic runtime-selection implementation gap.
It selects the already-reviewed opponent runtime realization bound to a canonical
Generation-2 execution descriptor.  Selection is keyed by exact snapshot
identity, not merely by runtime class, so controls that share a runtime class
remain distinct.

The selector never starts a runtime, performs network or host observation,
materializes commands or workdirs, launches OpenRA/models, trains, deploys,
mutates VOID, or moves funds.  Runtime authority, command materialization, and
isolated-workdir allocation remain separate blockers.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_execution_adapter_generation2 as execution_adapter,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_source_binding_review_generation2
    as materializer_review,
)
from openra_env.learning import (
    apollyon_opponent_runtime_realizations as runtime_realizations,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.cross-control-runtime-selector-contract.v1"
)
SELECTION_SCHEMA = (
    "void.abaddon.generation2.cross-control-runtime-selection.v1"
)

EXECUTION_ADAPTER_GIT_BLOB = "994d44d751c530619649322c72a65edf15f6a8c3"
RUNTIME_REALIZATIONS_GIT_BLOB = "0dbae61b0be96445e5fd6c23a07491a03f18b679"
MATERIALIZER_REVIEW_GIT_BLOB = "3dcc325c431ec451a737b6e228c365ce1acb4f98"
ORCHESTRATOR_GIT_BLOB = "8948b53d002e5d7e48a7aef2ec10ff5d690f5a1c"

RUNTIME_REALIZATION_SET_SHA256 = (
    "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"
)
OPPONENT_SNAPSHOT_SET_SHA256 = (
    "d7bfce0cb1456ec440f6ab362c781057837c3912c557f865ae95b7ddc6278526"
)

EXPECTED_RUNTIME_BINDINGS = {
    "apollyon-v13-v14-promoted": {
        "snapshot_sha256": (
            "457d0516ac22072ee4f69064763d002461fe056539be996a503b8c8fdefd0173"
        ),
        "runtime_class": "promoted_loopback_openai_runtime",
    },
    "apollyon-v13-v10-promoted": {
        "snapshot_sha256": (
            "be50560fd21f400bf72d5dfcf1312d86c3d1911b1bcc691cc1f1cc0aa0259239"
        ),
        "runtime_class": "promoted_loopback_openai_runtime",
    },
    "apollyon-v2r13-qualified-predecessor": {
        "snapshot_sha256": (
            "731da9720a3e3aecd7fe455cb951f9e1f0fbda7b2f9acc6be4ddfebe74ec4be6"
        ),
        "runtime_class": "legacy_warm_start_ollama_openai_tool_runtime",
    },
    "apollyon-v3-v8-accepted-model-control": {
        "snapshot_sha256": (
            "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667"
        ),
        "runtime_class": "accepted_v8_adapter_frozen_chat_template_tool_runtime",
    },
}

PRE_SELECTOR_BLOCKERS = tuple(execution_adapter.EXECUTION_BLOCKERS)
POST_SELECTOR_BLOCKERS = (
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)
POST_SELECTOR_SOURCE_BLOCKERS = (
    "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)

NEXT_GATE = "CROSS_CONTROL_RUNTIME_SELECTOR_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_cross_control_runtime_selector_source_binding_review"


class CrossControlRuntimeSelectorHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CrossControlRuntimeSelectorHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _realization_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_stable_bytes(dict(value))).hexdigest()


def _runtime_index() -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for raw in runtime_realizations.REVIEWED_REALIZATIONS:
        runtime_realizations.validate_realization(raw)
        snapshot_id = raw.get("snapshot_id")
        _require(
            snapshot_id in EXPECTED_RUNTIME_BINDINGS,
            f"unexpected reviewed runtime snapshot: {snapshot_id!r}",
        )
        expected = EXPECTED_RUNTIME_BINDINGS[snapshot_id]
        _require(
            raw.get("snapshot_sha256") == expected["snapshot_sha256"],
            f"runtime snapshot SHA drift: {snapshot_id}",
        )
        _require(
            raw.get("runtime_class") == expected["runtime_class"],
            f"runtime class drift: {snapshot_id}",
        )
        _require(
            raw.get("runtime_surface_realized") is True,
            f"runtime surface unrealized: {snapshot_id}",
        )
        _require(
            raw.get("warm_start_input_surface_compatible") is True,
            f"runtime input incompatible: {snapshot_id}",
        )
        _require(
            raw.get("portable_current_checkout_binding_complete") is True,
            f"runtime portable binding incomplete: {snapshot_id}",
        )
        _require(
            raw.get("current_campaign_runtime_realized") is True,
            f"runtime campaign realization incomplete: {snapshot_id}",
        )
        _require(raw.get("blockers") == [], f"runtime blockers present: {snapshot_id}")
        _require(snapshot_id not in rows, f"duplicate runtime snapshot: {snapshot_id}")
        rows[snapshot_id] = {
            **deepcopy(dict(raw)),
            "realization_sha256": _realization_sha256(raw),
        }

    _require(
        set(rows) == set(EXPECTED_RUNTIME_BINDINGS),
        "reviewed runtime snapshot set drift",
    )
    return rows


def _validate_dependencies() -> dict[str, Any]:
    review = (
        materializer_review
        .v2r13_frozen_worktree_materializer_source_binding_review_contract()
    )
    _require(
        review.get("frozen_worktree_materializer_reviewed") is True,
        "materializer source review not accepted",
    )
    _require(
        review.get("activation_source_review_frontier_complete") is True,
        "activation source-review frontier incomplete",
    )
    _require(
        review.get("runtime_execution_authorized") is False,
        "runtime unexpectedly authorized before selector",
    )
    _require(
        tuple(review.get("execution_materialization_source_blockers", ()))
        == (
            "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
            "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
            "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
        ),
        "pre-selector execution source blocker set drift",
    )
    _require(
        review.get("next_gate")
        == "CROSS_CONTROL_RUNTIME_SELECTOR_IMPLEMENTATION_REQUIRED",
        "pre-selector next gate drift",
    )

    runtime_index = _runtime_index()
    descriptors = execution_adapter.all_execution_descriptors()
    _require(len(descriptors) == 36, "execution descriptor cardinality drift")

    pair_bindings: dict[int, tuple[str, str]] = {}
    seen_snapshots: set[str] = set()

    for descriptor in descriptors:
        _require(
            descriptor.get("schema") == execution_adapter.DESCRIPTOR_SCHEMA,
            "execution descriptor schema drift",
        )
        _require(
            descriptor.get("runtime", {}).get(
                "cross_control_selector_implemented"
            )
            is False,
            "accepted execution adapter unexpectedly implements selector",
        )
        _require(
            descriptor.get("runtime", {}).get("selection_performed") is False,
            "accepted execution adapter unexpectedly selects runtime",
        )
        _require(
            descriptor.get("runtime", {}).get("started") is False,
            "accepted execution adapter unexpectedly starts runtime",
        )
        _require(
            tuple(descriptor.get("reasons", ())) == PRE_SELECTOR_BLOCKERS,
            "pre-selector blocker set drift",
        )
        _require(
            descriptor.get("eligible") is False,
            "pre-selector execution descriptor unexpectedly eligible",
        )
        _require(
            descriptor.get("authority", {}).get("runtime_execution_authorized")
            is False,
            "pre-selector descriptor unexpectedly authorizes runtime",
        )

        opponent = descriptor.get("apollyon_opponent")
        _require(isinstance(opponent, Mapping), "opponent descriptor missing")
        snapshot_id = opponent.get("snapshot_id")
        _require(
            snapshot_id in runtime_index,
            f"descriptor runtime snapshot not reviewed: {snapshot_id!r}",
        )
        expected_runtime = runtime_index[snapshot_id]
        _require(
            opponent.get("snapshot_sha256")
            == expected_runtime["snapshot_sha256"],
            "descriptor opponent snapshot SHA drift",
        )
        _require(
            opponent.get("selection_boundary")
            == "EXTERNAL_PRELAUNCH_REVIEWED_RUNTIME_REALIZATION",
            "descriptor runtime selection boundary drift",
        )
        _require(
            opponent.get("selection_performed") is False,
            "opponent runtime unexpectedly selected in accepted adapter",
        )
        _require(
            opponent.get("runtime_started") is False,
            "opponent runtime unexpectedly started in accepted adapter",
        )
        _require(
            opponent.get("runtime_realization") == expected_runtime,
            f"embedded runtime realization drift: {snapshot_id}",
        )

        pair_slot = descriptor.get("pair_slot")
        arm = descriptor.get("arm")
        _require(
            type(pair_slot) is int and 1 <= pair_slot <= 18,
            "descriptor pair slot drift",
        )
        _require(arm in {"baseline", "candidate"}, "descriptor arm drift")
        binding = (snapshot_id, expected_runtime["realization_sha256"])
        if pair_slot in pair_bindings:
            _require(
                pair_bindings[pair_slot] == binding,
                f"matched-pair runtime disagreement: {pair_slot}",
            )
        else:
            pair_bindings[pair_slot] = binding
        seen_snapshots.add(snapshot_id)

    _require(len(pair_bindings) == 18, "matched-pair runtime binding count drift")
    _require(
        seen_snapshots == set(EXPECTED_RUNTIME_BINDINGS),
        "not all reviewed controls appear in execution descriptors",
    )

    return {
        "materializer_review_contract": deepcopy(review),
        "runtime_index": deepcopy(runtime_index),
        "execution_descriptors": deepcopy(descriptors),
    }


def cross_control_runtime_selector_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    runtime_index = dependencies["runtime_index"]
    return {
        "schema": CONTRACT_SCHEMA,
        "execution_adapter_git_blob": EXECUTION_ADAPTER_GIT_BLOB,
        "runtime_realizations_git_blob": RUNTIME_REALIZATIONS_GIT_BLOB,
        "materializer_review_git_blob": MATERIALIZER_REVIEW_GIT_BLOB,
        "orchestrator_git_blob": ORCHESTRATOR_GIT_BLOB,
        "runtime_realization_set_sha256": RUNTIME_REALIZATION_SET_SHA256,
        "opponent_snapshot_set_sha256": OPPONENT_SNAPSHOT_SET_SHA256,
        "cross_control_runtime_selector_implemented": True,
        "cross_control_runtime_selector_reviewed": False,
        "selection_key": "opponent_snapshot_id",
        "runtime_class_is_not_selection_key": True,
        "reviewed_runtime_count": len(runtime_index),
        "reviewed_runtime_class_count": len(
            {row["runtime_class"] for row in runtime_index.values()}
        ),
        "execution_descriptor_count": 36,
        "matched_pair_count": 18,
        "selector_accepts_only_canonical_execution_descriptors": True,
        "selector_preserves_matched_pair_runtime_identity": True,
        "selector_removes_only_its_execution_blocker": True,
        "runtime_selection_source_only": True,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "command_materialized": False,
        "workdir_materialized": False,
        "runtime_execution_authorized": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "pre_selector_blockers": PRE_SELECTOR_BLOCKERS,
        "post_selector_blockers": POST_SELECTOR_BLOCKERS,
        "post_selector_source_blockers": POST_SELECTOR_SOURCE_BLOCKERS,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def select_cross_control_runtime(
    descriptor: Mapping[str, Any],
) -> dict[str, Any]:
    """Select the exact reviewed runtime bound to one canonical descriptor."""
    _require(isinstance(descriptor, Mapping), "execution descriptor must be object")
    pair_slot = descriptor.get("pair_slot")
    arm = descriptor.get("arm")
    _require(type(pair_slot) is int, "execution descriptor pair_slot must be int")
    _require(arm in {"baseline", "candidate"}, "execution descriptor arm unsupported")

    canonical = execution_adapter.execution_descriptor(
        pair_slot=pair_slot,
        arm=str(arm),
    )
    _require(
        dict(descriptor) == canonical,
        "execution descriptor is not canonical accepted adapter output",
    )

    runtime_index = _runtime_index()
    opponent = canonical["apollyon_opponent"]
    snapshot_id = opponent["snapshot_id"]
    selected = runtime_index[snapshot_id]
    _require(
        opponent["runtime_realization"] == selected,
        "canonical descriptor runtime realization disagrees with reviewed selector index",
    )

    return {
        "schema": SELECTION_SCHEMA,
        "pair_slot": pair_slot,
        "arm": arm,
        "execution_index": canonical["execution_index"],
        "selection_key": snapshot_id,
        "opponent_snapshot_id": snapshot_id,
        "opponent_snapshot_sha256": selected["snapshot_sha256"],
        "runtime_class": selected["runtime_class"],
        "runtime_realization_sha256": selected["realization_sha256"],
        "runtime_identity": deepcopy(selected["identity"]),
        "input_surface": deepcopy(selected["input_surface"]),
        "selection_boundary": opponent["selection_boundary"],
        "cross_control_selector_implemented": True,
        "selection_performed": True,
        "selection_is_source_only": True,
        "runtime_started": False,
        "command_materialized": False,
        "workdir_materialized": False,
        "runtime_execution_authorized": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "remaining_blockers": POST_SELECTOR_BLOCKERS,
        "selected_runtime_realization": deepcopy(selected),
    }


def select_runtime(*, pair_slot: int, arm: str) -> dict[str, Any]:
    return select_cross_control_runtime(
        execution_adapter.execution_descriptor(
            pair_slot=pair_slot,
            arm=arm,
        )
    )


def selected_execution_descriptor(
    *,
    pair_slot: int,
    arm: str,
) -> dict[str, Any]:
    descriptor = execution_adapter.execution_descriptor(
        pair_slot=pair_slot,
        arm=arm,
    )
    selection = select_cross_control_runtime(descriptor)
    composed = deepcopy(descriptor)
    composed["runtime"] = {
        "cross_control_selector_implemented": True,
        "selection_performed": True,
        "started": False,
        "selection": deepcopy(selection),
    }
    composed["reasons"] = list(POST_SELECTOR_BLOCKERS)
    composed["eligible"] = False
    return composed


def all_selected_execution_descriptors() -> list[dict[str, Any]]:
    return [
        selected_execution_descriptor(
            pair_slot=int(row["pair_slot"]),
            arm=str(row["arm"]),
        )
        for row in execution_adapter.all_execution_descriptors()
    ]


def materialize_command(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorHold(NEXT_GATE)


def allocate_isolated_workdir(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorHold(NEXT_GATE)


def start_runtime(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )
