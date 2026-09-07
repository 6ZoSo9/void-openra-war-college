#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path

from scripts import war_college_designated_host_verify_request_v1 as wrapper


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


class VerifyRequestTests(unittest.TestCase):
    def setUp(self):
        self._production_uid = wrapper.EXPECTED_UID
        self._production_gid = wrapper.EXPECTED_GID
        wrapper.EXPECTED_UID = os.getuid()
        wrapper.EXPECTED_GID = os.getgid()

    def tearDown(self):
        wrapper.EXPECTED_UID = self._production_uid
        wrapper.EXPECTED_GID = self._production_gid

    def test_production_identity_constants_are_precision_uid_gid(self):
        self.assertEqual(self._production_uid, 1000)
        self.assertEqual(self._production_gid, 1000)

    def make_bundle(self, root: Path, request_id: str, *, evidence=None, auth=None):
        evidence = {"attempt_id": "attempt"} if evidence is None else evidence
        auth = {"marker": "auth"} if auth is None else auth
        evidence_raw = canonical(evidence)
        auth_raw = canonical(auth)
        request = {
            "marker": wrapper.REQUEST_MARKER,
            "schema_version": wrapper.REQUEST_SCHEMA_VERSION,
            "request_id": request_id,
            "evidence_sha256": hashlib.sha256(evidence_raw).hexdigest(),
            "producer_auth_sha256": hashlib.sha256(auth_raw).hexdigest(),
        }
        req_dir = root / "war_college" / "verifier_requests_v1" / request_id
        req_dir.mkdir(parents=True, mode=0o700)
        os.chmod(root / "war_college", 0o700)
        os.chmod(root / "war_college" / "verifier_requests_v1", 0o700)
        os.chmod(req_dir, 0o700)
        files = {
            wrapper.REQUEST_FILE: canonical(request),
            wrapper.EVIDENCE_FILE: evidence_raw,
            wrapper.AUTH_FILE: auth_raw,
        }
        for name, payload in files.items():
            path = req_dir / name
            path.write_bytes(payload)
            os.chmod(path, 0o400)
        return req_dir, evidence, auth

    def test_invalid_request_id_fails_before_bundle_lookup(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            with self.assertRaisesRegex(wrapper.WrapperHold, "HOLD_REQUEST_ID_INVALID"):
                wrapper._process_request(
                    "../escape",
                    data_dir=root,
                    verify_callable=lambda *_: {},
                )

    def test_clean_bundle_calls_only_supplied_verifier_and_retains_files(self):
        request_id = "wcrq1_" + "a" * 32
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            req_dir, evidence, auth = self.make_bundle(root, request_id)
            calls = []

            def verify(e, a):
                calls.append((e, a))
                return {
                    "contract": "GREEN",
                    "holds": [],
                    "phase": "consumed",
                    "consumption_sha256": "b" * 64,
                    "runtime_evidence": "PENDING_DESIGNATED_HOST",
                }

            result = wrapper._process_request(
                request_id,
                data_dir=root,
                verify_callable=verify,
            )
            self.assertEqual(calls, [(evidence, auth)])
            self.assertEqual(result["verifier_contract"], "GREEN")
            self.assertFalse(result["private_key_read"])
            self.assertFalse(result["request_bundle_mutated"])
            self.assertEqual(
                set(path.name for path in req_dir.iterdir()),
                {wrapper.REQUEST_FILE, wrapper.EVIDENCE_FILE, wrapper.AUTH_FILE},
            )

    def test_raw_evidence_hash_substitution_fails_before_verifier(self):
        request_id = "wcrq1_" + "b" * 32
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            req_dir, _, _ = self.make_bundle(root, request_id)
            evidence_path = req_dir / wrapper.EVIDENCE_FILE
            os.chmod(evidence_path, 0o600)
            evidence_path.write_bytes(canonical({"attempt_id": "changed"}))
            os.chmod(evidence_path, 0o400)
            called = []

            with self.assertRaisesRegex(
                wrapper.WrapperHold,
                "HOLD_REQUEST_EVIDENCE_SHA256_MISMATCH",
            ):
                wrapper._process_request(
                    request_id,
                    data_dir=root,
                    verify_callable=lambda *_: called.append(True) or {},
                )
            self.assertEqual(called, [])

    def test_extra_bundle_entry_fails_closed(self):
        request_id = "wcrq1_" + "c" * 32
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            req_dir, _, _ = self.make_bundle(root, request_id)
            extra = req_dir / "extra"
            extra.write_text("x")
            os.chmod(extra, 0o400)
            with self.assertRaisesRegex(
                wrapper.WrapperHold,
                "HOLD_REQUEST_BUNDLE_ENTRIES_NOT_EXACT",
            ):
                wrapper._process_request(
                    request_id,
                    data_dir=root,
                    verify_callable=lambda *_: {},
                )

    def test_writable_evidence_file_fails_closed(self):
        request_id = "wcrq1_" + "d" * 32
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            req_dir, _, _ = self.make_bundle(root, request_id)
            os.chmod(req_dir / wrapper.EVIDENCE_FILE, 0o600)
            with self.assertRaisesRegex(
                wrapper.WrapperHold,
                "HOLD_REQUEST_FILE_MODE_MISMATCH",
            ):
                wrapper._process_request(
                    request_id,
                    data_dir=root,
                    verify_callable=lambda *_: {},
                )

    def test_symlinked_evidence_file_fails_closed(self):
        request_id = "wcrq1_" + "e" * 32
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            req_dir, _, _ = self.make_bundle(root, request_id)
            evidence = req_dir / wrapper.EVIDENCE_FILE
            target = req_dir / "target"
            target.write_bytes(evidence.read_bytes())
            os.chmod(target, 0o400)
            os.chmod(evidence, 0o600)
            evidence.unlink()
            evidence.symlink_to(target.name)
            with self.assertRaisesRegex(
                wrapper.WrapperHold,
                "HOLD_REQUEST_BUNDLE_ENTRIES_NOT_EXACT|HOLD_REQUEST_FILE_OPEN_FAILURE",
            ):
                wrapper._process_request(
                    request_id,
                    data_dir=root,
                    verify_callable=lambda *_: {},
                )

    def test_noncanonical_request_json_fails_closed(self):
        request_id = "wcrq1_" + "f" * 32
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            os.chmod(root, 0o700)
            req_dir, _, _ = self.make_bundle(root, request_id)
            path = req_dir / wrapper.REQUEST_FILE
            parsed = json.loads(path.read_text())
            os.chmod(path, 0o600)
            path.write_text(json.dumps(parsed, indent=2) + "\n")
            os.chmod(path, 0o400)
            with self.assertRaisesRegex(
                wrapper.WrapperHold,
                "HOLD_REQUEST_JSON_NOT_CANONICAL",
            ):
                wrapper._process_request(
                    request_id,
                    data_dir=root,
                    verify_callable=lambda *_: {},
                )


if __name__ == "__main__":
    unittest.main()
