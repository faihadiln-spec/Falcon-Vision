from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_auth_service, get_current_user
from app.schemas.auth_schema import (
    AuthUserResponse,
    LoginRequest,
    OrganizationRegisterRequest,
    RegisterOrganizationResponse,
    TokenResponse,
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/register-organization", response_model=RegisterOrganizationResponse, status_code=201)
async def register_organization(
    request: OrganizationRegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterOrganizationResponse:
    return await auth_service.register_organization(request)


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    return await auth_service.login(request)


@router.get("/me", response_model=AuthUserResponse)
async def get_me(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> AuthUserResponse:
    return AuthUserResponse(
        id=str(current_user["_id"]),
        organization_id=str(current_user["organization_id"]),
        full_name=current_user["full_name"],
        email=current_user["email"],
        role=current_user["role"],
        status=current_user["status"],
    )
