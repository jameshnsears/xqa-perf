from os import path

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
