from fastapi import APIRouter, status, HTTPException
from app.services.auth import register_user
from app.schemas.user import UserCreate, UserResponse
from tortoise.transactions import in_transaction
from tortoise.exceptions import IntegrityError

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register(user: UserCreate):
    try:
        async with in_transaction():
            return await register_user(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {ex}",
        )


@router.post("/login")
async def login(): ...
