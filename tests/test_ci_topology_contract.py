"""Executable contract for the default source-only CI topology."""

from pathlib import Path
import re

import pytest


WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"

CHECKOUT_PIN = "actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8"
SETUP_PYTHON_PIN = "actions/setup-python@e797f83bcb11b83ae66e0230d6156d7c80228e7c"


def validate_ci_topology(source: str) -> None:
    """Reject topology drift that could turn a green matrix into weak evidence."""
    required_once = (
        CHECKOUT_PIN,
        SETUP_PYTHON_PIN,
        "permissions:\n  contents: read",
        'python-version: ["3.10", "3.11", "3.12"]',
        "persist-credentials: false",
        "submodules: false",
        "fetch-depth: 2",
        "EXPECTED_INTEGRATION_SHA: ${{ github.sha }}",
        "EXPECTED_BASE_SHA: ${{ github.event.pull_request.base.sha }}",
        "EXPECTED_HEAD_SHA: ${{ github.event.pull_request.head.sha }}",
        "read -r actual_base_sha actual_head_sha extra_parent",
        'test -z "${extra_parent:-}"',
        'test "$actual_base_sha" = "$EXPECTED_BASE_SHA"',
        'test "$actual_head_sha" = "$EXPECTED_HEAD_SHA"',
        'git diff --check "$actual_base_sha" "$actual_head_sha"',
        "test ! -e OpenRA/.git",
        'python -m pip install --disable-pip-version-check -e ".[dev]"',
        "python -m pytest tests/ -v",
        "python -m ruff check openra_env/",
    )
    for marker in required_once:
        assert source.count(marker) == 1, f"required marker must occur exactly once: {marker}"

    assert not re.search(r"uses:\s+actions/(checkout|setup-python)@v\d", source)
    assert "submodules: recursive" not in source
    assert "persist-credentials: true" not in source
    assert "continue-on-error: true" not in source

    ordered = (
        "Bind pull-request integration generation",
        "Prove Python CI does not require private engine checkout",
        "Install dependencies",
        "Run tests",
        "Lint",
    )
    positions = [source.index(marker) for marker in ordered]
    assert positions == sorted(positions), "identity, isolation, tests, and lint must remain ordered"


def test_default_ci_topology_is_exactly_bound() -> None:
    validate_ci_topology(WORKFLOW.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("old", "new"),
    (
        (CHECKOUT_PIN, "actions/checkout@v5"),
        ("persist-credentials: false", "persist-credentials: true"),
        ("submodules: false", "submodules: recursive"),
        ('python-version: ["3.10", "3.11", "3.12"]', 'python-version: ["3.12"]'),
        ('test -z "${extra_parent:-}"', ": # parent cardinality bypassed"),
        (
            'git diff --check "$actual_base_sha" "$actual_head_sha"',
            'git diff --check "$actual_integration_sha^" "$actual_integration_sha"',
        ),
        ("python -m pytest tests/ -v", "python -m pytest tests/test_config.py -v"),
        ("python -m ruff check openra_env/", "true # lint skipped"),
    ),
)
def test_topology_mutations_fail_closed(old: str, new: str) -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    assert source.count(old) == 1
    with pytest.raises(AssertionError):
        validate_ci_topology(source.replace(old, new))


def test_terminal_step_reordering_fails_closed() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    mutated = source.replace("Run tests", "TEMP", 1).replace("Lint", "Run tests", 1).replace("TEMP", "Lint", 1)
    with pytest.raises(AssertionError):
        validate_ci_topology(mutated)
