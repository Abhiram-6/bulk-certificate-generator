from datetime import date, datetime

from sqlalchemy import Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    event_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    event_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    issuer: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # rest of the fields...

    issuer: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="PENDING",
        nullable=False
    )

    total_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    success_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    failed_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    recipients = relationship(
        "Recipient",
        back_populates="job",
        cascade="all, delete-orphan"
    )