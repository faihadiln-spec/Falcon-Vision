from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.base import MongoModel, PyObjectId
from app.utils.datetime import utc_now


class AuditEntity(BaseModel):
    type: str
    id: PyObjectId | None = None


class AuditRequestContext(BaseModel):
    ip_address: str | None = None
    user_agent: str | None = None


class AuditChanges(BaseModel):
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None


class AuditLogModel(MongoModel):
    organization_id: PyObjectId | None = None
    actor_user_id: PyObjectId | None = None
    action: str
    entity: AuditEntity | None = None
    request: AuditRequestContext = Field(default_factory=AuditRequestContext)
    changes: AuditChanges = Field(default_factory=AuditChanges)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
