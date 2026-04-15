from typing import Any

from bson import ObjectId

from app.models.user_model import UserModel
from app.repositories.base_repository import BaseRepository
from app.utils.datetime import utc_now


class UserRepository(BaseRepository):
    collection_name = "users"

    async def create(self, user: UserModel) -> dict[str, Any]:
        return await self.insert_model(user)

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        return await self.collection.find_one(
            {
                "email": email.lower(),
                "is_deleted": {"$ne": True},
            }
        )

    async def find_by_id(self, user_id: ObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one(
            {
                "_id": user_id,
                "is_deleted": {"$ne": True},
            }
        )

    async def list_by_organization(self, organization_id: ObjectId) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {
                "organization_id": organization_id,
                "is_deleted": {"$ne": True},
            }
        ).sort("created_at", -1)
        return await cursor.to_list(length=None)

    async def update_last_login(self, user_id: ObjectId) -> None:
        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"last_login_at": utc_now(), "updated_at": utc_now()}},
        )

    async def update_user(
        self,
        user_id: ObjectId,
        update_fields: dict[str, Any],
    ) -> dict[str, Any] | None:
        await self.collection.update_one(
            {"_id": user_id, "is_deleted": {"$ne": True}},
            {"$set": {**update_fields, "updated_at": utc_now()}},
        )
        return await self.find_by_id(user_id)
