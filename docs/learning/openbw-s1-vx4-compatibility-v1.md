# OpenBW S1 VX4/VX4EX compatibility v1

This lane records the source-level compatibility contract derived from the
Precision OpenBW/S1 acceptance work. It is intentionally source-only: importing
or testing it does not open CASC, launch OpenBW, run StarCraft, load a bot, train
a model, or mutate the War College runtime.

## Accepted observations

The pinned upstream sources are OpenBW
`4b046d5f65302b10cb0a745f0fecd37ec85b20a8`, BWAPI
`48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`, and CascLib
`2a280f5a231966dc5d1b534978dd9f9f04a374cd`.

The S1 catalog observed on Precision identified modern `*.vx4ex` tileset files
and no classic `*.vx4` entries. Badlands `TileSet\badlands.vx4ex` was 395,008
bytes: 6,172 64-byte records containing 98,752 little-endian u32 entries. The
maximum raw entry was 94,988, which resolves to VR4 index 47,494; the Badlands
VR4 payload contains 47,495 records. This proves that narrowing modern entries to
u16 is lossy and that the low-bit flip / `raw / 2` index interpretation remains
internally consistent.

The runtime acceptance lane subsequently initialized all eight StarCraft
tilesets through the patched OpenBW loader, then executed a bounded single
OpenBW game and a bounded two-instance local socketpair game. The dual run used
a test-only lobby adaptation because every one of the 11 pinned BWAPI test maps
contains exactly one open-human slot. That lobby adaptation is not part of this
production compatibility contract.

## Canonical representation

The internal canonical representation is one 64-byte record containing 16
little-endian u32 words.

- Modern VX4EX already uses that representation and is retained byte-for-byte.
- Classic VX4 uses one 32-byte record containing 16 little-endian u16 words.
  Each word is widened to u32 without changing its numeric value.
- The low bit remains the horizontal-flip bit.
- `raw / 2` remains the VR4 bitmap index.
- Modern lengths must be divisible by 64; classic lengths must be divisible by
  32. Malformed streams fail closed.

## Open/fallback policy

For an OpenBW request ending in `.vx4`:

1. Try the corresponding `.vx4ex` name first.
2. If that open succeeds, parse it as modern u32 records.
3. If and only if the modern open fails with exact file-not-found (`ENOENT` on
   Linux / `ERROR_FILE_NOT_FOUND` in the CascLib abstraction), try the original
   classic `.vx4` name.
4. Any other modern open error is terminal and must not be hidden by fallback.
5. A classic fallback open failure is terminal.
6. Non-VX4 files are opened exactly once under their requested names and pass
   through unchanged.

The pinned CascLib API exposes `GetCascError()`, and its Linux port maps
`ERROR_FILE_NOT_FOUND` to `ENOENT`. The eventual bridge must surface that last
open error so the adapter can implement this exact discrimination.

## Boundaries

This commit is a deterministic semantic contract and regression surface. It does
not yet wire CascLib/OpenBW into the repository build, does not promote the
Precision test-only lobby-slot adaptation, and does not claim full StarCraft
binary compatibility. The next source gate is the deterministic bridge/patch
builder that consumes this contract while retaining exact upstream pins.
