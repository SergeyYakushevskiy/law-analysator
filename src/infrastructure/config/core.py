from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseModel, field_validator

from src.infrastructure.config.paths import BASE_DIR, ASSETS_DIR

class ThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"

CONFIG_FILE_NAME = "app_settings.json"
LOGGER_CONFIG_FILE_NAME = "logger.json"
META_FILE_NAME_DEFAULT = ".lawmeta.json"

class AppSettings(BaseModel):
    # Пути
    base_dir: Path = BASE_DIR
    assets_dir: Path = ASSETS_DIR

    # Приложение
    app_name: str = "Анализатор НПА"
    version: str = "0.1.0 alpha"
    theme: ThemeMode = ThemeMode.LIGHT

    last_project_path: str = ""

    # Логирование
    log_level: str = "DEBUG"
    log_files_limit: int = 5

    # Парсер
    supported_formats: List[str] = [".txt"]
    encodings: List[str] = ["utf-8", "windows-1251", "cp1251", "utf-16"]

    # Алгоритмы Diff
    text_similarity_threshold: float = 0.6
    fallback_threshold: float = 0.2

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {Path: str}
    }

    @field_validator('text_similarity_threshold', 'fallback_threshold')
    @classmethod
    def check_probabilities(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('пороги вероятности должны быть от 0 до 1')
        return v