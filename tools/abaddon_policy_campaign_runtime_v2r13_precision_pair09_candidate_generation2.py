#!/usr/bin/env python3
"""Precision CLI for one explicitly authorized V2R13 pair-09 candidate arm."""

from __future__ import annotations

import argparse
import json
import sys

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_invocation_generation2
    as invocation,
)

MARK = "VOID_ABADDON_GENERATION2_V2R13_PRECISION_PAIR09_CANDIDATE_V1"
INVOCATION_SOURCE_SHA256 = (
    "4858f3fe148829d050604746cd64fa426963370a71029f95d7cc40bb71b5ba7c"
)
AUTHORIZATION_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_AUTHORIZE_PAIR09_CANDIDATE_ONCE"
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-main-head", required=True)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--confirm", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    print(MARK)
    print("pair_slot=9")
    print("arm=candidate")
    print("held_out=false")
    print("single_use_attempt=true")
    print("automatic_retry=false")
    print("baseline_rerun=false")
    print("held_out_execution=false")
    print("training=false")
    print("weights_updated=false")
    print("policy_promotion=false")
    print("deployment=false")
    print("void_chain_mutation=false")
    print("wallet_or_funds_action=false")
    print(f"expected_main_head={args.expected_main_head}")
    print(f"invocation_source_sha256={INVOCATION_SOURCE_SHA256}")

    if args.authorization != AUTHORIZATION_TOKEN:
        print(f"{MARK}_HOLD", file=sys.stderr)
        print(
            "blocker=PAIR09_CANDIDATE_SPECIFIC_AUTHORIZATION_REQUIRED",
            file=sys.stderr,
        )
        return 2

    try:
        receipt = invocation.execute_pair09_candidate(
            expected_main_head=args.expected_main_head,
            expected_invocation_source_sha256=INVOCATION_SOURCE_SHA256,
            authorization_accepted=True,
            confirm=args.confirm,
        )
    except Exception as error:
        print(f"{MARK}_HOLD", file=sys.stderr)
        print(
            f"blocker={type(error).__name__}:{error}",
            file=sys.stderr,
        )
        return 2

    print(
        "invocation_receipt_json="
        + json.dumps(
            receipt,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
    )
    print(
        "pair09_candidate_execution_performed="
        + str(
            receipt["pair09_candidate_execution_performed"]
        ).lower()
    )
    print(f"result_file={receipt['result_file']}")
    print(f"result_file_sha256={receipt['result_file_sha256']}")
    print(f"{MARK}_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
