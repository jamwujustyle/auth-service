from fastapi import APIRouter, status, HTTPException
from app.services.auth import register_user, login_user, refresh
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
)
from tortoise.transactions import in_transaction
from tortoise.exceptions import IntegrityError
from app.schemas.verification import TokenRefresh, TokenAccess, TokenPair
from kafka_producer import publish_user_registered_event

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse
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


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenPair)
async def login(creds: UserLogin):
    try:
        async with in_transaction():
            return await login_user(creds)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))


@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenAccess)
async def refresh_token(payload: TokenRefresh):
    return await refresh(payload)
