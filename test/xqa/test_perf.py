import time
from os import path

import pytest

from xqa.perf import wait_for_e2e_ingest_to_complete
from xqa.testing_support.chart import create_graphs
from xqa.testing_support.chart import save_values_for_graphs
from xqa.testing_support.database import create_stats_db

INGEST_THREADS = 2


@pytest.fixture
def dockerpy():
    return [
        {'image': 'jameshnsears/xqa-message-broker:latest',
         'name': 'xqa-message-broker',
         'ports': {'5672/tcp': 5672, '8161/tcp': 8161},
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-db:latest',
         'name': 'xqa-db',
         'ports': {'5432/tcp': 5432},
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-shard:latest',
         'name': 'xqa-shard-01',
         'ports': {'1984/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-shard:latest',
         'name': 'xqa-shard-02',
         'ports': {'1984/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-ingest-balancer:latest',
         'name': 'xqa-ingest-balancer',
         'command': ['-message_broker_host', 'xqa-message-broker',
                     '-pool_size', '%s' % INGEST_THREADS,
                     '-insert_thread_wait', '2000'],
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-db-amqp:latest',
         'name': 'xqa-db-amqp',
         'command': ['-message_broker_host', 'xqa-message-broker', '-storage_host', 'xqa-db', '-storage_port', '5432'],
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-ingest:latest',
         'name': 'xqa-ingest',
         'command': ['-message_broker_host', 'xqa-message-broker', '-path', '/xml'],
         'volumes': {
             path.abspath(path.join(path.dirname(__file__), '../../../xqa-test-data')): {'bind': '/xml', 'mode': 'rw'}},
         'network': 'xqa'
         }
    ]


stats_db = create_stats_db()


def test_2_shards_2_clients(dockerpy):
    # give travis time to start all the containers
    time.sleep(30)

    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, INGEST_THREADS, 2)
    create_graphs(stats_db, INGEST_THREADS)
