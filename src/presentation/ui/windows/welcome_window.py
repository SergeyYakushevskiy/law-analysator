from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout

from src.presentation.ui.screens.open_project_screen import OpenProjectScreen


class WelcomeWindow(QMainWindow):
    project_open_requested = pyqtSignal(str)
    browse_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.open_screen = OpenProjectScreen()
        layout.addWidget(self.open_screen)

        # Размер окна
        self.resize(1000, 700)

        # Центрирование
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def _connect_signals(self):
        self.open_screen.open_requested.connect(
            lambda path: self.project_open_requested.emit(path)
        )

        if hasattr(self.open_screen, "browse_requested"):
            self.open_screen.browse_requested.connect(self.browse_requested)

    def set_path(self, path: str):
        self.open_screen.set_path(path)
