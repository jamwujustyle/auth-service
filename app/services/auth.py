from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


async def register_user(user_data=UserCreate) -> UserResponse:

    user = User(
        id=user_data.id,
        name=user_data.name,
        email=user_data.email,
    )

    user.set_password(user_data.password)

    await user.save()

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
    )
