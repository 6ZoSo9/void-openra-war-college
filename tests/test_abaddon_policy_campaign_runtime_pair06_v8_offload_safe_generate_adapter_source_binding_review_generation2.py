from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_offload_safe_generate_adapter_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_adapter_source_and_test():
    out = review.pair06_v8_offload_safe_generate_adapter_review_contract()
    assert out["adapter_git_blob"] == "45f970eb4160bf6d3c5eafcbd74705eef8802121"
    assert out["adapter_source_sha256"] == (
        "f1a78fc386965f1108c6ae7ce1b94c870b7d21208bf9c9f336f9fb46eecc446d"
    )
    assert out["adapter_test_git_blob"] == "388aabe101bc319cc02e9ba1b91491272b3bcbd4"
    assert out["adapter_test_sha256"] == (
        "f53c6128c2bce961b09fda41bfd94a645671a326c20e397e4a599ff9b2ae3315"
    )


def test_review_confirms_offload_safe_input_placement_only():
    out = review.pair06_v8_offload_safe_generate_adapter_review_contract()
    assert out["pair06_v8_offload_safe_generate_adapter_reviewed"] is True
    assert out["accepted_v8_runtime_source_unchanged"] is True
    assert out["model_asset_bytes_unchanged"] is True
    assert out["tokenizer_asset_bytes_unchanged"] is True
    assert out["tool_translation_unchanged"] is True
    assert out["host_validation_unchanged"] is True
    assert out["generate_instance_method_only_replaced"] is True
    assert out["input_device_from_embedding_weight"] is True
    assert out["cpu_embedding_supported"] is True
    assert out["cuda_embedding_supported"] is True
    assert out["meta_embedding_rejected"] is True
    assert out["hard_coded_cuda_input_transfer_used"] is False


def test_review_grants_no_retry_or_execution_authority():
    out = review.pair06_v8_offload_safe_generate_adapter_review_contract()
    for field in (
        "model_load_authorized",
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
    out = review.pair06_v8_offload_safe_generate_adapter_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_SUPERVISOR_OFFLOAD_ADAPTER_BINDING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_SUPERVISOR_OFFLOAD_ADAPTER_BINDING_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8OffloadSafeGenerateReviewHold,
        match="PARENT_SUPERVISOR_OFFLOAD_ADAPTER_BINDING_REQUIRED",
    ):
        review.execute_or_retry()
