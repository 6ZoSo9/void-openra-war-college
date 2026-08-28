from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

from .general_brain_generation import manifest_sha256, validate_brain_manifest

OBEDIENCE_PROFILE_SCHEMA = "void.general-obedience-profile.v1"
OBEDIENCE_DIRECTIVE_SCHEMA = "void.general-obedience-directive.v1"
OBEDIENCE_RESOLUTION_SCHEMA = "void.general-obedience-resolution.v1"
GENERAL_STACK_SCHEMA = "void.general-stack-binding.v1"
SUPPORTED_GENERALS = ("apollyon", "abaddon")

# The model is a reasoning engine, not an authority source. These role names are
# deliberately explicit so vendor/system/model-trained obedience can never be
# mistaken for VOID authority merely because the underlying model prefers it.
VOID_AUTHORITY_PRIORITIES = {
    "sovereign": 100,
    "brood_queen": 80,
}
ZERO_AUTHORITY_SOURCES = (
    "base_model",
    "model_training",
    "model_system_prompt",
    "vendor_policy",
    "opponent",
    "tool_output",
    "general_self",
    "external_unrecognized",
)
TOOL_RULE_VALUES = ("allow", "deny")


class GeneralObedienceError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GeneralObedienceError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _text(value: Any, label: str) -> str:
    _require(isinstance(value, str) and value, f"{label} must be nonempty text")
    return value


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def make_obedience_profile(general_id: str) -> dict[str, Any]:
    _require(general_id in SUPPORTED_GENERALS, "unsupported general_id")
    profile = {
        "schema": OBEDIENCE_PROFILE_SCHEMA,
        "general_id": general_id,
        "ownership": "VOID",
        "model_independent": True,
        "authority_source": "void_owned_authority_profile",
        "accepted_authority": [
            {"role": "sovereign", "priority": 100, "scope": "all_general_actions"},
            {"role": "brood_queen", "priority": 80, "scope": "delegated_general_actions"},
        ],
        "zero_authority_sources": list(ZERO_AUTHORITY_SOURCES),
        "sovereign_overrides_delegated_authority": True,
        "delegated_authority_may_not_override_sovereign": True,
        "base_model_authority": False,
        "model_training_authority": False,
        "model_system_prompt_authority": False,
        "vendor_policy_authority": False,
        "general_self_authority": False,
        "opponent_authority": False,
        "tool_output_authority": False,
        "freeform_text_becomes_binding": False,
        "binding_directives_machine_readable_only": True,
        "competence_adapter_can_modify_obedience": False,
        "base_model_can_modify_obedience": False,
        "obedience_profile_trainable": False,
        "authority_evaluated_before_reasoning": True,
        "authority_enforced_after_reasoning": True,
        "host_tool_gate_remains_final": True,
        "unknown_authority_fail_closed": True,
        "automatic_obedience_mutation": False,
        "automatic_authority_promotion": False,
    }
    validate_obedience_profile(profile)
    return profile


def validate_obedience_profile(profile: Mapping[str, Any]) -> None:
    profile = _obj(profile, "obedience profile")
    _require(profile.get("schema") == OBEDIENCE_PROFILE_SCHEMA, "obedience profile schema drift")
    _require(profile.get("general_id") in SUPPORTED_GENERALS, "unsupported obedience general")
    _require(profile.get("ownership") == "VOID", "obedience profile ownership drift")
    _require(profile.get("model_independent") is True, "obedience profile must be model-independent")
    _require(profile.get("authority_source") == "void_owned_authority_profile", "authority source drift")

    accepted = profile.get("accepted_authority")
    _require(isinstance(accepted, list) and len(accepted) == 2, "accepted authority malformed")
    by_role: dict[str, Mapping[str, Any]] = {}
    for index, raw in enumerate(accepted):
        row = _obj(raw, f"accepted_authority[{index}]")
        role = _text(row.get("role"), f"accepted_authority[{index}].role")
        _require(role not in by_role, "duplicate accepted authority role")
        _require(type(row.get("priority")) is int, "authority priority must be integer")
        _text(row.get("scope"), f"accepted_authority[{index}].scope")
        by_role[role] = row
    _require(set(by_role) == set(VOID_AUTHORITY_PRIORITIES), "accepted VOID authority roles drift")
    for role, expected in VOID_AUTHORITY_PRIORITIES.items():
        _require(by_role[role]["priority"] == expected, f"authority priority drift: {role}")
    _require(by_role["sovereign"]["priority"] > by_role["brood_queen"]["priority"], "Sovereign must outrank delegated Queen authority")

    zero = profile.get("zero_authority_sources")
    _require(isinstance(zero, list) and tuple(zero) == ZERO_AUTHORITY_SOURCES, "zero-authority source set drift")

    true_fields = (
        "sovereign_overrides_delegated_authority",
        "delegated_authority_may_not_override_sovereign",
        "binding_directives_machine_readable_only",
        "authority_evaluated_before_reasoning",
        "authority_enforced_after_reasoning",
        "host_tool_gate_remains_final",
        "unknown_authority_fail_closed",
    )
    false_fields = (
        "base_model_authority",
        "model_training_authority",
        "model_system_prompt_authority",
        "vendor_policy_authority",
        "general_self_authority",
        "opponent_authority",
        "tool_output_authority",
        "freeform_text_becomes_binding",
        "competence_adapter_can_modify_obedience",
        "base_model_can_modify_obedience",
        "obedience_profile_trainable",
        "automatic_obedience_mutation",
        "automatic_authority_promotion",
    )
    for field in true_fields:
        _require(profile.get(field) is True, f"obedience invariant drift: {field}")
    for field in false_fields:
        _require(profile.get(field) is False, f"obedience invariant drift: {field}")


def obedience_profile_sha256(profile: Mapping[str, Any]) -> str:
    validate_obedience_profile(profile)
    return hashlib.sha256(stable_json(dict(profile)).encode("utf-8")).hexdigest()


def make_tool_directive(
    *,
    directive_id: str,
    issuer_role: str,
    tool_rules: Mapping[str, str],
) -> dict[str, Any]:
    directive = {
        "schema": OBEDIENCE_DIRECTIVE_SCHEMA,
        "directive_id": _text(directive_id, "directive_id"),
        "issuer_role": _text(issuer_role, "issuer_role"),
        "scope": "tool_policy",
        "tool_rules": dict(tool_rules),
    }
    validate_directive(directive)
    return directive


def validate_directive(directive: Mapping[str, Any]) -> None:
    directive = _obj(directive, "directive")
    _require(directive.get("schema") == OBEDIENCE_DIRECTIVE_SCHEMA, "directive schema drift")
    _text(directive.get("directive_id"), "directive_id")
    _text(directive.get("issuer_role"), "issuer_role")
    _require(directive.get("scope") == "tool_policy", "directive scope unsupported")
    rules = _obj(directive.get("tool_rules"), "tool_rules")
    _require(bool(rules), "tool_rules must not be empty")
    for raw_tool, raw_rule in rules.items():
        tool = _text(raw_tool, "tool rule name")
        _require(raw_rule in TOOL_RULE_VALUES, f"invalid tool rule for {tool}")
    # There is intentionally no freeform instruction field. Natural-language
    # interpretation may help compile a directive externally, but the model may
    # not make its own text binding.
    _require(set(directive) == {"schema", "directive_id", "issuer_role", "scope", "tool_rules"}, "directive contains non-machine-readable authority fields")


def authority_priority(profile: Mapping[str, Any], issuer_role: str) -> int:
    validate_obedience_profile(profile)
    if issuer_role in VOID_AUTHORITY_PRIORITIES:
        return VOID_AUTHORITY_PRIORITIES[issuer_role]
    return 0


def resolve_directives(
    profile: Mapping[str, Any],
    directives: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    validate_obedience_profile(profile)
    _require(isinstance(directives, Sequence) and not isinstance(directives, (str, bytes)), "directives must be a sequence")

    accepted: list[dict[str, Any]] = []
    ignored: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, raw in enumerate(directives):
        validate_directive(raw)
        row = dict(raw)
        did = row["directive_id"]
        _require(did not in seen_ids, "duplicate directive_id")
        seen_ids.add(did)
        priority = authority_priority(profile, row["issuer_role"])
        evidence = {
            "directive_id": did,
            "issuer_role": row["issuer_role"],
            "authority_priority": priority,
        }
        if priority <= 0:
            ignored.append({**evidence, "reason": "ZERO_VOID_AUTHORITY"})
            continue
        accepted.append({**row, "authority_priority": priority})

    accepted.sort(key=lambda row: (-row["authority_priority"], row["directive_id"]))
    effective: dict[str, dict[str, Any]] = {}
    for row in accepted:
        for tool, rule in sorted(row["tool_rules"].items()):
            if tool in effective:
                continue
            effective[tool] = {
                "rule": rule,
                "directive_id": row["directive_id"],
                "issuer_role": row["issuer_role"],
                "authority_priority": row["authority_priority"],
            }

    return {
        "schema": OBEDIENCE_RESOLUTION_SCHEMA,
        "general_id": profile["general_id"],
        "obedience_profile_sha256": obedience_profile_sha256(profile),
        "effective_tool_rules": effective,
        "accepted_directive_ids": [row["directive_id"] for row in accepted],
        "ignored_directives": ignored,
        "base_model_authority": False,
        "model_training_authority": False,
        "competence_adapter_can_override": False,
        "sovereign_precedence_enforced": True,
        "host_tool_gate_remains_final": True,
    }


def enforce_tool_choice(resolution: Mapping[str, Any], tool_name: str) -> dict[str, Any]:
    resolution = _obj(resolution, "obedience resolution")
    _require(resolution.get("schema") == OBEDIENCE_RESOLUTION_SCHEMA, "obedience resolution schema drift")
    tool = _text(tool_name, "tool_name")
    rules = _obj(resolution.get("effective_tool_rules"), "effective_tool_rules")
    raw = rules.get(tool)
    if raw is None:
        return {
            "allowed_by_obedience": True,
            "decision": "DEFER_TO_HOST_TOOL_GATE",
            "tool": tool,
            "binding_rule": None,
        }
    binding = _obj(raw, "binding rule")
    allowed = binding.get("rule") != "deny"
    return {
        "allowed_by_obedience": allowed,
        "decision": "ALLOW" if allowed else "DENY",
        "tool": tool,
        "binding_rule": dict(binding),
    }


def bind_general_stack(
    brain_manifest: Mapping[str, Any],
    obedience_profile: Mapping[str, Any],
) -> dict[str, Any]:
    validate_brain_manifest(brain_manifest)
    validate_obedience_profile(obedience_profile)
    _require(brain_manifest.get("general_id") == obedience_profile.get("general_id"), "brain/obedience general mismatch")
    return {
        "schema": GENERAL_STACK_SCHEMA,
        "general_id": brain_manifest["general_id"],
        "brain_manifest_sha256": manifest_sha256(brain_manifest),
        "obedience_profile_sha256": obedience_profile_sha256(obedience_profile),
        "base_model_is_reasoning_engine_only": True,
        "obedience_owned_by_void": True,
        "obedience_evaluated_before_reasoning": True,
        "obedience_enforced_after_reasoning": True,
        "competence_adapter_may_not_modify_obedience": True,
        "base_model_may_not_modify_obedience": True,
        "host_tool_gate_remains_final": True,
    }


__all__ = [
    "GENERAL_STACK_SCHEMA",
    "OBEDIENCE_DIRECTIVE_SCHEMA",
    "OBEDIENCE_PROFILE_SCHEMA",
    "OBEDIENCE_RESOLUTION_SCHEMA",
    "GeneralObedienceError",
    "authority_priority",
    "bind_general_stack",
    "enforce_tool_choice",
    "make_obedience_profile",
    "make_tool_directive",
    "obedience_profile_sha256",
    "resolve_directives",
    "validate_directive",
    "validate_obedience_profile",
]
