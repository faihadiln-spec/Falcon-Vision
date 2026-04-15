from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import EntityStatus
from app.models.base import PyObjectId, TenantModel
from app.models.regulation_model import StoredFile
from app.utils.datetime import utc_now


class FaceEmbedding(BaseModel):
    model_name: str
    dimension: int
    vector: list[float] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class FaceQuality(BaseModel):
    score: float | None = Field(default=None, ge=0, le=1)
    frontal: bool | None = None
    has_mask: bool | None = None
    lighting: str | None = None


class EmployeeFaceModel(TenantModel):
    employee_id: PyObjectId
    image: StoredFile
    embedding: FaceEmbedding | None = None
    quality: FaceQuality = Field(default_factory=FaceQuality)
    status: EntityStatus = EntityStatus.ACTIVE
