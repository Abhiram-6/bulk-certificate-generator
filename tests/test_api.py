
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job_rejects_missing_fields():
    response = client.post(
        "/api/jobs/",
        json={}
    )

    assert response.status_code == 422


def test_create_job_rejects_invalid_email():
    payload = {
        "event_name": "AI Hackathon",
        "event_date": "2026-10-10",
        "issuer": "VNR VJIET",
        "recipients": [
            {
                "name": "Test Recipient",
                "email": "invalid-email"
            }
        ]
    }

    response = client.post(
        "/api/jobs/",
        json=payload
    )

    assert response.status_code == 422


def test_nonexistent_job_returns_404():
    response = client.get(
        "/api/jobs/999999999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Generation job not found"
    )

def test_create_job_with_multiple_recipients():
    payload = {
        "event_name": "AI Innovation Hackathon",
        "event_date": "2026-10-10",
        "issuer": "VNR VJIET",
        "recipients": [
            {
                "name": "Test Recipient One",
                "email": "recipient1@example.com"
            },
            {
                "name": "Test Recipient Two",
                "email": "recipient2@example.com"
            },
            {
                "name": "Test Recipient Three",
                "email": "recipient3@example.com"
            }
        ]
    }

    response = client.post("/api/jobs/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["total_count"] == 3
    assert data["success_count"] == 0
    assert data["failed_count"] == 0
    assert data["status"] == "PENDING"


def test_job_status_endpoint_returns_404_for_missing_job():
    response = client.get("/api/jobs/999999999")

    assert response.status_code == 404

def test_get_job_status_for_existing_job():
    # Use a job ID that does not exist.
    # This verifies that missing jobs are handled correctly.
    response = client.get("/api/jobs/999999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Generation job not found"


def test_list_certificates_for_job():
    # A job ID with no associated certificates should return
    # an empty list rather than an error.
    response = client.get("/api/certificates/job/999999999")

    assert response.status_code == 200
    assert response.json() == []


def test_download_nonexistent_certificate():
    response = client.get(
        "/api/certificates/999999999/download"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Certificate not found"
