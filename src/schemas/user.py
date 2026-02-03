from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Campos comunes de usuario"""
    id: UUID
    email: str
    username: str
    is_active: bool = True
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

class UserCreateResponse(BaseModel):
    message: str = "Usuario creado exitosamente"
    id: UUID
    email: str
    username: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str = "Login exitoso"
    access_token: str
    token_type: str = "bearer"
    user: UserBase