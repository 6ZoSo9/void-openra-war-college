from __future__ import annotations

import ast
import subprocess
import unittest
from pathlib import Path

from openra_env.learning.g2_runtime_tool_classification import (
    TOOL_CLASSIFICATION,
)

BASE_HEAD = "5c815762cba15f350495d3c3dbeb99246964bee1"
BASE_TREE = "90c87bc19aab8b90d19774df99a1317f170f8b7b"
BASE_BLOBS = {
    "openra_env/agent.py": "2bf0e37d2f9d24c019acbd3c811638e8bc0960cc",
    "openra_env/mcp_ws_client.py": "fe144d0562314f6afe9284d087335720e19dc57f",
    "openra_env/learning/general_brain_direct_policy.py": "d7c0af773a0a36657e5f8225e46cb60d38b452dc",
    "openra_env/learning/general_brain_policy_adapter.py": "682d561e57a721a456325c568db6550ebbf19370",
    "scripts/capture_designated_host_controller_evidence_generation2_v1.py": (
        "c0bfd0565a96c64842d86a566dff273a6d19804f"
    ),
}
PRESERVED_CURRENT_BLOBS = {
    key: value for key, value in BASE_BLOBS.items()
    if key != "openra_env/agent.py"
}
EXPECTED_PATHS = {
    ".github/workflows/g2-runtime-frontier-adapter-source-contract.yml",
    "openra_env/agent.py",
    "openra_env/learning/g2_runtime_tool_classification.py",
    "openra_env/learning/g2_runtime_capability_projection.py",
    "openra_env/learning/g2_runtime_candidate_frontier.py",
    "openra_env/learning/g2_runtime_compiled_comparator_gate.py",
    "tests/test_g2_runtime_frontier_adapter_v1.py",
    "tests/test_g2_runtime_frontier_source_contract_v1.py",
    "tests/test_g2_runtime_comparator_loader_v1.py",
    "tests/test_agent_phase_tool_surfaces_v1.py",
}
FORBIDDEN_RUNTIME_IMPORTS = {
    "httpx", "requests", "urllib", "socket", "subprocess"
}
FORBIDDEN_CALL_NAMES = {
    "chat_completion", "urlopen", "post", "request"
}


class TestG2RuntimeFrontierSourceContractV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    @classmethod
    def git(cls, *args: str, check: bool = True) -> str:
        cp = subprocess.run(
            ["git", "-C", str(cls.root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if check and cp.returncode != 0:
            raise AssertionError(
                "git command failed: "
                + " ".join(args)
                + "\n"
                + cp.stderr
            )
        return cp.stdout.strip()

    def test_exact_pr40_parent_is_bound(self):
        self.assertEqual(
            self.git("rev-parse", f"{BASE_HEAD}^{{tree}}"),
            BASE_TREE,
        )
        for path, blob in BASE_BLOBS.items():
            self.assertEqual(
                self.git("rev-parse", f"{BASE_HEAD}:{path}"),
                blob,
                path,
            )
        cp = subprocess.run(
            ["git", "-C", str(self.root), "merge-base", "--is-ancestor", BASE_HEAD, "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stderr.decode())

    def test_child_scope_is_exact_and_capture_transport_are_preserved(self):
        changed = set(
            filter(
                None,
                self.git("diff", "--name-only", f"{BASE_HEAD}...HEAD").splitlines(),
            )
        )
        changed.update(
            filter(None, self.git("diff", "--name-only").splitlines())
        )
        changed.update(
            filter(
                None,
                self.git(
                    "ls-files", "--others", "--exclude-standard"
                ).splitlines(),
            )
        )
        self.assertEqual(changed, EXPECTED_PATHS)
        for path, blob in PRESERVED_CURRENT_BLOBS.items():
            self.assertEqual(self.git("rev-parse", f"HEAD:{path}"), blob, path)

    def test_agent_intercept_is_immediately_before_gameplay_call(self):
        text = (self.root / "openra_env/agent.py").read_text(encoding="utf-8")
        marker = "prepared_tool_call = await g2_frontier.prepare_call("
        self.assertEqual(text.count(marker), 1)
        start = text.index(marker)
        execute = text.index(
            "result = await env.call_tool(fn_name, **fn_args)", start
        )
        self.assertLess(start, execute)
        between = text[start:execute]
        self.assertIn("fn_name = prepared_tool_call.tool_name", between)
        self.assertIn("fn_args = prepared_tool_call.arguments", between)
        self.assertNotIn("await env.call_tool(", between)
        self.assertIn(
            '"g2_runtime_frontier": {',
            text,
        )

    def test_runtime_tool_surface_has_no_unclassified_offered_tools(self):
        source = (
            self.root / "openra_env/server/openra_environment.py"
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        offered = set()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == "configurable_tool":
                    offered.add(node.name)
        self.assertTrue(offered)
        missing = sorted(offered - set(TOOL_CLASSIFICATION))
        self.assertEqual(missing, [], "unclassified MCP tools: " + repr(missing))

    def test_adapter_modules_have_no_model_or_network_execution_path(self):
        for name in (
            "g2_runtime_tool_classification.py",
            "g2_runtime_capability_projection.py",
            "g2_runtime_candidate_frontier.py",
            "g2_runtime_compiled_comparator_gate.py",
        ):
            path = self.root / "openra_env/learning" / name
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    modules = []
                    if isinstance(node, ast.Import):
                        modules = [alias.name.split(".")[0] for alias in node.names]
                    else:
                        modules = [(node.module or "").split(".")[0]]
                    self.assertFalse(
                        FORBIDDEN_RUNTIME_IMPORTS.intersection(modules),
                        f"{name}: forbidden import {modules}",
                    )
                if isinstance(node, ast.Call):
                    fn = node.func
                    call_name = fn.id if isinstance(fn, ast.Name) else (
                        fn.attr if isinstance(fn, ast.Attribute) else ""
                    )
                    self.assertNotIn(
                        call_name, FORBIDDEN_CALL_NAMES,
                        f"{name}: forbidden call {call_name}",
                    )


if __name__ == "__main__":
    unittest.main()
