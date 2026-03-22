import json
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any


class MetadataRepository:

    def __init__(self, project_path: Path):
        self.meta_path = project_path / ".lawmeta.json"

        if not self.meta_path.exists():
            self._init_file()

    # ---------- public API ----------

    def get_all(self) -> List[Dict[str, Any]]:
        return self._load()["files"]

    def find_by_path(self, file_path: Path) -> Optional[Dict[str, Any]]:
        file_path = str(file_path)
        for f in self.get_all():
            if f["file_path"] == file_path:
                return f
        return None

    def find_by_hash(self, file_hash: str) -> Optional[Dict[str, Any]]:
        for f in self.get_all():
            if f["file_hash"] == file_hash:
                return f
        return None

    def add_file(self, file_path: Path, file_hash: str):
        data = self._load()

        entry = {
            "file_path": str(file_path),
            "file_hash": file_hash,
            "order_index": None
        }

        data["files"].append(entry)
        self._save(data)

        return entry

    def update_file(self, file_hash: str, **kwargs):
        data = self._load()

        for f in data["files"]:
            if f["file_hash"] == file_hash:
                f.update(kwargs)
                self._save(data)
                return f

        return None

    def delete_file(self, file_hash: str):
        data = self._load()

        data["files"] = [
            f for f in data["files"]
            if f["file_hash"] != file_hash
        ]

        self._save(data)

    def set_order(self, file_hash: str, order_index: int):
        return self.update_file(file_hash, order_index=order_index)

    # ---------- utils ----------

    def calculate_hash(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    # ---------- private ----------

    def _init_file(self):
        data = {"files": []}
        self._save(data)

    def _load(self) -> Dict[str, Any]:
        with open(self.meta_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]):
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
