from datetime import datetime, timezone

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.storage.models.base import Base


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    versions = relationship(
        "Version",
        back_populates="document",
        cascade="all, delete-orphan"
    )
