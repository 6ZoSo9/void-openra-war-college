from __future__ import annotations

from openra_env.learning.abaddon_policy_campaign_plan import (
    precommitted_campaign_plan,
)
from openra_env.learning.apollyon_opponent_runtime_realizations import (
    V10,
    V2R13,
    V8,
    reviewed_opponent_runtime_realizations,
)


def test_v2r13_portable_frozen_checkout_binding_is_reviewed_and_source_bound():
    assert V2R13["historical_game_facing_runtime_proven"] is True
    assert V2R13["runtime_surface_realized"] is True
    assert V2R13["warm_start_input_surface_compatible"] is True
    assert V2R13["portable_current_checkout_binding_complete"] is True
    assert V2R13["current_campaign_runtime_realized"] is True
    assert V2R13["identity"]["legacy_warm_start_runner_sha256"] == (
        "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
    )
    assert V2R13["identity"]["portable_checkout_binding_source_sha256"] == (
        "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
    )
    assert V2R13["identity"]["portable_checkout_binding_contract_sha256"] == (
        "677e503e8d4827a9d8950a177f308ad08982f612d70881f16de2c271e3b10e49"
    )
    assert V2R13["identity"]["frozen_war_college_commit"] == (
        "973802ef0a614e5afa782ff20e231e18966ae3e5"
    )
    assert V2R13["identity"]["frozen_war_college_tree"] == (
        "d8a2af418af00e95ca0f203a2f0264851f2308c6"
    )
    assert V2R13["input_surface"]["portable_checkout_binding_reviewed"] is True
    assert V2R13["input_surface"]["source_materialization"] == "detached_git_worktree"
    assert V2R13["input_surface"]["canonical_checkout_mutation_required"] is False
    assert V2R13["input_surface"]["host_validation_unchanged"] is True
    assert V2R13["blockers"] == []


def test_v10_campaign_translation_is_reviewed_and_source_bound():
    assert V10["historical_game_facing_runtime_proven"] is True
    assert V10["runtime_surface_realized"] is True
    assert V10["portable_current_checkout_binding_complete"] is True
    assert V10["warm_start_input_surface_compatible"] is True
    assert V10["current_campaign_runtime_realized"] is True
    assert V10["input_surface"]["translation_required"] is True
    assert V10["input_surface"]["translation_reviewed"] is True
    assert V10["input_surface"]["output_translation_reviewed"] is True
    assert V10["input_surface"]["current_state_only"] is True
    assert V10["input_surface"]["current_tool_list_authoritative"] is True
    assert V10["input_surface"]["host_validation_unchanged"] is True
    assert V10["input_surface"]["fabricated_information_allowed"] is False
    assert V10["identity"]["campaign_translation_source_sha256"] == (
        "2d32351dff8d96a3254436305c2c402ea06c9a344b6b3ea67cb70c512eef2d53"
    )
    assert V10["identity"]["campaign_translation_contract_sha256"] == (
        "69c862387dad806681c5d066fea8e87836d2c0825f792ae293177c23cddee38b"
    )
    assert V10["identity"]["openai_bridge_v7_sha256"] == (
        "c197f3b75016dd7c4c25346f98aafdb1f631e2ee6e8b3514f9ebb650490b4510"
    )
    assert V10["blockers"] == []


def test_v8_has_no_frozen_war_college_tool_runtime():
    assert V8["historical_game_facing_runtime_proven"] is False
    assert V8["runtime_surface_realized"] is False
    assert V8["warm_start_input_surface_compatible"] is False
    assert V8["current_campaign_runtime_realized"] is False
    assert V8["input_surface"]["tool_transport_frozen"] is False
    assert V8["blockers"] == [
        "V8_WAR_COLLEGE_TOOL_RUNTIME_NOT_FROZEN"
    ]


def test_realization_set_is_exact_and_fail_closed():
    result = reviewed_opponent_runtime_realizations()
    assert result["realization_set_sha256"] == "1da6d280460fb1136dd1dbcb8d5ec47cf63a445378ff7112399d7aef3bbb5c0b"
    assert result["source_binding_complete"] is True
    assert result["historical_game_facing_runtime_count"] == 2
    assert result["runtime_surface_realized_count"] == 2
    assert result["current_campaign_runtime_realized_count"] == 2
    assert result["opponent_runtime_realization_complete"] is False
    assert result["blockers"] == [
        "V8_WAR_COLLEGE_TOOL_RUNTIME_NOT_FROZEN",
    ]
    assert result["authority"] == {
        "runtime_execution_authorized": False,
        "game_started": False,
        "model_execution_performed": False,
        "training": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
    }


def test_every_precommitted_opponent_has_exactly_one_realization_record():
    plan = precommitted_campaign_plan()
    expected = {
        row["opponent_snapshot_id"]
        for row in plan["pair_slots"]
    }
    result = reviewed_opponent_runtime_realizations()
    actual = {
        row["snapshot_id"]
        for row in result["realizations"]
    }
    assert actual == expected
