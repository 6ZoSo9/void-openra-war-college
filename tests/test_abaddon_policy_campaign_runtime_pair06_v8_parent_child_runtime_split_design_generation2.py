from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_runtime_split_design_generation2
    as design,
)


def test_design_preserves_exact_two_venv_boundary():
    out = design.pair06_v8_parent_child_runtime_split_design_contract()
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["v8_parent_python"].endswith("/venv/bin/python3.12")
    assert out["game_child_python"].endswith("/venv/bin/python")
    assert out["separate_virtualenv_site_packages_preserved"] is True
    assert out["package_install_into_v8_required"] is False
    assert out["cross_venv_site_packages_injection_required"] is False


def test_design_assigns_model_and_game_ownership_to_correct_processes():
    out = design.pair06_v8_parent_child_runtime_split_design_contract()
    assert out["v8_parent_owns_model_load"] is True
    assert out["v8_parent_owns_model_inference"] is True
    assert out["v8_parent_owns_authority_check_before_load"] is True
    assert out["v8_parent_owns_authority_check_before_each_inference"] is True
    assert out["game_child_owns_grpc_proto"] is True
    assert out["game_child_owns_openra"] is True
    assert out["game_child_owns_legacy_runner"] is True
    assert out["game_child_must_not_load_model"] is True
    assert out["game_child_must_not_call_legacy_ollama"] is True


def test_design_uses_inherited_socketpair_and_bounded_protocol():
    out = design.pair06_v8_parent_child_runtime_split_design_contract()
    assert out["transport"] == "inherited_unix_socketpair"
    assert out["socketpair_inherited_fd_only"] is True
    assert out["filesystem_socket_path_created"] is False
    assert out["listening_network_socket_created"] is False
    assert out["framing"] == "uint32_be_length_plus_utf8_canonical_json"
    assert out["max_message_bytes"] == 4 * 1024 * 1024
    assert out["parent_to_child_message_types"] == (
        "HELLO",
        "DECIDE_RESPONSE",
        "ABORT",
    )
    assert out["child_to_parent_message_types"] == (
        "READY",
        "DECIDE_REQUEST",
        "GAME_RESULT",
        "ERROR",
    )
    assert out["terminal_child_message_types"] == ("GAME_RESULT", "ERROR")
    assert out["protocol_sequence_numbers_required"] is True
    assert out["canonical_json_required"] is True
    assert out["unknown_message_type_rejected"] is True
    assert out["unknown_message_fields_rejected"] is True


def test_design_requires_parent_process_group_containment_and_single_claim():
    out = design.pair06_v8_parent_child_runtime_split_design_contract()
    assert out["child_private_process_group_required"] is True
    assert out["parent_owns_child_process_group_retirement"] is True
    assert out["term_then_kill_escalation_required"] is True
    assert out["child_natural_zero_exit_required_for_clean_terminal"] is True
    assert out["create_only_game_attempt_claim_before_load_or_spawn"] is True
    assert out["single_authorization_covers_parent_and_child"] is True
    assert out["automatic_retry"] is False


def test_design_grants_no_execution_authority():
    out = design.pair06_v8_parent_child_runtime_split_design_contract()
    for field in (
        "parent_runtime_load_authorized",
        "parent_model_inference_authorized",
        "child_game_execution_authorized",
        "subprocess_spawn_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_design_advances_only_to_separate_source_review():
    out = design.pair06_v8_parent_child_runtime_split_design_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        design.Pair06V8ParentChildRuntimeSplitDesignHold,
        match="PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        design.execute_or_spawn()
