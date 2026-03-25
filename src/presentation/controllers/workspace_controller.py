import logging
from typing import Callable, Optional

from PyQt6.QtWidgets import QMessageBox

from src.application.services.diff_service import DiffService
from src.application.services.project_service import ProjectService
from src.infrastructure.parser.document import ParsedDocument
from src.presentation.filesystem.watcher import ProjectWatcher
from src.presentation.ui.features.context_builder import DiffContextBuilder
from src.presentation.ui.features.single_renderer import SingleRenderer
from src.presentation.ui.windows.main_window import MainWindow

logger = logging.getLogger(__name__)


class WorkspaceController:
    def __init__(
            self,
            window: MainWindow,
            project_service: ProjectService,
            on_close_requested: Callable
    ):
        self._watcher = None
        self.window = window
        self.project_service = project_service
        self._on_close_requested = on_close_requested

        self._current_old_doc: Optional[ParsedDocument] = None
        self._current_new_doc: Optional[ParsedDocument] = None

        self._connect_signals()

        self._init_workspace()

    def _connect_signals(self):
        self.window.close_requested.connect(self._on_close)
        self.window.compare_requested.connect(self._handle_compare)
        self.window.sort_requested.connect(self._handle_sorting)

    def _init_workspace(self):
        self._watcher = ProjectWatcher(
            root_path=self.project_service.project_path,
            on_change=self._handle_sorting
        )
        try:
            result = self.project_service.sync_project()
            files = result.get("files", [])

            self.window.set_files(files)

            if any([
                result["unordered_files"],
                result["new_files"],
                result["deleted_files"],
                result["renamed_files"]
            ]):
                sorted_files = self.window.show_sorting_dialog(files)

                if sorted_files:
                    self.project_service.finalize_sorting(sorted_files)
                    self.window.set_files(sorted_files)


        except Exception as e:
            logger.error(e)
            QMessageBox.critical(self.window, "Ошибка", f"Ошибка инициализации: {e}")

    def _handle_compare(self, old_path: str, new_path: str):
        try:
            old_doc = self.project_service.load_document(old_path)
            new_doc = self.project_service.load_document(new_path)

            diff_service = DiffService()
            change_set = diff_service.diff(old_doc, new_doc)


            builder = DiffContextBuilder(change_set)
            context = builder.build()

            old_rendered = SingleRenderer(old_doc.root, context, old_doc.path).render()
            new_rendered = SingleRenderer(new_doc.root, context, old_doc.path).render()

            self._current_old_doc = old_doc
            self._current_new_doc = new_doc

            self.window.display_diff(old_rendered, new_rendered)

            logger.info(f"сравнение выполнено: {len(change_set.changes)} изменений")

        except Exception as e:
            logger.exception(e)
            QMessageBox.critical(self.window, "Ошибка", f"Ошибка сравнения: {e}")

    def _handle_sync(self):
        try:
            result = self.project_service.sync_project()

            files = result.get("files", [])
            new_files = result.get("new_files", [])
            renamed_files = result.get("renamed_files", [])

            self.window.set_files(files)

            if new_files or renamed_files:
                QMessageBox.information(
                    self.window,
                    "Синхронизация",
                    f"Обнаружены изменения: {len(new_files) + len(renamed_files)}"
                )
                self._handle_sorting()
            else:
                QMessageBox.information(self.window, "Синхронизация", "Проект актуален")

        except Exception as e:
            QMessageBox.critical(self.window, "Ошибка", f"Ошибка синхронизации: {e}")

    def _handle_sorting(self):
        try:
            result = self.project_service.sync_project()
            files = result.get("files", [])
            if not files:
                return

            sorted_files = self.window.show_sorting_dialog(files)

            if sorted_files:
                self.project_service.finalize_sorting(sorted_files)
                self.window.set_files(sorted_files)

                QMessageBox.information(
                    self.window,
                    "Сортировка",
                    "Порядок файлов успешно обновлён"
                )

        except Exception as e:
            QMessageBox.critical(self.window, "Ошибка", f"Ошибка сортировки: {e}")

    def refresh_files(self):
        try:
            result = self.project_service.sync_project()
            file_names = result.get("files", [])
            self.window.set_files(file_names)
        except Exception as e:
            QMessageBox.critical(self.window, "Ошибка", f"Ошибка обновления: {e}")

    def _on_close(self):
        if self._watcher:
            self._watcher.stop()
            self._watcher = None
        self._on_close_requested()
