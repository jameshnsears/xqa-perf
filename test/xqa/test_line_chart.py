from os import path

from xqa.commons.charting.line_chart import LineChart


def test_line_chart(tmpdir):
    four_e2e_timings = [(3, 1, 40, 80056356, 22, 159, 152),
                        (3, 2, 40, 80056356, 31, 185, 178),
                        (3, 3, 40, 80056356, 28, 178, 171),
                        (3, 4, 40, 80056356, 23, 182, 175)]

    line_chart = LineChart(four_e2e_timings)
    line_chart.construct_lines()
    line_chart.annotate()

    atual_image = path.abspath(path.join(tmpdir.strpath, 'expected_line_chart.png'))
    line_chart.write(atual_image)
    assert open(atual_image, 'rb').read() == open(
        path.abspath(path.join(path.dirname(__file__), '../resources/png/expected_line_chart.png')),
        'rb').read()
