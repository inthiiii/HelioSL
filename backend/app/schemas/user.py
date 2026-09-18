from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    district: str | None = None
    user_type: str = "household"


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    district: str | None
    user_type: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )