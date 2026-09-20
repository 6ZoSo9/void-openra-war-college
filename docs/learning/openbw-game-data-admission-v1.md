# OpenBW local game-data admission V1

## Purpose

Create a reproducible **read-only identity record** for an operator-selected
local Brood War data root and map before any OpenBW match is considered.

This is not an asset downloader, installer, copy tool, license determination,
or game launcher.

## Explicit inputs

The operator supplies:

- one existing local game-data root;
- one map path relative to that root;
- the explicit confirmation string
  `VOID_OPENBW_LOCAL_GAME_DATA_RIGHTS_REVIEWED`.

That confirmation means only that the operator has personally reviewed the
license/ownership basis for using those local files. The tool does not make a
legal determination.

## Files admitted

Exactly these game-data filenames are opened beneath the supplied root:

- `Stardat.mpq`
- `Broodat.mpq`
- `Patch_rt.mpq`

The map is opened only at the exact relative path supplied by the operator.

The tool does not search the filesystem for installations or maps.

## Filesystem boundary

All path components beneath the selected root are opened without following
symlinks. Final targets must be ordinary regular files.

For each file the tool:

1. records stable file identity;
2. hashes from a retained read-only descriptor;
3. enforces a byte bound;
4. verifies byte count;
5. verifies file identity is unchanged after hashing.

It writes nothing. The result is printed to stdout only.

## Output

The receipt uses
`void.war-college.openbw-neutral-duel-runtime-admission.v1` and contains:

- SHA-256 and byte size for all three MPQs;
- selected relative map path, SHA-256, and byte size;
- the explicit operator rights-review fact;
- no-authority flags.

The existing neutral-duel harness validator checks the receipt shape and still
returns:

- `runtime_authorized=false`;
- `game_execution_authorized=false`.

## Next gate

Even a valid asset receipt does not launch OpenBW.

The next gate is a separate source-bound dual-process invocation plus a
**separate explicit authorization for one neutral smoke match**.

No Apollyon/Abaddon binding, model execution, training, corpus admission, or
policy promotion is created here.
