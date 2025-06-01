from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()


class JWTToken:
    SECRET_KEY = os.environ.get("SECRET_KEY", None)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUES = 314159

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str):
        return jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
