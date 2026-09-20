# Contributing to VOID OpenRA War College

Thank you for contributing.

This repository contains both upstream GPL-covered work and downstream VOID
Network work. Contributions must preserve that distinction.

## License and provenance

Before submitting code or documentation, identify its provenance:

1. **Original contribution** — work you have the right to contribute.
2. **Modified repository material** — derived from an existing file in this
   repository; preserve its existing notices and license.
3. **Upstream or third-party material** — identify the source and applicable
   license. Do not remove or replace upstream copyright notices.

Do not copy code into this repository unless its license is compatible with the
repository and you have the right to contribute it.

## New original VOID-authored source

New source files authored specifically as VOID OpenRA War College downstream
work should normally include, using the file's comment syntax:

```text
Copyright (c) 2026 6ZoSo9 and VOID Network contributors.
GPLv3 section 7 attribution/origin terms:
see /VOID_NETWORK_GPL_ATTRIBUTION_TERMS.md
```

This notice applies only where the copyright holder has the right to add those
terms. Do not add it to copied upstream files, generated third-party code,
historical fixtures, or material whose copyright belongs to someone else.

Existing hash-bound files are not to be mass-reheadered. Source-identity and
reproducibility migrations require separate review.

## Credit

Human contributors retain credit through Git authorship, pull-request history,
source notices, and the project credit files.

Do not remove or falsify authorship, provenance, copyright, or modification
notices.

See:

- `AUTHORS.md`
- `NOTICE`
- `VOID_PROVENANCE.md`
- `THIRD_PARTY_NOTICES.md`
- `VOID_NETWORK_GPL_ATTRIBUTION_TERMS.md`

## GPL compatibility

The repository remains GNU GPLv3-covered. Do not add restrictions that prohibit
redistribution, commercial use, hosting, SaaS, or forks of GPL-covered code.

Project names and branding are separate from copyright licensing. See
`docs/legal/TRADEMARKS.md`.

## Pull requests

Each pull request should state:

- what was changed;
- whether the change is original, modified repository material, or imported;
- any external source and license;
- whether existing copyright/license notices were preserved;
- whether new original VOID-owned source carries the attribution pointer;
- whether exact source hashes, fixtures, or reproducibility bindings are affected.

Runtime, model, game, deployment, funds, wallet, or network actions must be
declared separately from source-only changes.
