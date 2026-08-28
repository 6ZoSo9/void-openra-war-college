from __future__ import annotations

import json
from pathlib import Path

import pytest

from openra_env.analysis import general_brain_challenger_pair as pair_mod
from openra_env.analysis.general_brain_challenger_campaign import build_challenger_campaign
from openra_env.learning.general_brain_generation import (
    make_challenger_generation,
    make_generation_zero,
    manifest_sha256,
    stable_json,
)
from openra_env.learning.general_brain_runtime import (
    BRAIN_RUN_SCHEMA,
    load_challenger_binding,
    tactical_overlay,
)
from openra_env.learning.general_brain_training import (
    ADAPTER_SCHEMA,
    ALGORITHM_ID,
    adapter_sha256,
)
from tools.conditional_engagement_v2_2_g1_duel_wrapper import GeneralBrainOverlayHooks


def adapter(parent):
    return {
        "schema": ADAPTER_SCHEMA,
        "general_id": "apollyon",
        "scope": "tactical_competence_only",
        "algorithm": ALGORITHM_ID,
        "parent_manifest_sha256": manifest_sha256(parent),
        "corpus_snapshot_sha256": "a" * 64,
        "record_count": 18,
        "weights": {"FORCE_CONVERSION": {"move_units": 4.5}},
        "authority_envelope_embedded": False,
        "tool_authorization_embedded": False,
        "promotion_authority_embedded": False,
    }


def manifests():
    parent = make_generation_zero("apollyon")
    adapted = adapter(parent)
    challenger = make_challenger_generation(
        parent,
        adapter_artifact_sha256=adapter_sha256(adapted),
        corpus_snapshot_sha256="a" * 64,
        training_receipt_sha256="b" * 64,
    )
    return parent, adapted, challenger


def test_runtime_binding_and_overlay_use_only_tactical_weights(tmp_path):
    parent, adapted, challenger = manifests()
    adapter_path = tmp_path / "adapter.json"
    challenger_path = tmp_path / "challenger.json"
    adapter_path.write_text(stable_json(adapted) + "\n", encoding="utf-8")
    challenger_path.write_text(stable_json(challenger) + "\n", encoding="utf-8")

    binding = load_challenger_binding(
        adapter_path=adapter_path,
        challenger_manifest_path=challenger_path,
        expected_adapter_sha256=adapter_sha256(adapted),
        expected_challenger_file_sha256=manifest_sha256(challenger),
    )
    overlay = tactical_overlay(
        binding,
        mode="FORCE_CONVERSION",
        offered_tool_names=["attack_move", "move_units", "train_unit_e1"],
    )
    assert overlay["preferred_tool"] == "move_units"
    assert overlay["preferred_score"] == 4.5
    assert overlay["preferred_arguments"] == {"unit_ids": "all_combat"}
    assert overlay["tool_surface_unchanged"] is True
    assert overlay["authority_envelope_trainable"] is False
    assert overlay["tool_authorization_trainable"] is False
    assert "AUTHORITY_ENVELOPE_TRAINABLE=false" in overlay["coaching"]


def test_runtime_overlay_never_invents_unoffered_tool():
    _, adapted, _ = manifests()
    binding = {
        "schema": BRAIN_RUN_SCHEMA,
        "adapter": adapted,
        "adapter_sha256": adapter_sha256(adapted),
        "challenger_manifest_sha256": "c" * 64,
    }
    overlay = tactical_overlay(
        binding,
        mode="FORCE_CONVERSION",
        offered_tool_names=["attack_move", "train_unit_e1"],
    )
    assert overlay["preferred_tool"] is None
    assert overlay["preference_applied"] is False
    assert overlay["preferred_arguments"] == {}


class FakeHelper:
    def __init__(self):
        self.users = []

    def ollama_tool_call(self, system, user, tools):
        self.users.append(user)
        return {"ok": True}


class FakeSession:
    def prepare_round(self, state, *, round_no, allowed_tool_names):
        assert allowed_tool_names == ["attack_move", "move_units"]
        return {"decision": {"mode": "FORCE_CONVERSION"}}

    def commit_accepted_tool(self, selected_tool):
        return {"mode": "FORCE_CONVERSION", "selected_tool": selected_tool}


class FakeLegacy:
    def __init__(self):
        self.rows = []
        self.apollyon_decision_typed = self._decision
        self.append_jsonl = self._append

    def apollyon_tools_typed(self, base, state, pending):
        return None, {"offered_tool_names": ["attack_move", "move_units"]}

    def _decision(self, base, helper, state, pending, pb2, doctrine, round_no):
        helper.ollama_tool_call("system", "BASE_USER", [])
        return (
            "move_units",
            {"unit_ids": "all_combat"},
            [],
            [{"tool": "move_units", "accepted": True, "world_mutated_before_validation": False}],
            {"offered_tool_names": ["attack_move", "move_units"]},
        )

    def _append(self, path, row):
        self.rows.append(row)


def test_outer_hook_adds_weights_without_filtering_tools():
    _, adapted, _ = manifests()
    binding = {
        "schema": BRAIN_RUN_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "adapter": adapted,
        "adapter_sha256": adapter_sha256(adapted),
        "adapter_file_sha256": adapter_sha256(adapted),
        "challenger_manifest_sha256": "c" * 64,
        "challenger_manifest_file_sha256": "c" * 64,
    }
    legacy = FakeLegacy()
    helper = FakeHelper()
    hooks = GeneralBrainOverlayHooks(legacy, FakeSession(), binding)
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(None, helper, {}, None, None, "RUSHER", 1)
        assert result[0] == "move_units"
        assert "LEARNED_PREFERRED_TOOL=move_units" in helper.users[0]
        assert "LEARNED_PREFERRED_ARGUMENTS=unit_ids=\"all_combat\"" in helper.users[0]
        legacy.append_jsonl(Path("unused"), {"event": "run_header"})
        legacy.append_jsonl(Path("unused"), {"event": "joint_decision", "round": 1})
    finally:
        hooks.restore()
    assert legacy.rows[0]["general_brain_generation_1"]["automatic_promotion"] is False
    round_evidence = legacy.rows[1]["general_brain_generation_1"]
    assert round_evidence["selected_preferred_tool"] is True
    assert round_evidence["selected_arguments"] == {"unit_ids": "all_combat"}


def report(*, trajectory, warm, net, combat, attack_move=10, retries=None, post=True):
    retries = [] if retries is None else list(retries)
    return {
        "provenance": {
            "curriculum_id": "curriculum",
            "generation_id": "0123456789abcdef",
            "runtime_image_id": "sha256:" + "1" * 64,
            "engine_commit": "2" * 40,
            "war_college_commit": "3" * 40,
            "joint_training_attestation_sha256": "4" * 64,
            "warm_start_sha256": warm,
            "apollyon_model": "model",
            "abaddon_controller_sha256": "5" * 64,
            "abaddon_doctrine": "RUSHER",
            "seed": 2051,
            "round_limit": 72,
            "ticks_per_round": 25,
            "trajectory_sha256": trajectory,
            "summary_sha256": "6" * 64,
        },
        "integrity": {
            "trajectory_verified": True,
            "summary_verified": True,
            "world_clock_contiguous": True,
            "perspective_accounting_consistent": True,
            "rounds_completed": 72,
        },
        "authority": {
            "candidate_only": True,
            "review_required": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
        "sides": {
            "apollyon": {
                "net_kill_cost": net,
                "final_combat_capable_units": combat,
                "tools": {"attack_move": attack_move},
                "retried_rounds": retries,
                "contact_rounds": [1],
                "first_damage_inflicted": {"round": 1},
            },
            "abaddon": {
                "net_kill_cost": -net,
                "final_combat_capable_units": 5,
                "tools": {},
                "retried_rounds": [],
                "contact_rounds": [1],
                "first_damage_inflicted": {"round": 1},
            },
        },
        "conditional_engagement_v2_2": {
            "present": True,
            "reviewed_identity_verified": True,
            "all_round_receipts_verified": True,
            "tool_surface_bound": True,
            "accepted_tool_bound": True,
            "runtime_seed_branching": False,
        },
        "conditional_engagement_v2_2_conversion_utility": {
            "present": True,
            "post_conversion_productivity_pass": post,
        },
    }


def test_pair_compares_clean_challenger_and_binds_manifest(monkeypatch, tmp_path):
    parent, _, challenger = manifests()
    incumbent_report = report(trajectory="7" * 64, warm="8" * 64, net=0, combat=4)
    challenger_report = report(trajectory="9" * 64, warm="a" * 64, net=200, combat=6, attack_move=20)

    def fake_warm(path):
        raw = "8" * 64 if "inc" in path.name else "a" * 64
        return {"raw_sha256": raw, "normalized_sha256": "b" * 64}

    monkeypatch.setattr(pair_mod, "warm_start_identity", fake_warm)

    def fake_brain(path, *, expected_trajectory_sha256):
        if "inc" in path.name:
            return {"present": False, "rounds_verified": 0}
        return {
            "present": True,
            "all_round_receipts_verified": True,
            "reviewed_v2_2_identity_verified": True,
            "challenger_manifest_sha256": manifest_sha256(challenger),
            "adapter_sha256": challenger["competence_adapter"]["artifact_sha256"],
            "preference_follow_fraction": 1.0,
        }

    monkeypatch.setattr(pair_mod, "validate_general_brain_g1_evidence", fake_brain)
    out = pair_mod.compare_incumbent_challenger(
        incumbent_report,
        challenger_report,
        incumbent_trajectory_path=tmp_path / "inc.jsonl",
        challenger_trajectory_path=tmp_path / "chal.jsonl",
        incumbent_warm_start_path=tmp_path / "inc-warm.jsonl",
        challenger_warm_start_path=tmp_path / "chal-warm.jsonl",
        incumbent_manifest=parent,
        challenger_manifest=challenger,
    )
    assert out["comparison"]["verdict"] == "BETTER"
    assert out["comparison"]["behavioral_gates_pass"] is True
    assert out["comparison"]["protocol_clean"] is True
    assert out["automatic_promotion"] is False


def campaign_pair(seed, ordinal, parent, challenger, *, delta=100.0, clean=True, behavior=True):
    suffix = f"{seed}{ordinal}".encode().hex().ljust(64, "0")[:64]
    challenger_suffix = f"c{seed}{ordinal}".encode().hex().ljust(64, "1")[:64]
    return {
        "schema": pair_mod.PAIR_SCHEMA,
        "general_id": "apollyon",
        "incumbent_manifest_sha256": manifest_sha256(parent),
        "challenger_manifest_sha256": manifest_sha256(challenger),
        "adapter_sha256": challenger["competence_adapter"]["artifact_sha256"],
        "pair_identity": {"seed": seed},
        "incumbent": {"trajectory_sha256": suffix},
        "challenger": {"trajectory_sha256": challenger_suffix},
        "comparison": {
            "net_kill_cost_delta": delta,
            "protocol_clean": clean,
            "behavioral_gates_pass": behavior,
        },
    }


def test_campaign_requires_fifteen_unique_pairs_and_never_auto_promotes():
    parent, _, challenger = manifests()
    rows = [
        campaign_pair(seed, ordinal, parent, challenger)
        for seed in (2051, 2055, 2052, 2053, 2054)
        for ordinal in (1, 2, 3)
    ]
    out = build_challenger_campaign(rows, incumbent_manifest=parent, challenger_manifest=challenger)
    assert out["status"] == "PASS"
    assert out["observed_pair_count"] == 15
    assert out["promotion_decision"]["eligible_for_promotion"] is True
    assert out["promotion_decision"]["automatic_promotion"] is False
    assert out["review_required"] is True


def test_campaign_rejects_completed_regression_seed():
    parent, _, challenger = manifests()
    rows = [
        campaign_pair(2051, ordinal, parent, challenger, delta=-100.0)
        for ordinal in (1, 2, 3)
    ]
    out = build_challenger_campaign(rows, incumbent_manifest=parent, challenger_manifest=challenger)
    assert out["status"] == "REJECT"
    assert out["promotion_decision"]["eligible_for_promotion"] is False


def test_campaign_rejects_duplicate_incumbent_evidence():
    parent, _, challenger = manifests()
    first = campaign_pair(2051, 1, parent, challenger)
    second = campaign_pair(2051, 2, parent, challenger)
    second["incumbent"]["trajectory_sha256"] = first["incumbent"]["trajectory_sha256"]
    with pytest.raises(Exception, match="duplicate incumbent"):
        build_challenger_campaign([first, second], incumbent_manifest=parent, challenger_manifest=challenger)
