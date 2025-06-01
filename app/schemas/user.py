from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserCreateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True
