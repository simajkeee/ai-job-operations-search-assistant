from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import EmailStr, BaseModel, Field


class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=128)]


class RegisterUserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime
