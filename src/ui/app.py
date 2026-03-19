import sys

from PyQt6.QtWidgets import QApplication

from src.ui.startup_dialog import StartupDialog
from src.ui.main_window import MainWindow
from src.ui.controllers.app_controller import AppController


def run_ui():
    app = QApplication(sys.argv)

    controller = AppController()

    dialog = StartupDialog(controller)
    if dialog.exec():
        main_window = MainWindow(controller)
        main_window.show()
        sys.exit(app.exec())
