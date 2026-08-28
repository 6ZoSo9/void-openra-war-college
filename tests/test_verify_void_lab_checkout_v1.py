from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import unittest


SOURCE = Path(__file__).parents[1] / "scripts" / "verify_void_lab_checkout_v1.py"
SPEC = importlib.util.spec_from_file_location("verify_void_lab_checkout_v1", SOURCE)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def probe(**overrides):
    values = {
        "war_college_head": "a" * 40,
        "war_college_frozen_is_ancestor": True,
        "engine_gitlink_commit": MODULE.ENGINE_FROZEN_COMMIT,
        "engine_repository_url": MODULE.ENGINE_REPOSITORY_URL,
        "engine_checkout_present": False,
        "engine_checkout_head": None,
        "engine_checkout_clean": None,
        "war_college_checkout_clean": True,
    }
    values.update(overrides)
    return MODULE.Probe(**values)


class GitlinkParsingTests(unittest.TestCase):
    def test_accepts_exact_openra_gitlink(self):
        raw = f"160000 commit {MODULE.ENGINE_FROZEN_COMMIT}\tOpenRA\n"
        self.assertEqual(MODULE.parse_engine_gitlink(raw), MODULE.ENGINE_FROZEN_COMMIT)

    def test_rejects_blob_or_wrong_path(self):
        with self.assertRaises(MODULE.VerificationError):
            MODULE.parse_engine_gitlink(f"100644 blob {'a' * 40}\tOpenRA\n")
        with self.assertRaises(MODULE.VerificationError):
            MODULE.parse_engine_gitlink(f"160000 commit {'a' * 40}\tOther\n")

    def test_rejects_multiple_or_noncanonical_entries(self):
        with self.assertRaises(MODULE.VerificationError):
            MODULE.parse_engine_gitlink("")
        with self.assertRaises(MODULE.VerificationError):
            MODULE.parse_engine_gitlink(
                f"160000 commit {'A' * 40}\tOpenRA\n"
            )


class EvaluationTests(unittest.TestCase):
    def test_source_contract_can_be_green_without_private_checkout(self):
        report = MODULE.evaluate_probe(probe())
        self.assertEqual(report["source_contract"], "GREEN")
        self.assertEqual(report["checkout_contract"], "PENDING_ENGINE_CHECKOUT")
        self.assertEqual(report["runtime_evidence"], "PENDING_DESIGNATED_HOST")
        self.assertFalse(report["checks"]["engine_checkout_present"])

    def test_exact_clean_engine_checkout_is_green(self):
        report = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                engine_checkout_clean=True,
            )
        )
        self.assertEqual(report["source_contract"], "GREEN")
        self.assertEqual(report["checkout_contract"], "GREEN")
        self.assertEqual(report["holds"], [])

    def test_wrong_gitlink_holds_source_contract(self):
        report = MODULE.evaluate_probe(probe(engine_gitlink_commit="b" * 40))
        self.assertEqual(report["source_contract"], "HOLD")
        self.assertIn("engine_gitlink_is_frozen", report["holds"])

    def test_wrong_or_dirty_engine_checkout_holds_checkout_contract(self):
        wrong = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head="b" * 40,
                engine_checkout_clean=True,
            )
        )
        dirty = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                engine_checkout_clean=False,
            )
        )
        self.assertEqual(wrong["checkout_contract"], "HOLD")
        self.assertIn("engine_checkout_matches_gitlink", wrong["holds"])
        self.assertEqual(dirty["checkout_contract"], "HOLD")
        self.assertIn("engine_tracked_checkout_clean", dirty["holds"])

    def test_wrong_url_or_missing_frozen_ancestry_holds_source(self):
        wrong_url = MODULE.evaluate_probe(probe(engine_repository_url="https://example.invalid"))
        missing_ancestor = MODULE.evaluate_probe(
            probe(war_college_frozen_is_ancestor=False)
        )
        self.assertEqual(wrong_url["source_contract"], "HOLD")
        self.assertEqual(missing_ancestor["source_contract"], "HOLD")

    def test_canonical_json_is_stable_and_compact(self):
        report = MODULE.evaluate_probe(probe())
        encoded = MODULE.canonical_json(report)
        self.assertEqual(encoded, MODULE.canonical_json(report))
        self.assertEqual(json.loads(encoded), report)
        self.assertNotIn("\n", encoded)
        self.assertTrue(encoded.startswith('{"checkout_contract":'))


if __name__ == "__main__":
    unittest.main()
