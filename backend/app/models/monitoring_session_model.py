from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import MonitoringSessionStatus, VisionModule
from app.models.base import PyObjectId, TenantModel


class MonitoringSessionStats(BaseModel):
    detections_count: int = 0
    alerts_count: int = 0


class MonitoringSessionModel(TenantModel):
    name: str
    camera_ids: list[PyObjectId] = Field(default_factory=list)
    zone_ids: list[PyObjectId] = Field(default_factory=list)
    modules: list[VisionModule] = Field(default_factory=list)
    status: MonitoringSessionStatus = MonitoringSessionStatus.SCHEDULED
    started_at: datetime | None = None
    ended_at: datetime | None = None
    started_by: PyObjectId | None = None
    stopped_by: PyObjectId | None = None
    stats: MonitoringSessionStats = Field(default_factory=MonitoringSessionStats)
