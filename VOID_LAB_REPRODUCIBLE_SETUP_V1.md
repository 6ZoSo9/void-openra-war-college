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

- Python 3.10 or newer and Git are already installed.
- The operator already has authorized read access to both private repositories.
- The repository URL is supplied through existing Git configuration or a local
  environment variable. Do not place credentials in commands, files, receipts,
  shell history, or logs.
- Choose a new empty destination. Do not reuse a working tree that contains
  build products, runtime files, benchmark results, or local source changes.

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
reviewed ignored runtime/build inputs, and stable initial/final snapshots. Write
its single JSON record with owner-only permissions and validate the terminal:

```bash
umask 077
export VOID_LAB_RECEIPT="$VOID_WAR_COLLEGE_DIR/../void-lab-checkout-c164a7d2.json"
python "$VOID_WAR_COLLEGE_DIR/scripts/verify_void_lab_checkout_v1.py" \
  --repo-root "$VOID_WAR_COLLEGE_DIR" > "$VOID_LAB_RECEIPT"
python -c 'import json,sys; d=json.load(open(sys.argv[1], encoding="utf-8")); assert d["schema_version"] == 6; assert d["generation"] == "ad1926569b12466c"; assert d["source_contract"] == "GREEN"; assert d["checkout_contract"] == "GREEN"; assert d["exact_checkout_evidence"] is True; assert d["runtime_evidence"] == "PENDING_DESIGNATED_HOST"' "$VOID_LAB_RECEIPT"
sha256sum "$VOID_LAB_RECEIPT"
```

Keep the receipt outside the repository so it does not make the exact worktree
dirty. Record its SHA-256 with any later designated-host evidence. Do not treat
`--source-only` GREEN, unit tests, or hosted CI as exact designated-host checkout
evidence.

## Handoff boundary

A GREEN checkout receipt proves only the sampled pre-runtime composition. Before
any later build or benchmark, the designated operator must re-run the default
verifier against the same detached checkout and bind the new receipt digest to
the exact command and resulting evidence. If either worktree changes, repeat the
entire identity wall and verifier; never reuse an earlier GREEN receipt.

`runtime_evidence=PENDING_DESIGNATED_HOST`

