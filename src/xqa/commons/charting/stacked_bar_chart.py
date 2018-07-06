import logging
from itertools import groupby
from operator import itemgetter
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from numpy.core.multiarray import ndarray

from xqa.commons.charting.chart import Chart


class StackedBarChart(Chart):
    def __init__(self, source_data: List):
        self._source_data = source_data
        logging.info('StackedBarChart data=%s' % self._source_data)

    def transform_source_data_into_a_matrix(self) -> ndarray:
        matrix = StackedBarChart._create_zeroed_square_matrix(self._matrix_size())
        StackedBarChart._populate_matrix(self._source_data, matrix)
        return StackedBarChart._rotate_matrix_into_correct_shape(matrix)

    def _matrix_size(self) -> int:
        return max(self._source_data)[0]

    def construct_bars(self):
        matrix = self.transform_source_data_into_a_matrix()
        logging.info(matrix)

        for i, c in enumerate(matrix):
            if i == 0:
                plt.bar(np.arange(self._matrix_size()), matrix[0], 0.5)
            else:
                bottom = matrix[0]
                for b in range(1, i):
                    bottom = bottom + matrix[b]

                plt.bar(np.arange(self._matrix_size()), matrix[i], 0.5, bottom=bottom)

    def annotate(self):
        plt.xticks(np.arange(self._matrix_size()), np.arange(1, self._matrix_size() + 1, step=1))

        plt.grid()
        plt.title('item distribution amongst available shard(s)')
        plt.ylabel('items ingested')
        plt.xlabel('shard(s)')

    @staticmethod
    def _create_zeroed_square_matrix(matrix_size: int) -> ndarray:
        return np.zeros((matrix_size, matrix_size), dtype=int)

    @staticmethod
    def _group_bar_chart_data_by_column(bar_chart_data: List) -> List:
        return [(k, [x for _, x in g]) for k, g in groupby(bar_chart_data, itemgetter(0))]

    @staticmethod
    def _populate_matrix(bar_chart_data: List, matrix: ndarray):
        for y in StackedBarChart._group_bar_chart_data_by_column(bar_chart_data):
            for x, v in enumerate(y[1]):
                matrix[y[0] - 1, x] = v

    @staticmethod
    def _rotate_matrix_into_correct_shape(matrix: ndarray) -> ndarray:
        return np.rot90(matrix)
