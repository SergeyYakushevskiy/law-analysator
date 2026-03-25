from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QMenuBar, QStatusBar

from src.presentation.ui.screens.workspace_screen import WorkspaceScreen
from src.presentation.ui.windows.sorting_dialog import SortingDialog


class MainWindow(QMainWindow):
    sort_requested = pyqtSignal()
    report_requested = pyqtSignal()
    close_requested = pyqtSignal()

    compare_requested = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        self.project_menu = self.menu_bar.addMenu("Проект")

        self.sort_action = QAction("Упорядочить", self)
        self.close_action = QAction("Закрыть проект", self)

        self.project_menu.addSeparator()
        self.project_menu.addAction(self.sort_action)
        self.project_menu.addSeparator()
        self.project_menu.addAction(self.close_action)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.workspace = WorkspaceScreen()
        self.setCentralWidget(self.workspace)

        self.showMaximized()

    def _connect_signals(self):
        self.sort_action.triggered.connect(self.sort_requested)
        self.close_action.triggered.connect(self.close_requested)

        self.workspace.compare_requested.connect(self.compare_requested)
        self.workspace.report_requested.connect(self.report_requested)

    def set_files(self, files: list[str]):
        self.workspace.set_files(files)

    def display_diff(self, old_render, new_render):
        self.workspace.display_diff(old_render, new_render)

    def show_message(self, text: str, timeout: int = 3000):
        self.status_bar.showMessage(text, timeout)

    def show_sorting_dialog(self, files: list[str]) -> list[str] | None:
        dialog = SortingDialog(files, self)

        if dialog.exec():
            return dialog.get_sorted_files()

        return None
