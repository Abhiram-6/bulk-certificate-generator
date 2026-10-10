
from pathlib import Path

from app.services.pdf_service import generate_certificate


def test_generate_certificate():
    file_path = generate_certificate(
        recipient_name="Test Recipient",
        event_name="AI Hackathon",
        event_date="10 October 2026",
        issuer="VNR VJIET",
        certificate_number="TEST-CERT-0001",
    )

    pdf_file = Path(file_path)

    # Verify the PDF was created
    assert pdf_file.exists()

    # Verify it is a PDF file
    assert pdf_file.suffix == ".pdf"

    # Verify the file is not empty
    assert pdf_file.stat().st_size > 0
