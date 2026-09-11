from __future__ import annotations

import hashlib
import importlib.util
import os
import py_compile
import tempfile
import unittest
from pathlib import Path

from openra_env.learning.g2_runtime_compiled_comparator_gate import (
    EXPECTED_COMPARATOR_SHA256,
    load_accepted_comparator,
)
from tests.test_g2_runtime_frontier_adapter_v1 import ACCEPTED_COMPARATOR_SOURCE


class TestG2RuntimeComparatorLoaderV1(unittest.TestCase):
    def test_verified_source_bytes_ignore_timestamp_valid_poisoned_pyc(self):
        accepted = ACCEPTED_COMPARATOR_SOURCE
        poison = accepted.replace(
            'SCOPE = "tactical_competence_only"',
            'SCOPE = "poisoned_cached_bytecode"',
            1,
        )
        self.assertNotEqual(poison, accepted)
        self.assertEqual(len(poison.encode("utf-8")), len(accepted.encode("utf-8")))

        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / "compiled.py"
            fixed_mtime = 1_700_000_000

            source.write_text(poison, encoding="utf-8")
            os.utime(source, (fixed_mtime, fixed_mtime))
            cache = Path(importlib.util.cache_from_source(str(source)))
            cache.parent.mkdir(parents=True, exist_ok=True)
            py_compile.compile(str(source), cfile=str(cache), doraise=True)

            source.write_text(accepted, encoding="utf-8")
            os.utime(source, (fixed_mtime, fixed_mtime))
            self.assertEqual(
                hashlib.sha256(source.read_bytes()).hexdigest(),
                EXPECTED_COMPARATOR_SHA256,
            )

            # Prove the adversarial fixture is meaningful: the ordinary path
            # loader accepts the timestamp/size-valid poisoned bytecode cache.
            spec = importlib.util.spec_from_file_location("poison_probe", source)
            self.assertIsNotNone(spec)
            self.assertIsNotNone(spec.loader)
            probe = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(probe)
            self.assertEqual(probe.SCOPE, "poisoned_cached_bytecode")

            # The production loader must execute only the bytes it already
            # hashed, so the cached bytecode can never influence execution.
            loaded = load_accepted_comparator(source)
            self.assertEqual(loaded.SCOPE, "tactical_competence_only")


if __name__ == "__main__":
    unittest.main()
