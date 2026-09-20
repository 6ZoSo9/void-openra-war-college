"""Exact frozen controller-loop statements with inert model/transport inputs.

The full historical main, startup, service, loader and network are never called.
Only the exact controller for-loop is extracted with AST and executed here.
No observations from the historical match are padded to create these fixtures.
"""
from copy import deepcopy
import ast
import hashlib
import json
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from test_abaddon_scout_host_bridge_v1 import (
    InertStub, bridge, host, legacy, load_fixture, observation, pb,
)
from openra_env.learning.abaddon_scout_runner_binding_v1 import (
    CONTROLLER_SHA256, EVIDENCE_KEY, ScoutMissionRunnerBinding, ScoutRunnerHold,
)

# Imported names are pytest fixtures, not additional copies of their test cases.
ROOT = Path(__file__).resolve().parents[1]
RUNNER_SHA = 'ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901'
RUN_ID = 'synthetic-new-scout-experiment'
SEED = 1990061685


@pytest.fixture(scope='module')
def warm():
    return load_fixture('warm_start_runner_v1_4.py', RUNNER_SHA, 'scout_frozen_warm_runner')


def full_state(tick):
    o = observation(tick)
    o.update(done=False, result='', own_units=6, own_buildings=3,
             visible_enemy_units=0, visible_enemy_buildings=0)
    o['military'] = dict(units_killed=0, units_lost=0, buildings_killed=0,
        buildings_lost=0, army_value=600, assets_value=0, kills_cost=0, deaths_cost=0)
    o['economy'].update(power_provided=100, power_drained=0)
    return o


class StepStub(InertStub):
    def __init__(self, protocol):
        super().__init__(protocol)
        self.state_queries = []
    def JointAdvance(self, request, timeout):
        response = super().JointAdvance(request, timeout)
        self.start = response.end_tick
        return response
    def GetState(self, request, timeout):
        self.state_queries.append((request, timeout))
        return SimpleNamespace(phase='playing', winner='')


class Rig:
    def __init__(self, legacy, host, pb, warm, *, rounds=3, authority=lambda scope: True):
        self.logs = []
        self.model_calls = []
        self.fail_log = None
        self.warm = warm
        self.base = ModuleType('inert_base_instance')
        self.base.__dict__.update(vars(host))
        self.base.load_module = lambda path, name: legacy if path == host.ABADDON_CONTROLLER else SimpleNamespace()
        self.base.state_from_obs = lambda o: full_state(o.tick)
        self.pb = SimpleNamespace(**vars(pb))
        self.pb.StateRequest = lambda **kwargs: SimpleNamespace(**kwargs)
        self.stub = StepStub(self.pb)
        self.runner = SimpleNamespace(load_base=lambda: self.base, append_jsonl=self.log)
        self.original_slots = {k:getattr(self.base,k) for k in ('load_module','decision_to_commands','joint_advance')}
        self.original_runner_slots = {k:getattr(self.runner,k) for k in ('load_base','append_jsonl')}
        self.binding = ScoutMissionRunnerBinding(self.runner, doctrine='FEINTER', seed=SEED,
            round_limit=rounds, ticks_per_round=25, world_revision='frozen-fixture-world', authority_check=authority)
        self.binding.install()
        assert self.runner.load_base() is self.base
        proxy = self.base.load_module(self.base.ABADDON_CONTROLLER, 'fixture-controller')
        self.controller = proxy.AbaddonController(doctrine='FEINTER', seed=SEED)
        self.args = SimpleNamespace(doctrine='FEINTER', seed=SEED, rounds=rounds, ticks_per_round=25)

    def log(self, path, row):
        if row.get('event') == self.fail_log:
            raise OSError('inert log failure')
        self.logs.append((path, deepcopy(row)))

    def begin(self):
        self.runner.append_jsonl('warm-log', dict(event='warm_start_header', run_id=RUN_ID, seed=SEED))
        self.base.joint_advance(self.stub, self.pb, 'new-inert-session', 1, {'Multi0':[], 'Multi1':[]})
        self.runner.append_jsonl('trajectory', dict(event='run_header', run_id=RUN_ID, seed=SEED,
            abaddon_doctrine='FEINTER', ticks_per_round=25, round_limit=self.args.rounds,
            abaddon_controller_sha256=CONTROLLER_SHA256))

    def model(self, system, user, tools):
        self.model_calls.append((system, user, deepcopy(tools)))
        return 'advance', {}

    def execute_exact_loop(self, state=None):
        # Keep every statement in the frozen for-loop: no selective replacement,
        # removal of error branches, or reimplementation of its ordering.
        path = ROOT / 'fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py'
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == RUNNER_SHA
        parsed = ast.parse(raw)
        main = next(n for n in parsed.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        loops = [n for n in ast.walk(main) if isinstance(n, ast.For)
                 and isinstance(n.target, ast.Name) and n.target.id == 'round_no']
        assert len(loops) == 1
        function = ast.parse('def run_frozen_loop(states, pending):\n pass\n').body[0]
        function.body = [deepcopy(loops[0]), ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[]))]
        module = ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[]))
        env = dict(base=self.base, helper=SimpleNamespace(ollama_tool_call=self.model),
            controller=self.controller, stub=self.stub, pb2=self.pb, sid='new-inert-session',
            args=self.args, states={p:deepcopy(state or full_state(1)) for p in ('Multi0','Multi1')},
            pending={'Multi0':{},'Multi1':{}}, run_id=RUN_ID, traj='trajectory',
            CURRICULUM_ID=self.warm.CURRICULUM_ID, append_jsonl=self.runner.append_jsonl,
            reconcile_pending=self.warm.reconcile_pending, assert_no_stale_pending=self.warm.assert_no_stale_pending,
            apollyon_decision_typed=self.warm.apollyon_decision_typed,
            visible_count=self.warm.visible_count, combat_units=self.warm.combat_units)
        exec(compile(module, str(path), 'exec'), env)
        return env['run_frozen_loop'](env['states'], env['pending'])


def test_exact_frozen_loop_uses_real_gate_and_shared_step_without_source_edits(legacy,host,pb,warm):
    rig = Rig(legacy,host,pb,warm)
    rig.begin()
    result = rig.execute_exact_loop()
    assert result['completed_rounds'] == 3
    assert len(rig.stub.calls) == 4  # one unchanged warm-start call, then three joint rounds
    assert len(rig.model_calls) == 3
    decisions = [r for _,r in rig.logs if r.get('event') == 'joint_decision']
    results = [r for _,r in rig.logs if r.get('event') == 'joint_result']
    assert [r['abaddon']['decision']['action']['tool'] for r in decisions] == ['move_units','advance','advance']
    assert all(r[EVIDENCE_KEY]['dispatch_observed'] is False for r in decisions)
    assert all(r[EVIDENCE_KEY]['submission_feedback']['shared_clock_step_completed'] for r in results)
    assert all(r['apollyon']['tool']=='advance' for r in decisions)
    assert all(r['apollyon']['attempts'][0]['accepted'] is True for r in decisions)
    assert len(rig.stub.calls[1][0].player_actions[1].commands) == 1
    assert all(len(call[0].player_actions[1].commands)==0 for call in rig.stub.calls[2:])
    assert rig.binding.snapshot()['bridge']['controller']['active']['status']=='IN_PROGRESS'
    assert rig.binding.snapshot()['bridge']['controller']['history']==[]
    rig.binding.restore()
    assert not rig.binding.snapshot()['callbacks_installed']
    for name,fn in rig.original_slots.items(): assert getattr(rig.base,name) is fn
    for name,fn in rig.original_runner_slots.items(): assert getattr(rig.runner,name) is fn


@pytest.mark.parametrize('mode',['error','interrupt','session','shifted','short_step','observation_tick','missing_player','duplicate_player'])
def test_exact_loop_failed_reply_does_not_issue_or_retry(legacy,host,pb,warm,mode):
    rig=Rig(legacy,host,pb,warm); rig.begin(); rig.stub.mode=mode
    with pytest.raises((OSError, KeyboardInterrupt, RuntimeError)): rig.execute_exact_loop()
    assert len(rig.stub.calls)==2
    snap=rig.binding.snapshot()
    assert snap['held'] and snap['bridge']['controller']['active'] is None
    assert snap['bridge']['controller']['pending_host_result'] is True
    with pytest.raises(ScoutRunnerHold): rig.controller.decide(full_state(26))
    assert len(rig.stub.calls)==2
    rig.binding.restore()


@pytest.mark.parametrize('event,expected_calls,issued', [('joint_decision',1,False),('joint_result',2,True)])
def test_exact_loop_log_failure_does_not_forge_or_undo_dispatch(legacy,host,pb,warm,event,expected_calls,issued):
    rig=Rig(legacy,host,pb,warm);rig.begin();rig.fail_log=event
    with pytest.raises(OSError):rig.execute_exact_loop()
    assert len(rig.stub.calls)==expected_calls
    snap=rig.binding.snapshot()
    assert snap['held'] and (snap['bridge']['controller']['active'] is not None)==issued
    rig.binding.restore()


def test_exact_loop_uses_original_production_bookkeeping(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm,rounds=1);rig.begin()
    state=full_state(1); state['power_balance']=0;state['available_production']=['powr']
    result=rig.execute_exact_loop(state)
    assert 'powr' in result['pending']['Multi1']
    assert rig.stub.calls[-1][0].player_actions[1].commands[0].action==pb.BUILD
    assert rig.binding.snapshot()['bridge']['controller']['active'] is None
    rig.binding.restore()


def test_actual_loop_surfaces_end_state_query_failure_without_another_step(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm);rig.begin()
    def failed(*args,**kwargs): raise OSError('inert GetState failure')
    rig.stub.GetState=failed
    with pytest.raises(OSError):rig.execute_exact_loop()
    assert len(rig.stub.calls)==2
    # The outside runner error occurs after a successful joint call. The binding
    # awaits its result log; it must not let the next decision overtake that log.
    assert rig.binding.snapshot()['phase']=='WAIT_RESULT_LOG'
    with pytest.raises(ScoutRunnerHold): rig.controller.decide(full_state(26))
    assert rig.binding.snapshot()['held']
    rig.binding.restore()


@pytest.mark.parametrize('change',['tool','arguments','state','protocol'])
def test_split_runner_gate_echo_mismatch_stops_before_joint(legacy,host,pb,warm,change):
    rig=Rig(legacy,host,pb,warm);rig.begin();o=full_state(1);d=rig.controller.decide(o)
    name,args=d['action']['tool'],deepcopy(d['action']['arguments']); protocol=rig.pb
    if change=='tool':name='advance'
    elif change=='arguments':args['target_x']+=1
    elif change=='state':o['tick']+=1
    else:protocol=pb
    with pytest.raises(ScoutRunnerHold):rig.base.decision_to_commands(name,args,o,{},protocol)
    assert len(rig.stub.calls)==1 and rig.binding.snapshot()['held']
    rig.binding.restore()


def validated_round(rig):
    o=full_state(1);d=rig.controller.decide(o);a=d['action']
    ok,reason,commands=rig.base.decision_to_commands(a['tool'],a['arguments'],o,{},rig.pb)
    return o,d,ok,reason,commands


@pytest.mark.parametrize('change',['decision','accepted','count','reason','round','run','state'])
def test_log_echo_mismatch_cannot_reach_submission(legacy,host,pb,warm,change):
    rig=Rig(legacy,host,pb,warm);rig.begin();o,d,ok,reason,cmds=validated_round(rig)
    row=dict(event='joint_decision',run_id=RUN_ID,round=1,start_tick=1,abaddon_state=host.compact_state(o),
        abaddon={'decision':deepcopy(d),'accepted':ok,'host_reason':reason,'command_count':len(cmds)})
    if change=='decision':row['abaddon']['decision']['action']['arguments']['target_x']+=1
    elif change=='accepted':row['abaddon']['accepted']=1
    elif change=='count':row['abaddon']['command_count']+=1
    elif change=='reason':row['abaddon']['host_reason']='changed'
    elif change=='round':row['round']=2
    elif change=='run':row['run_id']='other'
    else:row['abaddon_state']['tick']+=1
    with pytest.raises(ScoutRunnerHold):rig.runner.append_jsonl('trajectory',row)
    assert len(rig.stub.calls)==1
    rig.binding.restore()


def test_no_joint_call_before_decision_log_and_no_early_result_log(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm);rig.begin();o,d,ok,reason,cmds=validated_round(rig)
    with pytest.raises(ScoutRunnerHold):
        rig.base.joint_advance(rig.stub,rig.pb,'new-inert-session',25,{'Multi0':[],'Multi1':cmds})
    assert len(rig.stub.calls)==1
    rig.binding.restore()


@pytest.mark.parametrize('phase',['warm_header','run_header','decide','gate','dispatch'])
def test_operation_permission_is_not_created_by_binding(legacy,host,pb,warm,phase):
    allowed=[True]
    rig=Rig(legacy,host,pb,warm,authority=lambda scope: allowed[0])
    if phase=='warm_header':
        allowed[0]=False
        with pytest.raises(ScoutRunnerHold):rig.begin()
    elif phase=='run_header':
        rig.runner.append_jsonl('warm-log',dict(event='warm_start_header',run_id=RUN_ID,seed=SEED))
        rig.base.joint_advance(rig.stub,rig.pb,'new-inert-session',1,{'Multi0':[],'Multi1':[]})
        allowed[0]=False
        with pytest.raises(ScoutRunnerHold):
            rig.runner.append_jsonl('trajectory',dict(event='run_header',run_id=RUN_ID,seed=SEED,
                abaddon_doctrine='FEINTER',ticks_per_round=25,round_limit=3,abaddon_controller_sha256=CONTROLLER_SHA256))
    else:
        rig.begin()
        if phase=='decide':
            allowed[0]=False
            with pytest.raises(ScoutRunnerHold):rig.controller.decide(full_state(1))
        elif phase=='gate':
            o=full_state(1);d=rig.controller.decide(o);allowed[0]=False;a=d['action']
            with pytest.raises(ScoutRunnerHold):rig.base.decision_to_commands(a['tool'],a['arguments'],o,{},rig.pb)
        else:
            original=rig.runner.append_jsonl
            def revoke_after_log(path,row):
                original(path,row)
                if row.get('event')=='joint_decision':allowed[0]=False
            rig.runner.append_jsonl=revoke_after_log
            with pytest.raises(ScoutRunnerHold):rig.execute_exact_loop()
            rig.runner.append_jsonl=original
    assert len(rig.stub.calls)<=1
    assert rig.binding.snapshot()['execution_permission_created'] is False
    rig.binding.restore()


def test_constructor_and_hook_installation_are_not_repeatable(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm)
    with pytest.raises(ScoutRunnerHold):rig.binding.install()
    rig.binding.restore()
    with pytest.raises(ScoutRunnerHold):rig.binding.install()


def test_restore_will_not_overwrite_another_callback(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm)
    installed=rig.base.joint_advance;foreign=lambda *a:None
    rig.base.joint_advance=foreign
    with pytest.raises(ScoutRunnerHold,match='do_not_overwrite'):rig.binding.restore()
    assert rig.base.joint_advance is foreign and rig.binding.snapshot()['held']
    rig.base.joint_advance=installed
    rig.binding.restore()


def test_split_bridge_proposal_and_gate_each_execute_once(legacy,host,pb):
    calls=[]
    def gate(*args):calls.append(args);return host.decision_to_commands(*args)
    b,c=bridge(legacy,host,pb,gate=gate)
    p=b.propose(observation(),evidence_id='first')
    assert calls==[] and b.snapshot()['phase']=='PROPOSED' and c.snapshot()['active'] is None
    ready=b.validate_proposal(p['proposal_id'],{})
    assert len(calls)==1 and ready['command_count']==1 and c.snapshot()['active'] is None
    with pytest.raises(RuntimeError):b.validate_proposal(p['proposal_id'],{})
    assert len(calls)==1


def test_binding_itself_has_no_source_or_launch_operations():
    path=ROOT/'openra_env/learning/abaddon_scout_runner_binding_v1.py'
    tree=ast.parse(path.read_bytes())
    calls={n.func.attr for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)}
    assert not calls.intersection({'Popen','run','execv','system','start_ollama','open','write_bytes','write_text','unlink'})
    assert 'if __name__' not in path.read_text()


def test_retained_controller_proxy_refuses_after_restoration(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm);rig.begin();rig.binding.restore()
    with pytest.raises(ScoutRunnerHold,match='not_installed'):rig.controller.decide(full_state(1))
    assert len(rig.stub.calls)==1


@pytest.mark.parametrize('change',['seed','doctrine','round_limit','ticks','run_id','controller_hash'])
def test_header_drift_refuses_before_first_scout_decision(legacy,host,pb,warm,change):
    rig=Rig(legacy,host,pb,warm)
    rig.runner.append_jsonl('warm-log',dict(event='warm_start_header',run_id=RUN_ID,seed=SEED))
    rig.base.joint_advance(rig.stub,rig.pb,'new-inert-session',1,{'Multi0':[],'Multi1':[]})
    row=dict(event='run_header',run_id=RUN_ID,seed=SEED,abaddon_doctrine='FEINTER',
             ticks_per_round=25,round_limit=3,abaddon_controller_sha256=CONTROLLER_SHA256)
    if change=='seed':row['seed']+=1
    elif change=='doctrine':row['abaddon_doctrine']='RUSHER'
    elif change=='round_limit':row['round_limit']+=1
    elif change=='ticks':row['ticks_per_round']=True
    elif change=='run_id':row['run_id']='another'
    else:row['abaddon_controller_sha256']='0'*64
    with pytest.raises(ScoutRunnerHold):rig.runner.append_jsonl('trajectory',row)
    assert rig.binding.snapshot()['held'] and rig.binding.snapshot()['bridge'] is None
    rig.binding.restore()


def test_failure_in_apollyon_protocol_does_not_make_an_abaddon_attempt(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm);rig.begin()
    calls=[]
    def invalid_model(*args):calls.append(1);return 'not_a_current_tool',{}
    rig.model=invalid_model
    with pytest.raises(RuntimeError,match='failed to produce a valid'):rig.execute_exact_loop()
    assert len(calls)==6  # Original runner's existing inference-output retry bound.
    assert len(rig.stub.calls)==1
    assert rig.binding.snapshot()['bridge']['controller']['pending_host_result'] is False
    assert rig.binding.snapshot()['bridge']['controller']['active'] is None
    rig.binding.restore()


def test_completed_round_bound_prevents_an_extra_controller_proposal(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm,rounds=1);rig.begin();rig.execute_exact_loop()
    assert len(rig.stub.calls)==2
    with pytest.raises(ScoutRunnerHold,match='not_ready'):rig.controller.decide(full_state(26))
    assert len(rig.stub.calls)==2
    rig.binding.restore()


def test_thirty_six_synthetic_rounds_keep_one_shared_step_and_preserve_scout_memory(legacy,host,pb,warm):
    rig=Rig(legacy,host,pb,warm,rounds=36);rig.begin();result=rig.execute_exact_loop()
    assert result['completed_rounds']==36 and len(rig.stub.calls)==37
    assert len(rig.model_calls)==36 and len(rig.stub.state_queries)==36
    for index,(request,_) in enumerate(rig.stub.calls[1:],1):
        assert request.ticks==25 and request.session_id=='new-inert-session'
    snap=rig.binding.snapshot()
    assert snap['bridge']['dispatch_call_count']==36
    assert not any(h['status']=='COMPLETED' for h in snap['bridge']['controller']['history'])
    # Synthetic states stay fixed; progress/arrival must not be invented.
    assert all(not r[EVIDENCE_KEY]['submission_feedback']['arrival_established_by_dispatch']
               for _,r in rig.logs if r.get('event')=='joint_result')
    rig.binding.restore()


def test_original_append_writes_real_temp_jsonl_with_stage_specific_evidence(legacy,host,pb,warm,tmp_path):
    rig=Rig(legacy,host,pb,warm,rounds=1)
    # The callback object installed on the runner is unchanged. The rig log sink
    # now delegates to the exact historical append routine on a temp file only.
    path=tmp_path/'rounds.jsonl'
    def sink(name,row):warm.append_jsonl(path,row)
    rig.binding._append=sink
    rig.begin();rig.execute_exact_loop()
    rows=[json.loads(s) for s in path.read_text().splitlines()]
    assert [r['event'] for r in rows]==['warm_start_header','run_header','joint_decision','joint_result']
    assert rows[2][EVIDENCE_KEY]['dispatch_observed'] is False
    assert rows[3][EVIDENCE_KEY]['submission_feedback']['shared_clock_step_completed'] is True
    assert all(r.get(EVIDENCE_KEY,{}).get('training_use_approved',False) is False for r in rows)
    rig.binding.restore()


def test_runner_full_main_and_host_process_helpers_never_called(legacy,host,pb,warm,monkeypatch):
    def forbidden(*args,**kwargs):raise AssertionError('unexpected operational helper')
    for module,names in ((warm,('main','load_base','parse_args','stage_to_contact','queue_structure')),
                         (host,('run','out','load_module','generate_proto','write_joint_attestation','verify_runtime_report'))):
        for name in names:
            if hasattr(module,name):monkeypatch.setattr(module,name,forbidden)
    rig=Rig(legacy,host,pb,warm,rounds=1);rig.begin();rig.execute_exact_loop();rig.binding.restore()


def test_returned_proposal_mutation_cannot_change_the_retained_gate_input(legacy,host,pb):
    b,c=bridge(legacy,host,pb)
    original=observation();p=b.propose(original,evidence_id='immutable-input')
    expected=deepcopy(p['decision'])
    p['decision']['action']['arguments']['target_x']=0
    original['units_summary'].clear()
    ready=b.validate_proposal(p['proposal_id'],{})
    assert ready['decision']==expected and ready['command_count']==1
    assert c.snapshot()['active'] is None
