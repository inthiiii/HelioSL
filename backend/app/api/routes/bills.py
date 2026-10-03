from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.models.user import User
from app.schemas.bill import BillExtractionResponse
from app.security.dependencies import get_current_user
from app.services.bill_extraction_service import (
    BillExtractionError,
    extract_bill_document,
)


router = APIRouter()

MAX_BILL_SIZE_BYTES = 5 * 1024 * 1024


@router.post(
    "/me/bills/extract",
    response_model=BillExtractionResponse,
)
async def extract_electricity_bill(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> BillExtractionResponse:
    del current_user

    content = await file.read(
        MAX_BILL_SIZE_BYTES + 1
    )

    if len(content) > MAX_BILL_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Electricity bill files must be 5 MB or smaller.",
        )

    try:
        return extract_bill_document(
            content=content,
            filename=file.filename or "electricity-bill",
            content_type=file.content_type,
        )
    except BillExtractionError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
