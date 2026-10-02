from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.models.user import User
from app.schemas.user import (
    UserResponse,
)
from app.security.dependencies import (
    get_current_user,
)


router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def read_user(
    user_id: int,
    current_user: User = Depends(
        get_current_user
    ),
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to another user is forbidden",
        )

    return current_user
