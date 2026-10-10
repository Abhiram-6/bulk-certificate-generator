# Bulk Certificate Generator

A REST API application built with **FastAPI, Python, SQLAlchemy, MySQL, and ReportLab** to generate and manage certificates in bulk. The application accepts event details and recipient information, processes certificate-generation jobs in the background, generates personalized PDF certificates, and provides APIs to track progress and download certificates.

## Features

- Create certificate-generation jobs for multiple recipients.
- Validate recipient names, email addresses, event details, and request data.
- Store jobs, recipients, and certificate records in MySQL.
- Process certificate-generation jobs using FastAPI background tasks.
- Generate personalized landscape A4 PDF certificates.
- Use a classic navy-blue and gold certificate design.
- Display recipient details, event information, certificate ID, appreciation message, and authorized signature section.
- Track job status, progress, successful certificates, and failures.
- Retrieve all certificates generated for a job.
- Download individual certificates through an API.
- Run automated tests using pytest.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| MySQL | Persistent data storage |
| Pydantic | Request validation and response schemas |
| ReportLab | PDF certificate generation |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |

## Project Structure

```text
bulk-certificate-generator/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── job.py
│   │   ├── recipient.py
│   │   └── certificate.py
│   ├── schemas/
│   │   ├── job.py
│   │   ├── recipient.py
│   │   └── certificate.py
│   ├── api/
│   │   ├── jobs.py
│   │   └── certificates.py
│   ├── services/
│   │   └── pdf_service.py
│   └── workers/
│       └── certificate_worker.py
├── tests/
│   ├── test_pdf_service.py
│   └── test_api.py
├── generated/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Prerequisites

Install the following before running the application:

- Python 3.10 or compatible version
- MySQL Server
- pip

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd bulk-certificate-generator
```

If you are already working in the project directory, skip this step.

### 2. Create and activate a virtual environment

On Windows CMD:

```cmd
python -m venv myvenv
myvenv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL and execute:

```sql
CREATE DATABASE certificate_generator;
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/certificate_generator
```

Replace `YOUR_PASSWORD` with your local MySQL password.

**Security:** Never commit `.env` or expose database credentials in the repository.

### 6. Start the application

```cmd
uvicorn app.main:app --reload
```

The application will be available at:

- Base URL: `http://127.0.0.1:8000`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Health and database connectivity check |
| POST | `/api/jobs/` | Create a certificate-generation job |
| GET | `/api/jobs/{job_id}` | Retrieve job status and progress |
| GET | `/api/certificates/job/{job_id}` | List certificates associated with a job |
| GET | `/api/certificates/{certificate_id}/download` | Download an individual PDF certificate |

Use the interactive Swagger documentation at `/docs` to explore and execute these endpoints.

## Example: Create a Certificate Job

Send a POST request to `/api/jobs/` with the following JSON body:

```json
{
  "event_name": "AI Innovation Hackathon",
  "event_date": "2026-10-10",
  "issuer": "VNR VJIET",
  "recipients": [
    {
      "name": "Abhiram",
      "email": "abhiram@example.com"
    },
    {
      "name": "Rahul",
      "email": "rahul@example.com"
    },
    {
      "name": "Priya",
      "email": "priya@example.com"
    }
  ]
}
```

Example response:

```json
{
  "job_id": 11,
  "status": "PENDING",
  "total_count": 3,
  "success_count": 0,
  "failed_count": 0
}
```

The returned job ID can be used to track progress. The actual ID will depend on the database.

## Job Status and Progress

Use:

```text
GET /api/jobs/{job_id}
```

The status response includes:

- `status`: Current job status.
- `total_count`: Total recipients in the job.
- `success_count`: Recipients processed successfully.
- `failed_count`: Recipients whose certificate generation failed.
- `pending_count`: Recipients not yet recorded as successful or failed.
- `progress`: Percentage of recipients processed.
- `created_at`: Job creation timestamp.
- `completed_at`: Job completion timestamp.

Depending on processing results, a job may finish with `COMPLETED`, `COMPLETED_WITH_ERRORS`, or `FAILED`.

## List and Download Certificates

To list certificates for a job:

```text
GET /api/certificates/job/{job_id}
```

The response contains certificate IDs, certificate numbers, recipient names, file paths, and creation timestamps.

To download an individual certificate:

```text
GET /api/certificates/{certificate_id}/download
```

The endpoint returns the generated PDF file.

Generated PDF files are stored in the `generated/` directory.

## Database Models

The application uses three main database models:

- **GenerationJob:** Stores event details, job status, recipient totals, success and failure counts, and timestamps.
- **Recipient:** Stores each recipient's name, email, associated job, processing status, and error information.
- **Certificate:** Stores the certificate number, recipient association, PDF file path, and creation timestamp.

## PDF Certificate Design

Certificates are generated using ReportLab in landscape A4 format.

The design includes:

- Ivory background with navy-blue and gold borders.
- Decorative corner elements and achievement emblem.
- Recipient name and event information.
- A general appreciation message suitable for different types of events.
- Issuer name and certificate ID.
- Authorized signature line.

The recipient, event, date, issuer, and certificate number are supplied dynamically during generation.

## Automated Testing

The project includes pytest tests for PDF generation and API validation.

Run all tests from the project root:

```cmd
python -m pytest -v
```

The current test suite contains six tests covering PDF creation, invalid request data, nonexistent jobs, and bulk job creation.

The existing tests have passed in the development environment. A clean environment should be configured with its own MySQL database before running the API tests.

## Current Implementation Notes

- Background processing uses FastAPI `BackgroundTasks`. It is suitable for this assignment but is not a durable task queue for long-running production workloads.
- Database tables are currently initialized by the application. A migration system such as Alembic can be introduced as the project grows.
- Generated PDFs must remain accessible at their stored file paths for the download endpoint to work.
- Production deployments should add structured logging, stronger retry safeguards, concurrency controls, authentication, and appropriate file-retention policies.

## Future Enhancements

- Add an optional certificate type to support participation, completion, achievement, and winner certificates.
- Add certificate verification through unique IDs or QR codes.
- Introduce a durable task queue such as Celery with Redis.
- Add database migrations and more extensive integration tests.
- Add configurable certificate templates and custom branding.

## Author

Developed as a bulk certificate-generation project using Python, FastAPI, MySQL, SQLAlchemy, and ReportLab.
