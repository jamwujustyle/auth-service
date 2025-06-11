from jose import JWTError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import User
from .jwt_config import JWT
import re

load_dotenv()

security = HTTPBearer()


# TODO:
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        payload = JWT.decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="InvalidToken"
            )

        user = await User.get_or_none(id=int(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def validate_password_strength(password: str) -> bool:
    if len(password) < 6:
        return False
    if not re.search(r"[a-z]", password):
        return False
    return True
