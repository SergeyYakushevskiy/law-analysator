import json
from pathlib import Path


class DiffCache:

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_cache_path(self, v1, v2):
        a, b = sorted((v1, v2))
        return self.cache_dir / f"{a}_{b}.json"

    def load(self, v1, v2):
        path = self.get_cache_path(v1, v2)
        if not path.exists():
            return None

        with open(path) as f:
            return json.load(f)

    def save(self, v1, v2, diff):
        path = self.get_cache_path(v1, v2)
        with open(path, "w") as f:
            json.dump(diff, f)
