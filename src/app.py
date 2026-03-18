import logging

from src.config.config_loader import ensure_directories
from src.config.logger import setup_logging


def main():
    logger = logging.getLogger(__name__)
    logger.info("запуск приложения")

    logger.info('приложение успешно запущено')


if __name__ == "__main__":
    ensure_directories()
    setup_logging()
    main()
