"""Complete protoc schema and serialized in-process joint-step regressions.

These tests exercise real protobuf serialization, not gRPC HTTP/2 or an engine.
The world callbacks are the existing explicitly synthetic whole-main fixtures.
"""
import hashlib
from pathlib import Path
from types import SimpleNamespace

from google.protobuf import message_factory
from google.protobuf.message import DecodeError
import pytest

from scout_protocol_fixture_v1 import compiled_protocol, PROTO, PROTO_BLOB, PROTO_SHA256
from test_abaddon_scout_host_bridge_v1 import (
    InertStub, bridge, host, legacy, prepare, submit,
)
from test_abaddon_scout_full_main_v1 import FullMainRig
from openra_env.learning.abaddon_scout_host_bridge_v1 import ScoutHostHold


@pytest.fixture(scope='module')
def wire_pb():
    return compiled_protocol()


class SerializedStub:
    """In-process byte boundary using the real service's request/response types."""
    def __init__(self, pb, target, *, corrupt_joint_reply=False):
        self.pb, self.target = pb, target
        self.corrupt_joint_reply = corrupt_joint_reply
        self.records = []

    def _call(self, name, request, timeout):
        method = self.pb.DESCRIPTOR.services_by_name['RLBridge'].methods_by_name[name]
        assert request.DESCRIPTOR is method.input_type
        request_bytes = request.SerializeToString(deterministic=True)
        receiver = message_factory.GetMessageClass(method.input_type).FromString(request_bytes)
        assert receiver is not request
        response = getattr(self.target, name)(receiver, timeout)
        # The old fake DestroySession deliberately returned an empty namespace.
        # The actual schema has a zero-field response; encode that exact message.
        if name == 'DestroySession':
            response = self.pb.DestroySessionResponse()
        assert response.DESCRIPTOR is method.output_type
        reply_bytes = response.SerializeToString(deterministic=True)
        self.records.append({'method': name, 'request': request_bytes, 'response': reply_bytes})
        if name == 'JointAdvance' and self.corrupt_joint_reply:
            reply_bytes += b'\x80'  # Invalid unterminated varint: decoder must refuse.
        return message_factory.GetMessageClass(method.output_type).FromString(reply_bytes)

    def JointAdvance(self, request, timeout):
        return self._call('JointAdvance', request, timeout)

    def CreateSession(self, request, timeout):
        return self._call('CreateSession', request, timeout)

    def DestroySession(self, request, timeout):
        return self._call('DestroySession', request, timeout)

    def GetState(self, request, timeout):
        return self._call('GetState', request, timeout)


def test_exact_whole_schema_not_a_handbuilt_message_subset(wire_pb):
    raw = PROTO.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PROTO_SHA256
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == PROTO_BLOB
    assert wire_pb.DESCRIPTOR.name == 'rl_bridge.proto'
    assert wire_pb.DESCRIPTOR.package == 'openra.rl'
    assert wire_pb.DESCRIPTOR.GetOptions().csharp_namespace == 'OpenRA.Mods.Common.RL'
    assert len(wire_pb.DESCRIPTOR.message_types_by_name) == 20
    assert len(wire_pb.DESCRIPTOR.enum_types_by_name['ActionType'].values) == 23
    assert wire_pb.COMPILER_METADATA['message_count'] == 20
    assert wire_pb.COMPILER_METADATA['generated_grpc_client_or_server_executed'] is False


@pytest.mark.parametrize('name,input_name,output_name,streaming', [
    ('GameSession','AgentAction','GameObservation',True),
    ('GetState','StateRequest','GameState',False),
    ('FastAdvance','FastAdvanceRequest','GameObservation',False),
    ('JointAdvance','JointAdvanceRequest','JointAdvanceResponse',False),
    ('CreateSession','CreateSessionRequest','CreateSessionResponse',False),
    ('DestroySession','DestroySessionRequest','DestroySessionResponse',False),
])
def test_all_service_signatures_retained(wire_pb,name,input_name,output_name,streaming):
    method = wire_pb.DESCRIPTOR.services_by_name['RLBridge'].methods_by_name[name]
    assert method.input_type.full_name == 'openra.rl.'+input_name
    assert method.output_type.full_name == 'openra.rl.'+output_name
    assert method.client_streaming is streaming
    assert method.server_streaming is streaming


def test_formerly_omitted_observation_fields_survive_real_wire_roundtrip(wire_pb):
    p = wire_pb
    sample = p.GameObservation(tick=27,episode_id='ep',spatial_map=b'\x00\xff',spatial_channels=2,
        reward=0.5,interrupted=True,interrupt_reason='fixture',actual_ticks_advanced=25)
    sample.military.experience, sample.military.order_count = 13, 17
    sample.units.add(actor_id=2**32-1,type='e1',pos_x=900,pos_y=1200,
        cell_x=3,cell_y=4,hp_percent=0.5,is_idle=True,ammo=-1,speed=12,
        attack_range=123,passenger_count=-1,is_building=False)
    sample.buildings.add(actor_id=25,type='fact',is_producing=True,producing_item='powr',
        is_repairing=True,sell_value=200,rally_x=-1,rally_y=-1,power_amount=-25,
        can_produce=['powr','proc'],cell_x=10,cell_y=12)
    sample.production.add(queue_type='Building',item='powr',remaining_cost=100,paused=True)
    raw = sample.SerializeToString(deterministic=True)
    restored = p.GameObservation.FromString(raw)
    assert restored == sample and restored is not sample
    assert restored.units[0].actor_id == 2**32-1
    assert restored.units[0].ammo == -1
    assert restored.buildings[0].can_produce == ['powr','proc']
    assert restored.production[0].remaining_cost == 100


@pytest.mark.parametrize('actor', [-1, 2**32, -(2**63)])
def test_real_unsigned_actor_boundaries_reject(wire_pb,actor):
    with pytest.raises((ValueError,OverflowError)):
        wire_pb.Command(action=wire_pb.MOVE,actor_id=actor)


@pytest.mark.parametrize('tick', [-2**31-1, 2**31])
def test_real_signed_tick_boundaries_reject(wire_pb,tick):
    with pytest.raises((ValueError,OverflowError)):
        wire_pb.GameObservation(tick=tick)


def test_dispatch_acknowledges_only_after_serialized_matching_reply(legacy,host,wire_pb):
    b,c=bridge(legacy,host,wire_pb)
    proposal=prepare(b)
    target=InertStub(wire_pb,during=lambda: assert_unissued(c))
    transport=SerializedStub(wire_pb,target)
    response,observations=submit(b,proposal,transport)
    assert response.end_tick==25 and set(observations)=={'Multi0','Multi1'}
    assert len(target.calls)==1 and len(transport.records)==1
    request=wire_pb.JointAdvanceRequest.FromString(transport.records[0]['request'])
    assert request.player_actions[1].commands[0]==proposal['commands'][0]
    assert c.snapshot()['active']['status']=='ISSUED'
    assert c.snapshot()['history']==[]


def assert_unissued(controller):
    assert controller.snapshot()['active'] is None
    assert controller.snapshot()['pending_host_result'] is True


def test_corrupt_reply_after_possible_step_never_acknowledges_or_retries(legacy,host,wire_pb):
    b,c=bridge(legacy,host,wire_pb); proposal=prepare(b)
    target=InertStub(wire_pb)
    transport=SerializedStub(wire_pb,target,corrupt_joint_reply=True)
    with pytest.raises(DecodeError): submit(b,proposal,transport)
    assert len(target.calls)==1 and c.snapshot()['active'] is None
    assert b.snapshot()['runtime_effects_possible'] is True
    assert b.snapshot()['phase']=='HELD'
    with pytest.raises(ScoutHostHold): submit(b,proposal,transport)
    assert len(target.calls)==1


@pytest.mark.parametrize('mode',['session','shifted','short_step','observation_tick','missing_player','duplicate_player'])
def test_well_formed_but_wrong_wire_reply_still_rejects(legacy,host,wire_pb,mode):
    b,c=bridge(legacy,host,wire_pb); proposal=prepare(b)
    target=InertStub(wire_pb,mode=mode)
    with pytest.raises(RuntimeError): submit(b,proposal,SerializedStub(wire_pb,target))
    assert len(target.calls)==1 and c.snapshot()['active'] is None
    assert b.snapshot()['phase']=='HELD'


def test_unknown_command_bytes_cannot_change_a_prepared_scout(legacy,host,wire_pb):
    b,c=bridge(legacy,host,wire_pb); proposal=prepare(b)
    proposal['commands'][0].MergeFromString(b'\xa0\x06\x01')  # Unknown field 100.
    target=InertStub(wire_pb)
    with pytest.raises(ScoutHostHold,match='batch_changed'):
        submit(b,proposal,SerializedStub(wire_pb,target))
    assert target.calls==[] and c.snapshot()['active'] is None
    assert b.snapshot()['runtime_effects_possible'] is False


@pytest.mark.parametrize('rounds',[1,3,36])
def test_entire_historical_main_with_serialized_session_state_and_joint_messages(tmp_path,monkeypatch,wire_pb,rounds):
    rig=FullMainRig(tmp_path,monkeypatch,wire_pb,rounds=rounds)
    original_world=rig.world
    transport=SerializedStub(wire_pb,original_world)
    original_generate = rig.base.generate_proto
    def generate(path):
        protocol, _ = original_generate(path)
        return protocol, SimpleNamespace(RLBridgeStub=lambda channel:transport)
    rig.base.generate_proto = generate
    try:
        rig.binding.run_main_once()
        methods=[row['method'] for row in transport.records]
        assert methods.count('CreateSession')==1
        assert methods.count('DestroySession')==1
        assert methods.count('GetState')==rounds
        assert original_world.controller_steps==rounds
        assert not rig.service_up and not rig.container_up and not rig.session_up
        assert rig.binding.snapshot()['main_lifecycle']['actual_runtime_state_verified'] is False
    finally:
        # run_main_once normally restores; restoration is not world cleanup.
        if rig.binding.snapshot()['callbacks_installed']:
            rig.binding.restore()


def test_no_protocol_client_or_server_generated_or_started(wire_pb):
    source=(Path(__file__).with_name('scout_protocol_fixture_v1.py')).read_text()
    assert 'openra_env.generated' in source
    assert 'AddSerializedFile' in source
    assert '--python_out=' not in source
    assert '--grpc_python_out' not in source
    assert 'grpc_tools.protoc' not in source
    assert 'insecure_channel(' not in source
    assert 'grpc.server(' not in source
    assert wire_pb.COMPILER_METADATA['compiler_executed'] is False
