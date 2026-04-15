from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.core.constants import UserRole, UserStatus
from app.models.base import TenantModel


class UserProfile(BaseModel):
    phone: str | None = None
    job_title: str | None = None


class UserPermissionsOverride(BaseModel):
    can_manage_cameras: bool | None = None
    can_manage_regulations: bool | None = None
    can_manage_employee_faces: bool | None = None
    can_acknowledge_alerts: bool | None = None
    can_resolve_alerts: bool | None = None


class UserModel(TenantModel):
    full_name: str
    email: EmailStr
    password_hash: str
    role: UserRole
    status: UserStatus = UserStatus.ACTIVE
    last_login_at: datetime | None = None
    profile: UserProfile = Field(default_factory=UserProfile)
    permissions_override: UserPermissionsOverride = Field(default_factory=UserPermissionsOverride)
