from os import path

from xqa.perf import make_png_timing_stats, make_png_shard_stats
from .db_testing_support import *


def create_e2e_test_charts(create_stats_db_fixture: sqlite3.Connection,
                           pool_size: int = 1,
                           max_shards: int = 1):
    make_png_timing_stats(retreive_timing_stats(create_stats_db_fixture),
                          path.abspath(path.join(path.dirname(__file__),
                                                 '../../../e2e_results/%s_%s-timing_stats.png' % (
                                                     pool_size,
                                                     max_shards))))

    make_png_shard_stats(retreive_shard_stats(create_stats_db_fixture),
                         path.abspath(path.join(path.dirname(__file__),
                                                '../../../e2e_results/%s_%s-shard_stats.png' % (
                                                    pool_size,
                                                    max_shards))))
