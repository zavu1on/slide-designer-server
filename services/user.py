from config import ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_COLOR
from core.logger import logger
from core.security import get_password_hash
from db.base import get_db
from repositories.user import create_user, get_user_by_email
from schemas.user import UserCreate


async def create_superuser():
    async for session in get_db():
        if not await get_user_by_email(session, ADMIN_EMAIL):
            user_data = UserCreate(email=ADMIN_EMAIL, password=ADMIN_PASSWORD, avatar_color=ADMIN_COLOR)
            hashed_password = get_password_hash(user_data.password)

            await create_user(session, user_data, hashed_password)

            logger.info("superuser created")

        break
