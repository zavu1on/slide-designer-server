import logging
from datetime import timedelta

LOGGING_LEVEL = logging.ERROR

SECRET_KEY = "028f32092c527ffd4336e638a54242e59904331a028f45cf0f52ef95711bfada"  # todo перенести в env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRE = timedelta(days=7)
