import os
from pathlib import Path
import sys

def get_base_dir() -> Path:
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS)
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent.parent.parent

def get_user_data_dir() -> Path:
    base = os.getenv("LOCALAPPDATA")
    if base:
        return Path(base) / "LawAnalyzer"
    return Path.home() / ".law_analyzer"

BASE_DIR = get_base_dir()
ASSETS_DIR = BASE_DIR / "assets"
STYLE_DIR = ASSETS_DIR / "style"
ICO_DIR = ASSETS_DIR / "ico"
LOG_DIR = get_user_data_dir() / "logs"
SRC_DIR = BASE_DIR / "src"

def get_asset(name: str) -> Path:
    path = ASSETS_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"ресурс не найден: {path}")
    return path