from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApiResponse(BaseModel):
    message: str


class TimestampResponse(BaseModel):
    created_at: datetime
    updated_at: datetime | None = None


class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
