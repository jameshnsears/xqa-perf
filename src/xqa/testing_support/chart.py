import logging
import multiprocessing
import sqlite3
from os import path
from typing import List

from xqa.commons.charting.stacked_bar_chart import StackedBarChart
from xqa.perf import make_png_timing_stats, get_ingest_count, get_ingest_size, \
    how_long_service_took_to_process_ingest, get_file_distribution
from .database import retrieve_timing_stats, retrieve_file_distribution
from .database import save_timing_stats, save_file_distribution


def create_graphs(stats_db: sqlite3.Connection,
                  pool_size: int = 1):
    make_png_timing_stats(retrieve_timing_stats(stats_db),
                          path.abspath(path.join(path.dirname(__file__),
                                                 '../../../graphs/%s-%s-timing_stats.png' % (
                                                     multiprocessing.cpu_count(),
                                                     pool_size))))

    make_png_file_distribution(retrieve_file_distribution(stats_db),
                               path.abspath(path.join(path.dirname(__file__),
                                                      '../../../graphs/%s-%s-file_distribution.png' % (
                                                          multiprocessing.cpu_count(),
                                                          pool_size))))


def make_png_file_distribution(shard_stats: List, location_to_save_chart: str):
    logging.info(location_to_save_chart)

    stacked_bar_chart = StackedBarChart(shard_stats)
    stacked_bar_chart.construct_bars()
    stacked_bar_chart.annotate()
    StackedBarChart.write(location_to_save_chart)


def save_values_for_graphs(stats_db, pool_size, shards):
    save_timing_stats(stats_db, pool_size, shards,
                      get_ingest_count(),
                      get_ingest_size(),
                      how_long_service_took_to_process_ingest('ingest'),
                      how_long_service_took_to_process_ingest('ingestbalancer'),
                      how_long_service_took_to_process_ingest('shard'))

    for file_distribution in get_file_distribution():
        save_file_distribution(stats_db, shards, file_distribution[1])
