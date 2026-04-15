from pydantic import BaseModel, Field

from app.core.constants import OrganizationStatus, Severity
from app.models.base import MongoModel, SoftDeleteMixin, TimestampMixin


class RetentionSettings(BaseModel):
    detections: int = 180
    audit_logs: int = 365


class OrganizationSettings(BaseModel):
    timezone: str = "Asia/Riyadh"
    default_alert_severity: Severity = Severity.MEDIUM
    retention_days: RetentionSettings = Field(default_factory=RetentionSettings)


class OrganizationModel(MongoModel, TimestampMixin, SoftDeleteMixin):
    name: str
    industry: str | None = None
    country: str | None = None
    city: str | None = None
    address: str | None = None
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    settings: OrganizationSettings = Field(default_factory=OrganizationSettings)
