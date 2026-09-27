from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_generation2
    as v1_wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_child_wiring_generation2
    as wiring,
)


def _kwargs() -> dict:
    return {
        "sock": object(),
        "attempt_id": "a" * 64,
        "runs_root": "/runs",
        "frozen_source_root": "/source",
        "exact_engine_root": "/engine",
        "policy_activation_authorized": True,
        "execution_authorized": True,
    }


def test_contract_binds_exact_v2_review_and_seals_consumed_lineage():
    out = wiring.pair06_v8_combat_priority_coherent_v2_proto_child_wiring_contract()

    assert out["repair_v2_review_main_head"] == (
        "ea0222f82189c7b55435742d78bb17169630e8f7"
    )
    assert out["repair_v2_review_git_blob"] == (
        "5e10ca44e614e37ff4f786e3ddff45ae7e0166d7"
    )
    assert out["repair_v2_review_source_sha256"] == (
        "d338be5a16fe809abcf412e06552f94fcb04cecb4ed99d337ae8c40e71f33e3c"
    )
    assert out["repair_v2_review_test_git_blob"] == (
        "e482b5d81f8ece9ba30604ef39e09c5db74333b6"
    )
    assert out["repair_v2_review_test_sha256"] == (
        "8f1db10374a4112123115683761c24941e21fb89b0e6293a231e7a66ab398714"
    )

    assert out["consumed_v2_precursor_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_v2_precursor_attempt_reusable"] is False
    assert out["consumed_v2_precursor_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260927T015002Z-feinter-s208354846"
    )
    assert out["consumed_v2_precursor_run_reusable_as_authority"] is False
    assert out["prior_authorization_reusable"] is False


def test_contract_binds_v2_legality_coherence():
    out = wiring.pair06_v8_combat_priority_coherent_v2_proto_child_wiring_contract()

    assert out["v2_repaired_decision_hook_bound"] is True
    assert out["production_functions_filtered_to_offered_surface_by_v1"] is True
    assert out["legal_buildings_reconstructed_from_remaining_production"] is True
    assert out["legal_units_reconstructed_from_remaining_production"] is True
    assert out["translator_legal_building_mapping_coherent"] is True
    assert out["translator_legal_unit_mapping_coherent"] is True


def test_v2_hook_class_extends_exact_v1_coherent_hook_class():
    assert issubclass(
        wiring.Pair06V8CombatPriorityCoherentV2ProtoChildHooks,
        wiring.ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS,
    )


def test_scoped_v2_hook_substitution_restores_on_success(monkeypatch):
    original = wiring.ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS
    seen = {}

    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(
        v1_wiring,
        "Pair06V8CombatPriorityCoherentProtoChildHooks",
        original,
    )

    def fake_run(**kwargs):
        seen["hook_class"] = (
            v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
        )
        seen["kwargs"] = kwargs
        return {"schema": "synthetic-v1-child-result"}

    monkeypatch.setattr(
        v1_wiring,
        "run_pair06_v8_combat_priority_coherent_proto_game_child",
        fake_run,
    )

    result = (
        wiring.run_pair06_v8_combat_priority_coherent_v2_proto_game_child(
            **_kwargs()
        )
    )

    assert result == {"schema": "synthetic-v1-child-result"}
    assert seen["hook_class"] is (
        wiring.Pair06V8CombatPriorityCoherentV2ProtoChildHooks
    )
    assert seen["kwargs"]["policy_activation_authorized"] is True
    assert seen["kwargs"]["execution_authorized"] is True
    assert (
        v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
        is original
    )


def test_scoped_v2_hook_substitution_restores_on_failure(monkeypatch):
    original = wiring.ORIGINAL_V1_COHERENT_PROTO_CHILD_HOOKS

    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(
        v1_wiring,
        "Pair06V8CombatPriorityCoherentProtoChildHooks",
        original,
    )

    def fail(**kwargs):
        assert (
            v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
            is wiring.Pair06V8CombatPriorityCoherentV2ProtoChildHooks
        )
        raise RuntimeError("synthetic V1 child failure")

    monkeypatch.setattr(
        v1_wiring,
        "run_pair06_v8_combat_priority_coherent_proto_game_child",
        fail,
    )

    with pytest.raises(RuntimeError, match="synthetic V1 child failure"):
        wiring.run_pair06_v8_combat_priority_coherent_v2_proto_game_child(
            **_kwargs()
        )

    assert (
        v1_wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
        is original
    )


def test_v2_child_wrapper_requires_both_authorities(monkeypatch):
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})

    values = _kwargs()
    values["policy_activation_authorized"] = False
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentV2ProtoChildWiringHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v8_combat_priority_coherent_v2_proto_game_child(
            **values
        )

    values = _kwargs()
    values["execution_authorized"] = False
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentV2ProtoChildWiringHold,
        match="CHILD_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v8_combat_priority_coherent_v2_proto_game_child(
            **values
        )


def test_contract_grants_no_retry_or_runtime_authority():
    out = wiring.pair06_v8_combat_priority_coherent_v2_proto_child_wiring_contract()

    for field in (
        "attempt_retry_authorized",
        "parent_supervisor_v2_wiring_implemented",
        "operator_invocation_v2_wiring_implemented",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_next_gate_is_source_binding_review():
    out = wiring.pair06_v8_combat_priority_coherent_v2_proto_child_wiring_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentV2ProtoChildWiringHold,
        match="REPAIR_V2_PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.wire_parent_or_execute()
