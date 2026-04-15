from typing import Any

from app.models.organization_model import OrganizationModel
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(BaseRepository):
    collection_name = "organizations"

    async def create(self, organization: OrganizationModel) -> dict[str, Any]:
        return await self.insert_model(organization)

    async def find_by_name(self, name: str) -> dict[str, Any] | None:
        return await self.collection.find_one(
            {
                "name": {"$regex": f"^{name}$", "$options": "i"},
                "is_deleted": {"$ne": True},
            }
        )
