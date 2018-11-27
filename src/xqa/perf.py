import logging
import time
from typing import List

import psycopg2

from xqa.commons import configuration, sql_queries
from xqa.commons.charting.line_chart import LineChart


class UnableToDetermineFinishState(Exception):
    pass


def wait_for_e2e_ingest_to_complete():
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
    retry_attempts = 5
    connected = False
    while connected is False:
        try:
            connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                                          (configuration.sqlite_name,
                                           configuration.sqlite_user,
                                           configuration.sqlite_host,
                                           configuration.sqlite_password))
            cursor = connection.cursor()
            cursor.execute(sql)
            connected = True

        except psycopg2.OperationalError:
            if retry_attempts == 0:
                raise
            retry_attempts -= 1
    return cursor.fetchall()[0][0]


def get_file_distribution() -> List:
    connection = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" %
                                  (configuration.sqlite_name,
                                   configuration.sqlite_user,
                                   configuration.sqlite_host,
                                   configuration.sqlite_password))
    cursor = connection.cursor()
    cursor.execute(sql_queries.item_count_to_shard_distribution)
    return cursor.fetchall()


def make_png_timing_stats(timing_stats: List, location_to_save_chart: str):
    logging.info(location_to_save_chart)

    line_chart = LineChart(timing_stats)
    line_chart.construct_lines()
    line_chart.annotate()
    LineChart.write(location_to_save_chart)
