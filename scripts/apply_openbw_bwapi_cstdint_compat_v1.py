#!/usr/bin/env python3
"""Apply the exact one-line OpenBW/BWAPI GCC-13 compatibility patch.

Source provenance:
- OpenBW/bwapi PR #16
- commit 04eb2f7f88174808ba46e3a53cc2a82f85da57ad
- base Game.h blob ccf26f5e77693e5f682ff27f7d3185ad08b6c7b6
- patched Game.h blob debb572f6eb23c44ff1096bf8ba3ebea5da3ac7b

This operates only on an explicitly supplied transient BWAPI checkout.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

BASE_BLOB = "ccf26f5e77693e5f682ff27f7d3185ad08b6c7b6"
PATCHED_BLOB = "debb572f6eb23c44ff1096bf8ba3ebea5da3ac7b"
UPSTREAM_PR = "OpenBW/bwapi#16"
UPSTREAM_PATCH_COMMIT = "04eb2f7f88174808ba46e3a53cc2a82f85da57ad"
TARGET = Path("bwapi/include/BWAPI/Game.h")


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def apply(checkout: Path) -> dict[str, object]:
    target = checkout / TARGET
    data = target.read_bytes()
    before = git_blob_sha1(data)
    if before != BASE_BLOB:
        raise RuntimeError(f"BWAPI_GAME_H_PREIMAGE_DRIFT:{before}")

    crlf = b"#include <cstdarg>\r\n"
    lf = b"#include <cstdarg>\n"
    if crlf in data:
        needle = crlf
        replacement = crlf + b"#include <cstdint>\r\n"
    elif lf in data:
        needle = lf
        replacement = lf + b"#include <cstdint>\n"
    else:
        raise RuntimeError("BWAPI_GAME_H_INCLUDE_ANCHOR_MISSING")

    if data.count(needle) != 1:
        raise RuntimeError("BWAPI_GAME_H_INCLUDE_ANCHOR_NOT_UNIQUE")
    if b"#include <cstdint>" in data:
        raise RuntimeError("BWAPI_GAME_H_CSTDINT_ALREADY_PRESENT")

    patched = data.replace(needle, replacement, 1)
    after = git_blob_sha1(patched)
    if after != PATCHED_BLOB:
        raise RuntimeError(f"BWAPI_GAME_H_POSTIMAGE_DRIFT:{after}")

    target.write_bytes(patched)
    return {
        "upstream_pr": UPSTREAM_PR,
        "upstream_patch_commit": UPSTREAM_PATCH_COMMIT,
        "target": str(TARGET),
        "preimage_git_blob_sha1": before,
        "postimage_git_blob_sha1": after,
        "semantic_change": "add_missing_cstdint_include",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkout", required=True)
    args = parser.parse_args()
    result = apply(Path(args.checkout).resolve())
    for key, value in result.items():
        print(f"{key}={value}")
    print("OPENBW_BWAPI_CSTDINT_COMPAT_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
