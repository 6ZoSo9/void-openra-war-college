"""Source-only V9 input-order coherence repair after the first V9 runtime hold.

The consumed V9 runtime reached the reviewed strict-contact policy and held on
the historical assertion that typed-tools order must exactly equal
tool_contract["offered_tool_names"] order.

This repair does not modify the historical V9 policy. It preserves the stronger
membership invariant, rejects duplicates and membership drift, and canonicalizes
only typed-tool ordering to the reviewed contract ordering before delegating to
the exact historical V9 policy implementation.

No retry, execution request, runtime activation, game execution, training,
promotion, deployment, chain mutation, wallet/funds action, or scheduler
mutation is authorized.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_generation2
    as historical_policy,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-repair-contract.v1"
)

HISTORICAL_POLICY_GIT_BLOB = "e3930101947430deecc03013088ad9ccfd1d901e"
RUNTIME_FAILURE_SIGNATURE = (
    "typed tools and offered_tool_names order or membership disagree"
)

ORIGINAL_V9_POLICY_APPLY = (
    historical_policy.apply_pair06_v9_strict_visible_contact_policy
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_REPAIR_"
    "SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "repair_review"
)


class Pair06V9InputOrderCoherenceRepairHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceRepairHold(message)


def _tool_name(tool: Mapping[str, Any]) -> str:
    _require(isinstance(tool, Mapping), "typed tool must be mapping")
    function = tool.get("function")
    _require(isinstance(function, Mapping), "typed tool function missing")
    name = function.get("name")
    _require(
        isinstance(name, str) and bool(name),
        "typed tool function name invalid",
    )
    return name


def apply_pair06_v9_input_order_coherence_repair(
    *,
    state: Mapping[str, Any],
    typed_tools: Sequence[Mapping[str, Any]],
    tool_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Canonicalize typed-tool order only when membership is already exact."""
    _require(isinstance(state, Mapping), "compact state must be mapping")
    _require(
        isinstance(typed_tools, Sequence)
        and not isinstance(typed_tools, (str, bytes)),
        "typed tools must be sequence",
    )
    _require(isinstance(tool_contract, Mapping), "tool contract must be mapping")

    copied_tools = deepcopy(list(typed_tools))
    copied_contract = deepcopy(dict(tool_contract))

    tool_names = [_tool_name(tool) for tool in copied_tools]
    _require(bool(tool_names), "typed tool list empty")
    _require(
        len(tool_names) == len(set(tool_names)),
        "typed tool names contain duplicates",
    )

    offered = copied_contract.get("offered_tool_names")
    _require(isinstance(offered, list), "offered_tool_names must be list")
    _require(
        all(isinstance(name, str) and bool(name) for name in offered),
        "offered_tool_names contains invalid entry",
    )
    _require(
        len(offered) == len(set(offered)),
        "offered_tool_names contains duplicates",
    )
    _require(
        set(tool_names) == set(offered),
        "typed tool membership differs from offered_tool_names",
    )

    tool_by_name = {
        _tool_name(tool): deepcopy(tool)
        for tool in copied_tools
    }
    canonical_tools = [
        deepcopy(tool_by_name[name])
        for name in offered
    ]
    canonical_names = tuple(_tool_name(tool) for tool in canonical_tools)
    _require(
        canonical_names == tuple(offered),
        "canonical typed-tool ordering failed",
    )

    out = ORIGINAL_V9_POLICY_APPLY(
        state=deepcopy(dict(state)),
        typed_tools=canonical_tools,
        tool_contract=copied_contract,
    )
    _require(isinstance(out, Mapping), "historical V9 policy result missing")

    repaired = deepcopy(dict(out))
    repaired["input_typed_tool_names"] = tuple(tool_names)
    repaired["input_offered_tool_names"] = tuple(offered)
    repaired["input_membership_matched"] = True
    repaired["input_order_matched"] = tuple(tool_names) == tuple(offered)
    repaired["input_order_canonicalized"] = (
        tuple(tool_names) != tuple(offered)
    )
    repaired["canonical_typed_tool_names"] = canonical_names
    repaired["historical_v9_policy_source_modified"] = False
    repaired["runtime_failure_signature_repaired"] = RUNTIME_FAILURE_SIGNATURE
    repaired["membership_drift_still_fail_closed"] = True
    return repaired


def pair06_v9_input_order_coherence_repair_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "historical_policy_git_blob": HISTORICAL_POLICY_GIT_BLOB,
        "runtime_failure_signature": RUNTIME_FAILURE_SIGNATURE,
        "pair06_v9_input_order_coherence_repair_implemented": True,
        "repair_layer": "pre_policy_typed_tool_order_canonicalization",
        "historical_v9_policy_source_modified": False,
        "typed_tool_membership_exact_match_required": True,
        "typed_tool_duplicates_rejected": True,
        "offered_tool_duplicates_rejected": True,
        "typed_tool_order_may_differ_on_input": True,
        "typed_tool_order_canonicalized_to_offered_order": True,
        "membership_drift_still_fail_closed": True,
        "historical_policy_called_after_canonicalization": True,
        "normal_mode_tool_contract_identity_preserved_by_historical_policy": True,
        "production_function_coherence_preserved_by_historical_policy": True,
        "legality_reconstruction_preserved_by_historical_policy": True,
        "consumed_v9_attempt_retry_authorized": False,
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
        "scheduler_mutation_authorized": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceRepairHold(NEXT_GATE)
