from datetime import datetime

from app.core.constants import EntityStatus, ZonePermissionType
from app.models.base import PyObjectId, TenantModel


class EmployeeZonePermissionModel(TenantModel):
    employee_id: PyObjectId
    zone_id: PyObjectId
    permission_type: ZonePermissionType
    reason: str | None = None
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    status: EntityStatus = EntityStatus.ACTIVE
