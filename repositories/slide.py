import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.slide import Slide
from schemas.slide import SlideCreate


async def get_slide_by_uuid(db: AsyncSession, slide_uuid: str) -> Slide | None:
    result = await db.execute(select(Slide).filter(Slide.uuid == slide_uuid))
    return result.scalar_one_or_none()


async def get_slides_by_user(db: AsyncSession, user_id: int) -> Sequence[Slide]:
    result = await db.execute(select(Slide).filter(Slide.user_id == user_id))
    return result.scalars().all()


async def create_user_slide(db: AsyncSession, slide_data: SlideCreate, user_id: int) -> Slide | None:
    slide = Slide(**slide_data.model_dump(), user_id=user_id, uuid=str(uuid.uuid4()))
    db.add(slide)
    await db.commit()
    await db.refresh(slide)
    return slide


async def delete_user_slide(db: AsyncSession, slide_uuid: str, user_id: int) -> bool:
    slide = await get_slide_by_uuid(db, slide_uuid)
    if not slide or slide.user_id != user_id:
        return False

    await db.delete(slide)
    await db.commit()
    return True
