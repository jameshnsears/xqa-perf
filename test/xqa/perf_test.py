import multiprocessing

from .testing_support.bash_testing_support import run_e2e_test
from .testing_support.chart_testing_support import create_e2e_test_charts
from .testing_support.db_testing_support import *


@pytest.mark.skip(reason="single core, single shard test")
def test_e2e_single_cpu_core(create_stats_db_fixture: sqlite3.Connection):
    run_e2e_test(create_stats_db_fixture)
    create_e2e_test_charts(create_stats_db_fixture)
    truncate_stats_db(create_stats_db_fixture)


def test_e2e_max_cpu_cores(create_stats_db_fixture: sqlite3.Connection):
    max_ingest_balancer_pool_size = multiprocessing.cpu_count()
    max_shards = multiprocessing.cpu_count()

    for pool_size in range(1, max_ingest_balancer_pool_size + 1):
        for shards in range(1, max_shards + 1):
            run_e2e_test(create_stats_db_fixture, pool_size, shards)

        create_e2e_test_charts(create_stats_db_fixture, pool_size, max_shards)

        truncate_stats_db(create_stats_db_fixture)
