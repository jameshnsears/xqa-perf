from os import path

import pytest

from xqa.perf import wait_for_e2e_ingest_to_complete
from xqa.testing_support.chart import save_values_for_graphs, create_graphs
from xqa.testing_support.database import create_stats_db

common_containers = [
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
     'ports': {'1983/tcp': None},
     'command': ['-message_broker_host', 'xqa-message-broker'],
     'network': 'xqa'},

    {'image': 'xqa-ingest-balancer:latest',
     'name': 'xqa-ingest-balancer',
     'command': ["-message_broker_host", "xqa-message-broker", "-pool_size", '1'],
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


@pytest.fixture
def dockerpy_1_shard():
    return common_containers


@pytest.fixture
def dockerpy_2_shards():
    return common_containers + [
        {'image': 'xqa-shard:latest',
         'name': 'xqa-shard-02',
         'ports': {'1983/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'}]


@pytest.fixture
def dockerpy_4_shards():
    return common_containers + [
        {'image': 'xqa-shard:latest',
         'name': 'xqa-shard-02',
         'ports': {'1983/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'},
        {'image': 'xqa-shard:latest',
         'name': 'xqa-shard-03',
         'ports': {'1983/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'},
        {'image': 'xqa-shard:latest',
         'name': 'xqa-shard-04',
         'ports': {'1983/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'},
    ]


stats_db = create_stats_db()


@pytest.mark.timeout(320)
def test_1_shard(dockerpy_1_shard, pool_size=1):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, pool_size, 1)


@pytest.mark.timeout(320)
def test_2_shards(dockerpy_2_shards, pool_size=1):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, pool_size, 2)


@pytest.mark.timeout(320)
def test_4_shards(dockerpy_4_shards, pool_size=1):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, pool_size, 4)


def test_create_graphs():
    create_graphs(stats_db, 1, 4)
