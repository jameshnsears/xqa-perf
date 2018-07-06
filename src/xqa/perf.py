import logging
import os
import subprocess
import time
from os import path
from typing import List

import psycopg2

from xqa.commons import configuration, sql_queries
from xqa.commons.charting.line_chart import LineChart
from xqa.commons.charting.stacked_bar_chart import StackedBarChart


class UnableToDetermineFinishState(Exception):
    pass


def invoke_e2e_env(pool_size: int, shards: int):
    logging.info('pool_size=%s; shards=%s' % (pool_size, shards))
    os.environ['POOL_SIZE'] = str(pool_size)
    os.environ['SHARDS'] = str(shards)

    process = subprocess.Popen([
        path.abspath(path.join(path.dirname(__file__), '../../bin/e2e.sh')),
        path.abspath(path.join(path.dirname(__file__), '../../docker-compose.dev.yml'))
    ], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if output:
        logging.debug(output.decode("utf-8"))
    if error:
        logging.error(error)


def wait_for_e2e_env_to_finish():
    _wait_for_service_to_complete('ingest')
    _wait_for_service_to_complete('ingestbalancer')
    _wait_for_service_to_complete('shard')


def get_ingest_count() -> int:
    return _query_db_for_count(sql_queries.get_ingest_count)


def get_ingest_size() -> int:
    return int(_query_db_for_count(sql_queries.get_ingest_size))


def how_long_service_took_to_process_ingest(service_id: str) -> int:
    return _query_db_for_count(sql_queries.how_long_service_took_to_process_test_data % service_id)


def _wait_for_service_to_complete(stage: str, test_data_items: int = 40):
    sleep_attempts = 1

    while _query_db_for_count(sql_queries.count_items % stage) != test_data_items:
        logging.info('%s=%d' % (stage, sleep_attempts))
        time.sleep(sleep_attempts)

        if sleep_attempts > test_data_items:
            raise UnableToDetermineFinishState

        sleep_attempts += 1


def _query_db_for_count(sql: str) -> int:
    connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                                  (configuration.storage_database_name,
                                   configuration.storage_user,
                                   configuration.storage_host,
                                   configuration.storage_password))
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchall()[0][0]


def get_item_count_to_shard_distribution() -> List:
    connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                                  (configuration.storage_database_name,
                                   configuration.storage_user,
                                   configuration.storage_host,
                                   configuration.storage_password))
    cursor = connection.cursor()
    cursor.execute(sql_queries.item_count_to_shard_distribution)
    return cursor.fetchall()


def make_png_shard_stats(shard_stats: List, location_to_save_chart: str):
    logging.info(location_to_save_chart)

    stacked_bar_chart = StackedBarChart(shard_stats)
    stacked_bar_chart.construct_bars()
    stacked_bar_chart.annotate()
    StackedBarChart.write(location_to_save_chart)


def make_png_timing_stats(timing_stats: List, location_to_save_chart: str):
    logging.info(location_to_save_chart)

    line_chart = LineChart(timing_stats)
    line_chart.construct_lines()
    line_chart.annotate()
    LineChart.write(location_to_save_chart)
