from pydantic import BaseModel, Field

from app.core.constants import AccessDefault, EntityStatus, Severity, ZoneType
from app.models.base import TenantModel


class Coordinates(BaseModel):
    lat: float | None = None
    lng: float | None = None


class ZoneLocation(BaseModel):
    building: str | None = None
    floor: str | None = None
    coordinates: Coordinates | None = None


class ZoneAccessControl(BaseModel):
    restricted: bool = False
    default_access: AccessDefault = AccessDefault.ALLOW


class ZoneModel(TenantModel):
    name: str
    code: str
    type: ZoneType
    description: str | None = None
    risk_level: Severity = Severity.MEDIUM
    required_ppe: list[str] = Field(default_factory=list)
    access_control: ZoneAccessControl = Field(default_factory=ZoneAccessControl)
    location: ZoneLocation = Field(default_factory=ZoneLocation)
    status: EntityStatus = EntityStatus.ACTIVE
