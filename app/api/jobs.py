from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import GenerationJob
from app.models.recipient import Recipient

from app.schemas.job import (
    GenerationJobCreate,
    GenerationJobResponse,
    GenerationJobStatusResponse
)

from app.workers.certificate_worker import process_generation_job


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)


@router.post(
    "/",
    response_model=GenerationJobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_generation_job(
    job_data: GenerationJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = GenerationJob(
        event_name=job_data.event_name,
        event_date=job_data.event_date,
        issuer=job_data.issuer,
        status="PENDING",
        total_count=len(job_data.recipients),
        success_count=0,
        failed_count=0
    )

    db.add(job)
    db.flush()

    for recipient_data in job_data.recipients:
        recipient = Recipient(
            job_id=job.id,
            name=recipient_data.name,
            email=recipient_data.email,
            status="PENDING"
        )

        db.add(recipient)

    db.commit()
    db.refresh(job)
    
    background_tasks.add_task(
    process_generation_job,
    job.id
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "total_count": job.total_count,
        "success_count": job.success_count,
        "failed_count": job.failed_count
    }

@router.get(
    "/{job_id}",
    response_model=GenerationJobStatusResponse
)
def get_generation_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generation job not found"
        )

    pending_count = (
        job.total_count
        - job.success_count
        - job.failed_count
    )

    if job.total_count > 0:
        progress = (
            (job.success_count + job.failed_count)
            / job.total_count
        ) * 100
    else:
        progress = 0

    return {
        "job_id": job.id,
        "event_name": job.event_name,
        "event_date": job.event_date,
        "issuer": job.issuer,
        "status": job.status,
        "total_count": job.total_count,
        "success_count": job.success_count,
        "failed_count": job.failed_count,
        "pending_count": pending_count,
        "progress": progress,
        "created_at": job.created_at,
        "completed_at": job.completed_at
    }