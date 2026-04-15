from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import CameraStatus, CameraStreamType, VisionModule
from app.models.base import PyObjectId, TenantModel


class CameraResolution(BaseModel):
    width: int
    height: int


class CameraStream(BaseModel):
    type: CameraStreamType = CameraStreamType.RTSP
    url: str
    masked_url: str | None = None
    fps: int | None = None
    resolution: CameraResolution | None = None


class RoiPoint(BaseModel):
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)


class CameraCalibration(BaseModel):
    roi_polygon: list[RoiPoint] = Field(default_factory=list)


class CameraModel(TenantModel):
    zone_id: PyObjectId
    name: str
    code: str
    stream: CameraStream
    enabled_modules: list[VisionModule] = Field(default_factory=list)
    calibration: CameraCalibration = Field(default_factory=CameraCalibration)
    status: CameraStatus = CameraStatus.ACTIVE
    last_seen_at: datetime | None = None
