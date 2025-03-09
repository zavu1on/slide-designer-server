from datetime import datetime

from pydantic import BaseModel, UUID4


class SlideCreate(BaseModel):
    name: str


class SlideUpdate(BaseModel):
    name: str | None = None
    data: str | None = None


class SlideResponse(BaseModel):
    id: int
    uuid: str
    name: str
    data: str | None
    user_id: int
    update_at: datetime

    class Config:
        from_attributes = True


class GetSlideByUUID(BaseModel):
    uuid: UUID4


class UploadMediaFileResponse(BaseModel):
    filename: str
    url: str
