import jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE
from core.logger import logger
from repositories.user import get_user_by_email, create_user
from schemas.auth import TokenPair
from schemas.user import UserCreate, UserLogin
from core.security import get_password_hash, verify_password, create_token, decode_token


async def register_user(user_data: UserCreate, session: AsyncSession) -> TokenPair:
    if await get_user_by_email(session, user_data.email):
        raise HTTPException(status_code=400, detail="The email has already been registered")

    hashed_password = get_password_hash(user_data.password)
    user = await create_user(session, user_data, hashed_password)

    if user:
        logger.info(f"{user_data.email} created account")
        return await authenticate_user(
            UserLogin(email=user_data.email, password=user_data.password),
            session
        )
    else:
        logger.error("Can not create user")
        raise HTTPException(status_code=400, detail="Can not create user")


async def authenticate_user(user_data: UserLogin, session: AsyncSession) -> TokenPair:
    user = await get_user_by_email(session, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_token({"sub": user.email, "type": "access_token"}, ACCESS_TOKEN_EXPIRE)
    refresh_token = create_token({"sub": user.email, "type": "refresh_token"}, REFRESH_TOKEN_EXPIRE)

    logger.info(f"{user.email} authenticated")

    return TokenPair(access_token=access_token, refresh_token=refresh_token)


async def refresh_access_token(refresh_token: str, session: AsyncSession):
    try:
        token_data = decode_token(refresh_token)
        email = token_data.get("sub")
        type_ = token_data.get("type")

        if type_ != "refresh_token":
            raise jwt.ExpiredSignatureError

    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = await get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = create_token({"sub": user.email, "type": "access_token"}, ACCESS_TOKEN_EXPIRE)
    refresh_token = create_token({"sub": user.email, "type": "refresh_token"}, REFRESH_TOKEN_EXPIRE)

    logger.info(f"Token pair refreshed, user - {email}")

    return TokenPair(access_token=access_token, refresh_token=refresh_token)
