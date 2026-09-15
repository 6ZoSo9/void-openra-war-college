from __future__ import annotations

from openra_env.learning.apollyon_v14_campaign_translation_binding import (
    v14_campaign_translation_binding_contract,
)


def test_v14_campaign_translation_binding_is_complete_and_nonexecuting():
    result = v14_campaign_translation_binding_contract()
    assert result["binding_contract_sha256"] == "f91c9b89155bb09eadf24d9491573fb8f8c364886cb2609c62616b7b355de677"
    assert result["binding_complete"] is True
    assert result["opponent_runtime_realization_complete"] is True
    assert result["runtime_execution_authorized"] is False
    assert result["runtime_execution_performed"] is False
    assert result["model_execution_performed"] is False
    assert result["game_started"] is False
    assert result["training"] is False
    assert result["weights_updated"] is False
    assert result["abaddon_campaign_execution"] is False
