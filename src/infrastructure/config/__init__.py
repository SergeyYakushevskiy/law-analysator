from src.infrastructure.config.core import AppSettings, ThemeMode, CONFIG_FILE_NAME, LOGGER_CONFIG_FILE_NAME
from src.infrastructure.config.loader import loader
from src.infrastructure.config.logger import setup_logging
from src.infrastructure.config.paths import STYLE_DIR

settings: AppSettings = loader.load()


__all__ = [
    "settings",
    "loader",
    "setup_logging",
    "AppSettings",
    "ThemeMode",
    "CONFIG_FILE_NAME",
    "LOGGER_CONFIG_FILE_NAME",
    "STYLE_DIR"
]