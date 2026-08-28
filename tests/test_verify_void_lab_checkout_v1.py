from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


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
        "engine_tracked_checkout_clean": None,
        "engine_exact_checkout_clean": None,
        "engine_ignored_runtime_inputs_absent": True,
        "engine_snapshot_stable": True,
        "war_college_tracked_checkout_clean": True,
        "war_college_exact_checkout_clean": True,
        "war_college_ignored_runtime_inputs_absent": True,
        "war_college_snapshot_stable": True,
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
        report = MODULE.evaluate_probe(probe(), source_only=True)
        self.assertEqual(report["source_contract"], "GREEN")
        self.assertEqual(report["checkout_contract"], "PENDING_ENGINE_CHECKOUT")
        self.assertEqual(report["runtime_evidence"], "PENDING_DESIGNATED_HOST")
        self.assertEqual(
            report["requested_contract"], "COMMITTED_TRACKED_COMPOSITION_ONLY"
        )
        self.assertEqual(
            report["source_only_limitation"],
            "DOES_NOT_ASSERT_EXACT_DESIGNATED_HOST_COMPOSITION",
        )
        self.assertFalse(report["exact_checkout_evidence"])
        self.assertFalse(report["checks"]["engine_checkout_present"])

    def test_exact_clean_engine_checkout_is_green(self):
        report = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                engine_tracked_checkout_clean=True,
                engine_exact_checkout_clean=True,
                engine_ignored_runtime_inputs_absent=True,
            )
        )
        self.assertEqual(report["source_contract"], "GREEN")
        self.assertEqual(report["checkout_contract"], "GREEN")
        self.assertEqual(
            report["requested_contract"],
            "EXACT_WORKTREE_WITH_RUNTIME_RELEVANT_IGNORED_INPUTS_ABSENT",
        )
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
                engine_tracked_checkout_clean=True,
                engine_exact_checkout_clean=True,
            )
        )
        dirty = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                engine_tracked_checkout_clean=False,
                engine_exact_checkout_clean=False,
            )
        )
        self.assertEqual(wrong["checkout_contract"], "HOLD")
        self.assertIn("engine_checkout_matches_gitlink", wrong["holds"])
        self.assertEqual(dirty["checkout_contract"], "HOLD")
        self.assertIn("engine_tracked_checkout_clean", dirty["holds"])

    def test_untracked_parent_or_engine_input_holds_exact_checkout(self):
        parent_dirty = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                engine_tracked_checkout_clean=True,
                engine_exact_checkout_clean=True,
                war_college_exact_checkout_clean=False,
            )
        )
        engine_dirty = MODULE.evaluate_probe(
            probe(
                engine_checkout_present=True,
                engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                engine_tracked_checkout_clean=True,
                engine_exact_checkout_clean=False,
            )
        )
        self.assertEqual(parent_dirty["checkout_contract"], "HOLD")
        self.assertIn("war_college_exact_checkout_clean", parent_dirty["holds"])
        self.assertEqual(engine_dirty["checkout_contract"], "HOLD")
        self.assertIn("engine_exact_checkout_clean", engine_dirty["holds"])

    def test_wrong_url_or_missing_frozen_ancestry_holds_source(self):
        wrong_url = MODULE.evaluate_probe(probe(engine_repository_url="https://example.invalid"))
        missing_ancestor = MODULE.evaluate_probe(
            probe(war_college_frozen_is_ancestor=False)
        )
        self.assertEqual(wrong_url["source_contract"], "HOLD")
        self.assertEqual(missing_ancestor["source_contract"], "HOLD")

    def test_source_only_rejects_mixed_war_college_generation(self):
        report = MODULE.evaluate_probe(
            probe(war_college_snapshot_stable=False), source_only=True
        )
        self.assertEqual(report["source_contract"], "HOLD")
        self.assertEqual(report["checkout_contract"], "HOLD")
        self.assertIn("war_college_snapshot_stable", report["holds"])

    def test_canonical_json_is_stable_and_compact(self):
        report = MODULE.evaluate_probe(probe())
        encoded = MODULE.canonical_json(report)
        self.assertEqual(encoded, MODULE.canonical_json(report))
        self.assertEqual(json.loads(encoded), report)
        self.assertNotIn("\n", encoded)
        self.assertTrue(encoded.startswith('{"checkout_contract":'))


class CliEnvironmentFailureTests(unittest.TestCase):
    def _assert_json_hold(self, result, reason_code: str) -> None:
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertEqual(len(result.stdout.splitlines()), 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema_version"], 6)
        self.assertEqual(report["source_contract"], "HOLD")
        self.assertEqual(report["checkout_contract"], "HOLD")
        self.assertEqual(report["runtime_evidence"], "PENDING_DESIGNATED_HOST")
        self.assertEqual(report["holds"], [reason_code])
        self.assertEqual(report["probe_failure"]["reason_code"], reason_code)
        self.assertNotIn("Traceback", result.stdout)

    def test_nonexistent_repo_root_emits_one_json_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing"
            result = subprocess.run(
                [sys.executable, str(SOURCE), "--repo-root", str(missing), "--source-only"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self._assert_json_hold(result, "repo_root_unavailable")

    def test_unavailable_git_emits_one_json_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SOURCE),
                    "--repo-root",
                    directory,
                    "--source-only",
                ],
                env={"PATH": ""},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        self._assert_json_hold(result, "git_unavailable")


class GitBackedCleanlinessTests(unittest.TestCase):
    def _repository(self, root: Path) -> None:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "larry-test@example.invalid"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Larry Checkout Test"],
            cwd=root,
            check=True,
        )
        tracked = root / "tracked.txt"
        tracked.write_text("preserved\n", encoding="utf-8")
        subprocess.run(["git", "add", "tracked.txt"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)

    def _commit_ignore(self, root: Path, pattern: str) -> None:
        (root / ".gitignore").write_text(pattern, encoding="utf-8")
        subprocess.run(["git", "add", ".gitignore"], cwd=root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "fixture ignore policy"],
            cwd=root,
            check=True,
        )

    def _composed_repositories(self, root: Path) -> tuple[str, str]:
        engine = root / MODULE.ENGINE_SUBMODULE_PATH
        engine.mkdir()
        self._repository(engine)
        engine_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=engine,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()

        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "larry-test@example.invalid"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Larry Checkout Test"],
            cwd=root,
            check=True,
        )
        (root / "tracked.txt").write_text("preserved\n", encoding="utf-8")
        (root / ".gitmodules").write_text(
            '[submodule "OpenRA"]\n'
            "\tpath = OpenRA\n"
            f"\turl = {MODULE.ENGINE_REPOSITORY_URL}\n",
            encoding="utf-8",
        )
        subprocess.run(
            ["git", "add", "tracked.txt", ".gitmodules"], cwd=root, check=True
        )
        subprocess.run(
            [
                "git",
                "update-index",
                "--add",
                "--cacheinfo",
                f"160000,{engine_head},{MODULE.ENGINE_SUBMODULE_PATH}",
            ],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-qm", "composed fixture"], cwd=root, check=True
        )
        parent_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        return parent_head, engine_head

    def test_untracked_war_college_benchmark_input_forces_exact_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._repository(root)
            untracked = root / "benchmarks" / "untracked-input.json"
            untracked.parent.mkdir()
            untracked.write_text("{}\n", encoding="utf-8")
            self.assertTrue(
                MODULE.git_checkout_clean(root, include_untracked=False)
            )
            self.assertFalse(
                MODULE.git_checkout_clean(root, include_untracked=True)
            )
            untracked.unlink()
            self.assertTrue(MODULE.git_checkout_clean(root, include_untracked=True))

    def test_untracked_engine_map_input_forces_exact_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._repository(root)
            untracked = root / "mods" / "ra" / "maps" / "untracked-map.yaml"
            untracked.parent.mkdir(parents=True)
            untracked.write_text("MapFormat: 12\n", encoding="utf-8")
            self.assertTrue(
                MODULE.git_checkout_clean(root, include_untracked=False)
            )
            self.assertFalse(
                MODULE.git_checkout_clean(root, include_untracked=True)
            )
            untracked.unlink()
            self.assertTrue(MODULE.git_checkout_clean(root, include_untracked=True))

    def test_ignored_war_college_build_input_forces_exact_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._repository(root)
            self._commit_ignore(root, "build/\n")
            artifact = root / "build" / "stale-benchmark-input.json"
            artifact.parent.mkdir()
            artifact.write_text("{}\n", encoding="utf-8")
            ignored_runtime_absent = MODULE.ignored_runtime_inputs_absent(
                root, MODULE.war_college_ignored_runtime_path
            )
            report = MODULE.evaluate_probe(
                probe(
                    engine_checkout_present=True,
                    engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                    engine_tracked_checkout_clean=True,
                    engine_exact_checkout_clean=True,
                    war_college_ignored_runtime_inputs_absent=(
                        ignored_runtime_absent
                    ),
                )
            )
            self.assertFalse(ignored_runtime_absent)
            self.assertEqual(report["checkout_contract"], "HOLD")
            self.assertIn(
                "war_college_ignored_runtime_inputs_absent", report["holds"]
            )
            artifact.unlink()
            artifact.parent.rmdir()
            self.assertTrue(
                MODULE.ignored_runtime_inputs_absent(
                    root, MODULE.war_college_ignored_runtime_path
                )
            )

    def test_ignored_engine_bin_input_forces_exact_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._repository(root)
            self._commit_ignore(root, "bin/\n")
            artifact = root / "bin" / "stale-runtime.dll"
            artifact.parent.mkdir()
            artifact.write_text("stale\n", encoding="utf-8")
            ignored_runtime_absent = MODULE.ignored_runtime_inputs_absent(
                root, MODULE.engine_ignored_runtime_path
            )
            report = MODULE.evaluate_probe(
                probe(
                    engine_checkout_present=True,
                    engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                    engine_tracked_checkout_clean=True,
                    engine_exact_checkout_clean=True,
                    engine_ignored_runtime_inputs_absent=ignored_runtime_absent,
                )
            )
            self.assertFalse(ignored_runtime_absent)
            self.assertEqual(report["checkout_contract"], "HOLD")
            self.assertIn("engine_ignored_runtime_inputs_absent", report["holds"])
            artifact.unlink()
            artifact.parent.rmdir()
            self.assertTrue(
                MODULE.ignored_runtime_inputs_absent(
                    root, MODULE.engine_ignored_runtime_path
                )
            )

    def test_harmless_ignored_cache_does_not_block_exact_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._repository(root)
            self._commit_ignore(root, ".pytest_cache/\n")
            cache = root / ".pytest_cache" / "README.md"
            cache.parent.mkdir()
            cache.write_text("cache metadata\n", encoding="utf-8")
            self.assertTrue(MODULE.git_checkout_clean(root, include_untracked=True))
            self.assertTrue(
                MODULE.ignored_runtime_inputs_absent(
                    root, MODULE.war_college_ignored_runtime_path
                )
            )
            report = MODULE.evaluate_probe(
                probe(
                    engine_checkout_present=True,
                    engine_checkout_head=MODULE.ENGINE_FROZEN_COMMIT,
                    engine_tracked_checkout_clean=True,
                    engine_exact_checkout_clean=True,
                    engine_ignored_runtime_inputs_absent=True,
                )
            )
            self.assertEqual(report["checkout_contract"], "GREEN")

    def test_post_war_college_sample_mutation_forces_snapshot_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent_head, engine_head = self._composed_repositories(root)

            def mutate(phase: str) -> None:
                if phase == "after_war_college_initial":
                    injected = root / "benchmarks" / "post-sample.json"
                    injected.parent.mkdir()
                    injected.write_text("{}\n", encoding="utf-8")

            with mock.patch.object(
                MODULE, "WAR_COLLEGE_FROZEN_COMMIT", parent_head
            ), mock.patch.object(MODULE, "ENGINE_FROZEN_COMMIT", engine_head):
                report = MODULE.evaluate_probe(
                    MODULE.collect_probe(root, phase_hook=mutate)
                )
            self.assertEqual(report["checkout_contract"], "HOLD")
            self.assertIn("war_college_snapshot_stable", report["holds"])

    def test_post_engine_sample_mutation_forces_snapshot_hold(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            parent_head, engine_head = self._composed_repositories(root)

            def mutate(phase: str) -> None:
                if phase == "after_engine_initial":
                    injected = root / MODULE.ENGINE_SUBMODULE_PATH / "mods" / "race.yaml"
                    injected.parent.mkdir()
                    injected.write_text("MapFormat: 12\n", encoding="utf-8")

            with mock.patch.object(
                MODULE, "WAR_COLLEGE_FROZEN_COMMIT", parent_head
            ), mock.patch.object(MODULE, "ENGINE_FROZEN_COMMIT", engine_head):
                report = MODULE.evaluate_probe(
                    MODULE.collect_probe(root, phase_hook=mutate)
                )
            self.assertEqual(report["checkout_contract"], "HOLD")
            self.assertIn("engine_snapshot_stable", report["holds"])


if __name__ == "__main__":
    unittest.main()
