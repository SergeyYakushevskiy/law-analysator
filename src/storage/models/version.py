from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.models.base import Base


class Version(Base):

    __tablename__ = "versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(String, nullable=False)

    position: Mapped[str] = mapped_column(String, nullable=False, index=True)

    file_hash: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    document = relationship(
        "Document",
        back_populates="versions"
    )
