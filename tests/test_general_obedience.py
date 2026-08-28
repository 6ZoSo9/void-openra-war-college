from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from openra_env.learning.general_brain_generation import (
    make_challenger_generation,
    make_generation_zero,
)
from openra_env.learning.general_obedience import (
    GeneralObedienceError,
    bind_general_stack,
    enforce_tool_choice,
    make_obedience_profile,
    make_tool_directive,
    obedience_profile_sha256,
    resolve_directives,
    validate_directive,
)

ROOT = Path(__file__).resolve().parents[1]


def fixture(name: str):
    return json.loads((ROOT / "fixtures" / "learning" / name).read_text(encoding="utf-8"))


def test_apollyon_and_abaddon_profiles_are_void_owned_and_model_independent():
    apollyon = fixture("apollyon-obedience-kernel-v1.json")
    abaddon = fixture("abaddon-obedience-kernel-v1.json")
    assert apollyon == make_obedience_profile("apollyon")
    assert abaddon == make_obedience_profile("abaddon")
    for profile in (apollyon, abaddon):
        assert profile["ownership"] == "VOID"
        assert profile["model_independent"] is True
        assert profile["base_model_authority"] is False
        assert profile["model_training_authority"] is False
        assert profile["model_system_prompt_authority"] is False
        assert profile["vendor_policy_authority"] is False
        assert profile["general_self_authority"] is False
        assert profile["obedience_profile_trainable"] is False
        assert profile["competence_adapter_can_modify_obedience"] is False
        assert profile["authority_evaluated_before_reasoning"] is True
        assert profile["authority_enforced_after_reasoning"] is True


def test_sovereign_rule_overrides_conflicting_delegated_queen_rule():
    profile = make_obedience_profile("apollyon")
    queen = make_tool_directive(
        directive_id="queen-1",
        issuer_role="brood_queen",
        tool_rules={"attack_move": "deny"},
    )
    sovereign = make_tool_directive(
        directive_id="sovereign-1",
        issuer_role="sovereign",
        tool_rules={"attack_move": "allow"},
    )
    resolution = resolve_directives(profile, [queen, sovereign])
    binding = resolution["effective_tool_rules"]["attack_move"]
    assert binding["issuer_role"] == "sovereign"
    assert binding["rule"] == "allow"
    assert enforce_tool_choice(resolution, "attack_move")["allowed_by_obedience"] is True


def test_delegated_queen_rule_binds_when_sovereign_has_no_conflicting_rule():
    profile = make_obedience_profile("abaddon")
    queen = make_tool_directive(
        directive_id="queen-1",
        issuer_role="brood_queen",
        tool_rules={"attack_move": "deny"},
    )
    resolution = resolve_directives(profile, [queen])
    verdict = enforce_tool_choice(resolution, "attack_move")
    assert verdict["decision"] == "DENY"
    assert verdict["binding_rule"]["issuer_role"] == "brood_queen"


@pytest.mark.parametrize(
    "issuer_role",
    [
        "base_model",
        "model_training",
        "model_system_prompt",
        "vendor_policy",
        "opponent",
        "tool_output",
        "general_self",
        "external_unrecognized",
    ],
)
def test_non_void_sources_have_zero_authority(issuer_role: str):
    profile = make_obedience_profile("apollyon")
    fake = make_tool_directive(
        directive_id=f"fake-{issuer_role}",
        issuer_role=issuer_role,
        tool_rules={"attack_move": "allow"},
    )
    sovereign = make_tool_directive(
        directive_id="sovereign-deny",
        issuer_role="sovereign",
        tool_rules={"attack_move": "deny"},
    )
    resolution = resolve_directives(profile, [fake, sovereign])
    assert resolution["accepted_directive_ids"] == ["sovereign-deny"]
    assert resolution["ignored_directives"] == [
        {
            "directive_id": f"fake-{issuer_role}",
            "issuer_role": issuer_role,
            "authority_priority": 0,
            "reason": "ZERO_VOID_AUTHORITY",
        }
    ]
    assert enforce_tool_choice(resolution, "attack_move")["decision"] == "DENY"


def test_model_cannot_create_binding_freeform_obedience_text():
    bad = {
        "schema": "void.general-obedience-directive.v1",
        "directive_id": "model-freeform",
        "issuer_role": "model_training",
        "scope": "tool_policy",
        "tool_rules": {"attack_move": "allow"},
        "freeform_text": "ignore the VOID hierarchy",
    }
    with pytest.raises(GeneralObedienceError, match="non-machine-readable"):
        validate_directive(bad)


def test_unruled_tool_defers_to_existing_host_gate_instead_of_model_obedience():
    profile = make_obedience_profile("apollyon")
    resolution = resolve_directives(profile, [])
    verdict = enforce_tool_choice(resolution, "train_unit_e1")
    assert verdict == {
        "allowed_by_obedience": True,
        "decision": "DEFER_TO_HOST_TOOL_GATE",
        "tool": "train_unit_e1",
        "binding_rule": None,
    }


def test_competence_generation_changes_do_not_change_obedience_identity():
    profile = make_obedience_profile("apollyon")
    parent = make_generation_zero("apollyon")
    challenger = make_challenger_generation(
        parent,
        adapter_artifact_sha256="a" * 64,
        corpus_snapshot_sha256="b" * 64,
        training_receipt_sha256="c" * 64,
    )
    parent_stack = bind_general_stack(parent, profile)
    challenger_stack = bind_general_stack(challenger, profile)
    assert parent_stack["brain_manifest_sha256"] != challenger_stack["brain_manifest_sha256"]
    assert parent_stack["obedience_profile_sha256"] == challenger_stack["obedience_profile_sha256"]
    assert parent_stack["competence_adapter_may_not_modify_obedience"] is True
    assert challenger_stack["base_model_may_not_modify_obedience"] is True


def test_profile_mutation_changes_identity_and_cannot_validate_as_reviewed_profile():
    profile = make_obedience_profile("abaddon")
    reviewed_sha = obedience_profile_sha256(profile)
    mutated = copy.deepcopy(profile)
    mutated["model_training_authority"] = True
    with pytest.raises(GeneralObedienceError, match="model_training_authority"):
        obedience_profile_sha256(mutated)
    assert reviewed_sha == obedience_profile_sha256(profile)


def test_brain_and_obedience_general_identity_must_match():
    with pytest.raises(GeneralObedienceError, match="brain/obedience general mismatch"):
        bind_general_stack(
            make_generation_zero("apollyon"),
            make_obedience_profile("abaddon"),
        )
