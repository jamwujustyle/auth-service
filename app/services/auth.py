from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserCreateResponse,
    UserLogin,
    UserLoginResponse,
)
from tortoise.exceptions import IntegrityError


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

    return UserLoginResponse(
        access="dummy",
        refresh="dummy",
    )
