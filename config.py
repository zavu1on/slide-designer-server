import os
import logging
from pathlib import Path

from datetime import timedelta
from dotenv import load_dotenv

load_dotenv(".env.local")

LOGGING_LEVEL = logging.ERROR

DATABASE_URL = os.getenv("DATABASE_URL")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_COLOR = os.getenv("ADMIN_COLOR")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE = timedelta(days=7)

MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024
ALLOWED_EXTENSIONS = [
    "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp",
    "ttf", "otf", "woff", "woff2",
    "mp4", "avi", "mov", "mkv", "webm"
]

HOST = os.getenv("HOST")
