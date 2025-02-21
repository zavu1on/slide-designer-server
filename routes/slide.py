from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.security import get_current_user
from db.base import get_db
from schemas.slide import SlideCreate, SlideResponse, GetSlideByUUID
from services import slide

slide_router = APIRouter(prefix="/api/slides", tags=["Slides"])


@slide_router.get("/", response_model=List[SlideResponse])
async def get_slides(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await slide.get_slides(db, current_user.id)


@slide_router.post("/", response_model=SlideResponse)
async def create_slide(
    slide_data: SlideCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    return await slide.create_slide(db, current_user.id, slide_data)


@slide_router.get("/{slide_id}", response_model=SlideResponse)
async def get_slide(
    slide_uuid: GetSlideByUUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    return await slide.get_slide(db, current_user.id, slide_uuid.uuid)


@slide_router.delete("/{slide_id}")
async def delete_slide(
    slide_uuid: GetSlideByUUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    success = await slide.delete_slide(db, current_user.id, slide_uuid.uuid)
    return {"message": "Слайд удален"} if success else {"error": "Ошибка удаления"}
