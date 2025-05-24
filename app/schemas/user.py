from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from app.models.user import UserRole
from app.schemas.base import BaseResponseSchema, TimestampSchema


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=8)
    role: UserRole = UserRole.USER


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[constr(min_length=8)] = None
    is_active: Optional[bool] = None


class UserInDB(UserBase, BaseResponseSchema, TimestampSchema):
    is_active: bool
    role: UserRole


class UserResponse(UserInDB):
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: int
    exp: int
    type: str 