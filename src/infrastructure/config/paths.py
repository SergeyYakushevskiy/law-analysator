from pathlib import Path
import sys

def get_base_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent.parent.parent

BASE_DIR = get_base_dir()
ASSETS_DIR = BASE_DIR / "assets"
STYLE_DIR = ASSETS_DIR / "style"
ICO_DIR = ASSETS_DIR / "ico"
LOG_DIR = BASE_DIR / "logs"
SRC_DIR = BASE_DIR / "src"

def get_asset(name: str) -> Path:
    path = ASSETS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"ресурс не найден: {path}")
    return path