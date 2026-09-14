from __future__ import annotations

from pathlib import Path

import pytest

import openra_env.analysis.spar_training_utility as utility
from openra_env.analysis._spar_contract import ContractError


def base_report():
    return {"provenance": {"trajectory_sha256": "a" * 64}}


def test_training_utility_exposes_abaddon_candidate_report(monkeypatch):
    monkeypatch.setattr(
        utility,
        "_analyze_trajectory_base",
        lambda *args, **kwargs: base_report(),
    )
    monkeypatch.setattr(
        utility,
        "validate_conditional_v2_evidence",
        lambda *args, **kwargs: {"present": False},
    )
    monkeypatch.setattr(
        utility,
        "validate_conditional_v21_evidence",
        lambda *args, **kwargs: {"present": False},
    )
    monkeypatch.setattr(
        utility,
        "validate_conditional_v22_evidence",
        lambda *args, **kwargs: {"present": False},
    )
    monkeypatch.setattr(
        utility,
        "validate_abaddon_policy_candidate_evidence",
        lambda *args, **kwargs: {"present": True, "rounds_verified": 3},
    )

    report = utility.analyze_trajectory(Path("unused"))
    assert report["abaddon_policy_candidate_v1"]["present"] is True


def test_training_utility_rejects_simultaneous_apollyon_and_abaddon_candidates(
    monkeypatch,
):
    monkeypatch.setattr(
        utility,
        "_analyze_trajectory_base",
        lambda *args, **kwargs: base_report(),
    )
    monkeypatch.setattr(
        utility,
        "validate_conditional_v2_evidence",
        lambda *args, **kwargs: {"present": True},
    )
    monkeypatch.setattr(
        utility,
        "validate_conditional_v21_evidence",
        lambda *args, **kwargs: {"present": False},
    )
    monkeypatch.setattr(
        utility,
        "validate_conditional_v22_evidence",
        lambda *args, **kwargs: {"present": False},
    )
    monkeypatch.setattr(
        utility,
        "validate_abaddon_policy_candidate_evidence",
        lambda *args, **kwargs: {"present": True},
    )

    with pytest.raises(ContractError, match="simultaneous Apollyon and Abaddon"):
        utility.analyze_trajectory(Path("unused"))
