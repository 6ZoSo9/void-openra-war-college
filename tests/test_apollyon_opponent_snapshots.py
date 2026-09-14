from __future__ import annotations

from openra_env.learning.apollyon_opponent_snapshots import (
    CURRENT_PROMOTED,
    PRIOR_ACCEPTED_MODEL_CONTROL,
    PRIOR_QUALIFIED_PREDECESSOR,
    SNAPSHOT_SET_SCHEMA,
    reviewed_snapshot_set,
    snapshot_sha256,
)


def test_current_promoted_v10_identity_is_exactly_bound():
    current = CURRENT_PROMOTED
    assert current["role"] == "current_promoted"
    assert current["promotion_proven"] is True
    assert current["runtime_activation_proven"] is True
    assert (
        current["identity"]["candidate_sha256"]
        == "c351d98912dfe18ff8552da5e620b0e3ba6d9877dbc185c45be0dda0fd7d4025"
    )
    assert (
        current["identity"]["promotion_record_sha256"]
        == "5a5e857d253f986eae0bda5187638ca6547d874db840fb24ea30ec550306f444"
    )
    assert len(snapshot_sha256(current)) == 64


def test_v2r13_is_qualified_predecessor_not_claimed_champion():
    prior = PRIOR_QUALIFIED_PREDECESSOR
    assert prior["role"] == "prior_qualified_predecessor"
    assert prior["promotion_proven"] is False
    assert prior["runtime_activation_proven"] is True
    assert (
        prior["identity"]["model_digest"]
        == "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
    )


def test_v8_is_accepted_control_not_claimed_champion():
    v8 = PRIOR_ACCEPTED_MODEL_CONTROL
    assert v8["role"] == "prior_accepted_model_control"
    assert v8["promotion_proven"] is False
    assert v8["runtime_activation_proven"] is False
    assert (
        v8["identity"]["adapter_model_sha256"]
        == "ba792bd9472b0f9ee8e7acb5b40115a41c4def378fe74438b2f33d43b742b0e6"
    )


def test_reviewed_snapshot_set_is_bound_but_previous_champion_remains_open():
    snapshot_set = reviewed_snapshot_set()
    assert snapshot_set["schema"] == SNAPSHOT_SET_SCHEMA
    assert snapshot_set["snapshot_count"] == 3
    assert snapshot_set["source_identity_binding_complete"] is True
    assert snapshot_set["minimum_snapshot_count_met"] is True
    assert snapshot_set["current_promoted_snapshot_proven"] is True
    assert snapshot_set["previous_champion_proven"] is False
    assert snapshot_set["qualified_for_campaign_opponent_set"] is False
    assert snapshot_set["reasons"] == [
        "PREVIOUS_APOLLYON_CHAMPION_NOT_CRYPTOGRAPHICALLY_PROVEN"
    ]
    assert snapshot_set["authority"]["runtime_execution_authorized"] is False
