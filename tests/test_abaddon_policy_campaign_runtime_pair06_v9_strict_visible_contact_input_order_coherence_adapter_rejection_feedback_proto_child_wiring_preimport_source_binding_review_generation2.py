from __future__ import annotations

import ast
from pathlib import Path
import shutil
import tempfile
import unittest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_feedback_proto_child_wiring_preimport_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]

DIRECT_ADVERSARY_PATHS = (
    review.WIRING_PATH,
    review.FEEDBACK_OVERLAY_PATH,
    review.HISTORICAL_WIRING_PATH,
    review.HISTORICAL_WIRING_REVIEW_PATH,
)


class AdapterFeedbackPreimportSourceReviewTest(unittest.TestCase):
    def test_review_module_imports_no_reviewed_learning_module(self) -> None:
        raw = Path(review.__file__).read_text(encoding="utf-8")
        tree = ast.parse(raw, filename=str(review.__file__))

        local_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module == "openra_env.learning" or module.startswith(
                    "openra_env.learning."
                ):
                    local_imports.append(module)

        self.assertEqual(local_imports, [])

    def test_clean_closure_is_verified_before_static_analysis(self) -> None:
        out = review.pair06_v9_adapter_feedback_preimport_source_review_contract()

        self.assertTrue(out["preimport_source_review_implemented"])
        self.assertFalse(out["reviewed_modules_imported_by_review"])
        self.assertFalse(out["reviewed_modules_executed_by_review"])
        self.assertTrue(out["worktree_bytes_verified_before_parse"])
        self.assertTrue(out["accepted_git_bytes_only_static_analysis"])
        self.assertTrue(out["reachable_local_import_closure_verified"])
        self.assertTrue(out["preimport_drift_fail_closed"])
        self.assertFalse(out["top_level_sentinel_execution_possible"])
        self.assertGreater(out["verified_closure_count"], 4)

    def test_direct_dependency_top_level_sentinels_never_execute(self) -> None:
        clean_sources = review._verify_worktree_before_parse(root=ROOT)

        for dirty_path in DIRECT_ADVERSARY_PATHS:
            with self.subTest(path=dirty_path):
                with tempfile.TemporaryDirectory() as td:
                    root = Path(td)
                    for path, raw in clean_sources.items():
                        target = root / path
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(raw)

                    marker = root / "TOP_LEVEL_SENTINEL_EXECUTED"
                    target = root / dirty_path
                    original = target.read_text(encoding="utf-8")
                    malicious = (
                        "from pathlib import Path as _SentinelPath\n"
                        f"_SentinelPath({str(marker)!r}).write_text('executed')\n"
                        + original
                    )
                    target.write_text(malicious, encoding="utf-8")

                    with self.assertRaises(
                        review.Pair06V9AdapterFeedbackPreimportSourceReviewHold
                    ):
                        review._verify_worktree_before_parse(root=root)

                    self.assertFalse(marker.exists())

    def test_predecessor_review_is_explicitly_superseded_for_authority(self) -> None:
        out = review.pair06_v9_adapter_feedback_preimport_source_review_contract()

        self.assertEqual(
            out["predecessor_review_git_blob"],
            "1027c91108750f25c8d730dc048e34ad8e6df6e0",
        )
        self.assertFalse(out["runtime_execution_authorized"])
        self.assertFalse(out["consumed_v9_attempt_retry_authorized"])
        self.assertEqual(
            out["next_gate"],
            "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
            "PARENT_SUPERVISOR_WIRING_REQUIRED",
        )

    def test_wire_parent_or_execute_holds(self) -> None:
        with self.assertRaises(
            review.Pair06V9AdapterFeedbackPreimportSourceReviewHold
        ):
            review.wire_parent_or_execute()


if __name__ == "__main__":
    unittest.main(verbosity=2)
