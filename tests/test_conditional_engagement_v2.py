from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.coaching.conditional_engagement_v2 import (
    CANDIDATE_SCHEMA,
    PolicyError,
    candidate_sha256,
    derive_candidate,
    format_coaching,
    select_mode,
    snapshot_from_state,
    validate_candidate,
)

MANIFEST_SHA = "d0802c23d31917a4ff295145b9192c9d0fc4b458087329bedf8ad50437635b0c"
REVIEW_SHA = "8cab03535e607fcf82a4e546f203cfb696249e591e706f4ce99583e182bc961a"
SOURCE_CANDIDATE_SHA = "71b427a80402c153f55c681b0b02a8608b57ec65d0d726d03a9547ce755ff8b6"
SOURCE_REVIEW_SHA = "47de83fa78556361bd595b94dfe5a1b3da1c0d63fea6916c35cb137e935e11ff"
EXPECTED_CANDIDATE_SHA = "27f28a6a46f63a055f8f35c021bafae1035084c444ba7e2009161109ec3efdd6"


def audit_review() -> dict:
    return {
        "schema": "void.apollyon.tactical-refinement-variance-audit-review.v1",
        "candidate_only": True,
        "classification": "SEED_CONDITIONAL_AGGRESSION_EFFECT_CONFIRMED",
        "recommendation": "REWORK_COACHING_BEFORE_ADMISSION",
        "next_step": "derive_conditional_engagement_candidate_v2",
        "generation_id": "ad1926569b12466c",
        "curriculum_id": "symmetric-contact-warm-start-v1",
        "doctrine": "RUSHER",
        "source_candidate_sha256": SOURCE_CANDIDATE_SHA,
        "source_review_sha256": SOURCE_REVIEW_SHA,
        "automatic_apollyon_weight_mutation": False,
        "automatic_abaddon_policy_promotion": False,
        "automatic_corpus_admission": False,
        "by_seed": {
            "2051": {
                "all_protocol_clean": True,
                "pair_count": 3,
                "better": 1,
                "worse": 2,
                "tie": 0,
                "median_net_delta": -200,
                "mean_net_delta": -100,
                "baseline_mean_attack_move_fraction": 0.7407407407407407,
                "refined_mean_attack_move_fraction": 0.861111111111111,
            },
            "2055": {
                "all_protocol_clean": True,
                "pair_count": 3,
                "better": 3,
                "worse": 0,
                "tie": 0,
                "median_net_delta": 600,
                "mean_net_delta": 600,
                "baseline_mean_attack_move_fraction": 0.0,
                "refined_mean_attack_move_fraction": 0.8981481481481481,
            },
        },
    }


def candidate() -> dict:
    return derive_candidate(
        audit_review(),
        manifest_sha256=MANIFEST_SHA,
        review_sha256=REVIEW_SHA,
    )


def snap(
    round_no: int,
    *,
    combat: int = 4,
    idle: int = 0,
    visible: int = 0,
    kills: int = 0,
    deaths: int = 0,
    tool: str | None = None,
) -> dict:
    return {
        "round": round_no,
        "combat_units": combat,
        "idle_combat_units": idle,
        "visible_enemies": visible,
        "kills_cost": kills,
        "deaths_cost": deaths,
        "selected_tool": tool,
    }


def test_derivation_binds_exact_audit_and_stays_candidate_only() -> None:
    result = candidate()
    assert result["schema"] == CANDIDATE_SCHEMA
    assert result["candidate_only"] is True
    assert result["source_evidence"]["variance_manifest_sha256"] == MANIFEST_SHA
    assert result["source_evidence"]["variance_review_sha256"] == REVIEW_SHA
    assert result["policy_boundaries"]["runtime_seed_branching"] is False
    assert result["policy_boundaries"]["unit_type_specific_rule"] is False
    assert result["automatic_apollyon_weight_mutation"] is False
    assert result["automatic_abaddon_policy_promotion"] is False
    assert result["automatic_corpus_admission"] is False
    assert candidate_sha256(result) == EXPECTED_CANDIDATE_SHA


def test_committed_fixture_matches_derivation() -> None:
    fixture = Path(__file__).parents[1] / "fixtures/training/conditional_engagement_candidate_v2.json"
    actual = json.loads(fixture.read_text(encoding="utf-8"))
    assert actual == candidate()
    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == EXPECTED_CANDIDATE_SHA


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("classification", "UNREVIEWED"),
        ("recommendation", "ADMIT"),
        ("next_step", "promote"),
        ("automatic_apollyon_weight_mutation", True),
        ("automatic_abaddon_policy_promotion", True),
        ("automatic_corpus_admission", True),
    ],
)
def test_derivation_rejects_evidence_or_authority_drift(field: str, value: object) -> None:
    review = audit_review()
    review[field] = value
    with pytest.raises(PolicyError):
        derive_candidate(review, manifest_sha256=MANIFEST_SHA, review_sha256=REVIEW_SHA)


def test_validation_rejects_runtime_seed_branching() -> None:
    result = candidate()
    result["policy_boundaries"]["runtime_seed_branching"] = True
    with pytest.raises(PolicyError):
        validate_candidate(result)


def test_snapshot_uses_observed_state_only() -> None:
    state = {
        "units_summary": [
            {"id": 1, "can_attack": True, "idle": True},
            {"id": 2, "can_attack": True, "idle": False},
            {"id": 3, "can_attack": False, "idle": True},
        ],
        "enemy_summary": [{"id": 10}],
        "enemy_buildings_summary": [{"id": 20}],
        "military": {"kills_cost": 400, "deaths_cost": 200},
    }
    assert snapshot_from_state(state, round_no=7, selected_tool="attack_target") == {
        "round": 7,
        "combat_units": 2,
        "idle_combat_units": 1,
        "visible_enemies": 2,
        "kills_cost": 400,
        "deaths_cost": 200,
        "selected_tool": "attack_target",
    }


def test_rebuild_force_precedes_other_modes() -> None:
    decision = select_mode(candidate(), snap(2, combat=1, visible=3), [snap(1, combat=4, tool="attack_move")])
    assert decision["mode"] == "REBUILD_FORCE"


def test_attrition_brake_on_losing_interval() -> None:
    decision = select_mode(
        candidate(),
        snap(2, combat=2, visible=2, kills=100, deaths=300),
        [snap(1, combat=4, visible=2, kills=0, deaths=0, tool="attack_move")],
    )
    assert decision["mode"] == "ATTRITION_BRAKE"
    assert "recent_deaths_cost_exceeds_kills_cost" in decision["reasons"]


def test_attrition_brake_on_saturated_attack_move_without_progress() -> None:
    history = [snap(i, tool="attack_move") for i in range(1, 6)]
    decision = select_mode(candidate(), snap(6), history)
    assert decision["mode"] == "ATTRITION_BRAKE"
    assert decision["evidence"]["attack_move_saturated"] is True


def test_contact_response_after_passive_choice() -> None:
    decision = select_mode(
        candidate(),
        snap(2, visible=2),
        [snap(1, visible=2, tool="train_unit_e1")],
    )
    assert decision["mode"] == "CONTACT_RESPONSE"


def test_measured_contact_when_already_engaging_cleanly() -> None:
    decision = select_mode(
        candidate(),
        snap(2, visible=2, kills=200),
        [snap(1, visible=2, kills=0, tool="attack_target")],
    )
    assert decision["mode"] == "MEASURED_CONTACT"


def test_engagement_deficit_after_passive_stagnation() -> None:
    history = [
        snap(1, tool="train_unit_e1"),
        snap(2, tool="build_structure_powr"),
    ]
    decision = select_mode(candidate(), snap(3), history)
    assert decision["mode"] == "ENGAGEMENT_DEFICIT"


def test_balanced_search_without_proven_emergency() -> None:
    decision = select_mode(candidate(), snap(1), [])
    assert decision["mode"] == "BALANCED_SEARCH"


def test_runtime_seed_metadata_cannot_change_decision() -> None:
    current_a = snap(3)
    current_b = copy.deepcopy(current_a)
    current_a["seed"] = 2051
    current_b["seed"] = 2055
    history = [snap(1, tool="train_unit_e1"), snap(2, tool="build_structure_powr")]
    assert select_mode(candidate(), current_a, history)["mode"] == select_mode(candidate(), current_b, history)["mode"]


def test_coaching_text_preserves_current_tool_and_hidden_state_boundary() -> None:
    decision = select_mode(candidate(), snap(1), [])
    text = format_coaching(decision)
    assert "CURRENT_ALLOWED_TOOL_NAMES" in text
    assert "do not infer hidden state" in text
    assert "MODE=BALANCED_SEARCH" in text
