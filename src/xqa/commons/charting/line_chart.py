import logging
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from xqa.commons.charting.chart import Chart


class LineChart(Chart):
    def __init__(self, source_data: List):
        self._source_data = source_data
        logging.info('LineChart data=%s' % self._source_data)

        self._ingest_size = 0
        self._ingest_count = 0
        self._pool_size = 0

    def construct_lines(self):
        number_of_shards = []
        ingest = []
        ingest_balancer = []
        shard = []

        for row in self._source_data:
            logging.debug(row)
            self._pool_size = row[0]
            number_of_shards.append(row[1])
            self._ingest_count = row[2]
            self._ingest_size = row[3]
            ingest.append(row[4])
            ingest_balancer.append(row[5])
            shard.append(row[6])

        plt.plot(number_of_shards, ingest, marker='x', color='red', label='ingest')
        plt.plot(number_of_shards, ingest_balancer, marker='x', color='grey', label='ingest-balancer')
        plt.plot(number_of_shards, shard, marker='x', color='blue', label='shard')
        plt.xticks(np.arange(1, 1 + max(number_of_shards), 1.0))

    def annotate(self):
        plt.grid()
        plt.title('%d bytes / %d items; %d ingest-balancer thread(s)' % (self._ingest_size,
                                                                         self._ingest_count,
                                                                         self._pool_size))

        plt.xlabel('shard(s)')
        plt.ylabel('seconds')
        plt.legend()
