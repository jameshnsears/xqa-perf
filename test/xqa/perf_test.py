import multiprocessing
import sqlite3

import pytest

from xqa.perf import *


@pytest.fixture
def stats_db_fixture():
    stats_db = sqlite3.connect(':memory:')

    cursor = stats_db.cursor()
    cursor.execute('''
        CREATE TABLE stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pool_size INTEGER NOT NULL,
            shards INTEGER NOT NULL,
            ingest_count INTEGER NOT NULL,
            ingest_size INTEGER NOT NULL,
            time_ingest INTEGER NOT NULL,
            time_ingest_balancer INTEGER NOT NULL,
            time_shard INTEGER NOT NULL)
    ''')
    stats_db.commit()

    yield stats_db
    stats_db.close()


def test_png_produced_as_expected(stats_db_fixture: sqlite3.Connection, tmpdir):
    save_e2e_stats(stats_db_fixture, 3, 1, 40, 80056356, 22, 159, 152)
    save_e2e_stats(stats_db_fixture, 3, 2, 40, 80056356, 31, 185, 178)
    save_e2e_stats(stats_db_fixture, 3, 3, 40, 80056356, 28, 178, 171)
    save_e2e_stats(stats_db_fixture, 3, 4, 40, 80056356, 23, 182, 175)

    atual_image = path.abspath(path.join(tmpdir.strpath, '3_1-2-3-4.png'))
    make_png(retreive_e2e_stats(stats_db_fixture), atual_image)

    assert open(atual_image, 'rb').read() == open(
        path.abspath(path.join(path.dirname(__file__), '../resources/3_1-2-3-4.png')), 'rb').read()


def _test_perf_single_e2e(stats_db_fixture: sqlite3.Connection, tmpdir):
    pool_size = 3
    shards = 1
    run_e2e_test(stats_db_fixture, 4, 1)
    png_filename = path.abspath(path.join(tmpdir.strpath, '%s_%s.png' % (pool_size, shards)))
    make_png(retreive_e2e_stats(stats_db_fixture), png_filename)
    truncate_e2e_stats(stats_db_fixture)


def test_perf_complete_e2e(stats_db_fixture: sqlite3.Connection):
    for pool_size in range(3, 4):
    #for pool_size in range(1, multiprocessing.cpu_count() + 2):
        for shards in range(1, multiprocessing.cpu_count() + 2):
            run_e2e_test(stats_db_fixture, pool_size, shards)

        make_png(retreive_e2e_stats(stats_db_fixture), path.abspath(path.join(path.dirname(__file__),
                                                                              '../../test_results/%s_%s.png' % (
                                                                                  pool_size,
                                                                                  multiprocessing.cpu_count() + 1))))
        truncate_e2e_stats(stats_db_fixture)


def run_e2e_test(stats_db_fixture: sqlite3.Connection, pool_size: int, shards: int):
    invoke_e2e_env(pool_size, shards)
    wait_for_e2e_env_to_process_test_data()

    time_ingest = how_long_service_took_to_process_ingest('ingest')
    time_ingest_balancer = how_long_service_took_to_process_ingest('ingestbalancer')
    time_shard = how_long_service_took_to_process_ingest('shard')

    save_e2e_stats(stats_db_fixture, pool_size, shards,
                   get_ingest_count(),
                   get_ingest_size(),
                   time_ingest,
                   time_ingest_balancer,
                   time_shard)


def save_e2e_stats(stats_db_fixture: sqlite3.Connection,
                   pool_size: int,
                   shards: int,
                   ingest_count: int,
                   ingest_size: int,
                   time_ingest: int,
                   time_ingest_balancer: int,
                   time_shard: int):
    logging.info(
        'pool_size=%d, shards=%d; ingest_count=%d; ingest_size=%d; time_ingest=%d; time_ingest_balancer=%d; time_shard=%d' %
        (pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard))

    cursor = stats_db_fixture.cursor()
    cursor.execute('''INSERT INTO stats(pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard)
        VALUES(?, ?, ?, ?, ?, ?, ?)''',
                   (pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard))
    stats_db_fixture.commit()


def retreive_e2e_stats(stats_db_fixture: sqlite3.Connection) -> List:
    cursor = stats_db_fixture.cursor()
    cursor.execute(
        '''SELECT pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard FROM stats''')
    return cursor.fetchall()


def truncate_e2e_stats(stats_db_fixture: sqlite3.Connection):
    cursor = stats_db_fixture.cursor()
    cursor.execute(
        '''DELETE FROM stats''')
    return cursor.fetchall()
