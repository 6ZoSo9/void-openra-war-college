from __future__ import annotations

from copy import deepcopy

from tools import (
    abaddon_policy_campaign_runtime_v2r13_precision_pair03_candidate_generation2
    as cli,
)


def test_cli_pins_reviewed_invocation_source_sha():
    assert cli.INVOCATION_SOURCE_SHA256 == (
        "1df36c53c6e7d1f6ff07f732e792e6fdcaab7a8d0d5b9d8249851b78e11202c0"
    )


def test_cli_dispatches_exact_pair03_candidate_arguments(monkeypatch, capsys):
    calls = []

    def execute(**kwargs):
        calls.append(deepcopy(kwargs))
        return {
            "candidate_execution_performed": True,
            "result_file": "/tmp/inert-result.json",
            "result_file_sha256": "a" * 64,
        }

    monkeypatch.setattr(cli.invocation, "execute_pair03_candidate", execute)
    rc = cli.main(
        [
            "--expected-main-head",
            "b" * 40,
            "--confirm",
            cli.invocation.CONFIRM_TOKEN,
        ]
    )
    assert rc == 0
    assert calls == [
        {
            "expected_main_head": "b" * 40,
            "expected_invocation_source_sha256": cli.INVOCATION_SOURCE_SHA256,
            "confirm": cli.invocation.CONFIRM_TOKEN,
        }
    ]
    out = capsys.readouterr()
    assert f"{cli.MARK}_GREEN" in out.out
    assert "pair_slot=3" in out.out
    assert "arm=candidate" in out.out
    assert "automatic_retry=false" in out.out
    assert "policy_promotion=false" in out.out
    assert "wallet_or_funds_action=false" in out.out


def test_cli_hold_returns_two_and_does_not_claim_success(monkeypatch, capsys):
    def execute(**kwargs):
        raise RuntimeError("inert hold")

    monkeypatch.setattr(cli.invocation, "execute_pair03_candidate", execute)
    rc = cli.main(
        [
            "--expected-main-head",
            "c" * 40,
            "--confirm",
            cli.invocation.CONFIRM_TOKEN,
        ]
    )
    assert rc == 2
    out = capsys.readouterr()
    assert f"{cli.MARK}_HOLD" in out.err
    assert f"{cli.MARK}_GREEN" not in out.out


def test_cli_requires_explicit_main_head_and_confirmation():
    for argv in (
        [],
        ["--expected-main-head", "d" * 40],
        ["--confirm", cli.invocation.CONFIRM_TOKEN],
    ):
        try:
            cli.parse_args(argv)
        except SystemExit as exc:
            assert exc.code == 2
        else:
            raise AssertionError("missing required CLI input must fail")
