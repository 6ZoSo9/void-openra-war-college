"""Pure controller tests: saved observations and synthetic accepted/rejected feedback.

No command dispatcher, model, engine, or new game is used. Changed proposals on
historical inputs are not counterfactual gameplay outcomes.
"""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

from openra_env.learning.abaddon_scout_missions_v1 import (
    MissionPolicy, ScoutMissionController, ScoutMissionHold,
)
from openra_env.learning.goal_effect_core_v1 import Scope

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'fixtures/learning/scout-missions-v1'
SAVED = (FIXTURE / 'pair03_saved_observations.json').read_bytes()
assert hashlib.sha256(SAVED).hexdigest() == '2c88f2a81dababba939fe839a3161e6d26833dee1a634670dc01164859224cff'
DATA = json.loads(SAVED)
SCOPE = Scope('offline-scout-regression', 'abaddon', 'frozen-openra-input-v1', 'game_ticks')


@pytest.fixture(scope='module')
def legacy():
    path = FIXTURE / 'abaddon_controller_v1.py'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == DATA['controller_sha256']
    spec = importlib.util.spec_from_file_location('scout_tests_frozen_controller', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def controller(legacy, **kwargs):
    return ScoutMissionController(legacy, scope=SCOPE, doctrine='FEINTER', seed=1990061685, **kwargs)


def obs(tick=0):
    return {'tick': tick, 'map': {'width': 112, 'height': 54}, 'enemy_summary': [],
            'enemy_buildings_summary': [], 'available_production': [], 'production_items': [],
            'economy': {'cash': 0, 'ore': 0, 'harvester_count': 1}, 'power_balance': 100,
            'explored_percent': 10, 'buildings_summary': [
                {'id': 1, 'type': 'fact', 'cell_x': 5, 'cell_y': 5},
                {'id': 2, 'type': 'proc', 'cell_x': 6, 'cell_y': 5},
                {'id': 3, 'type': 'barr', 'cell_x': 5, 'cell_y': 6}],
            'units_summary': [{'id': n, 'type': 'e1', 'can_attack': True, 'cell_x': 20,
                               'cell_y': 20, 'idle': n != 10, 'is_idle': n != 10,
                               'activity': 'Move' if n == 10 else '',
                               'current_activity': 'Move' if n == 10 else '', 'hp_percent': 1.0}
                              for n in (10, 20, 30, 40, 50, 60)]}


def propose(c, o, evidence=None):
    return c.decide(o, scope=SCOPE, evidence_id=evidence or f'sample:{o["tick"]}')


def accept(c, p, count=None):
    action = p['decision']['action']
    return c.acknowledge(p['proposal_id'], accepted=True,
                         command_count=(0 if action['tool'] == 'advance' else 1) if count is None else count)


def row(o, uid=20):
    return next(u for u in o['units_summary'] if u['id'] == uid)


def busy(o, uid=20):
    row(o, uid).update(idle=False, is_idle=False, activity='Move', current_activity='Move')


def test_proposal_host_acceptance_and_arrival_are_separate(legacy):
    c = controller(legacy)
    o = obs()
    untouched = deepcopy(o)
    p = propose(c, o)
    assert o == untouched
    assert p['execution_authorized'] is False and p['host_validation_required'] is True
    assert p['decision']['action']['arguments']['unit_ids'] == '20'  # Not busy lowest-ID 10.
    assert c.snapshot()['active'] is None and c.snapshot()['history'] == []
    assert p['decision']['memory']['scout_targets'] == []
    accepted = accept(c, p)
    assert accepted['active']['status'] == 'ISSUED' and accepted['history'] == []
    target = accepted['active']['target']
    later = obs(25)
    row(later).update(cell_x=target[0], cell_y=target[1])
    p = propose(c, later)
    completed = [h for h in c.snapshot()['history'] if h['status'] == 'COMPLETED']
    assert [h['target'] for h in completed] == [target]
    assert p['decision']['memory']['scout_targets'] == [list(target)]
    assert c.snapshot()['last_event']['status'] == 'COMPLETED'


def test_rejected_scout_never_creates_assignment_or_visit(legacy):
    c = controller(legacy)
    p = propose(c, obs())
    out = c.acknowledge(p['proposal_id'], accepted=False, command_count=0)
    assert out['active'] is None and out['history'] == []
    assert out['last_event']['status'] == 'REJECTED'
    assert propose(c, obs(25))['decision']['action']['tool'] == 'move_units'


def test_unresolved_bad_and_duplicate_acknowledgements_hold(legacy):
    c = controller(legacy)
    p = propose(c, obs())
    with pytest.raises(ScoutMissionHold, match='acknowledgement'):
        propose(c, obs(25))
    for pid, accepted, count in [('wrong', True, 1), (p['proposal_id'], 1, 1),
                                 (p['proposal_id'], True, 0), (p['proposal_id'], False, 1),
                                 (p['proposal_id'], True, True)]:
        before = c.snapshot()
        with pytest.raises(ScoutMissionHold):
            c.acknowledge(pid, accepted=accepted, command_count=count)
        assert c.snapshot() == before
    accept(c, p)
    with pytest.raises(ScoutMissionHold):
        accept(c, p)


def test_progress_retains_assignment_without_repeated_move_commands(legacy):
    c = controller(legacy, mission_policy=MissionPolicy(stall_ticks=50, maximum_mission_ticks=200))
    p = propose(c, obs()); accept(c, p)
    target = c.snapshot()['active']['target']
    for i, tick in enumerate((25, 60, 90, 120), 1):
        o = obs(tick); busy(o)
        row(o)['cell_x'] += i
        p = propose(c, o)
        assert p['decision']['action']['tool'] == 'advance'
        assert p['decision']['reason_codes'] == ['SCOUT_MISSION_IN_PROGRESS']
        assert c.snapshot()['active']['target'] == target
        assert c.snapshot()['history'] == []
        accept(c, p)


def test_progress_cannot_evade_absolute_mission_bound(legacy):
    c = controller(legacy, mission_policy=MissionPolicy(stall_ticks=50, maximum_mission_ticks=75))
    accept(c, propose(c, obs()))
    for i, tick in enumerate((25, 50, 75), 1):
        o = obs(tick); busy(o); row(o)['cell_x'] += i
        accept(c, propose(c, o))
    assert any(h['reason'] == 'maximum_mission_window_elapsed' for h in c.snapshot()['history'])


def test_oscillation_and_unrelated_production_do_not_reset_stall(legacy):
    c = controller(legacy, mission_policy=MissionPolicy(stall_ticks=50, maximum_mission_ticks=300))
    accept(c, propose(c, obs()))
    first = c.snapshot()['active']['target']
    for tick, x in ((25, 21), (50, 20), (75, 21)):
        o = obs(tick); busy(o); row(o)['cell_x'] = x
        o['economy']['cash'] = tick * 100
        o['production_items'] = [f'weap@{tick}%']
        p = propose(c, o); accept(c, p)
    assert any(h['target'] == first and h['status'] == 'FAILED' for h in c.snapshot()['history'])
    assert c.snapshot()['active']['unit_id'] != 20  # Busy stale assignment not blindly retasked.
    assert c.snapshot()['active']['target'] != first


@pytest.mark.parametrize('case', ['absent', 'zero_health', 'changed_type', 'noncombat'])
def test_lost_actor_releases_mission_without_recording_visit(legacy, case):
    c = controller(legacy)
    accept(c, propose(c, obs()))
    target = c.snapshot()['active']['target']
    o = obs(25)
    if case == 'absent': o['units_summary'] = [u for u in o['units_summary'] if u['id'] != 20]
    elif case == 'zero_health': row(o)['hp_percent'] = 0
    elif case == 'changed_type': row(o)['type'] = 'jeep'
    else: row(o)['can_attack'] = False
    p = propose(c, o)
    assert any(h['target'] == target and h['status'] == 'FAILED' for h in c.snapshot()['history'])
    assert p['decision']['memory']['scout_targets'] == []
    assert p['decision']['action']['arguments']['unit_ids'] != '20'


def test_contact_priority_interrupts_only_after_host_acceptance(legacy):
    c = controller(legacy)
    accept(c, propose(c, obs()))
    o = obs(25); o['enemy_summary'] = [{'id': 99, 'type': 'e1', 'cell_x': 22, 'cell_y': 21}]
    p = propose(c, o)
    assert p['decision']['action']['tool'] == 'attack_target'
    assert c.snapshot()['active'] is not None
    c.acknowledge(p['proposal_id'], accepted=False, command_count=0)
    assert c.snapshot()['active'] is not None
    o['tick'] = 50
    p = propose(c, o); accept(c, p)
    assert c.snapshot()['active'] is None
    assert c.snapshot()['history'][0]['status'] == 'INTERRUPTED'
    assert c.snapshot()['history'][0]['reason'] == 'accepted_higher_priority_order'


def test_production_priority_is_unchanged_and_does_not_cancel_scout(legacy):
    c = controller(legacy)
    accept(c, propose(c, obs()))
    old = c.snapshot()['active']['id']
    o = obs(25); o['available_production'] = ['powr']; o['power_balance'] = 0
    frozen = legacy.AbaddonController('FEINTER', 1990061685).decide(deepcopy(o))
    p = propose(c, o)
    assert p['decision']['action'] == frozen['action']
    assert p['decision']['reason_codes'] == frozen['reason_codes']
    accept(c, p)
    assert c.snapshot()['active']['id'] == old


@pytest.mark.parametrize('case', ['missing_idle', 'busy', 'inconsistent_activity'])
def test_uncertain_or_busy_unit_is_not_new_scout(legacy, case):
    c = controller(legacy)
    o = obs()
    for u in o['units_summary']:
        if case == 'missing_idle':
            u.pop('idle'); u.pop('is_idle'); u['activity'] = u['current_activity'] = ''
        elif case == 'busy': busy(o, u['id'])
        else: u.update(idle=True, is_idle=True, activity='Attack', current_activity='Attack')
    p = propose(c, o)
    assert p['decision']['action']['tool'] == 'advance'
    assert p['decision']['reason_codes'] == ['NO_ELIGIBLE_IDLE_SCOUT']
    accept(c, p)
    assert c.snapshot()['active'] is None


@pytest.mark.parametrize('bad', [
    lambda o: o.update(tick=True), lambda o: o.update(map={}),
    lambda o: o.update(units_summary=None), lambda o: o['units_summary'].append(deepcopy(o['units_summary'][0])),
    lambda o: row(o).update(cell_x=-1), lambda o: row(o).update(can_attack='true'),
    lambda o: row(o).update(idle=False, is_idle=True), lambda o: row(o).update(hp_percent=float('nan')),
    lambda o: o.pop('enemy_summary'), lambda o: o.update(minimap='x'*65537),
])
def test_invalid_evidence_has_no_partial_state_effect(legacy, bad):
    c = controller(legacy); o = obs(); before = c.snapshot(); bad(o)
    with pytest.raises(ScoutMissionHold): propose(c, o)
    assert c.snapshot() == before


def test_scope_evidence_clock_and_map_binding(legacy):
    c = controller(legacy); accept(c, propose(c, obs(), 'first'))
    for o, scope, eid in [(obs(), SCOPE, 'next'), (obs(25), SCOPE, 'first'),
                          (obs(25), Scope('other', 'abaddon', SCOPE.world_revision, 'game_ticks'), 'next')]:
        before = c.snapshot()
        with pytest.raises(ScoutMissionHold): c.decide(o, scope=scope, evidence_id=eid)
        assert c.snapshot() == before
    o = obs(25); o['map']['width'] = 200
    with pytest.raises(ScoutMissionHold, match='map_changed'): propose(c, o)


@pytest.mark.parametrize('overrides', [{'stall_ticks':0}, {'stall_ticks':True}, {'arrival_radius':-1},
                                       {'maximum_mission_ticks':1}, {'maximum_history':0}])
def test_invalid_mission_policy(overrides):
    with pytest.raises(ScoutMissionHold): MissionPolicy(**overrides)


def test_completed_and_failed_history_expires_by_ticks_not_order_count(legacy):
    c = controller(legacy, mission_policy=MissionPolicy(stall_ticks=25, maximum_mission_ticks=100,
                                                        failed_cooldown_ticks=50, completed_cooldown_ticks=50))
    accept(c, propose(c, obs()))
    target = c.snapshot()['active']['target']
    o = obs(25); busy(o)
    p = propose(c, o); c.acknowledge(p['proposal_id'], accepted=False, command_count=0)
    assert c.snapshot()['history'][0]['expires_tick'] == 75
    p = propose(c, obs(75))
    assert c.snapshot()['history'] == []
    assert (p['decision']['action']['arguments']['target_x'], p['decision']['action']['arguments']['target_y']) == target


def test_public_results_do_not_mutate_controller_state(legacy):
    c = controller(legacy); p = propose(c, obs()); accept(c, p)
    view = c.snapshot(); view['active']['target'] = (0,0); view['history'].append('bad')
    p['decision']['action']['arguments']['target_x'] = -999
    assert c.snapshot()['active']['target'] != (0,0) and c.snapshot()['history'] == []


def test_saved_round10_does_not_retask_busy_unit142_without_an_idle_scout(legacy):
    saved = next(r for r in DATA['streams']['candidate']['rows'] if r['round'] == 10)
    c = controller(legacy, policy=DATA['candidate_policy'])
    p = propose(c, deepcopy(saved['observation']))
    assert saved['original_decision']['action']['arguments']['unit_ids'] == '142'
    assert all(not u['is_idle'] for u in saved['observation']['units_summary'] if u['can_attack'])
    assert p['decision']['action']['tool'] == 'advance'
    assert p['decision']['reason_codes'] == ['NO_ELIGIBLE_IDLE_SCOUT']
    assert p['decision']['memory']['scout_targets'] == []


def test_saved_round17_is_not_permanently_exhausted_by_six_old_orders(legacy):
    saved = next(r for r in DATA['streams']['candidate']['rows'] if r['round'] == 17)
    assert len(saved['original_decision']['memory']['scout_targets']) == 6
    assert saved['original_decision']['action']['tool'] == 'advance'
    c = controller(legacy, policy=DATA['candidate_policy'])
    p = propose(c, deepcopy(saved['observation']))
    assert p['decision']['action']['tool'] == 'move_units'
    assert c.snapshot()['active'] is None
    assert c.snapshot()['history'] == []
    accept(c, p)
    assert c.snapshot()['active']['status'] == 'ISSUED'


def test_saved_sequence_does_not_mark_unreached_orders_completed(legacy):
    c = controller(legacy, policy=DATA['candidate_policy'])
    counts = {'proposed_scouts':0, 'retained_assignments':0}
    for saved in DATA['streams']['candidate']['rows']:
        if saved['round'] > 18: continue
        o = deepcopy(saved['observation']); before = deepcopy(o)
        p = propose(c, o)
        assert o == before
        counts['proposed_scouts'] += p['decision']['reason_codes'] == ['SCOUT_MISSION_PROPOSED_NOT_ISSUED']
        counts['retained_assignments'] += p['decision']['reason_codes'] == ['SCOUT_MISSION_IN_PROGRESS']
        accept(c, p)  # Synthetic acknowledgement, NOT a saved host verdict for a changed action.
    assert counts['retained_assignments'] > 0
    assert counts['proposed_scouts'] < 6
    assert all(h['status'] != 'COMPLETED' for h in c.snapshot()['history'])


@pytest.mark.parametrize('arm', ['baseline', 'candidate'])
def test_saved_round33_contact_difference_keeps_original_priority(legacy, arm):
    saved = next(r for r in DATA['streams'][arm]['rows'] if r['round'] == 33)
    c = controller(legacy, policy=DATA['candidate_policy'] if arm == 'candidate' else None)
    p = propose(c, deepcopy(saved['observation']))
    assert p['decision']['action']['tool'] == ('attack_target' if arm == 'baseline' else 'move_units')


def test_historical_sources_and_monitor_are_exact_and_not_globally_patched(legacy):
    core = ROOT/'openra_env/learning/goal_effect_core_v1.py'
    assert hashlib.sha256(core.read_bytes()).hexdigest() == 'eaa344512cd8895dff9c21011f6cee34cdeabdd85118e59a4e172334cf39661e'
    before = (legacy.AbaddonController, legacy._scout_target, deepcopy(legacy.PROFILES))
    c = controller(legacy); accept(c, propose(c, obs()))
    assert (legacy.AbaddonController, legacy._scout_target, legacy.PROFILES) == before
    assert c.snapshot()['execution_authorized'] is False
    assert c.snapshot()['runtime_integration_active'] is False


def test_accepted_zero_command_contact_does_not_cancel_existing_order(legacy):
    c = controller(legacy); accept(c, propose(c, obs()))
    prior = c.snapshot()['active']['id']
    o = obs(25); o['enemy_summary'] = [{'id': 99, 'type': 'e1', 'cell_x': 22, 'cell_y': 21}]
    p = propose(c, o); accept(c, p, count=0)
    assert c.snapshot()['active']['id'] == prior


@pytest.mark.parametrize('gap,complete', [(3, False), (2, True)])
def test_arrival_radius_uses_observed_position_not_busy_flag(legacy, gap, complete):
    c = controller(legacy); accept(c, propose(c, obs()))
    x, y = c.snapshot()['active']['target']
    o = obs(25); busy(o); row(o).update(cell_x=x-gap, cell_y=y)
    propose(c, o)
    assert any(h['status'] == 'COMPLETED' for h in c.snapshot()['history']) is complete


def test_observation_budget_is_not_silently_reset(legacy, monkeypatch):
    import openra_env.learning.abaddon_scout_missions_v1 as source
    monkeypatch.setattr(source, 'MAX_OBSERVATIONS', 1)
    c = controller(legacy); accept(c, propose(c, obs()))
    before = c.snapshot()
    with pytest.raises(ScoutMissionHold, match='observation_capacity'):
        propose(c, obs(25))
    assert c.snapshot() == before


def test_history_capacity_refuses_new_orders_without_discarding_entries(legacy):
    c = controller(legacy, mission_policy=MissionPolicy(maximum_history=1))
    accept(c, propose(c, obs()))
    x,y = c.snapshot()['active']['target']
    o = obs(25); row(o).update(cell_x=x,cell_y=y)
    # A full retained-history budget is an explicit hold, not silent eviction.
    before = c.snapshot()
    with pytest.raises(ScoutMissionHold, match='history_capacity'):
        propose(c,o)
    assert c.snapshot() == before


def test_independent_controllers_do_not_share_missions_or_caller_policy(legacy):
    p = {'group':3, 'scout_history_min':20}
    a = controller(legacy, policy=p); b = controller(legacy, policy=p)
    p['group'] = 99
    proposal = propose(a, obs()); accept(a, proposal)
    assert b.snapshot()['active'] is None
    assert a._base.profile['group'] == b._base.profile['group'] == 3
    assert propose(b,obs())['decision'] == proposal['decision']
