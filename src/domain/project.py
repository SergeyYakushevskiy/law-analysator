import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Project:
    """
    Доменная сущность проекта.

    Хранит только бизнес-данные, не зависит от инфраструктуры.
    Неизменяема после создания (frozen=True).
    Все изменения состояния происходят через сервисы.
    """
    path: Path
    name: str = field(init=False)
    created_at: datetime = field(default_factory=datetime.now)
    meta_file_name: str = ".lawmeta.json"

    def __post_init__(self):
        """Валидация и вычисление производных полей после инициализации."""
        # Приводим путь к абсолютному
        absolute_path = self.path.resolve()
        object.__setattr__(self, 'path', absolute_path)

        # Имя проекта = имя папки
        object.__setattr__(self, 'name', self.path.name)

        # Валидация имени (не пустое)
        if not self.name:
            raise ValueError("Имя проекта не может быть пустым")

    @property
    def meta_path(self) -> Path:
        """Путь к файлу метаданных."""
        return self.path / self.meta_file_name

    @property
    def exists(self) -> bool:
        """Существует ли папка проекта на диске."""
        return self.path.exists()

    @property
    def has_meta_file(self) -> bool:
        """Существует ли файл метаданных."""
        return self.meta_path.exists()

    @property
    def is_valid(self) -> bool:
        """
        Базовая валидация проекта.

        Проект считается валидным, если:
        - Путь абсолютный
        - Имя не пустое
        - Папка существует (для открытого проекта)
        """
        return (
                self.path.is_absolute() and
                bool(self.name) and
                self.exists
        )

    def requires_initialization(self) -> bool:
        """
        Требуется ли инициализация проекта.

        Возвращает True, если:
        - Папка не существует (нужно создать)
        - Файл метаданных не существует (нужно создать через sync)
        """
        return not self.exists or not self.has_meta_file

    def __str__(self) -> str:
        return f"Project(name='{self.name}', path='{self.path}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Project):
            return False
        return self.path == other.path