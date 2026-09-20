from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_repair_canary_source_design_v1 as source_design


def test_seed_derivation_is_fixed_fresh_and_shared_by_both_arms():
    out = source_design.scout_repair_canary_source_design()
    seed = out["seed_derivation"]["seed"]
    assert seed == 1100292357
    assert seed != source_design.PAIR03_SEED
    assert seed not in source_design.GENERATION2_CAMPAIGN_SEEDS
    assert out["seed_derivation"]["full_material_sha256"] == "c1952102e7f9586dd453bdf78bd77cc10a9927a2751fc4c4b8a7e1049c42dc7a"
    assert out["arm_seed_binding"] == {
        "legacy_control": seed,
        "scout_repair_treatment": seed,
        "same_seed": True,
    }


def test_canary_does_not_claim_generation2_or_held_out_slot():
    out = source_design.scout_repair_canary_source_design()
    assert out["experiment_namespace"] == "abaddon-scout-repair-canary-v1"
    assert out["campaign_pair_slot"] is None
    assert out["held_out_campaign_space_used"] is False


def test_opponent_and_runtime_inputs_remain_unresolved():
    out = source_design.scout_repair_canary_source_design()
    assert out["opponent"] == {
        "source_identity": None,
        "implementation": None,
        "model_backed": False,
        "deterministic_required": True,
        "same_for_both_arms": True,
    }
    for field in (
        "accepted_main_head_with_repair", "runtime_image_identity", "attempt_directory",
        "attempt_guard_source_identity", "invocation_source_identities", "post_run_evidence_contract",
    ):
        assert out[field] is None


def test_no_authority_or_retry_is_created():
    out = source_design.scout_repair_canary_source_design()
    for field in (
        "execution_authorized", "execution_performed", "automatic_retry",
        "training_authorized", "automatic_policy_promotion_authorized",
    ):
        assert out[field] is False
    assert out["next_gate"] == source_design.NEXT_GATE


def test_public_result_recomputes_identically():
    assert source_design.scout_repair_canary_source_design() == source_design.scout_repair_canary_source_design()


def test_execution_entrypoint_always_holds():
    for kwargs in ({}, {"authorized": True}, {"seed": 1100292357}, {"confirm": "yes"}):
        with pytest.raises(source_design.ScoutRepairCanarySourceDesignHold, match=source_design.NEXT_GATE):
            source_design.authorize_or_execute_canary(**kwargs)


def test_source_only_import_surface():
    tree = ast.parse(Path(source_design.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "hashlib", "typing", "openra_env.learning"}
