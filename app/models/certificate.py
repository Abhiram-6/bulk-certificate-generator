from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    recipient_id: Mapped[int] = mapped_column(
        ForeignKey("recipients.id"),
        nullable=False,
        unique=True
    )

    certificate_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    recipient = relationship(
        "Recipient",
        back_populates="certificate"
    )