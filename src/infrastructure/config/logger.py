import json
import logging
import logging.config
from datetime import datetime
from pathlib import Path

from src.infrastructure.config.core import AppSettings, LOGGER_CONFIG_FILE_NAME
# Импортируем наши новые компоненты конфига
from src.infrastructure.config.paths import LOG_DIR


def _create_log_file_path() -> Path:
    """Генерирует имя файла лога с текущей датой и временем."""
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return LOG_DIR / f"{date_str}.log"


def _cleanup_old_logs(limit: int):
    """Удаляет старые логи, оставляя только последние N файлов."""
    if not LOG_DIR.exists():
        return

    # Получаем все .log файлы, сортируем по времени создания (новые первыми)
    logs = sorted(
        LOG_DIR.glob("*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    # Удаляем все, что выходит за предел лимита
    for old_log in logs[limit-1:]:
        try:
            old_log.unlink()
        except OSError as e:
            # Если не удалось удалить (например, файл занят), просто логируем ошибку в консоль
            print(f"не удалось удалить старый лог {old_log}: {e}")


def setup_logging(settings: AppSettings):
    logger_config = settings.assets_dir / LOGGER_CONFIG_FILE_NAME
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    _cleanup_old_logs(settings.log_files_limit)
    log_file = _create_log_file_path()

    if not logger_config.exists():
        raise FileNotFoundError(f"конфигурация логгера не найдена: {logger_config}")

    with open(logger_config, "r", encoding="utf-8") as f:
        config = json.load(f)

    if "file" in config.get("handlers", {}):
        config["handlers"]["file"]["filename"] = str(log_file)
        config["handlers"]["file"]["level"] = settings.log_level

    config["root"]["level"] = settings.log_level

    logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)
    logger.debug(f"уровень логирования: {settings.log_level}")
    logger.debug(f"лимит файлов логов: {settings.log_files_limit}")