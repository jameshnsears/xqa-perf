from xqa.testing_support.database import save_timing_stats, retrieve_timing_stats, save_file_distribution, \
    retrieve_file_distribution, create_stats_db


def test_save_timing_stats():
    stats_db = create_stats_db()
    save_timing_stats(stats_db, 3, 1, 40, 80056356, 22, 159, 152)
    save_timing_stats(stats_db, 3, 2, 40, 80056356, 31, 185, 178)
    save_timing_stats(stats_db, 3, 3, 40, 80056356, 28, 178, 171)
    save_timing_stats(stats_db, 3, 4, 40, 80056356, 23, 182, 175)
    assert retrieve_timing_stats(stats_db) == [(3, 1, 40, 80056356, 22, 159, 152),
                                               (3, 2, 40, 80056356, 31, 185, 178),
                                               (3, 3, 40, 80056356, 28, 178, 171),
                                               (3, 4, 40, 80056356, 23, 182, 175)]


def test_save_shard_stats():
    stats_db = create_stats_db()
    save_file_distribution(stats_db, 1, 40)
    save_file_distribution(stats_db, 2, 22)
    save_file_distribution(stats_db, 2, 18)
    save_file_distribution(stats_db, 3, 13)
    save_file_distribution(stats_db, 3, 12)
    save_file_distribution(stats_db, 3, 15)
    assert retrieve_file_distribution(stats_db) == [(1, 40),
                                                    (2, 22),
                                                    (2, 18),
                                                    (3, 13),
                                                    (3, 12),
                                                    (3, 15)]
