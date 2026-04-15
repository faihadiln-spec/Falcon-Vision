from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import DetectionEventType, Severity, VisionModule
from app.models.base import MongoModel, PyObjectId
from app.utils.datetime import utc_now


class DetectionSubject(BaseModel):
    employee_id: PyObjectId | None = None
    tracking_id: str | None = None
    recognized: bool = False


class DetectionViolation(BaseModel):
    rule_id: PyObjectId | None = None
    rule_code: str | None = None
    missing_ppe: list[str] = Field(default_factory=list)


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class DetectionEvidence(BaseModel):
    frame_storage_path: str | None = None
    clip_storage_path: str | None = None
    bbox: BoundingBox | None = None


class DetectionProcessing(BaseModel):
    model_name: str | None = None
    model_version: str | None = None
    latency_ms: int | None = None


class DetectionModel(MongoModel):
    organization_id: PyObjectId
    monitoring_session_id: PyObjectId | None = None
    camera_id: PyObjectId
    zone_id: PyObjectId
    module: VisionModule
    event_type: DetectionEventType
    detected_at: datetime = Field(default_factory=utc_now)
    confidence: float = Field(ge=0, le=1)
    severity: Severity
    subject: DetectionSubject = Field(default_factory=DetectionSubject)
    violation: DetectionViolation = Field(default_factory=DetectionViolation)
    evidence: DetectionEvidence = Field(default_factory=DetectionEvidence)
    processing: DetectionProcessing = Field(default_factory=DetectionProcessing)
    alert_created: bool = False
    alert_id: PyObjectId | None = None
    created_at: datetime = Field(default_factory=utc_now)
