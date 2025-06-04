import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status


class JWT:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "50000"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "5000000"))
    ISSUER = os.getenv("JWT_ISSUER", "auth-service")

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=cls.ACESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update(
            {
                "exp": expire,
                "iss": cls.ISSUER,
                "type": "access",
            }
        )
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def create_refresh_token(cls, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            days=cls.REFRESH_TOKEN_EXPIRE_DAYS
        )
        to_encode.update(
            {
                "exp": expire,
                "iss": cls.ISSUER,
                "type": "refresh",
            }
        )
        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode_token(cls, token: str, expected_type: str = "access"):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])

            token_type = payload.get("type")
            if token_type != expected_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected: {expected_type}",
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
