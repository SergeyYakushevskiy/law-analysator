from sqlalchemy.orm import Session

from src.storage.models.version import Version


class VersionRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_version(self, version: Version):
        self.session.add(version)
        self.session.commit()

        return version

    def get_versions(self, document_id: int):
        return (
            self.session
            .query(Version)
            .filter_by(document_id=document_id)
            .order_by(Version.position)
            .all()
        )

    def get(self, version_id: int):
        return self.session.get(Version, version_id)

    def update_position(self, version_id: int, new_position: str):
        version = self.get(version_id)
        version.position = new_position
        self.session.commit()
        return version

    def delete_version(self, version_id: int):
        version = self.get(version_id)
        self.session.delete(version)
        self.session.commit()
