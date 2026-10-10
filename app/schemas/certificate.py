from datetime import datetime

from pydantic import BaseModel


class CertificateResponse(BaseModel):
    certificate_id: int
    certificate_number: str
    recipient_name: str
    file_path: str
    created_at: datetime