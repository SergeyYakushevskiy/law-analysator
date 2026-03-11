import logging
from src.config.config_loader import ensure_directories
from src.config.logger import setup_logging
from src.settings import ENV


def main():
    logger = logging.getLogger(__name__)
    logger.info("Application started")
    logger.info("Environment: %s", ENV)


if __name__ == "__main__":
    ensure_directories()
    setup_logging()
    main()
