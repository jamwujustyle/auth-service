from fastapi import APIRouter, HTTPException, status
from ...models.user import User

router = APIRouter(prefix="/internal")


@router.get("/verification-token/{user_id}")
async def get_verification_token(user_id: int):
    """Internal endpoint for notification service to get verification tokens"""
    user = await User.get_or_none(id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.verification_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verification token available",
        )
    return {
        "token": user.verification_token,
        "expires": (
            user.verification_token_expires.isoformat()
            if user.verification_token_expires
            else None
        ),
    }
