from __future__ import annotations

import ast
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNTIME = ROOT / (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "runtime_integration_generation2.py"
)
OVERLAY = ROOT / (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_overlay_generation2.py"
)
WIRING = ROOT / (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_proto_child_wiring_generation2.py"
)

SENTINEL = "__v8_adapter_rejected_unit_ids_invalid__"


def dotted_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return (base + "." if base else "") + node.attr
    return ""


def method_source(text: str, tree: ast.AST, class_name: str) -> str:
    lines = text.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for child in node.body:
                if (
                    isinstance(child, ast.FunctionDef)
                    and child.name == "_adapted_decision"
                ):
                    return "\n".join(
                        lines[child.lineno - 1 : child.end_lineno]
                    ) + "\n"
    raise AssertionError(f"_adapted_decision missing from {class_name}")


class AdapterFeedbackOverlaySourceOnlyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = RUNTIME.read_text(encoding="utf-8")
        cls.overlay = OVERLAY.read_text(encoding="utf-8")
        cls.wiring = WIRING.read_text(encoding="utf-8")
        cls.runtime_tree = ast.parse(cls.runtime, filename=str(RUNTIME))
        cls.overlay_tree = ast.parse(cls.overlay, filename=str(OVERLAY))
        cls.wiring_tree = ast.parse(cls.wiring, filename=str(WIRING))

    def test_exact_sentinel_branch_only(self) -> None:
        self.assertEqual(
            self.overlay.count(f'if name == "{SENTINEL}":'),
            1,
        )
        self.assertIn('reason = "unit_ids invalid"', self.overlay)
        self.assertIn("elif name not in offered:", self.overlay)
        self.assertIn(
            'reason = "function_not_offered:" + name',
            self.overlay,
        )

    def test_historical_method_otherwise_identical(self) -> None:
        old = method_source(
            self.runtime,
            self.runtime_tree,
            "Pair06V9StrictVisibleContactDecisionHooks",
        )
        new = method_source(
            self.overlay,
            self.overlay_tree,
            "Pair06V9AdapterRejectionFeedbackDecisionHooks",
        )
        repair = "\n".join(
            [
                f'            if name == "{SENTINEL}":',
                "                ok = False",
                '                reason = "unit_ids invalid"',
                "                commands = []",
                "            elif name not in offered:",
            ]
        ) + "\n"
        historical = "            if name not in offered:\n"
        self.assertEqual(new.replace(repair, historical, 1), old)

    def test_fail_closed_contract_flags(self) -> None:
        for text in (
            '"sentinel_accepted": False',
            '"sentinel_host_validation_performed": False',
            '"sentinel_world_mutation_performed": False',
            '"consumed_attempt_retry_authorized": False',
            '"execution_authorized": False',
            '"automatic_retry": False',
            '"training_authorized": False',
            '"deployment_authorized": False',
            '"void_chain_mutation_authorized": False',
            '"wallet_or_funds_action_authorized": False',
        ):
            self.assertIn(text, self.overlay)

    def test_historical_wiring_stays_source_bound(self) -> None:
        raw = WIRING.read_bytes()
        actual = hashlib.sha1(
            f"blob {len(raw)}\0".encode("ascii") + raw
        ).hexdigest()
        self.assertEqual(
            actual,
            "1b87cb5596c219e6118f4b69845dbecaa29a3ace",
        )
        self.assertNotIn("feedback_overlay", self.wiring)
        self.assertIn(
            "order_integration.Pair06V9InputOrderCoherentDecisionHooks(",
            self.wiring,
        )
        review_path = ROOT / (
            "openra_env/learning/"
            "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
            "input_order_coherence_proto_child_wiring_"
            "source_binding_review_generation2.py"
        )
        review_text = review_path.read_text(encoding="utf-8")
        self.assertIn(
            'WIRING_GIT_BLOB = "1b87cb5596c219e6118f4b69845dbecaa29a3ace"',
            review_text,
        )

    def test_overlay_sha_is_expected_candidate(self) -> None:
        self.assertEqual(
            hashlib.sha256(OVERLAY.read_bytes()).hexdigest(),
            "16b28f995943b37a2af60b20a636d7571abad134bbb6c556ea4d874baea19258",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
