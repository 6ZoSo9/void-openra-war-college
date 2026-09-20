"""Actual retained host functions with in-process protobuf/RPC fixtures only.

No network stub, model, engine, installer, service or game is run. Protocol
messages come from the complete pinned rl_bridge.proto compiled by protoc.
Generated gRPC client/server code and a real engine are not exercised.
"""
from copy import deepcopy
import hashlib
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import sys

from scout_protocol_fixture_v1 import compiled_protocol
import pytest

from openra_env.learning.abaddon_scout_host_bridge_v1 import ScoutHostHold, ScoutMissionHostBridge
from openra_env.learning.abaddon_scout_missions_v1 import ScoutMissionController
from openra_env.learning.goal_effect_core_v1 import Scope

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'fixtures/learning/scout-missions-v1'
SCOPE = Scope('offline-host-round', 'abaddon', 'frozen-openra-host-v1', 'game_ticks')
SESSION = 'inert-session'


def load_fixture(name, sha, modname):
    path = FIXTURES / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
    spec = importlib.util.spec_from_file_location(modname, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope='module')
def legacy():
    return load_fixture('abaddon_controller_v1.py',
        'b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103', 'host_test_controller')


@pytest.fixture(scope='module')
def host():
    # Main, loader, model and process helpers are never invoked.
    return load_fixture('joint_host_v1_2.py',
        'c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615', 'scout_historical_host')


@pytest.fixture(scope='module')
def pb():
    """All messages and enum values come from the complete compiler output."""
    return compiled_protocol()


def observation(tick=0):
    return {'tick':tick,'map':{'width':112,'height':54}, 'enemy_summary':[], 'enemy_buildings_summary':[],
        'available_production':[], 'production_items':[], 'production':[],
        'economy':{'cash':0,'ore':0,'harvester_count':1}, 'power_balance':100, 'explored_percent':10,
        'buildings_summary':[{'id':1,'type':'fact','cell_x':5,'cell_y':5},
                            {'id':2,'type':'proc','cell_x':6,'cell_y':5},
                            {'id':3,'type':'barr','cell_x':5,'cell_y':6}],
        'units_summary':[{'id':i,'type':'e1','can_attack':True,'cell_x':20,'cell_y':20,
                          'idle':True,'is_idle':True,'activity':'','current_activity':'','hp_percent':1.0}
                         for i in (20,30,40,50,60,70)]}


class InertStub:
    def __init__(self, pb, start=0, mode='success', during=None):
        self.pb, self.start, self.mode, self.during = pb, start, mode, during
        self.calls = []
    def JointAdvance(self, request, timeout):
        self.calls.append((deepcopy(request), timeout))
        if self.during: self.during()
        if self.mode == 'error': raise OSError('inert transport failure')
        if self.mode == 'interrupt': raise KeyboardInterrupt('inert interruption')
        response = self.pb.JointAdvanceResponse(session_id=request.session_id,
            start_tick=self.start, end_tick=self.start + request.ticks)
        for player in ('Multi0','Multi1'):
            response.player_observations.add(player=player).observation.tick = response.end_tick
        if self.mode == 'session': response.session_id = 'other-session'
        elif self.mode == 'shifted':
            response.start_tick += 25; response.end_tick += 25
            for row in response.player_observations: row.observation.tick = response.end_tick
        elif self.mode == 'short_step': response.end_tick -= 1
        elif self.mode == 'observation_tick': response.player_observations[0].observation.tick += 1
        elif self.mode == 'missing_player': del response.player_observations[1]
        elif self.mode == 'duplicate_player':
            response.player_observations.add(player='Multi0').observation.tick = response.end_tick
        return response


def bridge(legacy, host, pb, *, gate=None, joint=None, authority=lambda scope: True):
    c = ScoutMissionController(legacy, scope=SCOPE, doctrine='FEINTER', seed=1990061685)
    b = ScoutMissionHostBridge(c, scope=SCOPE, pb2=pb, decision_to_commands=gate or host.decision_to_commands,
        joint_advance=joint or host.joint_advance, authority_check=authority, session_id=SESSION, ticks_per_round=25)
    return b, c


def prepare(b, o=None):
    o = observation() if o is None else o
    return b.prepare(o, {}, evidence_id=f'row:{o["tick"]}')


def submit(b, p, stub, extra=None):
    return b.dispatch_joint(stub, proposal_id=p['proposal_id'],
        commands_by_player={'Multi0':[], 'Multi1': ([] if extra is None else extra)+p['commands']})


def test_real_host_gate_then_real_joint_function_acknowledges_after_rpc_only(legacy,host,pb):
    b,c = bridge(legacy,host,pb)
    o=observation(); original=deepcopy(o)
    p=prepare(b,o)
    assert o == original and p['accepted'] is True and p['command_count']==1
    assert c.snapshot()['active'] is None and c.snapshot()['pending_host_result'] is True
    def check_before_return():
        assert c.snapshot()['active'] is None and c.snapshot()['history']==[]
    stub=InertStub(pb,during=check_before_return)
    response,_=submit(b,p,stub)
    assert response.end_tick==25 and len(stub.calls)==1
    req,timeout=stub.calls[0]
    assert req.session_id==SESSION and req.ticks==25 and timeout==120.0
    assert [x.player for x in req.player_actions]==['Multi0','Multi1']
    assert req.player_actions[1].commands[0].SerializeToString()==p['commands'][0].SerializeToString()
    assert c.snapshot()['active']['status']=='ISSUED' and c.snapshot()['history']==[]
    feedback=b.snapshot()['last_feedback']
    assert feedback['shared_clock_step_completed'] is True
    assert feedback['per_command_engine_acceptance_established'] is False
    assert feedback['arrival_established_by_dispatch'] is False


def test_second_prepare_cannot_precede_joint_acknowledgement(legacy,host,pb):
    b,c=bridge(legacy,host,pb); prepare(b)
    with pytest.raises(ScoutHostHold,match='PREPARED'): prepare(b,observation(25))
    assert b.snapshot()['phase']=='HELD' and c.snapshot()['active'] is None


@pytest.mark.parametrize('mode',['error','interrupt','session','shifted','short_step','observation_tick','missing_player','duplicate_player'])
def test_failed_uncertain_or_mismatched_joint_never_issues_mission_or_retries(legacy,host,pb,mode):
    b,c=bridge(legacy,host,pb); p=prepare(b); stub=InertStub(pb,mode=mode)
    with pytest.raises((OSError,KeyboardInterrupt,RuntimeError)): submit(b,p,stub)
    assert c.snapshot()['active'] is None and c.snapshot()['pending_host_result'] is True
    assert b.snapshot()['phase']=='HELD' and b.snapshot()['runtime_effects_possible'] is True
    with pytest.raises(ScoutHostHold): submit(b,p,stub)
    assert len(stub.calls)==1


@pytest.mark.parametrize('mutation',['destination','actor','queued','extra_move','missing_move','missing_player','wrong_proposal','foreign_type'])
def test_command_or_binding_changes_stop_before_any_joint_call(legacy,host,pb,mutation):
    b,c=bridge(legacy,host,pb); p=prepare(b); stub=InertStub(pb)
    commands={'Multi0':[], 'Multi1':deepcopy(p['commands'])}; pid=p['proposal_id']
    if mutation=='destination': commands['Multi1'][0].target_x+=1
    elif mutation=='actor': commands['Multi1'][0].actor_id+=1
    elif mutation=='queued': commands['Multi1'][0].queued=True
    elif mutation=='extra_move': commands['Multi1'].insert(0,pb.Command(action=pb.MOVE,actor_id=30))
    elif mutation=='missing_move': commands['Multi1']=[]
    elif mutation=='missing_player': del commands['Multi0']
    elif mutation=='wrong_proposal': pid='wrong'
    elif mutation=='foreign_type': commands['Multi1']=[object()]
    with pytest.raises(ScoutHostHold): b.dispatch_joint(stub,proposal_id=pid,commands_by_player=commands)
    assert len(stub.calls)==0 and c.snapshot()['active'] is None
    assert b.snapshot()['runtime_effects_possible'] is False


def test_noop_does_not_count_mechanical_commands_as_scout_orders(legacy,host,pb):
    b,c=bridge(legacy,host,pb); o=observation()
    for u in o['units_summary']: u.update(idle=False,is_idle=False,activity='Move',current_activity='Move')
    p=prepare(b,o); assert p['decision']['action']['tool']=='advance' and p['commands']==[]
    mech=pb.Command(action=pb.PLACE_BUILDING,item_type='powr',target_x=6,target_y=7)
    stub=InertStub(pb); submit(b,p,stub,[mech])
    assert len(stub.calls)==1 and stub.calls[0][0].ticks==25
    assert len(stub.calls[0][0].player_actions[1].commands)==1
    assert c.snapshot()['active'] is None
    assert b.snapshot()['last_feedback']['submitted_controller_command_count']==0


def test_apollyon_and_mechanical_commands_preserved_byte_for_byte(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b)
    ap=[pb.Command(action=pb.ATTACK_MOVE,actor_id=101,target_x=55,target_y=28)]
    mech=[pb.Command(action=pb.CANCEL_PRODUCTION,item_type='weap')]
    batches={'Multi0':ap,'Multi1':mech+p['commands']}; before=deepcopy(batches)
    stub=InertStub(pb); b.dispatch_joint(stub,proposal_id=p['proposal_id'],commands_by_player=batches)
    for x in stub.calls[0][0].player_actions:
        assert list(x.commands)==before[x.player]
    assert batches==before and c.snapshot()['active']['unit_id']==20


def test_actual_gate_rejection_records_no_mission_after_shared_step(legacy,host,pb):
    def remove_owned_actor(name,args,state,pending,protocol):
        state['units_summary']=[]
        return host.decision_to_commands(name,args,state,pending,protocol)
    b,c=bridge(legacy,host,pb,gate=remove_owned_actor)
    p=prepare(b); assert p['accepted'] is False and p['host_reason']=='no_owned_units_resolved'
    assert c.snapshot()['last_event']['status']=='UNASSIGNED'
    stub=InertStub(pb); submit(b,p,stub)
    assert c.snapshot()['active'] is None and c.snapshot()['last_event']['status']=='REJECTED'
    assert b.snapshot()['last_feedback']['submitted_controller_command_count']==0


def test_actual_gate_production_pending_mutation_preserved(legacy,host,pb):
    b,c=bridge(legacy,host,pb); o=observation(); o.update(power_balance=0,available_production=['powr'])
    pending={}; p=b.prepare(o,pending,evidence_id='power')
    assert p['decision']['action']['tool']=='build_and_place' and 'powr' in pending
    assert p['commands'][0].action==pb.BUILD
    submit(b,p,InertStub(pb)); assert c.snapshot()['active'] is None


def test_contact_interrupts_active_scout_only_after_successful_dispatch(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b); submit(b,p,InertStub(pb))
    o=observation(25); o['enemy_summary']=[{'id':999,'type':'e1','cell_x':22,'cell_y':21}]
    p=prepare(b,o); assert p['decision']['action']['tool']=='attack_target'
    assert c.snapshot()['active'] is not None
    def remains_active():
        assert c.snapshot()['active'] is not None
    submit(b,p,InertStub(pb,start=25,during=remains_active))
    assert c.snapshot()['active'] is None and c.snapshot()['history'][-1]['status']=='INTERRUPTED'


def test_progress_keeps_one_move_and_arrival_requires_later_observation(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b); submit(b,p,InertStub(pb))
    target=c.snapshot()['active']['target']
    o=observation(25); o['units_summary'][0].update(cell_x=21,idle=False,is_idle=False,activity='Move',current_activity='Move')
    p=prepare(b,o); assert p['commands']==[] and c.snapshot()['history']==[]
    submit(b,p,InertStub(pb,start=25))
    o=observation(50); o['units_summary'][0].update(cell_x=target[0],cell_y=target[1])
    prepare(b,o); assert any(h['status']=='COMPLETED' for h in c.snapshot()['history'])
    assert b.snapshot()['dispatch_call_count']==2


@pytest.mark.parametrize('phase',['prepare','dispatch','last_check'])
def test_existing_authority_must_be_current_and_exactly_true(legacy,host,pb,phase):
    enabled={'value':False if phase=='prepare' else True}; calls=[]
    def authority(scope):
        assert scope==SCOPE; calls.append(scope)
        return False if phase=='last_check' and len(calls)==3 else enabled['value']
    b,c=bridge(legacy,host,pb,authority=authority); stub=InertStub(pb)
    if phase=='prepare':
        with pytest.raises(ScoutHostHold): prepare(b)
    else:
        p=prepare(b)
        if phase=='dispatch': enabled['value']=False
        with pytest.raises(ScoutHostHold): submit(b,p,stub)
    assert len(stub.calls)==0 and c.snapshot()['active'] is None


@pytest.mark.parametrize('value',[1,'yes',None])
def test_truthy_nonbool_authority_cannot_enter_prepare(legacy,host,pb,value):
    b,c=bridge(legacy,host,pb,authority=lambda scope:value)
    with pytest.raises(ScoutHostHold): prepare(b)
    assert c.snapshot()['pending_host_result'] is False


@pytest.mark.parametrize('kind',['shape','accepted','rejected_commands','changed_target','accepted_empty','advance_commands'])
def test_malformed_gate_outputs_cannot_manufacture_dispatch_ack(legacy,host,pb,kind):
    def gate(name,args,state,pending,protocol):
        ok,reason,cmds=host.decision_to_commands(name,args,state,pending,protocol)
        if kind=='shape': return {'accepted':True}
        if kind=='accepted': return 1,reason,cmds
        if kind=='rejected_commands': return False,reason,cmds
        if kind=='changed_target': cmds[0].target_x+=1
        if kind=='accepted_empty': cmds=[]
        if kind=='advance_commands': cmds=[pb.Command(action=pb.MOVE,actor_id=20)]
        return ok,reason,cmds
    b,c=bridge(legacy,host,pb,gate=gate); o=observation()
    if kind=='advance_commands':
        for u in o['units_summary']: u.update(idle=False,is_idle=False,activity='Move',current_activity='Move')
    with pytest.raises(ScoutHostHold): prepare(b,o)
    assert c.snapshot()['active'] is None and b.snapshot()['dispatch_call_count']==0


def test_gate_failure_preserves_pending_production_and_stops_bridge(legacy,host,pb):
    def gate(*args):
        args[3]['fixture_pending']={'attempt':0}; raise ValueError('inert gate failure')
    b,c=bridge(legacy,host,pb,gate=gate); pending={}
    with pytest.raises(ValueError): b.prepare(observation(),pending,evidence_id='bad-gate')
    assert pending=={'fixture_pending':{'attempt':0}} and b.snapshot()['phase']=='HELD'
    assert c.snapshot()['pending_host_result'] is True and c.snapshot()['active'] is None


def test_duplicate_submission_never_calls_original_joint_twice(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b); stub=InertStub(pb); submit(b,p,stub)
    with pytest.raises(ScoutHostHold): submit(b,p,stub)
    assert len(stub.calls)==1


def test_next_prepare_must_start_at_previous_joint_end(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b); submit(b,p,InertStub(pb))
    with pytest.raises(ScoutHostHold,match='previous_joint_end'): prepare(b,observation(50))
    assert b.snapshot()['dispatch_call_count']==1


def test_result_and_command_copies_do_not_change_internal_ack(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b); saved=deepcopy(p)
    p['accepted']=False; p['decision']['action']['tool']='advance'; p['commands'][0].target_x=-1
    submit(b,saved,InertStub(pb)); view=b.snapshot(); view['last_feedback']['mission']['active']['unit_id']=999
    assert b.snapshot()['last_feedback']['mission']['active']['unit_id']==20


def test_acknowledgement_error_after_rpc_never_retries(legacy,host,pb,monkeypatch):
    b,c=bridge(legacy,host,pb); p=prepare(b); stub=InertStub(pb)
    def fail(*a,**k): raise RuntimeError('inert acknowledgement failure')
    monkeypatch.setattr(c,'acknowledge',fail)
    with pytest.raises(RuntimeError): submit(b,p,stub)
    assert b.snapshot()['phase']=='HELD' and b.snapshot()['runtime_effects_possible'] is True
    with pytest.raises(ScoutHostHold): submit(b,p,stub)
    assert len(stub.calls)==1


@pytest.mark.parametrize('round_no,tool',[(10,'advance'),(17,'move_units'),(33,'move_units')])
def test_exact_saved_scout_observations_through_actual_gate_without_filling_gaps(legacy,host,pb,round_no,tool):
    import json
    fixture = json.loads((FIXTURES/'pair03_saved_observations.json').read_bytes())
    saved = next(row for row in fixture['streams']['candidate']['rows'] if row['round']==round_no)
    o=deepcopy(saved['observation']); untouched=deepcopy(o)
    assert 'production' not in o  # Export was compact; no fabricated raw production state.
    b,c=bridge(legacy,host,pb)
    p=prepare(b,o)
    assert p['decision']['action']['tool']==tool
    assert p['accepted'] is True and p['command_count']==(0 if tool=='advance' else 1)
    assert o==untouched and c.snapshot()['active'] is None
    stub=InertStub(pb,start=o['tick']); submit(b,p,stub)
    assert len(stub.calls)==1 and c.snapshot()['history']==[]
    assert (c.snapshot()['active'] is not None)==(tool=='move_units')


def test_exact_saved_baseline_contact_uses_unchanged_gate_and_owned_command_selection(legacy,host,pb):
    import json
    fixture=json.loads((FIXTURES/'pair03_saved_observations.json').read_bytes())
    saved=fixture['streams']['baseline']['rows'][0]
    assert saved['round']==33
    o=deepcopy(saved['observation']); assert 'production' not in o
    b,c=bridge(legacy,host,pb); p=prepare(b,o)
    assert p['decision']['action']['tool']=='attack_target' and p['accepted'] is True
    expected={u['id'] for u in o['units_summary'] if u['can_attack']}
    assert {cmd.actor_id for cmd in p['commands']}==expected
    assert all(cmd.target_actor_id==139 for cmd in p['commands'])
    submit(b,p,InertStub(pb,start=o['tick']))
    assert c.snapshot()['active'] is None


def test_missing_required_raw_production_state_is_not_invented(legacy,host,pb):
    b,c=bridge(legacy,host,pb); o=observation()
    o.update(power_balance=0,available_production=['powr']); del o['production']
    with pytest.raises(KeyError,match='production'): prepare(b,o)
    assert 'production' not in o and b.snapshot()['phase']=='HELD'
    assert b.snapshot()['dispatch_call_count']==0 and c.snapshot()['active'] is None


def test_no_loader_service_process_or_network_helper_is_called(legacy,host,pb,monkeypatch):
    def forbidden(*args,**kwargs): raise AssertionError('host operation outside gate/joint fixture')
    for name in ('run','out','load_module','generate_proto','write_joint_attestation'):
        monkeypatch.setattr(host,name,forbidden)
    b,c=bridge(legacy,host,pb); p=prepare(b); stub=InertStub(pb); submit(b,p,stub)
    assert len(stub.calls)==1


@pytest.mark.parametrize('kind',['too_many','too_large'])
def test_command_resource_bounds_hold_before_transport(legacy,host,pb,kind,monkeypatch):
    from openra_env.learning import abaddon_scout_host_bridge_v1 as module
    b,c=bridge(legacy,host,pb); p=prepare(b); stub=InertStub(pb)
    if kind=='too_many':
        monkeypatch.setattr(module,'MAX_COMMANDS',0)
    else:
        monkeypatch.setattr(module,'MAX_COMMAND_BYTES',1)
    with pytest.raises(ScoutHostHold): submit(b,p,stub)
    assert not stub.calls and c.snapshot()['active'] is None


def test_failed_contact_submission_does_not_interrupt_existing_scout(legacy,host,pb):
    b,c=bridge(legacy,host,pb); first=prepare(b); submit(b,first,InertStub(pb))
    before_id=c.snapshot()['active']['id']
    o=observation(25); o['enemy_summary']=[{'id':999,'type':'e1','cell_x':22,'cell_y':21}]
    p=prepare(b,o); assert p['decision']['action']['tool']=='attack_target'
    with pytest.raises(OSError): submit(b,p,InertStub(pb,start=25,mode='error'))
    assert c.snapshot()['active']['id']==before_id
    assert not any(h['status']=='INTERRUPTED' for h in c.snapshot()['history'])
    assert b.snapshot()['phase']=='HELD'


def test_bridge_does_not_forward_unobservable_false_runtime_integration_claim(legacy,host,pb):
    b,c=bridge(legacy,host,pb); p=prepare(b)
    assert 'runtime_integration_active' not in p['mission']
    submit(b,p,InertStub(pb))
    result=b.snapshot()
    assert result['runtime_effects_possible'] is True
    for row in (result['controller'],result['last_feedback']['mission']):
        assert 'runtime_integration_active' not in row
        assert row['runtime_integration_status_observed_by_controller'] is False
