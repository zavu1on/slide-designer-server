import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOGGING_LEVEL

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.WARNING)

logger = logging.getLogger("slide-designer-server")
logger.setLevel(LOGGING_LEVEL)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.info("Logger initialized successfully")
