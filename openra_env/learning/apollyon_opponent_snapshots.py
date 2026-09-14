"""Cryptographic source identities for Abaddon's Apollyon opponent controls.

These are source/evidence descriptors only.  They do not start a runtime,
execute OpenRA, mutate a model, admit training data, or grant promotion.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

SNAPSHOT_SCHEMA = "void.apollyon.opponent-snapshot.v1"
SNAPSHOT_SET_SCHEMA = "void.apollyon.opponent-snapshot-set.v1"

CURRENT_PROMOTED = {
    "schema": SNAPSHOT_SCHEMA,
    "snapshot_id": "apollyon-v13-v10-promoted",
    "role": "current_promoted",
    "promotion_proven": True,
    "runtime_activation_proven": True,
    "identity": {
        "candidate_sha256":
            "c351d98912dfe18ff8552da5e620b0e3ba6d9877dbc185c45be0dda0fd7d4025",
        "candidate_manifest_sha256":
            "dad33e3adad915b10110f2220ed7c3b0e951a9d85e639a15791513ae22628bba",
        "final_freeze_sha256":
            "b49e03b4e622f9251f5fb87735d40039a9d6db30abe57fd296feb8f43179a094",
        "final_acceptance_v7_report_sha256":
            "143f2f12d72245ebf80beac6a4e1d3e846c558aa274c8a000e509dbcea879367",
        "v8_adapter_sha256":
            "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6",
        "live_input_adapter_v4_sha256":
            "9ba6cfa75bea5ac708f7dd690f67640d3f84e03335de09c8a4514eb5c3437686",
        "live_input_contract_v6_sha256":
            "fe62a8488454e0974179519a53f79a2c823182daa5225b2ea455518a3489fcfe",
        "openai_bridge_v7_sha256":
            "c197f3b75016dd7c4c25346f98aafdb1f631e2ee6e8b3514f9ebb650490b4510",
        "promotion_record_sha256":
            "5a5e857d253f986eae0bda5187638ca6547d874db840fb24ea30ec550306f444",
        "active_runtime_unit_sha256":
            "407f5f8514502005ecbaefd7e7df7caf90d8024e496f948c3db90d6405d6f320",
        "active_runtime_record_sha256":
            "46045916b96ed53ff7abb06a198358a500d50226beb46c72df16ed5d45309b9f",
    },
}

PRIOR_QUALIFIED_PREDECESSOR = {
    "schema": SNAPSHOT_SCHEMA,
    "snapshot_id": "apollyon-v2r13-qualified-predecessor",
    "role": "prior_qualified_predecessor",
    "promotion_proven": False,
    "runtime_activation_proven": True,
    "identity": {
        "model_alias": "void-apollyon-candidate-v2r13:latest",
        "model_digest":
            "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932",
        "candidate_system_sha256":
            "6429fcc9086121a8a08eabc09a94cc911f1d7bcf6527917145b2c5aa37e2019f",
        "broker_v11_soak_v14_sha256":
            "41e5a4a760b9d6e67f11c35f2ed70c29c96c2f94019d511d5e289142828879e3",
        "hardening_sha256":
            "d3c81d5cd3f3dfbe0a45af4d7b7fa02a12efbb1ec361fd9ea3b8002aed6de833",
        "alignment_sandbox_sha256":
            "b5c6d4cc3e63e682118e67b2330a7011346628cff4e4e3d18b91e2cc061705f2",
        "local_only_sha256":
            "820df9b519b7c47a2047a5d7db98d7627802e66284915524fed46590aeea1508",
    },
}

PRIOR_ACCEPTED_MODEL_CONTROL = {
    "schema": SNAPSHOT_SCHEMA,
    "snapshot_id": "apollyon-v3-v8-accepted-model-control",
    "role": "prior_accepted_model_control",
    "promotion_proven": False,
    "runtime_activation_proven": False,
    "identity": {
        "adapter_model_sha256":
            "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6",
        "training_report_v8_sha256":
            "b9286ec3535e2a16df20dbbac742b61e37b479e0808f3bdceb34eec54a127d75",
        "final_acceptance_pack_sha256":
            "61935b744187c272bd1d5f920b8b3031728a534a66fd74a72befaadee18bb239",
        "final_acceptance_driver_sha256":
            "8ab9e197ba605799cf511407f9e95042935264b18a6bb5af056fee07df2284e8",
        "base_config_sha256":
            "14687c353af8012cc1b563b3aeeefaa0b78d8780d8ea5270c73fe9fcdb7387f2",
        "base_shard_1_sha256":
            "26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61",
        "base_shard_2_sha256":
            "cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188",
    },
}

REVIEWED_SNAPSHOTS = (
    CURRENT_PROMOTED,
    PRIOR_QUALIFIED_PREDECESSOR,
    PRIOR_ACCEPTED_MODEL_CONTROL,
)


class SnapshotContractError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SnapshotContractError(message)


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def stable_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def snapshot_sha256(snapshot: Mapping[str, Any]) -> str:
    validate_snapshot(snapshot)
    return hashlib.sha256(stable_json_bytes(snapshot)).hexdigest()


def validate_snapshot(snapshot: Mapping[str, Any]) -> None:
    _require(isinstance(snapshot, Mapping), "snapshot must be object")
    _require(snapshot.get("schema") == SNAPSHOT_SCHEMA, "snapshot schema drift")
    _require(
        snapshot.get("role")
        in {
            "current_promoted",
            "prior_qualified_predecessor",
            "prior_accepted_model_control",
            "previous_promoted_champion",
        },
        "snapshot role unsupported",
    )
    _require(
        type(snapshot.get("promotion_proven")) is bool,
        "promotion_proven must be bool",
    )
    _require(
        type(snapshot.get("runtime_activation_proven")) is bool,
        "runtime_activation_proven must be bool",
    )

    snapshot_id = snapshot.get("snapshot_id")
    _require(
        isinstance(snapshot_id, str) and bool(snapshot_id),
        "snapshot_id required",
    )
    identity = snapshot.get("identity")
    _require(isinstance(identity, Mapping) and bool(identity), "identity required")

    for key, value in identity.items():
        if key.endswith("_sha256") or key == "model_digest":
            _require(_is_sha256(value), f"{key} must be lowercase SHA-256")

    if snapshot["role"] == "current_promoted":
        _require(snapshot["promotion_proven"] is True, "current promotion not proven")
        _require(
            snapshot["runtime_activation_proven"] is True,
            "current runtime activation not proven",
        )


def reviewed_snapshot_set() -> dict[str, Any]:
    for snapshot in REVIEWED_SNAPSHOTS:
        validate_snapshot(snapshot)

    ids = [snapshot["snapshot_id"] for snapshot in REVIEWED_SNAPSHOTS]
    _require(len(ids) == len(set(ids)), "snapshot ids must be unique")

    roles = [snapshot["role"] for snapshot in REVIEWED_SNAPSHOTS]
    _require(roles.count("current_promoted") == 1, "exactly one current promoted required")

    previous_champions = [
        snapshot
        for snapshot in REVIEWED_SNAPSHOTS
        if snapshot["role"] == "previous_promoted_champion"
        and snapshot["promotion_proven"] is True
    ]
    previous_champion_proven = len(previous_champions) >= 1

    descriptors = [
        {
            **dict(snapshot),
            "snapshot_sha256": snapshot_sha256(snapshot),
        }
        for snapshot in REVIEWED_SNAPSHOTS
    ]
    set_payload = {
        "schema": SNAPSHOT_SET_SCHEMA,
        "snapshots": descriptors,
    }
    set_sha = hashlib.sha256(stable_json_bytes(set_payload)).hexdigest()

    reasons: list[str] = []
    if not previous_champion_proven:
        reasons.append("PREVIOUS_APOLLYON_CHAMPION_NOT_CRYPTOGRAPHICALLY_PROVEN")

    return {
        **set_payload,
        "snapshot_set_sha256": set_sha,
        "snapshot_count": len(descriptors),
        "source_identity_binding_complete": True,
        "minimum_snapshot_count_met": len(descriptors) >= 2,
        "current_promoted_snapshot_proven": True,
        "previous_champion_proven": previous_champion_proven,
        "qualified_for_campaign_opponent_set": not reasons,
        "reasons": reasons,
        "authority": {
            "runtime_execution_authorized": False,
            "training_use_approved": False,
            "automatic_training_admission": False,
            "automatic_weight_mutation": False,
            "automatic_policy_promotion": False,
        },
    }
