from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.slide import Slide
from repositories.slide import get_slide_by_uuid, get_slides_by_user, create_user_slide, delete_user_slide
from schemas.slide import SlideCreate, SlideResponse


async def get_slide(db: AsyncSession, user_id: int, slide_uuid: str) -> SlideResponse | None:
    slide = await get_slide_by_uuid(db, slide_uuid)
    if not slide or slide.user_id != user_id:
        raise HTTPException(status_code=404, detail="Slide not found")
    return SlideResponse.model_validate(slide)


async def get_slides(db: AsyncSession, user_id: int) -> list[SlideResponse]:
    result = await get_slides_by_user(db, user_id)
    return [SlideResponse.model_validate(slide) for slide in result]


async def create_slide(db: AsyncSession, user_id: int, slide_data: SlideCreate) -> SlideResponse | None:
    return SlideResponse.model_validate(await create_user_slide(db, slide_data, user_id))


async def delete_slide(db: AsyncSession, user_id: int, slide_uuid: str) -> bool:
    return await delete_user_slide(db, slide_uuid, user_id)
