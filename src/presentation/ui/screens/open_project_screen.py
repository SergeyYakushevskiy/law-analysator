from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy

from src.presentation.ui.components.action_buttons import ActionButton
from src.presentation.ui.components.path_input import PathInput


class OpenProjectScreen(QWidget):
    open_requested = pyqtSignal(str)
    browse_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("open_project_screen")
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(20)

        self.title_label = QLabel("Открыть проект")
        self.title_label.setObjectName("screen_title")
        layout.addWidget(self.title_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.path_input = PathInput()
        layout.addWidget(self.path_input)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.actions = ActionButton()
        self.actions.primary_button.setText("Открыть")

        layout.addWidget(self.actions)

    def _connect_signals(self):
        self.actions.primary_button.clicked.connect(
            lambda: self.open_requested.emit(self.path_input.line_edit.text())
        )

        self.path_input.browse_button.clicked.connect(
            lambda: self.browse_requested.emit()
        )

    def set_path(self, path: str):
        self.path_input.set_path(path)