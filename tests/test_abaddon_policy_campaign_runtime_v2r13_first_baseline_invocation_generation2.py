from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2
    as invocation,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2.py"
)
CLI = (
    REPO
    / "tools/"
    "abaddon_policy_campaign_runtime_v2r13_precision_first_baseline_generation2.py"
)


def test_contract_is_exactly_pair03_baseline_only():
    out = invocation.first_baseline_invocation_contract()
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["candidate_arm_implemented_by_this_source"] is False
    assert out["held_out_arm_implemented_by_this_source"] is False
    assert out["automatic_retry"] is False


def test_contract_requires_current_preflight_cached_sudo_and_revocation_check():
    out = invocation.first_baseline_invocation_contract()
    assert out["execution_requires_current_main_preflight"] is True
    assert out["execution_requires_cached_sudo_authority"] is True
    assert out["execution_requires_revocation_sentinel_absent"] is True
    assert out["execution_requires_isolated_grpc_python"] is True
    assert out["restricted_git_worktree_backend_implemented"] is True


def test_contract_requires_fresh_readiness_before_inference():
    out = invocation.first_baseline_invocation_contract()
    assert out["fresh_canonical_live_readiness_before_inference_implemented"] is True
    assert out["exact_v2r13_model_preload_before_readiness_implemented"] is True
    assert out["model_preload_uses_empty_generate_prompt"] is True
    assert out["model_preload_requires_empty_response_text"] is True
    assert out["model_preload_token_evaluation_forbidden"] is True
    assert out["model_preload_inference_performed"] is False
    assert (
        out["fresh_worktree_observation_from_materialization_path_record_implemented"]
        is True
    )
    assert out["materialization_receipt_direct_worktree_admission"] is False
    assert out["fresh_worktree_observation_uses_explicit_host_lstat_backend"] is True
    assert out["fresh_worktree_observation_uses_reviewed_git_backend"] is True
    assert out["fresh_worktree_observation_uses_reviewed_path_resolver"] is True
    assert out["fresh_readiness_uses_reviewed_ollama_http_backend"] is True
    assert out["fresh_readiness_uses_reviewed_rootless_docker_backend"] is True


def test_contract_preserves_nontraining_nonpromotion_authority():
    out = invocation.first_baseline_invocation_contract()
    assert out["runtime_execution_authorized"] is True
    assert out["runtime_execution_performed_by_contract_inspection"] is False
    assert out["model_inference_performed_by_contract_inspection"] is False
    assert out["game_execution_performed_by_contract_inspection"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_exact_confirmation_token_is_required():
    invocation._validate_confirmation(invocation.CONFIRM_TOKEN)
    with pytest.raises(
        invocation.V2R13FirstBaselineInvocationHold,
        match="FIRST_BASELINE_EXECUTION_CONFIRMATION_REQUIRED",
    ):
        invocation._validate_confirmation("wrong")


@pytest.mark.parametrize(
    "args",
    [
        ("rev-parse", "HEAD"),
        ("rev-parse", "--verify", "a" * 40 + "^{commit}"),
        ("status", "--porcelain", "--untracked-files=all"),
        ("symbolic-ref", "-q", "HEAD"),
        ("worktree", "list", "--porcelain"),
        (
            "worktree",
            "add",
            "--detach",
            str(invocation.ARM_ROOT / "frozen-source"),
            "a" * 40,
        ),
        (
            "worktree",
            "remove",
            str(invocation.ARM_ROOT / "frozen-source"),
        ),
    ],
)
def test_reviewed_git_shapes_are_accepted(args):
    invocation._validate_git_args(args)


@pytest.mark.parametrize(
    "args",
    [
        ("fetch", "origin"),
        ("push", "origin", "main"),
        ("checkout", "main"),
        ("reset", "--hard", "HEAD"),
        ("clean", "-fdx"),
        ("worktree", "add", "--force", "/tmp/x", "a" * 40),
        ("worktree", "remove", "--force", "/tmp/x"),
    ],
)
def test_unreviewed_git_mutations_are_rejected(args):
    with pytest.raises(invocation.V2R13FirstBaselineInvocationHold):
        invocation._validate_git_args(args)


def test_worktree_destination_cannot_escape_pair03_baseline_root():
    with pytest.raises(
        invocation.V2R13FirstBaselineInvocationHold,
        match="escaped pair-03 baseline root",
    ):
        invocation._validate_git_args(
            ("worktree", "add", "--detach", "/tmp/frozen-source", "a" * 40)
        )


def test_source_contains_exact_reviewed_execution_composition():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    names = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert "execute_v2r13_arm" in names
    assert "collect_v2r13_canonical_live_collection" in names
    assert "validate_bound_canonical_live_collection_entrypoint_receipt" in names
    assert "validate_host_preflight_snapshot" in names


def test_source_does_not_implement_training_or_promotion_calls():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
    forbidden = {
        "train",
        "fit",
        "backward",
        "optimizer_step",
        "promote",
        "deploy",
        "broadcast_transaction",
    }
    assert not (called & forbidden)


def test_cli_is_fixed_to_one_confirmation_argument():
    text = CLI.read_text(encoding="utf-8")
    assert "--confirm" in text
    assert "--pair-slot" not in text
    assert "--arm" not in text


def test_invocation_advances_to_execution_evidence_acceptance():
    assert invocation.NEXT_GATE == (
        "V2R13_PAIR03_BASELINE_EXECUTION_EVIDENCE_ACCEPTANCE_REQUIRED"
    )
    assert invocation.NEXT_CHANGE_CLASS == (
        "source_only_v2r13_pair03_baseline_execution_evidence_acceptance"
    )


def test_fresh_readiness_converts_materialization_to_worktree_observation(monkeypatch):
    materialization = {
        "path_input_record": {"sentinel": "exact-materialized-path-record"},
        "materialization_performed": True,
    }
    observed = {
        "schema": "test-worktree-observation",
        "sentinel": "observer-receipt",
    }
    calls = {}

    def fake_observe(
        record,
        *,
        observation_authorized,
        lstat_path,
        run_git,
        resolve_path,
    ):
        calls["record"] = record
        calls["observation_authorized"] = observation_authorized
        calls["lstat_path"] = lstat_path
        calls["run_git"] = run_git
        calls["resolve_path"] = resolve_path
        return observed

    def fake_validate(receipt):
        calls["validated_receipt"] = receipt
        return {"receipt_valid": True}

    def fake_collect(**kwargs):
        calls["live_worktree_receipt"] = kwargs["worktree_receipt"]
        calls["portable_binding_attestation"] = kwargs[
            "portable_binding_attestation"
        ]
        return {
            "activation_evidence": {"snapshot_id": "V2R13-test"},
        }

    def fake_entrypoint_validate(receipt, *, entrypoint_source_sha256):
        calls["entrypoint_receipt"] = receipt
        calls["entrypoint_source_sha256"] = entrypoint_source_sha256
        return {
            "bound_entrypoint_receipt_valid": True,
            "canonical_live_collection_path_complete": True,
            "runtime_readiness_admitted": True,
            "runtime_execution_authorized": False,
        }

    monkeypatch.setattr(
        invocation,
        "_preload_exact_v2r13_model",
        lambda: {
            "model_load_performed": True,
            "model_inference_performed": False,
        },
    )
    monkeypatch.setattr(
        invocation.worktree_observer,
        "observe_v2r13_worktrees",
        fake_observe,
    )
    monkeypatch.setattr(
        invocation.worktree_observer,
        "validate_v2r13_worktree_observation",
        fake_validate,
    )
    monkeypatch.setattr(
        invocation.live_entrypoint,
        "collect_v2r13_canonical_live_collection",
        fake_collect,
    )
    monkeypatch.setattr(
        invocation.live_entrypoint_binding,
        "validate_bound_canonical_live_collection_entrypoint_receipt",
        fake_entrypoint_validate,
    )

    evidence = invocation._fresh_readiness_provider(
        {
            "materialization_receipt": materialization,
            "portable_binding_attestation": {"portable": True},
        }
    )

    assert calls["record"] is materialization["path_input_record"]
    assert calls["observation_authorized"] is True
    assert calls["lstat_path"] is invocation.os.lstat
    assert calls["run_git"] is invocation.runtime_observers.host_git_runner
    assert calls["resolve_path"] is invocation.runtime_observers.host_path_resolver
    assert calls["validated_receipt"] is observed
    assert calls["live_worktree_receipt"] is observed
    assert calls["live_worktree_receipt"] is not materialization
    assert calls["portable_binding_attestation"] == {"portable": True}
    assert evidence == {"snapshot_id": "V2R13-test"}


def test_source_explicitly_observes_worktrees_before_live_readiness():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    names = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert "observe_v2r13_worktrees" in names
    assert "validate_v2r13_worktree_observation" in names


class _FakePreloadResponse:
    def __init__(self, payload, status=200):
        self._payload = payload
        self._status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def getcode(self):
        return self._status

    def read(self, maximum_bytes):
        raw = invocation.json.dumps(
            self._payload,
            sort_keys=True,
        ).encode("utf-8")
        assert len(raw) <= maximum_bytes
        return raw


def test_model_preload_is_empty_prompt_load_without_inference(monkeypatch):
    captured = {}

    def fake_urlopen(request, *, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["timeout"] = timeout
        captured["payload"] = invocation.json.loads(request.data.decode("utf-8"))
        return _FakePreloadResponse(
            {
                "model": invocation.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                "response": "",
                "done": True,
                "done_reason": "load",
            }
        )

    monkeypatch.setattr(invocation.urllib.request, "urlopen", fake_urlopen)
    receipt = invocation._preload_exact_v2r13_model()

    assert captured["url"] == invocation.OLLAMA_PRELOAD_URL
    assert captured["method"] == "POST"
    assert captured["timeout"] == invocation.OLLAMA_PRELOAD_TIMEOUT_SECONDS
    assert captured["payload"] == {
        "model": invocation.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
        "prompt": "",
        "keep_alive": invocation.OLLAMA_PRELOAD_KEEP_ALIVE,
        "stream": False,
    }
    assert receipt["model_load_performed"] is True
    assert receipt["model_inference_performed"] is False
    assert receipt["response_text_empty"] is True
    assert receipt["token_evaluation_performed"] is False


@pytest.mark.parametrize(
    "payload, pattern",
    [
        (
            {
                "model": invocation.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                "response": "generated text",
                "done": True,
            },
            "generated response text",
        ),
        (
            {
                "model": invocation.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                "response": "",
                "done": True,
                "eval_count": 1,
            },
            "unexpectedly evaluated tokens",
        ),
        (
            {
                "model": invocation.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                "response": "",
                "done": True,
                "prompt_eval_count": 1,
            },
            "unexpectedly evaluated tokens",
        ),
    ],
)
def test_model_preload_rejects_inference_signals(monkeypatch, payload, pattern):
    monkeypatch.setattr(
        invocation.urllib.request,
        "urlopen",
        lambda request, *, timeout: _FakePreloadResponse(payload),
    )
    with pytest.raises(invocation.V2R13FirstBaselineInvocationHold, match=pattern):
        invocation._preload_exact_v2r13_model()


def test_fresh_readiness_preloads_before_live_collection(monkeypatch):
    order = []
    materialization = {
        "path_input_record": {"sentinel": "paths"},
        "materialization_performed": True,
    }

    monkeypatch.setattr(
        invocation,
        "_preload_exact_v2r13_model",
        lambda: (
            order.append("preload")
            or {
                "model_load_performed": True,
                "model_inference_performed": False,
            }
        ),
    )
    monkeypatch.setattr(
        invocation.worktree_observer,
        "observe_v2r13_worktrees",
        lambda *args, **kwargs: order.append("worktree") or {"observer": True},
    )
    monkeypatch.setattr(
        invocation.worktree_observer,
        "validate_v2r13_worktree_observation",
        lambda receipt: {"receipt_valid": True},
    )
    monkeypatch.setattr(
        invocation.live_entrypoint,
        "collect_v2r13_canonical_live_collection",
        lambda **kwargs: order.append("live") or {
            "activation_evidence": {"snapshot_id": "V2R13-test"},
        },
    )
    monkeypatch.setattr(
        invocation.live_entrypoint_binding,
        "validate_bound_canonical_live_collection_entrypoint_receipt",
        lambda receipt, *, entrypoint_source_sha256: {
            "bound_entrypoint_receipt_valid": True,
            "canonical_live_collection_path_complete": True,
            "runtime_readiness_admitted": True,
            "runtime_execution_authorized": False,
        },
    )

    invocation._fresh_readiness_provider(
        {
            "materialization_receipt": materialization,
            "portable_binding_attestation": {"portable": True},
        }
    )
    assert order == ["preload", "worktree", "live"]
