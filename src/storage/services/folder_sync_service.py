import logging
from pathlib import Path

from src.config import SUPPORTED_FORMATS
from src.storage.repositories.version_repository import VersionRepository
from src.storage.services.versioning_service import VersioningService

logger = logging.getLogger(__name__)

class FolderSyncService:

    def __init__(
        self,
        project_path: Path,
        version_repo: VersionRepository,
        version_service: VersioningService
    ):

        self.project_path = project_path
        self.version_repo = version_repo
        self.version_service = version_service

    def scan_project_files(self):
        logger.debug('сканирование проекта')

        files = []
        for f in self.project_path.iterdir():
            if f.suffix.lower() in SUPPORTED_FORMATS:
                files.append(f)

        logger.debug('сканирование завершено. Найденные файлы:{}', ", ".join(map(str, files)))

        return files

    def detect_changes(self, document_id):
        logger.debug('поиск изменений')

        project_files = self.scan_project_files()
        versions = self.version_repo.get_versions(document_id)
        version_paths = {Path(v.file_path): v for v in versions}

        results = {
            "new_files": [],
            "missing_files": [],
            "modified_files": []
        }

        # новые файлы
        for f in project_files:
            if f not in version_paths:
                results["new_files"].append(f)

        # проверка существующих
        for path, version in version_paths.items():
            if not path.exists():
                results["missing_files"].append(version)
                continue

            new_hash = self.version_service.calculate_hash(path)
            if new_hash != version.file_hash:
                results["modified_files"].append(version)

        logger.debug('поиск изменений успешно завершён. Результаты: {}', results)

        return results
