from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.staticfiles import StaticFiles

from config import MEDIA_DIR
from core.logger import logger
from db.base import init_db, get_db
from routes.auth import auth_router
from routes.slide import slide_router
from services.user import create_superuser
from ws.slide import websocket_slide

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory=str(MEDIA_DIR), html=True), name="media")


app.include_router(auth_router)
app.include_router(slide_router)


@app.on_event("startup")
async def startup():
    logger.info("Starting FastAPI application...")
    await init_db()
    await create_superuser()
    logger.info("FastAPI application started successfully")


@app.websocket("/ws/slide/{slide_id}")
async def websocket_endpoint(websocket: WebSocket, slide_id: int):
    await websocket_slide(websocket, slide_id)
