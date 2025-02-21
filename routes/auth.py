from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from schemas.auth import TokenPair, RefreshToken
from schemas.user import UserCreate, UserLogin
from services.auth import register_user, authenticate_user, refresh_access_token

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@auth_router.post("/register", response_model=TokenPair)
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    return await register_user(user_data, session)


@auth_router.post("/login", response_model=TokenPair)
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_db)):
    return await authenticate_user(user_data, session)


@auth_router.post("/refresh", response_model=TokenPair)
async def refresh_token(refresh_data: RefreshToken, session: AsyncSession = Depends(get_db)):
    return await refresh_access_token(refresh_data.refresh_token, session)
