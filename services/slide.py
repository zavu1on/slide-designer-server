from time import time

from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from config import MEDIA_DIR, HOST, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
from core.logger import logger
from repositories.slide import get_slide_by_uuid, get_slides_by_user, create_user_slide, delete_user_slide
from schemas.slide import SlideCreate, SlideResponse, UploadMediaFileResponse


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


def allowed_file(filename: str) -> bool:
    return filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS


async def upload_media_file(file: UploadFile) -> UploadMediaFileResponse:
    filename = file.filename.split(".")
    filename = ".".join([*filename[:-1], str(time()), filename[-1]])
    file_location = MEDIA_DIR / filename


    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file extension")

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="The file is too big (max 2 GB)")

    try:
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        logger.error("error uploading file", exc_info=e)

        raise HTTPException(status_code=500, detail=f"Error saving the file: {e}")

    return UploadMediaFileResponse(filename=file.filename, url=HOST + f"/media/{filename}")