"""Optional fail-closed validation for Conditional Engagement V2.2 evidence."""
from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from ._spar_conditional_v2_2_reviewed_identity import (
    PARENT_V21_CANDIDATE_SHA256,
    REVIEWED_V22_IDENTITY,
)
from ._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    SHA256,
    SHA40,
    ContractError,
    _arr,
    _bool,
    _int,
    _jsonl,
    _obj,
    _pattern,
    _read,
    _str,
)

TRAJECTORY_KEY = "conditional_engagement_v2_2"
RUN_SCHEMA = "void.apollyon.conditional-engagement-run-binding.v2.2"
PREPARED_SCHEMA = "void.apollyon.conditional-engagement-prepared-round.v2.2"
ACCEPTED_SCHEMA = "void.apollyon.conditional-engagement-accepted-round.v2.2"
DECISION_SCHEMA = "void.apollyon.conditional-engagement-decision.v2.2"
COMPLIANCE_SCHEMA = "void.apollyon.conditional-engagement-action-compliance.v2.2"
REVIEWED_V22_HISTORY_WINDOW_ROUNDS = 6
MODES = (
    "REBUILD_FORCE",
    "ATTRITION_BRAKE",
    "CONTACT_RESPONSE",
    "MEASURED_CONTACT",
    "FORCE_CONVERSION",
    "ENGAGEMENT_DEFICIT",
    "BALANCED_SEARCH",
)


def _text_array(value: Any, label: str) -> list[str]:
    rows = _arr(value, label)
    return [_str(item, f"{label}[{index}]") for index, item in enumerate(rows)]


def _run_binding(header: dict[str, Any]) -> dict[str, Any] | None:
    raw = header.get(TRAJECTORY_KEY)
    if raw is None:
        return None
    raw = _obj(raw, f"run_header.{TRAJECTORY_KEY}")
    if _str(raw.get("schema"), "V2.2 run schema") != RUN_SCHEMA:
        raise ContractError("V2.2 run schema mismatch")
    _bool(raw.get("candidate_only"), "V2.2 candidate_only", True)
    for key in (
        "automatic_apollyon_weight_mutation",
        "automatic_abaddon_policy_promotion",
        "automatic_corpus_admission",
    ):
        _bool(raw.get(key), f"V2.2 {key}", False)

    parsed = {
        "source_commit": _pattern(raw.get("source_commit"), "V2.2 source_commit", SHA40),
        "candidate_sha256": _pattern(raw.get("candidate_sha256"), "V2.2 candidate SHA", SHA256),
        "policy_sha256": _pattern(raw.get("policy_sha256"), "V2.2 policy SHA", SHA256),
        "session_sha256": _pattern(raw.get("session_sha256"), "V2.2 session SHA", SHA256),
        "wrapper_sha256": _pattern(raw.get("wrapper_sha256"), "V2.2 wrapper SHA", SHA256),
    }
    for key, expected in REVIEWED_V22_IDENTITY.items():
        if parsed[key] != expected:
            raise ContractError(f"V2.2 reviewed identity mismatch: {key}")
    parent = _pattern(
        raw.get("parent_v2_1_candidate_sha256"),
        "V2.2 parent V2.1 candidate SHA",
        SHA256,
    )
    if parent != PARENT_V21_CANDIDATE_SHA256:
        raise ContractError("V2.2 parent V2.1 candidate mismatch")
    return {
        "schema": RUN_SCHEMA,
        "candidate_only": True,
        **parsed,
        "parent_v2_1_candidate_sha256": parent,
        "reviewed_identity_verified": True,
        "automatic_apollyon_weight_mutation": False,
        "automatic_abaddon_policy_promotion": False,
        "automatic_corpus_admission": False,
    }


def _round_binding(
    row: dict[str, Any],
    *,
    round_number: int,
    run: dict[str, Any] | None,
) -> tuple[str, dict[str, Any]] | None:
    raw = row.get(TRAJECTORY_KEY)
    if run is None:
        if raw is not None:
            raise ContractError("V2.2 round evidence is present without V2.2 run binding")
        return None
    if raw is None:
        raise ContractError(f"round {round_number} missing V2.2 evidence")

    raw = _obj(raw, f"round {round_number} V2.2 evidence")
    prepared = _obj(raw.get("prepared"), f"round {round_number} V2.2 prepared")
    accepted = _obj(raw.get("accepted"), f"round {round_number} V2.2 accepted")

    if _str(prepared.get("schema"), "V2.2 prepared schema") != PREPARED_SCHEMA:
        raise ContractError("V2.2 prepared schema mismatch")
    if _int(prepared.get("round"), "V2.2 prepared round", 1) != round_number:
        raise ContractError("V2.2 prepared round mismatch")
    if _pattern(prepared.get("candidate_sha256"), "V2.2 prepared candidate SHA", SHA256) != run["candidate_sha256"]:
        raise ContractError("V2.2 prepared candidate SHA mismatch")
    _bool(prepared.get("history_committed"), "V2.2 prepared history_committed", False)

    allowed = _text_array(prepared.get("current_allowed_tool_names"), "V2.2 current_allowed_tool_names")
    if not allowed or len(allowed) != len(set(allowed)):
        raise ContractError("V2.2 offered tool names must be nonempty and unique")

    apollyon = _obj(row.get("apollyon"), "V2.2-bound Apollyon decision")
    host_contract = _obj(apollyon.get("tool_contract"), "V2.2-bound Apollyon tool contract")
    host_allowed = _text_array(host_contract.get("offered_tool_names"), "Apollyon offered_tool_names")
    if allowed != host_allowed:
        raise ContractError("V2.2 prepared tool surface does not match host tool contract")

    decision = _obj(prepared.get("decision"), "V2.2 policy decision")
    if _str(decision.get("schema"), "V2.2 decision schema") != DECISION_SCHEMA:
        raise ContractError("V2.2 decision schema mismatch")
    mode = _str(decision.get("mode"), "V2.2 mode")
    if mode not in MODES:
        raise ContractError(f"unsupported V2.2 mode {mode!r}")
    reasons = _text_array(decision.get("reasons"), "V2.2 decision reasons")
    if not reasons:
        raise ContractError("V2.2 decision reasons must not be empty")
    if _pattern(decision.get("candidate_sha256"), "V2.2 decision candidate SHA", SHA256) != run["candidate_sha256"]:
        raise ContractError("V2.2 decision candidate SHA mismatch")
    _bool(decision.get("runtime_seed_branching"), "V2.2 runtime_seed_branching", False)
    evidence = _obj(decision.get("evidence"), "V2.2 decision evidence")
    if _int(evidence.get("round"), "V2.2 evidence round", 1) != round_number:
        raise ContractError("V2.2 evidence round mismatch")
    _str(decision.get("instruction"), "V2.2 decision instruction")

    coaching = _str(prepared.get("coaching"), "V2.2 coaching")
    if "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2_2" not in coaching or f"MODE={mode}" not in coaching:
        raise ContractError("V2.2 coaching text does not bind the recorded mode")
    exact_surface = "CURRENT_ALLOWED_TOOL_NAMES=" + ",".join(allowed)
    if exact_surface not in coaching:
        raise ContractError("V2.2 coaching does not bind the exact offered tool surface")
    if "do not infer hidden state" not in coaching or "TOOL_SURFACE_UNCHANGED=true" not in coaching:
        raise ContractError("V2.2 coaching boundary text is missing")

    compliance = _obj(prepared.get("action_compliance"), "V2.2 action_compliance")
    if _str(compliance.get("schema"), "V2.2 compliance schema") != COMPLIANCE_SCHEMA:
        raise ContractError("V2.2 action-compliance schema mismatch")
    if _str(compliance.get("mode"), "V2.2 compliance mode") != mode:
        raise ContractError("V2.2 action-compliance mode mismatch")
    _bool(compliance.get("tool_surface_unchanged"), "V2.2 tool_surface_unchanged", True)

    alternatives = [name for name in allowed if name != "attack_move"] if mode == "FORCE_CONVERSION" else []
    expected_discouraged = mode == "FORCE_CONVERSION" and bool(alternatives)
    _bool(compliance.get("attack_move_discouraged"), "V2.2 attack_move_discouraged", expected_discouraged)
    if _text_array(compliance.get("non_attack_move_offered_names"), "V2.2 non_attack_move_offered_names") != alternatives:
        raise ContractError("V2.2 non-attack-move offered alternatives mismatch")
    expected_preferred = "move_units" if mode == "FORCE_CONVERSION" and "move_units" in allowed else None
    actual_preferred = compliance.get("preferred_offered_alternative")
    if expected_preferred is None:
        if actual_preferred is not None:
            raise ContractError("V2.2 preferred alternative is present when not justified")
    elif _str(actual_preferred, "V2.2 preferred offered alternative") != expected_preferred:
        raise ContractError("V2.2 preferred offered alternative mismatch")

    if expected_discouraged and "Do not choose attack_move this round" not in coaching:
        raise ContractError("V2.2 FORCE_CONVERSION action rule is missing")
    if expected_preferred == "move_units" and "PREFERRED_OFFERED_ALTERNATIVE=move_units" not in coaching:
        raise ContractError("V2.2 preferred move_units coaching is missing")

    if _str(accepted.get("schema"), "V2.2 accepted schema") != ACCEPTED_SCHEMA:
        raise ContractError("V2.2 accepted schema mismatch")
    if _int(accepted.get("round"), "V2.2 accepted round", 1) != round_number:
        raise ContractError("V2.2 accepted round mismatch")
    if _pattern(accepted.get("candidate_sha256"), "V2.2 accepted candidate SHA", SHA256) != run["candidate_sha256"]:
        raise ContractError("V2.2 accepted candidate SHA mismatch")
    if _str(accepted.get("mode"), "V2.2 accepted mode") != mode:
        raise ContractError("V2.2 accepted mode mismatch")
    if _text_array(accepted.get("reasons"), "V2.2 accepted reasons") != reasons:
        raise ContractError("V2.2 accepted reasons do not match prepared decision")
    selected = _str(accepted.get("selected_tool"), "V2.2 accepted selected_tool")
    if selected != _str(apollyon.get("tool"), "Apollyon accepted tool"):
        raise ContractError("V2.2 accepted tool does not match Apollyon trajectory tool")
    if selected not in allowed:
        raise ContractError("V2.2 accepted tool was not in prepared tool surface")
    _bool(accepted.get("function_was_offered"), "V2.2 function_was_offered", True)
    history_size = _int(
        accepted.get("history_size"),
        "V2.2 history_size",
        1,
        REVIEWED_V22_HISTORY_WINDOW_ROUNDS,
    )
    expected_history_size = min(round_number, REVIEWED_V22_HISTORY_WINDOW_ROUNDS)
    if history_size != expected_history_size:
        raise ContractError("V2.2 history_size does not match reviewed bounded-history evolution")

    return mode, {
        "selected_tool": selected,
        "attack_move_discouraged": expected_discouraged,
        "preferred_move_units": expected_preferred == "move_units",
        "followed_non_attack_move": expected_discouraged and selected != "attack_move",
    }


def validate_conditional_v22_evidence(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str,
) -> dict[str, Any]:
    if SHA256.fullmatch(expected_trajectory_sha256) is None:
        raise ContractError("expected trajectory SHA-256 malformed for V2.2 validation")
    raw = _read(trajectory_path, "trajectory", MAX_TRAJECTORY_BYTES)
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_trajectory_sha256:
        raise ContractError("trajectory changed between base and V2.2 validation")
    rows = _jsonl(raw)
    if not rows:
        raise ContractError("trajectory is empty during V2.2 validation")
    run = _run_binding(rows[0])
    mode_counts: Counter[str] = Counter()
    rounds = 0
    discouraged = 0
    followed = 0
    ignored = 0
    move_units_preferred = 0
    move_units_selected = 0
    for row in rows[1:]:
        if row.get("event") != "joint_decision":
            continue
        rounds += 1
        bound = _round_binding(row, round_number=rounds, run=run)
        if bound is None:
            continue
        mode, compliance = bound
        mode_counts[mode] += 1
        if compliance["attack_move_discouraged"]:
            discouraged += 1
            if compliance["followed_non_attack_move"]:
                followed += 1
            else:
                ignored += 1
        if compliance["preferred_move_units"]:
            move_units_preferred += 1
            if compliance["selected_tool"] == "move_units":
                move_units_selected += 1
    if run is None:
        return {"present": False, "rounds_verified": 0, "mode_counts": {}}
    if rounds == 0:
        raise ContractError("V2.2 run binding has no joint_decision rows")
    return {
        "present": True,
        **run,
        "rounds_verified": rounds,
        "mode_counts": dict(sorted(mode_counts.items())),
        "all_round_receipts_verified": True,
        "tool_surface_bound": True,
        "accepted_tool_bound": True,
        "action_compliance_bound": True,
        "attack_move_discouraged_rounds": discouraged,
        "followed_non_attack_move_rounds": followed,
        "ignored_attack_move_discouragement_rounds": ignored,
        "preferred_move_units_offered_rounds": move_units_preferred,
        "preferred_move_units_selected_rounds": move_units_selected,
        "runtime_seed_branching": False,
    }
