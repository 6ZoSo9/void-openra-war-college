"""Exact-blob source review for the pair-06 V9 strict-contact proposal.

This review pins the proposal and its regression tests to repository bytes and
checks that it remains hypothesis-only. It does not implement the policy, open
an execution request, or grant runtime, training, promotion, deployment, chain,
wallet, transaction, or funds authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_proposal_generation2
    as proposal,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-policy-proposal-review-contract.v1"
)

ACCEPTED_BASE_MAIN_HEAD = "4853549d6fca608384ecca3f1312a3c780bec90d"
PROPOSAL_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_policy_proposal_generation2.py"
)
PROPOSAL_GIT_BLOB = "edee41ef40b967b5c9d418465ed17f280f2dbf02"
PROPOSAL_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_policy_proposal_generation2.py"
)
PROPOSAL_TEST_GIT_BLOB = "84b48e6f36c407aac9cd6be043cafaa96b7b6534"

NEXT_GATE = "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_policy_implementation"
)


class Pair06V9StrictVisibleContactProposalReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9StrictVisibleContactProposalReviewHold(message)


def pair06_v9_strict_visible_contact_policy_proposal_review_contract() -> dict[str, Any]:
    candidate = proposal.pair06_v9_strict_visible_contact_policy_proposal_contract()

    _require(
        candidate.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1",
        "V9 policy id drift",
    )
    _require(
        candidate.get("baseline_policy_id")
        == "pair06-v8-combat-action-priority-envelope-v1",
        "V9 baseline policy id drift",
    )
    _require(
        candidate.get("pair_slot") == 6
        and candidate.get("arm") == "baseline",
        "V9 pair identity drift",
    )

    evidence = candidate.get("evidence_basis")
    _require(isinstance(evidence, dict), "V9 evidence basis missing")
    _require(
        evidence.get("v8_policy_retains_reinforcement_tools_in_visible_contact")
        is True,
        "V9 baseline surface premise drift",
    )
    _require(
        evidence.get("v8_v2_coherent_run_completed") is True
        and evidence.get("v8_v2_coherent_rounds_completed") == 36
        and evidence.get("v8_v2_coherent_outcome") == "DRAW_OR_UNFINISHED",
        "V9 runtime evidence basis drift",
    )
    _require(
        evidence.get("action_level_causal_attribution_available") is False
        and candidate.get("causal_claim_made") is False,
        "V9 proposal overclaims causality",
    )

    _require(
        candidate.get("recovery_mode_changed") is False
        and candidate.get("normal_mode_changed") is False
        and candidate.get("visible_contact_mode_changed") is True,
        "V9 intervention boundary drift",
    )
    _require(
        candidate.get("reinforcement_tools_allowed_during_strict_visible_contact")
        is False,
        "V9 strict contact still allows reinforcement choices",
    )
    _require(
        candidate.get("implementation_present") is False
        and candidate.get("runtime_integration_present") is False
        and candidate.get("new_execution_request_opened") is False,
        "V9 proposal unexpectedly crossed source-only boundary",
    )

    for field in (
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
            candidate.get(field) is False,
            "V9 proposal authority drift: " + field,
        )

    _require(
        candidate.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_PROPOSAL_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "V9 proposal review frontier drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "proposal_path": PROPOSAL_PATH,
        "proposal_git_blob": PROPOSAL_GIT_BLOB,
        "proposal_test_path": PROPOSAL_TEST_PATH,
        "proposal_test_git_blob": PROPOSAL_TEST_GIT_BLOB,
        "pair06_v9_strict_visible_contact_policy_proposal_reviewed": True,
        "policy_id": candidate["policy_id"],
        "baseline_policy_id": candidate["baseline_policy_id"],
        "pair_slot": candidate["pair_slot"],
        "arm": candidate["arm"],
        "causal_claim_made": False,
        "action_level_causal_attribution_available": False,
        "recovery_mode_changed": False,
        "normal_mode_changed": False,
        "visible_contact_mode_changed": True,
        "reinforcement_tools_allowed_during_strict_visible_contact": False,
        "implementation_present": False,
        "runtime_integration_present": False,
        "new_execution_request_opened": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_proposal": deepcopy(candidate),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def implement_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9StrictVisibleContactProposalReviewHold(NEXT_GATE)
