from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_invocation_generation2
    as invocation,
)

HEAD = "a" * 40
TREE = "b" * 40
SELF_SHA = "c" * 64
HOLD = invocation.Pair06V8BaselineLoadInvocationHold


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path / "claims"
    monkeypatch.setattr(invocation, "ATTEMPT_ROOT", root)

    events = []
    calls = []

    monkeypatch.setattr(
        invocation,
        "_check_python",
        lambda: events.append("python"),
    )
    monkeypatch.setattr(
        invocation,
        "_verify_self",
        lambda expected: (
            events.append("source")
            or (
                expected
                if expected == SELF_SHA
                else (_ for _ in ()).throw(HOLD("source"))
            )
        ),
    )

    def current(expected):
        events.append("main")
        if expected != HEAD:
            raise HOLD("head")
        return {"head": HEAD, "tree": TREE}

    monkeypatch.setattr(invocation, "_current_main", current)
    monkeypatch.setattr(
        invocation,
        "_fresh_preflight",
        lambda: (
            events.append("preflight")
            or {
                "runtime_environment": {"validated": True},
                "runtime_assets": {
                    "verified_file_count": 17,
                    "model_dir": str(invocation.MODEL_DIR),
                    "adapter_dir": str(invocation.ADAPTER_DIR),
                },
            }
        ),
    )

    def load(**kwargs):
        events.append("load")
        calls.append(kwargs)
        assert kwargs["pair_slot"] == 6
        assert kwargs["arm"] == "baseline"
        assert kwargs["runtime_load_authorized"] is True
        assert kwargs["authority_check"](6, "baseline") is True
        assert kwargs["authority_check"](6, "candidate") is False
        assert kwargs["authority_check"](15, "baseline") is False
        return SimpleNamespace(model=object(), tokenizer=object())

    monkeypatch.setattr(invocation.capability, "load_pair06_v8_runtime", load)
    return SimpleNamespace(root=root, events=events, calls=calls)


def invoke(**overrides):
    return invocation.execute_pair06_baseline_load(
        **{
            "expected_main_head": HEAD,
            "expected_invocation_source_sha256": SELF_SHA,
            "authorization_accepted": True,
            "confirm": invocation.CONFIRM_TOKEN,
            **overrides,
        }
    )


def test_contract_is_implemented_but_nonexecuting():
    out = invocation.pair06_v8_baseline_load_invocation_contract()
    assert out["pair06_v8_baseline_load_invocation_implemented"] is True
    assert out["pair06_v8_baseline_load_invocation_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["runtime_load_authorized_by_reviewed_dependency"] is True
    assert out["single_use_attempt_consumed"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False
    assert out["automatic_retry"] is False


def test_success_claims_before_load_and_writes_noninference_result(env):
    out = invoke()

    marker = env.root / invocation.MARKER_NAME
    result = env.root / invocation.RESULT_NAME
    assert marker.is_file()
    assert result.is_file()
    assert len(env.calls) == 1
    assert env.events.index("preflight") < env.events.index("load")
    assert out["runtime_load_authorized"] is True
    assert out["runtime_load_performed"] is True
    assert out["model_weights_loaded"] is True
    assert out["model_inference_authorized"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_authorized"] is False
    assert out["game_execution_performed"] is False
    assert out["automatic_retry"] is False
    assert len(out["result_file_sha256"]) == 64


def test_second_invocation_cannot_reuse_successful_attempt(env):
    invoke()
    with pytest.raises(HOLD, match="PRIOR_RESULT_PRESENT"):
        invoke()
    assert len(env.calls) == 1


def test_loader_failure_preserves_claim_and_blocks_retry(env, monkeypatch):
    def fail(**kwargs):
        env.events.append("load-fail")
        env.calls.append(kwargs)
        raise RuntimeError("inert load failure")

    monkeypatch.setattr(
        invocation.capability,
        "load_pair06_v8_runtime",
        fail,
    )
    with pytest.raises(RuntimeError, match="inert load failure"):
        invoke()

    marker = env.root / invocation.MARKER_NAME
    result = env.root / invocation.RESULT_NAME
    assert marker.is_file()
    assert not result.exists()

    with pytest.raises(HOLD, match="PRIOR_ATTEMPT_PRESENT"):
        invoke()
    assert len(env.calls) == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"authorization_accepted": False},
        {"authorization_accepted": 1},
        {"confirm": ""},
        {"confirm": "PAIR06"},
        {"expected_main_head": "A" * 40},
        {"expected_main_head": "a" * 39},
        {"expected_invocation_source_sha256": "x" * 64},
        {"expected_invocation_source_sha256": "c" * 63},
    ],
)
def test_invalid_inputs_stop_before_host_actions(tmp_path, monkeypatch, overrides):
    monkeypatch.setattr(invocation, "ATTEMPT_ROOT", tmp_path / "claims")

    def forbidden(*args, **kwargs):
        raise AssertionError("host action")

    monkeypatch.setattr(invocation, "_check_python", forbidden)
    monkeypatch.setattr(invocation, "_verify_self", forbidden)
    monkeypatch.setattr(invocation, "_current_main", forbidden)
    monkeypatch.setattr(invocation, "_fresh_preflight", forbidden)

    with pytest.raises(HOLD):
        invoke(**overrides)

    assert not (tmp_path / "claims").exists()


def test_revocation_before_claim_consumes_nothing(env):
    env.root.mkdir(parents=True)
    (env.root / invocation.REVOCATION_NAME).write_text("revoke\n", encoding="utf-8")

    with pytest.raises(HOLD, match="REVOKED"):
        invoke()

    assert not (env.root / invocation.MARKER_NAME).exists()
    assert env.calls == []


def test_revocation_after_claim_blocks_capability_authority_callback(
    env,
    monkeypatch,
):
    original_write = invocation._write_create_only

    def write(path, value):
        digest = original_write(path, value)
        if path.name == invocation.MARKER_NAME:
            (env.root / invocation.REVOCATION_NAME).write_text(
                "revoke\n",
                encoding="utf-8",
            )
        return digest

    monkeypatch.setattr(invocation, "_write_create_only", write)

    with pytest.raises(HOLD, match="REVOKED"):
        invoke()

    assert (env.root / invocation.MARKER_NAME).is_file()
    assert not (env.root / invocation.RESULT_NAME).exists()
    assert env.calls == []


def test_claim_root_is_private_directory(tmp_path, monkeypatch):
    root = tmp_path / "claims"
    monkeypatch.setattr(invocation, "ATTEMPT_ROOT", root)
    out = invocation._claims_root()
    assert out == root
    assert (root.stat().st_mode & 0o777) == 0o700


def test_next_gate_is_separate_source_binding_review():
    out = invocation.pair06_v8_baseline_load_invocation_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v8_baseline_runtime_load_invocation_review"
    )
