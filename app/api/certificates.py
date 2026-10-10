from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.certificate import Certificate
from app.models.recipient import Recipient
from app.schemas.certificate import CertificateResponse


router = APIRouter(
    prefix="/api/certificates",
    tags=["Certificates"]
)


@router.get(
    "/job/{job_id}",
    response_model=list[CertificateResponse]
)
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    certificates = (
        db.query(Certificate)
        .join(Recipient)
        .filter(Recipient.job_id == job_id)
        .all()
    )

    return [
        {
            "certificate_id": certificate.id,
            "certificate_number": certificate.certificate_number,
            "recipient_name": certificate.recipient.name,
            "file_path": certificate.file_path,
            "created_at": certificate.created_at
        }
        for certificate in certificates
    ]

@router.get(
    "/{certificate_id}/download"
)
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )

    file_path = Path(certificate.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"{certificate.certificate_number}.pdf"
    )