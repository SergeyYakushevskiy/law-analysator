import logging
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.storage.models.base import Base

logger = logging.getLogger(__name__)

class Database:

    def __init__(self, project_path: Path):
        logger.debug('создание / открытие БД проекта: {}'.format(project_path))
        meta_path = project_path / ".lawmeta"
        meta_path.mkdir(exist_ok=True)

        db_path = meta_path / "project.db"

        logger.debug('создание сессии с БД')
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False,
            future=True
        )

        self.Session = scoped_session(
            sessionmaker(
                bind=self.engine,
                autoflush=False,
                autocommit=False
            )
        )
        logger.debug('БД проекта успешно инициализирована')

    def create_schema(self):
        logger.debug('создание схемы БД')
        Base.metadata.create_all(self.engine)
        logger.debug('схема БД успешно создана')

    def get_session(self):
        return self.Session()
