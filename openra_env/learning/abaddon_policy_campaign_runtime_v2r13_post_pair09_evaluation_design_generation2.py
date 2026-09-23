"""Source-only design after inconclusive pair-03 and pair-09 evaluations.

V2R13 currently exposes pair slots 3, 9, and 15. Pair 15 is explicitly held
out. Pair 03 and pair 09 are the available non-held-out evaluation slots and
both produced non-decisive matched baseline/candidate evidence.

This design therefore refuses to use pair 15 as a tuning tie-breaker. Further
candidate evaluation requires a newly reviewed non-held-out evaluation
allocation before any held-out evidence is observed.

No runtime execution, replay, held-out use, training, promotion, deployment,
VOID-chain mutation, wallet, or funds authority is granted.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_policy_disposition_source_binding_review_generation2
    as pair03_disposition_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_policy_disposition_source_binding_review_generation2
    as pair09_disposition_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as bounded_executor,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-post-pair09-evaluation-design-contract.v1"
)

PAIR03_DISPOSITION_REVIEW_GIT_BLOB = (
    "ff606911ce35499b0fd6d25eb10591fc80b0c338"
)
PAIR03_DISPOSITION_REVIEW_SOURCE_SHA256 = (
    "ab7fbc0be7b6f4a960d2a7f75f1ceeb6e111c6737a546e672098c74bb8c33fb9"
)
PAIR09_DISPOSITION_REVIEW_GIT_BLOB = (
    "21e87f2d594544886610cff2b5596c325a743494"
)
PAIR09_DISPOSITION_REVIEW_SOURCE_SHA256 = (
    "3bb506e3247f0116a960c38945766c8c340b15080890cf79c734ed6925afe21a"
)
BOUNDED_EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"

EXPECTED_AUTHORIZED_PAIR_SLOTS = (3, 9, 15)
EXPECTED_HELD_OUT_PAIR_SLOTS = (15,)
EXHAUSTED_NONHELDOUT_PAIR_SLOTS = (3, 9)

NEXT_GATE = "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_new_nonheldout_evaluation_allocation"


class V2R13PostPair09EvaluationDesignHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13PostPair09EvaluationDesignHold(message)


@lru_cache(maxsize=1)
def _pair03_cached() -> dict[str, Any]:
    contract = (
        pair03_disposition_review
        .v2r13_pair03_candidate_policy_disposition_review_contract()
    )
    _require(contract.get("pair_slot") == 3, "pair03 disposition slot drift")
    _require(
        contract.get("policy_disposition_reviewed") is True,
        "pair03 disposition not reviewed",
    )
    _require(
        contract.get("policy_disposition")
        == "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION",
        "pair03 disposition drift",
    )
    _require(
        contract.get("candidate_preserved_as_evidence") is True,
        "pair03 candidate not preserved",
    )
    _require(contract.get("candidate_promoted") is False, "pair03 candidate promoted")
    _require(contract.get("candidate_rejected") is False, "pair03 candidate rejected")
    _require(
        contract.get("held_out_execution_authorized") is False,
        "pair03 disposition authorized held-out execution",
    )
    return deepcopy(contract)


@lru_cache(maxsize=1)
def _pair09_cached() -> dict[str, Any]:
    contract = (
        pair09_disposition_review
        .v2r13_pair09_candidate_policy_disposition_review_contract()
    )
    _require(contract.get("pair_slot") == 9, "pair09 disposition slot drift")
    _require(
        contract.get("policy_disposition_reviewed") is True,
        "pair09 disposition not reviewed",
    )
    _require(
        contract.get("policy_disposition")
        == "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION",
        "pair09 disposition drift",
    )
    _require(
        contract.get("candidate_preserved_as_evidence") is True,
        "pair09 candidate not preserved",
    )
    _require(contract.get("candidate_promoted") is False, "pair09 candidate promoted")
    _require(contract.get("candidate_rejected") is False, "pair09 candidate rejected")
    _require(
        contract.get("additional_bounded_evaluation_required") is True,
        "pair09 additional evaluation requirement missing",
    )
    _require(
        contract.get("post_pair09_evaluation_design_required") is True,
        "pair09 post-evaluation design requirement missing",
    )
    _require(
        contract.get("held_out_execution_authorized") is False,
        "pair09 disposition authorized held-out execution",
    )
    _require(
        contract.get("next_gate") == "V2R13_POST_PAIR09_EVALUATION_DESIGN_REQUIRED",
        "pair09 disposition frontier drift",
    )
    return deepcopy(contract)


def v2r13_post_pair09_evaluation_design_contract() -> dict[str, Any]:
    pair03 = _pair03_cached()
    pair09 = _pair09_cached()

    _require(
        tuple(bounded_executor.AUTHORIZED_PAIR_SLOTS)
        == EXPECTED_AUTHORIZED_PAIR_SLOTS,
        "authorized V2R13 pair-slot set drift",
    )
    _require(
        tuple(bounded_executor.HELD_OUT_PAIR_SLOTS)
        == EXPECTED_HELD_OUT_PAIR_SLOTS,
        "held-out V2R13 pair-slot set drift",
    )

    nonheldout = tuple(
        slot
        for slot in bounded_executor.AUTHORIZED_PAIR_SLOTS
        if slot not in bounded_executor.HELD_OUT_PAIR_SLOTS
    )
    _require(
        nonheldout == EXHAUSTED_NONHELDOUT_PAIR_SLOTS,
        "non-held-out V2R13 pair-slot set drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "pair03_disposition_review_git_blob": (
            PAIR03_DISPOSITION_REVIEW_GIT_BLOB
        ),
        "pair03_disposition_review_source_sha256": (
            PAIR03_DISPOSITION_REVIEW_SOURCE_SHA256
        ),
        "pair09_disposition_review_git_blob": (
            PAIR09_DISPOSITION_REVIEW_GIT_BLOB
        ),
        "pair09_disposition_review_source_sha256": (
            PAIR09_DISPOSITION_REVIEW_SOURCE_SHA256
        ),
        "bounded_executor_git_blob": BOUNDED_EXECUTOR_GIT_BLOB,
        "post_pair09_evaluation_design_implemented": True,
        "post_pair09_evaluation_design_reviewed": False,
        "authorized_pair_slots": EXPECTED_AUTHORIZED_PAIR_SLOTS,
        "held_out_pair_slots": EXPECTED_HELD_OUT_PAIR_SLOTS,
        "nonheldout_pair_slots": EXHAUSTED_NONHELDOUT_PAIR_SLOTS,
        "completed_nondeci­sive_nonheldout_pair_slots": (
            EXHAUSTED_NONHELDOUT_PAIR_SLOTS
        ),
        "existing_nonheldout_capacity_exhausted": True,
        "held_out_pair15_preserved": True,
        "held_out_contamination_prohibited": True,
        "held_out_use_as_tuning_tiebreaker_allowed": False,
        "new_nonheldout_evaluation_allocation_required": True,
        "new_nonheldout_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair15_execution_performed": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "candidate_promoted": False,
        "candidate_rejected": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "pair03_disposition_review": deepcopy(pair03),
        "pair09_disposition_review": deepcopy(pair09),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_pair15(*args: Any, **kwargs: Any) -> None:
    raise V2R13PostPair09EvaluationDesignHold(
        "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED"
    )


def replay_existing_pair(*args: Any, **kwargs: Any) -> None:
    raise V2R13PostPair09EvaluationDesignHold(
        "V2R13_EXISTING_PAIR_REPLAY_NOT_AUTHORIZED"
    )


def promote_or_train_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13PostPair09EvaluationDesignHold(
        "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED"
    )
