from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
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


class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
    )
    district: str | None = Field(
        default=None,
        max_length=100,
    )
    user_type: str | None = None

    @field_validator("full_name")
    @classmethod
    def validate_full_name(
        cls,
        value: str | None,
    ) -> str:
        if value is None:
            raise ValueError(
                "Full name cannot be null"
            )

        return value

    @field_validator("user_type")
    @classmethod
    def validate_user_type(
        cls,
        value: str | None,
    ) -> str:
        if value is None:
            raise ValueError(
                "User type cannot be null"
            )

        if value not in {
            "household",
            "business",
        }:
            raise ValueError(
                "User type must be household or business"
            )

        return value
