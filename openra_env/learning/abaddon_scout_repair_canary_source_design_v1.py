"""Source-only canary identity design for the Abaddon scout repair.

This stage fixes a fresh namespace and seed by deterministic derivation so a
future operator cannot cherry-pick a convenient seed after observing results.
It still does not select an opponent implementation, accepted main head, runtime
image, attempt directory, invocation, or execution authority.
"""
from __future__ import annotations

import hashlib
from typing import Any

from openra_env.learning import abaddon_scout_repair_experiment_design_review_v1 as design_review

SCHEMA = "void.abaddon.scout-repair-canary-source-design.v1"
NEXT_GATE = "SCOUT_REPAIR_DETERMINISTIC_OPPONENT_SOURCE_BINDING_REQUIRED"
NAMESPACE = "abaddon-scout-repair-canary-v1"
SEED_DOMAIN = "void.abaddon.scout-repair-canary-v1"
SEED_BINDING_SHA256 = "5d8113072e904d59fde6145c73b2e9399772c46bcb1650bf9a687a46839cc9e6"
PAIR03_SEED = 1990061685
GENERATION2_CAMPAIGN_SEEDS = (
    1990061685, 208354846, 1496195137, 331379205, 905645055, 411746275,
)


class ScoutRepairCanarySourceDesignHold(ValueError):
    pass


def _derived_seed() -> tuple[int, str]:
    material = f"{SEED_DOMAIN}:{SEED_BINDING_SHA256}:seed".encode("ascii")
    full = hashlib.sha256(material).hexdigest()
    seed = int(full[:8], 16) % 2147483646 + 1
    return seed, full


def scout_repair_canary_source_design() -> dict[str, Any]:
    reviewed = design_review.scout_repair_experiment_design_review()
    if reviewed.get("experiment_namespace") != NAMESPACE:
        raise ScoutRepairCanarySourceDesignHold("namespace_drift")
    if reviewed.get("execution_authorized") is not False or reviewed.get("execution_performed") is not False:
        raise ScoutRepairCanarySourceDesignHold("design_carries_authority")
    seed, digest = _derived_seed()
    if seed == PAIR03_SEED or seed in GENERATION2_CAMPAIGN_SEEDS:
        raise ScoutRepairCanarySourceDesignHold("derived_seed_collides_with_historical_campaign")
    return {
        "schema": SCHEMA,
        "design_request_sha256": reviewed["request_sha256"],
        "experiment_namespace": NAMESPACE,
        "campaign_pair_slot": None,
        "held_out_campaign_space_used": False,
        "seed_derivation": {
            "domain": SEED_DOMAIN,
            "binding_sha256": SEED_BINDING_SHA256,
            "formula": "sha256(domain + ':' + binding_sha256 + ':seed')[:8] mod 2147483646 + 1",
            "full_material_sha256": digest,
            "seed": seed,
            "pair03_seed_reused": False,
            "generation2_campaign_seed_reused": False,
        },
        "arm_seed_binding": {
            "legacy_control": seed,
            "scout_repair_treatment": seed,
            "same_seed": True,
        },
        "opponent": {
            "source_identity": None,
            "implementation": None,
            "model_backed": False,
            "deterministic_required": True,
            "same_for_both_arms": True,
        },
        "accepted_main_head_with_repair": None,
        "runtime_image_identity": None,
        "attempt_directory": None,
        "attempt_guard_source_identity": None,
        "invocation_source_identities": None,
        "post_run_evidence_contract": None,
        "execution_authorized": False,
        "execution_performed": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute_canary(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairCanarySourceDesignHold(NEXT_GATE)
