from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as proto_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_generation2
    as v9_integration,
)


class _Legacy:
    def load_base(self):
        return None

    def apollyon_tools_typed(self, base, state, pending):
        return [], {
            "offered_tool_names": [],
            "production_functions": {},
            "legal_units": [],
            "legal_buildings": [],
        }

    def decision_to_commands_typed(
        self,
        base,
        name,
        args,
        state,
        pending,
        pb2,
        contract,
    ):
        return True, "accepted", []

    def apollyon_decision_typed(self, *args, **kwargs):
        return "original"


def test_contract_pins_exact_reviewed_dependencies():
    out = (
        wiring
        .pair06_v9_strict_visible_contact_proto_child_wiring_contract()
    )

    assert out["v9_integration_git_blob"] == (
        "8aa8a3bae62a914dfa1c1b7daf2fca6b13ecf2ef"
    )
    assert out["v9_integration_review_git_blob"] == (
        "9e92605527aeea59f9d99cfcb798adea569f7309"
    )
    assert out["proto_child_git_blob"] == (
        "7ea5d27c2d2bb499dfec4c00d2812d7ed043f8bc"
    )
    assert out["proto_child_review_git_blob"] == (
        "bd2d7d97a9ed9c04be3bddae5f64977265686fa5"
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["policy_id"] == (
        "pair06-v9-strict-visible-contact-envelope-v1"
    )


def test_specialized_hooks_replace_only_uninstalled_decision_hook():
    legacy = _Legacy()
    hooks = wiring.Pair06V9StrictVisibleContactProtoChildHooks(
        legacy,
        object(),
        "a" * 64,
    )

    assert hooks.v9_strict_visible_contact_decision_hook_bound is True
    assert isinstance(
        hooks._decision_hooks,
        v9_integration.Pair06V9StrictVisibleContactDecisionHooks,
    )
    assert hooks.legacy is legacy
    assert hooks.attempt_id == "a" * 64


def test_scoped_wrapper_requires_separate_v9_policy_activation_authority():
    original = proto_child.Pair06V8ProtoChildHooks

    with pytest.raises(
        wiring.Pair06V9StrictVisibleContactProtoChildWiringHold,
        match="V9_STRICT_VISIBLE_CONTACT_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v9_strict_visible_contact_proto_game_child(
            sock=object(),
            attempt_id="b" * 64,
            runs_root="/unused",
            frozen_source_root="/unused",
            exact_engine_root="/unused",
            policy_activation_authorized=False,
            execution_authorized=True,
        )

    assert proto_child.Pair06V8ProtoChildHooks is original


def test_scoped_wrapper_preserves_existing_child_execution_gate():
    original = proto_child.Pair06V8ProtoChildHooks

    with pytest.raises(
        wiring.Pair06V9StrictVisibleContactProtoChildWiringHold,
        match="CHILD_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v9_strict_visible_contact_proto_game_child(
            sock=object(),
            attempt_id="c" * 64,
            runs_root="/unused",
            frozen_source_root="/unused",
            exact_engine_root="/unused",
            policy_activation_authorized=True,
            execution_authorized=False,
        )

    assert proto_child.Pair06V8ProtoChildHooks is original


def test_scoped_wrapper_substitutes_factory_only_during_delegated_call(
    monkeypatch,
):
    observed = {}

    def fake_run(**kwargs):
        observed["factory"] = proto_child.Pair06V8ProtoChildHooks
        observed["kwargs"] = kwargs
        return {"fake_child_result": True}

    monkeypatch.setattr(
        proto_child,
        "run_pair06_v8_proto_game_child",
        fake_run,
    )

    original = wiring.ORIGINAL_PROTO_CHILD_HOOKS

    result = wiring.run_pair06_v9_strict_visible_contact_proto_game_child(
        sock=object(),
        attempt_id="d" * 64,
        runs_root="/runs",
        frozen_source_root="/source",
        exact_engine_root="/engine",
        policy_activation_authorized=True,
        execution_authorized=True,
    )

    assert result == {"fake_child_result": True}
    assert (
        observed["factory"]
        is wiring.Pair06V9StrictVisibleContactProtoChildHooks
    )
    assert observed["kwargs"]["execution_authorized"] is True
    assert proto_child.Pair06V8ProtoChildHooks is original


def test_scoped_wrapper_restores_factory_after_delegate_failure(monkeypatch):
    def fake_run(**kwargs):
        assert (
            proto_child.Pair06V8ProtoChildHooks
            is wiring.Pair06V9StrictVisibleContactProtoChildHooks
        )
        raise RuntimeError("synthetic child failure")

    monkeypatch.setattr(
        proto_child,
        "run_pair06_v8_proto_game_child",
        fake_run,
    )

    original = wiring.ORIGINAL_PROTO_CHILD_HOOKS

    with pytest.raises(RuntimeError, match="synthetic child failure"):
        wiring.run_pair06_v9_strict_visible_contact_proto_game_child(
            sock=object(),
            attempt_id="e" * 64,
            runs_root="/runs",
            frozen_source_root="/source",
            exact_engine_root="/engine",
            policy_activation_authorized=True,
            execution_authorized=True,
        )

    assert proto_child.Pair06V8ProtoChildHooks is original


def test_contract_preserves_existing_child_and_grants_no_authority():
    out = (
        wiring
        .pair06_v9_strict_visible_contact_proto_child_wiring_contract()
    )

    assert out["existing_proto_child_source_modified"] is False
    assert out["v9_proto_child_hook_subclass_implemented"] is True
    assert out["existing_proto_child_hook_factory_reused"] is True
    assert out["hook_factory_substitution_scoped_to_single_call"] is True
    assert out["hook_factory_restored_in_finally"] is True
    assert out["original_child_execution_authorization_gate_preserved"] is True
    assert out["additional_v9_policy_activation_gate_required"] is True
    assert out["reviewed_v9_decision_hook_used"] is True
    assert out["coherent_v9_tool_contract_path_preserved"] is True
    assert out["new_execution_request_opened"] is False
    assert out["attempt_created"] is False

    for field in (
        "parent_supervisor_wiring_implemented",
        "operator_entrypoint_wiring_implemented",
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
        "scheduler_mutation_authorized",
    ):
        assert out[field] is False


def test_wiring_advances_only_to_source_review():
    out = (
        wiring
        .pair06_v9_strict_visible_contact_proto_child_wiring_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V9StrictVisibleContactProtoChildWiringHold,
        match="PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.wire_parent_or_execute()
