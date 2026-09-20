# Darwin maintenance audit v1

## Source binding

- Repository: `6ZoSo9/void-openra-war-college`
- Original audited `main`: `b51137277ab5b17631712ecd035af85d4b8d81c8`
- Current integration base: `1c9683a207c67e74afbc08a9373973c4a9e0bba7`
- Audit mode: source-only; no game execution, training, model loading, weight update, promotion, deployment, service action, VOID mutation, credentials, wallets, transactions, or funds action.

## Live capability audit

The accepted Generation-2 source on this head separates deterministic source contracts from runtime authority. In particular, the merged isolated-workdir allocator review under `openra_env/learning/` preserves the unresolved `<GENERATION2_ISOLATED_WORKDIR_ROOT>` boundary, validates deterministic allocation identities, and leaves runtime execution authorization outside the source-only layer.

The pair-03 retry-gate chain remains outside this maintenance change. The retry-2 evidence/result chain through #171, CI merge-parent binder #172, deterministic review-test memoization #173, and pair-03 candidate execution preparation #174 are merged into `main`; active #175/#176 use disjoint CI-diagnostics and candidate-request paths.

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
14. rejects interpreter-native host-capability backends (`_io`, `_socket`, `_ctypes`, `_posixsubprocess`, `posix`, and `nt`) before lower-level file, network, foreign-function, process, or operating-system authority can bypass the higher-level module denylist.
15. rejects code-object reconstruction through `marshal` and `types` before deserialized bytecode can be wrapped as a callable and invoked without a direct `exec` call.
16. rejects lower-level POSIX process, memory, descriptor, signal, and terminal authority through `fcntl`, `mmap`, `pty`, `resource`, `signal`, and `termios`.
17. rejects terminal-input and network/descriptor I/O primitives through `getpass`, `readline`, `select`, `selectors`, and `ssl` before reviewed source can solicit secrets, install interactive hooks, multiplex host descriptors, or create network/TLS contexts.
18. rejects persistence and archive file-capability helpers through `dbm`, `shelve`, `sqlite3`, `tarfile`, and `zipfile` before reviewed source can create durable databases or read, write, or extract host archives.
19. rejects protocol-specific network clients and servers through `ftplib`, `imaplib`, `nntplib`, `poplib`, `smtplib`, `socketserver`, `telnetlib`, and `xmlrpc` before reviewed source can open network sessions without importing `socket` directly.
20. rejects debugger, profiler, doctest, and trace execution surfaces through `bdb`, `cProfile`, `doctest`, `pdb`, `profile`, and `trace` before reviewed source can execute source strings or recover debugger authority without spelling `exec` directly.
21. rejects standard-library module discovery and loader surfaces through `modulefinder`, `pkgutil`, `site`, and `zipimport` before reviewed source can locate, load, or execute modules without spelling `importlib` directly.
22. rejects interpreter packaging and compilation surfaces through `compileall`, `ensurepip`, `py_compile`, `venv`, and `zipapp` before reviewed source can write bytecode or archives, bootstrap package tooling, or create execution environments.
23. rejects implicit host-file opening through `bz2`, `configparser`, `fileinput`, `gzip`, `logging`, `lzma`, `mailbox`, and `wave` before reviewed source can read, create, replace, or append host files without importing `open`, `io`, `os`, or `pathlib` directly.

The guard should operate only on committed source and AST/contract output. It must not import modules that can perform host I/O, start a runtime, contact a provider, load a model, or execute a game. The first implementation should exclude the overlapping #148–#152 files until that stack lands, then bind them in a follow-up exact-head update.

## Exit condition

This audit is complete when the static guard and its negative fixture are committed on a new collision-checked branch, exercised by CI without runtime execution, and the protected module census is bound to an exact source head.
