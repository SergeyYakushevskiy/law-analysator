import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class HistogramWidget(FigureCanvasQTAgg):
    def __init__(self):
        self.figure = Figure(figsize=(8, 4))  # начальный размер (можно менять)
        super().__init__(self.figure)

    def plot(self, data: dict):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = list(data.keys())
        values = list(data.values())

        x = np.arange(len(labels))
        ax.bar(x, values)

        # строго вертикальные подписи
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=90, ha='center')

        # подгонка фигуры под подписи
        self.figure.tight_layout()

        # обновление виджета
        self.draw()
