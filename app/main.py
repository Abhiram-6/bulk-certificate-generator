from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import Base, engine
from app.models import GenerationJob, Recipient, Certificate
from app.api.jobs import router as jobs_router
from app.api.certificates import router as certificates_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for generating certificates in bulk",
    version="1.0.0"
)

app.include_router(certificates_router)
app.include_router(jobs_router)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }