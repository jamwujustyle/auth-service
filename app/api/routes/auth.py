from fastapi import APIRouter, status, HTTPException, Query
from app.services.auth import register_user, login_user, refresh, verify_user_email
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
)
from tortoise.transactions import in_transaction
from tortoise.exceptions import IntegrityError
from app.schemas.verification import (
    TokenRefresh,
    TokenAccess,
    TokenPair,
    EmailVerificationRequest,
)
from ...configs.logging_config import logger
from app.kafka_producer import publish_user_registered_event

router = APIRouter()


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse
)
async def register(user: UserCreate):
    try:
        async with in_transaction():
            user_response = await register_user(user)
            logger.critical(user_response)
            await publish_user_registered_event(user_response.model_dump())
            return user_response

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


@router.get("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email_get(user_id: int = Query(...), token: str = Query(...)):
    """GET endpoint for email verification (clickable links)"""
    try:
        user_data = EmailVerificationRequest(user_id=user_id, token=token)
        async with in_transaction():
            token_pair = await verify_user_email(user_data)
            return {
                "message": "Email verified successfully! You can now login.",
                "access": token_pair.access,
                "refresh": token_pair.refresh,
            }
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )


@router.post("/verify-email", status_code=status.HTTP_200_OK, response_model=TokenPair)
async def verify_email(verification_data: EmailVerificationRequest):
    try:
        async with in_transaction():
            return await verify_user_email(verification_data)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenPair)
async def login(creds: UserLogin):
    try:
        async with in_transaction():
            return await login_user(creds)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))


@router.post(
    "/refresh-token", status_code=status.HTTP_200_OK, response_model=TokenAccess
)
async def refresh_token(payload: TokenRefresh):
    return await refresh(payload)
