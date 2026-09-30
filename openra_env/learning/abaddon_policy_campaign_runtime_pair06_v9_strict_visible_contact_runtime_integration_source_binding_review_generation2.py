"""Exact-blob source review of pair-06 V9 runtime integration.

Pins the non-activated decision-hook integration and regression suite. The
review confirms that the reviewed coherent V9 policy is inserted only between
legacy tool construction and the supplied decider, while the unchanged legacy
host validator, six-attempt fail-closed loop, rejection feedback, frozen compact
state, and five-value return shape are preserved.

No proto-child or parent-supervisor wiring is present. No runtime activation,
execution, replay, training, promotion, deployment, chain, wallet, transaction,
funds, or scheduler authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_generation2
    as integration,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-runtime-integration-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "9a67e734423a9ca1f0e822607572a614cf1e756a"
INTEGRATION_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_runtime_integration_generation2.py"
)
INTEGRATION_GIT_BLOB = "8aa8a3bae62a914dfa1c1b7daf2fca6b13ecf2ef"
INTEGRATION_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_runtime_integration_generation2.py"
)
INTEGRATION_TEST_GIT_BLOB = "d1b0febbeee85e8e7c142e9bfef731128632e84e"

NEXT_GATE = "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_proto_child_wiring"
)


class Pair06V9StrictVisibleContactRuntimeIntegrationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactRuntimeIntegrationReviewHold(message)


@lru_cache(maxsize=1)
def _validated_integration() -> dict[str, Any]:
    out = (
        integration
        .pair06_v9_strict_visible_contact_runtime_integration_contract()
    )

    _require(
        out.get("decision_hook_runtime_integration_implemented") is True,
        "V9 strict-contact decision-hook integration missing",
    )
    _require(
        out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 runtime policy id drift",
    )
    _require(
        out.get("policy_applied_after_tool_build_before_decider") is True,
        "V9 policy application point drift",
    )
    _require(
        out.get("coherent_filtered_tools_and_contract_sent_to_decider")
        is True,
        "V9 coherent filtered surface drift",
    )
    _require(
        out.get("accepted_action_validated_against_filtered_surface") is True
        and out.get("unchanged_legacy_host_validator_used") is True,
        "V9 host validation boundary drift",
    )
    _require(
        out.get("legacy_five_value_return_shape_preserved") is True,
        "V9 legacy return-shape drift",
    )
    _require(
        out.get("max_attempts") == 6
        and out.get("host_rejection_feedback_forwarded") is True
        and out.get("world_mutation_before_host_validation") is False
        and out.get("frozen_compact_state_reused_across_rejected_attempts")
        is True,
        "V9 fail-closed retry semantics drift",
    )

    for field in (
        "production_functions_filtered_to_offered_surface",
        "legal_buildings_reconstructed_from_remaining_production",
        "legal_units_reconstructed_from_remaining_production",
        "normal_mode_contract_identity_preserved",
    ):
        _require(
            out.get(field) is True,
            "V9 runtime coherence invariant drift: " + field,
        )

    for field in (
        "proto_game_child_wiring_implemented",
        "parent_supervisor_wiring_implemented",
        "operator_invocation_implemented",
        "new_execution_request_opened",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(
            out.get(field) is False,
            "V9 runtime integration boundary drift: " + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_RUNTIME_INTEGRATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 runtime integration review frontier drift",
    )

    return deepcopy(out)


def pair06_v9_strict_visible_contact_runtime_integration_review_contract() -> dict[str, Any]:
    validated = _validated_integration()
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "integration_path": INTEGRATION_PATH,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "integration_test_path": INTEGRATION_TEST_PATH,
        "integration_test_git_blob": INTEGRATION_TEST_GIT_BLOB,
        "pair06_v9_strict_visible_contact_runtime_integration_reviewed": True,
        "decision_hook_runtime_integration_implemented": True,
        "coherent_filtered_surface_reviewed": True,
        "unchanged_legacy_host_validator_reviewed": True,
        "six_attempt_fail_closed_retry_reviewed": True,
        "frozen_compact_state_reuse_reviewed": True,
        "proto_game_child_wiring_implemented": False,
        "parent_supervisor_wiring_implemented": False,
        "operator_invocation_implemented": False,
        "new_execution_request_opened": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_integration": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactRuntimeIntegrationReviewHold(NEXT_GATE)
