from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_game_child_entrypoint_generation2
    as entrypoint,
)


def _argv(*, confirm: str, policy_confirm: str) -> list[str]:
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
        confirm,
        "--policy-confirm",
        policy_confirm,
    ]


def test_contract_preserves_distinct_execution_and_v9_policy_tokens():
    out = entrypoint.pair06_v9_strict_visible_contact_child_entrypoint_contract()

    assert out[
        "pair06_v9_strict_visible_contact_child_entrypoint_implemented"
    ] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["existing_execution_confirmation_token_required"] is True
    assert out["separate_v9_policy_activation_token_required"] is True
    assert out["execution_and_policy_confirmation_tokens_distinct"] is True
    assert entrypoint.CONFIRM_TOKEN != entrypoint.POLICY_CONFIRM_TOKEN


def test_wrong_execution_token_holds_before_socket_or_execution():
    with pytest.raises(
        entrypoint.Pair06V9StrictVisibleContactChildEntrypointHold,
        match="execution confirmation token required",
    ):
        entrypoint.main(
            _argv(
                confirm="wrong",
                policy_confirm=entrypoint.POLICY_CONFIRM_TOKEN,
            )
        )


def test_wrong_policy_token_holds_before_socket_or_execution():
    with pytest.raises(
        entrypoint.Pair06V9StrictVisibleContactChildEntrypointHold,
        match="V9 strict-contact policy activation token required",
    ):
        entrypoint.main(
            _argv(
                confirm=entrypoint.CONFIRM_TOKEN,
                policy_confirm="wrong",
            )
        )


def test_contract_creates_no_attempt_or_execution_request():
    out = entrypoint.pair06_v9_strict_visible_contact_child_entrypoint_contract()

    assert out["attempt_claim_created_by_entrypoint"] is False
    assert out["execution_request_created_by_entrypoint"] is False
    assert out["execution_performed_by_contract_inspection"] is False
    assert out["runtime_activation_authorized_by_contract_inspection"] is False
    assert out["automatic_retry"] is False


@pytest.mark.parametrize(
    "field",
    (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_contract_grants_no_follow_on_authority(field):
    out = entrypoint.pair06_v9_strict_visible_contact_child_entrypoint_contract()
    assert out[field] is False


def test_entrypoint_advances_only_to_parent_supervisor_wiring():
    out = entrypoint.pair06_v9_strict_visible_contact_child_entrypoint_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED"
    )
