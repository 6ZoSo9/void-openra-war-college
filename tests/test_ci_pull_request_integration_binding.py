from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/ci.yml"


def test_pull_request_binding_uses_merge_parent_as_authoritative_base():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "EVENT_BASE_SHA: ${{ github.event.pull_request.base.sha }}" in text
    assert 'test "$actual_base_sha" = "$EXPECTED_BASE_SHA"' not in text
    assert 'test "$actual_head_sha" = "$EXPECTED_HEAD_SHA"' in text
    assert 'test "$actual_base_sha" != "$actual_head_sha"' in text
    assert 'git cat-file -e "${actual_base_sha}^{commit}"' in text
    assert 'git cat-file -e "${actual_head_sha}^{commit}"' in text
    assert 'git diff --check "$actual_base_sha" "$actual_head_sha"' in text


def test_stale_event_base_is_diagnostic_not_a_hard_failure():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'if test "$actual_base_sha" = "$EVENT_BASE_SHA"; then' in text
    assert "base_event_matches_merge_parent=true" in text
    assert "base_event_matches_merge_parent=false" in text
    assert "event_base_sha=%s" in text
    assert "base_event_matches_merge_parent=%s" in text
