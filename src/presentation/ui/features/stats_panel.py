from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt

from src.domain.statistics.frequency_aggregator import TYPE_LABELS
from src.infrastructure.parser.structure.token_type import TokenType
from src.presentation.ui.features.histogram_widget import HistogramWidget


class StatsPanel(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # ScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        outer_layout.addWidget(self.scroll_area)

        # Контентный контейнер
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)

        # Layout внутри scroll area
        layout = QVBoxLayout(self.content_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Заголовок
        self.label = QLabel("Статистика")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.label)

        # Выбор узла
        self.choose_type_label = QLabel("Уровень подсчёта")
        self.choose_type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.choose_type_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.choose_type_label)

        self.type_selector = QComboBox()
        self.type_selector.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.type_selector)

        # Описание
        self.content = QLabel()
        self.content.setWordWrap(True)
        self.content.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.content.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.content.hide()
        layout.addWidget(self.content)

        # График
        self.chart = HistogramWidget()
        self.chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chart.hide()
        layout.addWidget(self.chart)
        layout.addStretch()


    def set_types(self, types: list[TokenType]):
        self.type_selector.clear()

        for t in types:
            label = TYPE_LABELS.get(t, str(t))

            self.type_selector.addItem(label, userData=t)

    def get_selected_type(self) -> str:
        return self.type_selector.currentData()

    def set_text_stats(self, text: str):
        self.content.setText(text)
        if not self.content.isVisible():
            self.content.show()

    def set_chart_data(self, data: dict):
        self.chart.plot(data)
        self.chart.show()

