from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.core.constants import UserRole, UserStatus, normalize_user_role
from app.core.exceptions import ConflictError, NotFoundError, PermissionDeniedError
from app.core.security import hash_password
from app.models.user_model import UserModel, UserProfile
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreateRequest,
    UserListResponse,
    UserResponse,
    UserStatusUpdateRequest,
    UserUpdateRequest,
)
from app.utils.object_id import validate_object_id


ADMIN_USER_ROLES = {
    UserRole.ADMIN,
}


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(
        self,
        request: UserCreateRequest,
        current_user: dict,
    ) -> UserResponse:
        self._ensure_admin(current_user)

        existing_user = await self.user_repository.find_by_email(str(request.email))
        if existing_user is not None:
            raise ConflictError("Email already exists")

        user = UserModel(
            organization_id=current_user["organization_id"],
            full_name=request.full_name,
            email=str(request.email).lower(),
            password_hash=hash_password(request.password),
            role=request.role,
            profile=UserProfile(phone=request.phone, job_title=request.job_title),
            created_by=current_user["_id"],
            updated_by=current_user["_id"],
        )

        try:
            user_doc = await self.user_repository.create(user)
        except DuplicateKeyError as exc:
            raise ConflictError("Email already exists") from exc

        return self._response(user_doc)

    async def list_users(self, current_user: dict) -> UserListResponse:
        self._ensure_admin(current_user)
        user_docs = await self.user_repository.list_by_organization(current_user["organization_id"])
        items = [self._response(user_doc) for user_doc in user_docs]
        return UserListResponse(items=items, total=len(items))

    async def get_user(self, user_id: str, current_user: dict) -> UserResponse:
        self._ensure_admin(current_user)
        user_doc = await self._get_org_user_or_raise(user_id, current_user["organization_id"])
        return self._response(user_doc)

    async def update_user(
        self,
        user_id: str,
        request: UserUpdateRequest,
        current_user: dict,
    ) -> UserResponse:
        self._ensure_admin(current_user)

        user_doc = await self._get_org_user_or_raise(user_id, current_user["organization_id"])
        update_fields: dict[str, object] = {}

        if request.email is not None:
            new_email = str(request.email).lower()
            existing_user = await self.user_repository.find_by_email(new_email)
            if existing_user is not None and existing_user["_id"] != user_doc["_id"]:
                raise ConflictError("Email already exists")
            update_fields["email"] = new_email

        if request.full_name is not None:
            update_fields["full_name"] = request.full_name

        if request.role is not None:
            update_fields["role"] = request.role

        if request.password is not None:
            update_fields["password_hash"] = hash_password(request.password)

        profile = dict(user_doc.get("profile") or {})
        if request.phone is not None:
            profile["phone"] = request.phone
        if request.job_title is not None:
            profile["job_title"] = request.job_title
        if request.phone is not None or request.job_title is not None:
            update_fields["profile"] = profile

        if not update_fields:
            return self._response(user_doc)

        update_fields["updated_by"] = current_user["_id"]

        try:
            updated_user_doc = await self.user_repository.update_user(user_doc["_id"], update_fields)
        except DuplicateKeyError as exc:
            raise ConflictError("Email already exists") from exc

        if updated_user_doc is None:
            raise NotFoundError("User not found")

        return self._response(updated_user_doc)

    async def update_user_status(
        self,
        user_id: str,
        request: UserStatusUpdateRequest,
        current_user: dict,
    ) -> UserResponse:
        self._ensure_admin(current_user)
        user_doc = await self._get_org_user_or_raise(user_id, current_user["organization_id"])

        updated_user_doc = await self.user_repository.update_user(
            user_doc["_id"],
            {
                "status": request.status,
                "updated_by": current_user["_id"],
            },
        )
        if updated_user_doc is None:
            raise NotFoundError("User not found")

        return self._response(updated_user_doc)

    async def delete_user(self, user_id: str, current_user: dict) -> None:
        self._ensure_admin(current_user)
        user_doc = await self._get_org_user_or_raise(user_id, current_user["organization_id"])

        if user_doc["_id"] == current_user["_id"]:
            raise PermissionDeniedError("You cannot delete your own account")

        deleted = await self.user_repository.soft_delete(user_doc["_id"], updated_by=current_user["_id"])
        if not deleted:
            raise NotFoundError("User not found")

    async def _get_org_user_or_raise(
        self,
        user_id: str,
        organization_id: ObjectId,
    ) -> dict:
        user_object_id = validate_object_id(user_id)
        user_doc = await self.user_repository.find_by_id(user_object_id)

        if user_doc is None or user_doc["organization_id"] != organization_id:
            raise NotFoundError("User not found")

        return user_doc

    def _ensure_admin(self, current_user: dict) -> None:
        if normalize_user_role(current_user["role"]) not in ADMIN_USER_ROLES:
            raise PermissionDeniedError("Only admins can manage users")

    def _response(self, user_doc: dict) -> UserResponse:
        profile = user_doc.get("profile") or {}
        return UserResponse(
            id=str(user_doc["_id"]),
            organization_id=str(user_doc["organization_id"]),
            full_name=user_doc["full_name"],
            email=user_doc["email"],
            role=normalize_user_role(user_doc["role"]),
            status=user_doc["status"],
            phone=profile.get("phone"),
            job_title=profile.get("job_title"),
            created_at=user_doc["created_at"],
            updated_at=user_doc["updated_at"],
        )
