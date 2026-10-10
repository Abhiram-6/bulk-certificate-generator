
from datetime import date
from unittest.mock import patch

from app.core.database import SessionLocal
from app.models.job import GenerationJob
from app.models.recipient import Recipient
from app.models.certificate import Certificate
from app.workers.certificate_worker import process_generation_job


def test_worker_continues_after_pdf_generation_failure():
    db = SessionLocal()
    job_id = None

    try:
        # Create an isolated test job
        job = GenerationJob(
            event_name="Worker Test Event",
            event_date=date(2026, 10, 10),
            issuer="Test Issuer",
            status="PENDING",
            total_count=3,
            success_count=0,
            failed_count=0,
        )
        db.add(job)
        db.flush()
        job_id = job.id

        recipients = [
            Recipient(
                job_id=job.id,
                name="Test Recipient One",
                email="worker1@example.com",
                status="PENDING",
            ),
            Recipient(
                job_id=job.id,
                name="Test Recipient Two",
                email="worker2@example.com",
                status="PENDING",
            ),
            Recipient(
                job_id=job.id,
                name="Test Recipient Three",
                email="worker3@example.com",
                status="PENDING",
            ),
        ]

        db.add_all(recipients)
        db.commit()

        # Fail PDF generation for the first recipient only.
        original_generator = (
            "app.workers.certificate_worker.generate_certificate"
        )
        call_count = 0

        def generate_with_one_failure(**kwargs):
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                raise RuntimeError("Simulated PDF generation failure")

            from app.services.pdf_service import generate_certificate
            return generate_certificate(**kwargs)

        with patch(
            original_generator,
            side_effect=generate_with_one_failure,
        ):
            process_generation_job(job_id)

        db.expire_all()

        saved_job = (
            db.query(GenerationJob)
            .filter(GenerationJob.id == job_id)
            .first()
        )

        saved_recipients = (
            db.query(Recipient)
            .filter(Recipient.job_id == job_id)
            .order_by(Recipient.id)
            .all()
        )

        assert saved_job.status == "COMPLETED_WITH_ERRORS"
        assert saved_job.total_count == 3
        assert saved_job.success_count == 2
        assert saved_job.failed_count == 1

        assert [r.status for r in saved_recipients] == [
            "FAILED",
            "SUCCESS",
            "SUCCESS",
        ]

        assert db.query(Certificate).filter(
            Certificate.recipient_id.in_(
                [r.id for r in saved_recipients]
            )
        ).count() == 2

    finally:
        # Remove the test job and its related records.
        if job_id is not None:
            db.rollback()
            test_job = (
                db.query(GenerationJob)
                .filter(GenerationJob.id == job_id)
                .first()
            )
            if test_job:
                db.delete(test_job)
                db.commit()

        db.close()
