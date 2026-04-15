from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import NotificationChannel, NotificationStatus, NotificationType
from app.models.base import MongoModel, PyObjectId
from app.utils.datetime import utc_now


class RelatedEntity(BaseModel):
    type: str
    id: PyObjectId


class NotificationModel(MongoModel):
    organization_id: PyObjectId
    recipient_user_id: PyObjectId
    type: NotificationType
    channel: NotificationChannel = NotificationChannel.IN_APP
    title: str
    message: str
    related_entity: RelatedEntity | None = None
    status: NotificationStatus = NotificationStatus.PENDING
    read_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    delivered_at: datetime | None = None
