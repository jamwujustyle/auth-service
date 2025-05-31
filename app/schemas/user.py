from pydantic import BaseModel, EmailStr, UUID4


class User(BaseModel):
    id: UUID4
    name: str
    email: EmailStr

    class Config:
        orm_model = True
