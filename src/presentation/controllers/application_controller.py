import logging
from pathlib import Path
from typing import Optional, Callable

from PyQt6.QtWidgets import QApplication

from src.application.services.diff_service import DiffService
from src.application.services.project_service import ProjectService
from src.application.services.statistics_service import StatisticsService
from src.infrastructure.config import AppSettings
from src.presentation.controllers.analytics_controller import AnalyticsController
from src.presentation.controllers.welcome_cotroller import WelcomeController
from src.presentation.controllers.workspace_controller import WorkspaceController
from src.presentation.theme import ThemeManager
from src.presentation.ui.windows.main_window import MainWindow
from src.presentation.ui.windows.welcome_window import WelcomeWindow

logger = logging.getLogger(__name__)


class ApplicationController:
    def __init__(
            self,
            app: QApplication,
            settings: AppSettings,
            save_settings: Callable,
            theme_manager: ThemeManager,
            project_service: ProjectService,
            last_project_path: Optional[Path]
    ):
        self.app = app
        self.settings = settings
        self.save_settings = save_settings
        self.theme_manager = theme_manager
        self.project_service = project_service
        self.last_project_path = last_project_path

        self.welcome_window: Optional[WelcomeWindow] = None
        self.main_window: Optional[MainWindow] = None
        self.welcome_controller: Optional[WelcomeController] = None
        self.workspace_controller: Optional[WorkspaceController] = None

    def start(self):
        try:
            self.project_service.open_project(self.last_project_path)
            self._open_main_window()
        except Exception as e:
            self._open_welcome_window()

    def _open_welcome_window(self):
        if not self.welcome_window:
            self.welcome_window = WelcomeWindow()
            self.welcome_controller = WelcomeController(
                window=self.welcome_window,
                settings=self.settings,
                apply_settings=self._on_settings_applied,
                on_project_opened=self._on_project_opened
            )
        if self.main_window:
            self.main_window.hide()
        self.welcome_window.show()

    def _open_main_window(self):
        if not self.main_window:
            self.main_window = MainWindow()
            self.statistics_service = StatisticsService()

        self.workspace_controller = WorkspaceController(
            window=self.main_window,
            project_service=self.project_service,
            on_close_requested=self._open_welcome_window
        )

        self.analytics_controller = AnalyticsController(
            window=self.main_window,
            project_service=self.project_service,
            diff_service=DiffService(),
            statistics_service=self.statistics_service
        )

        self.analytics_controller.load_types()
        self.main_window.show()

    def _on_project_opened(self, path: Path):
        self.project_service.open_project(path)

        if self.welcome_window:
            self.welcome_window.hide()

        self._open_main_window()

    def _on_settings_applied(self):
        self.save_settings(self.settings)
