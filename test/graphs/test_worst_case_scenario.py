import pytest

from graphs.common import one_shard
from xqa.perf import wait_for_e2e_ingest_to_complete
from xqa.testing_support.chart import save_values_for_graphs, create_graphs
from xqa.testing_support.database import create_stats_db

INGEST_THREADS = 1

ingest_balancer = [
    {'image': 'xqa-ingest-balancer:latest',
     'name': 'xqa-ingest-balancer',
     'command': ['-message_broker_host', 'xqa-message-broker',
                 '-pool_size', '%s' % INGEST_THREADS,
                 '-insert_thread_wait', '1000',
                 '-insert_thread_secondary_wait', '2000'],
     'network': 'xqa'},
]


@pytest.fixture
def dockerpy_1_shard():
    return one_shard + ingest_balancer


stats_db = create_stats_db()


def test_1_shards_1_client(dockerpy_1_shard):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 1)
    create_graphs(stats_db, INGEST_THREADS)
