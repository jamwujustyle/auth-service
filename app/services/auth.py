from app.models.user import User
from uuid import uuid4


async def register_user(id: uuid4, email: str, password: str) -> "User":

    user = User.create(id=uuid4, email=email, password=password)
