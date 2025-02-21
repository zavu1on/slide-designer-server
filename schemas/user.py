import re
from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    avatar_color: str

    @validator("avatar_color")
    def validate_color(cls, value):
        hex_color_pattern = r"^#(?:[0-9a-fA-F]{3}){1,2}$"  # #RGB или #RRGGBB
        if not re.match(hex_color_pattern, value):
            raise ValueError("Некорректный цвет. Используйте HEX формат (#RRGGBB)")
        return value


class UserLogin(BaseModel):
    email: str
    password: str
