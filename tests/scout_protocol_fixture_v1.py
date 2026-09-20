"""Use the accepted repository's complete generated protobuf descriptor offline.

The source .proto fixture is hash-bound to accepted main, and the committed
``openra_env.generated.rl_bridge_pb2`` descriptor must expose the same complete
message/enum/service surface. No compiler, generated gRPC client/server, RPC,
package installation, network, model, engine, or service is invoked.
"""
from functools import lru_cache
import hashlib
from pathlib import Path
from types import SimpleNamespace

from google.protobuf import descriptor_pool, message_factory
from openra_env.generated import rl_bridge_pb2 as generated_pb2

PROTO = Path(__file__).resolve().parents[1] / 'fixtures/learning/scout-missions-v1/rl_bridge.proto'
PROTO_BLOB = 'a20e85cf7d9f3b4c1523b1916569942d7b74e694'
PROTO_SHA256 = '9a48ca90bd525b7fd5502e7426cd8c1bb96b1308c2b18904d4d7af023699eae3'
GENERATED_DESCRIPTOR_SHA256 = '9ddf76b88e85556de8098c0a110574a2886a0ea6e64ca4570f9e8ca96215a4dc'


@lru_cache(maxsize=1)
def compiled_protocol():
    """Build fresh message classes from the committed complete descriptor."""
    raw = PROTO.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != PROTO_BLOB or hashlib.sha256(raw).hexdigest() != PROTO_SHA256:
        raise RuntimeError('full protocol fixture identity mismatch')

    serialized = generated_pb2.DESCRIPTOR.serialized_pb
    if hashlib.sha256(serialized).hexdigest() != GENERATED_DESCRIPTOR_SHA256:
        raise RuntimeError('committed generated protocol descriptor identity mismatch')
    source_descriptor = generated_pb2.DESCRIPTOR
    if source_descriptor.name != 'rl_bridge.proto' or source_descriptor.package != 'openra.rl':
        raise RuntimeError('protocol namespace/schema drift')
    if len(source_descriptor.message_types_by_name) != 20:
        raise RuntimeError('complete protocol message count drift')
    action = source_descriptor.enum_types_by_name.get('ActionType')
    service = source_descriptor.services_by_name.get('RLBridge')
    if action is None or len(action.values) != 23 or service is None or len(service.methods) != 6:
        raise RuntimeError('complete protocol enum/service surface drift')

    # Use a fresh pool so the tests do not return the repository module's classes.
    pool = descriptor_pool.DescriptorPool()
    descriptor = pool.AddSerializedFile(serialized)
    values = {value.name: value.number for value in descriptor.enum_types_by_name['ActionType'].values}
    values.update({name: message_factory.GetMessageClass(
        pool.FindMessageTypeByName('openra.rl.' + name))
        for name in descriptor.message_types_by_name})
    values['DESCRIPTOR'] = descriptor
    values['COMPILER_METADATA'] = {
        'version': 'committed-generated-descriptor',
        'source_sha256': PROTO_SHA256,
        'source_git_blob': PROTO_BLOB,
        'descriptor_set_sha256': GENERATED_DESCRIPTOR_SHA256,
        'message_count': len(descriptor.message_types_by_name),
        'enum_value_count': len(descriptor.enum_types_by_name['ActionType'].values),
        'service_count': len(descriptor.services_by_name),
        'rpc_method_count': len(descriptor.services_by_name['RLBridge'].methods),
        'generated_grpc_client_or_server_executed': False,
        'compiler_executed': False,
    }
    return SimpleNamespace(**values)
