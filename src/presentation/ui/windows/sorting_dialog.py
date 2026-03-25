from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton
)

from src.presentation.ui.components.sortable_list import SortableListWidget

class SortingDialog(QDialog):
    sorting_applied = pyqtSignal(list)

    def __init__(self, files: list[str], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Упорядочивание файлов")
        self.resize(400, 500)

        self._init_ui()
        self._connect_signals()

        self.set_files(files)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.label = QLabel("Перетащите файлы в нужном порядке:")
        layout.addWidget(self.label)

        self.list_widget = SortableListWidget()
        layout.addWidget(self.list_widget, stretch=1)

        self.apply_button = QPushButton("Применить")
        layout.addWidget(self.apply_button)

    def _connect_signals(self):
        self.apply_button.clicked.connect(self._apply)

    def set_files(self, files: list[str]):
        self.list_widget.set_items(files)

    def get_sorted_files(self) -> list[str]:
        return self.list_widget.get_items()

    def _apply(self):
        result = self.get_sorted_files()
        self.sorting_applied.emit(result)
        self.accept()
