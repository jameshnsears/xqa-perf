import matplotlib.pyplot as plt


class Chart:
    @staticmethod
    def show():
        plt.show()
        plt.close()

    @staticmethod
    def write(location_to_write_chart: str):
        plt.savefig(location_to_write_chart)
        plt.close()
