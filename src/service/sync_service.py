import logging
from pathlib import Path
from typing import Dict, List

from src.storage.metadata_repository import MetadataRepository

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

    def sync(self) -> Dict[str, List]:
        logger.debug("Начало синхронизации")

        actual_files = self.scan_files()
        meta_files = self.repo.get_all()

        meta_by_hash = {f["file_hash"]: f for f in meta_files}

        results = {
            "new_files": [],
            "renamed_files": [],
            "deleted_files": []
        }

        seen_hashes = set()

        # --- обработка файлов в папке ---
        for path in actual_files:
            file_hash = self.repo.calculate_hash(path)
            seen_hashes.add(file_hash)

            str_path = str(path)

            if file_hash in meta_by_hash:
                entry = meta_by_hash[file_hash]

                if entry["file_path"] != str_path:
                    self.repo.update_file(file_hash, file_path=str_path)

                    results["renamed_files"].append({
                        "old_path": entry["file_path"],
                        "new_path": str_path
                    })
            else:
                self.repo.add_file(path, file_hash)
                results["new_files"].append(str_path)

        # --- удаление отсутствующих файлов ---
        for entry in meta_files:
            if entry["file_hash"] not in seen_hashes:
                logger.debug(f"Удаление файла из метаданных: {entry['file_path']}")

                self.repo.delete_file(entry["file_hash"])
                results["deleted_files"].append(entry["file_path"])

        logger.debug(f"Синхронизация завершена: {results}")
        return results

