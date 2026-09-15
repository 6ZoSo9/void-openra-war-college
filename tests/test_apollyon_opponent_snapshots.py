from __future__ import annotations

from openra_env.learning.apollyon_opponent_snapshots import (
    CURRENT_PROMOTED,
    PREVIOUS_PROMOTED_CHAMPION,
    PRIOR_ACCEPTED_MODEL_CONTROL,
    PRIOR_QUALIFIED_PREDECESSOR,
    SNAPSHOT_SET_SCHEMA,
    reviewed_snapshot_set,
    snapshot_sha256,
)


def test_current_promoted_v14_identity_is_exactly_bound():
    current = CURRENT_PROMOTED
    assert current["snapshot_id"] == "apollyon-v13-v14-promoted"
    assert current["role"] == "current_promoted"
    assert current["promotion_proven"] is True
    assert current["runtime_activation_proven"] is True
    assert current["identity"]["candidate_sha256"] == "9d7c5a4121d2926e32955f9c7ee1b6cb6da3c6bf7f705c455ad4cb54f7f509db"
    assert current["identity"]["promotion_record_sha256"] == "c7195d13f0579ff07da0cdfe98522dd64f4b4ffc3a86c67a91a19d7b61d1fd66"
    assert len(snapshot_sha256(current)) == 64


def test_v10_is_cryptographically_proven_previous_promoted_champion():
    prior = PREVIOUS_PROMOTED_CHAMPION
    assert prior["snapshot_id"] == "apollyon-v13-v10-promoted"
    assert prior["role"] == "previous_promoted_champion"
    assert prior["promotion_proven"] is True
    assert prior["runtime_activation_proven"] is True
    assert prior["identity"]["candidate_sha256"] == "c351d98912dfe18ff8552da5e620b0e3ba6d9877dbc185c45be0dda0fd7d4025"
    assert prior["identity"]["previous_champion_record_sha256"] == "1115aa2230c294839787aaff93cf3db107a613d4268d580c08086587b6aa3fc0"
    assert prior["identity"]["superseded_by_v14_promotion_record_sha256"] == (
        "c7195d13f0579ff07da0cdfe98522dd64f4b4ffc3a86c67a91a19d7b61d1fd66"
    )


def test_historical_controls_remain_controls_not_promoted_champions():
    assert PRIOR_QUALIFIED_PREDECESSOR["role"] == "prior_qualified_predecessor"
    assert PRIOR_QUALIFIED_PREDECESSOR["promotion_proven"] is False
    assert PRIOR_QUALIFIED_PREDECESSOR["runtime_activation_proven"] is True

    assert PRIOR_ACCEPTED_MODEL_CONTROL["role"] == "prior_accepted_model_control"
    assert PRIOR_ACCEPTED_MODEL_CONTROL["promotion_proven"] is False
    assert PRIOR_ACCEPTED_MODEL_CONTROL["runtime_activation_proven"] is False


def test_reviewed_snapshot_set_is_four_way_and_campaign_qualified():
    snapshot_set = reviewed_snapshot_set()
    assert snapshot_set["schema"] == SNAPSHOT_SET_SCHEMA
    assert snapshot_set["snapshot_set_sha256"] == "d7bfce0cb1456ec440f6ab362c781057837c3912c557f865ae95b7ddc6278526"
    assert snapshot_set["snapshot_count"] == 4
    assert snapshot_set["source_identity_binding_complete"] is True
    assert snapshot_set["minimum_snapshot_count_met"] is True
    assert snapshot_set["current_promoted_snapshot_proven"] is True
    assert snapshot_set["previous_champion_proven"] is True
    assert snapshot_set["qualified_for_campaign_opponent_set"] is True
    assert snapshot_set["reasons"] == []
    assert snapshot_set["authority"]["runtime_execution_authorized"] is False
