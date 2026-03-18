from collections import defaultdict
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.storage.models.base import Base
from src.storage.repositories.document_repository import DocumentRepository
from src.storage.repositories.version_repository import VersionRepository
from src.storage.services.versioning_service import VersioningService

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".odt"}

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    Session = scoped_session(sessionmaker(bind=engine))
    session = Session()
    yield session
    session.close()
    Session.remove()

@pytest.fixture
def document_repo(db_session):
    return DocumentRepository(db_session)

@pytest.fixture
def version_repo(db_session):
    return VersionRepository(db_session)

@pytest.fixture
def version_service(version_repo):
    return VersioningService(version_repo)

@pytest.fixture(scope="session")
def versioned_folder():
    return Path("resources/versioned_files/fl_152")


@pytest.fixture(scope="session")
def grouped_versions(versioned_folder):
    groups = defaultdict(list)

    for f in versioned_folder.iterdir():
        if f.is_file() and f.suffix in SUPPORTED_EXTENSIONS:
            name = f.stem  # test_1, test_2...
            groups[name].append(f)

    return dict(groups)
