from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from app.utils.datetime import utc_now


class BaseRepository:
    collection_name: str

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = db[self.collection_name]

    async def insert_model(self, model: BaseModel) -> dict[str, Any]:
        data = model.model_dump(by_alias=True)
        await self.collection.insert_one(data)
        return data

    async def find_by_id(self, entity_id: ObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": entity_id, "is_deleted": {"$ne": True}})

    async def soft_delete(self, entity_id: ObjectId, updated_by: ObjectId | None = None) -> bool:
        update = {"is_deleted": True, "updated_at": utc_now()}
        if updated_by is not None:
            update["updated_by"] = updated_by

        result = await self.collection.update_one({"_id": entity_id}, {"$set": update})
        return result.modified_count == 1
