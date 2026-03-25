import logging
from pathlib import Path
from typing import Optional, List

from src.application.factories.project_factory import ProjectFactory
from src.application.ports.metadata_repository_port import MetadataRepositoryPort
from src.application.services.sync_service import SyncService
from src.domain.project import Project
from src.infrastructure.parser.document import ParsedDocument

logger = logging.getLogger(__name__)


class ProjectService:

    def __init__(self, repository_factory: callable):
        self._repository_factory = repository_factory

        self._project: Optional[Project] = None
        self._repo: Optional[MetadataRepositoryPort] = None
        self._sync_service: Optional[SyncService] = None

    def open_project(self, path: Path) -> dict:
        project = ProjectFactory.create(path)
        repo = self._repository_factory(project.path)

        sync_service = SyncService(project.path, repo)
        sync_result = sync_service.sync()

        self._project = project
        self._repo = repo
        self._sync_service = sync_service

        return {
            "project": project,
            "files": sync_result.get("files", []),
            "new_files": sync_result.get("new_files", []),
            "renamed_files": sync_result.get("renamed_files", []),
            "unordered_files": sync_result.get("unordered_files", [])
        }

    def create_project(self, path: Path) -> dict:
        project = ProjectFactory.create(path)

        if not project.exists:
            project.path.mkdir(parents=True, exist_ok=True)
            logger.info(f"папка проекта создана: {project.path}")

        repo = self._repository_factory(project.path)
        sync_service = SyncService(project.path, repo)

        self._project = project
        self._repo = repo
        self._sync_service = sync_service

        logger.info(f"Проект создан: {project.path}")

        return {
            "project": project,
            "files": [],
            "new_files": [],
            "renamed_files": [],
            "unordered_files": []
        }

    def sync_project(self) -> dict:
        self._ensure_initialized()

        result = self._sync_service.sync()

        logger.info("Синхронизация выполнена")

        return result

    def finalize_sorting(self, ordered_files: List[str]):
        self._ensure_initialized()

        self._sync_service.apply_order(ordered_files)

        logger.info("Порядок файлов сохранён")

    def load_document(self, file_name: str) -> ParsedDocument:
        self._ensure_initialized()

        if not hasattr(self._repo, "load_document"):
            raise RuntimeError("Repository не поддерживает загрузку документов")

        file_path = self._project.path / file_name

        return self._repo.load_document(file_path)

    @property
    def project_path(self) -> Path:
        self._ensure_initialized()
        return self._project.path

    @property
    def current_project(self) -> Optional[Project]:
        return self._project

    def _ensure_initialized(self):
        if not self._project or not self._repo or not self._sync_service:
            raise RuntimeError("проект не инициализирован")
