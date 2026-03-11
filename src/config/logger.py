import json
import logging
import logging.config
from datetime import datetime
from pathlib import Path

from src.config.paths import LOG_DIR, LOGGER_CONFIG
from src.settings import LOG_FILES_LIMIT, LOG_LEVEL


def _create_log_file_path() -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return LOG_DIR / f"{date_str}.log"


def _cleanup_old_logs():
    logs = sorted(
        LOG_DIR.glob("*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    for old_log in logs[LOG_FILES_LIMIT:]:
        old_log.unlink()


def setup_logging():
    log_file = _create_log_file_path()
    with open(LOGGER_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["handlers"]["file"]["filename"] = str(log_file)
    config["handlers"]["file"]["level"] = LOG_LEVEL
    config["root"]["level"] = LOG_LEVEL

    logging.config.dictConfig(config)
    _cleanup_old_logs()
