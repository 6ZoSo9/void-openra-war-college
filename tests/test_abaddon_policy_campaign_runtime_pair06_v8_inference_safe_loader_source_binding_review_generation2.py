from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_inference_safe_loader_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_loader_source_and_test():
    out = review.pair06_v8_inference_safe_loader_review_contract()
    assert out["loader_git_blob"] == "02edc92db7823270b521f7429730ee3de230db4e"
    assert out["loader_source_sha256"] == (
        "824d7e65e293ac8eb1a3e44bf33361a92fe806f268309556895be26baf9f962c"
    )
    assert out["loader_test_git_blob"] == "ae686f6d73faf85cebc5da6751808809ea1e815e"
    assert out["loader_test_sha256"] == (
        "2059a642b9c7e77060273a45ad35c11603359a92d9098bd02e0a5797e6b96118"
    )


def test_review_forbids_cpu_disk_meta_inference_placement():
    out = review.pair06_v8_inference_safe_loader_review_contract()
    assert out["pair06_v8_inference_safe_loader_reviewed"] is True
    assert out["device_map"] == {"": 0}
    assert out["offload_embedding"] is False
    assert out["cpu_embedding_offload_allowed"] is False
    assert out["cpu_parameter_offload_allowed"] is False
    assert out["disk_parameter_offload_allowed"] is False
    assert out["meta_parameter_allowed_after_load"] is False
    assert out["all_parameters_cuda0_required"] is True
    assert out["input_embedding_cuda0_required"] is True


def test_review_grants_no_execution_or_retry_authority():
    out = review.pair06_v8_inference_safe_loader_review_contract()
    for field in (
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "automatic_retry",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_parent_binding():
    out = review.pair06_v8_inference_safe_loader_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_SUPERVISOR_INFERENCE_SAFE_LOADER_BINDING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_SUPERVISOR_INFERENCE_SAFE_LOADER_BINDING_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8InferenceSafeLoaderReviewHold,
        match="PARENT_SUPERVISOR_INFERENCE_SAFE_LOADER_BINDING_REQUIRED",
    ):
        review.execute_or_retry()
