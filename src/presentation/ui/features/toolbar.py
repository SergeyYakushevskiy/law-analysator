from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal

from src.infrastructure.config.paths import get_asset


class Toolbar(QWidget):
    stats_toggled = pyqtSignal(bool)
    report_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(50)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 10)
        layout.setSpacing(10)

        self.stats_button = QPushButton()
        self.stats_button.setIcon(QIcon(str(get_asset("ico/statistics.svg"))))
        self.stats_button.setFixedSize(40, 40)
        self.stats_button.setCheckable(True)

        self.report_button = QPushButton()
        self.report_button.setIcon(QIcon(str(get_asset("ico/report.svg"))))
        self.report_button.setFixedSize(40, 40)

        layout.addWidget(self.stats_button)
        layout.addWidget(self.report_button)
        layout.addStretch()

        self._connect_signals()

    def _connect_signals(self):
        self.stats_button.toggled.connect(self.stats_toggled.emit)
        self.report_button.clicked.connect(self.report_requested.emit)
