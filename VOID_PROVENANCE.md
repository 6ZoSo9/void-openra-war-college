# VOID OpenRA War College Provenance Record

This document records downstream project provenance without changing the
license of any source file or claiming ownership of third-party material.

## Upstream baseline

Primary Python upstream reference:

- https://github.com/yxc20089/OpenRA-RL

Engine upstream reference:

- https://github.com/OpenRA/OpenRA

VOID engine fork/submodule:

- https://github.com/6ZoSo9/void-openra-engine

## Downstream-only project areas

As reviewed on 2026-09-20, the following directories exist in
`6ZoSo9/void-openra-war-college` but do not exist on the current
`yxc20089/OpenRA-RL` `main` branch:

- `openra_env/learning/`
- `docs/learning/`

These areas contain substantial downstream War College work, including policy
campaigns, controller contracts, source/runtime bindings, experiment gates,
evidence contracts, and associated design documentation.

Their absence from the current upstream tree is provenance evidence that these
paths are downstream additions. It is **not**, by itself, a claim that VOID
Network contributors own every byte that may appear inside them.

In particular:

- copied historical fixtures retain their original copyright;
- exact upstream source excerpts retain upstream copyright;
- generated protocol material remains subject to the rights and license of its
  source;
- third-party quotations, assets, libraries, and dependencies retain their own
  rights.

Original copyrightable expression authored by 6ZoSo9 / VOID Network
contributors within downstream-added material remains attributed to those
contributors.

## Git history as evidence

The repository commit graph, pull-request history, exact Git blobs, source hashes,
test fixtures, and dated design/evidence documents provide the authoritative
technical record for when downstream material entered the project.

This provenance record is intended to make that authorship history explicit,
not to replace Git history or expand copyright beyond material actually authored
by VOID Network contributors.

## Licensing relationship

The repository remains GNU GPLv3-covered. OpenRA's separate engine terms remain
GPLv3-or-later upstream.

For designated VOID-owned source files that explicitly point to
`VOID_NETWORK_GPL_ATTRIBUTION_TERMS.md`, the narrow GPLv3 section 7
attribution/origin terms in that document apply.

Existing hash-bound source is not mechanically modified merely to add headers,
because doing so would destroy accepted source identities and reproducibility.
