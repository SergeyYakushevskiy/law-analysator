import logging

from src.config.config_loader import ensure_directories
from src.config.logger import setup_logging
from src.ui.app import run_ui


def main():
    logger = logging.getLogger(__name__)
    logger.info("запуск приложения")
    run_ui()

    logger.info('приложение успешно запущено')


if __name__ == "__main__":
    ensure_directories()
    setup_logging()
    main()
