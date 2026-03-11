from pathlib import Path

TESTS_DIR = Path(__file__).parent
RESOURCES_DIR = TESTS_DIR / "resources"

def get_resource(path: str) -> Path:
    return RESOURCES_DIR / path