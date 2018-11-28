import pytest

from graphs.common import one_shard, two_shards, three_shards, four_shards, five_shards, six_shards, seven_shards, \
    eight_shards
from xqa.perf import wait_for_e2e_ingest_to_complete
from xqa.testing_support.chart import save_values_for_graphs, create_graphs
from xqa.testing_support.database import create_stats_db

INGEST_THREADS = 8

ingest_balancer = [
    {'image': 'xqa-ingest-balancer:latest',
     'name': 'xqa-ingest-balancer',
     'command': ['-message_broker_host', 'xqa-message-broker',
                 '-pool_size', '%s' % INGEST_THREADS,
                 '-insert_thread_wait', '60000',
                 '-insert_thread_secondary_wait', '1000'],
     'network': 'xqa'},
]


@pytest.fixture
def dockerpy_1_shard():
    return one_shard + ingest_balancer


@pytest.fixture
def dockerpy_2_shards():
    return two_shards + ingest_balancer


@pytest.fixture
def dockerpy_3_shards():
    return three_shards + ingest_balancer


@pytest.fixture
def dockerpy_4_shards():
    return four_shards + ingest_balancer


@pytest.fixture
def dockerpy_5_shards():
    return five_shards + ingest_balancer


@pytest.fixture
def dockerpy_6_shards():
    return six_shards + ingest_balancer


@pytest.fixture
def dockerpy_7_shards():
    return seven_shards + ingest_balancer


@pytest.fixture
def dockerpy_8_shards():
    return eight_shards + ingest_balancer


stats_db = create_stats_db()


def test_1_shard(dockerpy_1_shard):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 1)


def test_2_shards(dockerpy_2_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 2)


def test_3_shards(dockerpy_3_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 3)


def test_4_shards(dockerpy_4_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 4)


def test_5_shards(dockerpy_5_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 5)


def test_6_shards(dockerpy_6_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 6)


def test_7_shards(dockerpy_7_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 7)


def test_8_shards(dockerpy_8_shards):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 8)
    create_graphs(stats_db, INGEST_THREADS)
