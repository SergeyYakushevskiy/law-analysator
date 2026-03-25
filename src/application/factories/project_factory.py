import logging
from pathlib import Path

from src.domain.project import Project

logger = logging.getLogger(__name__)


class ProjectFactory:
    """
    Фабрика для создания доменных сущностей Project.

    Отвечает за валидацию пути и создание сущности.
    Не создаёт папки и файлы — это задача сервисов.
    """

    @staticmethod
    def create(path: Path) -> Project:
        """
        Создаёт сущность Project из пути.

        Args:
            path: Путь к папке проекта (может не существовать)

        Returns:
            Project: Доменная сущность

        Raises:
            ValueError: Если путь невалиден
        """
        normalized_path = path.resolve() if path.exists() else Path(path).absolute()

        logger.debug(f"cоздание проекта: {normalized_path}")
        return Project(path=normalized_path)

    @staticmethod
    def create_or_raise(path: Path) -> Project:
        """
        Создаёт Project или выбрасывает исключение при ошибке.

        Удобно для использования в сервисах, где нужна явная обработка ошибок.
        """
        try:
            return ProjectFactory.create(path)
        except ValueError as e:
            logger.error(f"Не удалось создать проект: {e}")
            raise