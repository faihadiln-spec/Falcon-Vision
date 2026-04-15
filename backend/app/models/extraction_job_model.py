from datetime import datetime

from pydantic import Field

from app.core.constants import ExtractionStatus
from app.models.base import PyObjectId, TenantModel


class ExtractionJobModel(TenantModel):
    regulation_id: PyObjectId
    status: ExtractionStatus = ExtractionStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    queued_at: datetime | None = None
    model_name: str | None = None
    extracted_rule_ids: list[PyObjectId] = Field(default_factory=list)
