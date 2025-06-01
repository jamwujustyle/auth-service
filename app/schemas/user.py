from pydantic import BaseModel, EmailStr, UUID4


class UserCreate(BaseModel):
    id: UUID4
    name: str
    email: EmailStr

    class Config:
        from_attribures = True
