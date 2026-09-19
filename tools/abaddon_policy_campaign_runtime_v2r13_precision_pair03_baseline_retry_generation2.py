#!/usr/bin/env python3
"""CLI for the single authorized V2R13 pair-03 baseline retry."""

from __future__ import annotations

import argparse
import json
import sys

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_invocation_generation2
    as retry,
)

MARK = "VOID_ABADDON_GENERATION2_V2R13_PRECISION_PAIR03_BASELINE_RETRY_V1"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print(MARK)
    print("pair_slot=3")
    print("arm=baseline")
    print("retry_index=1")
    print("max_retry_executions=1")
    print("automatic_retry=false")
    print("candidate_arm=false")
    print("held_out_arm=false")
    print("training=false")
    print("weights_updated=false")
    print("automatic_policy_promotion=false")
    print("deployment=false")
    print("void_chain_mutation=false")
    print("wallet_or_funds_action=false")
    try:
        receipt = retry.execute_pair03_baseline_retry(confirm=args.confirm)
    except Exception as error:
        print(f"{MARK}_HOLD", file=sys.stderr)
        print(f"blocker={type(error).__name__}:{error}", file=sys.stderr)
        return 2

    print(
        "retry_receipt_json="
        + json.dumps(receipt, sort_keys=True, separators=(",", ":"), default=str)
    )
    print(
        "retry_invocation_receipt_sha256="
        f"{receipt['retry_invocation_receipt_sha256']}"
    )
    print(f"next_gate={receipt['next_gate']}")
    print(f"{MARK}_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
