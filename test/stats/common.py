import os
from os import path

os.environ["PYTEST_DOCKER_PY_KEEP_LOGS"] = "1"

one_shard = [
    {'image': 'google/cadvisor:latest',
     'name': 'cadvisor',
     'ports': {'8080/tcp': 8888},
     'volumes': {
         '/': {'bind': '/rootfs', 'mode': 'ro'},
         '/var/run': {'bind': '/var/run', 'mode': 'rw'},
         '/sys': {'bind': '/sys', 'mode': 'ro'},
         '/var/lib/docker/': {'bind': '/var/lib/docker', 'mode': 'ro'},
         '/dev/disk': {'bind': '/dev/disk', 'mode': 'ro'}},
     },

    {'image': 'xqa-message-broker:latest',
     'name': 'xqa-message-broker',
     'ports': {'5672/tcp': 5672, '8161/tcp': 8161},
     'network': 'xqa'},

    {'image': 'xqa-db:latest',
     'name': 'xqa-db',
     'ports': {'5432/tcp': 5432},
     'network': 'xqa'},

    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-01',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},

    {'image': 'xqa-db-amqp:latest',
     'name': 'xqa-db-amqp',
     'command': ['-message_broker_host', 'xqa-message-broker', '-storage_host', 'xqa-db', '-storage_port', '5432'],
     'network': 'xqa'},

    {'image': 'xqa-ingest:latest',
     'name': 'xqa-ingest',
     'command': ['-message_broker_host', 'xqa-message-broker', '-path', '/xml'],
     'volumes': {
         path.abspath(path.join(path.dirname(__file__), '../../../xqa-test-data')): {'bind': '/xml', 'mode': 'rw'}},
     'network': 'xqa'
     }
]

two_shards = one_shard + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-02',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'}
]

three_shards = two_shards + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-03',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},
]

four_shards = three_shards + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-04',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},
]

five_shards = four_shards + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-05',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},
]

six_shards = five_shards + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-06',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},
]

seven_shards = six_shards + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-07',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},
]

eight_shards = seven_shards + [
    {'image': 'xqa-shard:latest',
     'name': 'xqa-shard-08',
     'ports': {'1984/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},
]
