# from datetime import date
from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field

from app.schemas.recipient import RecipientCreate


class GenerationJobCreate(BaseModel):
    event_name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    event_date: date

    issuer: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    recipients: List[RecipientCreate] = Field(
        ...,
        min_length=1,
        max_length=5000
    )


class GenerationJobResponse(BaseModel):
    job_id: int
    status: str
    total_count: int
    success_count: int
    failed_count: int

    class Config:
        from_attributes = True


class GenerationJobStatusResponse(BaseModel):
    job_id: int
    event_name: str
    event_date: date
    issuer: str

    status: str

    total_count: int
    success_count: int
    failed_count: int
    pending_count: int

    progress: float

    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True