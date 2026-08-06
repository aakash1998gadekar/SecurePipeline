from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# Auth schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


# Vault schemas
class SecretCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    value: str = Field(..., min_length=1, max_length=10000)


class SecretUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    value: Optional[str] = Field(None, min_length=1, max_length=10000)


class SecretResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SecretDetailResponse(SecretResponse):
    value: str
