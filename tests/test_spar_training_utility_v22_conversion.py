from __future__ import annotations

from pathlib import Path

import pytest

from openra_env.analysis import spar_training_utility as utility
from openra_env.analysis._spar_contract import ContractError


TRAJECTORY_SHA = "a" * 64


def base_report() -> dict:
    return {"provenance": {"trajectory_sha256": TRAJECTORY_SHA}}


def absent() -> dict:
    return {"present": False, "rounds_verified": 0, "mode_counts": {}}


def v22_present() -> dict:
    return {
        "present": True,
        "candidate_sha256": "b" * 64,
        "rounds_verified": 72,
    }


def install_base(monkeypatch):
    monkeypatch.setattr(utility, "_analyze_trajectory_base", lambda *args, **kwargs: base_report())


def test_v22_trajectory_attaches_exact_conversion_utility(monkeypatch):
    install_base(monkeypatch)
    monkeypatch.setattr(utility, "validate_conditional_v2_evidence", lambda *args, **kwargs: absent())
    monkeypatch.setattr(utility, "validate_conditional_v21_evidence", lambda *args, **kwargs: absent())
    monkeypatch.setattr(utility, "validate_conditional_v22_evidence", lambda *args, **kwargs: v22_present())

    calls = []

    def conversion(path, *, expected_trajectory_sha256):
        calls.append((path, expected_trajectory_sha256))
        return {
            "schema": "void.apollyon.conditional-engagement-v2-2-conversion-utility.v1",
            "trajectory_sha256": expected_trajectory_sha256,
            "reviewed_identity_verified": True,
            "v2_2_candidate_sha256": "b" * 64,
            "rounds_verified": 72,
            "conversion_productivity_applicable": True,
            "post_conversion_productivity_pass": False,
        }

    monkeypatch.setattr(utility, "analyze_conversion_productivity", conversion)
    path = Path("/does/not/need/to/exist.jsonl")
    report = utility.analyze_trajectory(path)

    assert calls == [(path, TRAJECTORY_SHA)]
    attached = report["conditional_engagement_v2_2_conversion_utility"]
    assert attached["present"] is True
    assert attached["trajectory_sha256"] == TRAJECTORY_SHA
    assert attached["post_conversion_productivity_pass"] is False


def test_non_v22_trajectory_does_not_invoke_conversion_utility(monkeypatch):
    install_base(monkeypatch)
    monkeypatch.setattr(utility, "validate_conditional_v2_evidence", lambda *args, **kwargs: absent())
    monkeypatch.setattr(utility, "validate_conditional_v21_evidence", lambda *args, **kwargs: absent())
    monkeypatch.setattr(utility, "validate_conditional_v22_evidence", lambda *args, **kwargs: absent())

    def forbidden(*args, **kwargs):
        raise AssertionError("conversion utility must not run for non-V2.2 evidence")

    monkeypatch.setattr(utility, "analyze_conversion_productivity", forbidden)
    report = utility.analyze_trajectory(Path("unused.jsonl"))
    assert report["conditional_engagement_v2_2_conversion_utility"] == {"present": False}


def test_generation_mixing_fails_before_conversion_analysis(monkeypatch):
    install_base(monkeypatch)
    monkeypatch.setattr(utility, "validate_conditional_v2_evidence", lambda *args, **kwargs: {"present": True})
    monkeypatch.setattr(utility, "validate_conditional_v21_evidence", lambda *args, **kwargs: absent())
    monkeypatch.setattr(utility, "validate_conditional_v22_evidence", lambda *args, **kwargs: v22_present())

    def forbidden(*args, **kwargs):
        raise AssertionError("conversion utility must not run after generation-mixing failure")

    monkeypatch.setattr(utility, "analyze_conversion_productivity", forbidden)
    with pytest.raises(ContractError, match="multiple Conditional Engagement generations"):
        utility.analyze_trajectory(Path("unused.jsonl"))
