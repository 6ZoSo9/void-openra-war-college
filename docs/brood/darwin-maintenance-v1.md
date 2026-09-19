# Darwin maintenance audit v1

## Source binding

- Repository: `6ZoSo9/void-openra-war-college`
- Original audited `main`: `b51137277ab5b17631712ecd035af85d4b8d81c8`
- Current integration base: `59a39ce69826ba937bfaf004fed43a28b030aec4`
- Audit mode: source-only; no game execution, training, model loading, weight update, promotion, deployment, service action, VOID mutation, credentials, wallets, transactions, or funds action.

## Live capability audit

The accepted Generation-2 source on this head separates deterministic source contracts from runtime authority. In particular, the merged isolated-workdir allocator review under `openra_env/learning/` preserves the unresolved `<GENERATION2_ISOLATED_WORKDIR_ROOT>` boundary, validates deterministic allocation identities, and leaves runtime execution authorization outside the source-only layer.

The pair-03 retry-gate chain remains outside this maintenance change. PRs #148–#164 have merged into `main`; no overlapping active pull request is attributed to this lane.

## Actionable improvement

Add a dedicated static CI guard that enumerates Generation-2 runtime-gated modules and fails closed unless each module:

1. keeps runtime, process-spawn, game-execution, training, weight-update, promotion, deployment, VOID-chain, wallet, and funds capabilities false by default;
2. exposes a named next gate instead of silently enabling an action;
3. retains source-binding tests for exact dependency identities and rejects relative local imports rather than silently omitting them; and
4. rejects a fixture that flips any protected capability flag or replaces an authority-held entrypoint with an executable path; and
5. rejects indirect host-execution imports through `builtins` or dynamic module loading through `importlib`; and
6. rejects builtin-namespace, function-global introspection, and `pathlib`/`sys` filesystem escape surfaces; and
7. rejects aliases of forbidden builtin capabilities before the aliased call can hide their authority;
8. rejects bare local-package imports whose reachable submodules cannot be deterministically enumerated; and
9. rejects traceback, frame, generator, coroutine, code-object, and closure introspection paths that can recover builtin or global capabilities without naming a forbidden builtin directly; and
10. rejects reflective attribute dispatch through `object.__getattribute__`, `type.__getattribute__`, or `__getattr__` before string-selected globals, builtins, classes, or MRO state can escape the static surface; and
11. rejects reflective helper modules (`operator`, `inspect`, and `gc`) plus interactive builtins (`breakpoint`, `input`, and `help`) that can recover or invoke host capabilities without spelling a previously forbidden call.
12. rejects standard-library host-capability helpers (`code`, `codeop`, `concurrent`, `io`, `pickle`, `pydoc`, `runpy`, and `webbrowser`) before they can execute source, open host files, deserialize executable reducers, spawn workers, enter an interactive console, or launch a browser.
13. rejects import-loader introspection through `__loader__`, `__spec__`, and loader dispatch methods before a permitted module can recover dynamic module-loading authority.

The guard should operate only on committed source and AST/contract output. It must not import modules that can perform host I/O, start a runtime, contact a provider, load a model, or execute a game. The first implementation should exclude the overlapping #148–#152 files until that stack lands, then bind them in a follow-up exact-head update.

## Exit condition

This audit is complete when the static guard and its negative fixture are committed on a new collision-checked branch, exercised by CI without runtime execution, and the protected module census is bound to an exact source head.
