"""Reviewed Apollyon opponent runtime-realization evidence.

This module classifies what is already executable or historically proven for the
three opponent controls bound by the Abaddon campaign.  It performs no runtime
or game action and grants no execution authority.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .apollyon_opponent_snapshots import reviewed_snapshot_set
from .apollyon_v10_campaign_translation import translation_contract
from .apollyon_v2r13_portable_checkout import portable_binding_contract

REALIZATION_SCHEMA = "void.apollyon.opponent-runtime-realization.v1"
REALIZATION_SET_SCHEMA = "void.apollyon.opponent-runtime-realization-set.v1"

V2R13 = {
    "schema": REALIZATION_SCHEMA,
    "snapshot_id": "apollyon-v2r13-qualified-predecessor",
    "snapshot_sha256":
        "731da9720a3e3aecd7fe455cb951f9e1f0fbda7b2f9acc6be4ddfebe74ec4be6",
    "runtime_class": "legacy_warm_start_ollama_openai_tool_runtime",
    "historical_game_facing_runtime_proven": True,
    "runtime_surface_realized": True,
    "warm_start_input_surface_compatible": True,
    "portable_current_checkout_binding_complete": True,
    "current_campaign_runtime_realized": True,
    "identity": {
        "legacy_warm_start_runner_sha256":
            "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901",
        "base_joint_runner_sha256":
            "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615",
        "apollyon_boundary_runner_sha256":
            "72fb0e9909dcdddb6c4a7713a5aa55568d2bef43020e6478945ca69247590abc",
        "portable_checkout_binding_source_sha256":
            "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d",
        "portable_checkout_binding_contract_sha256":
            "677e503e8d4827a9d8950a177f308ad08982f612d70881f16de2c271e3b10e49",
        "model_alias": "void-apollyon-candidate-v2r13:latest",
        "model_digest":
            "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932",
        "candidate_system_sha256":
            "6429fcc9086121a8a08eabc09a94cc911f1d7bcf6527917145b2c5aa37e2019f",
        "broker_v11_soak_v14_sha256":
            "41e5a4a760b9d6e67f11c35f2ed70c29c96c2f94019d511d5e289142828879e3",
        "engine_commit": "1607a7a6501d42a47638393ecef8b22831064932",
        "frozen_war_college_commit":
            "973802ef0a614e5afa782ff20e231e18966ae3e5",
        "frozen_war_college_tree":
            "d8a2af418af00e95ca0f203a2f0264851f2308c6",
        "runtime_image_id":
            "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5",
        "chat_completions_url":
            "http://127.0.0.1:11434/v1/chat/completions",
    },
    "input_surface": {
        "kind": "legacy_current_tool_list_plus_compact_state_json",
        "same_as_frozen_warm_start_runner": True,
        "translation_required": False,
        "portable_checkout_binding_reviewed": True,
        "source_materialization": "detached_git_worktree",
        "canonical_checkout_mutation_required": False,
        "host_validation_unchanged": True,
    },
    "blockers": [],
}

V10 = {
    "schema": REALIZATION_SCHEMA,
    "snapshot_id": "apollyon-v13-v10-promoted",
    "snapshot_sha256":
        "2c7c6a87908bf16ac3f3daab53faaa6e808f00be65f9c362f42af9595f540bf8",
    "runtime_class": "promoted_loopback_openai_runtime",
    "historical_game_facing_runtime_proven": True,
    "runtime_surface_realized": True,
    "warm_start_input_surface_compatible": True,
    "portable_current_checkout_binding_complete": True,
    "current_campaign_runtime_realized": True,
    "identity": {
        "candidate_sha256":
            "c351d98912dfe18ff8552da5e620b0e3ba6d9877dbc185c45be0dda0fd7d4025",
        "v8_adapter_sha256":
            "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6",
        "live_input_adapter_v4_sha256":
            "9ba6cfa75bea5ac708f7dd690f67640d3f84e03335de09c8a4514eb5c3437686",
        "live_input_contract_v6_sha256":
            "fe62a8488454e0974179519a53f79a2c823182daa5225b2ea455518a3489fcfe",
        "openai_bridge_v7_sha256":
            "c197f3b75016dd7c4c25346f98aafdb1f631e2ee6e8b3514f9ebb650490b4510",
        "campaign_translation_source_sha256":
            "2d32351dff8d96a3254436305c2c402ea06c9a344b6b3ea67cb70c512eef2d53",
        "campaign_translation_contract_sha256":
            "69c862387dad806681c5d066fea8e87836d2c0825f792ae293177c23cddee38b",
        "promotion_record_sha256":
            "5a5e857d253f986eae0bda5187638ca6547d874db840fb24ea30ec550306f444",
        "active_runtime_unit_sha256":
            "407f5f8514502005ecbaefd7e7df7caf90d8024e496f948c3db90d6405d6f320",
        "active_runtime_record_sha256":
            "46045916b96ed53ff7abb06a198358a500d50226beb46c72df16ed5d45309b9f",
        "model_id": "void-apollyon-v3-v13-guard-first-v10-shadow",
        "chat_completions_url":
            "http://127.0.0.1:11435/v1/chat/completions",
    },
    "input_surface": {
        "accepted_kind": "turn_briefing_plus_recent_tool_results",
        "campaign_kind": "legacy_current_tool_list_plus_compact_state_json",
        "translation_required": True,
        "translation_reviewed": True,
        "output_translation_reviewed": True,
        "current_state_only": True,
        "current_tool_list_authoritative": True,
        "host_validation_unchanged": True,
        "fabricated_information_allowed": False,
    },
    "blockers": [],
}

V8 = {
    "schema": REALIZATION_SCHEMA,
    "snapshot_id": "apollyon-v3-v8-accepted-model-control",
    "snapshot_sha256":
        "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667",
    "runtime_class": "accepted_adapter_without_frozen_war_college_tool_runtime",
    "historical_game_facing_runtime_proven": False,
    "runtime_surface_realized": False,
    "warm_start_input_surface_compatible": False,
    "portable_current_checkout_binding_complete": False,
    "current_campaign_runtime_realized": False,
    "identity": {
        "adapter_model_sha256":
            "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6",
        "training_report_v8_sha256":
            "b9286ec3535e2a16df20dbbac742b61e37b479e0808f3bdceb34eec54a127d75",
        "final_acceptance_pack_sha256":
            "61935b744187c272bd1d5f920b8b3031728a534a66fd74a72befaadee18bb239",
        "final_acceptance_driver_sha256":
            "8ab9e197ba605799cf511407f9e95042935264b18a6bb5af056fee07df2284e8",
    },
    "input_surface": {
        "kind": None,
        "tool_transport_frozen": False,
        "translation_required": True,
        "translation_reviewed": False,
    },
    "blockers": [
        "V8_WAR_COLLEGE_TOOL_RUNTIME_NOT_FROZEN",
    ],
}

REVIEWED_REALIZATIONS = (V2R13, V10, V8)


class RuntimeRealizationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeRealizationError(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def validate_realization(value: Mapping[str, Any]) -> None:
    _require(isinstance(value, Mapping), "realization must be object")
    _require(value.get("schema") == REALIZATION_SCHEMA, "realization schema drift")
    _require(
        isinstance(value.get("snapshot_id"), str) and bool(value["snapshot_id"]),
        "snapshot id required",
    )
    snapshot_sha = value.get("snapshot_sha256")
    _require(
        isinstance(snapshot_sha, str)
        and len(snapshot_sha) == 64
        and all(char in "0123456789abcdef" for char in snapshot_sha),
        "snapshot SHA-256 malformed",
    )
    for key in (
        "historical_game_facing_runtime_proven",
        "runtime_surface_realized",
        "warm_start_input_surface_compatible",
        "portable_current_checkout_binding_complete",
        "current_campaign_runtime_realized",
    ):
        _require(type(value.get(key)) is bool, f"{key} must be bool")
    _require(isinstance(value.get("identity"), Mapping), "runtime identity missing")
    _require(isinstance(value.get("input_surface"), Mapping), "input surface missing")
    _require(isinstance(value.get("blockers"), list), "blocker list missing")
    if value["current_campaign_runtime_realized"]:
        _require(value["runtime_surface_realized"], "campaign runtime lacks runtime surface")
        _require(
            value["warm_start_input_surface_compatible"],
            "campaign runtime lacks compatible warm-start input",
        )
        _require(
            value["portable_current_checkout_binding_complete"],
            "campaign runtime lacks portable checkout binding",
        )
        _require(not value["blockers"], "realized campaign runtime still has blockers")


def reviewed_opponent_runtime_realizations() -> dict[str, Any]:
    snapshot_set = reviewed_snapshot_set()
    translation = translation_contract()
    translation_path = Path(__file__).with_name("apollyon_v10_campaign_translation.py")
    _require(translation_path.is_file(), "V10 campaign translation source missing")
    translation_source_sha256 = hashlib.sha256(translation_path.read_bytes()).hexdigest()
    _require(
        translation_source_sha256
        == V10["identity"]["campaign_translation_source_sha256"],
        "V10 campaign translation source digest drift",
    )
    _require(
        translation["translation_contract_sha256"]
        == V10["identity"]["campaign_translation_contract_sha256"],
        "V10 campaign translation contract digest drift",
    )
    _require(
        translation["v10_candidate_sha256"] == V10["identity"]["candidate_sha256"],
        "V10 translation candidate binding drift",
    )
    _require(
        translation["v10_live_input_adapter_sha256"]
        == V10["identity"]["live_input_adapter_v4_sha256"],
        "V10 translation adapter binding drift",
    )
    _require(
        translation["v10_live_input_contract_sha256"]
        == V10["identity"]["live_input_contract_v6_sha256"],
        "V10 translation input-contract binding drift",
    )
    _require(
        translation["v10_openai_bridge_sha256"]
        == V10["identity"]["openai_bridge_v7_sha256"],
        "V10 translation bridge binding drift",
    )
    _require(
        translation["campaign_input_kind"] == V10["input_surface"]["campaign_kind"],
        "V10 campaign input kind drift",
    )
    _require(
        translation["accepted_input_kind"] == V10["input_surface"]["accepted_kind"],
        "V10 accepted input kind drift",
    )
    for key in (
        "input_translation_reviewed",
        "output_translation_reviewed",
        "current_state_only",
        "current_tool_list_authoritative",
        "host_validation_unchanged",
    ):
        _require(translation[key] is True, f"V10 translation contract lacks {key}")
    _require(
        translation["fabricated_information_allowed"] is False,
        "V10 translation permits fabricated information",
    )
    _require(
        translation["runtime_execution_performed"] is False
        and translation["model_execution_performed"] is False
        and translation["game_started"] is False,
        "V10 translation review crossed execution boundary",
    )
    portable = portable_binding_contract()
    portable_path = Path(__file__).with_name("apollyon_v2r13_portable_checkout.py")
    _require(portable_path.is_file(), "V2R13 portable checkout binding source missing")
    portable_source_sha256 = hashlib.sha256(portable_path.read_bytes()).hexdigest()
    _require(
        portable_source_sha256
        == V2R13["identity"]["portable_checkout_binding_source_sha256"],
        "V2R13 portable checkout binding source digest drift",
    )
    _require(
        portable["binding_contract_sha256"]
        == V2R13["identity"]["portable_checkout_binding_contract_sha256"],
        "V2R13 portable checkout binding contract digest drift",
    )
    _require(
        portable["frozen_war_college_commit"]
        == V2R13["identity"]["frozen_war_college_commit"],
        "V2R13 frozen source commit drift",
    )
    _require(
        portable["frozen_war_college_tree"]
        == V2R13["identity"]["frozen_war_college_tree"],
        "V2R13 frozen source tree drift",
    )
    _require(
        portable["frozen_engine_commit"] == V2R13["identity"]["engine_commit"],
        "V2R13 frozen engine commit drift",
    )
    _require(
        portable["legacy_warm_start_runner_sha256"]
        == V2R13["identity"]["legacy_warm_start_runner_sha256"],
        "V2R13 legacy runner binding drift",
    )
    _require(
        portable["base_joint_runner_sha256"]
        == V2R13["identity"]["base_joint_runner_sha256"],
        "V2R13 base runner binding drift",
    )
    _require(
        portable["apollyon_boundary_runner_sha256"]
        == V2R13["identity"]["apollyon_boundary_runner_sha256"],
        "V2R13 boundary runner binding drift",
    )
    _require(
        portable["broker_v11_soak_v14_sha256"]
        == V2R13["identity"]["broker_v11_soak_v14_sha256"],
        "V2R13 broker qualification binding drift",
    )
    for key in (
        "source_worktree_must_be_clean",
        "source_worktree_detached",
        "canonical_checkout_must_remain_unchanged",
        "legacy_source_root_rebound",
        "base_source_root_rebound",
        "joint_proto_rebound_to_frozen_source",
        "engine_root_rebound_to_exact_engine_worktree",
        "runtime_image_identity_unchanged",
        "host_validation_unchanged",
        "input_surface_unchanged",
        "current_main_head_independent",
        "worktree_cleanup_required",
    ):
        _require(portable[key] is True, f"V2R13 portable binding lacks {key}")
    _require(
        portable["canonical_checkout_mutation_required"] is False,
        "V2R13 portable binding requires canonical checkout mutation",
    )
    _require(
        portable["runtime_execution_performed"] is False
        and portable["model_execution_performed"] is False
        and portable["game_started"] is False,
        "V2R13 portable binding review crossed execution boundary",
    )
    snapshots = {
        row["snapshot_id"]: row
        for row in snapshot_set["snapshots"]
    }

    descriptors = []
    for realization in REVIEWED_REALIZATIONS:
        validate_realization(realization)
        snapshot_id = realization["snapshot_id"]
        _require(snapshot_id in snapshots, f"unknown snapshot: {snapshot_id}")
        _require(
            realization["snapshot_sha256"]
            == snapshots[snapshot_id]["snapshot_sha256"],
            f"snapshot digest drift: {snapshot_id}",
        )
        descriptors.append(
            {
                **dict(realization),
                "realization_sha256": _sha256(realization),
            }
        )

    ids = [row["snapshot_id"] for row in descriptors]
    _require(len(ids) == len(set(ids)) == 3, "exactly three unique realizations required")

    realized = [
        row for row in descriptors
        if row["current_campaign_runtime_realized"]
    ]
    blockers = [
        blocker
        for row in descriptors
        for blocker in row["blockers"]
    ]

    body = {
        "schema": REALIZATION_SET_SCHEMA,
        "opponent_snapshot_set_sha256": snapshot_set["snapshot_set_sha256"],
        "realizations": descriptors,
        "source_binding_complete": True,
        "historical_game_facing_runtime_count": sum(
            1
            for row in descriptors
            if row["historical_game_facing_runtime_proven"]
        ),
        "runtime_surface_realized_count": sum(
            1
            for row in descriptors
            if row["runtime_surface_realized"]
        ),
        "current_campaign_runtime_realized_count": len(realized),
        "opponent_runtime_realization_complete": len(realized) == 3,
        "blockers": blockers,
        "authority": {
            "runtime_execution_authorized": False,
            "game_started": False,
            "model_execution_performed": False,
            "training": False,
            "weights_updated": False,
            "automatic_corpus_admission": False,
            "automatic_policy_promotion": False,
        },
    }
    return {
        **body,
        "realization_set_sha256": _sha256(body),
    }
