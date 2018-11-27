import logging
import sqlite3
from typing import List


def create_stats_db():
    stats_db = sqlite3.connect(':memory:')
    cursor = stats_db.cursor()
    cursor.execute('''
        CREATE TABLE timing_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pool_size INTEGER NOT NULL,
            shards INTEGER NOT NULL,
            ingest_count INTEGER NOT NULL,
            ingest_size INTEGER NOT NULL,
            time_ingest INTEGER NOT NULL,
            time_ingest_balancer INTEGER NOT NULL,
            time_shard INTEGER NOT NULL)
    ''')
    cursor.execute('''
        CREATE TABLE shard_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shards INTEGER NOT NULL,
            storage_size INTEGER NOT NULL)
    ''')
    stats_db.commit()
    return stats_db


def save_timing_stats(stats_db: sqlite3.Connection,
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
    cursor = stats_db.cursor()
    cursor.execute('''INSERT INTO timing_stats(pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard)
        VALUES(?, ?, ?, ?, ?, ?, ?)''',
                   (pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard))
    stats_db.commit()


def retrieve_timing_stats(stats_db: sqlite3.Connection) -> List:
    cursor = stats_db.cursor()
    cursor.execute(
        '''SELECT pool_size, shards, ingest_count, ingest_size, time_ingest, time_ingest_balancer, time_shard FROM timing_stats''')
    return cursor.fetchall()


def save_file_distribution(stats_db: sqlite3.Connection,
                           shards: int,
                           storage_size: int):
    logging.info('shards=%d; storage_size=%d' % (shards, storage_size))
    cursor = stats_db.cursor()
    cursor.execute('''INSERT INTO shard_stats(shards, storage_size) VALUES(?, ?)''',
                   (shards, storage_size))
    stats_db.commit()


def retrieve_file_distribution(stats_db: sqlite3.Connection) -> List:
    cursor = stats_db.cursor()
    cursor.execute(
        '''SELECT shards, storage_size FROM shard_stats''')
    return cursor.fetchall()
