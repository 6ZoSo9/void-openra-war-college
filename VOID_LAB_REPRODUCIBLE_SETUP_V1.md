# VOID War College reproducible setup v1

This guide prepares and verifies one exact private-lab source composition. It
does not start OpenRA, invoke a model or provider, publish benchmark evidence,
or grant runtime authority.

## Bound identities

- War College source commit: `c164a7d2f4399a73bf3aaca411953a4a44222fed`
- preserved War College comparison point: `973802ef0a614e5afa782ff20e231e18966ae3e5`
- preserved engine commit and gitlink: `1607a7a6501d42a47638393ecef8b22831064932`
- generation: `ad1926569b12466c`
- checkout receipt schema: `6`

The source commit is a reproducible candidate composition, not a protected
baseline. The preserved comparison point, engine commit, generation, and any
`runtime-proven/ad1926569b12466c` refs must not be rewritten or repurposed.

## Preconditions

- Use a GNU/Linux host with POSIX `sh` semantics. This generation is tested on
  Ubuntu 24.04 and requires `uname`, Python 3.10 or newer, Git, `awk`,
  `dirname`, `ln`, `mktemp`, `rm`, `sha256sum`, `stat`, and `sync`
  with the option semantics proved by the preflight below.
- The operator already has authorized read access to both private repositories.
- The repository URL is supplied through existing Git configuration or a local
  environment variable. Do not place credentials in commands, files, receipts,
  shell history, or logs.
- Choose a new empty destination. Do not reuse a working tree that contains
  build products, runtime files, benchmark results, or local source changes.

Run this prerequisite wall before choosing or creating the checkout destination. It
uses only a disposable temporary directory and must complete before clone,
submodule, receipt, build, or benchmark mutation:

```bash
# VOID_LAB_HOST_PREFLIGHT_V1_BEGIN
void_require_lab_setup_host() (
  set -eu
  for command in uname python3 git awk dirname ln mktemp rm sha256sum stat sync; do
    command -v "$command" >/dev/null 2>&1 || exit 70
  done
  test "$(uname -s)" = 'Linux' || exit 70
  python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 70)' || exit 70
  git --version >/dev/null || exit 70
  VOID_LAB_PREFLIGHT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/void-lab-prereq.XXXXXX")" || exit 70
  cleanup_preflight() {
    rm -rf -- "$VOID_LAB_PREFLIGHT_DIR"
  }
  trap cleanup_preflight EXIT HUP INT TERM
  printf 'probe\n' > "$VOID_LAB_PREFLIGHT_DIR/source" || exit 70
  ln -- "$VOID_LAB_PREFLIGHT_DIR/source" "$VOID_LAB_PREFLIGHT_DIR/link" || exit 70
  VOID_LAB_PREFLIGHT_SOURCE_ID="$(stat -c '%d:%i' "$VOID_LAB_PREFLIGHT_DIR/source")" || exit 70
  VOID_LAB_PREFLIGHT_LINK_ID="$(stat -c '%d:%i' "$VOID_LAB_PREFLIGHT_DIR/link")" || exit 70
  test "$VOID_LAB_PREFLIGHT_SOURCE_ID" = "$VOID_LAB_PREFLIGHT_LINK_ID" || exit 70
  test "$(dirname -- "$VOID_LAB_PREFLIGHT_DIR/source")" = "$VOID_LAB_PREFLIGHT_DIR" || exit 70
  test "$(printf 'left right\n' | awk '{print $2}')" = 'right' || exit 70
  sha256sum "$VOID_LAB_PREFLIGHT_DIR/source" | awk 'NF == 2 && $2 ~ /source$/ { ok=1 } END { exit ok ? 0 : 1 }' || exit 70
  sync -f "$VOID_LAB_PREFLIGHT_DIR" || exit 70
  rm -- "$VOID_LAB_PREFLIGHT_DIR/link" || exit 70
  test ! -e "$VOID_LAB_PREFLIGHT_DIR/link" || exit 70
)
void_require_lab_setup_host || {
  printf '%s\n' 'HOLD_VOID_LAB_SETUP_HOST_PREREQUISITES' >&2
  exit 70
}
# VOID_LAB_HOST_PREFLIGHT_V1_END
```

Set only non-secret local variables:

```bash
export VOID_WAR_COLLEGE_REPOSITORY='<authorized-private-repository-url>'
export VOID_WAR_COLLEGE_DIR="$HOME/dev/void-openra-war-college-c164a7d2"
export VOID_WAR_COLLEGE_COMMIT='c164a7d2f4399a73bf3aaca411953a4a44222fed'
export VOID_WAR_COLLEGE_FROZEN='973802ef0a614e5afa782ff20e231e18966ae3e5'
export VOID_ENGINE_COMMIT='1607a7a6501d42a47638393ecef8b22831064932'
export VOID_LAB_GENERATION='ad1926569b12466c'
```

Stop if the destination already exists:

```bash
test ! -e "$VOID_WAR_COLLEGE_DIR"
```

## Exact detached checkout

Clone without selecting a moving branch, fetch the exact candidate, and detach
at that commit:

```bash
git clone --no-checkout "$VOID_WAR_COLLEGE_REPOSITORY" "$VOID_WAR_COLLEGE_DIR"
git -C "$VOID_WAR_COLLEGE_DIR" fetch --no-tags origin "$VOID_WAR_COLLEGE_COMMIT"
git -C "$VOID_WAR_COLLEGE_DIR" checkout --detach "$VOID_WAR_COLLEGE_COMMIT"
```

Initialize only the reviewed `OpenRA` gitlink. Do not use recursive initialization
for unrelated future submodules:

```bash
git -C "$VOID_WAR_COLLEGE_DIR" submodule sync -- OpenRA
git -C "$VOID_WAR_COLLEGE_DIR" submodule update --init --depth 1 -- OpenRA
```

Do not run `git pull`, check out a moving branch, edit `.gitmodules`, alter global
Git configuration, or replace the `OpenRA` checkout to make a mismatch pass.

## Independent identity wall

Every command below must succeed before the checkout verifier is allowed to
classify the composition:

```bash
test "$(git -C "$VOID_WAR_COLLEGE_DIR" rev-parse HEAD)" = "$VOID_WAR_COLLEGE_COMMIT"
test "$(git -C "$VOID_WAR_COLLEGE_DIR" ls-tree HEAD -- OpenRA | awk '{print $3}')" = "$VOID_ENGINE_COMMIT"
test "$(git -C "$VOID_WAR_COLLEGE_DIR/OpenRA" rev-parse HEAD)" = "$VOID_ENGINE_COMMIT"
git -C "$VOID_WAR_COLLEGE_DIR" merge-base --is-ancestor "$VOID_WAR_COLLEGE_FROZEN" "$VOID_WAR_COLLEGE_COMMIT"
test "$VOID_LAB_GENERATION" = 'ad1926569b12466c'
```

Any mismatch is a terminal HOLD. Do not fetch a substitute commit, rewrite a
baseline ref, or continue to build or benchmark.

## Exact checkout receipt

The default verifier checks both worktrees, including ordinary untracked files,
reviewed ignored runtime/build inputs, and stable initial/final snapshots. Give
each verification attempt a new explicit identifier and publish its single JSON
record create-only. Attempt identifiers are non-secret lowercase labels, not
timestamps or inferred mutable state. A pre-existing receipt for the selected
identifier is a terminal HOLD and must remain byte-for-byte untouched:

```bash
void_publish_lab_receipt() (
  set -eu
  umask 077
  test "$#" -eq 1
  VOID_LAB_RECEIPT_ID="$1"
  python -c 'import re,sys; raise SystemExit(0 if re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", sys.argv[1]) else 2)' "$VOID_LAB_RECEIPT_ID"
  VOID_LAB_RECEIPT="$VOID_WAR_COLLEGE_DIR/../void-lab-checkout-c164a7d2-$VOID_LAB_RECEIPT_ID.json"
  VOID_LAB_RECEIPT_DIR="$(dirname -- "$VOID_LAB_RECEIPT")"
  test -d "$VOID_LAB_RECEIPT_DIR"
  test ! -e "$VOID_LAB_RECEIPT"
  test ! -L "$VOID_LAB_RECEIPT"
  VOID_LAB_RECEIPT_TEMP="$(mktemp "$VOID_LAB_RECEIPT_DIR/.void-lab-checkout-$VOID_LAB_RECEIPT_ID.XXXXXX.pending")"
  VOID_LAB_RECEIPT_TEMP_ID="$(stat -c '%d:%i' "$VOID_LAB_RECEIPT_TEMP")"
  report_retained_temp() {
    if [ -n "${VOID_LAB_RECEIPT_TEMP:-}" ]; then
      printf 'receipt_staging_path=%s\npending_retired=false\nstaging_cleanup=DEFERRED_NO_PATHNAME_DELETE\n' \
        "$VOID_LAB_RECEIPT_TEMP" >&2
    fi
  }
  trap report_retained_temp EXIT
  python "$VOID_WAR_COLLEGE_DIR/scripts/verify_void_lab_checkout_v1.py" \
    --repo-root "$VOID_WAR_COLLEGE_DIR" > "$VOID_LAB_RECEIPT_TEMP"
  test -f "$VOID_LAB_RECEIPT_TEMP"
  test ! -L "$VOID_LAB_RECEIPT_TEMP"
  test "$(stat -c '%a' "$VOID_LAB_RECEIPT_TEMP")" = '600'
  python -c 'import json,sys; d=json.load(open(sys.argv[1], encoding="utf-8")); assert d["schema_version"] == 6; assert d["generation"] == "ad1926569b12466c"; assert d["source_contract"] == "GREEN"; assert d["checkout_contract"] == "GREEN"; assert d["exact_checkout_evidence"] is True; assert d["runtime_evidence"] == "PENDING_DESIGNATED_HOST"' "$VOID_LAB_RECEIPT_TEMP"
  ln -- "$VOID_LAB_RECEIPT_TEMP" "$VOID_LAB_RECEIPT"
  test -f "$VOID_LAB_RECEIPT"
  test ! -L "$VOID_LAB_RECEIPT"
  test "$(stat -c '%a' "$VOID_LAB_RECEIPT")" = '600'
  test "$(stat -c '%d:%i' "$VOID_LAB_RECEIPT")" = "$VOID_LAB_RECEIPT_TEMP_ID"
  sync -f "$VOID_LAB_RECEIPT_DIR"
  printf 'receipt_id=%s\nreceipt_path=%s\n' "$VOID_LAB_RECEIPT_ID" "$VOID_LAB_RECEIPT"
  sha256sum "$VOID_LAB_RECEIPT"
)
void_publish_lab_receipt setup-001
```

Keep the receipt outside the repository so it does not make the exact worktree
dirty. The hard-link publication is create-only even if another process creates
the destination after the initial preflight. This generation deliberately keeps
the owner-only staging alias after publication and performs no pathname cleanup.
The function reports `receipt_staging_path`, `pending_retired=false`, and
`staging_cleanup=DEFERRED_NO_PATHNAME_DELETE` on success and on verifier exits
after staging creation. This removes check-then-unlink authority: a same-UID
replacement at the staging pathname cannot be deleted by this workflow, and
staging retirement cannot reverse the validated final receipt.

One attempt creates at most one discoverable staging alias whose name includes
the explicit attempt identifier. Preserve it for bounded reconciliation; do not
delete, rename, chmod, or reuse it through this evidence-creation function.
Staging retirement requires a separately reviewed generation-conditional
primitive or explicit operator reconciliation outside this contract. A verifier
or validation failure cannot truncate an earlier receipt. Record the receipt
identifier, final path, staging path, `pending_retired=false`, and final SHA-256
with any later designated-host evidence. Retain earlier receipts; never delete,
rename, chmod, or replace one to reuse its identifier. Do not treat
`--source-only` GREEN, unit tests, or hosted CI as exact designated-host checkout
evidence.

## Handoff boundary

A GREEN checkout receipt proves only the sampled pre-runtime composition. Before
any later build or benchmark, the designated operator must re-run the default
verifier against the same detached checkout with a new identifier, for example:

```bash
void_publish_lab_receipt prebuild-001
```

Bind that exact new receipt identifier, path, and digest to the exact command and
resulting evidence. The earlier `setup-001` receipt remains immutable evidence;
the later command is authorized only by its named `prebuild-001` receipt. If
either worktree changes, repeat the entire identity wall and verifier with
another new identifier; never reuse or remove an earlier GREEN receipt.

`runtime_evidence=PENDING_DESIGNATED_HOST`
