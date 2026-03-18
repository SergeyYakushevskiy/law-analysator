from pathlib import Path
import hashlib

from src.storage.models.version import Version
from src.storage.repositories.version_repository import VersionRepository
from src.storage.services.position_service import LexPositionService

class VersioningService:

    def __init__(self, version_repository: VersionRepository):
        self.version_repository = version_repository
        self.position_service = LexPositionService()

    def calculate_hash(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def add_new_version(self, document_id: int, file_path: Path) -> Version:
        versions = self.version_repository.get_versions(document_id)
        last = versions[-1] if versions else None
        position = self.position_service.new_position_after(last.position if last else None)
        version = Version(
            document_id=document_id,
            file_path=str(file_path),
            position=position,
            file_hash=self.calculate_hash(file_path)
        )
        return self.version_repository.create_version(version)

    def insert_between_versions(self, document_id, prev_version_id, next_version_id, file_path) -> Version:
        prev = self.version_repository.get(prev_version_id)
        next_v = self.version_repository.get(next_version_id)
        position = self.position_service.new_position_between(prev.position, next_v.position)
        version = Version(
            document_id=document_id,
            file_path=str(file_path),
            position=position,
            file_hash=self.calculate_hash(file_path)
        )
        return self.version_repository.create_version(version)

    def move_version(self, version_id, prev_pos, next_pos) -> Version:
        new_position = self.position_service.new_position_between(prev_pos, next_pos)
        return self.version_repository.update_position(version_id, new_position)

    def get_document_pair(self, version_a_id, version_b_id):
        v1 = self.version_repository.get(version_a_id)
        v2 = self.version_repository.get(version_b_id)
        return v1.file_path, v2.file_path
