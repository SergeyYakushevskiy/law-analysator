from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR = BASE_DIR / "assets"
LOG_DIR = BASE_DIR / "logs"
SRC_DIR = BASE_DIR / "src"
STYLE_DIR = ASSETS_DIR / "styles"

LOGGER_CONFIG = ASSETS_DIR / "logger.json"

REPORTS_DIR = "reports"

def get_asset(name):
    if not (ASSETS_DIR / name).exists():
        raise FileNotFoundError(f"ресурс не найден: {ASSETS_DIR}/{name}")
    return ASSETS_DIR / name