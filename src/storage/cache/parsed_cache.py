import pickle
from pathlib import Path


class ParsedCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_path(self, version_id):
        return self.cache_dir / f"{version_id}.pickle"

    def load(self, version_id):
        path = self.get_cache_path(version_id)
        if not path.exists():
            return None
        with open(path, "rb") as f:
            return pickle.load(f)

    def save(self, version_id, parsed_document):
        path = self.get_cache_path(version_id)
        with open(path, "wb") as f:
            pickle.dump(parsed_document, f)
