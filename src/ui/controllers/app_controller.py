from pathlib import Path

from src.storage.database import Database
from src.storage.repositories.document_repository import DocumentRepository
from src.storage.repositories.version_repository import VersionRepository
from src.storage.services.versioning_service import VersioningService
from src.storage.services.folder_sync_service import FolderSyncService
from src.storage.services.integrity_service import IntegrityService


class AppController:

    def __init__(self):
        self.project_path: Path | None = None

        self.db = None
        self.session = None

        self.document_repo = None
        self.version_repo = None

        self.version_service = None
        self.sync_service = None
        self.integrity_service = None

    def open_project(self, path: Path):
        self.project_path = path

        self.db = Database(path)
        self.db.create_schema()
        self.session = self.db.get_session()

        self.document_repo = DocumentRepository(self.session)
        self.version_repo = VersionRepository(self.session)

        self.version_service = VersioningService(self.version_repo)
        self.sync_service = FolderSyncService(
            path,
            self.version_repo,
            self.version_service
        )
        self.integrity_service = IntegrityService(
            self.version_repo,
            self.version_service
        )

    def create_project(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        self.open_project(path)
