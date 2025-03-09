from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict

from core.security import get_current_user
from db.base import get_db
from db.slide import Slide
from schemas.slide import SlideResponse

active_connections: dict[int, list[WebSocket]] = defaultdict(list)


async def websocket_slide(
        websocket: WebSocket,
        slide_id: int,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
):
    await websocket.accept()
    active_connections[slide_id].append(websocket)

    try:
        while True:
            data = await websocket.receive_json()

            slide = await session.get(Slide, slide_id)
            if slide is None or slide.user_id != user.id:
                raise HTTPException(status_code=404, detail="Slide not found")

            slide.name = data.get("name", slide.name)
            slide.data = data.get("data", slide.data)

            await session.commit()
            await session.refresh(slide)

            slide_schema = SlideResponse.model_validate(slide)

            for conn in active_connections[slide_id]:
                await conn.send_json(slide_schema.model_dump())

    except WebSocketDisconnect:
        active_connections[slide_id].remove(websocket)
