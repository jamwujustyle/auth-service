from fastapi import APIRouter
from app.services.auth import register_user
from app.schemas.user import UserCreate
from tortoise.transactions import in_transaction

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate):
    async with in_transaction():
        return await register_user(user)


@router.post("/login")
async def login(): ...
