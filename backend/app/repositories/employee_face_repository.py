from typing import Any

from bson import ObjectId

from app.core.constants import EntityStatus
from app.models.employee_face_model import EmployeeFaceModel
from app.repositories.base_repository import BaseRepository


class EmployeeFaceRepository(BaseRepository):
    collection_name = "employee_faces"

    async def create(self, employee_face: EmployeeFaceModel) -> dict[str, Any]:
        return await self.insert_model(employee_face)

    async def employee_exists(self, organization_id: ObjectId, employee_id: ObjectId) -> bool:
        employee = await self.db["employees"].find_one(
            {
                "_id": employee_id,
                "organization_id": organization_id,
                "is_deleted": {"$ne": True},
            },
            {"_id": 1},
        )
        return employee is not None

    async def get_employee(self, organization_id: ObjectId, employee_id: ObjectId) -> dict[str, Any] | None:
        return await self.db["employees"].find_one(
            {
                "_id": employee_id,
                "organization_id": organization_id,
                "is_deleted": {"$ne": True},
            }
        )

    async def find_by_sha256(
        self,
        organization_id: ObjectId,
        employee_id: ObjectId,
        sha256: str,
    ) -> dict[str, Any] | None:
        return await self.collection.find_one(
            {
                "organization_id": organization_id,
                "employee_id": employee_id,
                "image.sha256": sha256,
                "is_deleted": {"$ne": True},
            }
        )

    async def list_active_faces(self, organization_id: ObjectId) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {
                "organization_id": organization_id,
                "status": EntityStatus.ACTIVE,
                "is_deleted": {"$ne": True},
            }
        )
        return await cursor.to_list(length=None)
