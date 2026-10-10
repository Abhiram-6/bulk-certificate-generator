
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.job import GenerationJob
from app.models.recipient import Recipient
from app.models.certificate import Certificate
from app.services.pdf_service import generate_certificate


def process_generation_job(job_id: int):
    db: Session = SessionLocal()

    try:
        # 1. Find the job
        job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        if not job:
            return

        # 2. Mark the job as processing
        job.status = "PROCESSING"
        db.commit()

        # Get recipient IDs so each recipient can be
        # reloaded safely after a transaction rollback.
        recipient_ids = [
            recipient_id
            for (recipient_id,) in (
                db.query(Recipient.id)
                .filter(Recipient.job_id == job_id)
                .order_by(Recipient.id)
                .all()
            )
        ]

        # 3. Process each recipient independently
        for recipient_id in recipient_ids:

            try:
                recipient = (
                    db.query(Recipient)
                    .filter(Recipient.id == recipient_id)
                    .first()
                )

                if not recipient:
                    continue

                # Avoid generating duplicate certificates
                existing_certificate = (
                    db.query(Certificate)
                    .filter(
                        Certificate.recipient_id == recipient.id
                    )
                    .first()
                )

                if existing_certificate:
                    recipient.status = "SUCCESS"
                    recipient.error_message = None
                    db.commit()
                    continue

                # 4. Generate the PDF
                certificate_number = f"CERT-{recipient.id:04d}"

                file_path = generate_certificate(
                    recipient_name=recipient.name,
                    event_name=recipient.job.event_name,
                    event_date=recipient.job.event_date.strftime(
                        "%d %B %Y"
                    ),
                    issuer=recipient.job.issuer,
                    certificate_number=certificate_number
                )

                # 5. Save certificate and recipient status
                certificate = Certificate(
                    recipient_id=recipient.id,
                    certificate_number=certificate_number,
                    file_path=file_path
                )

                db.add(certificate)

                recipient.status = "SUCCESS"
                recipient.error_message = None

                # Commit the certificate and status together
                db.commit()

            except Exception as e:
                # A failed flush/commit requires rollback first
                db.rollback()

                # Reload the recipient in a fresh transaction
                recipient = (
                    db.query(Recipient)
                    .filter(Recipient.id == recipient_id)
                    .first()
                )

                if recipient:
                    recipient.status = "FAILED"
                    recipient.error_message = str(e)[:1000]

                    try:
                        db.commit()
                    except Exception:
                        db.rollback()

                        # Stop if even the failure status
                        # cannot be saved to the database.
                        raise
                else:
                    raise

        # 6. Recalculate counters from saved recipient statuses
        db.rollback()

        job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        if not job:
            return

        recipients = (
            db.query(Recipient)
            .filter(Recipient.job_id == job_id)
            .all()
        )

        job.success_count = sum(
            1 for r in recipients if r.status == "SUCCESS"
        )

        job.failed_count = sum(
            1 for r in recipients if r.status == "FAILED"
        )

        if job.failed_count > 0:
            job.status = "COMPLETED_WITH_ERRORS"
        else:
            job.status = "COMPLETED"

        job.completed_at = datetime.utcnow()
        db.commit()

    except Exception:
        # Handle unexpected job-level errors safely
        db.rollback()

        try:
            job = (
                db.query(GenerationJob)
                .filter(GenerationJob.id == job_id)
                .first()
            )

            if job:
                job.status = "FAILED"
                job.completed_at = datetime.utcnow()
                db.commit()

        except Exception:
            db.rollback()

        finally:
            # The exception is handled here; add logging
            # later if you need detailed diagnostics.

            pass

    finally:
        db.close()
