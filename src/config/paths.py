from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = BASE_DIR / "assets"
LOG_DIR = BASE_DIR / "logs"
SRC_DIR = BASE_DIR / "src"

LOGGER_CONFIG = ASSETS_DIR / "logger.json"

VERSIONS_NAME = ".versions"
REPORTS_DIR = "reports"