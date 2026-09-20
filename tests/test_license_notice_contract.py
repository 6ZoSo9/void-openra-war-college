from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_gpl_license_text_remains_primary():
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "GNU GENERAL PUBLIC LICENSE" in license_text
    assert "Version 3, 29 June 2007" in license_text


def test_notice_preserves_upstream_and_void_provenance():
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "yxc20089/OpenRA-RL" in notice
    assert "OpenRA Developers and Contributors" in notice
    assert "6ZoSo9 and VOID Network contributors" in notice
    assert "anti-redistribution" in notice
    assert "are NOT imposed" in notice


def test_void_terms_are_attribution_only_not_vcl_restrictions():
    terms = (ROOT / "VOID_NETWORK_GPL_ATTRIBUTION_TERMS.md").read_text(
        encoding="utf-8"
    )
    assert "GNU GPLv3 section 7(b)" in terms
    assert "GNU GPLv3 section 7(c)" in terms
    assert "do not" in terms.lower()
    for required_freedom in (
        "forks",
        "modifications",
        "redistribution",
        "commercial use",
    ):
        assert required_freedom in terms.lower()
    assert "do **not** add the VCL restrictions" in terms


def test_third_party_branding_and_provenance_notices_exist():
    third_party = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
    trademarks = (ROOT / "docs/legal/TRADEMARKS.md").read_text(encoding="utf-8")
    provenance = (ROOT / "VOID_PROVENANCE.md").read_text(encoding="utf-8")
    assert "OpenRA/OpenRA" in third_party
    assert "6ZoSo9/void-openra-engine" in third_party
    assert "original Command & Conquer / Red Alert" in third_party
    assert "falsely implies sponsorship" in trademarks
    assert "OpenRA" in trademarks
    assert "openra_env/learning/" in provenance
    assert "docs/learning/" in provenance
    assert "does not exist on the current" in provenance


def test_visible_downstream_authorship_credit():
    authors = (ROOT / "AUTHORS.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "maintained by **6ZoSo9**" in authors
    assert "OpenRA-RL contributors" in authors
    assert "OpenRA Developers and Contributors" in authors
    assert "VOID OpenRA War College" in readme
    assert "maintained by **6ZoSo9**" in readme


def test_future_contribution_credit_policy_exists():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    template = (ROOT / ".github/pull_request_template.md").read_text(encoding="utf-8")
    assert "6ZoSo9 and VOID Network contributors" in contributing
    assert "Do not remove or falsify authorship" in contributing
    assert "GPLv3 section 7 attribution/origin terms" in contributing
    assert "upstream/third-party material" in template
    assert "copyright, authorship, provenance" in template


def test_github_citation_credits_downstream_project():
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    assert "VOID OpenRA War College" in citation
    assert 'family-names: "6ZoSo9"' in citation
    assert "OpenRA/OpenRA-RL attribution" in citation
    assert "GPL-3.0-only" in citation


def test_forensic_provenance_baseline_is_fixed_and_non_accusatory():
    import json

    report = (ROOT / "docs/legal/VOID_WAR_COLLEGE_PROVENANCE_BASELINE_V1.md").read_text(
        encoding="utf-8"
    )
    manifest = json.loads(
        (ROOT / "docs/legal/void-war-college-provenance-baseline-v1.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["schema"] == "void.war-college.provenance-baseline.v1"
    assert manifest["void_reference"]["commit"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert manifest["comparison_references"]["openra_rl"]["commit"] == "5dadd449c912ac2d4021cc8ed84fc0b385b1543c"
    assert manifest["comparison_references"]["openra_rl_website"]["commit"] == "0007f1fed49e954a7706c7c64a6c98894f98cfb1"
    assert len(manifest["fingerprints"]) == 159
    assert all(
        row["same_path_in_openra_rl_main"] is False
        and row["same_path_in_openra_rl_website_main"] is False
        for row in manifest["fingerprints"]
    )
    assert "shared upstream history; not claimed" in json.dumps(
        manifest["shared_upstream_prior_art_exclusions"]
    )
    assert "No automatic accusation" in manifest["future_comparison_rules"]["decision_rule"]
    assert "Similarity to this baseline is evidence to investigate" in report
