from sqlalchemy.orm import Session

from src.storage.models.document import Document

class DocumentRepository:

    def __init__(self, session: Session):
        self.session = session

    def add_document(self, name: str) -> Document:
        document = Document(name=name)
        self.session.add(document)
        self.session.commit()

        return document

    def get(self, document_id: int):
        return self.session.get(Document, document_id)

    def get_all(self):
        return self.session.query(Document).all()
