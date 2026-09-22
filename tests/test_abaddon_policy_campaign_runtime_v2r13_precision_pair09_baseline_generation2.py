from __future__ import annotations

import pytest

from tools import (
    abaddon_policy_campaign_runtime_v2r13_precision_pair09_baseline_generation2
    as cli,
)


def test_cli_pins_exact_invocation_source():
    assert cli.INVOCATION_SOURCE_SHA256 == (
        "1920cf9892f0962cd7b14b12db7848eda7d45552c3b43ef96ba2cb5b68c2cd4a"
    )
    assert cli.AUTHORIZATION_TOKEN == (
        "VOID_ABADDON_GENERATION2_V2R13_AUTHORIZE_PAIR09_BASELINE_ONCE"
    )


def test_wrong_authorization_never_calls_invocation(monkeypatch, capsys):
    called = False

    def forbidden(**kwargs):
        nonlocal called
        called = True
        raise AssertionError("invocation reached")

    monkeypatch.setattr(
        cli.invocation,
        "execute_pair09_baseline",
        forbidden,
    )

    rc = cli.main(
        [
            "--expected-main-head",
            "a" * 40,
            "--authorization",
            "wrong",
            "--confirm",
            cli.invocation.CONFIRM_TOKEN,
        ]
    )
    assert rc == 2
    assert called is False
    captured = capsys.readouterr()
    assert "PAIR09_BASELINE_SPECIFIC_AUTHORIZATION_REQUIRED" in captured.err


def test_exact_authorization_dispatches_only_reviewed_arguments(
    monkeypatch,
    capsys,
):
    calls = []

    def execute(**kwargs):
        calls.append(kwargs)
        return {
            "pair09_baseline_execution_performed": True,
            "result_file": "/tmp/inert-result.json",
            "result_file_sha256": "d" * 64,
        }

    monkeypatch.setattr(
        cli.invocation,
        "execute_pair09_baseline",
        execute,
    )

    rc = cli.main(
        [
            "--expected-main-head",
            "a" * 40,
            "--authorization",
            cli.AUTHORIZATION_TOKEN,
            "--confirm",
            cli.invocation.CONFIRM_TOKEN,
        ]
    )

    assert rc == 0
    assert calls == [
        {
            "expected_main_head": "a" * 40,
            "expected_invocation_source_sha256": (
                cli.INVOCATION_SOURCE_SHA256
            ),
            "authorization_accepted": True,
            "confirm": cli.invocation.CONFIRM_TOKEN,
        }
    ]

    captured = capsys.readouterr()
    assert cli.MARK in captured.out
    assert "pair_slot=9" in captured.out
    assert "arm=baseline" in captured.out
    assert "single_use_attempt=true" in captured.out
    assert "automatic_retry=false" in captured.out
    assert "pair09_candidate_execution=false" in captured.out
    assert f"{cli.MARK}_GREEN" in captured.out


def test_invocation_hold_returns_nonzero(monkeypatch, capsys):
    def hold(**kwargs):
        raise RuntimeError("inert-hold")

    monkeypatch.setattr(
        cli.invocation,
        "execute_pair09_baseline",
        hold,
    )

    rc = cli.main(
        [
            "--expected-main-head",
            "a" * 40,
            "--authorization",
            cli.AUTHORIZATION_TOKEN,
            "--confirm",
            cli.invocation.CONFIRM_TOKEN,
        ]
    )
    assert rc == 2
    captured = capsys.readouterr()
    assert f"{cli.MARK}_HOLD" in captured.err
    assert "RuntimeError:inert-hold" in captured.err


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["--expected-main-head", "a" * 40],
        [
            "--expected-main-head",
            "a" * 40,
            "--authorization",
            cli.AUTHORIZATION_TOKEN,
        ],
    ],
)
def test_required_cli_fields_cannot_be_omitted(argv):
    with pytest.raises(SystemExit):
        cli.parse_args(argv)
