"""Pure deterministic-opponent adapter for the scout-repair canary runner.

This is a source-only composition seam. It matches the historical
``apollyon_decision_typed`` call shape so a later reviewed binding can replace
that one decision callback without invoking a model. It does not install itself,
start/stop a service, create an attempt marker, write evidence, dispatch a joint
step, or authorize execution.

One call derives the CURRENT typed tool contract, asks the fixed deterministic
pressure opponent for exactly one proposal, passes that exact proposal through
the supplied unchanged typed host validator exactly once, and fails closed on
rejection. There is no retry and no fallback-to-advance after rejection.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Mapping

from openra_env.learning import abaddon_scout_canary_opponent_source_binding_review_v1 as opponent_review
from openra_env.learning import abaddon_scout_canary_opponent_v1 as opponent
from openra_env.learning import abaddon_scout_repair_canary_runner_requirements_v1 as requirements

SCHEMA = "void.abaddon.scout-repair-canary-runner-adapter.v1"
REVIEW_SCHEMA = "void.abaddon.scout-repair-canary-runner-adapter-review.v1"
NEXT_GATE = "SCOUT_REPAIR_CANARY_FULL_RUNNER_COMPOSITION_SOURCE_REVIEW_REQUIRED"
MAX_REASON = 4096
MAX_OFFERED_TOOLS = 512


class ScoutRepairCanaryRunnerAdapterHold(ValueError):
    pass


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutRepairCanaryRunnerAdapterHold(reason)


def _validate_contract(contract: Any) -> tuple[str, ...]:
    _require(type(contract) is dict, "typed_tool_contract_object_required")
    names = contract.get("offered_tool_names")
    _require(
        type(names) is list
        and 0 < len(names) <= MAX_OFFERED_TOOLS
        and all(type(name) is str and name for name in names),
        "offered_tool_names_invalid",
    )
    _require(len(names) == len(set(names)), "offered_tool_names_duplicate")
    return tuple(names)


class DeterministicCanaryOpponentAdapter:
    """Drop-in decision callback for the future canary composition layer.

    ``helper`` is accepted only to preserve the historical function signature;
    it is deliberately never dereferenced. A later binding must also prevent the
    historical runner from starting or cleaning up the model service and must
    rewrite durable run/controller labels to the reviewed canary schema.
    """

    def __init__(self, *, tool_contract_builder: Callable, typed_host_validator: Callable):
        _require(callable(tool_contract_builder), "tool_contract_builder_required")
        _require(callable(typed_host_validator), "typed_host_validator_required")
        reviewed = opponent_review.scout_repair_opponent_source_binding_review()
        req = requirements.scout_repair_canary_runner_requirements()
        source = reviewed["opponent"]["source_identity"]
        _require(source["sha256"] == req["opponent_source_identity"]["sha256"], "opponent_binding_drift")
        _require(reviewed["opponent"]["model_backed"] is False, "model_backed_opponent_forbidden")
        _require(reviewed["execution_authorized"] is False, "prior_stage_carries_authority")
        self._tool_contract_builder = tool_contract_builder
        self._typed_host_validator = typed_host_validator
        self._opponent_source = deepcopy(source)
        self._calls = 0
        self._last_round = 0
        self._last_review_row: dict[str, Any] | None = None

    def decide(
        self,
        base: Any,
        helper: Any,
        state: Mapping[str, Any],
        pending: Mapping[str, Any],
        pb2: Any,
        doctrine: str,
        round_no: int,
    ) -> tuple[str, dict[str, Any], list[Any], list[dict[str, Any]], dict[str, Any]]:
        """Return the historical five-tuple without using ``helper`` or retrying."""
        _require(type(doctrine) is str and doctrine == "FEINTER", "canary_doctrine_must_be_default_feinter")
        _require(type(round_no) is int and 1 <= round_no <= 200, "round_number_invalid")
        _require(round_no > self._last_round, "round_must_advance_monotonically")
        _require(isinstance(state, Mapping), "state_object_required")
        _require(isinstance(pending, Mapping), "pending_object_required")
        _require(callable(getattr(base, "compact_state", None)), "base_compact_state_required")

        # ``helper`` is intentionally unused. Keep this assignment explicit so
        # source review can see that preserving the historical signature does
        # not create a model-call capability in this adapter.
        _ = helper

        tools, contract = self._tool_contract_builder(base, state, pending)
        _require(type(tools) is list, "typed_tool_definitions_required")
        offered = _validate_contract(contract)
        proposal = opponent.propose_deterministic_pressure_action(
            base.compact_state(state),
            offered_tool_names=offered,
        )
        _require(proposal["tool"] in offered, "deterministic_proposal_not_offered")
        _require(proposal["model_backed"] is False, "model_backed_proposal_forbidden")
        _require(proposal["host_validation_required"] is True, "host_validation_must_remain_required")
        _require(proposal["execution_authority"] is False, "proposal_carries_execution_authority")

        name = proposal["tool"]
        args = deepcopy(proposal["arguments"])
        result = self._typed_host_validator(
            base,
            name,
            deepcopy(args),
            state,
            pending,
            pb2,
            contract,
        )
        _require(type(result) is tuple and len(result) == 3, "host_validation_result_shape")
        accepted, reason, commands = result
        _require(type(accepted) is bool, "host_validation_accepted_type")
        _require(type(reason) is str and len(reason) <= MAX_REASON, "host_validation_reason_type")
        _require(type(commands) is list, "host_validation_commands_type")
        if not accepted:
            # No second proposal, no model retry, and no manufactured advance.
            raise ScoutRepairCanaryRunnerAdapterHold("deterministic_proposal_rejected_by_host:" + reason)

        attempt = {
            "attempt": 1,
            "tool": name,
            "arguments": deepcopy(args),
            "accepted": True,
            "host_reason": reason,
            "function_was_offered": True,
            "decision_source": proposal["decision_source"],
            "deterministic": True,
            "model_backed": False,
            "world_mutated_before_validation": False,
            "automatic_retry": False,
            "training_candidate": False,
            "opponent_source_sha256": self._opponent_source["sha256"],
        }
        self._calls += 1
        self._last_round = round_no
        self._last_review_row = {
            "schema": SCHEMA,
            "round": round_no,
            "doctrine": doctrine,
            "tool": name,
            "arguments": deepcopy(args),
            "host_reason": reason,
            "command_count": len(commands),
            "offered_tool_names": list(offered),
            "deterministic_opponent_identity": deepcopy(self._opponent_source),
            "model_service_used": False,
            "model_inference_used": False,
            "proposal_count": 1,
            "host_validation_count": 1,
            "automatic_retry": False,
            "training_candidate": False,
            "execution_authority": False,
        }
        return name, args, commands, [attempt], deepcopy(contract)

    def review_snapshot(self) -> dict[str, Any]:
        return {
            "schema": REVIEW_SCHEMA,
            "decision_calls": self._calls,
            "last_round": self._last_round,
            "last_review_row": deepcopy(self._last_review_row),
            "opponent_source_identity": deepcopy(self._opponent_source),
            "helper_dereferenced": False,
            "model_service_start_implemented": False,
            "model_inference_implemented": False,
            "automatic_retry_implemented": False,
            "joint_dispatch_implemented": False,
            "attempt_marker_implemented": False,
            "evidence_write_implemented": False,
            "execution_authority_created": False,
            "next_gate": NEXT_GATE,
        }


def adapter_review_claim() -> dict[str, Any]:
    """Describe only this adapter's source boundary; do not claim full-runner admission."""
    req = requirements.scout_repair_canary_runner_requirements()
    return {
        "schema": "void.abaddon.scout-repair-canary-runner-adapter-review.v1",
        "experiment_namespace": req["experiment_namespace"],
        "seed": req["seed"],
        "opponent_source_sha256": req["opponent_source_identity"]["sha256"],
        "typed_current_turn_tool_contract_consumed": True,
        "typed_host_validator_callback_required": True,
        "one_deterministic_proposal_per_call": True,
        "one_host_validation_per_call": True,
        "rejected_proposal_retry_implemented": False,
        "rejected_proposal_advance_fallback_implemented": False,
        "model_helper_dereferenced": False,
        "model_service_start_implemented": False,
        "model_inference_implemented": False,
        "joint_dispatch_implemented": False,
        "attempt_marker_implemented": False,
        "evidence_write_implemented": False,
        "adapter_review_rows_nontraining": True,
        "historical_runner_model_service_start_suppressed": False,
        "historical_runner_cleanup_service_action_suppressed": False,
        "historical_runner_durable_controller_rows_relabelled_nontraining": False,
        "full_runner_source_review_claim_valid": False,
        "execution_authority_created": False,
        "next_gate": NEXT_GATE,
    }


def authorize_install_run_or_dispatch(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairCanaryRunnerAdapterHold(NEXT_GATE)
