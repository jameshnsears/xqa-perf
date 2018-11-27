import pytest

from stats.common import common_containers
from xqa.perf import wait_for_e2e_ingest_to_complete
from xqa.testing_support.chart import save_values_for_graphs, create_graphs
from xqa.testing_support.database import create_stats_db

INGEST_THREADS = 1

containers = common_containers + [
    {'image': 'xqa-ingest-balancer:latest',
     'name': 'xqa-ingest-balancer',
     'command': ["-message_broker_host", "xqa-message-broker", "-pool_size", '1'],
     'network': 'xqa'},
]


@pytest.fixture
def dockerpy_1_shard():
    return containers


@pytest.fixture
def dockerpy_2_shards():
    return containers + [
        {'image': 'xqa-shard:latest',
         'name': 'xqa-shard-02',
         'ports': {'1983/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'}
    ]


@pytest.fixture
def dockerpy_3_shards():
    return containers + [
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
    ]


@pytest.fixture
def dockerpy_4_shards():
    return containers + [
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
def test_1_shard(dockerpy_1_shard):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 1)


@pytest.mark.timeout(320)
def test_2_shards(dockerpy_2_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 2)


@pytest.mark.timeout(320)
def test_3_shards(dockerpy_3_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 3)


@pytest.mark.timeout(320)
def test_4_shards(dockerpy_4_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 4)


def test_create_graphs():
    create_graphs(stats_db, INGEST_THREADS, 4)
