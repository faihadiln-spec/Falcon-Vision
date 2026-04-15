from pydantic import BaseModel, EmailStr, Field

from app.core.constants import UserRole


class OrganizationRegisterRequest(BaseModel):
    organization_name: str = Field(min_length=2, max_length=120)
    industry: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=80)
    city: str | None = Field(default=None, max_length=80)
    address: str | None = Field(default=None, max_length=200)

    admin_full_name: str = Field(min_length=2, max_length=120)
    admin_email: EmailStr
    admin_password: str = Field(min_length=8, max_length=72)
    admin_phone: str | None = Field(default=None, max_length=30)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthUserResponse(BaseModel):
    id: str
    organization_id: str
    full_name: str
    email: EmailStr
    role: UserRole
    status: str


class AuthOrganizationResponse(BaseModel):
    id: str
    name: str
    status: str


class RegisterOrganizationResponse(BaseModel):
    organization: AuthOrganizationResponse
    user: AuthUserResponse
