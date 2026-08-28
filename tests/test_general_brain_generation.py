from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from openra_env.learning.general_brain_generation import (
    BRAIN_MANIFEST_SCHEMA,
    NONTRAINABLE_AUTHORITY_ENVELOPE,
    TRAINING_ELIGIBILITY_SCHEMA,
    GeneralBrainContractError,
    classify_abaddon_from_apollyon_v22_pair,
    classify_apollyon_v22_pair_for_training,
    make_challenger_generation,
    make_generation_zero,
    validate_brain_manifest,
)


def reviewed_pair() -> dict:
    return {
        "schema": "void.apollyon.conditional-engagement-v2-2-pair-comparison.v2",
        "candidate_only": True,
        "warm_start_binding": {"semantic_match": True},
        "candidate": {
            "reviewed_identity_verified": True,
            "trajectory_sha256": "a" * 64,
        },
        "comparison": {
            "verdict": "BETTER",
            "protocol_clean": True,
            "force_preservation_pass": True,
            "productive_contact_pass": True,
            "attack_move_reduction_pass": True,
        },
    }


def test_generation_zero_fixtures_are_exact_contracts():
    root = Path(__file__).parents[1] / "fixtures" / "learning"
    for general_id in ("apollyon", "abaddon"):
        fixture = json.loads((root / f"{general_id}-brain-generation-0.json").read_text(encoding="utf-8"))
        assert fixture == make_generation_zero(general_id)
        validate_brain_manifest(fixture)
        assert fixture["schema"] == BRAIN_MANIFEST_SCHEMA
        assert fixture["competence_adapter"]["state"] == "untrained"
        assert fixture["authority_envelope"] == NONTRAINABLE_AUTHORITY_ENVELOPE


def test_only_clear_reviewed_apollyon_improvement_is_training_eligible():
    result = classify_apollyon_v22_pair_for_training(reviewed_pair())
    assert result["schema"] == TRAINING_ELIGIBILITY_SCHEMA
    assert result["general_id"] == "apollyon"
    assert result["eligible"] is True
    assert result["training_role"] == "positive_tactical_example"
    assert result["candidate_trajectory_sha256"] == "a" * 64
    assert result["reasons"] == []
    assert result["authority_envelope_trainable"] is False
    assert result["automatic_corpus_admission"] is False
    assert result["automatic_weight_mutation"] is False
    assert result["automatic_promotion"] is False


def test_seed_2051_style_regression_and_retry_is_diagnostic_only():
    pair = reviewed_pair()
    pair["comparison"]["verdict"] = "WORSE"
    pair["comparison"]["protocol_clean"] = False
    pair["comparison"]["productive_contact_pass"] = False
    result = classify_apollyon_v22_pair_for_training(pair)
    assert result["eligible"] is False
    assert result["candidate_trajectory_sha256"] is None
    assert set(result["reasons"]) >= {
        "PRIMARY_METRIC_NOT_BETTER",
        "PROTOCOL_NOT_CLEAN",
        "PRODUCTIVE_CONTACT_FAILED",
    }


def test_seed_2055_style_behavioral_failure_is_diagnostic_only():
    pair = reviewed_pair()
    pair["comparison"]["attack_move_reduction_pass"] = False
    result = classify_apollyon_v22_pair_for_training(pair)
    assert result["eligible"] is False
    assert result["reasons"] == ["ATTACK_MOVE_BEHAVIOR_GATE_FAILED"]


def test_tie_is_not_positive_training_data():
    pair = reviewed_pair()
    pair["comparison"]["verdict"] = "TIE"
    result = classify_apollyon_v22_pair_for_training(pair)
    assert result["eligible"] is False
    assert "PRIMARY_METRIC_NOT_BETTER" in result["reasons"]


def test_unreviewed_or_unbound_evidence_cannot_enter_corpus():
    pair = reviewed_pair()
    pair["candidate"]["reviewed_identity_verified"] = False
    pair["warm_start_binding"]["semantic_match"] = False
    result = classify_apollyon_v22_pair_for_training(pair)
    assert result["eligible"] is False
    assert set(result["reasons"]) >= {
        "CANDIDATE_IDENTITY_NOT_REVIEWED",
        "WARM_START_NOT_SEMANTICALLY_BOUND",
    }


def test_abaddon_requires_its_own_symmetric_challenger_evidence():
    result = classify_abaddon_from_apollyon_v22_pair(reviewed_pair())
    assert result["general_id"] == "abaddon"
    assert result["eligible"] is False
    assert result["reasons"] == ["ABADDON_REQUIRES_SYMMETRIC_REVIEWED_CHALLENGER_EVIDENCE"]


def test_challenger_changes_competence_generation_but_not_authority():
    parent = make_generation_zero("apollyon")
    challenger = make_challenger_generation(
        parent,
        adapter_artifact_sha256="b" * 64,
        corpus_snapshot_sha256="c" * 64,
        training_receipt_sha256="d" * 64,
    )
    assert challenger["generation"] == 1
    assert challenger["competence_adapter"] == {
        "trainable": True,
        "scope": "tactical_competence_only",
        "state": "challenger",
        "artifact_sha256": "b" * 64,
    }
    assert challenger["authority_envelope"] == parent["authority_envelope"]
    assert challenger["authority_envelope"] == NONTRAINABLE_AUTHORITY_ENVELOPE
    assert challenger["learning"] == parent["learning"]
    assert challenger["training_lineage"]["corpus_snapshot_sha256"] == "c" * 64
    assert challenger["training_lineage"]["training_receipt_sha256"] == "d" * 64
    validate_brain_manifest(challenger)


def test_authority_envelope_cannot_become_trainable():
    manifest = make_generation_zero("apollyon")
    tampered = copy.deepcopy(manifest)
    tampered["authority_envelope"]["role_hierarchy_trainable"] = True
    with pytest.raises(GeneralBrainContractError, match="authority envelope drift"):
        validate_brain_manifest(tampered)


def test_general_cannot_gain_automatic_self_promotion():
    manifest = make_generation_zero("abaddon")
    tampered = copy.deepcopy(manifest)
    tampered["learning"]["automatic_promotion"] = True
    with pytest.raises(GeneralBrainContractError, match="automatic promotion forbidden"):
        validate_brain_manifest(tampered)
