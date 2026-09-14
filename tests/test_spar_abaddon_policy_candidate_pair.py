from __future__ import annotations

import pytest

from openra_env.analysis.spar_abaddon_policy_candidate_pair import (
    PAIR_SCHEMA,
    PairContractError,
    compare_reports,
)

MARKER = "VOID_WAR_COLLEGE_SPAR_TRAINING_UTILITY_V1"


def side(*, net=0, combat=5, contact=True, damage=True, retries=None):
    return {
        "final_combat_capable_units": combat,
        "net_kill_cost": net,
        "retried_rounds": [] if retries is None else retries,
        "contact_rounds": [1] if contact else [],
        "first_damage_inflicted": {"round": 1} if damage else None,
    }


def evidence(*, present: bool):
    if not present:
        return {
            "present": False,
            "rounds_verified": 0,
            "host_accept_count": 0,
            "host_rejection_count": 0,
        }
    return {
        "present": True,
        "candidate_file_sha256": "1" * 64,
        "candidate_genome_sha256": "2" * 64,
        "wrapper_sha256": "3" * 64,
        "legacy_runner_sha256": "4" * 64,
        "abaddon_controller_sha256": "5" * 64,
        "abaddon_refiner_sha256": "6" * 64,
        "reviewed_wrapper_identity_verified": True,
        "all_round_receipts_verified": True,
        "host_acceptance_bound": True,
        "host_validation_unchanged": True,
        "training_use_approved": False,
        "training_performed": False,
        "weights_updated": False,
        "rounds_verified": 3,
        "host_accept_count": 3,
        "host_rejection_count": 0,
    }


def report(*, candidate=False, ab_net=0, ab_combat=5):
    trajectory = ("b" if candidate else "a") * 64
    return {
        "marker": MARKER,
        "version": 1,
        "provenance": {
            "curriculum_id": "symmetric-contact-warm-start-v1",
            "generation_id": "0123456789abcdef",
            "runtime_image_id": "sha256:" + "7" * 64,
            "engine_commit": "8" * 40,
            "war_college_commit": "9" * 40,
            "joint_training_attestation_sha256": "a" * 64,
            "warm_start_sha256": "b" * 64,
            "warm_start_handoff": {"tick": 100},
            "apollyon_model": "fixed-apollyon",
            "abaddon_controller_sha256": "5" * 64,
            "abaddon_doctrine": "RUSHER",
            "seed": 2050,
            "round_limit": 3,
            "ticks_per_round": 25,
            "trajectory_sha256": trajectory,
            "summary_sha256": ("d" if candidate else "c") * 64,
        },
        "integrity": {
            "trajectory_verified": True,
            "summary_verified": True,
            "rounds_completed": 3,
            "world_clock_contiguous": True,
            "perspective_accounting_consistent": True,
        },
        "sides": {
            "apollyon": side(net=-ab_net, combat=5),
            "abaddon": side(net=ab_net, combat=ab_combat),
        },
        "authority": {
            "candidate_only": True,
            "review_required": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
        "conditional_engagement_v2": {"present": False},
        "conditional_engagement_v2_1": {"present": False},
        "conditional_engagement_v2_2": {"present": False},
        "abaddon_policy_candidate_v1": evidence(present=candidate),
    }


def test_better_symmetric_candidate_is_review_candidate():
    pair = compare_reports(
        report(ab_net=0, ab_combat=5),
        report(candidate=True, ab_net=200, ab_combat=6),
    )
    assert pair["schema"] == PAIR_SCHEMA
    assert pair["comparison"]["verdict"] == "BETTER"
    assert pair["comparison"]["review_candidate_pass"] is True
    assert pair["authority"]["automatic_corpus_admission"] is False


@pytest.mark.parametrize("candidate_net", [0, -100])
def test_tie_or_worse_is_not_review_candidate(candidate_net):
    pair = compare_reports(
        report(ab_net=0),
        report(candidate=True, ab_net=candidate_net),
    )
    assert pair["comparison"]["review_candidate_pass"] is False


def test_host_rejection_blocks_review_candidate():
    candidate = report(candidate=True, ab_net=200, ab_combat=6)
    candidate["abaddon_policy_candidate_v1"]["host_rejection_count"] = 1
    candidate["abaddon_policy_candidate_v1"]["host_accept_count"] = 2
    pair = compare_reports(report(ab_net=0), candidate)
    assert pair["comparison"]["host_acceptance_pass"] is False
    assert pair["comparison"]["review_candidate_pass"] is False


def test_apollyon_candidate_evidence_in_candidate_arm_is_rejected():
    candidate = report(candidate=True, ab_net=200)
    candidate["conditional_engagement_v2_2"] = {"present": True}
    with pytest.raises(PairContractError, match="Apollyon candidate evidence"):
        compare_reports(report(), candidate)


def test_pair_identity_drift_is_rejected():
    candidate = report(candidate=True, ab_net=200)
    candidate["provenance"]["seed"] = 2051
    with pytest.raises(PairContractError, match="pair identity mismatch: seed"):
        compare_reports(report(), candidate)
