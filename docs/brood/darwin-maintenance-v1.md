# Darwin maintenance audit v1

## Source binding

- Repository: `6ZoSo9/void-openra-war-college`
- Original audited `main`: `b51137277ab5b17631712ecd035af85d4b8d81c8`
- Current integration base after retry-gate merges: `78e136ee30721ca1e2823c1cef037dd867b8ea6b`
- Audit mode: source-only; no game execution, training, model loading, weight update, promotion, deployment, service action, VOID mutation, credentials, wallets, transactions, or funds action.

## Live capability audit

The accepted Generation-2 source on this head separates deterministic source contracts from runtime authority. In particular, the merged isolated-workdir allocator review under `openra_env/learning/` preserves the unresolved `<GENERATION2_ISOLATED_WORKDIR_ROOT>` boundary, validates deterministic allocation identities, and leaves runtime execution authorization outside the source-only layer.

The pair-03 retry-gate chain remains outside this maintenance change. PRs #148–#150 have merged into `main`; #151–#152 remain the active retry invocation/review stack. Those runtime paths are intentionally not modified here.

## Actionable improvement

Add a dedicated static CI guard that enumerates Generation-2 runtime-gated modules and fails closed unless each module:

1. keeps runtime, process-spawn, game-execution, training, weight-update, promotion, deployment, VOID-chain, wallet, and funds capabilities false by default;
2. exposes a named next gate instead of silently enabling an action;
3. retains source-binding tests for exact dependency identities; and
4. rejects a fixture that flips any protected capability flag or replaces an authority-held entrypoint with an executable path.

The guard should operate only on committed source and AST/contract output. It must not import modules that can perform host I/O, start a runtime, contact a provider, load a model, or execute a game. The first implementation should exclude the overlapping #148–#152 files until that stack lands, then bind them in a follow-up exact-head update.

## Exit condition

This audit is complete when the static guard and its negative fixture are committed on a new collision-checked branch, exercised by CI without runtime execution, and the protected module census is bound to an exact source head.
