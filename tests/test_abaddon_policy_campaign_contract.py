from __future__ import annotations

import pytest

from openra_env.learning.abaddon_policy_campaign_contract import (
    ABADDON_REFINER_SHA256,
    CONTRACT_SCHEMA,
    DUEL_REVIEW_SCHEMA,
    FUNDAMENTALS,
    MAX_SINGLE_FUNDAMENTAL_REGRESSION,
    MIN_APOLLYON_SNAPSHOTS,
    MIN_COMPOSITE_GAIN,
    MIN_REVIEWED_MATCHES,
    MIN_VARIED_SEEDS,
    CampaignContractError,
    promotion_recommendation,
    reviewed_plan,
    validate_generation_review,
)


def review(
    score=0.70,
    *,
    matches=12,
    seeds=6,
    snapshots=2,
    infra=0,
    full_controller=True,
    safety=True,
    fundamentals=None,
):
    if fundamentals is None:
        fundamentals = {name: 0.70 for name in FUNDAMENTALS}
    return {
        "schema": DUEL_REVIEW_SCHEMA,
        "full_abaddon_controller_active": full_controller,
        "review_complete": True,
        "safety_invariants_green": safety,
        "matches": matches,
        "varied_seed_count": seeds,
        "opponent_snapshot_count": snapshots,
        "infra_failures": infra,
        "composite_score": score,
        "fundamentals": fundamentals,
    }


def test_plan_mirrors_recovered_refiner_policy_and_stays_nonexecuting():
    plan = reviewed_plan()
    assert plan["schema"] == CONTRACT_SCHEMA
    assert plan["abaddon_refiner_sha256"] == ABADDON_REFINER_SHA256
    assert plan["requirements"]["minimum_reviewed_matches"] == MIN_REVIEWED_MATCHES
    assert plan["requirements"]["minimum_varied_seeds"] == MIN_VARIED_SEEDS
    assert plan["requirements"]["minimum_apollyon_snapshots"] == MIN_APOLLYON_SNAPSHOTS
    assert plan["requirements"]["minimum_composite_gain"] == MIN_COMPOSITE_GAIN
    assert (
        plan["requirements"]["maximum_single_fundamental_regression"]
        == MAX_SINGLE_FUNDAMENTAL_REGRESSION
    )
    assert plan["pre_execution_gates"]["opponent_snapshot_binding_required"] is True
    assert plan["authority"]["runtime_execution_authorized"] is False
    assert plan["authority"]["automatic_training_admission"] is False
    assert plan["authority"]["automatic_policy_promotion"] is False


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"matches": 11}, "12 reviewed matches"),
        ({"seeds": 5}, "6 varied seeds"),
        ({"snapshots": 1}, "2 Apollyon snapshots"),
        ({"infra": 1}, "infrastructure failures must be zero"),
        ({"full_controller": False}, "proxy matches cannot qualify"),
        ({"safety": False}, "safety invariants not green"),
    ],
)
def test_review_prerequisites_fail_closed(kwargs, message):
    with pytest.raises(CampaignContractError, match=message):
        validate_generation_review(review(**kwargs))


def test_exact_minimum_review_is_valid():
    normalized = validate_generation_review(review())
    assert normalized["matches"] == 12
    assert normalized["varied_seed_count"] == 6
    assert normalized["opponent_snapshot_count"] == 2
    assert normalized["infra_failures"] == 0


def test_promotion_requires_minimum_gain():
    champion = review(0.70)
    candidate = review(0.719)
    result = promotion_recommendation(champion, candidate)
    assert result["recommend_promotion"] is False
    assert result["automatic_promotion"] is False

    candidate = review(0.72)
    result = promotion_recommendation(champion, candidate)
    assert result["recommend_promotion"] is True


def test_material_fundamental_regression_blocks_promotion():
    champion_f = {name: 0.70 for name in FUNDAMENTALS}
    candidate_f = dict(champion_f)
    candidate_f["force_preservation"] = 0.61
    result = promotion_recommendation(
        review(0.70, fundamentals=champion_f),
        review(0.80, fundamentals=candidate_f),
    )
    assert result["recommend_promotion"] is False
    assert result["dimension_regressions"]["force_preservation"] > 0.08
