import logging
from pathlib import Path
from typing import Callable, Optional

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from src.infrastructure.config import AppSettings
from src.presentation.ui.windows.welcome_window import WelcomeWindow

logger = logging.getLogger(__name__)


class WelcomeController:
    def __init__(
            self,
            window: WelcomeWindow,
            settings : AppSettings,
            apply_settings : Callable,
            on_project_opened: Callable[[Path], None]

    ):
        self.window = window
        self.settings = settings
        self._on_project_opened = on_project_opened
        self.apply_settings = apply_settings
        self._connect_signals()

    def _connect_signals(self):
        self.window.project_open_requested.connect(self._handle_project_open)
        self.window.browse_requested.connect(self._handle_browse)

    def _handle_browse(self) -> Optional[str]:
        folder = QFileDialog.getExistingDirectory(
            self.window,
            "Выберите папку проекта",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )

        if folder:
            self.window.set_path(folder)

        return folder if folder else None

    def _handle_project_open(self, path_str: str):
        path = Path(path_str)

        if not path.exists():
            QMessageBox.critical(self.window, "Ошибка", "Папка не найдена")
            return

        try:
            self.settings.last_project_path = str(path)
            self.apply_settings()

            self._on_project_opened(path)

        except Exception as e:
            QMessageBox.critical(self.window, "Ошибка открытия проекта", str(e))