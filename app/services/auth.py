from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
    UserLoginResponse,
)
from app.core.security import JWTToken
from datetime import timedelta


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


async def login_user(creds: UserLogin) -> "UserLoginResponse":
    user = await User.get_or_none(email=creds.email)

    if not user:
        raise ValueError("Invalid credentials or user does not exist")

    if not user.check_password(password=creds.password):
        raise ValueError("Invalid credentials")

    access = JWTToken.create_access_token(data={"sub": str(user.id)})
    refresh = JWTToken.create_access_token(
        data={"sub": str(user.id)}, expires_delta=timedelta(days=88)
    )
    return UserLoginResponse(
        access=access,
        refresh=refresh,
    )
