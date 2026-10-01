from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_game_child_entrypoint_generation2
    as entrypoint,
)


def _argv(
    *,
    confirm: str | None = None,
    policy_confirm: str | None = None,
    order_confirm: str | None = None,
) -> list[str]:
    return [
        "--fd",
        "3",
        "--attempt-id",
        "a" * 64,
        "--runs-root",
        "/runs",
        "--frozen-source-root",
        "/source",
        "--exact-engine-root",
        "/engine",
        "--confirm",
        entrypoint.CONFIRM_TOKEN if confirm is None else confirm,
        "--policy-confirm",
        entrypoint.POLICY_CONFIRM_TOKEN if policy_confirm is None else policy_confirm,
        "--order-confirm",
        entrypoint.ORDER_CONFIRM_TOKEN if order_confirm is None else order_confirm,
    ]


def test_contract_requires_three_distinct_confirmation_tokens():
    out = entrypoint.pair06_v9_input_order_coherence_child_entrypoint_contract()

    assert out["pair06_v9_input_order_coherence_child_entrypoint_implemented"] is True
    assert out["existing_execution_confirmation_token_required"] is True
    assert out["historical_v9_policy_activation_token_required"] is True
    assert out["separate_order_coherence_activation_token_required"] is True
    assert out["all_confirmation_tokens_distinct"] is True
    assert len(
        {
            entrypoint.CONFIRM_TOKEN,
            entrypoint.POLICY_CONFIRM_TOKEN,
            entrypoint.ORDER_CONFIRM_TOKEN,
        }
    ) == 3


@pytest.mark.parametrize(
    ("field", "value", "message"),
    (
        ("confirm", "wrong", "execution confirmation token required"),
        ("policy_confirm", "wrong", "strict-contact policy activation token required"),
        ("order_confirm", "wrong", "input-order coherence activation token required"),
    ),
)
def test_wrong_confirmation_token_holds_before_socket(field, value, message):
    kwargs = {field: value}
    with pytest.raises(
        entrypoint.Pair06V9InputOrderCoherenceChildEntrypointHold,
        match=message,
    ):
        entrypoint.main(_argv(**kwargs))


def test_contract_preserves_fail_closed_order_boundary():
    out = entrypoint.pair06_v9_input_order_coherence_child_entrypoint_contract()

    assert out["typed_tool_membership_exact_match_required"] is True
    assert out["typed_tool_order_canonicalized_to_offered_order"] is True
    assert out["membership_drift_still_fail_closed"] is True
    assert out["consumed_v9_attempt_retry_authorized"] is False


@pytest.mark.parametrize(
    "field",
    (
        "socketpair_created_by_entrypoint",
        "child_spawn_performed_by_entrypoint",
        "model_load_performed_by_entrypoint",
        "attempt_claim_created_by_entrypoint",
        "execution_request_created_by_entrypoint",
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
        "scheduler_mutation_authorized",
    ),
)
def test_contract_grants_no_execution_or_follow_on_authority(field):
    out = entrypoint.pair06_v9_input_order_coherence_child_entrypoint_contract()
    assert out[field] is False


def test_entrypoint_advances_only_to_parent_supervisor_wiring():
    out = entrypoint.pair06_v9_input_order_coherence_child_entrypoint_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
