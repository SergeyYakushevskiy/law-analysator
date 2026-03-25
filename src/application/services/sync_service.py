import logging
from pathlib import Path
from typing import Dict, List

from src.infrastructure.storage.metadata_repository import MetadataRepository

logger = logging.getLogger(__name__)


class SyncService:

    def __init__(self, project_path: Path, repository: MetadataRepository):
        self.project_path = project_path
        self.repo = repository

    def scan_files(self) -> List[Path]:
        return [
            f for f in self.project_path.iterdir()
            if f.is_file() and not f.name.startswith(".")
        ]

    logger = logging.getLogger(__name__)

    def sync(self) -> Dict[str, List]:
        logger.debug("Начало синхронизации")

        actual_files = self.scan_files()
        meta_files = self.repo.get_all()

        meta_by_hash = {f["file_hash"]: f for f in meta_files}

        results = {
            "files": [],
            "new_files": [],
            "renamed_files": [],
            "deleted_files": [],
            "unordered_files": []
        }

        seen_hashes = set()

        for path in actual_files:
            file_hash = self.repo.calculate_hash(path)
            seen_hashes.add(file_hash)

            file_name = path.name
            results["files"].append(file_name)

            if file_hash in meta_by_hash:
                entry = meta_by_hash[file_hash]

                if entry["file_path"] != str(path):
                    self.repo.update_file(file_hash, file_path=str(path))

                    results["renamed_files"].append({
                        "old_path": Path(entry["file_path"]).name,
                        "new_path": file_name
                    })

                if entry.get("order_index") is None:
                    results["unordered_files"].append(file_name)

            else:
                self.repo.add_file(path, file_hash)
                results["new_files"].append(file_name)
                results["unordered_files"].append(file_name)

        for entry in meta_files:
            if entry["file_hash"] not in seen_hashes:
                self.repo.delete_file(entry["file_hash"])
                results["deleted_files"].append(Path(entry["file_path"]).name)

        logger.debug(f"синхронизация завершена: {results}")
        return results

    def apply_order(self, ordered_files: List[str]):
        for index, file_name in enumerate(ordered_files):
            file_path = self.project_path / file_name
            file_hash = self.repo.calculate_hash(Path(file_path))
            self.repo.update_file(file_hash, order_index=index)
