from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.presentation.ui.components.file_selector import FileSelector
from src.presentation.ui.features.diff_view import DiffViewWidget


class DocumentViewer(QWidget):

    on_scroll = pyqtSignal(int)

    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.selector = FileSelector(title)
        layout.addWidget(self.selector)

        self.diff_view = DiffViewWidget()
        layout.addWidget(self.diff_view, stretch=1)



    def set_files(self, files: list[str]):
        self.selector.set_files(files)

    def get_selected(self) -> str:
        return self.selector.get_selected()

    def sync_scroll(self, value: int):
        self.diff_view.sync_scroll(value)