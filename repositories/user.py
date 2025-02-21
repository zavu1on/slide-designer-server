from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.logger import logger
from db.user import User
from schemas.user import UserCreate


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(session: AsyncSession, user_data: UserCreate, hashed_password: str) -> User | None:
    new_user = User(email=user_data.email, hashed_password=hashed_password, avatar_color=user_data.avatar_color)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    logger.info(f"DB: user {user_data.email} created")

    return new_user
