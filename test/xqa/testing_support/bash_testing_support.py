import sqlite3

from xqa.perf import invoke_e2e_env, wait_for_e2e_env_to_finish, how_long_service_took_to_process_ingest, \
    get_ingest_count, get_ingest_size, get_item_count_to_shard_distribution
from .db_testing_support import save_timing_stats, save_shard_stats


def run_e2e_test(stats_db_fixture: sqlite3.Connection, pool_size: int=1, shards: int=1):
    invoke_e2e_env(pool_size, shards)

    wait_for_e2e_env_to_finish()

    save_timing_stats(stats_db_fixture, pool_size, shards,
                      get_ingest_count(),
                      get_ingest_size(),
                      how_long_service_took_to_process_ingest('ingest'),
                      how_long_service_took_to_process_ingest('ingestbalancer'),
                      how_long_service_took_to_process_ingest('shard'))

    for item_count_to_shard_distribution in get_item_count_to_shard_distribution():
        save_shard_stats(stats_db_fixture, shards, item_count_to_shard_distribution[1])
