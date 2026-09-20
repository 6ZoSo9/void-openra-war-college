# Scout repair V4: full-main composition and failed-start cleanup

## Outcome

The complete historical warm-start `main()` now runs under the scout binding in
an inert local integration fixture. Unlike V3's extracted-loop tests, this calls
the entire original function, including its warm-start recipes, round loop,
summary writer, and outer cleanup. No game engine or live host service is used.

A reproduced failure path is repaired in the **unpublished scout runner binding**.
The historical runner, helper, controller, host, mission planner, goal/effect core,
accepted repository source, and completed pair-03 evidence are not modified.
Thirteen of the fourteen V3 repository files remain byte-identical. This update
modifies the runner binding and adds this document and one new test file.

Publication is still unresolved after the earlier source-write rejection. No
alternate source-publication route was attempted. There is no new source commit,
branch, PR, hosted check, Precision installation, or approved new experiment.

## Reproduced failure, not an allegation about the completed run

The frozen runner calls `helper.start_ollama()` and sets its local
`ollama_started = True` only after that call returns. Its outer `finally` calls
`helper.cleanup()` only when that local flag is true. The retained helper can
start its service and then fail while waiting for its endpoint or verifying its
boundary. A partial failure therefore can leave helper effects without reaching
that outer cleanup call. The prior executor's readiness wrapper also calls its
original start before its own readiness-protection `try` block.

The original helper was inspected at Library source
`void-apollyon-openra-war-college-attested-run-v1_13.py`, whose bytes hash to the recorded
SHA-256 `72fb0e9909dcdddb6c4a7713a5aa55568d2bef43020e6478945ca69247590abc`.
It was **read and hash-verified, not executed**, in this continuation. The fixture below substitutes
its process/service/model backends rather than claiming real helper execution.

Before the repair, the new whole-main suite had **23 passes and 2 failures**:
an exception and a KeyboardInterrupt after simulated partial helper startup both
caused zero helper-cleanup calls. The original failed test log is retained.
This is a failure-path reproduction, not evidence that the earlier completed
Precision game suffered such a leak. Its recorded post-run checks remain intact.

## Repair inside the existing binding

When the already trusted Apollyon helper is loaded, the binding retains its
original start and cleanup callbacks and installs narrow in-memory wrappers.
No callback rewrites the underlying cleanup implementation or changes its command
scope. Installation itself does not start a service.

- Startup requires current caller authority and can be attempted only once,
  before the controller header. Permission is checked immediately before entering
  the supplied start callback.
- If startup raises, including an interrupt, the binding reaches the existing
  helper cleanup if none was observed through its wrapper during that call.
  Cleanup failure is retained separately without replacing the startup exception.
- Cleanup remains callable while the binding is held or authority has expired.
  Refusing new game work must not refuse teardown of already started work.
- An observed failed cleanup is not retried. If the startup callback privately
  called an earlier captured cleanup, that call is not observable by this counter:
  one fallback can repeat that teardown. A dedicated test demonstrates this limit;
  the supplied original helper must support idempotent cleanup. This is not a
  claim that every nested implementation makes exactly one cleanup call.

The same class now supplies `run_main_once()`. **This is an explicit operational
call to the supplied runner, not a read-only diagnostic.** An admitted caller
first installs a fresh binding and then uses this method for one main invocation.
The method restores its callbacks afterward and refuses re-entry. It does not
create source acceptance, authenticate an operator, or replace the required
external durable attempt guard.

The historical outer cleanup can itself raise before reaching helper teardown,
for example during Docker inspection. `run_main_once()` independently reaches
the saved helper cleanup if startup was attempted but no helper cleanup through
the binding occurred. A secondary cleanup or restoration error is retained in the
snapshot without replacing the exception that reached this method from main.
It does not recover an earlier exception already masked inside historical main.
Restoration still refuses to overwrite another callback replacement.

## Callback success is not shutdown proof

`main_lifecycle` and `helper_lifecycle` snapshots report attempted/returned
callbacks and sanitized error class names. Both explicitly retain
`actual_runtime_state_verified = False`.

Two characterizations make that distinction executable:

1. The historical runner writes a summary before teardown. A later Docker
   inspection failure leaves a summary on disk even though cleanup is incomplete.
2. The historical runner can print `engine_container_removed=true` after an
   unchecked nonzero removal result. A helper cleanup can likewise return without
   demonstrating actual service dormancy. Neither print nor callback return is
   promoted into verified cleanup by this binding.

The external caller still needs independent post-run service/permit/container,
worktree, baseline and source observations and a fresh experiment/result binding.
The old pair-03 launcher and consumed attempt are not reusable for this repair.
There is no new reset API, background runner, retry loop, container-removal
implementation, host command, or automatic evidence deletion in this addition.
Abrupt process kill, power loss and a hostile caller are outside these in-memory
exception-handling guarantees.

## What the full-main tests actually execute

The fixture imports the hash-matched historical sources:

- warm-start runner: `ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901`;
- joint host: `c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615`;
- controller: `b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103`.

Every statement in original `main()` is retained. The original warm-start recipes,
placement and reconciliation functions, typed Apollyon gate, Abaddon command gate,
`joint_advance`, `state_from_obs`, decision/result log writing, summary writing and
outer cleanup branches run. Actual file writes occur only in temporary directories.
The repair does not patch or AST-reconstruct main in these new tests.

A deliberately simple in-process world supplies synthetic typed observations:
construction is instantaneous after its specified test transitions; warm-start
movement is scripted, and controller scout movement is deliberately stationary.
It is **not OpenRA physics, not a learned simulator, and not a reconstruction of
unlogged historical production state**. The fake model returns scripted tools.
Git/source admission, Docker/systemd commands, helper startup/cleanup, session
transport, and generation/readiness backends are fixtures. Unmocked process and
socket creation raise assertions. The actual model endpoint, engine, sudo,
service manager, source loader and protobuf generator are never invoked.

The dynamically constructed protobuf fixture extends the prior message subset
with fields needed by the original observation converter and session/state calls.
Field numbers/types follow the inspected schema. It is not the complete generated
bridge package or a certification of real engine compatibility.

Cases cover one, three and 36 controller rounds; a programmed early terminal;
source/image/protocol/container/channel/daemon/session/player failures; warm and
controller logging failures; failed/mismatched/interrupted joint calls; state
query failure; startup and cleanup exceptions; permission loss; repeated start;
restoration conflicts; and no re-entry after the one main invocation. The complete
parsed warm-start logs from bound and unbound original main are equal after
removing only the header run ID.

Captured output from the unmodified main can contain its historical words
`actual`, `GREEN`, and cleanup booleans. They are **synthetic-fixture stdout**, not
new Precision, runtime, game-outcome or shutdown evidence.

## Actual verification

Python 3.13.5 / pytest 9.0.2 / protobuf 6.33.6 in the local workspace:

| Suite | Unique passing cases | Deselected |
|---|---:|---:|
| New whole-main/lifecycle tests | 41 | 0 |
| Existing runner-loop tests | 47 | 0 |
| Existing host-bridge tests | 51 | 0 |
| Existing mission tests | 45 | 0 |
| Combined repair package | **184** | **0** |
| Original pair-03 evidence reviewer, separately | **29** | **0** |

The same 184 cases are repeated from a clean archive extraction; that is not an
additional set of unique cases. Python-3.10 grammar parsing, in-memory compilation,
text whitespace and archive checksums are also checked. No actual Python 3.10,
3.11 or 3.12 execution, Ruff, full War College repository suite or hosted CI is
claimed. A read-only raw-source download failed DNS resolution; that failure is
retained, not described as a successful repository fetch.

This closes the local whole-main/exception-teardown composition gap under the
stated fixtures. It does not close publication, full-repository acceptance,
real readiness/post-run verification or authorization of a new live experiment.
No Precision command is supplied. Both completed runs and the used marker/result
remain unchanged; no new game, model inference, training, policy promotion,
scheduler change or funds action occurred.
