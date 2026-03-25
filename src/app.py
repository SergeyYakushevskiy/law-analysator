import sys
import logging
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.application.services.project_service import ProjectService
from src.infrastructure.config import setup_logging, settings, STYLE_DIR, loader
from src.infrastructure.storage.metadata_repository import MetadataRepository
from src.presentation.controllers.application_controller import ApplicationController
from src.presentation.theme import ThemeManager


def main():
    setup_logging(settings)
    logger = logging.getLogger(__name__)
    logger.info(f"запуск {settings.app_name} v{settings.version}")

    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)

    theme_manager = ThemeManager(STYLE_DIR)
    theme_manager.switch_theme(app, settings.theme)

    def repo_factory(path: Path) -> MetadataRepository:
        return MetadataRepository(path)

    project_service = ProjectService(repository_factory=repo_factory)

    last_project_path = settings.last_project_path

    if last_project_path:
        last_project_path = Path(last_project_path)

    controller = ApplicationController(
        app=app,
        settings=settings,
        save_settings=loader.save,
        theme_manager=theme_manager,
        project_service=project_service,
        last_project_path=last_project_path
    )

    controller.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
