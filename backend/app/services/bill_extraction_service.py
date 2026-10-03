import re
from datetime import date
from decimal import Decimal, InvalidOperation
from io import BytesIO

from pypdf import PdfReader

from app.schemas.bill import BillExtractionResponse


MAX_BILL_PAGES = 5


class BillExtractionError(ValueError):
    """Raised when an uploaded bill cannot be read safely."""


def _clean_number(value: str) -> Decimal | None:
    try:
        return Decimal(
            value.replace(",", "").strip()
        )
    except InvalidOperation:
        return None


def _first_match(
    text: str,
    patterns: tuple[str, ...],
) -> str | None:
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
        if match:
            return match.group(1).strip()

    return None


def _parse_month(text: str) -> date | None:
    iso_value = _first_match(
        text,
        (
            r"billing\s*month\s*[:\-]\s*(\d{4}[-/]\d{1,2})",
            r"billing\s*period\s*[:\-]\s*(\d{4}[-/]\d{1,2})",
        ),
    )

    if iso_value:
        year, month = re.split(
            r"[-/]",
            iso_value,
        )
        try:
            return date(int(year), int(month), 1)
        except ValueError:
            return None

    named_match = re.search(
        r"billing\s*month\s*[:\-]\s*"
        r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|"
        r"may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{4})",
        text,
        flags=re.IGNORECASE,
    )

    if named_match:
        month_names = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }
        return date(
            int(named_match.group(2)),
            month_names[named_match.group(1)[:3].lower()],
            1,
        )

    period_start = _first_match(
        text,
        (
            r"billing\s*period\s*[:\-]\s*"
            r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})",
        ),
    )

    if period_start:
        day, month, year = re.split(
            r"[-/]",
            period_start,
        )
        try:
            return date(
                int(year),
                int(month),
                1,
            )
        except ValueError:
            return None

    return None


def extract_text_from_bill(
    content: bytes,
    content_type: str | None,
) -> str:
    is_pdf = (
        content.startswith(b"%PDF")
        or content_type == "application/pdf"
    )

    if is_pdf:
        try:
            reader = PdfReader(BytesIO(content))
        except Exception as exc:
            raise BillExtractionError(
                "The uploaded PDF could not be opened."
            ) from exc

        if reader.is_encrypted:
            raise BillExtractionError(
                "Password-protected bills are not supported."
            )

        if len(reader.pages) > MAX_BILL_PAGES:
            raise BillExtractionError(
                f"Electricity bills may contain at most {MAX_BILL_PAGES} pages."
            )

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )
    elif content_type in {
        "text/plain",
        "text/csv",
    }:
        text = content.decode(
            "utf-8",
            errors="replace",
        )
    else:
        raise BillExtractionError(
            "Upload a text-based PDF or plain-text electricity bill."
        )

    if not text.strip():
        raise BillExtractionError(
            "No readable text was found. Scanned-image OCR is not yet supported."
        )

    return text


def extract_bill_data(
    text: str,
    filename: str,
) -> BillExtractionResponse:
    normalized = " ".join(text.split())

    table_header_match = re.search(
        r"account\s*(?:number|no\.?)\s+customer\s*type\s+"
        r"billing\s*month\s+([A-Z0-9\-/]+)\s+"
        r"(?:household|business|commercial|domestic)\s+"
        r"(\d{4}[-/]\d{1,2})",
        normalized,
        flags=re.IGNORECASE,
    )

    provider = None
    if re.search(
        r"\b(?:ceylon electricity board|ceb)\b",
        normalized,
        flags=re.IGNORECASE,
    ):
        provider = "CEB"
    elif re.search(
        r"\b(?:lanka electricity company|leco)\b",
        normalized,
        flags=re.IGNORECASE,
    ):
        provider = "LECO"

    account_number = _first_match(
        normalized,
        (
            r"account\s*(?:number|no\.?|#)\s*[:\-]\s*([A-Z0-9\-/]+)",
            r"contract\s*account\s*[:\-]\s*([A-Z0-9\-/]+)",
        ),
    )

    if account_number is None and table_header_match:
        account_number = table_header_match.group(1)

    consumption_value = _first_match(
        normalized,
        (
            r"(?:total\s*)?(?:units?\s*consumed|consumption|usage)"
            r"\s*[:\-]?\s*([\d,]+(?:\.\d+)?)\s*(?:kwh|units?)",
            r"([\d,]+(?:\.\d+)?)\s*kwh\s*(?:consumed|used)",
        ),
    )
    amount_value = _first_match(
        normalized,
        (
            r"(?:amount\s*due|total\s*amount|current\s*bill|bill\s*amount)"
            r"\s*[:\-]?\s*(?:lkr|rs\.?|රු\.?)?\s*([\d,]+(?:\.\d+)?)",
            r"(?:lkr|rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:amount\s*due)?",
        ),
    )
    previous_value = _first_match(
        normalized,
        (
            r"previous\s*(?:meter\s*)?reading\s*[:\-]?\s*([\d,]+(?:\.\d+)?)",
        ),
    )
    current_value = _first_match(
        normalized,
        (
            r"current\s*(?:meter\s*)?reading\s*[:\-]?\s*([\d,]+(?:\.\d+)?)",
        ),
    )

    consumption = (
        _clean_number(consumption_value)
        if consumption_value
        else None
    )
    amount = (
        _clean_number(amount_value)
        if amount_value
        else None
    )
    previous = (
        _clean_number(previous_value)
        if previous_value
        else None
    )
    current = (
        _clean_number(current_value)
        if current_value
        else None
    )

    warnings = []

    if (
        consumption is None
        and previous is not None
        and current is not None
        and current >= previous
    ):
        consumption = current - previous
        warnings.append(
            "Consumption was calculated from the detected meter readings."
        )

    billing_month = _parse_month(normalized)

    if billing_month is None and table_header_match:
        year, month = re.split(
            r"[-/]",
            table_header_match.group(2),
        )
        try:
            billing_month = date(
                int(year),
                int(month),
                1,
            )
        except ValueError:
            billing_month = None

    fields = {
        "provider": provider,
        "account number": account_number,
        "billing month": billing_month,
        "consumption": consumption,
        "bill amount": amount,
    }

    for label, value in fields.items():
        if value is None:
            warnings.append(
                f"Could not confidently identify the {label}."
            )

    if billing_month is None and consumption is None and amount is None:
        raise BillExtractionError(
            "The document does not look like a supported electricity bill."
        )

    weights = {
        "provider": 0.10,
        "account number": 0.05,
        "billing month": 0.30,
        "consumption": 0.35,
        "bill amount": 0.20,
    }
    confidence_score = round(
        sum(
            weights[label]
            for label, value in fields.items()
            if value is not None
        ),
        2,
    )

    if confidence_score >= 0.80:
        confidence = "high"
    elif confidence_score >= 0.50:
        confidence = "medium"
    else:
        confidence = "low"

    return BillExtractionResponse(
        filename=filename,
        provider=provider,
        account_number=account_number,
        billing_month=billing_month,
        consumption_kwh=consumption,
        bill_amount_lkr=amount,
        previous_meter_reading=previous,
        current_meter_reading=current,
        confidence=confidence,
        confidence_score=confidence_score,
        warnings=warnings,
    )


def extract_bill_document(
    content: bytes,
    filename: str,
    content_type: str | None,
) -> BillExtractionResponse:
    text = extract_text_from_bill(
        content,
        content_type,
    )
    return extract_bill_data(
        text,
        filename,
    )
