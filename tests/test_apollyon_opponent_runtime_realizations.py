from __future__ import annotations

from openra_env.learning.apollyon_opponent_runtime_realizations import (
    V14,
    reviewed_opponent_runtime_realizations,
)


def test_v14_runtime_realization_is_complete_and_bound():
    assert V14["current_campaign_runtime_realized"] is True
    assert V14["warm_start_input_surface_compatible"] is True
    assert V14["input_surface"]["translation_reviewed"] is True
    assert V14["input_surface"]["output_translation_reviewed"] is True
    assert V14["identity"]["v14_campaign_translation_binding_contract_sha256"] == "f91c9b89155bb09eadf24d9491573fb8f8c364886cb2609c62616b7b355de677"
    assert V14["blockers"] == []


def test_runtime_realization_set_is_four_of_four_complete():
    result = reviewed_opponent_runtime_realizations()
    assert result["realization_set_sha256"] == "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"
    assert result["current_campaign_runtime_realized_count"] == 4
    assert result["opponent_runtime_realization_complete"] is True
    assert result["blockers"] == []
    assert result["authority"]["runtime_execution_authorized"] is False
