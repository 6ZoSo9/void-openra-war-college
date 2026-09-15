"""Precommitted Abaddon Generation-2 campaign candidate 252 and pair ledger.

This is a parallel frozen plan. It does not modify or generalize the
Generation-1 planner and does not authorize runtime execution.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .apollyon_opponent_runtime_realizations import (
    reviewed_opponent_runtime_realizations,
)
from .apollyon_opponent_snapshots import reviewed_snapshot_set

PLAN_SCHEMA = "void.abaddon.policy-campaign-plan.v1"
SEED_SCHEMA = "void.abaddon.policy-campaign-seed-derivation.v1"

CANDIDATE_FIXTURE_REL = (
    "fixtures/learning/abaddon-policy-genome-generation-2-candidate-252.json"
)
PLAN_FIXTURE_REL = (
    "fixtures/learning/abaddon-policy-campaign-generation-2-candidate-252-plan.json"
)

CONTROLLER_SOURCE_SHA256 = (
    "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
)
REFINER_SOURCE_SHA256 = (
    "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
)
PARENT_GENOME_SHA256 = (
    "3c4346e0c92ea7225425d9ff4fd7ae12daa44162b06d471530179325b7d38a26"
)
CANDIDATE_GENOME_SHA256 = (
    "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
)
CANDIDATE_FIXTURE_SHA256 = (
    "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
)
PLAN_FIXTURE_SHA256 = "9a50b8100d33a6ae08578e5ef6e9bf59d5bd8edc537ed44853f3d8eca8bbb4e0"
PLAN_INTERNAL_SHA256 = "64e5003fa0d339ea1bea14eb0e4026e0dfe3455e86f38ef0fb9c0a26fbc4c594"
SNAPSHOT_SET_SHA256 = "d7bfce0cb1456ec440f6ab362c781057837c3912c557f865ae95b7ddc6278526"
RUNTIME_REALIZATION_SET_SHA256 = "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"

EXPECTED_SEEDS = (
    1990061685,
    208354846,
    1496195137,
    331379205,
    905645055,
    411746275,
)

EXPECTED_MUTATIONS = (
    {
        "doctrine": "FEINTER",
        "key": "group",
        "old": 4,
        "new": 3,
    },
    {
        "doctrine": "FEINTER",
        "key": "scout_history_min",
        "old": 16,
        "new": 20,
    },
)


class CampaignPlanGeneration2Error(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CampaignPlanGeneration2Error(message)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _file_sha256(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise CampaignPlanGeneration2Error(f"missing or symlinked fixture: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise CampaignPlanGeneration2Error(f"invalid JSON fixture: {path}") from exc
    _require(isinstance(value, dict), f"fixture must be object: {path}")
    return value


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _genome_digest(genome: dict[str, Any]) -> str:
    body = dict(genome)
    body.pop("genome_sha256", None)
    return hashlib.sha256(_stable_bytes(body)).hexdigest()


def _plan_digest(plan: dict[str, Any]) -> str:
    body = dict(plan)
    body.pop("plan_sha256", None)
    return hashlib.sha256(_stable_bytes(body)).hexdigest()


def derive_seed(seed_index: int) -> int:
    _require(
        type(seed_index) is int and 0 <= seed_index < len(EXPECTED_SEEDS),
        "seed index out of reviewed range",
    )
    raw = (
        "void.abaddon.policy-campaign.v1:"
        + CANDIDATE_GENOME_SHA256
        + ":"
        + str(seed_index)
    ).encode("utf-8")
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "big") % 2147483646 + 1


def validate_candidate_fixture() -> dict[str, Any]:
    path = _repo_root() / CANDIDATE_FIXTURE_REL
    _require(
        _file_sha256(path) == CANDIDATE_FIXTURE_SHA256,
        "candidate fixture file SHA-256 drift",
    )
    candidate = _load_json(path)
    _require(candidate.get("schema") == "void.abaddon.policy-genome.v1", "candidate schema drift")
    _require(candidate.get("identity") == "Abaddon", "candidate identity drift")
    _require(candidate.get("generation") == 2, "candidate generation drift")
    _require(candidate.get("candidate_index") == 252, "candidate index drift")
    _require(candidate.get("controller_version") == 1, "candidate controller version drift")
    _require(
        candidate.get("source") == "bounded_deterministic_mutation",
        "candidate source drift",
    )
    _require(
        candidate.get("parent_genome_sha256") == PARENT_GENOME_SHA256,
        "candidate parent genome drift",
    )
    _require(
        candidate.get("genome_sha256") == CANDIDATE_GENOME_SHA256,
        "candidate genome identity drift",
    )
    _require(
        _genome_digest(candidate) == CANDIDATE_GENOME_SHA256,
        "candidate semantic genome digest mismatch",
    )
    _require(
        tuple(candidate.get("mutations") or ()) == EXPECTED_MUTATIONS,
        "candidate mutation set drift",
    )
    return candidate


def _snapshot_index() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    snapshot_set = reviewed_snapshot_set()
    _require(
        snapshot_set.get("snapshot_set_sha256") == SNAPSHOT_SET_SHA256,
        "opponent snapshot-set SHA-256 drift",
    )
    rows = snapshot_set.get("snapshots")
    _require(isinstance(rows, list), "opponent snapshots missing")
    by_id = {
        str(row["snapshot_id"]): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("snapshot_id"), str)
    }
    expected = {
        "apollyon-v13-v14-promoted",
        "apollyon-v13-v10-promoted",
        "apollyon-v2r13-qualified-predecessor",
        "apollyon-v3-v8-accepted-model-control",
    }
    _require(set(by_id) == expected, "reviewed opponent snapshot identities drifted")
    return snapshot_set, by_id


def _computed_plan() -> dict[str, Any]:
    validate_candidate_fixture()
    snapshot_set, by_id = _snapshot_index()
    realizations = reviewed_opponent_runtime_realizations()
    _require(
        realizations["realization_set_sha256"] == RUNTIME_REALIZATION_SET_SHA256,
        "runtime realization-set SHA drift",
    )
    _require(
        realizations["opponent_runtime_realization_complete"] is True,
        "opponent runtime realization incomplete",
    )

    for index, expected in enumerate(EXPECTED_SEEDS):
        _require(derive_seed(index) == expected, f"seed derivation drift at index {index}")

    pair_slots: list[dict[str, Any]] = []
    pair_slot = 1
    for seed_index, seed in enumerate(EXPECTED_SEEDS):
        historical_id = (
            "apollyon-v2r13-qualified-predecessor"
            if seed_index % 2 == 0
            else "apollyon-v3-v8-accepted-model-control"
        )
        for opponent_id in (
            "apollyon-v13-v14-promoted",
            "apollyon-v13-v10-promoted",
            historical_id,
        ):
            opponent = by_id[opponent_id]
            pair_slots.append({
                "abaddon_doctrine": "FEINTER",
                "baseline_arm": {
                    "abaddon_genome_sha256": PARENT_GENOME_SHA256,
                    "arm": "champion_baseline",
                    "candidate_fixture_sha256": None,
                    "policy_source": "controller_defaults",
                },
                "candidate_arm": {
                    "abaddon_genome_sha256": CANDIDATE_GENOME_SHA256,
                    "arm": "generation_2_candidate_252",
                    "candidate_fixture_sha256": CANDIDATE_FIXTURE_SHA256,
                    "policy_source": "bounded_deterministic_mutation",
                },
                "execution_state": "NOT_EXECUTED",
                "held_out": seed_index >= 4,
                "opponent_role": opponent["role"],
                "opponent_snapshot_id": opponent_id,
                "opponent_snapshot_sha256": opponent["snapshot_sha256"],
                "pair_binding": {
                    "same_abaddon_doctrine": True,
                    "same_opponent_snapshot": True,
                    "same_round_limit": True,
                    "same_seed": True,
                    "same_ticks_per_round": True,
                    "same_warm_start_contract_required": True,
                },
                "pair_slot": pair_slot,
                "rounds": 36,
                "seed": seed,
                "staging_max_ticks": 800,
                "starter_infantry": 4,
                "ticks_per_round": 25,
            })
            pair_slot += 1

    return {
        "authority": {
            "automatic_corpus_admission": False,
            "automatic_policy_promotion": False,
            "deployment": False,
            "game_started": False,
            "model_execution": False,
            "training": False,
            "weights_updated": False,
        },
        "candidate": {
            "candidate_fixture_path": CANDIDATE_FIXTURE_REL,
            "candidate_fixture_sha256": CANDIDATE_FIXTURE_SHA256,
            "candidate_frozen_before_campaign_evidence": True,
            "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
            "candidate_index": 252,
            "controller_source_sha256": CONTROLLER_SOURCE_SHA256,
            "generation": 2,
            "parent_genome_sha256": PARENT_GENOME_SHA256,
            "refiner_source_sha256": REFINER_SOURCE_SHA256,
            "target_doctrine": "FEINTER",
        },
        "execution_eligible": False,
        "opponent_runtime_realization_set_sha256": realizations["realization_set_sha256"],
        "opponent_snapshot_set_sha256": snapshot_set["snapshot_set_sha256"],
        "pair_slots": pair_slots,
        "pre_execution_gates": {
            "campaign_attempt_ledger_complete": True,
            "candidate_frozen_before_campaign_evidence": True,
            "opponent_runtime_realization_complete": True,
            "opponent_snapshot_source_binding_complete": True,
            "pair_arms_precommitted": True,
            "previous_champion_binding_complete": True,
            "runtime_execution_authorized": False,
        },
        "reasons": ["RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"],
        "schema": PLAN_SCHEMA,
        "seed_derivation": {
            "formula": (
                'sha256("void.abaddon.policy-campaign.v1:'
                '<candidate_genome_sha256>:<zero_based_seed_index>")[:8] '
                "mod 2147483646 + 1"
            ),
            "held_out_seed_indices": [4, 5],
            "schema": SEED_SCHEMA,
            "seeds": list(EXPECTED_SEEDS),
        },
        "summary": {
            "baseline_execution_count": 18,
            "candidate_execution_count": 18,
            "current_promoted_pair_slots": 6,
            "held_out_eventual_game_executions": 12,
            "held_out_pair_slot_count": 6,
            "opponent_snapshot_count": 4,
            "pair_slot_count": 18,
            "previous_promoted_champion_pair_slots": 6,
            "prior_accepted_model_control_pair_slots": 3,
            "prior_qualified_predecessor_pair_slots": 3,
            "total_eventual_game_executions": 36,
            "unique_seed_count": 6,
        },
    }


def precommitted_campaign_plan() -> dict[str, Any]:
    computed = _computed_plan()
    computed["plan_sha256"] = _plan_digest(computed)
    _require(
        computed["plan_sha256"] == PLAN_INTERNAL_SHA256,
        "computed campaign plan digest drift",
    )

    path = _repo_root() / PLAN_FIXTURE_REL
    _require(
        _file_sha256(path) == PLAN_FIXTURE_SHA256,
        "campaign plan fixture file SHA-256 drift",
    )
    fixture = _load_json(path)
    _require(
        fixture.get("plan_sha256") == PLAN_INTERNAL_SHA256,
        "campaign plan fixture internal digest drift",
    )
    _require(
        _plan_digest(fixture) == PLAN_INTERNAL_SHA256,
        "campaign plan internal hash mismatch",
    )
    _require(fixture == computed, "campaign plan fixture differs from computed precommit")
    return fixture
