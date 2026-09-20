"""Run the entire unchanged historical main with inert boundary backends.

The real warm-start recipes, command gates, observation conversion, round loop,
JSONL/summary writes and outer finally execute. Service/Git/Docker/model/transport
are synthetic, and every output directory is temporary. This is not a game.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from types import ModuleType, SimpleNamespace

import pytest

from test_abaddon_scout_host_bridge_v1 import load_fixture, pb
from openra_env.learning.abaddon_scout_runner_binding_v1 import (
    EVIDENCE_KEY, ScoutMissionRunnerBinding, ScoutRunnerHold,
)

ROOT = Path(__file__).resolve().parents[1]
RUNNER_SHA = 'ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901'
HOST_SHA = 'c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615'
CONTROLLER_SHA = 'b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103'


@pytest.fixture(scope='module')
def full_pb(pb):
    """Use the same complete compiler-derived protocol as the bridge tests."""
    return pb


class InertMainWorld:
    """Explicitly synthetic instant construction/placement, stationary scouting.

    This test state machine is not OpenRA physics or a replay of recorded states.
    It produces typed messages for the original state_from_obs function.
    """
    def __init__(self, rig):
        self.rig, self.pb, self.tick = rig, rig.pb, 0
        self.requests = []
        self.controller_steps = 0
        self.states = {}
        for offset, player in enumerate(('Multi0','Multi1')):
            o = self.pb.GameObservation(tick=0, explored_percent=10)
            o.map_info.width, o.map_info.height, o.map_info.map_name = 112, 54, 'synthetic-only'
            o.economy.cash, o.economy.power_provided = 10000, 100
            o.available_production.extend(['powr','proc','barr','e1'])
            o.units.add(actor_id=10+offset*1000, type='mcv', cell_x=10+offset*80,
                        cell_y=10+offset*25, hp_percent=1, is_idle=True, owner=player)
            self.states[player] = o
        self.next_id = 2000

    def CreateSession(self, request, timeout):
        self.rig.events.append('session_create')
        if self.rig.fault == 'session_create':
            raise OSError('fixture session-create failure')
        self.rig.session_up = True
        return self.pb.CreateSessionResponse(session_id='synthetic-main-session')

    def DestroySession(self, request, timeout):
        self.rig.events.append('session_destroy')
        if self.rig.fault == 'session_destroy':
            raise OSError('fixture destroy failure')
        self.rig.session_up = False
        return SimpleNamespace()

    def _apply(self, player, cmd):
        o, p = self.states[player], self.pb
        self.next_id += 1
        if cmd.action == p.DEPLOY:
            unit = next(u for u in o.units if u.actor_id == cmd.actor_id)
            o.buildings.add(actor_id=self.next_id,type='fact',cell_x=unit.cell_x,cell_y=unit.cell_y,hp_percent=1,is_powered=True)
            o.units.remove(unit)
        elif cmd.action == p.BUILD:
            o.production.add(queue_type='Building',item=cmd.item_type,progress=1)
        elif cmd.action == p.PLACE_BUILDING:
            o.buildings.add(actor_id=self.next_id,type=cmd.item_type,cell_x=cmd.target_x,cell_y=cmd.target_y,hp_percent=1,is_powered=True)
            for row in list(o.production):
                if row.item == cmd.item_type:
                    o.production.remove(row)
            if cmd.item_type == 'proc':
                o.economy.harvester_count = 1
                o.units.add(actor_id=self.next_id+10000,type='harv',cell_x=cmd.target_x,cell_y=cmd.target_y,
                            hp_percent=1,is_idle=True,owner=player)
        elif cmd.action == p.TRAIN:
            o.units.add(actor_id=self.next_id,type=cmd.item_type,cell_x=20,cell_y=20,
                        can_attack=True,hp_percent=1,is_idle=True,owner=player)
        elif cmd.action == p.MOVE:
            unit = next(u for u in o.units if u.actor_id == cmd.actor_id)
            if self.rig.start_returned:
                unit.is_idle, unit.current_activity = False, 'Move'
            else:
                unit.cell_x, unit.cell_y = cmd.target_x, cmd.target_y
        elif cmd.action == p.CANCEL_PRODUCTION:
            for row in list(o.production):
                if row.item == cmd.item_type:
                    o.production.remove(row)
        else:
            raise AssertionError('unexpected synthetic command: '+str(cmd.action))

    def JointAdvance(self, request, timeout):
        self.requests.append(deepcopy(request))
        is_controller = self.rig.binding.snapshot()['phase'] == 'WAIT_JOINT'
        label = 'controller_joint' if is_controller else 'warm_joint'
        self.rig.events.append(label)
        if self.rig.fault == label:
            raise OSError('fixture joint failure')
        if is_controller and self.rig.fault == 'joint_interrupt':
            raise KeyboardInterrupt('fixture interrupted joint')
        if is_controller:
            self.controller_steps += 1
        for batch in request.player_actions:
            for cmd in batch.commands:
                self._apply(batch.player, cmd)
        old = self.tick
        self.tick += request.ticks
        response = self.pb.JointAdvanceResponse(session_id=request.session_id,start_tick=old,end_tick=self.tick)
        for player in ('Multi0','Multi1'):
            o = self.states[player]
            o.tick = self.tick
            row = response.player_observations.add(player=player)
            row.observation.CopyFrom(o)
        if is_controller and self.rig.fault == 'wrong_session':
            response.session_id = 'wrong'
        return response

    def GetState(self, request, timeout):
        self.rig.events.append('state_query')
        if self.rig.fault == 'state_query':
            raise OSError('fixture state query failure')
        over = self.rig.fault == 'early_game_over'
        return self.pb.GameState(tick=self.tick,phase='game_over' if over else 'playing',winner='Multi1' if over else '')


class FullMainRig:
    def __init__(self, tmp_path, monkeypatch, protocol, *, fault=None, rounds=3):
        self.fault, self.events, self.rounds = fault, [], rounds
        self.container_up = self.session_up = self.service_up = self.start_returned = False
        self.pb = protocol
        self.runner = load_fixture('warm_start_runner_v1_4.py',RUNNER_SHA,'full_main_frozen_runner')
        self.base = load_fixture('joint_host_v1_2.py',HOST_SHA,'full_main_frozen_host')
        self.controller = load_fixture('abaddon_controller_v1.py',CONTROLLER_SHA,'full_main_frozen_controller')
        self.runner.RUNS_DIR = tmp_path / 'runs'
        self.runner.parse_args = lambda: SimpleNamespace(doctrine='FEINTER',seed=1990061685,
            rounds=rounds,ticks_per_round=25,starter_infantry=6,staging_max_ticks=50)
        self.runner.socket = SimpleNamespace(gethostname=lambda:self.base.HOST)
        self.runner.tempfile = SimpleNamespace(TemporaryDirectory=lambda **kw:tempfile.TemporaryDirectory(dir=tmp_path,**kw))
        self.base.PROTO_PY = Path(sys.executable)
        self.base.out, self.base.run = self.out, self.run
        self.base.exact_file = lambda *a:self.events.append('fixture_source_check')
        self.base.verify_runtime_report = lambda:self.events.append('fixture_report_check')
        self.base.free_port = lambda:45678  # No socket is opened for this value.
        self.base.wait_daemon = self.wait_daemon
        self.base.wait_players = self.wait_players
        self.helper = SimpleNamespace(MODEL=self.base.APOLLYON_MODEL,EXACT={},
            V14=tmp_path/'not-executed-model-helper',V14_SHA='fixture',SERVICE='ollama.service',
            start_ollama=self.start,cleanup=self.cleanup,ollama_tool_call=self.model)
        self.base.load_module = self.load_module
        self.runner.load_base = lambda:self.base
        original_append = self.runner.append_jsonl
        def log(path,row):
            self.events.append('log:'+row.get('event','unknown'))
            if self.fault == 'log:'+row.get('event','unknown'):
                raise OSError('fixture logging failure')
            original_append(path,row)
        self.runner.append_jsonl = log
        self.binding = ScoutMissionRunnerBinding(self.runner,doctrine='FEINTER',seed=1990061685,
            round_limit=rounds,ticks_per_round=25,world_revision='synthetic-full-main-world',authority_check=self.authority)
        self.world = InertMainWorld(self)
        self.channel = SimpleNamespace(close=self.close_channel)
        grpc = ModuleType('grpc')
        grpc.insecure_channel = self.open_channel
        monkeypatch.setitem(sys.modules,'grpc',grpc)
        self.base.generate_proto = self.generate_proto
        self.binding.install()
        def forbidden(*a,**kw):
            raise AssertionError('unmocked process/network boundary')
        monkeypatch.setattr(subprocess,'Popen',forbidden)
        monkeypatch.setattr(socket,'socket',forbidden)

    def authority(self, scope):
        return not (self.fault == 'revoked_after_warm' and 'log:warm_start_step' in self.events)

    def out(self, argv, **kw):
        if argv[0] == 'git':
            if argv[1:] == ['rev-parse','HEAD']:
                return self.runner.ENGINE_COMMIT if kw.get('cwd') == self.runner.OPENRA else self.runner.WAR_COLLEGE_COMMIT
            if argv[1] == 'status':
                return ' M fixture' if self.fault == 'dirty_source' else ''
        if argv[:3] == ['docker','image','inspect']:
            return 'wrong' if self.fault == 'image' else self.runner.IMAGE_ID
        if argv == ['docker','context','show']:
            return 'rootless'
        raise AssertionError('unexpected host query '+repr(argv))

    def run(self, argv, **kw):
        if argv[0] == 'systemctl':
            return SimpleNamespace(returncode=0,stdout='inactive\n' if argv[1]=='is-active' else 'disabled\n')
        if argv[:2] == ['docker','run']:
            self.events.append('container_start');self.container_up=True
            if self.fault == 'container_start':raise OSError('fixture partial container start')
            return SimpleNamespace(returncode=0,stdout='inert-id')
        if argv[:2] == ['docker','inspect']:
            self.events.append('container_inspect')
            if self.fault == 'container_inspect':raise OSError('fixture inspect failure')
            return SimpleNamespace(returncode=0 if self.container_up else 1,stdout='')
        if argv[:3] == ['docker','rm','-f']:
            self.events.append('container_remove')
            if self.fault == 'container_remove':return SimpleNamespace(returncode=1,stdout='')
            self.container_up=self.session_up=False
            return SimpleNamespace(returncode=0,stdout='')
        raise AssertionError('unexpected host action '+repr(argv))

    def load_module(self, path, name):
        if path == self.base.ABADDON_CONTROLLER:return self.controller
        if path == self.base.APOLLYON_RUNNER:return self.helper
        raise AssertionError('unexpected module load')

    def generate_proto(self, path):
        self.events.append('protocol_fixture')
        if self.fault == 'protocol':raise OSError('fixture protocol failure')
        return self.pb,SimpleNamespace(RLBridgeStub=lambda channel:self.world)

    def open_channel(self,*args,**kwargs):
        self.events.append('channel_open')
        if self.fault == 'channel_open':raise OSError('fixture channel failure')
        return self.channel

    def close_channel(self):
        self.events.append('channel_close')
        if self.fault == 'channel_close':raise OSError('fixture close failure')

    def wait_daemon(self,*args):
        self.events.append('daemon_ready')
        if self.fault == 'daemon_ready':raise OSError('fixture daemon failure')

    def wait_players(self,*args):
        self.events.append('players_ready')
        if self.fault == 'players_ready':raise OSError('fixture player failure')

    def start(self):
        self.events.append('helper_start');self.service_up=True
        if self.fault == 'partial_helper_start':raise OSError('fixture service up then start failed')
        if self.fault == 'startup_interrupt':raise KeyboardInterrupt('fixture interrupted partial startup')
        self.start_returned=True
        for o in self.world.states.values():
            del o.available_production[:]

    def cleanup(self):
        self.events.append('helper_cleanup')
        if self.fault == 'helper_cleanup':raise OSError('fixture helper cleanup failure')
        self.service_up=False

    def model(self,*args):
        self.events.append('model_fixture')
        if self.fault == 'model':raise OSError('fixture inference failure')
        return 'advance',{}

    def execute(self):
        # Calls the ENTIRE original main, not an AST slice; fallback and
        # restoration use the existing binding's explicit one-call interface.
        return self.binding.run_main_once()

    def rows(self,name='trajectory.jsonl'):
        paths=list(self.runner.RUNS_DIR.glob('*/'+name))
        return [json.loads(x) for p in paths for x in p.read_text().splitlines()]


@pytest.mark.parametrize('rounds',[1,3,36])
def test_full_main_warmstart_loop_summary_and_finally(tmp_path,monkeypatch,full_pb,rounds):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,rounds=rounds)
    rig.execute()
    rows=rig.rows();decisions=[r for r in rows if r['event']=='joint_decision']
    assert len(decisions)==rig.world.controller_steps==rounds
    assert rig.events.index('warm_joint') < rig.events.index('helper_start') < rig.events.index('controller_joint')
    assert all(not r[EVIDENCE_KEY]['dispatch_observed'] for r in decisions)
    assert all(r[EVIDENCE_KEY]['submission_feedback']['shared_clock_step_completed']
               for r in rows if r['event']=='joint_result')
    assert not rig.container_up and not rig.session_up and not rig.service_up
    assert rig.events.count('session_destroy')==rig.events.count('helper_cleanup')==1
    assert rig.events.index('session_destroy')<rig.events.index('channel_close')<rig.events.index('container_remove')<rig.events.index('helper_cleanup')
    summary=json.loads(next(rig.runner.RUNS_DIR.glob('*/summary.json')).read_text())
    assert summary['rounds_completed']==rounds and summary['outcome']=='DRAW_OR_UNFINISHED'
    assert summary['trajectory_sha256']==hashlib.sha256(next(rig.runner.RUNS_DIR.glob('*/trajectory.jsonl')).read_bytes()).hexdigest()
    assert rig.binding.snapshot()['callbacks_installed'] is False
    assert len(rig.rows('warm-start.jsonl'))>5


@pytest.mark.parametrize('fault', ['image','dirty_source','protocol','container_start','channel_open',
    'daemon_ready','session_create','players_ready','warm_joint','log:warm_start_header',
    'log:warm_start_step','log:run_header','model','log:joint_decision','controller_joint',
    'joint_interrupt','wrong_session','state_query','log:joint_result'])
def test_full_main_failure_paths_restore_binding_and_bound_steps(tmp_path,monkeypatch,full_pb,fault):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault=fault)
    with pytest.raises((OSError,RuntimeError,KeyboardInterrupt)):
        rig.execute()
    assert rig.binding.snapshot()['callbacks_installed'] is False
    assert not rig.container_up and not rig.session_up and not rig.service_up
    assert rig.world.controller_steps<=1
    assert rig.events.count('helper_start')<=1
    if 'container_start' in rig.events:assert 'container_remove' in rig.events
    if rig.start_returned:assert rig.events.count('helper_cleanup')==1
    if fault=='log:joint_decision':assert rig.world.controller_steps==0
    if fault in ('state_query','log:joint_result'):assert rig.world.controller_steps==1


@pytest.mark.parametrize('fault',['partial_helper_start','startup_interrupt'])
def test_partial_start_failure_must_call_existing_helper_cleanup(tmp_path,monkeypatch,full_pb,fault):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault=fault)
    with pytest.raises((OSError,KeyboardInterrupt)):
        rig.execute()
    assert rig.events.count('helper_start')==1
    assert rig.events.count('helper_cleanup')==1
    assert not rig.service_up and not rig.container_up
    assert rig.world.controller_steps==0


def test_early_terminal_still_cleans_up(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='early_game_over',rounds=36)
    rig.execute()
    assert rig.world.controller_steps==1 and not rig.service_up and not rig.container_up
    summary=json.loads(next(rig.runner.RUNS_DIR.glob('*/summary.json')).read_text())
    assert summary['rounds_completed']==1 and summary['status']=='game_over'
    # This is a programmed fixture terminal, not a real candidate victory.
    assert summary['outcome']=='ABADDON_WIN'


def test_outer_cleanup_inspect_failure_still_reaches_helper_teardown(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='container_inspect')
    with pytest.raises(OSError,match='inspect failure'):
        rig.execute()
    assert rig.world.controller_steps==3 and rig.events.count('helper_cleanup')==1
    assert not rig.service_up and rig.container_up
    snap=rig.binding.snapshot()
    assert snap['main_lifecycle']['final_cleanup_fallback_attempted'] is True
    assert snap['main_lifecycle']['actual_runtime_state_verified'] is False
    assert snap['callbacks_installed'] is False
    # The runner wrote this BEFORE teardown. Existence is not cleanup success.
    assert len(list(rig.runner.RUNS_DIR.glob('*/summary.json')))==1


def test_nonzero_container_removal_is_not_upgraded_to_teardown_evidence(tmp_path,monkeypatch,full_pb,capsys):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='container_remove')
    rig.execute()
    assert rig.container_up and not rig.service_up
    assert 'engine_container_removed=true' in capsys.readouterr().out
    # Characterize the inherited unchecked print, do not certify it as true.
    assert rig.binding.snapshot()['main_lifecycle']['callback_returned'] is True
    assert rig.binding.snapshot()['main_lifecycle']['actual_runtime_state_verified'] is False


def test_helper_cleanup_exception_is_not_retried(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='helper_cleanup')
    with pytest.raises(OSError,match='helper cleanup failure'):
        rig.execute()
    assert rig.events.count('helper_cleanup')==1 and rig.service_up
    snap=rig.binding.snapshot()
    assert snap['helper_lifecycle']['cleanup_callback_returned'] is False
    assert snap['helper_lifecycle']['cleanup_error_type']=='OSError'
    assert snap['main_lifecycle']['final_cleanup_fallback_attempted'] is False


@pytest.mark.parametrize('secondary',[OSError,KeyboardInterrupt])
def test_startup_error_is_not_masked_by_failed_cleanup(tmp_path,monkeypatch,full_pb,secondary):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='partial_helper_start')
    def broken_cleanup():
        rig.events.append('helper_cleanup')
        raise secondary('fixture secondary cleanup error')
    rig.helper.cleanup=broken_cleanup
    with pytest.raises(OSError,match='service up then start failed'):
        rig.execute()
    snap=rig.binding.snapshot()
    assert rig.events.count('helper_cleanup')==1
    assert snap['helper_lifecycle']['failed_start_cleanup_error_type']==secondary.__name__
    assert snap['main_lifecycle']['error_type']=='OSError'
    assert not snap['callbacks_installed'] and rig.service_up


def test_container_inspect_error_preserved_when_fallback_cleanup_also_fails(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='container_inspect')
    def broken_cleanup():
        rig.events.append('helper_cleanup')
        raise ValueError('fixture secondary teardown error')
    rig.helper.cleanup=broken_cleanup
    with pytest.raises(OSError,match='inspect failure'):
        rig.execute()
    assert rig.binding.snapshot()['main_lifecycle']['final_cleanup_error_type']=='ValueError'
    assert rig.events.count('helper_cleanup')==1 and rig.service_up


def test_cleanup_already_observed_inside_start_is_not_repeated(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    def internally_cleaned_start():
        rig.events.append('helper_start');rig.service_up=True
        rig.helper.cleanup()
        raise OSError('fixture readiness refused after observed cleanup')
    rig.helper.start_ollama=internally_cleaned_start
    with pytest.raises(OSError,match='readiness refused'):
        rig.execute()
    assert rig.events.count('helper_cleanup')==1 and not rig.service_up
    assert rig.binding.snapshot()['helper_lifecycle']['failed_start_cleanup_attempted'] is False


def test_unobserved_internal_cleanup_may_be_followed_by_one_idempotent_fallback(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    captured_cleanup=rig.helper.cleanup
    def internally_cleaned_start():
        rig.events.append('helper_start');rig.service_up=True
        captured_cleanup()  # This closure is invisible to the binding's counter.
        raise OSError('fixture hidden internal cleanup')
    rig.helper.start_ollama=internally_cleaned_start
    with pytest.raises(OSError,match='hidden internal'):
        rig.execute()
    assert rig.events.count('helper_cleanup')==2 and not rig.service_up
    assert rig.binding.snapshot()['helper_lifecycle']['cleanup_callback_attempts']==1
    assert rig.binding.snapshot()['helper_lifecycle']['failed_start_cleanup_attempted'] is True


def test_authority_rechecked_immediately_before_helper_start(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    rig.binding._authority=lambda scope:'helper_start' not in rig.events and not any(
        row['event']=='warm_start_step' and row['label']=='stage_squads_to_center'
        for row in rig.rows('warm-start.jsonl'))
    with pytest.raises(ScoutRunnerHold,match='operation_authority'):
        rig.execute()
    assert 'helper_start' not in rig.events and not rig.service_up and not rig.container_up
    assert rig.world.controller_steps==0


def test_held_binding_still_allows_original_cleanup_after_round_failure(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb,fault='log:joint_decision')
    rig.execute_error=None
    with pytest.raises(OSError,match='logging failure'):
        rig.execute()
    assert rig.binding.snapshot()['held'] and rig.events.count('helper_cleanup')==1
    assert not rig.service_up and rig.world.controller_steps==0


def test_run_main_once_refuses_reentry_after_completion_or_failure(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    rig.execute();calls=len(rig.world.requests)
    with pytest.raises(ScoutRunnerHold):rig.binding.run_main_once()
    with pytest.raises(ScoutRunnerHold):rig.binding.install()
    assert len(rig.world.requests)==calls


def test_helper_callbacks_restored_and_saved_proxy_cannot_restart(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    start,cleanup=rig.helper.start_ollama,rig.helper.cleanup
    held_start=[]
    original_model=rig.helper.ollama_tool_call
    def capture(*args):
        held_start.append(rig.helper.start_ollama)
        return original_model(*args)
    rig.helper.ollama_tool_call=capture
    rig.execute()
    assert rig.helper.start_ollama is start and rig.helper.cleanup is cleanup
    with pytest.raises(ScoutRunnerHold):held_start[0]()
    assert rig.events.count('helper_start')==1


def test_restoration_error_does_not_replace_primary_main_error(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    outsider=lambda path,row:None
    def failed_model(*args):
        rig.runner.append_jsonl=outsider
        raise OSError('fixture primary model error')
    rig.helper.ollama_tool_call=failed_model
    with pytest.raises(OSError,match='primary model error'):
        rig.execute()
    snap=rig.binding.snapshot()
    assert snap['main_lifecycle']['restoration_error_type']=='ScoutRunnerHold'
    assert rig.runner.append_jsonl is outsider
    assert rig.events.count('helper_cleanup')==1


def test_returned_helper_cleanup_is_not_claimed_as_actual_dormancy(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    def quiet_failure():rig.events.append('helper_cleanup')  # Service deliberately remains up.
    rig.helper.cleanup=quiet_failure
    rig.execute()
    snap=rig.binding.snapshot()
    assert snap['helper_lifecycle']['cleanup_callback_returned'] is True and rig.service_up
    assert snap['helper_lifecycle']['actual_runtime_state_verified'] is False
    assert snap['main_lifecycle']['actual_runtime_state_verified'] is False


def test_full_main_preserves_all_parsed_warmstart_rows_against_unbound_main(tmp_path,monkeypatch,full_pb):
    raw=FullMainRig(tmp_path/'unbound',monkeypatch,full_pb,rounds=1)
    raw.binding.restore()
    raw.runner.main()  # Same complete main without candidate callbacks.
    candidate=FullMainRig(tmp_path/'bound',monkeypatch,full_pb,rounds=1)
    candidate.execute()
    left,right=raw.rows('warm-start.jsonl'),candidate.rows('warm-start.jsonl')
    for rows in (left,right):
        for row in rows:
            row.pop('run_id',None)
    assert left==right
    assert all(EVIDENCE_KEY not in row for row in right)
    assert all(row.get('training_candidate') is False for row in right if 'training_candidate' in row)
    assert not raw.service_up and not candidate.service_up


def test_repeated_helper_start_is_refused_before_second_callback(tmp_path,monkeypatch,full_pb):
    rig=FullMainRig(tmp_path,monkeypatch,full_pb)
    def attempted_restart(*args):
        rig.helper.start_ollama()
        raise AssertionError('second runtime start should not return')
    rig.helper.ollama_tool_call=attempted_restart
    with pytest.raises(ScoutRunnerHold,match='runtime_start_once'):
        rig.execute()
    assert rig.events.count('helper_start')==1
    assert rig.events.count('helper_cleanup')==1
    assert not rig.service_up and rig.world.controller_steps==0
