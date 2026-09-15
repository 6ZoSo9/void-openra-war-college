from __future__ import annotations

from openra_env.learning.abaddon_policy_campaign_contract_generation2 import (
    reviewed_plan,
)


def test_generation2_contract_preserves_manual_review_and_authority_walls():
    result = reviewed_plan()
    plan = result["precommitted_campaign_plan"]

    assert result["status"] == "READY_PENDING_RUNTIME_EXECUTION_AUTHORIZATION"
    assert plan["plan_sha256"] == "64e5003fa0d339ea1bea14eb0e4026e0dfe3455e86f38ef0fb9c0a26fbc4c594"
    assert plan["candidate"]["generation"] == 2
    assert plan["candidate"]["candidate_index"] == 252
    assert plan["candidate"]["candidate_genome_sha256"] == "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
    assert plan["execution_eligible"] is False

    assert result["requirements"]["minimum_reviewed_matches"] == 12
    assert result["requirements"]["minimum_varied_seeds"] == 6
    assert result["requirements"]["minimum_apollyon_snapshots"] == 2
    assert result["requirements"]["minimum_composite_gain"] == 0.02
    assert result["requirements"]["maximum_single_fundamental_regression"] == 0.08

    assert result["pre_execution_gates"]["pair_evidence_required"] is True
    assert result["pre_execution_gates"]["manual_review_required"] is True
    assert result["authority"]["runtime_execution_authorized"] is False
    assert result["authority"]["training_use_approved"] is False
    assert result["authority"]["automatic_training_admission"] is False
    assert result["authority"]["automatic_weight_mutation"] is False
    assert result["authority"]["automatic_policy_promotion"] is False
