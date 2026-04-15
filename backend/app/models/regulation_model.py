from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import ExtractionStatus, RegulationStatus
from app.models.base import PyObjectId, TenantModel


class StoredFile(BaseModel):
    original_filename: str
    storage_provider: str = "local"
    storage_path: str
    mime_type: str
    size_bytes: int
    sha256: str


class RegulationExtractionState(BaseModel):
    status: ExtractionStatus = ExtractionStatus.NOT_STARTED
    started_at: datetime | None = None
    completed_at: datetime | None = None
    model_name: str | None = None
    error_message: str | None = None
    rules_count: int = 0


class RegulationModel(TenantModel):
    title: str
    description: str | None = None
    document_type: str = "safety_regulation"
    file: StoredFile
    version: int = Field(default=1, ge=1)
    status: RegulationStatus = RegulationStatus.ACTIVE
    extraction: RegulationExtractionState = Field(default_factory=RegulationExtractionState)
    uploaded_by: PyObjectId
