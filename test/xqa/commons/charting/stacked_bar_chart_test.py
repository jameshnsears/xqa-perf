from os import path

import numpy as np

from xqa.commons.charting.stacked_bar_chart import StackedBarChart

one_to_three_shards = [(1, 40),
                       (2, 22),
                       (2, 18),
                       (3, 15),
                       (3, 5),
                       (3, 20)]


def test_transform_source_data_into_a_matrix():
    stacked_bar_chart = StackedBarChart([(1, 40),
                                         (2, 22),
                                         (2, 18)])
    np.testing.assert_array_equal(stacked_bar_chart.transform_source_data_into_a_matrix(),
                                  np.array([[0, 18],
                                            [40, 22],
                                            ]))

    stacked_bar_chart = StackedBarChart(one_to_three_shards)
    np.testing.assert_array_equal(stacked_bar_chart.transform_source_data_into_a_matrix(),
                                  np.array([[0, 0, 20],
                                            [0, 18, 5],
                                            [40, 22, 15]
                                            ]))


def test_stacked_bar_chart(tmpdir):
    stacked_bar_chart = StackedBarChart(one_to_three_shards)
    stacked_bar_chart.construct_bars()
    stacked_bar_chart.annotate()

    atual_image = path.abspath(path.join(tmpdir.strpath, 'expected_stacked_bar_chart.png'))
    stacked_bar_chart.write(atual_image)
    assert open(atual_image, 'rb').read() == open(
        path.abspath(path.join(path.dirname(__file__), '../../../resources/png/expected_stacked_bar_chart.png')),
        'rb').read()
