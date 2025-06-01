from pydantic import BaseModel


class TokenRefresh(BaseModel):
    refresh: str


class TokenAccess(BaseModel):
    access: str


class TokenPair(BaseModel):
    refresh: str
    access: str
