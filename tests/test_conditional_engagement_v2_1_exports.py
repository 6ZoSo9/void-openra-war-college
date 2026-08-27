from openra_env.coaching import (
    ConditionalEngagementSessionV21,
    V21_CANDIDATE_SCHEMA,
    V21_EXPECTED_CANDIDATE_SHA256,
    V21_PREPARED_SCHEMA,
    v21_candidate_sha256,
)


def test_v21_package_exports_are_unambiguous():
    assert V21_CANDIDATE_SCHEMA == "void.apollyon.conditional-engagement-candidate.v2.1"
    assert V21_EXPECTED_CANDIDATE_SHA256 == "a0b08f7a7ea807de53416f589790059e2540404f680d6b470395bdbdc067f460"
    assert V21_PREPARED_SCHEMA == "void.apollyon.conditional-engagement-prepared-round.v2.1"
    assert ConditionalEngagementSessionV21.__name__ == "ConditionalEngagementSessionV21"
    assert callable(v21_candidate_sha256)
