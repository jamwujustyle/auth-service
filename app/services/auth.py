from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
)
from app.core.security import JWTToken
from datetime import timedelta
from app.schemas.token import TokenRefresh, TokenPair, TokenAccess


async def register_user(user_data=UserCreate) -> "UserCreateResponse":

    user = User(
        name=user_data.name,
        email=user_data.email,
    )

    user.set_password(user_data.password)

    await user.save()

    return UserCreateResponse(
        id=user.id,
        name=user.name,
        email=user.email,
    )


async def login_user(creds: UserLogin) -> "TokenPair":
    user = await User.get_or_none(email=creds.email)

    if not user:
        raise ValueError("Invalid credentials or user does not exist")

    if not user.check_password(password=creds.password):
        raise ValueError("Invalid credentials")

    access = JWTToken.create_access_token(data={"sub": str(user.id)})
    refresh = JWTToken.create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(days=88)
    )
    return TokenPair(
        access=access,
        refresh=refresh,
    )


async def refresh(refresh_token: TokenRefresh) -> "TokenAccess":
    payload = JWTToken.decode_token(refresh_token.refresh)
    user_id = payload["sub"]
    new_access = JWTToken.create_access_token(data={"sub": str(user_id)})
    return TokenAccess(access=new_access)
