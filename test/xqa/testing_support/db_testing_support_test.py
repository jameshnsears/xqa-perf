import sqlite3

from .db_testing_support import save_timing_stats, retreive_timing_stats, save_shard_stats, \
    retreive_shard_stats


def test_save_timing_stats(create_stats_db_fixture: sqlite3.Connection):
    save_timing_stats(create_stats_db_fixture, 3, 1, 40, 80056356, 22, 159, 152)
    save_timing_stats(create_stats_db_fixture, 3, 2, 40, 80056356, 31, 185, 178)
    save_timing_stats(create_stats_db_fixture, 3, 3, 40, 80056356, 28, 178, 171)
    save_timing_stats(create_stats_db_fixture, 3, 4, 40, 80056356, 23, 182, 175)
    assert retreive_timing_stats(create_stats_db_fixture) == [(3, 1, 40, 80056356, 22, 159, 152),
                                                              (3, 2, 40, 80056356, 31, 185, 178),
                                                              (3, 3, 40, 80056356, 28, 178, 171),
                                                              (3, 4, 40, 80056356, 23, 182, 175)]


def test_save_shard_stats(create_stats_db_fixture: sqlite3.Connection):
    save_shard_stats(create_stats_db_fixture, 1, 40)
    save_shard_stats(create_stats_db_fixture, 2, 22)
    save_shard_stats(create_stats_db_fixture, 2, 18)
    save_shard_stats(create_stats_db_fixture, 3, 13)
    save_shard_stats(create_stats_db_fixture, 3, 12)
    save_shard_stats(create_stats_db_fixture, 3, 15)
    assert retreive_shard_stats(create_stats_db_fixture) == [(1, 40),
                                                             (2, 22),
                                                             (2, 18),
                                                             (3, 13),
                                                             (3, 12),
                                                             (3, 15)]