from __future__ import annotations

from openra_env.learning.abaddon_policy_campaign_contract import reviewed_plan


def test_contract_waits_only_for_separate_runtime_execution_authorization():
    result = reviewed_plan()
    assert result["status"] == "READY_PENDING_RUNTIME_EXECUTION_AUTHORIZATION"
    assert result["opponent_snapshot_set"]["previous_champion_proven"] is True
    assert result["opponent_runtime_realizations"]["opponent_runtime_realization_complete"] is True
    assert result["precommitted_campaign_plan"]["plan_sha256"] == "2a3f13699b29f1f8fcc4a5d4e31609ada0bc8524f42e0cf9e86642dc1d374e98"
    assert result["precommitted_campaign_plan"]["execution_eligible"] is False
    assert result["pre_execution_gates"]["previous_champion_binding_complete"] is True
    assert result["pre_execution_gates"]["opponent_runtime_realization_complete"] is True
    assert result["authority"]["runtime_execution_authorized"] is False
