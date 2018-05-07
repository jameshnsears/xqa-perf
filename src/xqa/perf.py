import logging
import os
import subprocess
import time
from os import path

import matplotlib.pyplot as plt
import psycopg2
from psycopg2._psycopg import List

from xqa.commons import configuration, sql_queries


class UnableToDetermineFinishState(Exception):
    pass


def invoke_e2e_env(pool_size: str, shards: str):
    logging.info('pool_size=%s; shards=%s' % (pool_size, shards))
    os.environ['POOL_SIZE'] = str(pool_size)
    os.environ['SHARDS'] = str(shards)

    process = subprocess.Popen([
        path.abspath(path.join(path.dirname(__file__), '../../bin/e2e.sh')),
        path.abspath(path.join(path.dirname(__file__), '../../docker-compose.dev.yml'))
    ], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        logging.debug(output)
    if error:
        logging.info(error)


def wait_for_e2e_env_to_process_test_data():
    _wait_for_service_to_complete('ingest')
    _wait_for_service_to_complete('ingestbalancer')
    _wait_for_service_to_complete('shard')


def get_ingest_count() -> int:
    return _query_db_for_count(sql_queries.get_ingest_count)


def get_ingest_size() -> int:
    return int(_query_db_for_count(sql_queries.get_ingest_size))


def how_long_service_took_to_process_ingest(service_id: str) -> int:
    return _query_db_for_count(sql_queries.how_long_service_took_to_process_test_data % service_id)


def _wait_for_service_to_complete(stage: str):
    test_data_items = 40
    sleep_attempts = 1

    while _query_db_for_count(sql_queries.count_items % stage) != test_data_items:
        logging.info('%s=%d' % (stage, sleep_attempts))
        time.sleep(sleep_attempts)

        if sleep_attempts > test_data_items:
            raise UnableToDetermineFinishState

        sleep_attempts += 1


def _query_db_for_count(sql: str) -> int:
    try:
        connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                                      (configuration.storage_database_name,
                                       configuration.storage_user,
                                       configuration.storage_host,
                                       configuration.storage_password))
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()[0][0]
    except Exception:
        pass


def make_png(e2e_stats: List, location_to_save_chart):
    logging.info(location_to_save_chart)

    number_of_shards = []
    ingest = []
    ingest_balancer = []
    shard = []

    for row in e2e_stats:
        pool_size = row[0]
        number_of_shards.append(row[1])
        ingest_count = row[2]
        ingest_size = row[3]
        ingest.append(row[4])
        ingest_balancer.append(row[5])
        shard.append(row[6])
        logging.info(row)

    plt.plot(number_of_shards, ingest, marker='x', color='red', label='ingest')
    plt.plot(number_of_shards, ingest_balancer, marker='x', color='grey', label='ingest-balancer')
    plt.plot(number_of_shards, shard, marker='x', color='blue', label='shard')

    # plt.grid()
    plt.xlabel('shards')
    plt.ylabel('seconds')
    plt.title('%s bytes / %s items; %s ingest-balancer threads' % (ingest_size, ingest_count, pool_size))
    plt.legend()

    # plt.show()
    plt.savefig(location_to_save_chart)
    plt.close()
