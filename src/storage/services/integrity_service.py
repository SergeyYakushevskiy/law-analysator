from pathlib import Path

from src.storage.models.version import Version
from src.storage.repositories.version_repository import VersionRepository
from src.storage.services.versioning_service import VersioningService


class IntegrityService:

    def __init__(
        self,
        version_repository: VersionRepository,
        versioning_service: VersioningService
    ):
        self.version_repository = version_repository
        self.versioning_service = versioning_service

    def verify_versions(self):
        problems = []

        versions = self.version_repository.session.query(Version).all()

        for version in versions:
            path = Path(version.file_path)
            if not path.exists():
                problems.append(("missing_file", version.id))
                continue

            new_hash = self.versioning_service.calculate_hash(path)
            if new_hash != version.file_hash:
                problems.append(("file_modified", version.id))

        return problems
