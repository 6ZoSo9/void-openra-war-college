"""Keep CI diagnostics separate from test selection and acceptance."""

from pathlib import Path
import shlex

import pytest
import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/ci.yml"


@pytest.fixture(scope="module")
def workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def _step(workflow, name):
    matches = [
        step for step in workflow["jobs"]["test"]["steps"]
        if step.get("name") == name
    ]
    assert len(matches) == 1
    return matches[0]


def test_diagnostics_keep_one_direct_full_suite_invocation(workflow):
    # Exact argv excludes test filters, retries, shell pipelines, and masks.
    assert shlex.split(_step(workflow, "Run tests")["run"]) == [
        "python", "-m", "pytest", "tests/", "-v", "--durations=25",
        "-o", "faulthandler_timeout=300",
    ]


def test_python_matrix_and_independent_failures_are_preserved(workflow):
    job = workflow["jobs"]["test"]
    assert job["runs-on"] == "ubuntu-24.04"
    assert job["strategy"]["fail-fast"] is False
    assert job["strategy"]["matrix"] == {
        "python-version": ["3.10", "3.11", "3.12"],
    }


def test_diagnostics_cannot_skip_or_accept_failed_tests(workflow):
    job = workflow["jobs"]["test"]
    step = _step(workflow, "Run tests")
    assert "if" not in job
    assert "if" not in step
    assert "continue-on-error" not in job
    assert "continue-on-error" not in step
    assert "env" not in step
    assert set(step) == {"name", "run"}


def test_private_engine_and_persistent_credentials_stay_disabled(workflow):
    checkout = workflow["jobs"]["test"]["steps"][0]
    assert checkout["uses"] == (
        "actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8"
    )
    assert checkout["with"]["submodules"] is False
    assert checkout["with"]["persist-credentials"] is False
    assert checkout["with"]["fetch-depth"] == 2
    assert workflow["permissions"] == {"contents": "read"}


def test_integration_generation_binding_is_retained(workflow):
    binding = _step(workflow, "Bind pull-request integration generation")
    assert binding["if"] == "github.event_name == 'pull_request'"
    assert binding["env"]["EXPECTED_INTEGRATION_SHA"] == "${{ github.sha }}"
    assert binding["env"]["EXPECTED_HEAD_SHA"] == (
        "${{ github.event.pull_request.head.sha }}"
    )
    assert 'test "$actual_integration_sha" = "$EXPECTED_INTEGRATION_SHA"' in binding["run"]
    assert 'test "$actual_head_sha" = "$EXPECTED_HEAD_SHA"' in binding["run"]
    assert 'git diff --check "$actual_base_sha" "$actual_head_sha"' in binding["run"]


def test_lint_still_follows_successful_tests(workflow):
    steps = workflow["jobs"]["test"]["steps"]
    tests = _step(workflow, "Run tests")
    lint = _step(workflow, "Lint")
    assert steps.index(lint) > steps.index(tests)
    assert lint == {"name": "Lint", "run": "python -m ruff check openra_env/"}
