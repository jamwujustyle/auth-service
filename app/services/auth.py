from ..models.user import User
from ..schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
)
from ..core.jwt_config import JWT
from datetime import timedelta
from ..schemas.verification import (
    TokenRefresh,
    TokenPair,
    TokenAccess,
    EmailVerificationRequest,
)
from ..configs.logging_config import logger
from ..core.security import validate_password_strength


async def register_user(user_data=UserCreate) -> UserCreateResponse:
    if not validate_password_strength(user_data.password):
        raise ValueError("Password must be at least 6 chars")

    user = User(
        name=user_data.name,
        email=user_data.email,
    )

    user.set_password(user_data.password)
    await user.save()
    user.generate_verification_token()  # Generate and set the token
    await user.save()

    return UserCreateResponse(
        message="Registration successful. Please check your email to verify your account.",
        id=user.id,
        name=user.name,
        email=user.email,
    )


async def verify_user_email(user_data=EmailVerificationRequest) -> "TokenPair":
    user = await User.get_or_none(id=user_data.user_id)
    if not user:
        raise ValueError("User not found")

    if user.is_verified:
        raise ValueError("User already verified")

    if not user.verify_token(user_data.token):
        raise ValueError("Invalid or expired token")
    try:
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None
        await user.save()

        access = JWT.create_refresh_token(data={"sub": str(user_data.user_id)})
        refresh = JWT.create_access_token(
            data={"sub": str(user_data.user_id)}, expires_delta=timedelta(days=88)
        )
        return TokenPair(access=access, refresh=refresh)
    except Exception as ex:
        raise ValueError(f"something went wrong: {str(ex)}")


async def login_user(creds: UserLogin) -> "TokenPair":
    user = await User.get_or_none(email=creds.email)

    if not user:
        raise ValueError("Invalid credentials or user does not exist")

    if not user.check_password(password=creds.password):
        raise ValueError("Invalid credentials")

    if not user.is_verified:
        raise ValueError("Please verify your email address before logging in")

    access = JWT.create_refresh_token(data={"sub": str(user.id)})
    refresh = JWT.create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(days=88)
    )
    return TokenPair(
        access=access,
        refresh=refresh,
    )


async def refresh(refresh_token: TokenRefresh) -> "TokenAccess":
    payload = JWT.decode_token(refresh_token.refresh)
    user_id = payload["sub"]
    new_access = JWT.create_refresh_token(data={"sub": str(user_id)})
    return TokenAccess(access=new_access)
