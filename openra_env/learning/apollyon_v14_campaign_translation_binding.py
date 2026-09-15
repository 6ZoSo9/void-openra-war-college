# Source-bound V14 campaign translation compatibility proof.

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .apollyon_v10_campaign_translation import translation_contract

SCHEMA = "void.apollyon.v14-campaign-translation-binding.v1"
FIXTURE_REL = "fixtures/learning/apollyon-v14-campaign-translation-binding-v1.json"
FIXTURE_SHA256 = "19321230b0a555b7d848be686768dc05773089b53ad5c580312a74bf49f90876"
TRANSLATION_SOURCE_SHA256 = "2d32351dff8d96a3254436305c2c402ea06c9a344b6b3ea67cb70c512eef2d53"
TRANSLATION_CONTRACT_SHA256 = "69c862387dad806681c5d066fea8e87836d2c0825f792ae293177c23cddee38b"
V14_CANDIDATE_SHA256 = "9d7c5a4121d2926e32955f9c7ee1b6cb6da3c6bf7f705c455ad4cb54f7f509db"
V14_LIVE_INPUT_ADAPTER_SHA256 = "9ba6cfa75bea5ac708f7dd690f67640d3f84e03335de09c8a4514eb5c3437686"
V14_PROMOTED_BRIDGE_SHA256 = "d5e99d9d9aecbf27f90dc7716dedc11127339ea1b7f5331cdfe7d906d3afbd25"
V14_PROMOTION_RECORD_SHA256 = "c7195d13f0579ff07da0cdfe98522dd64f4b4ffc3a86c67a91a19d7b61d1fd66"
V14_PROMOTION_RECONCILIATION_SHA256 = "274833334fad538717630b9575c7e1c4f04ae210237124663f33bed3ab6139d4"


class V14CampaignTranslationBindingError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V14CampaignTranslationBindingError(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def v14_campaign_translation_binding_contract() -> dict[str, Any]:
    fixture_path = _repo_root() / FIXTURE_REL
    raw = fixture_path.read_bytes()
    _require(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "binding fixture SHA drift")
    fixture = json.loads(raw.decode("utf-8"))
    _require(fixture.get("schema") == "VOID_APOLLYON_V14_CAMPAIGN_TRANSLATION_BINDING_V1",
             "binding fixture schema drift")
    compatibility = fixture.get("compatibility") or {}
    _require(compatibility.get("deterministic_vectors_green") == 6,
             "deterministic vector count drift")
    _require(compatibility.get("movement_identity_green") is True,
             "movement identity proof missing")
    _require(compatibility.get("v14_campaign_translation_binding_complete") is True,
             "V14 translation binding incomplete")
    _require(compatibility.get("opponent_runtime_realization_complete") is True,
             "opponent runtime realization incomplete")
    authority = fixture.get("authority") or {}
    for key in (
        "runtime_execution",
        "model_execution",
        "game_started",
        "game_mutation",
        "training",
        "weights_updated",
        "abaddon_campaign_execution",
        "runtime_execution_authorized",
    ):
        _require(authority.get(key) is False, f"authority boundary drift: {key}")
    tc = translation_contract()
    _require(tc["translation_contract_sha256"] == TRANSLATION_CONTRACT_SHA256,
             "translation contract digest drift")
    body = {
        "schema": SCHEMA,
        "fixture_sha256": FIXTURE_SHA256,
        "translation_source_sha256": TRANSLATION_SOURCE_SHA256,
        "translation_contract_sha256": TRANSLATION_CONTRACT_SHA256,
        "v14_candidate_sha256": V14_CANDIDATE_SHA256,
        "v14_live_input_adapter_sha256": V14_LIVE_INPUT_ADAPTER_SHA256,
        "v14_promoted_bridge_sha256": V14_PROMOTED_BRIDGE_SHA256,
        "v14_promotion_record_sha256": V14_PROMOTION_RECORD_SHA256,
        "v14_promotion_reconciliation_sha256": V14_PROMOTION_RECONCILIATION_SHA256,
        "deterministic_compatibility_vectors": 6,
        "movement_identity_translation_green": True,
        "binding_complete": True,
        "opponent_runtime_realization_complete": True,
        "runtime_execution_authorized": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
        "training": False,
        "weights_updated": False,
        "abaddon_campaign_execution": False,
    }
    return {
        **body,
        "binding_contract_sha256": hashlib.sha256(_stable_bytes(body)).hexdigest(),
    }
