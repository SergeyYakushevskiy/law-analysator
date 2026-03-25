import json
import os
from typing import Optional

from src.infrastructure.config.core import AppSettings, CONFIG_FILE_NAME
from src.infrastructure.config.paths import BASE_DIR

class ConfigLoader:
    config_path = BASE_DIR / CONFIG_FILE_NAME

    def __init__(self):
        self._settings: Optional[AppSettings] = None

    def load(self) -> AppSettings:
        data = {}

        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    file_data = json.load(f)
                    data.update(file_data)
            except Exception as e:
                print(f"Ошибка чтения конфига {self.config_path}: {e}. Используются настройки по умолчанию.")

        # Приоритет переменных окружения (опционально)
        if env_level := os.getenv("LOG_LEVEL"):
            data["log_level"] = env_level
        if env_theme := os.getenv("APP_THEME"):
            data["theme"] = env_theme.lower()

        self._settings = AppSettings(**data)
        return self._settings

    def save(self, settings: AppSettings):

        data = settings.model_dump(exclude={'base_dir', 'assets_dir'})

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


loader = ConfigLoader()