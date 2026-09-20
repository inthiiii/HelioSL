from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    district: str | None = None
    user_type: str = "household"


class UserResponse(BaseModel):
    id: int = Field(ge=1, examples=[1])
    full_name: str
    email: EmailStr
    district: str | None
    user_type: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
