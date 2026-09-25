from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_game_child_entrypoint_generation2
    as entrypoint,
)


def _argv(*, confirm: str, policy_confirm: str) -> list[str]:
    return [
        "--fd",
        "9",
        "--attempt-id",
        "a" * 64,
        "--runs-root",
        "/runs",
        "--frozen-source-root",
        "/source",
        "--exact-engine-root",
        "/engine",
        "--confirm",
        confirm,
        "--policy-confirm",
        policy_confirm,
    ]


def test_contract_requires_two_distinct_confirmation_tokens():
    out = entrypoint.pair06_v8_combat_priority_proto_child_entrypoint_contract()
    assert out[
        "pair06_v8_combat_priority_proto_child_entrypoint_implemented"
    ] is True
    assert out["existing_execution_confirmation_token_required"] is True
    assert out["separate_policy_activation_token_required"] is True
    assert out[
        "policy_activation_token_distinct_from_execution_token"
    ] is True
    assert entrypoint.POLICY_CONFIRM_TOKEN != entrypoint.CONFIRM_TOKEN


def test_wrong_execution_token_holds_before_socket_creation():
    with pytest.raises(
        entrypoint.Pair06V8CombatPriorityChildEntrypointHold,
        match="execution confirmation token required",
    ):
        entrypoint.main(
            _argv(
                confirm="WRONG",
                policy_confirm=entrypoint.POLICY_CONFIRM_TOKEN,
            )
        )


def test_wrong_policy_token_holds_before_socket_creation():
    with pytest.raises(
        entrypoint.Pair06V8CombatPriorityChildEntrypointHold,
        match="policy activation token required",
    ):
        entrypoint.main(
            _argv(
                confirm=entrypoint.CONFIRM_TOKEN,
                policy_confirm="WRONG",
            )
        )


def test_contract_grants_no_runtime_or_training_authority():
    out = entrypoint.pair06_v8_combat_priority_proto_child_entrypoint_contract()
    for field in (
        "execution_performed_by_contract_inspection",
        "runtime_activation_authorized_by_contract_inspection",
        "automatic_retry",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
