"""Auth-related Pydantic schemas."""

from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, field_validator


class LoginRequest(BaseModel):
    email: str  # plain str so .local / custom TLDs are accepted
    password: str

    @field_validator("email")
    @classmethod
    def normalise_email(cls, v: str) -> str:
        return v.strip().lower()


class SetupRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


# UserOut must be defined before TokenResponse since TokenResponse references it
class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    password_change_required: bool = False

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    role: Optional[Literal["admin", "user"]] = None
    password: Optional[str] = None


class RegistrationStatusOut(BaseModel):
    allow_registration: bool


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters.")
        return v
