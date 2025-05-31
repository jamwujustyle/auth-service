from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register(): ...


@router.post("/login")
async def login(): ...
