from os import path

import pytest

from xqa.perf import wait_for_e2e_ingest_to_complete
from xqa.testing_support.chart import create_graphs
from xqa.testing_support.chart import save_values_for_graphs
from xqa.testing_support.database import create_stats_db


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
         'ports': {'1983/tcp': None},
         'command': ['-message_broker_host', 'xqa-message-broker'],
         'network': 'xqa'},

        {'image': 'jameshnsears/xqa-ingest-balancer:latest',
         'name': 'xqa-ingest-balancer',
         'command': ["-message_broker_host", "xqa-message-broker", "-pool_size", '1'],
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


@pytest.mark.timeout(320)
def test_1_ingest_thread_and_1_shard(dockerpy, pool_size=1, shards=1):
    wait_for_e2e_ingest_to_complete()
    save_values_for_graphs(stats_db, pool_size, shards)
    create_graphs(stats_db, pool_size)
